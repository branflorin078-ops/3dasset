"""Combat reference model for design-forge — tier-steps, counters, stacks, beds, walls.

    python tools/combat_model.py all                 # every table in references/combat.md + verdict
    python tools/combat_model.py units   [--alpha 0.6] [--r 1.40]
    python tools/combat_model.py counter [--alphas 0.5,0.6,0.7,0.8] [--rs 1.35,1.40,1.50]
    python tools/combat_model.py tiers   [--g 1.45]
    python tools/combat_model.py mix
    python tools/combat_model.py stack   [--lords 0.50] [--realm 0.50] [--temp 0.25] [--cap 1.25]
    python tools/combat_model.py losses  [--march 25000]
    python tools/combat_model.py beds    [--march 25000] [--beta 1.25]
    python tools/combat_model.py walls
    python tools/combat_model.py cost    [--players 50000]
    python tools/combat_model.py ts --mult 1.015 --mult 1.015 --ratio 2 --extra 30

This is the REFERENCE model behind references/combat.md, not the game's resolver.
The frozen resolver (gameplay-forge) wins; the combat probe (qa-forge) measures
its real alpha and r, and this tool then re-prints every table for those values.

The unit is the TIER-STEP (TS): the strength of one troop tier.
  strength S = q * N^(1+alpha)           (per round a side deals damage ~ q * N^alpha)
  r   = draw ratio: t(n) troops per t(n+1) troop, same line, no modifiers
  Q   = r^(1+alpha)                      quality step per tier (attack x HP per troop)
  TS of a q multiplier M = ln M / ln Q;  TS of a troop ratio x = ln x / ln r
  two-sided counter c: the hunter deals (1+c) and takes (1-c), so (1+c)/(1-c) = Q
The simulator (fight / draw_ratio) splits each side's damage by attacker weight x
target share x the pair's counter factor; losses = damage / HP. Pure Python,
no randomness: the same arguments always print the same numbers.

`all` ends with `COMBAT MODEL OK - ...` (exit 0) or `COMBAT MODEL FAIL - ...` (exit 1).
"""
import argparse
import math
import sys

# ---------------------------------------------------------------- constants
LINES = ("infantry", "spearmen", "archers", "crossbows", "cavalry")
# PROPOSAL counter ring (owner decision; may be a sacred constant): each hunts the next.
RING = ("spearmen", "cavalry", "crossbows", "archers", "infantry")
HUNTS = {RING[i]: RING[(i + 1) % len(RING)] for i in range(len(RING))}

ALPHA, R = 0.6, 1.40            # PROPOSALS; the probe measures the shipped values
G_COST = 1.45                   # training cost growth per tier (> r)
P1 = 10.0                       # power of a t1 troop

# stack pools (TS). Lords = lords.md §6 cap. Structures are defender-only, outside the cap.
POOLS = {"lords": 0.50, "realm": 0.50, "temporary": 0.25}
STRUCTURES = 0.50
CAP = 1.25
LEAD_MAX = 0.30                 # heavy - free, same day, main march
# stack targets, all non-counter pools, main march (free lords column = lords.md §6 timeline)
FREE = {7: 0.15, 30: 0.35, 90: 0.60, 180: 0.85}
FREE_LORDS = {7: 0.12, 30: 0.28, 90: 0.43, 180: 0.50}
HEAVY = {7: 0.35, 30: 0.60, 90: 0.85, 180: 1.05}
HEAVY_LORDS = {7: 0.21, 30: 0.39, 90: 0.48, 180: 0.50}   # lords.md: only if paid Seals exist

