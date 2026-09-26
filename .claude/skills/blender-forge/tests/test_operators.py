"""Construction operators: helm_shell, boolean_cut (+ slot_cutter), plate,
rivet_row, strap / buckle / strap_buckle, gem_brilliant, gem_cabochon.
Every operator must produce WATERTIGHT parts (qa.md gates) with the expected
structure — never a stack of primitives."""
import math
import bpy
from mathutils import Vector
import forge as F
from _util import check, watertight, shells, volume


def _verts(ob):
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = ev.to_mesh(); pts = [ob.matrix_world @ v.co for v in me.vertices]; ev.to_mesh_clear()
    return pts


# ── helm_shell ───────────────────────────────────────────────────────────────
def test_helm_shell_watertight():
    R, TAIL, FLARE, ROLL = 0.105, 0.07, 0.035, 0.0022
    helm = F.helm_shell("Sallet", radius=R, height=0.15, thickness=0.0018,
                        tail=TAIL, tail_flare=FLARE, tail_width=140, roll=ROLL)
    r = watertight(helm, "sallet")
    check(shells(helm) == 2, "expected bowl + rolled rim = 2 shells, got %d" % shells(helm))
    pts = _verts(helm)
    ymin, ymax = min(p.y for p in pts), max(p.y for p in pts)
    zmin = min(p.z for p in pts)
    check(ymax - abs(ymin) > 0.5 * FLARE, "tail does not flare to the back (+Y): ymin=%.3f ymax=%.3f" % (ymin, ymax))
    check(zmin < -0.8 * TAIL, "tail does not drop: zmin=%.3f" % zmin)
    front = [p for p in pts if p.y < -0.8 * R]
    check(front and min(p.z for p in front) > -0.01, "the face side must not carry the tail")
    F.hard_surface(helm, 0.0006, 2)
    watertight(helm, "sallet + hard_surface")
    kettle = F.helm_shell("Kettle", radius=0.1, height=0.12, brim=0.06, roll=0.002)
    watertight(kettle, "kettle hat")
    w = kettle.dimensions.x
    check(w > 2 * (0.1 + 0.05), "brim too narrow: %.3f" % w)
    basc = F.helm_shell("Bascinet", radius=0.1, height=0.17, apex=0.25, roll=0.0)
    watertight(basc, "bascinet")
    check(shells(basc) == 1, "roll=0 must not add a rim")
    return "sallet tris=%d" % r["triangles"]


# ── boolean_cut ──────────────────────────────────────────────────────────────
def test_boolean_cut_visor_slits():
    helm = F.helm_shell("Helm", radius=0.105, height=0.16, thickness=0.0018, roll=0.0)
    F.hard_surface(helm, 0.0005, 2)
    v0 = volume(helm)
    slits = []
    for side in (-1, 1):                                   # two sights either side of the nose
        c = F.slot_cutter("Sight%d" % side, length=0.055, width=0.007, depth=0.06)
        c.location = (side * 0.034, -0.105, 0.075); c.rotation_euler = (0, math.radians(side * -6), 0)
        slits.append(c)
    F.boolean_cut(helm, slits)
    r = watertight(helm, "helm after sights")
    check(not any(o.name.startswith("Sight") for o in bpy.data.objects), "cutters left in the scene")
    v1 = volume(helm)
    check(v1 < v0 - 1e-8, "no material removed: %.3e -> %.3e" % (v0, v1))
    check(any(m.type == 'BEVEL' for m in helm.modifiers), "cut rims are not bevelled")
    check(helm.modifiers[0].type == 'BEVEL', "the boolean must be applied, bevel first in the stack")
    # a plain part without a bevel gets one added
    ring = F.lathe("Pauldron", [(0.05, 0.0), (0.06, 0.0), (0.06, 0.04), (0.05, 0.04)], 48, cap=True)
    hole = F.slot_cutter("Hole", length=0.008, width=0.008, depth=0.05)   # round hole
    hole.location = (0.055, 0, 0.02); hole.rotation_euler = (0, 0, math.radians(90))
    F.boolean_cut(ring, hole)
    watertight(ring, "ring with rivet hole")
    check(any(m.type == 'BEVEL' for m in ring.modifiers), "bevel cleanup not added")
    return "tris=%d  volume -%.1f%%" % (r["triangles"], 100 * (1 - v1 / v0))


