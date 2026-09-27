"""Lord Seals, XP and the free path for design-forge (lords.md sections 4, 6, 10, 11).

    python seal_path.py                          # full report: costs, Summons, XP, supply, paths, pool
    python seal_path.py --only summons           # one section: costs|summons|xp|supply|path|pool
    python seal_path.py --mc 200000 --seed 1     # Monte Carlo of the Summons: served odds, pity bound
    python seal_path.py --paths-mc 400 --seed 1  # sampled Summons in the free path: median and p90 days
    python seal_path.py --paid-seals 35 --paid-xp 5040   # the heavy profile's weekly paid lord goods

Every number below is a PROPOSAL of lords.md; change it there and here in the same edit.

Seals    10 swear a lord (a duplicate lord = 10 Seals); rank-ups 20 / 40 / 70; each of the three
         skills costs 4 / 8 / 12 / 16 for its levels 2..5. A lord is COMPLETE at a rank when the
         rank and all three skills are at that rank's cap: 22 / 66 / 142 / 260 Seals.
Summons  1 free draw a day. 1 / 2 / 5 / 10 Seals at 55 / 25 / 15 / 5 %. A result goes to the
         Favoured lord with 50 % chance, else to one of the other 7 at random. Hard pity: the 20th
         draw since the last 10-Seal result IS a 10-Seal result for the Favoured lord.
XP       1 XP = 1 minute of standard play. Level L -> L+1 costs row L of curve.py
         (--levels 49 --first 3m --last 7d --shape phased). Level caps by rank: 20 / 30 / 40 / 50.
Path     expected-value, day-by-day model of the ENGAGED free player (about 3 check-ins a day,
         liveops.md section 0): every chooseable Seal goes to one focus lord until it is complete,
         then to the next lord in swear order. Day 0 = the install day; "day N" = end of day N.
Pool     the main march's pair (the first lord primary, the second lord secondary) in E-points
         (combat.md section 1: % extra troops the other side needs for a draw), additive inside the
         pool, clamped by the primary's rank ceiling; TS = ln(1 + E/100) / ln r.

Deterministic: no clock and no unseeded randomness; the same inputs print the same bytes.
Plain Python 3, standard library only (plus curve.py beside this file).
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curve import curve  # noqa: E402

# ---------------------------------------------------------------- Seals (lords.md section 10)
SWEAR = 10
RANK_UP = [20, 40, 70]            # Issued->Sound, Sound->Fine, Fine->Masterwork
SKILL_COST = [4, 8, 12, 16]       # one skill, level 2, 3, 4, 5
N_SKILLS = 3                      # Order, Passive I, Passive II (the Oath costs 0)
RANKS = ["Issued", "Sound", "Fine", "Masterwork"]


def spend_steps():
    """The spend order of a complete lord: swear, skills to 2, Sound, skills to 3, ..."""
    steps = [("swear", SWEAR), ("skills", N_SKILLS * SKILL_COST[0])]
    for i, cost in enumerate(RANK_UP):
        steps += [("rank", cost), ("skills", N_SKILLS * SKILL_COST[i + 1])]
    return steps


def thresholds():
    """Cumulative Seals: (rank reached [4], rank complete [4])."""
    reached, complete, cum, rank = [], [], 0, -1
    for kind, cost in spend_steps():
        cum += cost
        if kind in ("swear", "rank"):
            rank += 1
            reached.append(cum)
        else:
            complete.append(cum)
    return reached, complete


RANK_REACHED, RANK_COMPLETE = thresholds()      # [10, 42, 106, 212], [22, 66, 142, 260]
FULL = RANK_COMPLETE[-1]


def lord_state(seals):
    """(rank index -1..3, skill level 0..5) after spending `seals` in the spend order."""
    rank, skill, left = -1, 0, seals + 1e-9
    for kind, cost in spend_steps():
        if left < cost:
            break
        left -= cost
        if kind == "swear":
            rank, skill = 0, 1
        elif kind == "rank":
            rank += 1
        else:
            skill += 1
    return rank, skill


# ---------------------------------------------------------------- the Herald's Summons
ODDS = [(1, 0.55), (2, 0.25), (5, 0.15), (10, 0.05)]
PITY = 20
FAVOURED_SHARE = 0.5
OTHER_LORDS = 7


def summons_math(odds=ODDS, pity=PITY, fav=FAVOURED_SHARE, others=OTHER_LORDS):
    """Closed-form published math (renewal-reward over one pity cycle)."""
    p10 = dict((s, p) for s, p in odds)[10]
    q = 1.0 - p10
    draws_per_10 = sum(q ** k for k in range(pity))          # E[cycle length], capped at `pity`
    small = sum(s * p for s, p in odds if s != 10) / q       # mean of a non-10 result
    forced = q ** (pity - 1)                                 # share of cycles ended by pity
    ev = ((draws_per_10 - 1) * small + 10) / draws_per_10
    favoured = ((draws_per_10 - 1) * small * fav + 10 * (forced + (1 - forced) * fav)) / draws_per_10
    return {
        "ev_no_pity": sum(s * p for s, p in odds),
        "ev": ev,
        "draws_per_10": draws_per_10,
        "rate_10": 1.0 / draws_per_10,
        "forced_share": forced,
        "natural_within_19": 1 - forced,
        "favoured": favoured,
        "other_each": (ev - favoured) / others,
    }


def summons_math_markov(odds=ODDS, pity=PITY):
    """Independent check: stationary distribution of the pity counter (0..pity-1)."""
    p10 = dict((s, p) for s, p in odds)[10]
    q = 1.0 - p10
    weights = [q ** c for c in range(pity)]                  # P(counter reaches c) per cycle
    total = sum(weights)
    pi = [w / total for w in weights]
    small_ev = sum(s * p for s, p in odds if s != 10)
    ev = sum(pi[c] * (10.0 if c == pity - 1 else small_ev + p10 * 10) for c in range(pity))
    return ev


class Summons:
    """One player's draw stream, with the hard pity counter (the rule served by the server)."""

    def __init__(self, rng, odds=ODDS, pity=PITY, fav=FAVOURED_SHARE, others=OTHER_LORDS):
        self.rng, self.odds, self.pity, self.fav, self.others = rng, odds, pity, fav, others
        self.since_10 = 0            # draws since the last 10-Seal result

    def draw(self):
        """-> (seals, target): target 0 = the Favoured lord, 1..others = one of the other lords."""
        self.since_10 += 1
        if self.since_10 >= self.pity:
            self.since_10 = 0
            return 10, 0
        x, acc, seals = self.rng.random(), 0.0, self.odds[-1][0]
        for s, p in self.odds:
            acc += p
            if x < acc:
                seals = s
                break
        if seals == 10:
            self.since_10 = 0
        target = 0 if self.rng.random() < self.fav else 1 + self.rng.randrange(self.others)
        return seals, target