# loss rows: (context, light, severe, dead, beds-full rule)
LOSS_ROWS = [
    ("Camp hunt (PvE)", 90, 10, 0, "Light"),
    ("Rally on a stronghold or AI-lord hold (PvE)", 60, 40, 0, "Light"),
    ("Defending your own castle", 30, 70, 0, "Routed"),
    ("Reinforcing an ally; defending an alliance structure", 25, 60, 15, "Dead"),
    ("Field battle", 35, 55, 10, "Dead"),
    ("Attacking an alliance structure or landmark (war window)", 25, 50, 25, "Dead"),
    ("Attacking a castle in a war window", 20, 50, 30, "Dead"),
    ("Attacking a castle outside war windows", 10, 30, 60, "Dead"),
    ("Tourneys and trial grounds", 100, 0, 0, "-"),
]
NEVER_KILL = (0, 1, 2, 8)       # rows (0-based) where dead must be 0

# mixed-march matchups of combat.md §2 rule 6 (shares of the march)
EVEN = {k: 0.2 for k in LINES}
OURS = [
    ("even 5 x 20%", EVEN),
    ("spearmen 60%, others 10%", {"spearmen": .6, "infantry": .1, "archers": .1, "crossbows": .1, "cavalry": .1}),
    ("spearmen 100%", {"spearmen": 1.0}),
    ("cavalry 50, crossbows 30, infantry 20", {"cavalry": .5, "crossbows": .3, "infantry": .2}),
    ("cavalry 100%", {"cavalry": 1.0}),
]
ENEMIES = [
    ("even 5 x 20%", EVEN),
    ("cavalry 60%, others 10%", {"cavalry": .6, "infantry": .1, "spearmen": .1, "archers": .1, "crossbows": .1}),
    ("crossbows 40, archers 40, infantry 20", {"crossbows": .4, "archers": .4, "infantry": .2}),
]


# ---------------------------------------------------------------- unit math
def q_step(alpha=ALPHA, r=R):
    """Quality step per tier Q = r^(1+alpha)."""
    return r ** (1.0 + alpha)


def counter_c(alpha=ALPHA, r=R):
    """Two-sided counter worth exactly 1 TS: c = (Q-1)/(Q+1)."""
    q = q_step(alpha, r)
    return (q - 1.0) / (q + 1.0)


def one_sided_c(alpha=ALPHA, r=R):
    """A counter that only adds damage needs +(Q-1) for the same 1 TS."""
    return q_step(alpha, r) - 1.0


def ts_of_mult(m, alpha=ALPHA, r=R):
    return math.log(m) / math.log(q_step(alpha, r))


def ts_of_ratio(x, r=R):
    return math.log(x) / math.log(r)


def ts_of_extra(e_pct, r=R):
    """E = % extra troops the other side needs for a draw (mirror test)."""
    return ts_of_ratio(1.0 + e_pct / 100.0, r)


def extra_of_ts(ts, r=R):
    return (r ** ts - 1.0) * 100.0


def power(t, r=R, p1=P1):
    return p1 * r ** (t - 1)


def quality(t, alpha=ALPHA, r=R):
    return q_step(alpha, r) ** (t - 1)


def cost_per_power(t, g=G_COST, r=R):
    return (g / r) ** (t - 1)


def cf(i, j, c):
    """Damage factor of line i hitting line j."""
    if HUNTS[i] == j:
        return 1.0 + c
    if HUNTS[j] == i:
        return 1.0 - c
    return 1.0


def matchup_index(a, b):
    """MI = sum_i sum_j sA_i * sB_j * C_ij (C = +1 hunts, -1 hunted, 0 neutral)."""
    s = 0.0
    for i, si in a.items():
        for j, sj in b.items():
            if HUNTS[i] == j:
                s += si * sj
            elif HUNTS[j] == i:
                s -= si * sj
    return s


