#!/usr/bin/env python3
"""Tests for tools/report_tool.py — run: python tests/test_report_tool.py
Prints `REPORT TOOL OK - <n> checks` or the first failures. Stdlib only."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import report_tool as rt  # noqa: E402

FX = os.path.join(HERE, "fixtures")
checks, fails = 0, []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def fx(name):
    return rt.load(os.path.join(FX, name))


BATTLES = ["win_field.json", "loss_castle.json", "rally_stronghold.json", "even_draw.json"]

# 1. every fixture passes the invariants; nets are symmetric between viewpoints
for f in sorted(os.listdir(FX)):
    ok(rt.check(fx(f)) == [], f"{f}: {rt.check(fx(f))}")

# 2. worked example 1 — the win (examples.md section 1)
e = rt.explain(fx("win_field.json"), 0)
ok([r["factor"] for r in e["rows"]] == ["counter", "lord"], f"win rows {[r['factor'] for r in e['rows']]}")
ok(e["rows"][0].get("label") == "rpt.why.flip.win", "win: counter must carry the flip label")
ok(e["margin"] == 62 and e["outcome"] == "win", f"win margin {e['margin']}")
ok(e["counterpoint"]["factor"] == "numbers" and e["counterpoint"]["n"] == -57, "win: counterpoint numbers -57")
ok(e["advice"]["link"] == ["rally", None], f"win advice {e['advice']}")
ok(e["headline"]["stats"] == ["Enemy out of action 2,780", "Taken 84,000 wood"], f"{e['headline']}")

# 3. worked example 2 — the loss, both viewpoints (examples.md section 2)
e = rt.explain(fx("loss_castle.json"), 0)
ok([r["factor"] for r in e["rows"]] == ["defences", "counter", "numbers"], f"loss rows {e['rows']}")
ok(e["hidden_rows"] == ["stats"], "loss: the 4th cause (stats -8%) waits in Details")
ok(all("label" not in r for r in e["rows"]), "loss at the wall: no flip (structure end) and no main (< 250)")
ok(e["counterpoint"]["factor"] == "siege", "loss: what went well = siege")
ok(e["advice"]["key"] == "rpt.next.defences_more" and e["advice"]["link"] == ["siege", None], f"{e['advice']}")
ok("Your infirmary was full: 340 severely wounded died." in [n["text"] for n in e["notes"]], "overflow note")
ok(e["headline"]["stats"] == ["Wounded coming back 2,420", "Lost 2,180"], f"{e['headline']}")
e1 = rt.explain(fx("loss_castle.json"), 1)
ok(e1["headline"]["word"] == "Castle held" and "Your castle" in e1["headline"]["vs"], f"{e1['headline']}")
ok(e1["advice"]["link"] == ["wall", None], f"defender advice {e1['advice']}")

# 4. rally and draw edge fixtures
e = rt.explain(fx("rally_stronghold.json"), 0)
ok([r["factor"] for r in e["rows"]] == ["siege", "numbers", "lord"], f"rally rows {e['rows']}")
ok(e["counterpoint"]["key"] == "rpt.why.defences.against_fell", "rally: gate fell variant")
ok(e["advice"]["key"] == "rpt.next.defences_more", "rally: engines already brought -> 'more' advice")
ok("[]" not in e["headline"]["vs"], "empty alliance tag must not print []")
e = rt.explain(fx("even_draw.json"), 0)
ok(e["rows"] == [] and e["even"]["key"] == "rpt.why.even" and e["advice"]["link"] == ["scout", None], "draw")

# 5. thresholds at their boundaries (explain.md section 3)
base = fx("win_field.json")


def with_nets(counter_a, lord_a=0, tier_a=0):
    r = copy.deepcopy(base)
    r["why"]["f"][0] = [counter_a, tier_a, 0, lord_a, 0, 0, 0, 0]
    r["why"]["f"][1] = [0] * 8
    return r


ok([x["factor"] for x in rt.explain(with_nets(49), 0)["rows"]] == [], "49 per mille is hidden")
ok([x["factor"] for x in rt.explain(with_nets(50), 0)["rows"]] == ["counter"], "50 per mille is shown")
m = rt.explain(base, 0)["margin"]                     # 62
flip_at = -(-125 * m // 100)                           # ceil(1.25 * m) = 78
ok(rt.explain(with_nets(flip_at), 0)["rows"][0].get("label") == "rpt.why.flip.win", "flip at 1.25 x margin")
ok(rt.explain(with_nets(flip_at - 1), 0)["rows"][0].get("label") is None, "no flip just below 1.25 x margin")
r = with_nets(260)
r["end"] = 3                                           # structure-decided end: no flip claim
ok(rt.explain(r, 0)["rows"][0].get("label") == "rpt.why.main", "main reason at >= 250 without flip")
ok([x["factor"] for x in rt.explain(with_nets(56, lord_a=64), 0)["rows"]] == ["counter", "lord"],
   "equal displayed percent (6% = 6%) falls back to action order: counter before lord")
ok([x["factor"] for x in rt.explain(with_nets(56, lord_a=66), 0)["rows"]] == ["lord", "counter"],
   "7% lord outranks 6% counter: bars always read in order")
r = copy.deepcopy(base)
r["why"]["f"][0][7] = 120
ok("why_other_high" in rt.explain(r, 0)["flags"], "untagged share >= 100 per mille raises a flag")

# 6. mutation tests — each invariant must catch its defect
def must_fail(rep, what):
    ok(rt.check(rep) != [], f"check() missed: {what}")


r = fx("scout_t2.json"); r["sc"]["t"] = [[1, 7, 6000]]; must_fail(r, "tier-2 scout leaks tier rows")
r = fx("scout_t2.json"); r["sc"]["tt"] = 11234; must_fail(r, "tier-2 scout total not rounded")
r = fx("win_field.json"); r["s"][0]["u"][0]["t"][0][5] = 6000; must_fail(r, "casualties exceed sent")
r = fx("win_field.json"); r["why"]["c"][0] = [3, 6, 0, 6, 210]; must_fail(r, "counter evidence names a line not sent")
r = fx("rally_stronghold.json"); r["s"][0]["u"][0].pop("e"); must_fail(r, "siege credit with no engines")
r = fx("loss_castle.json"); r["s"][1]["u"][0]["l"][0][4] = 0; must_fail(r, "an enemy heal not booked")
r = fx("loss_castle.json"); r["why"]["f"][1][5] = 10; must_fail(r, "tower hits not 100% defences")
r = fx("win_field.json"); r["why"]["f"][0][0] = 700; must_fail(r, "factor extras exceed the side's share")
r = fx("win_field.json"); r["mo"].reverse(); must_fail(r, "moments out of beat order")

# 7. strings: every key the engine can emit exists; key families are documented in explain.md
text = open(os.path.join(ROOT, "references", "explain.md"), encoding="utf-8").read()
for k in rt.STR:
    if re.match(r"rpt\.(why|next|loss|outcome|margin|head)\.", k):
        ok(k in text, f"key {k} not documented in references/explain.md")
for f in BATTLES:
    for pov in (0, 1):
        ex = rt.explain(fx(f), pov)
        ok(not [x for x in ex["flags"] if x.startswith("long_sentence")], f"{f} pov {pov}: {ex['flags']}")
        ok(ex["advice"] is None or ex["advice"]["link"][0] in rt.LINK_ALLOWED, "advice links only to play")
        ok(not re.search(r"\b(shop|gems?|offer|buy)\b", json.dumps(ex).lower()),
           f"{f}: no shop, gem, offer or buy word anywhere in a report (money-law)")

# 8. byte budgets (schema.md section 4) and the cost ceiling (storage.md section 4)
for f in BATTLES:
    ok(rt.size_report(fx(f))["gzip"] <= 600, f"{f}: battle record over 600 B gzip")
    ok(rt.size_report(fx(f))["list_line_minified"] <= 160, f"{f}: list line over 160 B")
ok(rt.size_report(rt.synth_rally(30, fx("rally_stronghold.json")))["gzip"] <= 1200, "30-player rally over 1,200 B gzip")
ok(rt.size_report(fx("scout_t2.json"))["gzip"] <= 300, "scout record over 300 B gzip")
out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "report_tool.py"), "cost", "--battles", "5",
                      "--rallies", "1", "--scouts", "6"], capture_output=True, text=True).stdout
eur = float(re.search(r"TOTAL ≈ €([0-9.]+)", out).group(1))
ok(eur <= 10.0, f"war-day cost €{eur} over the €10 (5% of budget) ceiling")

# 9. golden outputs for the Godot report_probe
with tempfile.TemporaryDirectory() as d:
    res = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "report_tool.py"), "golden", FX, d],
                         capture_output=True, text=True)
    ok(res.stdout.startswith("GOLDEN OK - 8 expected outputs"), res.stdout + res.stderr)

if fails:
    print(f"REPORT TOOL FAIL - {len(fails)} of {checks} checks")
    for x in fails:
        print("  -", x)
    sys.exit(1)
print(f"REPORT TOOL OK - {checks} checks")
