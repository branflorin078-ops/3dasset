"""Every mat_* builds, every tier wires a glow, and they all render."""
import os
import bpy
import numpy as np
import forge as F
from _util import check, outdir


def _linked(mb, canon):
    return F.get_in(mb.p, F.IN[canon]).is_linked


def _all_materials():
    mats = dict(
        metal=F.mat_metal("T_Metal", '#7E7466', brush_axis='Z'),
        blued=F.mat_metal("T_Blued", '#1E2A40', brushed=False, aniso=0.3, brush_axis='X'),
        leather=F.mat_leather("T_Leather", '#4A1418', grain=1400),
        cloth=F.mat_cloth("T_Cloth", '#6B6862'),
        stone=F.mat_stone("T_Stone"),
        gem=F.mat_gem("T_Gem", '#C4661A', emit_strength=1.3, heart='#FFB347', density=70),
    )
    for tier in F.TIERS:
        m = F.mat_metal("T_Glow_" + tier, '#7E7466')
        ax = m.math('ABSOLUTE', m.obj_axis('X'))
        F.add_glow(m, m.map_range(ax, 0.0, 0.01, 1.0, 0.0), tier, hot_gradient=m.obj_axis('Z'))
        mats["glow_" + tier] = m
    return mats


def test_every_mat_builds():
    mats = _all_materials()
    for key in ("metal", "blued", "leather", "stone"):
        mb = mats[key]
        check(_linked(mb, "base") and _linked(mb, "rough") and _linked(mb, "normal"),
              "%s is not layered (base/rough/normal must be driven)" % key)
    check(_linked(mats["cloth"], "normal"), "cloth has no weave bump")
    check(_linked(mats["gem"], "emit_str"), "gem has no emissive heart")
    for tier in F.TIERS:
        mb = mats["glow_" + tier]
        check(_linked(mb, "emit_col") and _linked(mb, "emit_str"), "tier %s glow not wired" % tier)
    return "%d materials, tiers=%s" % (len(mats), ",".join(F.TIERS))


def test_leather_edge_scale():
    """lessons #9: the burnish (edge) mask distance must scale with the part.
    A 3 mm strap with the default 2.5 mm mask reads as all-edge (pink)."""
    mb = F.mat_leather("T_Strap", '#5A3420', edge=0.0005)
    d = [n.inputs['Distance'].default_value for n in mb.mat.node_tree.nodes
         if n.type == 'AMBIENT_OCCLUSION' and n.inside]
    check(d and abs(d[0] - 0.0005) < 1e-9, "edge mask distance %s, expected 0.0005" % d)
    dflt = F.mat_leather("T_Grip", '#5A3420')
    d0 = [n.inputs['Distance'].default_value for n in dflt.mat.node_tree.nodes
          if n.type == 'AMBIENT_OCCLUSION' and n.inside]
    check(abs(d0[0] - 0.0025) < 1e-9, "default changed: %s" % d0)


def test_materials_render():
    """One tiny Cycles render with every material: catches shader-compile breakage."""
    mats = _all_materials()
    x = 0.0
    for key, mb in mats.items():
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(x, 0, 0), segments=16, ring_count=8)
        F.assign(bpy.context.object, mb.mat); x += 0.1
    for i, t in enumerate(F.TIERS):
        F.ember("E%d" % i, (0.05 * i, -0.05, 0.08), t)
    F.world_dark('#202226')
    c = (x / 2 - 0.05, 0, 0)
    F.studio_rig(c, radius=1.0)
    cam = F.camera(c, (c[0], -2.0, 0.3), lens=50)
    F.render_setup(res=(96, 32), samples=4, bloom=True)
    F.frame_camera(cam, [o for o in bpy.context.scene.objects if o.type == 'MESH'], margin=1.1)
    path = F.render(os.path.join(outdir("materials"), "materials.png"))
    im = bpy.data.images.load(path)
    a = np.empty(im.size[0] * im.size[1] * 4, np.float32); im.pixels.foreach_get(a)
    check(a.reshape(-1, 4)[:, :3].max() > 0.2, "materials render is black")
    return "device=%s" % bpy.context.scene.cycles.device