# ---------------------------------------------------------------- simulator
def fight(A, B, alpha=ALPHA, r=R, c=None, K=0.05, rounds=400, modA=1.0, modB=1.0, rout=0.0):
    """A, B: {line: (count, tier)}. Returns the surviving fraction of each side.

    Per round a side deals K * N^alpha * mean attack * mod, split by attacker weight
    (count x attack) x target share (count) x counter factor; losses = damage / HP.
    Attack = HP = sqrt(Q^(t-1)) per troop. Ends at `rounds`, or when a side falls to `rout`.
    """
    if c is None:
        c = counter_c(alpha, r)
    Q = q_step(alpha, r)
    sides = []
    for army in (A, B):
        rows = [[ln, float(n), math.sqrt(Q ** (t - 1))] for ln, (n, t) in sorted(army.items()) if n > 0]
        sides.append(rows)
    a, b = sides
    n0 = [sum(x[1] for x in a), sum(x[1] for x in b)]
    mods = (modA, modB)
    for _ in range(rounds):
        NA, NB = sum(x[1] for x in a), sum(x[1] for x in b)
        if NA <= n0[0] * rout or NB <= n0[1] * rout or NA <= 0 or NB <= 0:
            break
        dmg = ([0.0] * len(a), [0.0] * len(b))
        for s, (me, other, N, No) in enumerate(((a, b, NA, NB), (b, a, NB, NA))):
            w = sum(x[1] * x[2] for x in me)
            total = K * N ** alpha * (w / N) * mods[s]
            tgt = dmg[1 - s]
            for ln_i, n_i, at_i in me:
                di = total * n_i * at_i / w
                for k, (ln_j, n_j, _) in enumerate(other):
                    tgt[k] += di * (n_j / No) * cf(ln_i, ln_j, c)
        for k, x in enumerate(a):
            x[1] = max(0.0, x[1] - dmg[0][k] / x[2])
        for k, x in enumerate(b):
            x[1] = max(0.0, x[1] - dmg[1][k] / x[2])
    return sum(x[1] for x in a) / n0[0], sum(x[1] for x in b) / n0[1]


def draw_ratio(make_a, make_b, iters=40, lo=0.2, hi=5.0, **kw):
    """Count multiplier on A that makes both sides end with equal surviving fractions."""
    for _ in range(iters):
        m = (lo + hi) / 2.0
        fa, fb = fight(make_a(m), make_b(), **kw)
        if fa > fb:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2.0


def sim_ts(comp_a, comp_b, tier_a=5, tier_b=5, n=10000, r=R, **kw):
    """Strength margin of A over B in TS (> 0: A is stronger), equal troop counts."""
    x = draw_ratio(lambda m: {k: (n * v * m, tier_a) for k, v in comp_a.items() if v > 0},
                   lambda: {k: (n * v, tier_b) for k, v in comp_b.items() if v > 0}, r=r, **kw)
    return -ts_of_ratio(x, r)


# ---------------------------------------------------------------- sections
def pct(x):
    return "%+.0f%%" % (100 * x)


def cmd_units(a, out):
    Q = q_step(a.alpha, a.r)
    out("== units (alpha %.2f, r %.2f)" % (a.alpha, a.r))
    out("Q = r^(1+alpha) = %.2f; attack and HP x%.2f each" % (Q, math.sqrt(Q)))
    out("2x troops = %+.2f TS" % ts_of_ratio(2.0, a.r))
    out("E-point: 1 TS = %.1f E; 0.50 TS = %.1f E; 30 E = %.2f TS" % (
        extra_of_ts(1.0, a.r), extra_of_ts(0.5, a.r), ts_of_extra(30, a.r)))
    out("%5s %8s %16s %10s" % ("TS", "q mult", "attack / taken", "troops x"))
    for ts in (0.25, 0.5, 1.0, 2.0):
        m = Q ** ts
        s = math.sqrt(m)
        out("%5.2f %8.2f %7s / %-7s %10.2f" % (ts, m, pct(s - 1), pct(1 / s - 1), a.r ** ts))
    out("model check (reference simulator, t5 infantry): draw ratio vs t6 by end rule")
    for label, kw in (("to the end", {}), ("rout 50%", {"rout": 0.5}), ("12 rounds", {"rounds": 12})):
        x = draw_ratio(lambda m: {"infantry": (10000 * m, 5)}, lambda: {"infantry": (10000, 6)},
                       alpha=a.alpha, r=a.r, **kw)
        out("  %-10s r = %.3f" % (label, x))
    return {"Q": Q}


