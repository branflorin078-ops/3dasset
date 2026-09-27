"""Palette separation check for design-forge: CIEDE2000 under normal vision and
simulated protanopia, deuteranopia and tritanopia. Pure Python, no dependencies,
deterministic (same input -> same output, byte for byte).

    python palette_check.py --colours self=#FAF6EA ally=#2042D8 enemy=#FF4F19 neutral=#786868
    python palette_check.py --colours self=#... ally=#... --against GILT=#C9A04C Sound=#4F7FD6 \
        --min 20 --min-against 15 --clash-conditions normal --allow self:PARCHMENT [--all] [--json]

What it answers: "can a player tell these colours apart, including players with a
colour-vision deficiency (CVD), and do they collide with colours that already have
another job?" For each condition it prints
  - the worst pair INSIDE --colours (every pair is checked), and
  - the worst clash between a --colours entry and an --against entry.
--min holds inner pairs in all four conditions; --min-against holds clashes in the
--clash-conditions (default all four; every condition is always reported). --allow
exempts a pair that another rule already fixes (say which rule in the spec).
The last line is a verdict: PALETTE OK / PALETTE FAIL, then the exit code is
0 (all pass), 1 (a pair is below a threshold) or 2 (bad input).

Method (stated so the numbers can be reproduced anywhere):
  1. sRGB hex -> linear RGB (IEC 61966-2-1 transfer curve).
  2. CVD simulation: Machado, Oliveira & Fernandes 2009 matrices at severity 1.0
     (full dichromacy), applied to LINEAR RGB, result clamped to [0, 1].
     G. M. Machado, M. M. Oliveira, L. A. F. Fernandes, "A Physiologically-based
     Model for Simulation of Color Vision Deficiency", IEEE Transactions on
     Visualization and Computer Graphics 15(6):1291-1298, 2009. Matrices from the
     authors' published per-severity table. Tritanopia is the rarest deficiency and
     the least tested case of any simulation model: read tritan numbers as an estimate.
  3. Linear RGB -> CIE XYZ (sRGB primaries, D65) -> CIELAB (D65 white, exact CIE
     constants epsilon = 216/24389, kappa = 24389/27).
  4. Colour difference: CIEDE2000 with kL = kC = kH = 1, implemented as in
     G. Sharma, W. Wu, E. N. Dalal, "The CIEDE2000 color-difference formula:
     Implementation notes, supplementary test data, and mathematical observations",
     Color Research and Application 30(1):21-30, 2005 (tests/test_palette_check.py
     reproduces its 34 reference pairs to 4 decimals).

Why the default --min is 15 (Delta E00):
  - 1 is about one just-noticeable difference for large patches side by side; a map
    marker is a 6 px line or a 16-44 px icon, seen alone, on painted ground, often
    moving. Telling colours apart there needs many JNDs, not one.
  - 15 is the studio's existing floor for "different job, never confused": the reserved
    radius around relationship colours and the tincture / sigil distance
    (game-art-director references/readability.md section 4, rules 1-2; design-forge
    references/alliance.md tinctures). The default equals it so the tool and the art
    rules agree.
  - Colours that must be NAMED at icon size (relationship classes, line accents) use
    --min 20: ui-forge references/components.md section 4 counts a pair below 20 as
    colliding at icon size. design-forge references/world.md section 12 runs with 20.
  - No threshold replaces shape coding: a pass here is necessary, never sufficient.
"""
import argparse
import itertools
import json
import math
import re
import sys

# Machado et al. 2009, severity 1.0, rows produce linear R, G, B.
MACHADO_2009 = {
    "protan": ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}
CONDITIONS = ("normal", "protan", "deutan", "tritan")

# sRGB (IEC 61966-2-1) linear RGB -> XYZ, D65; white (1,1,1) -> WHITE_D65.
RGB_TO_XYZ = ((0.4124564, 0.3575761, 0.1804375),
              (0.2126729, 0.7151522, 0.0721750),
              (0.0193339, 0.1191920, 0.9503041))
WHITE_D65 = (0.95047, 1.0, 1.08883)
EPSILON = 216.0 / 24389.0
KAPPA = 24389.0 / 27.0

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")


