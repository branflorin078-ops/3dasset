"""Shared helpers for the blender-forge regression suite."""
import os, struct
import bpy, bmesh
import numpy as np
import forge as F

OUT = None  # set by run_tests.py


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def watertight(ob, label=None):
    """The QA topology gates on the EVALUATED mesh (modifiers included)."""
    r = F.quality_report(ob)
    bad = {k: r[k] for k in ("non_manifold_edges", "open_boundary_edges", "loose_verts",
                             "degenerate_faces") if r[k]}
    check(not bad, "%s not watertight: %s" % (label or ob.name, bad))
    return r


def shells(ob):
    """Connected components of the evaluated mesh (closed parts inside one object)."""
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = ev.to_mesh(); bm = bmesh.new(); bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    seen, count = set(), 0
    for v in bm.verts:
        if v.index in seen:
            continue
        count += 1; stack = [v]
        while stack:
            x = stack.pop()
            if x.index in seen:
                continue
            seen.add(x.index)
            stack.extend(e.other_vert(x) for e in x.link_edges if e.other_vert(x).index not in seen)
    bm.free(); ev.to_mesh_clear()
    return count


def volume(ob):
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = ev.to_mesh(); bm = bmesh.new(); bm.from_mesh(me)
    v = bm.calc_volume(signed=False)
    bm.free(); ev.to_mesh_clear()
    return v


def png_header(path):
    """(bit_depth, colour_type) from the IHDR chunk."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    check(head[:8] == b"\x89PNG\r\n\x1a\n", "%s is not a PNG" % path)
    return head[24], head[25]


def byte_pixels(path):
    """Raw 0..1 byte values of an 8-bit PNG (Blender does not colour-manage the
    pixels of BYTE images). Returns an (N, 4) float array."""
    im = bpy.data.images.load(path, check_existing=False)
    check(not im.is_float, "%s loaded as float (expected an 8-bit PNG)" % path)
    a = np.empty(im.size[0] * im.size[1] * 4, np.float32); im.pixels.foreach_get(a)
    bpy.data.images.remove(im)
    return a.reshape(-1, 4)


def srgb_decode(v):
    v = np.asarray(v, np.float64)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def outdir(*parts):
    p = os.path.join(OUT, *parts)
    os.makedirs(p, exist_ok=True)
    return p