def cmd_counter(a, out):
    alphas = [float(x) for x in a.alphas.split(",")]
    rs = [float(x) for x in a.rs.split(",")]
    out("== counter c = (Q-1)/(Q+1), two-sided, worth 1.0 TS")
    out("alpha \\ r " + " ".join("%6.2f" % r for r in rs))
    lo, hi, lo1, hi1 = 9, 0, 9, 0
    for al in alphas:
        row = []
        for r in rs:
            c = counter_c(al, r)
            lo, hi = min(lo, c), max(hi, c)
            c1 = one_sided_c(al, r)
            lo1, hi1 = min(lo1, c1), max(hi1, c1)
            row.append("%5.0f%%" % (100 * c))
        out("%9.1f " % al + " ".join(row))
    out("band %.0f%%-%.0f%% (numbers.md: 20-50%%); one-sided equivalent %.0f%%-%.0f%%" % (
        100 * lo, 100 * hi, 100 * lo1, 100 * hi1))
    c = counter_c(ALPHA, R)
    out("ring (PROPOSAL): " + " -> ".join(RING + (RING[0],)))
    out("sim, c = %.3f: hunter t(n) vs prey t(n+1), equal count -> TS margin (0.00 = draw)" % c)
    res = []
    for h in RING:
        res.append((h, 5, sim_ts({h: 1.0}, {HUNTS[h]: 1.0}, 5, 6)))
    res.append(("spearmen", 10, sim_ts({"spearmen": 1.0}, {"cavalry": 1.0}, 10, 11)))
    for h, t, ts in res:
        out("  %-9s t%-2d vs %-9s t%-2d  %+.3f" % (h, t, HUNTS[h], t + 1, ts))
    two_up = sim_ts({"spearmen": 1.0}, {"cavalry": 1.0}, 5, 7)
    neutral = sim_ts({"infantry": 1.0}, {"cavalry": 1.0}, 5, 5)
    out("  spearmen t5 vs cavalry t7 (two tiers up) %+.3f; neutral infantry t5 vs cavalry t5 %+.3f" % (two_up, neutral))
    return {"c": c, "band": (lo, hi), "pairs": res, "two_up": two_up, "neutral": neutral}


def cmd_tiers(a, out):
    out("== tiers (p_t = %g * r^(t-1), Q = %.3f, training cost growth g = %.2f)" % (P1, q_step(), a.g))
    ts = range(1, 12)
    out("tier             " + " ".join("%6d" % t for t in ts))
    out("power per troop  " + " ".join("%6.0f" % power(t) for t in ts))
    out("quality q (xt1)  " + " ".join("%6s" % ("%.3g" % quality(t)) for t in ts))
    out("cost per power   " + " ".join("%6.2f" % cost_per_power(t, a.g) for t in ts))
    out("t10 / t1 power = %.1fx; cost per power +%.1f%% per tier; 2x troops = %+.2f TS" % (
        power(10) / power(1), 100 * (a.g / R - 1), ts_of_ratio(2.0)))
    return {"t10": power(10) / power(1)}


def cmd_mix(a, out):
    out("== mixed marches, t5, equal counts: sim TS (MI)")
    out("%-38s" % "ours \\ enemy" + "".join("%-40s" % e for e, _ in ENEMIES))
    worst_rel, worst_abs, cells = 0.0, 0.0, []
    for on, od in OURS:
        row = []
        for en, ed in ENEMIES:
            ts = sim_ts(od, ed)
            mi = matchup_index(od, ed)
            cells.append((on, en, ts, mi))
            if abs(mi) >= 0.1:
                worst_rel = max(worst_rel, abs(ts / mi - 1))
            else:
                worst_abs = max(worst_abs, abs(ts - mi))
            row.append("%-40s" % ("%+.2f (%+.2f)" % (ts, mi)))
        out("%-38s" % on + "".join(row))
    out("sim TS vs MI: within %.0f%% where |MI| >= 0.1; within %.2f TS where MI ~ 0" % (100 * worst_rel, worst_abs))
    return {"worst_rel": worst_rel, "worst_abs": worst_abs, "cells": cells}


