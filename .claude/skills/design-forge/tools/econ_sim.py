"""Economy simulator for design-forge — sources vs sinks per player type.

    python econ_sim.py <model.json> [--days 1,7,30,90] [--csv out.csv]
    python econ_sim.py --example > model.json      # a starter model to edit

A model is plain JSON:
{
  "resources": ["food", "wood", "stone", "iron", "gold"],
  "players": {                         # sessions/day and spend multiplier
    "free":  {"sessions": 4,  "minutes": 35,  "pack_mult": 0},
    "light": {"sessions": 5,  "minutes": 45,  "pack_mult": 1},
    "heavy": {"sessions": 8,  "minutes": 120, "pack_mult": 6}
  },
  "sources": [                         # per day unless "per" says otherwise
    {"name": "farms", "res": "food", "base": 40000, "growth": 0.035},
    {"name": "gathering", "res": "wood", "per": "minute", "base": 180, "growth": 0.02},
    {"name": "daily chest", "res": "gold", "base": 5000},
    {"name": "packs", "res": "gold", "base": 20000, "scale": "pack_mult"}
  ],
  "sinks": [
    {"name": "building upgrades", "res": "wood", "base": 50000, "growth": 0.05},
    {"name": "troop upkeep", "res": "food", "base": 30000, "growth": 0.04}
  ]
}

`growth` is daily compound growth of that line (the player's income grows as
the city grows; costs grow as levels rise). `per: "minute"` multiplies by
active minutes/day; `per: "session"` by sessions/day. `scale` names a player
field that multiplies the line (e.g. pack_mult: 0 removes paid income).

It prints, per player type and checkpoint day: cumulative sources, sinks,
the balance and the ratio sinks/sources. The design rule (SKILL.md red-team
#6): for the FREE player at day 30 the ratio is 0.90–1.10 for every resource
unless the spec names the imbalance on purpose. A ratio < 0.9 means hoarding
(inflation: rewards stop feeling like rewards); > 1.1 means a hard wall
(the player is gated by resources, not by time or skill).
"""
import argparse
import json
import sys

EXAMPLE = {
    "resources": ["food", "wood", "stone", "gold"],
    "players": {
        "free": {"sessions": 4, "minutes": 35, "pack_mult": 0},
        "light": {"sessions": 5, "minutes": 45, "pack_mult": 1},
        "heavy": {"sessions": 8, "minutes": 120, "pack_mult": 6},
    },
    "sources": [
        {"name": "farms", "res": "food", "base": 40000, "growth": 0.035},
        {"name": "lumber camps", "res": "wood", "base": 36000, "growth": 0.035},
        {"name": "quarries", "res": "stone", "base": 18000, "growth": 0.035},
        {"name": "gathering", "res": "wood", "per": "minute", "base": 180, "growth": 0.02},
        {"name": "camp raids", "res": "food", "per": "session", "base": 6000, "growth": 0.03},
        {"name": "daily tasks", "res": "gold", "base": 5000, "growth": 0.01},
        {"name": "packs", "res": "gold", "base": 20000, "scale": "pack_mult"},
    ],
    "sinks": [
        {"name": "building upgrades", "res": "wood", "base": 55000, "growth": 0.045},
        {"name": "building upgrades", "res": "stone", "base": 16000, "growth": 0.05},
        {"name": "research", "res": "gold", "base": 4500, "growth": 0.04},
        {"name": "troop training", "res": "food", "base": 26000, "growth": 0.04},
        {"name": "troop upkeep", "res": "food", "base": 12000, "growth": 0.04},
    ],
}


def line_amount(line, player, day):
    """Amount of one source/sink line on a given day (day 1 = first day)."""
    amt = float(line["base"]) * (1.0 + float(line.get("growth", 0.0))) ** (day - 1)
    per = line.get("per", "day")
    if per == "minute":
        amt *= player["minutes"]
    elif per == "session":
        amt *= player["sessions"]
    elif per != "day":
        raise ValueError("unknown per=%r in %s" % (per, line["name"]))
    if line.get("scale"):
        amt *= float(player.get(line["scale"], 1.0))
    return amt


def simulate(model, days):
    """-> {player: {day: {res: (src, snk)}}} cumulative up to each checkpoint."""
    out = {}
    last = max(days)
    for pname, p in model["players"].items():
        cum = {r: [0.0, 0.0] for r in model["resources"]}
        out[pname] = {}
        for d in range(1, last + 1):
            for ln in model["sources"]:
                cum[ln["res"]][0] += line_amount(ln, p, d)
            for ln in model["sinks"]:
                cum[ln["res"]][1] += line_amount(ln, p, d)
            if d in days:
                out[pname][d] = {r: tuple(v) for r, v in cum.items()}
    return out


def verdict(ratio):
    if ratio is None:
        return "no sink"
    if ratio < 0.9:
        return "HOARD"
    if ratio > 1.1:
        return "WALL"
    return "ok"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("model", nargs="?")
    ap.add_argument("--days", default="1,7,30,90")
    ap.add_argument("--csv")
    ap.add_argument("--example", action="store_true")
    a = ap.parse_args(argv)
    if a.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if not a.model:
        ap.error("model.json required (or --example)")
    with open(a.model, encoding="utf-8") as fh:
        model = json.load(fh)
    for ln in model["sources"] + model["sinks"]:
        if ln["res"] not in model["resources"]:
            ap.error("line %r uses unknown resource %r" % (ln["name"], ln["res"]))
    days = sorted(int(x) for x in a.days.split(","))
    res = simulate(model, days)
    rows = []
    for pname, by_day in res.items():
        print("\n== %s" % pname)
        print("%5s  %-8s %14s %14s %14s %7s  %s" % ("day", "res", "sources", "sinks", "balance", "ratio", ""))
        for d, by_res in by_day.items():
            for r, (src, snk) in by_res.items():
                ratio = (snk / src) if src else None
                v = verdict(ratio) if snk else "no sink"
                print("%5d  %-8s %14.0f %14.0f %14.0f %7s  %s" % (
                    d, r, src, snk, src - snk, "%.2f" % ratio if ratio is not None else "-", v))
                rows.append((pname, d, r, round(src), round(snk), round(src - snk),
                             round(ratio, 3) if ratio is not None else "", v))
    free30 = [r for r in rows if r[0] == "free" and r[1] == 30 and r[7] not in ("ok", "no sink")]
    if free30:
        print("\nRED-TEAM #6: free player at day 30 out of band -> " +
              ", ".join("%s %s" % (r[2], r[7]) for r in free30))
    elif any(r[0] == "free" and r[1] == 30 for r in rows):
        print("\nRED-TEAM #6: free player at day 30 within 0.90-1.10 on every resource with a sink")
    if a.csv:
        with open(a.csv, "w", encoding="utf-8") as fh:
            fh.write("player,day,resource,sources,sinks,balance,ratio,verdict\n")
            for r in rows:
                fh.write(",".join(str(x) for x in r) + "\n")
        print("CSV " + a.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