def summons_mc(n, seed):
    rng, s = random.Random(seed), None
    s = Summons(rng)
    gaps, gap, total, fav, tens, forced, counts = [], 0, 0, 0, 0, 0, {1: 0, 2: 0, 5: 0, 10: 0}
    for _ in range(n):
        before = s.since_10
        seals, target = s.draw()
        gap += 1
        total += seals
        fav += seals if target == 0 else 0
        counts[seals] += 1
        if seals == 10:
            tens += 1
            forced += 1 if before == PITY - 1 else 0
            gaps.append(gap)
            gap = 0
    return {"draws": n, "max_gap": max(gaps) if gaps else 0, "seals_per_draw": total / n,
            "favoured_per_draw": fav / n, "draws_per_10": n / max(tens, 1),
            "forced_share": forced / max(tens, 1),
            "served": dict((k, v / n) for k, v in counts.items())}


# ---------------------------------------------------------------- XP (lords.md section 4)
LEVEL_CAP = [20, 30, 40, 50]
XP_STEPS = [round(t / 60) for t in curve(49, 180, 7 * 86400, "phased")]   # XP for L -> L+1
XP_TO = [0, 0]                                                            # XP_TO[L] = XP to reach L
for _x in XP_STEPS:
    XP_TO.append(XP_TO[-1] + _x)
MAX_LEVEL = 50
CAMP_XP = 60               # per camp kill at or above the recommended level, to EACH lord in the march
CHEST_XP = 240             # the daily 100-point chest (PROPOSAL to core-loop.md section 7)


def camps(day):
    """Camp kills a day: the Resolve ramp of a newcomer, then 240 Resolve / 10 per kill."""
    return 10 if day <= 1 else (20 if day <= 7 else 24)


def level_of(xp):
    lvl = 1
    while lvl < MAX_LEVEL and XP_TO[lvl + 1] <= xp + 1e-9:
        lvl += 1
    return lvl


