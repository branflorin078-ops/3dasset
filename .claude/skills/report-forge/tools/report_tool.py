#!/usr/bin/env python3
"""report-forge reference tool: the oracle the Godot report builder must match.

  python report_tool.py explain FILE [--pov 0|1] [--json]   ranked causes + text
  python report_tool.py render  FILE [--pov 0|1]            the full report as text
  python report_tool.py size    FILE [FILE ...]             bytes: full, summary, gzip
  python report_tool.py check   FILE [FILE ...]             invariants (exit 1 on error)
  python report_tool.py cost    [--fixtures DIR] [--players N] [...]
  python report_tool.py golden  FIXTURE_DIR OUT_DIR         expected outputs for report_probe

Stdlib only (Python 3.8+). Thresholds and tables marked PROPOSAL come from
references/explain.md and design-forge combat.md; change them there first.
"""
import argparse
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "strings_en.json"), encoding="utf-8") as _f:
    STR = json.load(_f)

# ---- constants (explain.md section 3; PROPOSAL values) ---------------------
FACTORS = ("counter", "tier", "numbers", "lord", "stats", "defences", "siege", "other")
ACTION_ORDER = ("counter", "lord", "numbers", "tier", "defences", "siege", "stats")
T_SHOW = 50          # per mille of the battle: a cause below this is not shown
T_MAIN = 250         # "This was the main reason."
FLIP_SAFETY = 1.25   # |n| >= 1.25 * |margin| before we claim the result would flip
T_CLOSE = 100        # |margin| below this: "close"
T_BIG = 500          # |margin| at or above this: "crushing" / "heavy"
T_OTHER_WARN = 100   # untagged share that raises a QA flag
MAX_ROWS = 3         # cause rows shown before "Details"
MAX_SENTENCE = 64    # English characters per filled sentence (l10n room +40%)
CASUALTY_ENDS = {0, 1, 2, 5}
END_NAMES = {0: "annihilated", 1: "routed", 2: "withdrew", 3: "wall held",
             4: "gate broken", 5: "recalled"}
PLACE_CASTLE = 1
BATTLE_KINDS = (1, 2, 3)
LINE_MAX_TIER = (10, 10, 10, 10, 11)
# PROPOSAL counter graph (design-forge combat.md decides): line -> the line that counters it
COUNTERED_BY = {4: 1, 2: 4, 3: 4, 0: 2, 1: 0}
LORDS = ("Edwin", "Alric", "Elena", "Rowan", "Godric", "Maud", "Faber", "Fable")
# Placeholder skill names for fixtures only; lords.md / commander-forge own the real names.
EXAMPLE_SKILLS = {(0, 0): "Rally Cry", (1, 0): "Shock", (2, 0): "Volley", (3, 0): "Charge",
                  (4, 0): "Sapper Fire", (5, 0): "Shield Wall", (6, 0): "Temper",
                  (7, 0): "Chronicle"}
EXAMPLE_ENGINES = {0: "ladders", 1: "rams", 2: "trebuchets", 3: "mantlets"}  # siege-forge owns the catalogue
LINK_ALLOWED = {"train", "rally", "scout", "research", "siege", "wall", "infirmary", "replay"}
# Scout information tiers (scout.md section 2): fields allowed per tier, and rounded ones.
SCOUT_FIELDS = {0: {"ct", "pw", "wb"},
                1: {"ct", "pw", "wb", "wl", "rs", "tt", "tw"},
                2: {"ct", "pw", "wb", "wl", "rs", "tt", "tw", "tl", "l", "rf", "tr"},
                3: {"ct", "pw", "wb", "wl", "rs", "tt", "tw", "t", "l", "rf", "tr"},
                4: {"ct", "pw", "wb", "wl", "rs", "tt", "tw", "t", "l", "rf", "tr", "bo", "hf", "ma"}}
SCOUT_ROUNDED = {0: {"pw"}, 1: {"pw", "rs", "tt"}, 2: {"pw", "rs", "tt", "tl", "rf"}, 3: set(), 4: set()}


def s(key, **p):
    """Fill one string key. Numbers arrive pre-formatted."""
    return STR[key].format(**p)


def num(n):
    return f"{int(n):,}"


def pct(permille):
    """Per mille -> whole percent, half away from zero."""
    v = abs(permille) / 10.0
    r = int(math.floor(v + 0.5))
    return -r if permille < 0 else r


def line_name(i):
    return STR[f"troop.line.{i}"]


def sig2(n):
    """Round to 2 significant figures, half up (scout.md: deterministic, never noise)."""
    if n < 100:
        return int(n)
    e = int(math.floor(math.log10(n))) - 1
    q = 10 ** e
    return int(math.floor(n / q + 0.5)) * q


# ---- record access ----------------------------------------------------------
def rows(side):
    for u in side["u"]:
        for r in u.get("t", []):
            yield u, r


def sent(side):
    return sum(r[2] for _, r in rows(side))


def light(side):
    return sum(r[3] for _, r in rows(side))


def hosp(side):
    return sum(r[4] for _, r in rows(side))


def dead(side):
    return sum(r[5] for _, r in rows(side))


def out(side):
    return light(side) + hosp(side) + dead(side)


