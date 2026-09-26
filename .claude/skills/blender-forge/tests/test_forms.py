"""Forms are watertight: loft with a tip, lathe with caps, sweep welded (lessons #15)."""
import math
import forge as F
from _util import check, watertight


def _diamond_sections(n=10, length=0.1):
    secs = []
    for i in range(n):
        t = i / n; w = 0.02 * (1 - t) + 0.001; h = 0.004 * (1 - t) + 0.0005
        secs.append([(-w, 0, t * length), (0, h, t * length), (w, 0, t * length), (0, -h, t * length)])
    return secs


def test_loft_tip_watertight():
    ob = F.loft("LoftTip", _diamond_sections(), tip=(0, 0, 0.1))
    watertight(ob, "loft raw")
    F.hard_surface(ob, 0.0005, 2)
    r = watertight(ob, "loft + hard_surface")
    return "tris=%d" % r["triangles"]


def test_loft_closed_ends_watertight():
    ob = F.loft("LoftCaps", _diamond_sections(), closed_start=True, closed_end=True)
    watertight(ob)


def test_lathe_caps_watertight():
    ring = F.lathe("Ring", [(0.010, 0.0), (0.015, 0.005), (0.012, 0.010)], 24, cap=True)
    watertight(ring, "lathe capped (no poles)")
    poles = F.lathe("Poles", [(0, 0), (0.010, 0.002), (0.008, 0.010), (0, 0.012)], 24)
    watertight(poles, "lathe with poles")
    F.subsurf(poles, 1)
    watertight(poles, "lathe + subsurf")
    open_ = F.lathe("Open", [(0.010, 0.0), (0.015, 0.005)], 24, cap=False)
    check(F.quality_report(open_)["open_boundary_edges"] > 0, "gate cannot fail: open lathe reads closed")


def test_sweep_welded():
    pts = [(0.01 * i, 0.004 * math.sin(i), 0.002 * i) for i in range(12)]
    wire = F.sweep("Wire", pts, radius=0.002, res=4, taper=[1 - 0.05 * i for i in range(12)])
    watertight(wire, "open tapered sweep")
    F.hard_surface(wire, 0.0003, 1, angle=45)
    watertight(wire, "sweep + hard_surface")
    loop = [(0.03 * math.cos(a), 0.03 * math.sin(a), 0.0) for a in
            [2 * math.pi * k / 24 for k in range(24)]]
    ring = F.sweep("Loop", loop, radius=0.002, res=4, closed=True)
    watertight(ring, "cyclic sweep")
    helix = F.sweep("Helix", F.helix((0, 0), 0.02, 0, 0.1, 3, 16), radius=0.0012, res=3)
    watertight(helix, "helix sweep")