def talent_points(level):
    """1 per level 2..20, then 1 per even level 22..50 -> 34."""
    return min(max(level - 1, 0), 19) + (max(0, (level - 20) // 2) if level > 20 else 0)


def stat_steps(level):
    """Odd levels 21..49 each give a stat step -> 15."""
    return len([x for x in range(21, level + 1, 2)])


# ---------------------------------------------------------------- supply (lords.md section 11)
CAMPAIGN = 35                                   # liveops.md section 3.1: 1 Truce + 4 contest weeks
TRACK_FREE_TOP = 2500                           # liveops.md section 3.1
TRACK_POINTS_DAY = 100                          # core-loop.md section 7
NEW_REALM_WEEK = {1: 5, 2: 5, 4: 5, 5: 15}      # onboarding.md section 6 chapters 2,3,5,6,7 (20..120 h)
WRIT_PLAIN_WEEK, WRIT_FROM = 5, 7
STORE_PLAIN_WEEK, STORE_FROM = 5, 4             # alliance.md section 4, the Quartermaster
LABOURS_FEATURED, LABOURS_PLAIN, LABOURS_PER_CAMPAIGN, LABOURS_FROM = 12, 6, 4, 7
TRACK_PLAIN_CAMPAIGN = 40
HUNT_LADDER_KILLS = 150                         # the third starter swears at this camp kill


def day_reaching(total, per_day):
    cum, d = 0, 0
    while True:
        cum += per_day(d)
        if cum >= total:
            return d
        d += 1


LORDS = ["Edwin", "Elena", "Maud", "Rowan", "Godric", "Faber", "Alric", "Fable"]   # model swear order
CHANNELS = [   # (lord, free channel, activity, day of the median engaged free player)
    ("Edwin", "the identity pick (onboarding.md section 3)", "first session", 0),
    ("Elena", "chapter 4 of the founding week (onboarding.md section 6)", "first week", 4),
    ("Maud", "3 days in one alliance + 30 helps given", "alliance", 7),
    ("Rowan", "the %dth camp kill (hunt ladder)" % HUNT_LADDER_KILLS, "PvE",
     day_reaching(HUNT_LADDER_KILLS, camps)),
    ("Godric", "the arsenal built (progression.md, crossbows)", "castle", 9),
    ("Faber", "the first 4 set pieces crafted at the smithy", "crafting", 10),
    ("Alric", "the first AI-lord host defeated", "PvE, realm", 15),
    ("Fable", "the chronicle's free top, %d points counted across seasons" % TRACK_FREE_TOP,
     "campaign, time", day_reaching(TRACK_FREE_TOP, lambda d: TRACK_POINTS_DAY)),
]
CHANNEL_DAY = dict((c[0], c[3]) for c in CHANNELS)


def supply_rows(summ):
    """Steady-state free Seal supply (from day 8): (name, per day, per campaign, goes to, chooseable)."""
    lab_total = (LABOURS_FEATURED + LABOURS_PLAIN) * LABOURS_PER_CAMPAIGN
    return [
        ("Herald's Summons, 1 free draw a day", summ["ev"], summ["ev"] * CAMPAIGN,
         "%.2f Favoured, %.2f each other" % (summ["favoured"], summ["other_each"]), summ["favoured"]),
        ("Hunt tally, 1 per 10 camp kills led", camps(8) / 10.0, camps(8) / 10.0 * CAMPAIGN,
         "the leading lord", camps(8) / 10.0),
        ("Weekly writ 500 chest, 5 Plain", WRIT_PLAIN_WEEK / 7.0, WRIT_PLAIN_WEEK / 7.0 * CAMPAIGN,
         "any", WRIT_PLAIN_WEEK / 7.0),
        ("Alliance store, 5 Plain a week", STORE_PLAIN_WEEK / 7.0, STORE_PLAIN_WEEK / 7.0 * CAMPAIGN,
         "any", STORE_PLAIN_WEEK / 7.0),
        ("Labours Lords stage, 4 a campaign, 12 featured + 6 Plain", lab_total / float(CAMPAIGN),
         lab_total, "featured / any", LABOURS_PLAIN * LABOURS_PER_CAMPAIGN / float(CAMPAIGN)),
        ("Season track free, 40 Plain a campaign", TRACK_PLAIN_CAMPAIGN / float(CAMPAIGN),
         TRACK_PLAIN_CAMPAIGN, "any", TRACK_PLAIN_CAMPAIGN / float(CAMPAIGN)),
    ]


# ---------------------------------------------------------------- lord pool (lords.md section 6)
ALPHA, R_DRAW = 0.6, 1.40        # combat.md section 1 PROPOSALS (measured by the combat probe)
POOL_CAP_E = 30.0                # combat.md section 5: 0.78 TS
RANK_CEILING_E = [3.0, 6.0, 14.0, 30.0]
STEP_E = 0.1                     # per odd-level stat step (+0.08 % damage and +0.08 % defence)
TALENT_E = 5.0                   # 34 points, combat nodes only
SKILL_E = {"order": 4.5, "p1": 2.0, "p2": 1.5, "oath": 1.0}
SECONDARY_E = {"order": 1.5, "p1": 2.0}      # one cast on the half-rate drum; its Passive I
SKILL_VALUE = [0.0, 0.20, 0.35, 0.50, 0.70, 1.00]
PIECE_E = [0.25, 0.75, 1.25, 2.25]           # per piece by finish Issued..Masterwork
SET_E = {2: 1.0, 4: 1.0}                     # 2-piece and 4-piece bonuses
GEAR_DAYS = [(3, 5, 30, 60), (7, 9, 34, 70), (9, 12, 38, 80), (10, 14, 42, 90)]   # free = heavy
COMBAT_FREE = {7: 0.20, 30: 0.60, 90: 0.93, 180: 1.03}   # combat.md section 5 stack targets
COMBAT_HEAVY = {7: 0.45, 30: 0.88, 90: 1.03, 180: 1.08}
REALM_CAP_TS = 0.30


def e_of_mult(m, alpha=ALPHA):
    """E-points of a strength multiplier q x m (attack x HP): troops needed scale as m^(1/(1+a))."""
    return 100.0 * (m ** (1.0 / (1.0 + alpha)) - 1.0)


def ts_of_e(e, r=R_DRAW):
    return math.log(1.0 + e / 100.0) / math.log(r)


def order_e(round_share=0.6, casts=3, r_med=24):
    """An Order worth `round_share` of one normal round, cast `casts` times in r_med rounds."""
    return e_of_mult(1.0 + round_share * casts / float(r_med))


def gear_e(day):
    pieces, e = 0, 0.0
    for days in GEAR_DAYS:
        finish = sum(1 for d in days if day >= d) - 1
        if finish >= 0:
            pieces += 1
            e += PIECE_E[finish]
    return e + sum(v for n, v in SET_E.items() if pieces >= n)


def pool_e(level, rank, skill, sec_skill, day):
    if rank < 0:
        return 0.0, 0.0
    v = SKILL_VALUE[skill]
    e = stat_steps(level) * STEP_E + TALENT_E * talent_points(level) / 34.0
    e += v * (SKILL_E["order"] + SKILL_E["p1"] + SKILL_E["p2"])
    e += SKILL_E["oath"] if (rank == 3 and skill == 5) else 0.0
    e += gear_e(day)
    e += SKILL_VALUE[sec_skill] * (SECONDARY_E["order"] + SECONDARY_E["p1"])
    return min(e, RANK_CEILING_E[rank], POOL_CAP_E), e


def pool_budget():
    return [
        ("Primary level steps: 15 odd levels 21-49 x %.1f" % STEP_E, 15 * STEP_E),
        ("Primary talents: 34 points, combat nodes", TALENT_E),
        ("Primary gear: 4 Masterwork pieces x %.2f + set 2-piece %.0f + 4-piece %.0f"
         % (PIECE_E[3], SET_E[2], SET_E[4]), 4 * PIECE_E[3] + SET_E[2] + SET_E[4]),
        ("Primary skills: Order %.1f, Passive I %.1f, Passive II %.1f, Oath %.1f"
         % (SKILL_E["order"], SKILL_E["p1"], SKILL_E["p2"], SKILL_E["oath"]), sum(SKILL_E.values())),
        ("Secondary: Order %.1f (one cast), Passive I %.1f" % (SECONDARY_E["order"], SECONDARY_E["p1"]),
         sum(SECONDARY_E.values())),
    ]


# ---------------------------------------------------------------- the path model
PROFILES = {"free": (0, 0), "heavy": (35, 5040)}   # paid Seals and paid XP per week (lords.md 17 #2)


def run_path(paid_seals_week=0, paid_xp_week=0, days=400, rng=None, stop_all=True):
    """Day-by-day path. rng=None -> expected values; rng -> sampled Summons (pity served)."""
    summ = summons_math()
    n = len(LORDS)
    seals = [0.0] * n
    received, bank = 0.0, 0.0
    sworn = [None] * n
    reached = [[None] * 4 for _ in range(n)]
    complete = [[None] * 4 for _ in range(n)]
    xp, lvl_day = [0.0, 0.0], [dict(), dict()]
    first_complete = all_complete = None
    snaps = {}
    stream = Summons(rng) if rng else None
    for d in range(days + 1):
        focus = next((i for i in range(n) if seals[i] < FULL - 1e-9), None)
        add = [0.0] * n

        def to_focus(x):
            if focus is None:
                return x
            add[focus] += x
            return 0.0
        spill = 0.0
        # channels: the lord itself, or 10 of its Seals if already sworn
        for i, lord in enumerate(LORDS):
            if CHANNEL_DAY[lord] == d:
                add[i] += SWEAR
        # the Herald's Summons (the Favoured lord = the focus)
        others = [i for i in range(n) if i != focus] if focus is not None else list(range(1, n))
        if stream is None:
            spill += to_focus(summ["favoured"])
            for i in others[:OTHER_LORDS]:
                add[i] += summ["other_each"]
        else:
            s, target = stream.draw()
            if target == 0:
                spill += to_focus(s)
            else:
                add[others[(target - 1) % len(others)]] += s
        # chooseable income
        plain = camps(d) / 10.0 + NEW_REALM_WEEK.get(d, 0) + TRACK_PLAIN_CAMPAIGN / float(CAMPAIGN)
        plain += WRIT_PLAIN_WEEK / 7.0 if d >= WRIT_FROM else 0.0
        plain += STORE_PLAIN_WEEK / 7.0 if d >= STORE_FROM else 0.0
        plain += LABOURS_PLAIN * LABOURS_PER_CAMPAIGN / float(CAMPAIGN) if d >= LABOURS_FROM else 0.0
        plain += paid_seals_week / 7.0
        spill += to_focus(plain)
        if d >= LABOURS_FROM:   # featured lord rotates weekly through the eight, in swear order
            add[(d // 7) % n] += LABOURS_FEATURED * LABOURS_PER_CAMPAIGN / float(CAMPAIGN)
        received += sum(add) + spill
        bank += spill
        for i in range(n):
            seals[i] += add[i]
        # a complete lord's Seals turn into Plain Seals: to the next incomplete lord, else the bank
        for i in range(n):
            while seals[i] > FULL + 1e-9:
                extra = seals[i] - FULL
                seals[i] = float(FULL)
                nxt = next((j for j in range(n) if seals[j] < FULL - 1e-9), None)
                if nxt is None:
                    bank += extra
                else:
                    seals[nxt] += extra
        for i in range(n):
            if sworn[i] is None and seals[i] >= SWEAR - 1e-9:
                sworn[i] = d
            for k in range(4):
                if reached[i][k] is None and seals[i] >= RANK_REACHED[k] - 1e-9:
                    reached[i][k] = d
                if complete[i][k] is None and seals[i] >= RANK_COMPLETE[k] - 1e-9:
                    complete[i][k] = d
        # XP: march XP to the primary (lord 0) and the secondary (lord 1, once sworn);
        # the chest and paid tomes go to the XP focus (lord 0 until level 50, then lord 1)
        xp_focus = 0 if xp[0] < XP_TO[MAX_LEVEL] else 1
        xp[0] += camps(d) * CAMP_XP
        if sworn[1] is not None:
            xp[1] += camps(d) * CAMP_XP
        if xp_focus == 0 or sworn[1] is not None:
            xp[xp_focus] += CHEST_XP + paid_xp_week / 7.0
        states = [lord_state(seals[i]) for i in range(n)]
        levels = []
        for i in (0, 1):
            rank = states[i][0]
            lvl = min(level_of(xp[i]), LEVEL_CAP[rank]) if rank >= 0 else 1
            levels.append(lvl)
            for mark in (20, 30, 40, 50):
                if lvl >= mark and mark not in lvl_day[i]:
                    lvl_day[i][mark] = d
        n_complete = sum(1 for i in range(n) if seals[i] >= FULL - 1e-9)
        if first_complete is None and n_complete >= 1:
            first_complete = d
        if all_complete is None and n_complete == n:
            all_complete = d
        pool, raw = pool_e(levels[0], states[0][0], states[0][1],
                           states[1][1] if sworn[1] is not None else 0, d)
        snaps[d] = {"sworn": sum(1 for x in sworn if x is not None), "focus": focus,
                    "state0": states[0], "level0": levels[0], "xp_level0": level_of(xp[0]),
                    "complete": n_complete, "received": received, "pool_e": pool, "raw_e": raw,
                    "seals0": seals[0]}
        if stop_all and all_complete is not None and d >= 180:
            break
    held = sum(seals)
    return {"sworn": sworn, "reached": reached, "complete": complete, "lvl_day": lvl_day,
            "first_complete": first_complete, "all_complete": all_complete, "snaps": snaps,
            "waste": received - held - bank, "received": received, "bank": bank}


def heavy_ratios(free, heavy):
    pairs = [("first lord complete (Seals)", free["first_complete"], heavy["first_complete"]),
             ("first lord level 50 (XP)", free["lvl_day"][0][50], heavy["lvl_day"][0][50]),
             ("all 8 complete (the hall)", free["all_complete"], heavy["all_complete"])]
    return [(name, f, h, f / float(max(h, 1))) for name, f, h in pairs]


# ---------------------------------------------------------------- report
def p(line=""):
    print(line)


def fmt_day(x):
    return "-" if x is None else str(x)


def report_costs():
    p("== COSTS (Seals)")
    p("  swear %d; rank-ups %s; skill levels 2-5 cost %s each, x%d skills; the Oath costs 0"
      % (SWEAR, " / ".join(map(str, RANK_UP)), " / ".join(map(str, SKILL_COST)), N_SKILLS))
    p("  %-11s %8s %10s" % ("rank", "reached", "complete"))
    for k in range(4):
        p("  %-11s %8d %10d" % (RANKS[k], RANK_REACHED[k], RANK_COMPLETE[k]))
    p("  skills share of %d: %d" % (FULL, N_SKILLS * sum(SKILL_COST)))
    p()


def report_summons(mc=0, seed=1):
    m = summons_math()
    p("== SUMMONS (published math)")
    p("  odds: " + ", ".join("%d Seal%s %d%%" % (s, "" if s == 1 else "s", round(pr * 100)) for s, pr in ODDS))
    p("  Seals per draw without pity  %.2f" % m["ev_no_pity"])
    p("  Seals per draw with pity %d   %.2f   (Markov check %.3f)" % (PITY, m["ev"], summons_math_markov()))
    p("  draws per 10-Seal result     %.2f average, never more than %d" % (m["draws_per_10"], PITY))
    p("  10-Seal results forced by pity %.1f%%; a natural 10 within 19 draws %.1f%%"
      % (100 * m["forced_share"], 100 * m["natural_within_19"]))
    p("  Favoured lord %.2f per draw; each other lord %.2f per draw" % (m["favoured"], m["other_each"]))
    p("  per %d-day campaign (1 free draw a day): %.1f Seals, %.2f ten-results on average, >= %d by pity"
      % (CAMPAIGN, CAMPAIGN * m["ev"], CAMPAIGN / m["draws_per_10"], CAMPAIGN // PITY))
    if mc:
        r = summons_mc(mc, seed)
        p("  MONTE CARLO %d draws, seed %d: max gap %d (<= %d), %.3f Seals/draw, %.2f draws per 10,"
          " forced %.1f%%, Favoured %.3f/draw" % (r["draws"], seed, r["max_gap"], PITY, r["seals_per_draw"],
                                                   r["draws_per_10"], 100 * r["forced_share"],
                                                   r["favoured_per_draw"]))
        p("  served odds: " + ", ".join("%d: %.2f%%" % (k, 100 * v) for k, v in sorted(r["served"].items())))
    p()


def report_xp():
    p("== XP (1 XP = 1 minute; curve.py --levels 49 --first 3m --last 7d --shape phased)")
    p("  focus lord per day: camps x %d + %d chest = %d at 24 camps (ramp: 10 camps days 0-1, 20 days 2-7)"
      % (CAMP_XP, CHEST_XP, 24 * CAMP_XP + CHEST_XP))
    p("  %5s %8s %11s %7s  %s" % ("level", "step", "cumulative", "points", "note"))
    notes = {20: "Issued cap", 30: "Sound cap", 40: "Fine cap", 50: "Masterwork cap"}
    for lvl in (2, 10, 20, 30, 40, 45, 50):
        p("  %5d %8s %11s %7d  %s" % (lvl, "{:,}".format(XP_STEPS[lvl - 2]), "{:,}".format(XP_TO[lvl]),
                                      talent_points(lvl), notes.get(lvl, "")))
    p("  talent points at 50: %d; stat steps at 50: %d" % (talent_points(50), stat_steps(50)))
    p()


def report_supply():
    m = summons_math()
    rows = supply_rows(m)
    p("== SUPPLY (free Seals, steady state from day 8; one campaign = %d days)" % CAMPAIGN)
    p("  %-56s %7s %9s %8s  %s" % ("source", "per day", "campaign", "choose", "goes to"))
    for name, day, camp, to, ch in rows:
        p("  %-56s %7.2f %9.1f %8.2f  %s" % (name, day, camp, ch, to))
    tot = sum(r[1] for r in rows)
    ch = sum(r[4] for r in rows)
    p("  %-56s %7.2f %9.1f %8.2f" % ("FREE TOTAL", tot, tot * CAMPAIGN, ch))
    p("  new-realm week (by account age, days 1-5): %d Plain; heavy only if paid Seals: +%.2f a day"
      % (sum(NEW_REALM_WEEK.values()), PROFILES["heavy"][0] / 7.0))
    p()


def report_path(free, heavy):
    p("== PATH (days; free = engaged free player; heavy = + %d paid Seals and %s XP a week, only if"
      " lords.md 17 #2 is accepted; gear is never sold)" % (PROFILES["heavy"][0], "{:,}".format(PROFILES["heavy"][1])))
    p("  sworn day   " + "  ".join("%s %s" % (LORDS[i], fmt_day(free["sworn"][i])) for i in range(len(LORDS))))
    p("  channels    " + "; ".join("%s: %s (%s)" % (c[0], c[1], c[2]) for c in CHANNELS))
    p("  %-18s %6s  %13s  %13s  %13s" % ("rank complete", "Seals", "first lord", "second lord", "last lord"))
    for k in range(4):
        p("  %-18s %6d  %6s / %-5s  %6s / %-5s  %6s / %-5s" % (
            RANKS[k], RANK_COMPLETE[k], fmt_day(free["complete"][0][k]), fmt_day(heavy["complete"][0][k]),
            fmt_day(free["complete"][1][k]), fmt_day(heavy["complete"][1][k]),
            fmt_day(free["complete"][-1][k]), fmt_day(heavy["complete"][-1][k])))
    p("  %-18s %6s  %6s / %-5s  %6s / %-5s   (first lord rank reached: Sound %s, Fine %s, Masterwork %s)" % (
        "level 50 (XP)", "-", fmt_day(free["lvl_day"][0].get(50)), fmt_day(heavy["lvl_day"][0].get(50)),
        fmt_day(free["lvl_day"][1].get(50)), fmt_day(heavy["lvl_day"][1].get(50)),
        fmt_day(free["reached"][0][1]), fmt_day(free["reached"][0][2]), fmt_day(free["reached"][0][3])))
    p("  first lord level 20 / 30 / 40: free %s / %s / %s; heavy %s / %s / %s" % tuple(
        fmt_day(r["lvl_day"][0].get(x)) for r in (free, heavy) for x in (20, 30, 40)))
    p("  first lord complete: free %s, heavy %s; all 8 complete (%d Seals): free %s, heavy %s" % (
        fmt_day(free["first_complete"]), fmt_day(heavy["first_complete"]), FULL * len(LORDS),
        fmt_day(free["all_complete"]), fmt_day(heavy["all_complete"])))
    for name, f, h, ratio in heavy_ratios(free, heavy):
        p("  heavy / free  %-30s %4s / %-4s = %.2fx" % (name, f, h, ratio))
    p("  checkpoints (free): day  sworn  focus-lord rank/skill  level (XP level)  complete  Seals received")
    for d in (1, 7, 30, 90, 180):
        s = free["snaps"].get(d)
        if s:
            r, k = s["state0"]
            p("    %4d  %5d  %-10s skill %d  %5d (%d)  %8d  %8.0f" % (
                d, s["sworn"], RANKS[r] if r >= 0 else "-", k, s["level0"], s["xp_level0"], s["complete"],
                s["received"]))
    p("  Seal waste: free %.6f, heavy %.6f (a complete lord's Seals flow to the next lord)" % (
        free["waste"], heavy["waste"]))
    p()


def report_pool(free, heavy):
    p("== POOL (E-points, combat.md: TS = ln(1+E/100)/ln %.2f; cap %.0f E = %.2f TS)"
      % (R_DRAW, POOL_CAP_E, ts_of_e(POOL_CAP_E)))
    for name, e in pool_budget():
        p("  %-78s %5.1f" % (name, e))
    p("  %-78s %5.1f" % ("MAXED PAIR", sum(e for _, e in pool_budget())))
    p("  rank ceilings E: " + ", ".join("%s %.0f (%.2f TS)" % (RANKS[k], RANK_CEILING_E[k], ts_of_e(RANK_CEILING_E[k]))
                                          for k in range(4)))
    p("  Order at L5 = 0.6 of a normal round, 3 casts in R_med 24 -> %.1f E; stat step +0.08%% dmg/def -> %.2f E"
      % (order_e(), e_of_mult(1.0008 / (1 - 0.0008))))
    p("  %4s %10s %10s %10s %13s %13s" % ("day", "free E", "free TS", "heavy TS", "combat free", "left: realm"))
    for d in sorted(COMBAT_FREE):
        f, h = free["snaps"][d], heavy["snaps"][d]
        ft, ht = ts_of_e(f["pool_e"]), ts_of_e(h["pool_e"])
        p("  %4d %10.1f %10.2f %10.2f %13.2f %13.2f" % (d, f["pool_e"], ft, ht, COMBAT_FREE[d],
                                                         COMBAT_FREE[d] - round(ft, 2)))
    p()


def verdict(free, heavy, mc_gap=None):
    faults = []
    ratios = heavy_ratios(free, heavy)
    worst = max(r[3] for r in ratios)
    if worst > 2.0:
        faults.append("heavy/free %.2f > 2.0" % worst)
    if max(x for x in free["sworn"]) > 28:
        faults.append("all 8 sworn after day 28")
    if free["first_complete"] > 35:
        faults.append("first lord complete after day 35")
    if not 45 <= free["lvl_day"][0][50] <= 70:
        faults.append("free L50 outside days 45-70")
    if free["all_complete"] > 240:
        faults.append("all 8 complete after day 240")
    if abs(free["waste"]) > 1e-6 or abs(heavy["waste"]) > 1e-6:
        faults.append("Seals wasted")
    if abs(sum(e for _, e in pool_budget()) - POOL_CAP_E) > 1e-9:
        faults.append("pool budget != cap")
    for d, total in COMBAT_FREE.items():
        left = total - round(ts_of_e(free["snaps"][d]["pool_e"]), 2)
        if not 0 <= left <= REALM_CAP_TS + 1e-9:
            faults.append("day %d: realm share %.2f outside 0-%.2f" % (d, left, REALM_CAP_TS))
    for d in COMBAT_FREE:
        gap = ts_of_e(heavy["snaps"][d]["pool_e"]) - ts_of_e(free["snaps"][d]["pool_e"])
        if gap > 0.30:
            faults.append("day %d: heavy - free lord pool %.2f > 0.30 TS" % (d, gap))
    if mc_gap is not None and mc_gap > PITY:
        faults.append("pity exceeded")
    head = "SEAL PATH OK" if not faults else "SEAL PATH FAIL"
    tail = ("free: first lord complete day %d, L50 day %d, all 8 day %d; heavy/free max %.2f <= 2.0; "
            "waste 0; pity <= %d; maxed pair %.0f E = %.2f TS" % (
                free["first_complete"], free["lvl_day"][0][50], free["all_complete"], worst, PITY,
                POOL_CAP_E, ts_of_e(POOL_CAP_E)))
    return head + " - " + (tail if not faults else "; ".join(faults)), not faults


def paths_mc(k, seed):
    rng = random.Random(seed)
    firsts, alls = [], []
    for _ in range(k):
        r = run_path(rng=random.Random(rng.random()))
        firsts.append(r["first_complete"])
        alls.append(r["all_complete"])
    firsts.sort()
    alls.sort()

    def q(v, x):
        return v[min(len(v) - 1, int(x * len(v)))]
    p("== PATHS MONTE CARLO (%d sampled free paths, seed %d)" % (k, seed))
    p("  first lord complete: median %d, p90 %d, worst %d" % (q(firsts, 0.5), q(firsts, 0.9), firsts[-1]))
    p("  all 8 complete:      median %d, p90 %d, worst %d" % (q(alls, 0.5), q(alls, 0.9), alls[-1]))
    p()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", choices=["costs", "summons", "xp", "supply", "path", "pool"])
    ap.add_argument("--mc", type=int, default=0, help="Monte Carlo draws of the Summons")
    ap.add_argument("--paths-mc", type=int, default=0, help="sampled free paths")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--paid-seals", type=float, default=PROFILES["heavy"][0], help="heavy: paid Seals a week")
    ap.add_argument("--paid-xp", type=float, default=PROFILES["heavy"][1], help="heavy: paid lord XP a week")
    a = ap.parse_args(argv)
    PROFILES["heavy"] = (a.paid_seals, a.paid_xp)
    free = run_path(*PROFILES["free"])
    heavy = run_path(*PROFILES["heavy"])
    sections = {"costs": report_costs, "summons": lambda: report_summons(a.mc, a.seed), "xp": report_xp,
                "supply": report_supply, "path": lambda: report_path(free, heavy),
                "pool": lambda: report_pool(free, heavy)}
    for name in ("costs", "summons", "xp", "supply", "path", "pool"):
        if a.only in (None, name):
            sections[name]()
    if a.paths_mc:
        paths_mc(a.paths_mc, a.seed)
    gap = summons_mc(a.mc, a.seed)["max_gap"] if a.mc else None
    line, ok = verdict(free, heavy, gap)
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
