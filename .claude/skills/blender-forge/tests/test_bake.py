"""Bake + export: a tiny glowing asset of KNOWN emission must bake to that exact
strength (not merely '> 1': the 5.x colourspace regression read 3.054 for a true
13.383, which passes '> 1'), and survive the GLB round trip."""
import os
import bpy
import numpy as np
import forge as F
from _util import check, outdir, png_header, byte_pixels, srgb_decode

S = 5.0          # analytic emission peak (white x S on the upper half, S/2 below)


def _glowing_parts():
    body = F.lathe("Body", [(0, 0), (0.02, 0.0), (0.02, 0.08), (0, 0.08)], 24)
    F.hard_surface(body, 0.001, 2)
    # a curve-converted wire arrives WITH UVs, the lathe WITHOUT: lessons #14 trap
    wire = F.sweep("Wire", F.helix((0, 0), 0.0215, 0.005, 0.075, 3, 16), radius=0.0015, res=4)
    m = F.mat_metal("GlowBody", '#7E7466')
    F.set_in(m.p, F.IN["emit_col"], (1, 1, 1, 1))
    upper = m.math('GREATER_THAN', m.obj_axis('Z'), 0.04)
    m.link(m.math('MULTIPLY', m.math('ADD', 0.5, m.math('MULTIPLY', upper, 0.5)), S),
           F.get_in(m.p, F.IN["emit_str"]))
    F.assign(body, m.mat)
    F.assign(wire, F.mat_metal("Gold", '#D6A64A', brushed=False).mat)
    return [body, wire]


def test_quality_report_partial_uvs():
    """A lathe (no UVs) joined with a curve sweep (UVs) — lessons #14 — must not
    crash quality_report (5.x can leave uv_layers with NO active layer) and
    must REPORT the zero-area faces, so the trap is visible before any bake."""
    body = F.lathe("Body", [(0, 0), (0.02, 0.0), (0.02, 0.08), (0, 0.08)], 24)
    wire = F.sweep("Wire", F.helix((0, 0), 0.0215, 0.005, 0.075, 3, 16), radius=0.0015, res=4)
    j = F.join([body, wire], "Joined")
    rep = F.quality_report(j)
    z = rep["uv_zero_area_faces"]
    check(isinstance(z, int) and z > 0, "partial UVs not reported: %r" % (z,))
    return "uv_zero_area_faces=%d (expected > 0: the trap is visible)" % z


def test_bake_emission_exact():
    parts = _glowing_parts()
    game = F.make_bake_target(parts, "GlowTest")
    zero = F.uv_zero_area_faces(game)
    check(zero == 0, "joined target has %d zero-area UV faces" % zero)
    out = outdir("bake")
    info = F.bake_pbr(game, sources=parts, size=128, out_dir=out, samples=4)
    es = info["emission_strength"]
    check(abs(es - S) / S < 0.02, "emission_strength %.4f, expected %.1f (sRGB-encoded peak would be %.3f)"
          % (es, S, 1.055 * S ** (1 / 2.4) - 0.055))
    path = info["files"]["emission"]
    depth, ctype = png_header(path)
    check(depth == 8, "emission PNG is %d-bit (expected 8-bit sRGB)" % depth)
    lin = srgb_decode(byte_pixels(path)[:, :3]).max(axis=1) * es
    check(abs(lin.max() - S) / S < 0.02, "emission PNG decodes to peak %.3f, expected %.1f" % (lin.max(), S))
    half = int((np.abs(lin - S / 2) < 0.04 * S).sum())
    check(half > 30, "only %d texels decode to S/2 (mid-tones distorted)" % half)
    alb = byte_pixels(info["files"]["albedo"])[:, :3]
    check(alb.max() > 0.1, "albedo map is black")
    return "strength=%.3f  S/2 texels=%d  8-bit sRGB" % (es, half)


def test_glb_roundtrip():
    parts = _glowing_parts()
    game = F.make_bake_target(parts, "RoundTrip")
    out = outdir("roundtrip")
    info = F.bake_pbr(game, sources=parts, size=64, out_dir=os.path.join(out, "textures"), samples=2)
    for o in parts:
        bpy.data.objects.remove(o, do_unlink=True)
    rep = F.quality_report(game)
    path = F.export_glb([game], os.path.join(out, "EQ-test-roundtrip.glb"))
    check(os.path.getsize(path) > 1000, "GLB is empty")
    F.reset_scene()
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    check(len(meshes) == 1, "%d meshes after import" % len(meshes))
    ob = meshes[0]
    mats = [s.material for s in ob.material_slots if s.material]
    check(len(mats) == 1, "%d materials after import" % len(mats))
    p = next(n for n in mats[0].node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    es = F.get_in(p, F.IN["emit_str"]).default_value
    check(abs(es - info["emission_strength"]) < 0.01,
          "emission strength %.3f -> %.3f after round trip" % (info["emission_strength"], es))
    imgs = {n.image.name for n in mats[0].node_tree.nodes if n.type == 'TEX_IMAGE' and n.image}
    check(len(imgs) == 4, "expected albedo, emission, normal, packed ORM; got %s" % sorted(imgs))
    tris = F.quality_report(ob)["triangles"]
    check(tris == rep["triangles"], "triangles %d -> %d after round trip" % (rep["triangles"], tris))
    ec = F.get_in(p, F.IN["emit_col"])
    src = ec.links[0].from_node if ec.is_linked else None
    while src is not None and src.type != 'TEX_IMAGE':        # importer may insert nodes
        src = src.inputs[0].links[0].from_node if src.inputs and src.inputs[0].is_linked else None
    check(src is not None, "emission texture not linked after import")
    a = np.empty(src.image.size[0] * src.image.size[1] * 4, np.float32); src.image.pixels.foreach_get(a)
    peak = a.reshape(-1, 4)[:, :3].max()
    check(peak > 0.97, "imported emission texture peaks at %.3f (expected 1.0 after normalising)" % peak)
    return "tris=%d strength=%.3f images=%d" % (tris, es, len(imgs))