def cmd_stack(a, out):
    pools = {"lords": a.lords, "realm": a.realm, "temporary": a.temp}
    Q = q_step()
    total = sum(pools.values())
    out("== stack pools (TS; additive inside a pool, multiplicative across pools)")
    out("%-22s %6s %10s" % ("pool", "max TS", "q x at max"))
    out("%-22s %6.2f %10.2f" % ("counter (own category)", 1.0, Q))
    for k, v in pools.items():
        out("%-22s %6.2f %10.2f" % (k, v, Q ** v))
    out("%-22s %6.2f %10.2f" % ("structures (defender)", STRUCTURES, Q ** STRUCTURES))
    out("%-22s %6.2f %10.2f   (cap %.2f)" % ("all non-counter pools", total, Q ** total, a.cap))
    i1a = 1.0 - pools["lords"]
    i1b = 1.0 - (a.cap - FREE[30])
    i1c = 1.0 - (a.cap - FREE[90])
    out("I1 counter beats stack: no lords vs a maxed pair %+.2f TS; free day-30 stack vs max stack %+.2f; day 90 %+.2f"
        % (i1a, i1b, i1c))
    out("I3 lords vs counter: lord pool = %.2f of one counter" % pools["lords"])
    out("%4s %6s %6s %6s %6s %6s" % ("day", "free", "lords", "heavy", "lords", "lead"))
    leads = {}
    ok_split = True
    for d in sorted(FREE):
        leads[d] = HEAVY[d] - FREE[d]
        ok_split &= FREE_LORDS[d] <= min(FREE[d], pools["lords"]) and HEAVY_LORDS[d] <= min(HEAVY[d], pools["lords"])
        ok_split &= HEAVY[d] - HEAVY_LORDS[d] <= pools["realm"] + pools["temporary"] + 1e-9
        out("%4d %6.2f %6.2f %6.2f %6.2f %+6.2f" % (d, FREE[d], FREE_LORDS[d], HEAVY[d], HEAVY_LORDS[d], leads[d]))
    lead = max(leads.values())
    out("I2 heavy lead max %.2f TS (limit %.2f)" % (lead, LEAD_MAX))
    return {"total": total, "i1": (i1a, i1b, i1c), "lead": lead, "split_ok": ok_split, "pools": pools}