def test_boolean_cut_multi_shell():
    """A helm WITH its rolled rim is two intersecting closed shells: EXACT on
    the whole object produced inside-out garbage (volume UP, 20 non-manifold
    edges, blades sticking out of the face). boolean_cut must cut per shell."""
    helm = F.helm_shell("Sallet", radius=0.104, height=0.150, thickness=0.0018, squareness=2.3,
                        tail=0.085, tail_flare=0.045, tail_width=150, roll=0.0024)
    F.hard_surface(helm, 0.0006, 2)
    v0, s0 = volume(helm), shells(helm)
    cs = []
    for side in (-1, 1):
        c = F.slot_cutter("Sight%d" % side, length=0.062, width=0.0085, depth=0.08)
        c.location = (side * 0.036, -0.10, 0.058); c.rotation_euler = (0, math.radians(side * 7), 0)
        cs.append(c)
    F.boolean_cut(helm, cs)
    r = watertight(helm, "rolled sallet after sights")
    v1 = volume(helm)
    check(v1 < v0, "volume went UP %.3e -> %.3e (inside-out result)" % (v0, v1))
    check(shells(helm) == s0, "shell count changed %d -> %d" % (s0, shells(helm)))
    pts = _verts(helm)
    check(min(p.y for p in pts) > -0.104 - 0.006, "geometry sticks out of the face (min y %.3f)" % min(p.y for p in pts))
    return "tris=%d volume -%.2f%%" % (r["triangles"], 100 * (1 - v1 / v0))


# ── plate ────────────────────────────────────────────────────────────────────
def _arc(width=0.2, depth=0.035, n=9):
    return [(width * (i / (n - 1) - 0.5), -depth * (1 - (2 * i / (n - 1) - 1) ** 2)) for i in range(n)]


def test_plate_single_watertight():
    p = F.plate("Breastplate", _arc(0.3, 0.06), height=0.32, thickness=0.0016, bulge=0.02,
                taper=0.18, roll=0.003, roll_edges=('top',))
    r = watertight(p, "breastplate")
    check(shells(p) == 2, "plate + top roll = 2 shells, got %d" % shells(p))
    pts = _verts(p)
    check(min(p_.y for p_ in pts) < -0.06, "profile curvature/bulge not toward the viewer (-Y)")
    return "tris=%d" % r["triangles"]


def test_plate_lames_watertight():
    p = F.plate("Fauld", _arc(0.34, 0.05), height=0.16, thickness=0.0016, lames=4,
                roll=0.0025, roll_edges=('top', 'bottom'))
    watertight(p, "fauld")
    n = shells(p)
    check(n == 6, "4 lames + top roll + bottom roll = 6 shells, got %d" % n)
    check(abs(p.dimensions.z - 0.16) < 0.02, "fauld height %.3f" % p.dimensions.z)
    return "shells=%d" % n


# ── rivet_row ────────────────────────────────────────────────────────────────
def test_rivet_row_straight():
    row = F.rivet_row("Rivets", [(0, 0, 0), (0.2, 0, 0)], count=6, head_r=0.004,
                      head_h=0.0022, normal=(0, -1, 0))
    watertight(row, "rivet row")
    check(shells(row) == 6, "6 rivets -> 6 shells, got %d" % shells(row))
    xs = sorted(list(row["forge_rivet_pts"])[0::3])       # IDProperty arrays: list() before stepping
    gaps = [b - a for a, b in zip(xs, xs[1:])]
    check(max(gaps) - min(gaps) < 1e-6, "uneven spacing %s" % gaps)
    pts = _verts(row)
    check(min(p.y for p in pts) < -0.0015, "heads do not face -Y")
    inst = F.rivet_row("Inst", [(0, 0, 0), (0.1, 0, 0.05)], count=4, join=False)
    check(len(inst) == 4 and len({o.data.name for o in inst}) == 1, "instances must share ONE mesh")
    return "gap=%.4f" % gaps[0]