def parse_hex(text):
    """'#FAF6EA', 'faf6ea' or '#FFF' -> (r, g, b) in 0..1 (sRGB, gamma-encoded)."""
    m = HEX_RE.match(text.strip())
    if not m:
        raise ValueError("not a hex colour: %r" % text)
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def simulate(linear_rgb, condition):
    """Linear RGB as seen under `condition` (normal returns the input)."""
    if condition == "normal":
        return tuple(linear_rgb)
    m = MACHADO_2009[condition]
    return tuple(min(1.0, max(0.0, sum(m[i][j] * linear_rgb[j] for j in range(3)))) for i in range(3))


def linear_to_lab(lin):
    xyz = [sum(RGB_TO_XYZ[i][j] * lin[j] for j in range(3)) for i in range(3)]

    def f(t):
        return t ** (1.0 / 3.0) if t > EPSILON else (KAPPA * t + 16.0) / 116.0

    fx, fy, fz = (f(xyz[i] / WHITE_D65[i]) for i in range(3))
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def hex_to_lab(text, condition="normal"):
    lin = tuple(srgb_to_linear(c) for c in parse_hex(text))
    return linear_to_lab(simulate(lin, condition))


def ciede2000(lab1, lab2, kl=1.0, kc=1.0, kh=1.0):
    """CIEDE2000 colour difference (Sharma, Wu, Dalal 2005, equations 1-17)."""
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c_bar = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2.0
    c_bar7 = c_bar ** 7
    g = 0.5 * (1.0 - math.sqrt(c_bar7 / (c_bar7 + 25.0 ** 7)))
    a1p, a2p = (1.0 + g) * a1, (1.0 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)

    def hue(b, ap):
        return 0.0 if (b == 0 and ap == 0) else math.degrees(math.atan2(b, ap)) % 360.0

    h1p, h2p = hue(b1, a1p), hue(b2, a2p)
    d_lp = l2 - l1
    d_cp = c2p - c1p
    if c1p * c2p == 0:
        d_hp = 0.0
    else:
        d_hp = h2p - h1p
        if d_hp > 180.0:
            d_hp -= 360.0
        elif d_hp < -180.0:
            d_hp += 360.0
    d_hp_big = 2.0 * math.sqrt(c1p * c2p) * math.sin(math.radians(d_hp / 2.0))

    l_bar_p = (l1 + l2) / 2.0
    c_bar_p = (c1p + c2p) / 2.0
    if c1p * c2p == 0:
        h_bar_p = h1p + h2p
    elif abs(h1p - h2p) <= 180.0:
        h_bar_p = (h1p + h2p) / 2.0
    elif h1p + h2p < 360.0:
        h_bar_p = (h1p + h2p + 360.0) / 2.0
    else:
        h_bar_p = (h1p + h2p - 360.0) / 2.0

    t = (1.0 - 0.17 * math.cos(math.radians(h_bar_p - 30.0))
         + 0.24 * math.cos(math.radians(2.0 * h_bar_p))
         + 0.32 * math.cos(math.radians(3.0 * h_bar_p + 6.0))
         - 0.20 * math.cos(math.radians(4.0 * h_bar_p - 63.0)))
    d_theta = 30.0 * math.exp(-(((h_bar_p - 275.0) / 25.0) ** 2))
    c_bar_p7 = c_bar_p ** 7
    r_c = 2.0 * math.sqrt(c_bar_p7 / (c_bar_p7 + 25.0 ** 7))
    s_l = 1.0 + (0.015 * (l_bar_p - 50.0) ** 2) / math.sqrt(20.0 + (l_bar_p - 50.0) ** 2)
    s_c = 1.0 + 0.045 * c_bar_p
    s_h = 1.0 + 0.015 * c_bar_p * t
    r_t = -math.sin(math.radians(2.0 * d_theta)) * r_c
    tl, tc, th = d_lp / (kl * s_l), d_cp / (kc * s_c), d_hp_big / (kh * s_h)
    return math.sqrt(tl * tl + tc * tc + th * th + r_t * tc * th)


def delta_e(hex1, hex2, condition="normal"):
    return ciede2000(hex_to_lab(hex1, condition), hex_to_lab(hex2, condition))