def healed(side):
    return sum(l[4] for u in side["u"] for l in u.get("l", []))


def dealt(side):
    total = sum(r[6] for _, r in rows(side))
    for u in side["u"]:
        total += sum(l[3] for l in u.get("l", []))
        total += sum(e[4] for e in u.get("e", []))
    st = side.get("st")
    if st:
        total += st[3] + st[5]
    return total


def castle_side(rep):
    for i, sd in enumerate(rep["s"]):
        if sd.get("st"):
            return i
    return None


def name_of(rep, pid):
    if pid == 0:
        return STR["rpt.name.garrison"]
    return rep.get("_names", {}).get(str(pid), STR["rpt.name.gone"])


def has_moment(rep, kind):
    return any(m[1] == kind for m in rep.get("mo", []))


# ---- the explanation engine (explain.md section 3) --------------------------
def cause_text(rep, v, factor, polar):
    """Return (key, params) for one cause row, or None when evidence is missing."""
    o = 1 - v
    side = v if polar == "for" else o
    why = rep["why"]
    if factor in ("counter", "tier"):
        ev = why.get("c" if factor == "counter" else "t", [[], []])[side]
        if not ev:
            return None
        return (f"rpt.why.{factor}.{polar}",
                {"a_line": line_name(ev[0]), "a_tier": ev[1],
                 "d_line": line_name(ev[2]), "d_tier": ev[3]})
    if factor == "numbers":
        return (f"rpt.why.numbers.{polar}",
                {"n_v": num(sent(rep["s"][v])), "n_o": num(sent(rep["s"][o]))})
    if factor == "lord":
        best = None
        for u in rep["s"][side]["u"]:
            for l in u.get("l", []):
                if best is None or l[3] + l[4] > best[3] + best[4]:
                    best = l
        if best is None or not best[5]:
            return None
        sk = sorted(best[5], key=lambda x: (-x[1], x[0]))[0]
        heal = "_heal" if best[4] > best[3] else ""
        return (f"rpt.why.lord.{polar}{heal}",
                {"lord": LORDS[best[0]], "skill": EXAMPLE_SKILLS.get((best[0], sk[0]), f"skill {sk[0]}"),
                 "casts": sk[1]})
    if factor == "stats":
        sv = why.get("s", [0, 0])
        return (f"rpt.why.stats.{polar}", {"s_v": pct(sv[v]), "s_o": pct(sv[o])})
    c = castle_side(rep)
    if c is None:
        return None
    st = rep["s"][c]["st"]
    gate = has_moment(rep, 3)
    if factor == "defences":
        return (f"rpt.why.defences.{polar}{'_fell' if gate else ''}",
                {"wall": pct(st[1]), "towers": st[2]})
    if factor == "siege":
        return (f"rpt.why.siege.{polar}{'_gate' if gate else ''}", {"wall": pct(st[1])})
    return None


def order_causes(items):
    """items: list of (factor, n). Sort by the DISPLAYED percent, largest first, so the bars
    always read in order; equal displayed percents fall back to ACTION_ORDER."""
    rank = {f: i for i, f in enumerate(ACTION_ORDER)}
    return sorted(items, key=lambda x: (-abs(pct(x[1])), rank[x[0]]))


def advice(rep, v, factor):
    o = 1 - v
    why = rep["why"]
    if factor == "counter":
        ev = why["c"][o]
        c_line = COUNTERED_BY[ev[0]]
        return ("rpt.next.counter", {"c_line": line_name(c_line), "d_line": line_name(ev[0])},
                ("train", c_line))
    if factor == "tier":
        ev = why["t"][o]
        return ("rpt.next.tier", {"line": line_name(ev[2]), "tier": ev[1]}, ("train", ev[2]))
    if factor == "defences" and any(u.get("e") for u in rep["s"][v]["u"]):
        return ("rpt.next.defences_more", {}, ("siege", None))
    table = {"numbers": ("rpt.next.numbers", ("rally", None)),
             "lord": ("rpt.next.lord", ("scout", None)),
             "stats": ("rpt.next.stats", ("research", None)),
             "defences": ("rpt.next.defences", ("siege", None)),
             "siege": ("rpt.next.siege", ("wall", None)),
             "even": ("rpt.next.even", ("scout", None))}
    key, link = table[factor]
    return (key, {}, link)


def button_text(link):
    kind, arg = link
    if kind == "train":
        return s("rpt.btn.train", line=line_name(arg))
    return STR[f"rpt.btn.{kind}"]


