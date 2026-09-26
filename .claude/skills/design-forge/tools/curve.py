"""Level-curve designer for design-forge — design by player time, derive the numbers.

    python curve.py --levels 25 --first 1m --last 14d --shape phased [--csv out.csv]
    python curve.py --levels 10 --first 30s --last 8h --shape geometric

Designers think in "how long until level L feels earned", not in raw growth
factors. Give the first and last upgrade times and a shape; it prints the
per-level duration, the cumulative time, and the growth factor between
levels, so the spec's tuning table comes from a stated intent.

Shapes
  geometric  constant ratio g between levels (T_L = T_1 * g^(L-1))
  phased     three phases — fast onboarding (first 30% of levels, ratio 1.6x
             the mean log-step), a steady middle, and a late plateau
             (last 20%, ratio 0.6x) so the top levels are long but do not
             explode; the endpoints still hit --first and --last exactly
  poly       T_L = T_1 + (T_N - T_1) * ((L-1)/(N-1))^p with --power p (2.5)

Durations accept s, m, h, d suffixes. Speed-up math: --help-cut 0.01 --helps 20
applies alliance-help style reductions (each help cuts max(cut*T, floor)) and
prints the effective time too (--help-floor 60s).
"""
import argparse
import math
import sys

UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def parse_dur(s):
    s = s.strip().lower()
    if s[-1] in UNITS:
        return float(s[:-1]) * UNITS[s[-1]]
    return float(s)


def fmt(sec):
    sec = int(round(sec))
    if sec < 60:
        return "%ds" % sec
    if sec < 3600:
        return "%dm%02ds" % (sec // 60, sec % 60)
    if sec < 86400:
        return "%dh%02dm" % (sec // 3600, (sec % 3600) // 60)
    return "%dd%02dh" % (sec // 86400, (sec % 86400) // 3600)


def curve(n, first, last, shape="phased", power=2.5):
    if n < 2:
        return [first]
    if shape == "geometric":
        g = (last / first) ** (1.0 / (n - 1))
        return [first * g ** i for i in range(n)]
    if shape == "poly":
        return [first + (last - first) * (i / (n - 1)) ** power for i in range(n)]
    if shape == "phased":
        # weights for each of the n-1 log-steps, then scale to hit `last`
        w = []
        for i in range(n - 1):
            f = i / (n - 1)
            w.append(1.6 if f < 0.3 else (0.6 if f >= 0.8 else 1.0))
        total = math.log(last / first)
        k = total / sum(w)
        out, t = [first], first
        for wi in w:
            t *= math.exp(k * wi)
            out.append(t)
        return out
    raise ValueError(shape)


def with_help(t, helps, cut, floor):
    for _ in range(helps):
        t -= max(cut * t, floor)
        if t <= 0:
            return 0.0
    return t


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--levels", type=int, required=True)
    ap.add_argument("--first", required=True)
    ap.add_argument("--last", required=True)
    ap.add_argument("--shape", default="phased", choices=["geometric", "phased", "poly"])
    ap.add_argument("--power", type=float, default=2.5)
    ap.add_argument("--helps", type=int, default=0)
    ap.add_argument("--help-cut", type=float, default=0.01)
    ap.add_argument("--help-floor", default="60s")
    ap.add_argument("--csv")
    a = ap.parse_args(argv)
    first, last = parse_dur(a.first), parse_dur(a.last)
    ts = curve(a.levels, first, last, a.shape, a.power)
    floor = parse_dur(a.help_floor)
    cum = 0.0
    lines = []
    print("%5s %12s %8s %14s%s" % ("level", "duration", "ratio", "cumulative",
                                   "   with %d helps" % a.helps if a.helps else ""))
    for i, t in enumerate(ts):
        cum += t
        ratio = (t / ts[i - 1]) if i else float("nan")
        extra = "   %12s" % fmt(with_help(t, a.helps, a.help_cut, floor)) if a.helps else ""
        print("%5d %12s %8s %14s%s" % (i + 1, fmt(t), "-" if i == 0 else "%.3f" % ratio, fmt(cum), extra))
        lines.append((i + 1, round(t), round(ratio, 4) if i else "", round(cum)))
    print("TOTAL %s to max (%.1f days of build queue)" % (fmt(cum), cum / 86400))
    if a.csv:
        with open(a.csv, "w", encoding="utf-8") as fh:
            fh.write("level,seconds,ratio,cumulative_seconds\n")
            for ln in lines:
                fh.write(",".join(str(x) for x in ln) + "\n")
        print("CSV " + a.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
