"""python tests/test_combat_model.py  -> 'PASS all N tests' (plain Python, no deps).

Checks the invariants references/combat.md rests on, using tools/combat_model.py.
"""
import io
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import combat_model as cm  # noqa: E402

N = 10000


def near(a, b, tol):
    return abs(a - b) <= tol


def test_ring_one_hunt_one_hunter():
    assert sorted(cm.RING) == sorted(cm.LINES) and len(cm.LINES) == 5
    prey = list(cm.HUNTS.values())
    assert sorted(prey) == sorted(cm.LINES)                 # every line is hunted exactly once
    assert all(cm.HUNTS[cm.HUNTS[x]] != x for x in cm.LINES)  # no mutual pair
    pairs = [(i, j) for i in cm.LINES for j in cm.LINES if i < j]
    counters = [p for p in pairs if cm.HUNTS[p[0]] == p[1] or cm.HUNTS[p[1]] == p[0]]
    assert len(pairs) == 10 and len(counters) == 5          # 5 counters, 5 neutral
    assert cm.HUNTS["spearmen"] == "cavalry" and cm.HUNTS["infantry"] == "spearmen"


def test_unit_math():
    assert near(cm.q_step(0.6, 1.4), 1.4 ** 1.6, 1e-12)
    assert near(cm.ts_of_ratio(2.0), 2.06, 0.005)
    assert near(cm.extra_of_ts(1.0), 40.0, 1e-9)
    assert near(cm.ts_of_mult(cm.q_step() ** 0.37), 0.37, 1e-12)
    assert near(cm.ts_of_extra(cm.extra_of_ts(0.5)), 0.5, 1e-12)


def test_counter_is_one_tier_and_in_band():
    for al in (0.5, 0.6, 0.7, 0.8):
        for r in (1.35, 1.40, 1.50):
            c = cm.counter_c(al, r)
            assert near((1 + c) / (1 - c), cm.q_step(al, r), 1e-9)
            assert 0.20 <= c <= 0.50, (al, r, c)             # numbers.md §4 band
            assert cm.one_sided_c(al, r) > c
    assert round(100 * cm.counter_c()) == 26


def test_sim_tier_draw_ratio_is_r_for_every_end_rule():
    for kw in ({}, {"rout": 0.5}, {"rounds": 12}):
        for t in (1, 5, 9):
            x = cm.draw_ratio(lambda m: {"infantry": (N * m, t)}, lambda: {"infantry": (N, t + 1)}, **kw)
            assert near(x, cm.R, 1e-3), (kw, t, x)


def test_sim_every_hunter_pair_draws_one_tier_up():
    for h in cm.RING:
        assert near(cm.sim_ts({h: 1.0}, {cm.HUNTS[h]: 1.0}, 5, 6), 0.0, 0.01), h
    assert near(cm.sim_ts({"spearmen": 1.0}, {"cavalry": 1.0}, 10, 11), 0.0, 0.01)
    assert near(cm.sim_ts({"spearmen": 1.0}, {"cavalry": 1.0}, 5, 7), -1.0, 0.01)   # t(n+2) prey wins by 1 TS
    assert near(cm.sim_ts({"infantry": 1.0}, {"cavalry": 1.0}, 5, 5), 0.0, 0.01)    # neutral pair draws


def test_sim_stack_multiplier_equals_its_ts():
    for ts in (0.5, 1.0):
        m = cm.q_step() ** ts
        x = cm.draw_ratio(lambda k: {"infantry": (N * k, 5)}, lambda: {"infantry": (N, 5)}, modB=m)
        assert near(x, cm.R ** ts, 1e-3), (ts, x)


def test_matchup_index():
    assert cm.matchup_index(cm.EVEN, cm.EVEN) == 0
    for _, a in cm.OURS:
        for _, b in cm.ENEMIES:
            assert near(cm.matchup_index(a, b), -cm.matchup_index(b, a), 1e-12)
            assert near(sum(a.values()), 1.0, 1e-9) and near(sum(b.values()), 1.0, 1e-9)
    res = cm.cmd_mix(None, lambda *_: None)
    assert res["worst_rel"] <= 0.08 and res["worst_diff"] <= 0.04 and res["worst_abs"] <= 0.03
    assert res["best"] >= cm.LEAD_MAX                        # a scouted pick answers the money lead