def explain(rep, pov=0):
    v, o = pov, 1 - pov
    S = rep["s"]
    cp = [S[1]["lp"], S[0]["lp"]]          # power dealt BY side 0, BY side 1
    T = cp[0] + cp[1]
    win = rep["win"]
    outcome = "win" if win == v else ("loss" if win == o else "draw")
    m = round(1000 * (cp[v] - cp[o]) / T) if T else 0
    F = rep["why"]["f"]
    nets = {f: F[v][i] - F[o][i] for i, f in enumerate(FACTORS)}
    flags = []
    if max(abs(F[0][7]), abs(F[1][7])) >= T_OTHER_WARN:
        flags.append("why_other_high")
    real = [(f, n) for f, n in nets.items() if f != "other"]
    pos = [(f, n) for f, n in real if n >= T_SHOW]
    neg = [(f, n) for f, n in real if n <= -T_SHOW]
    if outcome == "win":
        main, counter_pool, counter_label = pos, neg, "rpt.why.despite"
    elif outcome == "loss":
        main, counter_pool, counter_label = neg, pos, "rpt.why.still"
    else:
        main, counter_pool, counter_label = pos + neg, [], None
    main = order_causes(main)
    out_rows, dropped = [], []
    for f, n in main:
        ct = cause_text(rep, v, f, "for" if n > 0 else "against")
        if ct is None:
            dropped.append(f)
            continue
        out_rows.append({"factor": f, "n": n, "key": ct[0], "params": ct[1]})
    if dropped:
        flags.append("no_evidence:" + ",".join(dropped))
    extra_rows = out_rows[MAX_ROWS:]
    out_rows = out_rows[:MAX_ROWS]
    label = None
    if out_rows and outcome != "draw":
        top = out_rows[0]["n"]
        sign_ok = (m > 0 and outcome == "win") or (m < 0 and outcome == "loss")
        if rep["end"] in CASUALTY_ENDS and sign_ok and abs(top) >= FLIP_SAFETY * abs(m):
            label = "rpt.why.flip." + outcome
        elif abs(top) >= T_MAIN:
            label = "rpt.why.main"
    cpt = None
    if counter_pool:
        f, n = order_causes(counter_pool)[0]
        ct = cause_text(rep, v, f, "for" if n > 0 else "against")
        if ct:
            cpt = {"factor": f, "n": n, "key": ct[0], "params": ct[1], "label": counter_label}
    if T == 0:
        loser = S[o] if outcome == "win" else S[v]
        even_key = "rpt.why.empty" if sent(loser) == 0 else "rpt.why.even"
    else:
        even_key = "rpt.why.even"
    # advice: the strongest cause against the viewer
    against = None
    if outcome == "loss" and out_rows and out_rows[0]["n"] < 0:
        against = out_rows[0]["factor"]
    elif cpt and cpt["n"] < 0:
        against = cpt["factor"]
    elif outcome == "draw":
        against = next((r["factor"] for r in out_rows if r["n"] < 0), None)
    if against is None and outcome in ("loss", "draw"):
        against = "even"
    adv = None
    if against:
        k, p, link = advice(rep, v, against)
        assert link[0] in LINK_ALLOWED
        adv = {"factor": against, "key": k, "params": p, "link": list(link),
               "text": s(k, **p), "button": button_text(link)}
    for r in out_rows + ([cpt] if cpt else []):
        r["text"] = s(r["key"], **r["params"])
        if len(r["text"]) > MAX_SENTENCE:
            flags.append(f"long_sentence:{r['key']}:{len(r['text'])}")
    if label:
        out_rows[0]["label"] = label
        out_rows[0]["label_text"] = STR[label]
    band = "close" if abs(m) < T_CLOSE else ("clear" if abs(m) < T_BIG else "big")
    return {"pov": v, "outcome": outcome, "margin": m, "margin_word": STR[f"rpt.margin.{outcome}.{band}"],
            "T": T, "cp_you": cp[v], "cp_them": cp[o], "nets": nets,
            "rows": out_rows, "hidden_rows": [r["factor"] for r in extra_rows],
            "counterpoint": cpt, "even": None if out_rows else {"key": even_key, "text": s(even_key, pct=pct(T_SHOW))},
            "advice": adv, "notes": loss_notes(rep, v), "headline": headline(rep, v, outcome, band),
            "flags": flags}


def loss_notes(rep, v):
    sd = rep["s"][v]
    notes = []
    lt, hp, ho = light(sd), hosp(sd), sum(u.get("ho", 0) for u in sd["u"])
    if lt:
        notes.append(("rpt.loss.light", {"n": num(lt)}))
    if hp:
        notes.append(("rpt.loss.hosp", {"n": num(hp)}))
    if ho:
        notes.append(("rpt.loss.hosp_full", {"n": num(ho)}))
    if out(sd):
        notes.append((f"rpt.loss.lc.{sd['lc']}", {}))
    else:
        notes.append(("rpt.loss.none", {}))
    return [{"key": k, "params": p, "text": s(k, **p)} for k, p in notes]


def headline(rep, v, outcome, band):
    o = 1 - v
    S = rep["s"]
    word = STR[f"rpt.outcome.{outcome}"]
    if rep["pl"][0] == PLACE_CASTLE and castle_side(rep) == v and outcome != "draw":
        word = STR["rpt.outcome.held" if outcome == "win" else "rpt.outcome.breached"]
    opp = S[o]["u"][0]
    place = STR[f"rpt.place.{rep['pl'][0]}"]
    if rep["pl"][0] == PLACE_CASTLE and castle_side(rep) == v:
        place = STR["rpt.place.own"]
    key = "rpt.head.vs" if opp.get("tg") else "rpt.head.vs_notag"
    vs = s(key, name=name_of(rep, opp["id"]), tag=opp.get("tg", ""), place=place, x=rep["at"][0], y=rep["at"][1])
    stats = []
    if outcome == "loss":
        stats = [s("rpt.head.home_wounded", n=num(light(S[v]) + hosp(S[v]))),
                 s("rpt.head.lost", n=num(dead(S[v])))]
    else:
        stats.append(s("rpt.head.enemy_out", n=num(out(S[o]))))
        rs = rep.get("rs")
        if rs and v == 0 and any(rs):
            i = max(range(5), key=lambda k: rs[k])
            stats.append(s("rpt.head.taken", n=num(rs[i]), res=STR[f"res.{i}"]))
        else:
            stats.append(s("rpt.head.your_out", n=num(out(S[v]))))
    return {"word": word, "margin": STR[f"rpt.margin.{outcome}.{band}"], "vs": vs, "stats": stats}