def cmd_losses(a, out):
    out("== loss rows (light / severe / dead %, beds full ->)")
    bad = []
    for k, (ctx, li, se, de, full) in enumerate(LOSS_ROWS, 1):
        s = li + se + de
        out("%d %-58s %3d %3d %3d  %-6s sum %d" % (k, ctx, li, se, de, full, s))
        if s != 100:
            bad.append("row %d sums %d" % (k, s))
        if k - 1 in NEVER_KILL and de:
            bad.append("row %d kills" % k)
    _, li, se, de, _ = LOSS_ROWS[4]
    m = a.march
    out("worked, row 5, lost march of %d: %d walk home, %d to beds, %d dead" % (
        m, m * li // 100, m * se // 100, m * de // 100))
    out("war score weak-target factor at P_def/P_att 0.25 / 0.30 / 0.45 / 0.60 / 1.00: " + " / ".join(
        "%.2f" % weak_target(x) for x in (0.25, 0.30, 0.45, 0.60, 1.00)))
    out("pair decay 0.5^(n-1), fights 1..4: " + " / ".join("%.0f%%" % (100 * 0.5 ** (n - 1)) for n in range(1, 5)))
    return {"bad": bad}


def weak_target(ratio):
    return min(1.0, max(0.0, (ratio - 0.3) / 0.3))


def scout_level(e_scout, e_target):
    return min(5, max(1, 3 + e_scout - e_target))


def cmd_beds(a, out):
    m, beta = a.march, a.beta
    beds = beta * m
    field = LOSS_ROWS[4][2] / 100.0
    assault = LOSS_ROWS[6][2] / 100.0
    home = LOSS_ROWS[2][2] / 100.0
    cases = [("lost field march", field), ("two lost war-window castle assaults", 2 * assault),
             ("lost home defence, 1.25 marches at home", 1.25 * home)]
    worst = max(v for _, v in cases)
    out("== infirmary (C_march %d, beta %.2f)" % (m, beta))
    out("H1 beds = %.0f" % beds)
    for label, v in cases:
        out("H2 %-42s %.3f x C_march = %6.0f to beds" % (label, v, v * m))
    out("H2 worst normal day %.2f <= beta %.2f: %s" % (worst, beta, "fits" if worst <= beta else "OVERFLOW"))
    used = 2 * assault * m
    third = assault * m
    over = third - (beds - used)
    out("a third lost assault adds %.0f to %.0f free beds -> overflow warning ~%s" % (
        third, beds - used, "{:,}".format(int(round(over, -2)))))
    out("H3 heal time per top-tier troop <= 28,800 s / %.0f beds = %.2f s" % (beds, 28800.0 / beds))
    return {"worst": worst, "beds": beds, "over": over}


def cmd_walls(a, out):
    out("== Walls & Gate (%% of W_max)")
    won_no_engines, won_train, repair = 8.0, 30.0, 10.0
    out("won assaults to breach: no engines %d; standard train %d; standard train + 20%% lord structure damage %d" % (
        math.ceil(100 / won_no_engines), math.ceil(100 / won_train), math.ceil(100 / (won_train * 1.2))))
    w, log = 100.0, ["100"]
    for minute, kind in ((10, "won"), (11, "repair"), (15, "won"), (20, "won"), (25, "won")):
        w = min(100.0, w + repair) if kind == "repair" else max(0.0, w - won_train)
        log.append(("repair %.0f" if kind == "repair" else "%.0f") % w + " (min %d)" % minute)
    out("worked war window, rallies 5 min apart: " + " -> ".join(log))
    out("auto-repair 12.5%%/h: 0 -> 100 in %.0f h; 20%%/h (well tier 6): %.0f h" % (100 / 12.5, 100 / 20.0))
    return {"end": w, "no_engines": math.ceil(100 / won_no_engines)}


def cmd_cost(a, out):
    p = a.players
    pvp = 0.30 * 5 * 4 * p
    scouts = 2 * 2 * p
    resolutions = 24 * p + 0.30 * 5 * p + 2 * p
    out("== server cost at %d players (upper bound)" % p)
    out("PvP writes %.0f + scout writes %.0f = %.2f M writes/day (camp writes are in core-loop)" % (
        pvp, scouts, (pvp + scouts) / 1e6))
    out("resolutions/day %.2f M (camps 24 + PvP 1.5 + scouts 2 per player) x 2 ms = %.0f CPU-min/day" % (
        resolutions / 1e6, resolutions * 0.002 / 60))
    return {"writes": pvp + scouts, "cpu_min": resolutions * 0.002 / 60}


def cmd_ts(a, out):
    total = 0.0
    for m in a.mult or []:
        total += ts_of_mult(m)
        out("q x %.4f = %+.3f TS" % (m, ts_of_mult(m)))
    for x in a.ratio or []:
        total += ts_of_ratio(x)
        out("troops x %.3f = %+.3f TS" % (x, ts_of_ratio(x)))
    for e in a.extra or []:
        total += ts_of_extra(e)
        out("%.1f E (extra troops for a draw) = %+.3f TS" % (e, ts_of_extra(e)))
    out("sum %+.3f TS" % total)
    return {"sum": total}


def cmd_all(a, out):
    res = {}
    for name, fn in (("units", cmd_units), ("counter", cmd_counter), ("tiers", cmd_tiers), ("mix", cmd_mix),
                     ("stack", cmd_stack), ("losses", cmd_losses), ("beds", cmd_beds), ("walls", cmd_walls),
                     ("cost", cmd_cost)):
        res[name] = fn(a, out)
        out("")
    fails = []
    ctr = res["counter"]
    ok_pairs = sum(1 for _, _, ts in ctr["pairs"] if abs(ts) <= 0.01)
    if ok_pairs != len(ctr["pairs"]):
        fails.append("counter pairs off 1 TS")
    lo, hi = ctr["band"]
    if lo < 0.20 or hi > 0.50:
        fails.append("c outside 20-50%")
    if res["mix"]["worst_rel"] > 0.07 or res["mix"]["worst_abs"] > 0.03:
        fails.append("MI off sim")
    st = res["stack"]
    if abs(st["total"] - a.cap) > 0.005:
        fails.append("pools sum %.2f != cap %.2f" % (st["total"], a.cap))
    if min(st["i1"]) <= 0:
        fails.append("I1 counter does not beat stack")
    if st["lead"] > LEAD_MAX + 1e-9:
        fails.append("heavy lead %.2f > %.2f" % (st["lead"], LEAD_MAX))
    if not st["split_ok"]:
        fails.append("stack targets exceed a pool")
    fails += res["losses"]["bad"]
    if res["beds"]["worst"] > a.beta:
        fails.append("worst day overflows beds")
    if res["walls"]["end"] != 0:
        fails.append("worked war window does not breach")
    if fails:
        out("COMBAT MODEL FAIL - " + "; ".join(fails))
        return 1
    out("COMBAT MODEL OK - r %.2f, c %.1f%%, counter %d/%d at 1.00 TS, MI within %.0f%%, pools %.2f TS, "
        "I1 %+.2f, lead %.2f <= %.2f, worst day %.2f <= beds %.2f" % (
            a.r, 100 * ctr["c"], ok_pairs, len(ctr["pairs"]), 100 * res["mix"]["worst_rel"], st["total"],
            min(st["i1"]), st["lead"], LEAD_MAX, res["beds"]["worst"], a.beta))
    return 0


COMMANDS = {"all": cmd_all, "units": cmd_units, "counter": cmd_counter, "tiers": cmd_tiers, "mix": cmd_mix,
            "stack": cmd_stack, "losses": cmd_losses, "beds": cmd_beds, "walls": cmd_walls, "cost": cmd_cost,
            "ts": cmd_ts}


def main(argv=None, out=print):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=sorted(COMMANDS))
    ap.add_argument("--alpha", type=float, default=ALPHA)
    ap.add_argument("--r", type=float, default=R)
    ap.add_argument("--alphas", default="0.5,0.6,0.7,0.8")
    ap.add_argument("--rs", default="1.35,1.40,1.50")
    ap.add_argument("--g", type=float, default=G_COST)
    ap.add_argument("--lords", type=float, default=POOLS["lords"])
    ap.add_argument("--realm", type=float, default=POOLS["realm"])
    ap.add_argument("--temp", type=float, default=POOLS["temporary"])
    ap.add_argument("--cap", type=float, default=CAP)
    ap.add_argument("--march", type=int, default=25000)
    ap.add_argument("--beta", type=float, default=1.25)
    ap.add_argument("--players", type=int, default=50000)
    ap.add_argument("--mult", type=float, action="append")
    ap.add_argument("--ratio", type=float, action="append")
    ap.add_argument("--extra", type=float, action="append")
    a = ap.parse_args(argv)
    rc = COMMANDS[a.command](a, out)
    return rc if isinstance(rc, int) else 0


if __name__ == "__main__":
    sys.exit(main())
