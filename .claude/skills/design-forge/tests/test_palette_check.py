"""python tests/test_palette_check.py  -> 'PASS all N tests' (plain Python, no deps).

Checks tools/palette_check.py: CIEDE2000 against the published reference data
(Sharma, Wu, Dalal 2005, Table 1, all 34 pairs), sRGB -> CIELAB anchors, the
Machado 2009 simulation's basic properties, the CLI exit codes, and the palette
numbers quoted in references/world.md section 12 (so the doc cannot drift from the tool).
"""
import io
import math
import os
import sys
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import palette_check as pc  # noqa: E402

# Sharma, Wu, Dalal (2005), Color Res. Appl. 30(1):21-30, Table 1:
# (L1, a1, b1), (L2, a2, b2), expected Delta E00 (kL = kC = kH = 1).
SHARMA_2005 = [
    ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
    ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
    ((50.0000, 2.8361, -74.0200), (50.0000, 0.0000, -82.7485), 3.4412),
    ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
    ((50.0000, -1.1848, -84.8006), (50.0000, 0.0000, -82.7485), 1.0000),
    ((50.0000, -0.9009, -85.5211), (50.0000, 0.0000, -82.7485), 1.0000),
    ((50.0000, 0.0000, 0.0000), (50.0000, -1.0000, 2.0000), 2.3669),
    ((50.0000, -1.0000, 2.0000), (50.0000, 0.0000, 0.0000), 2.3669),
    ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0009), 7.1792),
    ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0010), 7.1792),
    ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0011), 7.2195),
    ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0012), 7.2195),
    ((50.0000, -0.0010, 2.4900), (50.0000, 0.0009, -2.4900), 4.8045),
    ((50.0000, -0.0010, 2.4900), (50.0000, 0.0010, -2.4900), 4.8045),
    ((50.0000, -0.0010, 2.4900), (50.0000, 0.0011, -2.4900), 4.7461),
    ((50.0000, 2.5000, 0.0000), (50.0000, 0.0000, -2.5000), 4.3065),
    ((50.0000, 2.5000, 0.0000), (73.0000, 25.0000, -18.0000), 27.1492),
    ((50.0000, 2.5000, 0.0000), (61.0000, -5.0000, 29.0000), 22.8977),
    ((50.0000, 2.5000, 0.0000), (56.0000, -27.0000, -3.0000), 31.9030),
    ((50.0000, 2.5000, 0.0000), (58.0000, 24.0000, 15.0000), 19.4535),
    ((50.0000, 2.5000, 0.0000), (50.0000, 3.1736, 0.5854), 1.0000),
    ((50.0000, 2.5000, 0.0000), (50.0000, 3.2972, 0.0000), 1.0000),
    ((50.0000, 2.5000, 0.0000), (50.0000, 1.8634, 0.5757), 1.0000),
    ((50.0000, 2.5000, 0.0000), (50.0000, 3.2592, 0.3350), 1.0000),
    ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
    ((63.0109, -31.0961, -5.8663), (62.8187, -29.7946, -4.0864), 1.2630),
    ((61.2901, 3.7196, -5.3901), (61.4292, 2.2480, -4.9620), 1.8731),
    ((35.0831, -44.1164, 3.7933), (35.0232, -40.0716, 1.5901), 1.8645),
    ((22.7233, 20.0904, -46.6940), (23.0331, 14.9730, -42.5619), 2.0373),
    ((36.4612, 47.8580, 18.3852), (36.2715, 50.5065, 21.2231), 1.4146),
    ((90.8027, -2.0831, 1.4410), (91.1528, -1.6435, 0.0447), 1.4441),
    ((90.9257, -0.5406, -0.9208), (88.6381, -0.8985, -0.7239), 1.5381),
    ((6.7747, -0.2908, -2.4247), (5.8714, -0.0985, -2.2286), 0.6377),
    ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
]

# The canonical "other jobs" set used by references/world.md section 12.
STUDIO_AGAINST = [
    ("GILT", "#C9A04C"), ("GILT_lit", "#E0BC6A"), ("WAX", "#8A1F24"), ("PARCHMENT", "#E8D9B5"),
    ("OAK", "#4A2E1B"), ("IRON", "#3B4048"), ("INK", "#1E1712"),
    ("infantry", "#B4432E"), ("spearmen", "#8B8F95"), ("archers", "#4F7A4A"),
    ("crossbows", "#6D8AA8"), ("cavalry", "#C9A76A"),
    ("Sound", "#4F7FD6"), ("Fine", "#8F6ADB"), ("Masterwork", "#E8A33C"),
]
WORLD_SET = [("self", "#FAF6EA"), ("ally", "#2042D8"), ("enemy", "#FF4F19"), ("neutral", "#786868")]
READABILITY_SET = [("self", "#9ADB6E"), ("ally", "#3A8FE0"), ("enemy", "#E0482A"), ("neutral", "#F3F1EC")]


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = pc.main(argv)
    return code, out.getvalue(), err.getvalue()


def test_ciede2000_sharma_2005_all_34_pairs():
    for i, (lab1, lab2, want) in enumerate(SHARMA_2005, 1):
        got = pc.ciede2000(lab1, lab2)
        assert abs(got - want) < 5e-5, "pair %d: %.4f != %.4f" % (i, got, want)


def test_ciede2000_symmetric_and_zero_on_identity():
    for lab1, lab2, _ in SHARMA_2005:
        assert math.isclose(pc.ciede2000(lab1, lab2), pc.ciede2000(lab2, lab1), abs_tol=1e-9)
        assert pc.ciede2000(lab1, lab1) == 0.0