# ---- rendering ---------------------------------------------------------------
def bar(n):
    return ("+" if n > 0 else "-") + f"{abs(pct(n))}%"


def render(rep, pov=0):
    if rep["k"] not in BATTLE_KINDS:
        return render_scout(rep) if rep["k"] == 5 else json.dumps(strip(rep))
    e = explain(rep, pov)
    v, o = pov, 1 - pov
    h = e["headline"]
    L = [f"{h['word']} · {h['margin']}", h["vs"], " · ".join(h["stats"])]
    top = e["rows"][0] if e["rows"] else None
    if top:
        L.append("Why: " + top["text"] + (" " + top["label_text"] if top.get("label_text") else ""))
    else:
        L.append("Why: " + e["even"]["text"])
    L.append("")
    L.append("WHY (tap a row for its numbers)")
    for r in e["rows"]:
        mark = "▲" if r["n"] > 0 else "▼"
        L.append(f"  {mark} {bar(r['n']):>5}  {r['text']}")
        if r.get("label_text"):
            L.append(f"           {r['label_text']}")
    if e["counterpoint"]:
        c = e["counterpoint"]
        L.append(f"  {STR[c['label']]}")
        L.append(f"  {'▲' if c['n'] > 0 else '▼'} {bar(c['n']):>5}  {c['text']}")
    if e["advice"]:
        a = e["advice"]
        L.append(f"  Next: {a['text']}  [{a['button']}]")
    L.append("")
    L.append("YOUR TROOPS              sent   light  infirm.   dead   dealt")
    for u, r in rows(rep["s"][v]):
        L.append(f"  {line_name(r[0]):<10} t{r[1]:<3} {num(r[2]):>9} {num(r[3]):>7} {num(r[4]):>8} {num(r[5]):>6} {num(r[6]):>7}")
    for u in rep["s"][v]["u"]:
        for g in u.get("e", []):
            L.append(f"  {EXAMPLE_ENGINES.get(g[0], g[0]):<10} ×{g[1]:<3} lost {g[2]}, wall damage {pct(g[3])}%")
    for n in e["notes"]:
        L.append("  " + n["text"])
    L.append("THEIR TROOPS             sent  out of action")
    for u, r in rows(rep["s"][o]):
        L.append(f"  {line_name(r[0]):<10} t{r[1]:<3} {num(r[2]):>9} {num(r[3] + r[4] + r[5]):>9}")
    L.append("LORDS          lvl   dealt  healed  skill casts")
    for side, who in ((v, "you"), (o, "they")):
        for u in rep["s"][side]["u"]:
            for l in u.get("l", []):
                casts = ", ".join(f"{EXAMPLE_SKILLS.get((l[0], k), k)} ×{c}" for k, c in l[5])
                L.append(f"  {LORDS[l[0]]:<7}({who:<4}) {l[2]:>3} {num(l[3]):>7} {num(l[4]):>7}  {casts}")
    if rep["k"] == 3:
        tot = dealt(rep["s"][v])
        L.append("RALLY SHARE (damage dealt, all participants)")
        for u in rep["s"][v]["u"]:
            d = sum(r[6] for r in u.get("t", [])) + sum(l[3] for l in u.get("l", [])) + sum(e[4] for e in u.get("e", []))
            L.append(f"  {name_of(rep, u['id']):<10} {num(d):>7}  {pct(round(1000 * d / tot)):>3}%")
    rs = rep.get("rs")
    if rs and any(rs):
        taken = ", ".join(f"{num(x)} {STR[f'res.{i}']}" for i, x in enumerate(rs) if x)
        verb = "Taken" if v == 0 else "Plundered from you"
        L.append(f"RESOURCES  {verb}: {taken}" + (f" (load {pct(rep['ld'])}% used)" if v == 0 and "ld" in rep else ""))
    if rep.get("mo"):
        L.append("TIMELINE (tap = replay from 1 s before)")
        for m in rep["mo"]:
            L.append(f"  beat {m[0]:>3}  {moment_text(rep, v, m)}")
    L.append("REPLAY  " + ("available" if rep.get("bx") else STR["rpt.replay.expired"]))
    return "\n".join(L)


def moment_text(rep, v, m):
    who = "you" if m[2] == v else "they"
    k = m[1]
    p = {}
    if k in (1, 5):
        p = {"a_line": line_name(m[3]), "b_line": line_name(m[4]) if k == 1 else ""}
    elif k == 2:
        p = {"lord": LORDS[m[3]], "skill": EXAMPLE_SKILLS.get((m[3], m[4]), m[4])}
    elif k == 4:
        p = {"wall": pct(m[3])}
    return s(f"rpt.mo.{k}.{who}", **p)