def parse_named(items, flag):
    """['self=#FAF6EA', ...] -> ordered list of (name, '#FAF6EA')."""
    out, seen = [], set()
    for item in items or []:
        if "=" not in item:
            raise ValueError("%s expects name=#RRGGBB, got %r" % (flag, item))
        name, value = item.split("=", 1)
        name = name.strip()
        if not name or name in seen:
            raise ValueError("%s: empty or repeated name %r" % (flag, name))
        parse_hex(value)
        seen.add(name)
        h = value.strip().lstrip("#").upper()
        out.append((name, "#" + (h if len(h) == 6 else "".join(c * 2 for c in h))))
    return out


def parse_allow(items, colour_names, against_names):
    allow = set()
    for item in items or []:
        a, sep, b = item.partition(":")
        if not sep:
            raise ValueError("--allow expects name:name, got %r" % item)
        known = set(colour_names) | set(against_names)
        for n in (a, b):
            if n not in known:
                raise ValueError("--allow names an unknown colour %r" % n)
        allow.add(frozenset((a, b)))
    return allow


def check(colours, against=(), min_de=15.0, min_against=15.0, allow=frozenset(),
          conditions=CONDITIONS, clash_conditions=CONDITIONS):
    """Every pair inside `colours` and every colours x against pair, per condition.

    `min_de` applies to inner pairs in every condition; `min_against` applies to
    clashes in `clash_conditions` only (the others are still reported).
    Returns a dict: per condition the sorted inner pairs and cross pairs
    (de, name_a, name_b, allowed), the worst of each, and an overall `ok`.
    """
    result = {"conditions": {}, "failures": [], "min": min_de, "min_against": min_against,
              "clash_conditions": tuple(c for c in conditions if c in clash_conditions)}
    for cond in conditions:
        labs = {n: hex_to_lab(h, cond) for n, h in list(colours) + list(against)}
        inner = sorted((round(ciede2000(labs[a], labs[b]), 6), a, b, frozenset((a, b)) in allow)
                       for (a, _), (b, _) in itertools.combinations(colours, 2))
        cross = sorted((round(ciede2000(labs[a], labs[b]), 6), a, b, frozenset((a, b)) in allow)
                       for (a, _) in colours for (b, _) in against)
        worst_inner = next((p for p in inner if not p[3]), None)
        worst_cross = next((p for p in cross if not p[3]), None)
        result["conditions"][cond] = {"inner": inner, "cross": cross,
                                      "worst_inner": worst_inner, "worst_cross": worst_cross}
        for p in inner:
            if not p[3] and p[0] < min_de:
                result["failures"].append((cond, "pair") + p[:3])
        for p in cross:
            if cond in clash_conditions and not p[3] and p[0] < min_against:
                result["failures"].append((cond, "clash") + p[:3])
    for key, kind in (("worst_cvd", "worst_inner"), ("worst_cvd_clash", "worst_cross")):
        cvd = [(result["conditions"][c][kind], c) for c in conditions
               if c != "normal" and result["conditions"][c][kind]]
        result[key] = min(cvd) if cvd else None
    result["ok"] = not result["failures"]
    return result


def _pair(p):
    return "-" if p is None else "%-22s %5.1f" % ("%s / %s" % (p[1], p[2]), p[0])


