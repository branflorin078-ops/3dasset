"""PROBE - the commander-forge smoke test. NEVER an asset.

It uses stand-in primitives (a monkey head, an elliptic torso, two arm
cylinders) ONLY to prove that figure_kit works on this Blender: skin, fitted
plate, hero rig, sworn rim, bust camera, mask + meta for figure_check.
A real figure starts from a licensed base (references/figure-lane.md).

    py <skills>/blender-forge/tools/forge_run.py run <skills>/commander-forge/examples/figure_probe.py preview <outdir>
    py <skills>/commander-forge/tools/figure_check.py <outdir>/probe_unsworn.png --sheet <outdir>/probe_check.png
Modes: preview (384x480, 24 samples) | final (1024x1280, 96 samples)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.environ.get("FORGE_LIB") or os.path.join(SKILLS, "blender-forge", "lib"))
sys.path.insert(0, os.path.join(SKILLS, "commander-forge", "tools"))
import bpy                      # noqa: E402
import forge as F               # noqa: E402
import figure_kit as FK         # noqa: E402
from mathutils import Vector    # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "preview"
OUT = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(HERE, "..", "out", "probe")
os.makedirs(OUT, exist_ok=True)
F.reset_scene()

# -- stand-in body (probe only) ------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.0, depth=0.62, location=(0, 0, 1.24))
torso = bpy.context.object
torso.name = "TorsoProxy"
torso.scale = (0.17, 0.115, 1.0)
arms = []
for sx in (-1, 1):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.045, depth=0.55, location=(sx * 0.235, 0.0, 1.22))
    arms.append(bpy.context.object)
body = F.join([torso] + arms, "BodyProxy")
bpy.ops.mesh.primitive_monkey_add(size=1.0, location=(0, 0, 1.70))
head = bpy.context.object
head.name = "HeadProxy"
bpy.context.view_layer.update()
head.scale = [0.24 / head.dimensions.z] * 3
F.subsurf(head, 2)
for p in head.data.polygons:
    p.use_smooth = True

# -- materials -------------------------------------------------------------------
skin = FK.mat_skin("Skin", base='#C8967A')
F.assign(head, skin.mat)
wool = F.mat_cloth("Wool", '#6B2A22', sheen=0.55, rough=0.86)
F.assign(body, wool.mat)

# -- kit fitted to the body: breastplate over a gambeson (offset 25 mm) -------------
plate = FK.plate_on_body(body, "Breastplate", z_bottom=1.02, height=0.40, offset=0.025,
                         arc=(190.0, 350.0), thickness=0.0018, bulge=0.012, taper=0.08,
                         roll=0.003, roll_edges=('top', 'bottom'))
F.hard_surface(plate, 0.0006, 2)
steel = F.mat_metal("Steel", '#7E7466', rough=0.30, wear=0.6, cavity='#1C1D20', brush_axis='X')
F.assign(plate, steel.mat)
FK.clearance(plate, body)

# -- the other figure materials and the base importer must build on this Blender ----
import numpy as np                                                           # noqa: E402
atlas = bpy.data.images.new("strand_atlas", 64, 64, alpha=True)
px = np.zeros((64, 64, 4), np.float32)
px[:, :, :3] = (0.20, 0.12, 0.07)
px[:, ::4, 3] = 1.0                                                          # 1 px strands every 4 px
atlas.pixels.foreach_set(px.ravel())
atlas.filepath_raw = os.path.join(OUT, "strand_atlas.png")
atlas.file_format = 'PNG'
atlas.save()
cards = FK.mat_hair_cards("HairCards", atlas.filepath_raw)
flat_n = bpy.data.images.new("flat_normal", 8, 8)                            # textured-skin branch
flat_n.pixels.foreach_set(np.tile(np.array([0.5, 0.5, 1.0, 1.0], np.float32), 64))
flat_n.filepath_raw = os.path.join(OUT, "flat_normal.png")
flat_n.file_format = 'PNG'
flat_n.save()
skin_tx = FK.mat_skin("SkinTextured", albedo=atlas.filepath_raw, rough_map=atlas.filepath_raw,
                      normal_map=flat_n.filepath_raw)
strands = FK.mat_hair_strands("HairStrands", melanin=0.8)
cornea = FK.mat_cornea("Cornea")
obj_path = os.path.join(OUT, "head_proxy.obj")
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True)
bpy.context.view_layer.objects.active = head
if hasattr(bpy.ops.wm, 'obj_export'):
    bpy.ops.wm.obj_export(filepath=obj_path, export_selected_objects=True)
    for o in FK.import_base(obj_path):
        bpy.data.objects.remove(o, do_unlink=True)
print("QA_MATS", dict(cards=cards.mat.name, strands=strands.name, cornea=cornea.mat.name,
                     skin_textured=skin_tx.mat.name))

# -- read back what the skin actually carries -------------------------------------
p = skin.p
print("QA_SKIN", dict(method=p.subsurface_method,
                      radius=tuple(round(x, 3) for x in F.get_in(p, F.IN["sss_rad"]).default_value),
                      scale=round(F.get_in(p, ["Subsurface Scale"]).default_value, 4),
                      weight=F.get_in(p, F.IN["sss"]).default_value))

# -- stage -------------------------------------------------------------------------
F.world_dark('#050608')
res = (384, 480) if MODE == "preview" else (1024, 1280)
eye = head.matrix_world.translation + Vector((0, 0, 0.015))
cam = FK.bust_camera(eye, head_h=0.24, fill=0.45, lens=85, fstop=4.0, yaw=18.0, res=res)
rig = FK.hero_rig(eye, dist=2.0, yaw=18.0)
F.backdrop_radial(eye, cam.location, color='#241A10', edge='#030304', strength=0.9, dist=0.9, falloff=0.35)
F.render_setup(res=res, samples=24 if MODE == "preview" else 96, glare_threshold=0.9)
for state in (False, True):
    FK.set_sworn(rig, state)
    tag = "sworn" if state else "unsworn"
    path = os.path.join(OUT, "probe_%s.png" % tag)
    FK.render_with_mask(path)
    FK.write_meta(path, cam, face_pts=FK.box_corners(head), kind="bust", sworn=state)
    print("RENDER", path)