def test_power_and_cost_tables():
    p = [cm.power(t) for t in range(1, 12)]
    assert all(b > a for a, b in zip(p, p[1:]))
    assert near(p[9] / p[0], 20.7, 0.05) and 15 <= p[9] / p[0] <= 38   # numbers.md §3 band
    cpp = [cm.cost_per_power(t) for t in range(1, 12)]
    assert cpp[0] == 1 and all(b > a for a, b in zip(cpp, cpp[1:])) and near(cpp[10], 1.42, 0.005)


def test_stack_caps_and_invariants():
    assert near(sum(cm.POOLS.values()), cm.CAP, 1e-9)       # 0.50 + 0.50 + 0.25 = 1.25
    assert cm.POOLS["lords"] <= 0.5                         # half a counter
    assert 1.0 - cm.POOLS["lords"] > 0                      # I1: counter with no lords beats a maxed pair
    assert 1.0 - (cm.CAP - cm.FREE[30]) > 0                 # I1: free day-30 stack + counter beats max stack
    for d in cm.FREE:
        assert cm.HEAVY[d] - cm.FREE[d] <= cm.LEAD_MAX + 1e-9, d          # I2
        assert cm.FREE_LORDS[d] <= min(cm.FREE[d], cm.POOLS["lords"])
        assert cm.HEAVY_LORDS[d] <= min(cm.HEAVY[d], cm.POOLS["lords"])
        assert cm.HEAVY[d] <= cm.CAP
    days = sorted(cm.FREE)
    assert all(cm.FREE[a] < cm.FREE[b] for a, b in zip(days, days[1:]))


def test_loss_rows():
    for ctx, li, se, de, _ in cm.LOSS_ROWS:
        assert li + se + de == 100, ctx
    for k in cm.NEVER_KILL:
        assert cm.LOSS_ROWS[k][3] == 0, cm.LOSS_ROWS[k][0]
    assert cm.LOSS_ROWS[2][4] == "Routed"                   # home never kills
    dead = [row[3] for row in cm.LOSS_ROWS[3:8]]
    assert dead == sorted(dead)                             # aggression costs more


def test_war_score_factors_and_scout_level():
    assert cm.weak_target(0.29) == 0 and near(cm.weak_target(0.45), 0.5, 1e-9) and cm.weak_target(0.6) == 1
    assert cm.scout_level(3, 3) == 3 and cm.scout_level(1, 6) == 1 and cm.scout_level(6, 1) == 5


def test_beds_worst_day_fits():
    a = type("A", (), {"march": 25000, "beta": 1.25})()
    res = cm.cmd_beds(a, lambda *_: None)
    assert res["worst"] <= 1.25 and res["beds"] == 31250 and res["over"] == 6250


def test_walls_worked_window_and_no_engine_count():
    res = cm.cmd_walls(None, lambda *_: None)
    assert res["end"] == 0 and res["no_engines"] == 13


def test_deterministic_and_cli_verdict():
    a = {"spearmen": (6000, 5), "archers": (4000, 5)}
    b = {"cavalry": (7000, 5), "infantry": (3000, 6)}
    assert cm.fight(a, b) == cm.fight(a, b)
    buf = io.StringIO()
    rc = cm.main(["all"], out=lambda s: buf.write(s + "\n"))
    assert rc == 0 and "COMBAT MODEL OK" in buf.getvalue(), buf.getvalue()[-400:]
    rc = cm.main(["all", "--lords", "0.78", "--realm", "0.30", "--temp", "0.15"], out=lambda s: None)
    assert rc == 1                                          # 1.23 != 1.25 cap: the check catches a bad sum


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    for name, fn in tests:
        fn()
        print("PASS", name)
    print("PASS all %d tests" % len(tests))
