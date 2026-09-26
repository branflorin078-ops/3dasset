"""TEMPLATE — start every new asset here (copy, rename, replace the BUILD).
As shipped it builds a PROBE FINIAL (a banner-pole finial): the one-command
install smoke test that touches every stage of the pipeline.

    py tools/forge_run.py run examples/_template_asset.py <mode> <outdir> [tier]
    mode: preview (768 px) | final (1600 px) | tiers (every tier, 512 px) | export (bake + GLB)
    tier: common | rare | epic | legendary (default) | mythic

BRIEF (fill this in for a real asset — SKILL.md pipeline step 1)
  id        CST-probe_finial          tier: from argv
  silhouette  socket -> collar -> bulb -> neck -> spike; reads as a finial at 64 px
  reference   1) pole finials were cast bronze on an iron socket, riveted or pinned
              2) the socket is wire-bound where it grips the pole
              3) a raised band marks the bulb's equator (a seat for inlay)
  twist     the equator band is a GLOW channel; an amber cabochon on the front
  budget    <= 4k tris in-world (map prop class, export.md)
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib"))
import bpy, forge as F
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "preview"
OUT = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(HERE, "..", "out", "probe")
TIER = argv[2] if len(argv) > 2 else "legendary"
if TIER not in F.TIERS:
    sys.exit("unknown tier %r - one of %s" % (TIER, ", ".join(F.TIERS)))
os.makedirs(OUT, exist_ok=True)
F.reset_scene()

# ── BUILD: real forms only (lathe / loft / sweep / operators), metres, +Z up ──
BAND_Z = 0.095                                    # bulb equator (the glow channel)
socket = F.lathe("Socket", [(0, 0.0), (0.0165, 0.0), (0.0175, 0.004), (0.0160, 0.008), (0.0158, 0.040),
                            (0.0178, 0.043), (0.0178, 0.048), (0, 0.050)], 48)
F.hard_surface(socket, 0.0006, 2)
wrap = F.sweep("Wrap", F.helix((0, 0), 0.0168, 0.012, 0.036, 5, 24), radius=0.0011, res=4)
bulb = F.lathe("Bulb", [(0, 0.049), (0.012, 0.050), (0.021, 0.060), (0.0275, 0.078), (0.0290, 0.090),
                        (0.0262, 0.0925), (0.0262, 0.0975), (0.0290, 0.100), (0.0270, 0.112),
                        (0.0190, 0.124), (0.0090, 0.131), (0.0070, 0.137), (0, 0.139)], 64)
F.hard_surface(bulb, 0.0006, 2)
secs = []
for i in range(16):                               # a four-sided spike: loft to a true point
    t = i / 16; w = 0.0095 * (1 - t) ** 0.9 + 0.0004; z = 0.136 + t * 0.085
    secs.append([(-w, 0, z), (0, w * 0.8, z), (w, 0, z), (0, -w * 0.8, z)])
spike = F.loft("Spike", secs, tip=(0, 0, 0.225))
F.hard_surface(spike, 0.0004, 2, angle=35)
gem = F.gem_cabochon("Cabochon", rx=0.0075, ry=0.0060, height=0.0042)
gem.rotation_euler = (math.radians(90), 0, 0); gem.location = (0, -0.0272, 0.112)
parts = [socket, wrap, bulb, spike, gem]

# ── MATERIALS: layered, plus the tier glow (common = strength 0) ─────────────
bronze = F.mat_metal("Bronze", '#9A6B3A', rough=0.30, brushed=False, wear=0.6,
                     wear_color='#D9A566', cavity='#2A1A0C', cavity_amt=0.6)
band = F.mat_metal("BronzeBand", '#9A6B3A', rough=0.30, brushed=False, wear=0.6,
                   wear_color='#D9A566', cavity='#2A1A0C', cavity_amt=0.6)
dz = band.math('ABSOLUTE', band.math('SUBTRACT', band.obj_axis('Z'), BAND_Z))
F.add_glow(band, band.map_range(dz, 0.0005, 0.0032, 1.0, 0.0), TIER)   # the channel glows
iron = F.mat_metal("Iron", '#3A3A3E', rough=0.45, wear=0.5, cavity='#101012', brush_axis='Z')
amber = F.mat_gem("Amber", '#C4661A', emit_strength=1.2, heart='#FFB347', density=70)
F.assign(socket, bronze.mat); F.assign(wrap, bronze.mat); F.assign(bulb, band.mat)
F.assign(spike, iron.mat); F.assign(gem, amber.mat)
embers = [F.ember("Ember%d" % i, (0.012 * (-1) ** i, -0.03, 0.11 + 0.02 * i), TIER, size=0.0012)
          for i in range(3)]

# ── EXPORT: bake selected-to-active -> one texture set -> GLB (export.md) ────
if MODE == "export":
    game = F.make_bake_target(parts, "ProbeFinial", decimate=0.35)   # detail survives in the normal map
    info = F.bake_pbr(game, sources=parts, size=512, out_dir=os.path.join(OUT, "textures"), samples=8)
    for o in parts + embers:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.scene.cursor.location = (0, 0, 0)            # pivot: base centre
    bpy.ops.object.select_all(action='DESELECT'); game.select_set(True)
    bpy.context.view_layer.objects.active = game
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    print("BAKE", info)
    print("QA_GAME", F.quality_report(game, tri_budget=4000))
    path = F.export_glb([game], os.path.join(OUT, "CST-%s-finial_probe.glb" % TIER[:3]))
    print("GLB", path, os.path.getsize(path))
    sys.exit(0)

# ── STAGE: item card — backdrop_radial, rig, camera; frame AFTER render_setup ──
F.world_dark('#050608')
center = Vector((0, 0, 0.11))
rig = F.studio_rig(center, radius=1.2, rim=F.TIERS[TIER]['rim'], key_energy=260,
                   rim_energy=420, hair_energy=40)
F.retier(TIER, rig=rig)                                  # rim gain + embers per tier
cam = F.camera(center, (0.30, -0.95, 0.24), lens=85)
F.backdrop_radial(center, cam.location, color='#241A10', edge='#030304', strength=0.9,
                  dist=0.6, falloff=0.35)
if MODE == "tiers":
    F.render_setup(res=(512, 512), samples=32, glare_threshold=0.85)
    F.frame_fill(cam, parts, fill=0.8)          # in OR out: fill 80% (lessons #3)
    for t in ("common", "rare", "epic", "legendary", "mythic"):
        F.retier(t, rig=rig)
        print("CARD", t, F.render(os.path.join(OUT, "probe_finial_%s.png" % t)))
    sys.exit(0)
res = (768, 768) if MODE == "preview" else (1600, 1600)
F.render_setup(res=res, samples=48 if MODE == "preview" else 110, glare_threshold=0.85)
F.frame_fill(cam, parts, fill=0.8)          # in OR out: fill 80% (lessons #3)
for o in parts:
    r = F.quality_report(o)
    print("QA_PART", o.name, {k: r[k] for k in ("triangles", "non_manifold_edges", "open_boundary_edges",
                                                "degenerate_faces", "loose_verts")})
print("RENDER", F.render(os.path.join(OUT, "probe_finial_%s_%s.png" % (TIER, MODE))))
