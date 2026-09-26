"""python tests/test_tools.py  -> 'PASS all N tests' (plain Python, no deps)."""
import io
import json
import math
import os
import sys
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import curve  # noqa: E402
import econ_sim  # noqa: E402


def test_curve_endpoints_exact():
    for shape in ("geometric", "phased", "poly"):
        ts = curve.curve(25, 60, 14 * 86400, shape)
        assert len(ts) == 25 and math.isclose(ts[0], 60) and math.isclose(ts[-1], 14 * 86400, rel_tol=1e-9), shape


def test_curve_monotonic():
    for shape in ("geometric", "phased", "poly"):
        ts = curve.curve(12, 30, 8 * 3600, shape)
        assert all(b > a for a, b in zip(ts, ts[1:])), shape


def test_phased_early_steeper_than_late():
    ts = curve.curve(25, 60, 14 * 86400, "phased")
    assert ts[1] / ts[0] > ts[-1] / ts[-2]


def test_help_floor_and_cut():
    assert curve.with_help(1000, 1, 0.01, 60) == 940          # floor wins
    assert math.isclose(curve.with_help(100000, 1, 0.01, 60), 99000)  # cut wins
    assert curve.with_help(100, 5, 0.01, 60) == 0.0          # never negative


def test_parse_dur():
    assert curve.parse_dur("90s") == 90 and curve.parse_dur("2h") == 7200 and curve.parse_dur("1.5d") == 129600


def test_econ_line_scaling():
    p = {"sessions": 4, "minutes": 30, "pack_mult": 0}
    assert econ_sim.line_amount({"name": "x", "base": 10, "per": "minute"}, p, 1) == 300
    assert econ_sim.line_amount({"name": "x", "base": 10, "per": "session"}, p, 1) == 40
    assert econ_sim.line_amount({"name": "x", "base": 10, "scale": "pack_mult"}, p, 1) == 0
    assert math.isclose(econ_sim.line_amount({"name": "x", "base": 100, "growth": 0.1}, p, 3), 121)


def test_econ_balanced_model_is_ok():
    m = {"resources": ["food"], "players": {"free": {"sessions": 1, "minutes": 1}},
         "sources": [{"name": "s", "res": "food", "base": 100}],
         "sinks": [{"name": "k", "res": "food", "base": 100}]}
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump(m, fh)
    buf = io.StringIO()
    with redirect_stdout(buf):
        econ_sim.main([path, "--days", "1,30"])
    os.remove(path)
    assert "within 0.90-1.10" in buf.getvalue()
    assert econ_sim.verdict(0.5) == "HOARD" and econ_sim.verdict(1.5) == "WALL" and econ_sim.verdict(1.0) == "ok"


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    for name, fn in tests:
        fn()
        print("PASS", name)
    print("PASS all %d tests" % len(tests))
