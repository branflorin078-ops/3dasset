"""Rarity tiers: every tier exists (common..mythic), retier() rewires a built
asset in place (same geometry, camera, rig — only glow, embers and rim change)."""
import bpy
import forge as F
from _util import check

LADDER = ("common", "rare", "epic", "legendary", "mythic")


def _glow_mat(tier="legendary"):
    m = F.mat_metal("TierSteel", '#7E7466')
    ax = m.math('ABSOLUTE', m.obj_axis('X'))
    F.add_glow(m, m.map_range(ax, 0.0, 0.01, 1.0, 0.0), tier, hot_gradient=m.obj_axis('Z'))
    return m


def _ramp_colours(mat):
    r = next(n for n in mat.node_tree.nodes if n.label == "forge:glow_ramp")
    return [tuple(round(c, 4) for c in e.color[:3]) for e in r.color_ramp.elements]


def _strength(mat):
    return next(n for n in mat.node_tree.nodes if n.label == "forge:glow_strength").inputs[1].default_value


def test_tier_ladder_complete():
    for t in LADDER:
        check(t in F.TIERS, "TIERS lacks %r" % t)
        for k in ("core", "body", "haze", "strength", "breathe", "rim"):
            check(k in F.TIERS[t], "TIERS[%r] lacks %r" % (t, k))
    check(F.TIERS["common"]["strength"] == 0, "common must not glow")
    s = [F.TIERS[t]["strength"] for t in ("rare", "epic")]
    check(s[0] < s[1], "rare must be dimmer than epic: %s" % s)


def test_retier_rewires_in_place():
    m = _glow_mat("legendary")
    n_nodes = len(m.mat.node_tree.nodes)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05); ob = bpy.context.object; F.assign(ob, m.mat)
    emb = F.ember("E0", (0, 0, 0.1), "legendary")
    rig = F.studio_rig((0, 0, 0), rim_energy=1000)
    for t in LADDER:
        F.retier(t, rig=rig)
        T = F.TIERS[t]
        cols = _ramp_colours(m.mat)
        check(cols[-1] == tuple(round(c, 4) for c in F.hex_lin(T["core"])[:3]), "%s core colour not applied" % t)
        check(cols[2] == tuple(round(c, 4) for c in F.hex_lin(T["body"])[:3]), "%s body colour not applied" % t)
        check(abs(_strength(m.mat) - T["strength"]) < 1e-6, "%s strength %.3f" % (t, _strength(m.mat)))
        check(m.mat.get("forge_tier") == t, "material not tagged %s" % t)
        rim = rig["rim"].data
        check(tuple(round(c, 4) for c in rim.color) == tuple(round(c, 4) for c in F.hex_lin(T["rim"])[:3]),
              "%s rim colour" % t)
        check(abs(rim.energy - 1000 * T.get("rim_gain", 1.0)) < 1e-3, "%s rim energy %.1f" % (t, rim.energy))
        check(emb.hide_render == (not T.get("embers", False)), "%s ember visibility" % t)
    check(len(m.mat.node_tree.nodes) == n_nodes, "retier added/removed nodes")
    return "ladder=%s" % ",".join(LADDER)