def test_rivet_row_on_surface():
    helm = F.helm_shell("Helm", radius=0.105, height=0.15, roll=0.0)
    path = [(0.106 * math.cos(a), 0.106 * math.sin(a), 0.02) for a in
            [math.radians(d) for d in range(200, 341, 10)]]
    row = F.rivet_row("BrowRivets", path, count=7, surface=helm)
    watertight(row, "surface rivets")
    check(shells(row) == 7, "7 rivets expected")
    pts = list(row["forge_rivet_pts"]); nrm = list(row["forge_rivet_nrm"])
    for k in range(7):
        p = Vector(pts[3 * k:3 * k + 3]); n = Vector(nrm[3 * k:3 * k + 3])
        radial = Vector((p.x, p.y, 0)).normalized()
        check(n.dot(radial) > 0.8, "rivet %d not normal to the bowl (dot %.2f)" % (k, n.dot(radial)))


# ── strap / buckle ───────────────────────────────────────────────────────────
def test_strap_buckle_watertight():
    path = [(0.0, 0.0, 0.0), (0.08, 0.0, 0.01), (0.16, 0.0, 0.0), (0.24, 0.0, -0.01), (0.3, 0.0, 0.0)]
    st = F.strap("Strap", path, width=0.025, thickness=0.003, tip='round')
    watertight(st, "strap")
    check(shells(st) == 1, "strap must be one closed shell")
    check(abs(st.dimensions.y - 0.025) < 0.003, "strap width %.4f" % st.dimensions.y)
    bk = F.buckle("Buckle", width=0.032, height=0.028, wire_r=0.0022)
    watertight(bk, "buckle")
    check(shells(bk) == 3, "frame + bar + prong = 3 shells, got %d" % shells(bk))
    s2, b2 = F.strap_buckle("Belt", path, width=0.025, thickness=0.003, at=0.35)
    watertight(s2, "belt strap"); watertight(b2, "belt buckle")
    inner = b2["forge_inner_width"]
    check(inner > 0.025, "buckle opening %.4f narrower than the strap" % inner)


# ── gems ─────────────────────────────────────────────────────────────────────
def _max_nonplanar(ob):
    me = ob.data; worst = 0.0
    for poly in me.polygons:
        if len(poly.vertices) <= 3:
            continue
        c = poly.center; n = poly.normal
        worst = max(worst, max(abs((me.vertices[v].co - c).dot(n)) for v in poly.vertices))
    return worst


def test_gem_brilliant_facets():
    D = 0.01
    g = F.gem_brilliant("Brilliant", diameter=D)
    watertight(g, "brilliant")
    nf = len(g.data.polygons)
    check(nf == 73, "round brilliant (8 mains) = 73 faces incl. 16 girdle facets, got %d" % nf)
    check(not any(p.use_smooth for p in g.data.polygons), "facets must be flat-shaded")
    npl = _max_nonplanar(g)
    check(npl < 1e-6 * D, "a facet is not planar (%.2e m)" % npl)
    table = max(v.co.z for v in g.data.vertices)
    top = [v.co for v in g.data.vertices if abs(v.co.z - table) < 1e-9]
    tw = max(Vector((p.x, p.y, 0)).length for p in top) * 2
    check(abs(tw / D - 0.56) < 0.03, "table %.2f of diameter" % (tw / D))
    check(abs(g.dimensions.x - D) / D < 0.02, "diameter %.4f" % g.dimensions.x)
    return "faces=%d depth=%.1f%%" % (nf, 100 * g.dimensions.z / D)


def test_gem_cabochon_watertight():
    g = F.gem_cabochon("Cabochon", rx=0.008, ry=0.006, height=0.005)
    watertight(g, "cabochon")
    d = g.dimensions
    check(abs(d.x - 0.016) < 0.0005 and abs(d.y - 0.012) < 0.0005, "outline %.4f x %.4f" % (d.x, d.y))
    check(all(p.use_smooth for p in g.data.polygons), "cabochon must be smooth-shaded")