def render_scout(rep):
    sc, it = rep["sc"], rep["it"]
    L = [f"Scout report · tier {it} of 4", s("rpt.head.vs", name=name_of(rep, rep["tid"]), tag=rep.get("ttg", ""),
                                               place=STR[f"rpt.place.{rep['pl'][0]}"], x=rep["at"][0], y=rep["at"][1])]
    rounded = SCOUT_ROUNDED[it]

    def fmt(field, n):
        return s("rpt.scout.about", n=num(n)) if field in rounded and n >= 100 else num(n)
    L.append(f"Castle tier {sc['ct']} · power {fmt('pw', sc['pw'])} · wall {STR['rpt.wall.' + str(sc['wb'])]}"
             + (f" {pct(sc['wl'])}%" if "wl" in sc else ""))
    for field, label, reveal in (("tt", "Troops at home", 1), ("rs", "Resources above protection", 1),
                                 ("tl", "Troops per line", 2), ("t", "Troops per line and tier", 3),
                                 ("l", "Lords", 2), ("rf", "Reinforcements", 2), ("bo", "Boosts", 4),
                                 ("hf", "Infirmary", 4)):
        if field in sc:
            val = sc[field]
            if field == "tt":
                txt = fmt("tt", val)
            elif field == "rs":
                txt = ", ".join(f"{fmt('rs', x)} {STR['res.' + str(i)]}" for i, x in enumerate(val))
            elif field == "tl":
                txt = ", ".join(f"{line_name(a)} {fmt('tl', b)}" for a, b in val)
            elif field == "t":
                txt = ", ".join(f"{line_name(a)} t{b} {num(c)}" for a, b, c in val)
            elif field == "l":
                txt = ", ".join(LORDS[x[0]] + (f" lvl {x[1]}" if len(x) > 1 else "") for x in val)
            elif field == "rf":
                txt = (f"allies {val[0]}, troops {fmt('rf', val[1])}" if isinstance(val[0], int)
                       else ", ".join(f"{name_of(rep, a)} {num(b)}" for a, b in val))
            elif field == "bo":
                txt = "attack +{}%, defence +{}%, health +{}%".format(*[pct(x) for x in val])
            else:
                txt = f"{pct(val)}% full"
            L.append(f"  {label}: {txt}")
        elif field != "t" or it < 3:
            if not (field == "tl" and it >= 3):
                L.append(f"  {label}: " + s("rpt.scout.unknown", tier=reveal))
    return "\n".join(L)