def test_srgb_to_lab_anchors():
    for hexv, want in (("#FFFFFF", (100.0, 0.0, 0.0)), ("#000000", (0.0, 0.0, 0.0)),
                       ("#FF0000", (53.24, 80.09, 67.20)), ("#0000FF", (32.30, 79.19, -107.86)),
                       ("#808080", (53.59, 0.0, 0.0))):
        got = pc.hex_to_lab(hexv)
        assert all(abs(g - w) < 0.02 for g, w in zip(got, want)), (hexv, got)


def test_machado_keeps_greys_grey():
    # Every Machado row sums to ~1, so white, black and greys are unchanged.
    for cond in ("protan", "deutan", "tritan"):
        for row in pc.MACHADO_2009[cond]:
            assert abs(sum(row) - 1.0) < 1e-5, (cond, row)
        for g in ("#FFFFFF", "#808080", "#202020"):
            assert pc.delta_e(g, g, cond) == 0.0
            assert pc.ciede2000(pc.hex_to_lab(g), pc.hex_to_lab(g, cond)) < 0.05, (cond, g)


def test_cvd_collapses_the_classic_confusions():
    red, green = "#D03020", "#40A030"
    normal = pc.delta_e(red, green)
    assert normal > 50
    assert pc.delta_e(red, green, "deutan") < 0.5 * normal
    assert pc.delta_e(red, green, "protan") < 0.5 * normal
    blue, green2 = "#3060D0", "#30A080"   # a tritan confusion pair is blue/green, not red/green
    assert pc.delta_e(blue, green2, "tritan") < pc.delta_e(blue, green2)
    assert pc.delta_e(red, green, "tritan") > 0.6 * normal


def test_parse_hex_and_names():
    assert pc.parse_hex("#fff") == (1.0, 1.0, 1.0)
    assert pc.parse_hex("FAF6EA") == pc.parse_hex("#faf6ea")
    for bad in ("#12345", "#GGGGGG", "", "12"):
        try:
            pc.parse_hex(bad)
        except ValueError:
            continue
        raise AssertionError("accepted %r" % bad)
    assert pc.parse_named(["a=#fff", "b=#000000"], "--colours") == [("a", "#FFFFFF"), ("b", "#000000")]


def test_cli_exit_codes():
    assert run_cli(["--colours", "a=#FFFFFF", "b=#000000"])[0] == 0
    code, out, _ = run_cli(["--colours", "a=#808080", "b=#828282"])
    assert code == 1 and "PALETTE FAIL" in out
    assert run_cli(["--colours", "a=#12"])[0] == 2
    assert run_cli(["--colours", "a=#FFF", "a=#000"])[0] == 2          # repeated name
    assert run_cli(["--colours", "a=#FFF", "b=#000", "--allow", "a:zz"])[0] == 2


def test_allow_and_clash_conditions():
    base = ["--colours"] + ["%s=%s" % c for c in WORLD_SET] + ["--against", "PARCHMENT=#E8D9B5", "GILT=#C9A04C"]
    assert run_cli(base + ["--min-against", "15"])[0] == 1                       # self/PARCHMENT 10.4
    assert run_cli(base + ["--min-against", "15", "--allow", "self:PARCHMENT"])[0] == 1   # deutan enemy/GILT 6.7
    code, out, _ = run_cli(base + ["--min-against", "15", "--allow", "self:PARCHMENT",
                                   "--clash-conditions", "normal"])
    assert code == 0 and "worst CVD 6.7 deutan (enemy/GILT)" in out, out


def test_deterministic_output():
    argv = ["--colours"] + ["%s=%s" % c for c in READABILITY_SET] + ["--against"] + \
        ["%s=%s" % c for c in STUDIO_AGAINST] + ["--all"]
    assert run_cli(argv) == run_cli(argv)


def test_world_md_section_12_numbers():
    # references/world.md section 12 quotes these; change the doc and this test together.
    w = pc.check(WORLD_SET, STUDIO_AGAINST, 20, 15, {frozenset(("self", "PARCHMENT"))},
                 clash_conditions=("normal",))
    assert w["ok"]
    (d, a, b, _), cond = w["worst_cvd"]
    assert (round(d, 1), cond, {a, b}) == (23.7, "protan", {"enemy", "neutral"})
    n = w["conditions"]["normal"]
    assert round(n["worst_inner"][0], 1) == 30.2
    assert (round(n["worst_cross"][0], 1), n["worst_cross"][1:3]) == (16.9, ("neutral", "spearmen"))
    (d, a, b, _), cond = w["worst_cvd_clash"]
    assert (round(d, 1), cond, a, b) == (6.7, "deutan", "enemy", "GILT")
    assert [round(w["conditions"][c]["worst_inner"][0], 1) for c in pc.CONDITIONS] == [30.2, 23.7, 30.3, 26.5]
    assert round(pc.delta_e("#FAF6EA", "#E8D9B5"), 1) == 10.4       # the keyline case

    r = pc.check(READABILITY_SET, STUDIO_AGAINST, 20, 15, {frozenset(("neutral", "PARCHMENT"))},
                 clash_conditions=("normal",))
    assert not r["ok"]
    (d, a, b, _), cond = r["worst_cvd"]
    assert (round(d, 1), cond, {a, b}) == (18.4, "deutan", {"self", "enemy"})
    n = r["conditions"]["normal"]
    assert (round(n["worst_cross"][0], 1), n["worst_cross"][1:3]) == (7.2, ("ally", "Sound"))
    (d, a, b, _), cond = r["worst_cvd_clash"]
    assert (round(d, 1), cond, a, b) == (1.2, "deutan", "self", "GILT_lit")


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    for name, fn in tests:
        fn()
        print("PASS", name)
    print("PASS all %d tests" % len(tests))
