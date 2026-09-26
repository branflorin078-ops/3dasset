"""Round-trip proof for ANY asset: re-import the exported GLB and render it.
What this renders is exactly what Godot receives — baked textures only.
Run via: forge_run.py run verify_glb.py verify <outdir>   (uses the newest .glb there)"""
import sys, os, math, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib"))
import bpy, forge as F
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = argv[1] if len(argv) > 1 else "out"
glbs = sorted(glob.glob(os.path.join(OUT, "*.glb")), key=os.path.getmtime)
if not glbs: sys.exit("no .glb in " + OUT)
GLB = glbs[-1]
F.reset_scene()
bpy.ops.import_scene.gltf(filepath=GLB)
obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']; ob = obs[0]
mats = [s.material for s in ob.material_slots if s.material]
imgs = sorted({n.image.name for m in mats for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image})
emit = [round(F.get_in(n, F.IN["emit_str"]).default_value, 3) for m in mats for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
print("IMPORT", dict(glb=os.path.basename(GLB), meshes=len(obs), materials=[m.name for m in mats], images=imgs, emission_strength=emit))
print("QA_IMPORT", F.quality_report(ob))
c, size = F.bounds([ob])
elongated = size.z > 2.5 * max(size.x, size.y)          # weapons, spears, staffs
tilt = 52 if elongated else 0
M = (Matrix.Translation((0, 0, 0.62)) @ Matrix.Rotation(math.radians(28), 4, 'Z')
     @ Matrix.Rotation(math.radians(tilt), 4, 'Y') @ Matrix.Translation(-c))
ob.matrix_world = M @ ob.matrix_world
F.world_dark('#050608'); center = Vector((0, 0, 0.62))
F.studio_rig(center, radius=1.9, rim='#E8A33C', key_energy=480, rim_energy=1250, hair_energy=80)
cam = F.camera(center, (0.35, -2.6, 0.78), lens=85)
F.backdrop_radial(center, cam.location, color='#2A1B0C', edge='#030304', strength=0.9, dist=1.4, falloff=0.35)
F.render_setup(res=(800, 800), samples=48, glare_threshold=0.85, glare_size=7)
F.frame_camera(cam, [ob], margin=1.08)
print("RENDER", F.render(os.path.join(OUT, os.path.splitext(os.path.basename(GLB))[0] + "_roundtrip.png")))
