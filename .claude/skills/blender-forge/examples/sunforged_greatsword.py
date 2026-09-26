"""Sunforged Daybreak Greatsword — legendary. Real-form build with forge.py.
Run: py tools/forge_run.py run examples/sunforged_greatsword.py <preview|final|export|tiers> <outdir>
     (tiers = the same sword at common/rare/epic/legendary/mythic, identical camera + rig)"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib"))
import bpy, forge as F
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "preview"
OUT = argv[1] if len(argv) > 1 else "/tmp/forge_out"
os.makedirs(OUT, exist_ok=True)
F.reset_scene()

# ── DIMENSIONS (metres; built blade-up, guard at z=0) ─────────────────────
L, W0, T0 = 1.02, 0.030, 0.0048      # blade length, half-width, half-thickness
FULLER_HALF, FULLER_DEPTH = 0.0095, 0.0024
FULLER_Z = (0.045, 0.62*L)

def smooth(a, b, x):
    t = max(0.0, min(1.0, (x-a)/(b-a))); return t*t*(3-2*t)

# ── BLADE: loft of a lenticular cross-section with a rounded fuller ──────
xs = [-1, -0.94, -0.85, -0.72, -0.58, -0.46, -0.38, -0.30, -0.22, -0.14, -0.07, 0,
      0.07, 0.14, 0.22, 0.30, 0.38, 0.46, 0.58, 0.72, 0.85, 0.94, 1]
def blade_section(t):
    z = t*L
    if t < 0.80: W = W0*(1-0.22*t)
    else:
        u = (t-0.80)/0.20; W = W0*(1-0.22*0.80)*max(0.0015, (1-u**1.7))**0.75
    T = T0*(1-0.55*t)*(1 if t < 0.8 else max(0.02, (1-(t-0.8)/0.2))**0.6)
    fz = smooth(FULLER_Z[0], FULLER_Z[0]+0.05, z) * (1-smooth(FULLER_Z[1]-0.10, FULLER_Z[1], z))
    top, bot = [], []
    for fx in xs:
        x = fx*W; ax = abs(x)
        y = T*max(0.0, 1-abs(fx)**2.2)**0.62
        if ax < FULLER_HALF and fz > 0:
            y -= FULLER_DEPTH*fz*math.cos(math.pi/2*ax/FULLER_HALF)**2
        y = max(y, T*0.12) if abs(fx) < 0.999 else 0.0
        top.append((x, y, z))
    for (x, y, z2) in reversed(top[1:-1]):
        bot.append((x, -y, z2))
    return top + bot
sections = [blade_section(i/80) for i in range(80)]           # tip is a true point
blade = F.loft("Blade", sections, tip=(0.0, 0.0, L)); F.hard_surface(blade, width=0.0006, segments=2, angle=35)

# ── RICASSO COLLAR (lathe) ───────────────────────────────────────────────
collar = F.lathe("Collar", [(0,0.0),(0.013,0.0),(0.016,0.004),(0.014,0.010),(0.0,0.012)], 40)
collar.scale = (2.4, 0.62, 1.0); F.hard_surface(collar, 0.0008, 2)

# ── QUILLON: swept, tapered, tips curving toward the blade ───────────────
qpts, qtap = [], []
for i in range(33):
    u = -1 + 2*i/32; x = u*0.155
    z = -0.006 + 0.022*abs(u)**2.4
    qpts.append((x, 0, z)); qtap.append(1.0 - 0.42*abs(u)**1.3)
quillon = F.sweep("Quillon", qpts, radius=0.0105, res=6, taper=qtap)
quillon.scale = (1, 0.72, 1); F.hard_surface(quillon, 0.0005, 2, angle=45)
finials = []
for sx in (-1, 1):
    fin = F.lathe(f"Finial{sx}", [(0,-0.009),(0.006,-0.007),(0.0085,0),(0.006,0.007),(0.003,0.010),(0,0.012)], 32)
    fin.location = (sx*0.158, 0, 0.018); fin.rotation_euler = (0, math.radians(-sx*28), 0)
    finials.append(fin); F.subsurf(fin, 1)

# ── SUNBURST LANGETS: a half-sun on each blade face, rays fanning upward ─
rays = []
ray_specs = [(-74,0.050),(-56,0.068),(-37,0.058),(-18,0.088),(0,0.074),(18,0.088),(37,0.058),(56,0.068),(74,0.050)]
for side in (-1, 1):
    y0 = side*(T0*0.9 + 0.0012)
    for k, (a_deg, length) in enumerate(ray_specs):
        secs = []
        for i in range(14):
            t = i/14; w = 0.0062*(1-t)**0.85 + 0.00015; h = 0.0016*(1-t)**0.7 + 0.0001
            secs.append([(-w,0,t*length),(0,h,t*length),(w,0,t*length),(0,-h,t*length)])
        r = F.loft(f"Ray{side}_{k}", secs, tip=(0.0, 0.0, length))
        ang = math.radians(a_deg)
        r.location = (math.sin(ang)*0.006, y0, 0.010 + math.cos(ang)*0.004)
        r.rotation_euler = (0, ang, 0)
        F.hard_surface(r, 0.00025, 1, angle=40); rays.append(r)
    # the sun's disc at the ray origin
    disc = F.lathe(f"SunDisc{side}", [(0,-0.0024),(0.0150,-0.0024),(0.0172,0),(0.0150,0.0024),(0,0.0032)], 48)
    disc.rotation_euler = (math.radians(90), 0, 0); disc.location = (0, y0, 0.010)
    F.hard_surface(disc, 0.0004, 2); rays.append(disc)

# ── GRIP: lathed core with a subtle swell + twisted gold-wire pair ───────
GL = 0.27
gprof = [(0, -0.004)]
for i in range(19):
    t = i/18; z = -0.004 - t*GL
    rr = 0.0150 + 0.0022*math.sin(math.pi*t)**1.5
    gprof.append((rr, z))
gprof.append((0, -0.004-GL))
grip = F.lathe("Grip", gprof, 36)
for p in grip.data.polygons: p.use_smooth = True
wires = []
for ph in (0.0, math.pi):
    pts = F.helix((0,0), 0.0170, -0.012, -0.004-GL+0.008, turns=11, pts_per_turn=28, phase=ph)
    # follow the grip swell
    pts = [(x*(1+0.12*math.sin(math.pi*((-z-0.004)/GL))**1.5), y*(1+0.12*math.sin(math.pi*((-z-0.004)/GL))**1.5), z) for x,y,z in pts]
    wires.append(F.sweep(f"Wire{int(ph*10)}", pts, radius=0.00135, res=4))
ferrules = []
for zc in (-0.006, -0.004-GL+0.002):
    fr = F.lathe(f"Ferrule{zc}", [(0.0158,zc-0.004),(0.0182,zc-0.003),(0.0186,zc),(0.0182,zc+0.003),(0.0158,zc+0.004)], 40)
    ferrules.append(fr); F.hard_surface(fr, 0.0004, 2)

# ── WHEEL POMMEL (lathe, axis turned to face the viewer) + gems ──────────
PZ = -0.004-GL-0.036
wheel = F.lathe("Pommel", [(0,-0.0095),(0.020,-0.0095),(0.027,-0.012),(0.034,-0.0075),
                           (0.0355,0),(0.034,0.0075),(0.027,0.012),(0.020,0.0095),(0,0.0095)], 56)
wheel.rotation_euler = (math.radians(90), 0, 0); wheel.location = (0, 0, PZ)
F.hard_surface(wheel, 0.0007, 3, angle=25)
neck = F.lathe("PommelNeck", [(0.0,0.0),(0.012,0.0),(0.010,-0.010),(0.0,-0.012)], 32)
neck.location = (0, 0, -0.004-GL+0.004); F.subsurf(neck, 1)
peen = F.lathe("Peen", [(0,0),(0.006,0),(0.0045,-0.004),(0,-0.0055)], 24)
peen.location = (0, 0, PZ-0.0355); F.subsurf(peen, 1)
gems, bezels = [], []
for side in (-1, 1):
    gem = F.lathe(f"Gem{side}", [(0,-0.0065),(0.0138,0.0),(0.0090,0.0042),(0,0.0046)], 12)
    F.flat(gem)
    gem.rotation_euler = (math.radians(90*side*-1), 0, 0)
    gem.location = (0, side*-0.0095, PZ); gems.append(gem)
    bz = F.lathe(f"Bezel{side}", [(0.0135,-0.0015),(0.0158,-0.0010),(0.0160,0.0015),(0.0140,0.0022)], 48)
    bz.rotation_euler = gem.rotation_euler; bz.location = gem.location
    F.hard_surface(bz, 0.0003, 2); bezels.append(bz)

# ── MATERIALS ─────────────────────────────────────────────────────────────
blade_m = F.mat_metal("BladeSteel", base='#7E7466', rough=0.30, rough_var=0.12,
                      brush_axis='Z', wear=0.5, cavity='#2A2016', cavity_amt=0.45, scratch=0.22)
# glow lives IN the fuller: |x| mask x fuller-length window; hottest at ricasso
ax = blade_m.math('ABSOLUTE', blade_m.obj_axis('X'))
across = blade_m.map_range(ax, FULLER_HALF*0.10, FULLER_HALF*1.05, 1.0, 0.0)
zc = blade_m.obj_axis('Z')
along = blade_m.math('MULTIPLY', blade_m.map_range(zc, FULLER_Z[0], FULLER_Z[0]+0.06),
                     blade_m.map_range(zc, FULLER_Z[1]-0.16, FULLER_Z[1]-0.02, 1.0, 0.0))
mask = blade_m.math('MULTIPLY', across, along)
hot = blade_m.map_range(zc, FULLER_Z[0], 0.42*L, 1.0, 0.0)
F.add_glow(blade_m, mask, "legendary", hot_gradient=hot)

gold = F.mat_metal("Gold", base='#D6A64A', rough=0.18, rough_var=0.08, brushed=False,
                   wear=0.7, wear_color='#F2D38A', cavity='#3A2208', cavity_amt=0.65, scratch=0.15)
rays_m = F.mat_metal("RayGold", base='#D6A64A', rough=0.16, brushed=False, wear=0.7,
                     wear_color='#F2D38A', cavity='#3A2208', cavity_amt=0.6, scratch=0.12)
rz = rays_m.obj_axis('Z')
F.add_glow(rays_m, rays_m.map_range(rz, 0.0, 0.034, 0.80, 0.0), "legendary")
leather = F.mat_leather("OxbloodLeather", base='#4A1418', rough=0.55, grain=1400)
amber = F.mat_gem("AmberSunGem", '#C4661A', emit_strength=1.3, heart='#FFB347', density=70)

for o in [blade]: F.assign(o, blade_m.mat)
for o in [collar, quillon, *finials, *wires, *ferrules, wheel, neck, peen, *bezels]: F.assign(o, gold.mat)
for o in rays: F.assign(o, rays_m.mat)
F.assign(grip, leather.mat)
for g in gems: F.assign(g, amber.mat)

# ── EMBERS rising from the ricasso ────────────────────────────────────────
embers = []
for i, (dx, dy, dz) in enumerate([(0.018,-0.035,0.10),(-0.010,-0.050,0.16),(0.030,-0.028,0.22),(-0.024,-0.040,0.27)]):
    embers.append(F.ember(f"Ember{i}", (dx, dy, dz), "legendary", size=0.0016 - 0.00025*i))


# ── EXPORT MODE: canonical orientation, bake to one texture set, GLB ─────
if MODE == "export":
    parts = [blade, collar, quillon, *finials, *rays, grip, *wires, *ferrules, wheel, neck, peen, *gems, *bezels]
    game = F.make_bake_target(parts, "SunforgedGreatsword", decimate=0.30)   # in-world LOD ≤12k
    info = F.bake_pbr(game, sources=parts, size=1024, out_dir=os.path.join(OUT, "textures"), samples=8)
    for o in parts + embers:                     # sources were only for the bake
        bpy.data.objects.remove(o, do_unlink=True)
    GRIP_C = -0.004 - GL/2                        # pivot convention: grip centre
    bpy.context.scene.cursor.location = (0, 0, GRIP_C)
    bpy.ops.object.select_all(action='DESELECT'); game.select_set(True)
    bpy.context.view_layer.objects.active = game
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR'); game.location = (0, 0, 0)
    rep = F.quality_report(game, tri_budget=12000)
    path = F.export_glb([game], os.path.join(OUT, "EQ-leg-blade_sunforged.glb"))
    print("BAKE", info); print("QA_GAME", rep); print("GLB", path, os.path.getsize(path))
    sys.exit(0)

# ── POSE: hero diagonal — blade flat faces camera, turned 28° for 3/4 ─────
sword = [blade, collar, quillon, *finials, *rays, grip, *wires, *ferrules, wheel, neck, peen, *gems, *bezels]
MID = Vector((0, 0, (L - 0.35) / 2))          # visual centre of the whole weapon
M = (Matrix.Translation((0, 0, 0.62)) @ Matrix.Rotation(math.radians(28), 4, 'Z')
     @ Matrix.Rotation(math.radians(52), 4, 'Y') @ Matrix.Translation(-MID))
for o in sword:
    o.matrix_world = M @ o.matrix_world
ric = M @ Vector((0, 0, 0.07))                   # ricasso = hottest point
for i, e_ in enumerate(embers):
    e_.location = ric + Vector((0.010*((-1)**i) + 0.004*i, -0.025, 0.035 + 0.042*i))
    e_.rotation_euler = (0, 0, 0); e_.scale = (1, 1, 3.2 - 0.4*i)
# ── STAGE ─────────────────────────────────────────────────────────────────
F.world_dark('#050608')
center = Vector((0, 0, 0.62))
rig = F.studio_rig(center, radius=1.9, rim='#E8A33C', key_energy=480, rim_energy=1250, hair_energy=80)
cam = F.camera(center, (0.35, -2.6, 0.78), lens=85)
F.backdrop_radial(center, cam.location, color='#2A1B0C', edge='#030304', strength=0.9, dist=1.4, falloff=0.35)

# ── RARITY SHEET: identical camera + rig; retier() changes only glow, embers, rim
if MODE == "tiers":
    F.render_setup(res=(768, 768), samples=48, glare_threshold=0.85, glare_size=7)
    F.frame_camera(cam, sword, margin=1.08)
    for tier in ("common", "rare", "epic", "legendary", "mythic"):
        F.retier(tier, rig=rig)
        print("CARD", tier, F.render(os.path.join(OUT, f"sunforged_{tier}.png")))
    sys.exit(0)

res = (1000, 1000) if MODE == "preview" else (1600, 1600)
F.render_setup(res=res, samples=64 if MODE == "preview" else 110, glare_threshold=0.85, glare_size=7)
F.frame_camera(cam, sword, margin=1.08)
print("QA", F.quality_report(blade))
print("RENDER", F.render(os.path.join(OUT, f"sunforged_{MODE}.png")))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "sunforged_greatsword.blend"))