def report(res, colours, against, show_all=False):
    lines = ["colours: " + "  ".join("%s %s" % c for c in colours)]
    if against:
        lines.append("against: " + "  ".join("%s %s" % c for c in against))
    lines.append("method: Machado 2009 severity 1.0 on linear sRGB; CIELAB D65; CIEDE2000 (Sharma 2005)")
    lines.append("%-7s %-28s %s" % ("cond", "worst pair (dE00)", "worst clash vs --against (dE00)" if against else ""))
    for cond, data in res["conditions"].items():
        lines.append("%-7s %-28s %s" % (cond, _pair(data["worst_inner"]),
                                        _pair(data["worst_cross"]) if against else ""))
        if show_all:
            lines.append("        pairs: " + ", ".join("%s/%s %.1f%s" % (a, b, d, " (allowed)" if al else "")
                                                     for d, a, b, al in data["inner"]))
            if against:
                lines.append("        clashes: " + ", ".join("%s/%s %.1f%s" % (a, b, d, " (allowed)" if al else "")
                                                         for d, a, b, al in data["cross"]))
    allowed = ["%s/%s %.1f %s" % (a, b, d, c) for c, data in res["conditions"].items()
               for d, a, b, al in data["inner"] + data["cross"] if al]
    if allowed:
        lines.append("allowed (exempt; the spec gives the reason): " + "; ".join(allowed))
    n = res["conditions"].get("normal")
    pairs, clashes = [], []
    if n and n["worst_inner"]:
        pairs.append("normal %.1f" % n["worst_inner"][0])
    if res["worst_cvd"]:
        (d, a, b, _), c = res["worst_cvd"]
        pairs.append("worst CVD %.1f %s (%s/%s)" % (d, c, a, b))
    if against and n and n["worst_cross"]:
        clashes.append("normal %.1f (%s/%s)" % (n["worst_cross"][0], n["worst_cross"][1], n["worst_cross"][2]))
    if against and res["worst_cvd_clash"]:
        (d, a, b, _), c = res["worst_cvd_clash"]
        clashes.append("worst CVD %.1f %s (%s/%s)" % (d, c, a, b))
    summary = "pairs " + ", ".join(pairs) + ("; clashes " + ", ".join(clashes) if clashes else "")
    rule = "min %g" % res["min"]
    if against:
        rule += ", min-against %g in %s" % (res["min_against"], "/".join(res["clash_conditions"]) or "none")
    if res["ok"]:
        lines.append("PALETTE OK - %s [%s]" % (summary, rule))
    else:
        lines.append("PALETTE FAIL - %d below threshold [%s]: %s" % (
            len(res["failures"]), rule,
            "; ".join("%s %s %s/%s %.1f" % (c, k, a, b, d) for c, k, d, a, b in res["failures"][:8])))
    return "\n".join(lines)


def to_json(res, colours, against):
    def pl(p):
        return None if p is None else {"de00": round(p[0], 2), "a": p[1], "b": p[2]}
    return json.dumps({
        "colours": dict(colours), "against": dict(against),
        "min": res["min"], "min_against": res["min_against"], "ok": res["ok"],
        "clash_conditions": list(res["clash_conditions"]),
        "conditions": {c: {"worst_pair": pl(d["worst_inner"]), "worst_clash": pl(d["worst_cross"])}
                       for c, d in res["conditions"].items()},
        "failures": [{"condition": c, "kind": k, "de00": round(d, 2), "a": a, "b": b}
                     for c, k, d, a, b in res["failures"]],
    }, indent=1, sort_keys=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--colours", "--colors", nargs="+", required=True, metavar="NAME=#HEX",
                    help="the palette under test; every pair must stay >= --min apart")
    ap.add_argument("--against", nargs="*", default=[], metavar="NAME=#HEX",
                    help="colours with other jobs (tokens, line accents, rarity) to check clashes with")
    ap.add_argument("--min", type=float, default=15.0, help="min dE00 inside --colours, every condition (15)")
    ap.add_argument("--min-against", type=float, default=None,
                    help="min dE00 colours vs --against, every condition (default: same as --min)")
    ap.add_argument("--clash-conditions", nargs="+", choices=CONDITIONS, default=list(CONDITIONS),
                    help="conditions in which --min-against is enforced (default: all four; all are reported)")
    ap.add_argument("--allow", nargs="*", default=[], metavar="A:B",
                    help="exempt a known, mitigated pair (e.g. self:PARCHMENT because of a keyline)")
    ap.add_argument("--all", action="store_true", help="print every pair, not only the worst")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    try:
        colours = parse_named(args.colours, "--colours")
        against = parse_named(args.against, "--against")
        if len(colours) < 2 and not against:
            raise ValueError("give at least two --colours, or one plus --against")
        clash_names = {n for n, _ in colours} & {n for n, _ in against}
        if clash_names:
            raise ValueError("a name is in both --colours and --against: %s" % ", ".join(sorted(clash_names)))
        allow = parse_allow(args.allow, [n for n, _ in colours], [n for n, _ in against])
    except ValueError as e:
        print("palette_check: %s" % e, file=sys.stderr)
        return 2
    min_against = args.min if args.min_against is None else args.min_against
    res = check(colours, against, args.min, min_against, allow, CONDITIONS, tuple(args.clash_conditions))
    print(to_json(res, colours, against) if args.json else report(res, colours, against, args.all))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