# ---- sizes -------------------------------------------------------------------
def strip(obj):
    if isinstance(obj, dict):
        return {k: strip(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [strip(x) for x in obj]
    return obj


def mini(obj):
    return json.dumps(strip(obj), separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def gz(b):
    return gzip.compress(b, compresslevel=6, mtime=0)


def summary_form(rep):
    """storage.md section 3: day 7 -> drop moments and beats ref, collapse tiers per line,
    keep only each lord's top skill. The why block stays whole."""
    r = json.loads(mini(rep))
    r.pop("mo", None)
    r.pop("bx", None)
    for sd in r.get("s", []):
        for u in sd["u"]:
            agg = {}
            for t in u.get("t", []):
                a = agg.setdefault(t[0], [t[0], 0, 0, 0, 0, 0, 0])
                for i in range(2, 7):
                    a[i] += t[i]
            u["t"] = [agg[k] for k in sorted(agg)]
            for l in u.get("l", []):
                if l[5]:
                    l[5] = [sorted(l[5], key=lambda x: (-x[1], x[0]))[0]]
    return r


def opponent_view(rep, viewer):
    """schema.md section 5: what the server sends to `viewer` (0/1): the other side's bucket
    split, overflow and protected resources are removed."""
    r = json.loads(mini(rep))
    o = 1 - viewer
    for u in r["s"][o]["u"]:
        u["t"] = [[t[0], t[1], t[2], t[3] + t[4] + t[5], t[6]] for t in u.get("t", [])]
        u.pop("ho", None)
        for l in u.get("l", []):
            if len(l) > 6:
                del l[6:]
    if viewer != castle_side(rep):
        r.pop("rp", None)
    return r


def size_report(rep):
    full = mini(rep)
    res = {"minified": len(full), "gzip": len(gz(full)), "sections": {}}
    for k, val in strip(rep).items():
        res["sections"][k] = len(json.dumps({k: val}, separators=(",", ":"), ensure_ascii=False).encode()) - 1
    if rep["k"] in BATTLE_KINDS:
        sm = mini(summary_form(rep))
        res["summary_minified"], res["summary_gzip"] = len(sm), len(gz(sm))
        ov = mini(opponent_view(rep, 0))
        res["view_attacker_gzip"] = len(gz(ov))
        res["list_line_minified"] = len(mini(list_line(rep, 0)))
    return res


def list_line(rep, pov):
    """schema.md section 6: the inbox row mail-forge stores per viewer, so the list and the
    headline render with 0 extra reads."""
    e = explain(rep, pov)
    S = rep["s"]
    o = 1 - pov
    top = e["rows"][0] if e["rows"] else None
    if e["outcome"] == "loss":
        nums = [light(S[pov]) + hosp(S[pov]), dead(S[pov])]
    else:
        nums = [out(S[o]), max(rep.get("rs") or [0]) if pov == 0 else out(S[pov])]
    return {"r": rep["id"], "k": rep["k"], "ts": rep["ts"], "o": ("win", "loss", "draw").index(e["outcome"]),
            "m": e["margin"], "p": S[o]["u"][0]["id"], "tg": S[o]["u"][0].get("tg", ""), "pl": rep["pl"][0],
            "at": rep["at"], "n": nums, "c": [FACTORS.index(top["factor"]), 1 if top["n"] > 0 else 0] if top else []}


def synth_rally(n, base):
    """A rally with n attacking participants built from rally_stronghold.json's joiners, for
    the storage table (storage.md section 2). Numbers vary so gzip cannot cheat on repeats."""
    rep = json.loads(mini(base))
    lead = rep["s"][0]["u"][0]
    joiners = []
    for i in range(1, n):
        line, tier = i % 5, 5 + i % 3
        sentn = 1500 + 137 * i
        lt, hp = 40 + 7 * i, 90 + 13 * i
        joiners.append({"id": 30000 + 97 * i, "tg": "GRY", "t": [[line, tier, sentn, lt, hp, 0, 2000 + 211 * i]], "ho": 0})
    rep["s"][0]["u"] = [lead] + joiners
    return rep


# ---- invariants (qa.md section 2) ---------------------------------------------
def check(rep):
    err = []
    E = err.append
    for key in ("v", "id", "k", "ts"):
        if key not in rep:
            E(f"missing {key}")
    if rep.get("v") != 1:
        E("schema version must be 1")
    if not (isinstance(rep.get("id"), str) and len(rep["id"]) == 16):
        E("id must be 16 hex chars")
    if rep.get("k") == 5:
        return err + check_scout(rep)
    if rep.get("k") == 4 and len(rep.get("hu", [])) > 5:
        E("a hunt holds at most 5 camp fights")
    if rep.get("k") not in BATTLE_KINDS:
        return err
    S = rep["s"]
    if rep["win"] not in (0, 1, 2):
        E("win must be 0, 1 or 2")
    if rep["end"] not in END_NAMES:
        E("unknown end reason")
    for i, sd in enumerate(S):
        if len(sd["u"]) > 30:
            E(f"side {i}: more than 30 participants")
        for u, r in rows(sd):
            if len(r) != 7:
                E(f"side {i}: troop row needs 7 fields: {r}")
                continue
            if not (0 <= r[0] <= 4 and 1 <= r[1] <= LINE_MAX_TIER[r[0]]):
                E(f"side {i}: bad line/tier {r[:2]}")
            if min(r[2:]) < 0 or r[3] + r[4] + r[5] > r[2]:
                E(f"side {i}: casualties exceed sent {r}")
        for u in sd["u"]:
            if u.get("ho", 0) > sum(r[5] for r in u.get("t", [])):
                E(f"side {i}: overflow dead > dead")
        net = dealt(sd) - healed(S[1 - i])
        if abs(net - S[1 - i]["lp"]) > 1:
            E(f"side {i}: dealt {dealt(sd)} - healed by the other side {healed(S[1 - i])}"
              f" != power lost by the other side {S[1 - i]['lp']}")
    T = S[0]["lp"] + S[1]["lp"]
    F = rep["why"]["f"]
    for i in (0, 1):
        if len(F[i]) != 8:
            E("why.f needs 8 factors per side")
            continue
        share = round(1000 * S[1]["lp"] / T) if i == 0 and T else (round(1000 * S[0]["lp"] / T) if T else 0)
        neutral = share - sum(F[i])
        if neutral < 0:
            E(f"side {i}: factor extras {sum(F[i])} exceed its share {share} (neutral < 0)")
        if any(abs(x) > 1000 for x in F[i]):
            E("why.f value outside -1000..1000")
    c = castle_side(rep)
    if c is None and any(F[i][5] or F[i][6] for i in (0, 1)):
        E("defences/siege factors without structures (st)")
    if c is not None:
        if F[c][6] > 0 or F[1 - c][5] > 0:
            E("siege credit belongs to the attacker, tower/wall credit to the castle side")
        eng = [g for u in S[1 - c]["u"] for g in u.get("e", [])]
        if F[1 - c][6] > 0 and not eng:
            E("siege credit with no siege engines on the attacking side")
        st = S[c]["st"]
        if sum(g[3] for g in eng) > st[0] - st[1]:
            E("engine wall damage exceeds the wall durability lost")
        if round(1000 * (st[3] + st[5]) / T) > F[c][5] + 1 if T else False:
            E("tower and trap hits are 100% DEFENCES: F[castle][defences] is too small")
    for fac, key in (("counter", "c"), ("tier", "t")):
        for i in (0, 1):
            ev = rep["why"].get(key, [[], []])[i]
            if not ev:
                continue
            own = {(r[0], r[1]) for _, r in rows(S[i])}
            other = {(r[0], r[1]) for _, r in rows(S[1 - i])}
            if (ev[0], ev[1]) not in own or (ev[2], ev[3]) not in other:
                E(f"why.{key}[{i}] names a line/tier not in the rows: {ev}")
            if fac == "counter" and COUNTERED_BY.get(ev[2]) != ev[0]:
                E(f"why.c[{i}] {ev[:4]} is not a counter pair in the PROPOSAL graph")
            if fac == "counter" and ev[4] > F[i][0] + 1:
                E(f"why.c[{i}] top matchup {ev[4]} exceeds the side's counter total {F[i][0]}")
    for i in (0, 1):
        if F[i][0] < 0:
            E(f"side {i}: a counter bonus only adds damage, counter extras cannot be negative")
        skill = sum(l[3] for u in S[i]["u"] for l in u.get("l", []))
        heal_against = healed(S[1 - i])
        if T and round(1000 * (skill - heal_against) / T) > F[i][3] + 1:
            E(f"side {i}: skill hits are 100% LORD, F[lord] {F[i][3]} is too small")
    mo = rep.get("mo", [])
    if len(mo) > 8:
        E("more than 8 moments")
    if [m[0] for m in mo] != sorted(m[0] for m in mo):
        E("moments must be in beat order")
    if any(m[0] >= rep.get("bn", 10 ** 9) for m in mo):
        E("moment beat index beyond bn")
    if "rs" in rep and (len(rep["rs"]) != 5 or min(rep["rs"]) < 0):
        E("rs needs 5 non-negative ints")
    if "ld" in rep and not 0 <= rep["ld"] <= 1000:
        E("ld is per mille 0..1000")
    for pov in (0, 1):
        try:
            e = explain(rep, pov)
            err.extend(f"pov {pov}: {f}" for f in e["flags"] if f.startswith("long_sentence"))
        except Exception as ex:  # noqa: BLE001 - the probe reports any crash as a failure
            E(f"explain crashed for pov {pov}: {ex!r}")
    e0, e1 = explain(rep, 0), explain(rep, 1)
    if any(e0["nets"][f] != -e1["nets"][f] for f in FACTORS):
        E("nets are not symmetric between the two viewpoints")
    return err


def check_scout(rep):
    err = []
    it, sc = rep.get("it"), rep.get("sc", {})
    if it not in SCOUT_FIELDS:
        return ["scout tier must be 0..4"]
    extra = set(sc) - SCOUT_FIELDS[it]
    if extra:
        err.append(f"tier {it} leaks fields {sorted(extra)}")
    for f in SCOUT_ROUNDED[it] & set(sc):
        vals = sc[f]
        flat = []
        if isinstance(vals, int):
            flat = [vals]
        elif f == "rs":
            flat = vals
        elif f == "tl":
            flat = [b for _, b in vals]
        elif f == "rf":
            flat = [vals[1]]
        if any(x != sig2(x) for x in flat):
            err.append(f"tier {it}: field {f} not rounded to 2 significant figures: {vals}")
    return err


# ---- cost (storage.md section 4) -------------------------------------------------
def cost(a, sizes):
    """storage.md section 4. One record per battle (shared by every viewer), gzip JSON,
    30 days; the beats blob 7 days; kept (starred) reports 90 days."""
    P, ov = a.players, a.row_overhead
    battle_rec = a.battles / 2 + a.rallies / a.rally_size          # records per player per day
    rec = {  # name: (records per player per day, bytes per record incl. row overhead, days kept)
        "battle record": (battle_rec, sizes["battle_gz"] + ov, a.record_days),
        "beats (replay)": (battle_rec, a.beats_gz + ov, a.beats_days),
        "scout": (a.scouts, sizes["scout_gz"] + ov, a.scout_days),
        "hunt": (a.hunts, sizes["hunt_gz"] + ov, a.hunt_days),
        "gather": (a.gathers, sizes["gather_gz"] + ov, a.gather_days),
        "kept (starred)": (battle_rec * a.star_share, sizes["battle_gz"] + a.beats_gz + 2 * ov,
                           a.star_days - a.record_days),
    }
    total_gb, lines = 0.0, []
    for name, (per_day, b, days) in rec.items():
        gb = P * per_day * b * days / 1e9
        total_gb += gb
        lines.append(f"  {name:<15} {per_day:5.2f}/player/day × {b:>5} B × {days:>3} d = {gb:5.2f} GB")
    records = battle_rec * 2 + a.scouts + a.hunts + a.gathers   # battle record + its beats blob
    inbox = a.battles + a.rallies + a.scouts + a.hunts + a.gathers  # one list line per viewer (mail-forge)
    writes_day = P * (records + inbox)
    reads_day = P * a.opens
    egress_gb_month = reads_day * 30 * sizes["battle_gz"] / 1e9
    eur = total_gb * a.eur_gb + egress_gb_month * a.eur_egress
    lines.append(f"  steady-state storage {total_gb:.2f} GB -> €{total_gb * a.eur_gb:.2f}/month at €{a.eur_gb}/GB-month")
    lines.append(f"  writes {writes_day:,.0f}/day (records + beats + inbox rows) = {writes_day / 86400:.1f}/s average,"
                 f" {writes_day / 86400 * a.peak:.0f}/s at the war-hour peak (×{a.peak:g})")
    lines.append(f"  report opens {reads_day:,.0f}/day; egress {egress_gb_month:.1f} GB/month -> €{egress_gb_month * a.eur_egress:.2f}")
    lines.append(f"  TOTAL ≈ €{eur:.2f}/month = {100 * eur / 200:.1f}% of the €200 budget")
    return "\n".join(lines), eur


# ---- CLI ---------------------------------------------------------------------------
def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("explain"); p.add_argument("file"); p.add_argument("--pov", type=int, default=0); p.add_argument("--json", action="store_true")
    p = sub.add_parser("render"); p.add_argument("file"); p.add_argument("--pov", type=int, default=0)
    p = sub.add_parser("size"); p.add_argument("files", nargs="*"); p.add_argument("--rally", type=int, default=0)
    p = sub.add_parser("check"); p.add_argument("files", nargs="+")
    p = sub.add_parser("golden"); p.add_argument("fixtures"); p.add_argument("out")
    p = sub.add_parser("cost")
    p.add_argument("--fixtures", default=os.path.join(HERE, "..", "tests", "fixtures"))
    for name, val in (("players", 50000), ("battles", 1.0), ("rallies", 0.3), ("rally_size", 13.0),
                      ("scouts", 1.5), ("hunts", 3.0), ("gathers", 4.0), ("opens", 8.0),
                      ("record_days", 30), ("beats_days", 7), ("scout_days", 3),
                      ("hunt_days", 7), ("gather_days", 7), ("star_share", 0.05), ("star_days", 90),
                      ("beats_gz", 1800), ("row_overhead", 60),
                      ("eur_gb", 0.25), ("eur_egress", 0.05), ("peak", 15.0)):
        p.add_argument("--" + name.replace("_", "-"), dest=name, type=type(val), default=val)
    a = ap.parse_args(argv)
    if a.cmd == "explain":
        e = explain(load(a.file), a.pov)
        if a.json:
            print(json.dumps(e, indent=1, ensure_ascii=False))
        else:
            print(f"outcome {e['outcome']}  margin {e['margin']}‰ ({e['margin_word']})  T={num(e['T'])} cp")
            print("factor     net‰  shown")
            shown = {r["factor"] for r in e["rows"]} | ({e["counterpoint"]["factor"]} if e["counterpoint"] else set())
            for f in FACTORS:
                print(f"  {f:<9}{e['nets'][f]:>6}  {'yes' if f in shown else '-'}")
            print("flags:", ", ".join(e["flags"]) or "none")
            print()
            print(render(load(a.file), a.pov))
    elif a.cmd == "render":
        print(render(load(a.file), a.pov))
    elif a.cmd == "size":
        for f in a.files:
            print(os.path.basename(f), json.dumps(size_report(load(f))))
        if a.rally:
            base = load(os.path.join(HERE, "..", "tests", "fixtures", "rally_stronghold.json"))
            r = size_report(synth_rally(a.rally, base))
            print(f"synthetic rally, {a.rally} participants: minified {r['minified']} B, gzip {r['gzip']} B")
    elif a.cmd == "check":
        bad = 0
        for f in a.files:
            errs = check(load(f))
            bad += bool(errs)
            print(f"{os.path.basename(f)}: " + ("OK" if not errs else "; ".join(errs)))
        print(f"REPORT CHECK {'OK' if not bad else 'FAIL'} - {len(a.files)} files, {bad} with errors")
        return 1 if bad else 0
    elif a.cmd == "golden":
        os.makedirs(a.out, exist_ok=True)
        n = 0
        for f in sorted(os.listdir(a.fixtures)):
            rep = load(os.path.join(a.fixtures, f))
            if rep.get("k") not in BATTLE_KINDS:
                continue
            for pov in (0, 1):
                e = explain(rep, pov)
                keep = {"outcome": e["outcome"], "margin": e["margin"],
                        "rows": [[r["key"], r["n"], r.get("label")] for r in e["rows"]],
                        "counterpoint": [e["counterpoint"]["key"], e["counterpoint"]["n"]] if e["counterpoint"] else None,
                        "advice": [e["advice"]["key"], e["advice"]["link"]] if e["advice"] else None,
                        "notes": [x["key"] for x in e["notes"]], "headline": e["headline"]}
                with open(os.path.join(a.out, f"{f[:-5]}.pov{pov}.json"), "w", encoding="utf-8") as g:
                    json.dump(keep, g, indent=1, ensure_ascii=False)
                n += 1
        print(f"GOLDEN OK - {n} expected outputs written to {a.out}")
    elif a.cmd == "cost":
        fx = a.fixtures
        win = load(os.path.join(fx, "win_field.json"))
        sc = load(os.path.join(fx, "scout_t2.json"))
        szw = size_report(win)
        sizes = {"battle_gz": szw["gzip"], "scout_gz": size_report(sc)["gzip"],
                 "hunt_gz": size_report(load(os.path.join(fx, "hunt.json")))["gzip"],
                 "gather_gz": size_report(load(os.path.join(fx, "gather.json")))["gzip"]}
        text, _ = cost(a, sizes)
        print("measured sizes (gzip): " + ", ".join(f"{k[:-3]} {v} B" for k, v in sizes.items()))
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
