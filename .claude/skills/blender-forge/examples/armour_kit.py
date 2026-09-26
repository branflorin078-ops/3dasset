"""Armour-kit operators in one still life — the reference for helm_shell,
boolean_cut + slot_cutter, rivet_row, plate (lames + rolled edges),
strap_buckle, gem_brilliant and gem_cabochon.
Run: py tools/forge_run.py run examples/armour_kit.py <preview|final> <outdir>"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib"))
import bpy, forge as F
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "preview"
OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)
F.reset_scene()

# ── SALLET: one raised bowl drawn into a tail, sights cut, brow rivets ────
# Proportions measured on Met CC0 German sallets (art/references/EX-armour-kit):
# overall H/W 1.00-1.22 (23091, 23233, 23088), D/W 1.31-1.54, and the tail
# sweeps BACK (D - W = 7-13 cm) and down at ~35° (21984) — neither hanging
# like a neck guard nor flat like a cap brim. Overall H = height + tail;
# D = 2*radius + tail_flare. Here H/W = 0.240/0.208 = 1.15, D/W = 0.283/0.208
# = 1.36, rear sweep atan(0.050/0.075) = 34°.
helm = F.helm_shell("Sallet", radius=0.104, height=0.190, thickness=0.0018, squareness=2.3,
                    tail=0.050, tail_flare=0.075, tail_width=200, roll=0.0024)
F.hard_surface(helm, 0.0006, 2)
sights = []
for side in (-1, 1):                          # two sights either side of a nasal bar
    c = F.slot_cutter("Sight%d" % side, length=0.062, width=0.0085, depth=0.08)
    c.location = (side * 0.036, -0.10, 0.058); c.rotation_euler = (0, math.radians(side * 7), 0)
    sights.append(c)
F.boolean_cut(helm, sights)
brow = [(0.109 * math.cos(a), 0.109 * math.sin(a), 0.030) for a in
        [math.radians(d) for d in range(205, 336, 5)]]
rivets = F.rivet_row("BrowRivets", brow, count=7, head_r=0.0058, head_h=0.0032, surface=helm)  # ~12 mm heads, ~4 cm apart (Met 21984)

# ── FAULD: four lames from one profile, rolled top and bottom ─────────────
prof = [(0.34 * (i / 12 - 0.5), -0.06 * (1 - (2 * i / 12 - 1) ** 2)) for i in range(13)]
fauld = F.plate("Fauld", prof, height=0.17, thickness=0.0016, lames=4, overlap=0.3,
                bulge=0.012, roll=0.0026, roll_edges=('top', 'bottom'))
F.hard_surface(fauld, 0.0005, 2)
lame_rivets = []
for k, z in enumerate((0.148, 0.113, 0.078, 0.043)):
    lame_rivets.append(F.rivet_row("LameRivets%d" % k, [(-0.15, -0.05, z), (0.15, -0.05, z)], count=2,
                                   head_r=0.0038, head_h=0.002, surface=fauld, inset=False))

# ── BELT: strap with a centre-bar buckle ─────────────────────────────────
belt_path = [(-0.20, 0.0, 0.0), (-0.08, -0.03, 0.004), (0.04, -0.035, 0.0), (0.16, -0.01, -0.004),
             (0.26, 0.03, 0.0)]
strap, buckle = F.strap_buckle("Belt", belt_path, width=0.028, thickness=0.0032, at=0.42)

# ── GEMS: a real brilliant and a cabochon ────────────────────────────────
brilliant = F.gem_brilliant("Brilliant", diameter=0.030)
cabochon = F.gem_cabochon("Cabochon", rx=0.020, ry=0.015, height=0.011)

# ── MATERIALS ─────────────────────────────────────────────────────────────
# A raised bowl is hammered and polished, not brushed: mottled roughness
# (~2.5 cm patches, 0.31-0.61) like the Met sallets' patina, no Z streaks.
steel = F.mat_metal("MunitionSteel", '#7E8186', rough=0.46, rough_var=0.30, brushed=False, wear=0.6,
                    cavity='#1C1D20', cavity_amt=0.55, scratch=0.25)
dark = F.mat_metal("DarkSteel", '#5E5A54', rough=0.38, wear=0.55, cavity='#15130F', brush_axis='X')
brass = F.mat_metal("Brass", '#B08D57', rough=0.28, brushed=False, wear=0.6, wear_color='#E6C98A',
                    cavity='#3A2A10', cavity_amt=0.6)
leather = F.mat_leather("BeltLeather", '#5A3420', rough=0.6, grain=1300, edge=0.0005)  # 3 mm strap: lessons #9
sapphire = F.mat_gem("Sapphire", '#1F4FC4', emit_strength=0.8, heart='#9FB8FF', density=60)
ruby = F.mat_gem("Ruby", '#B01830', emit_strength=0.8, heart='#FF8FA0', density=60)
F.assign(helm, steel.mat); F.assign(fauld, dark.mat); F.assign(strap, leather.mat)
for o in [rivets, buckle, *lame_rivets]: F.assign(o, brass.mat)
F.assign(brilliant, sapphire.mat); F.assign(cabochon, ruby.mat)

# ── STAGE: a still life on a dark ground ─────────────────────────────────
rivets.parent = helm                       # parent while helm/fauld sit at identity,
for r in lame_rivets:                      # then move them: fittings follow
    r.parent = fauld
helm.location = (-0.17, 0.05, 0.085); helm.rotation_euler = (0, 0, math.radians(-38))  # 67° off the view: sights AND tail read
# Lean the fauld back 20°: an upright plate only mirrors the dark world and
# reads black; tilted, its face catches the key from above.
fauld.location = (0.20, 0.10, 0.0); fauld.rotation_euler = (math.radians(-20), 0, math.radians(18))
for o in (strap, buckle):
    o.location += Vector((0.0, -0.13, 0.0035))
brilliant.location = (-0.03, -0.22, 0.012); brilliant.rotation_euler = (math.radians(58), 0, math.radians(20))
cabochon.location = (0.07, -0.23, 0.0)
bpy.context.view_layer.update()
F.world_dark('#07080B')                     # floating card: no floor (lessons #8)
center = Vector((0.02, -0.02, 0.07))
F.studio_rig(center, radius=1.6, rim='#C9D4E6', key_energy=260, rim_energy=520, hair_energy=70)
cam = F.camera(center, (0.55, -1.25, 0.62), lens=60)
F.backdrop_radial(center, cam.location, color='#1C1914', edge='#030304', strength=0.9,
                  dist=0.9, falloff=0.4)
# The kit lies ~1.5:1 wide, so it gets a 3:2 frame — a square one left the
# lower third empty black (r6).
res = (1200, 800) if MODE == "preview" else (2400, 1600)
# No glow tier here (gems 0.8), so no bloom: a raised threshold (2.0) still
# haloed the sallet's key highlight — polished steel specular exceeds 2.
F.render_setup(res=res, samples=64 if MODE == "preview" else 128, bloom=False)
parts = [helm, rivets, fauld, *lame_rivets, strap, buckle, brilliant, cabochon]


def aim_at_silhouette(cam, objs):
    """Point the camera at the centre of the parts' projected silhouette
    (mesh vertices, not bbox corners): a spread still life aimed at a hand-
    picked point sits off-centre."""
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs, ys = [], []
    for o in objs:
        mw = o.matrix_world
        for v in o.data.vertices:
            lp = inv @ (mw @ v.co)
            xs.append(lp.x / -lp.z); ys.append(lp.y / -lp.z)
    d = cam.matrix_world.to_quaternion() @ Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, -1.0))
    F.look_at(cam, cam.location + d)
    bpy.context.view_layer.update()


aim_at_silhouette(cam, parts)
F.frame_fill(cam, parts, fill=0.95)   # bbox corners overshoot a spread still life: ~0.75 real fill
aim_at_silhouette(cam, parts)         # the dolly shifts parallax: re-centre once
for o in (helm, fauld, strap, buckle, rivets, brilliant, cabochon):
    print("QA_PART", {k: v for k, v in F.quality_report(o).items()
                      if k in ("object", "triangles", "non_manifold_edges", "open_boundary_edges",
                               "degenerate_faces", "loose_verts")})
print("RENDER", F.render(os.path.join(OUT, "armour_kit_%s.png" % MODE)))
