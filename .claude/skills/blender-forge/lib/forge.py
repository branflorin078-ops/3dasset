"""
forge.py — professional asset toolkit for headless Blender (4.0+).
Real forms (loft, lathe, sweep), hard-surface finishing, layered PBR
materials with wear, rarity glow tiers, studio lighting, bloom, PBR
baking for game export, GLB export, and automated quality gates.

Import from a Blender script:
    import sys; sys.path.insert(0, "<path-to>/lib"); import forge as F
"""
import bpy, bmesh, math, json, os, bisect
import numpy as np                      # bundled with every Blender since 2.8
from mathutils import Vector, Matrix

V = bpy.app.version  # (major, minor, patch)

# ─────────────────────────────── colour utils ──────────────────────────────
def hex_lin(h, a=1.0):
    """'#RRGGBB' -> linear RGBA (Blender shader colours are linear)."""
    h = h.lstrip('#')
    def c(x):
        x = int(x, 16) / 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return (c(h[0:2]), c(h[2:4]), c(h[4:6]), a)

def srgb_encode(a):
    """Linear 0..1 -> sRGB-encoded 0..1 (IEC 61966-2-1 OETF). numpy in/out."""
    a = np.clip(np.asarray(a, np.float64), 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(a, 1 / 2.4) - 0.055)

def srgb_decode(v):
    """sRGB-encoded 0..1 -> linear 0..1 (EOTF). numpy in/out."""
    v = np.asarray(v, np.float64)
    return np.where(v <= 0.04045, v / 12.92, np.power((v + 0.055) / 1.055, 2.4))

def set_in(node, names, value):
    """Set the first matching input — survives Principled renames across versions."""
    for n in ([names] if isinstance(names, str) else names):
        if n in node.inputs:
            node.inputs[n].default_value = value
            return node.inputs[n]
    raise KeyError(f"none of {names} on {node.name}")

def get_in(node, names):
    for n in ([names] if isinstance(names, str) else names):
        if n in node.inputs:
            return node.inputs[n]
    raise KeyError(names)

IN = {  # canonical -> candidate socket names (4.x first, 3.x fallback)
    "base": ["Base Color"], "metal": ["Metallic"], "rough": ["Roughness"],
    "normal": ["Normal"], "emit_col": ["Emission Color", "Emission"],
    "emit_str": ["Emission Strength"], "trans": ["Transmission Weight", "Transmission"],
    "sss": ["Subsurface Weight", "Subsurface"], "sss_rad": ["Subsurface Radius"],
    "coat": ["Coat Weight", "Clearcoat"], "sheen": ["Sheen Weight", "Sheen"],
    "sheen_rough": ["Sheen Roughness"], "ior": ["IOR"], "aniso": ["Anisotropic"],
    "spec": ["Specular IOR Level", "Specular"],
}

# ──────────────────────────────── scene setup ──────────────────────────────
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'; s.unit_settings.scale_length = 1.0
    return s

_DENOISE_OK = None
def denoise_available():
    """Probe once with a tiny render; some Linux builds ship without OIDN.
    A scene without a camera cannot render at all — a temporary camera is
    added for the probe, so 'no camera yet' is never cached as 'no denoiser'
    (which silently switched denoising off and multiplied samples by 2.5)."""
    global _DENOISE_OK
    if _DENOISE_OK is not None:
        return _DENOISE_OK
    s = bpy.context.scene
    old = (s.render.engine, s.render.resolution_x, s.render.resolution_y,
           s.render.resolution_percentage, s.render.filepath)
    tmp = None
    if s.camera is None:
        cd = bpy.data.cameras.new("__forge_probe_cam")
        tmp = bpy.data.objects.new("__forge_probe_cam", cd); s.collection.objects.link(tmp)
        s.camera = tmp
    s.render.engine = 'CYCLES'; s.cycles.samples = 1; s.cycles.use_denoising = True
    s.render.resolution_x = s.render.resolution_y = 8; s.render.resolution_percentage = 100
    try:
        bpy.ops.render.render(write_still=False); _DENOISE_OK = True
    except RuntimeError:
        _DENOISE_OK = False
    if tmp is not None:
        cd = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.cameras.remove(cd)
        s.camera = None
    (s.render.engine, s.render.resolution_x, s.render.resolution_y,
     s.render.resolution_percentage, s.render.filepath) = old
    return _DENOISE_OK

_GPU = None
def gpu_setup():
    """Probe once: OptiX > CUDA > HIP > Metal > oneAPI, else CPU. Returns the
    backend name. OptiX on the RTX 3500 Ada measured ~10x the 20-core CPU.
    reset_scene() (read_factory_settings) WIPES the Cycles device preferences:
    the cached backend is re-applied here, so a script that resets and renders
    again never silently falls back to CPU (tests/test_render.py)."""
    global _GPU
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
    except Exception:
        _GPU = 'CPU'
        return _GPU
    if _GPU == 'CPU':
        return _GPU
    if _GPU and prefs.compute_device_type == _GPU and any(
            d.use and d.type == _GPU for d in prefs.devices):
        return _GPU
    found = 'CPU'
    for backend in ((_GPU,) if _GPU else ()) + ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
        try:
            prefs.compute_device_type = backend
            prefs.get_devices()
        except (TypeError, ValueError, AttributeError):
            continue
        if any(d.type == backend for d in prefs.devices):
            for d in prefs.devices:
                d.use = d.type == backend
            found = backend
            break
    _GPU = found
    return _GPU

# 4.5+/5.x Glare sockets, calibrated 2026-09-26 by render strip on the Sunforged
# (art/forge/calibration): the documented 2^(size-9) mapping (7 -> 0.25 of the
# frame) put a third of the halo's lift 24-96 px out — a warm veil. 0.0625 keeps
# the near halo (0.0755 vs 0.0767 mean lift within 24 px) with 4.3x less veil
# and zero far-field lift. Strength is ADDITIVE on 4.5+; the old Mix -0.55 was
# 1.124*image + 0.326*glare.
BLOOM_SIZE_AT_7 = 0.0625
BLOOM_STRENGTH = 0.40

def _glare_bloom(gl, threshold, size, strength=None, rel_size=None):
    """Glare node → subtle bloom on 4.0 (properties) and 4.5/5.x (sockets).
    `size` is the legacy int (6–9); on 4.5+ it maps to a RELATIVE size of
    BLOOM_SIZE_AT_7 * 2^(size-7) unless `rel_size` is given."""
    if 'glare_type' in gl.bl_rna.properties:          # 4.0–4.4: properties
        types = [i.identifier for i in gl.bl_rna.properties['glare_type'].enum_items]
        gl.glare_type = 'BLOOM' if 'BLOOM' in types else 'FOG_GLOW'
        gl.quality = 'HIGH'; gl.threshold = threshold; gl.size = size
        gl.mix = -0.55  # keep bloom subtle: halo, not haze
        return
    for name in ('Bloom', 'BLOOM', 'Fog Glow'):           # 4.5+/5.x: menu sockets
        try:
            gl.inputs['Type'].default_value = name; break
        except (TypeError, ValueError):
            continue
    for name in ('High', 'HIGH'):
        try:
            gl.inputs['Quality'].default_value = name; break
        except (TypeError, ValueError):
            continue
    gl.inputs['Threshold'].default_value = threshold
    gl.inputs['Size'].default_value = rel_size if rel_size is not None else BLOOM_SIZE_AT_7 * 2.0 ** (size - 7)
    gl.inputs['Strength'].default_value = BLOOM_STRENGTH if strength is None else strength

def render_setup(res=(1200, 1600), samples=256, bloom=True, glare_threshold=0.9,
                 glare_size=7, exposure=0.0, bloom_strength=None, bloom_size=None):
    """Cycles + AgX item-card setup. bloom_strength / bloom_size (relative
    0..1) override the calibrated 4.5+/5.x Glare values; glare_size is the
    legacy int kept for 4.0–4.4 and mapped on newer builds."""
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'GPU' if gpu_setup() != 'CPU' else 'CPU'
    s.render.resolution_x, s.render.resolution_y = res
    s.render.resolution_percentage = 100
    s.render.film_transparent = False
    s.cycles.max_bounces = 12; s.cycles.glossy_bounces = 6
    s.cycles.transmission_bounces = 12; s.cycles.caustics_refractive = True
    s.cycles.caustics_reflective = True
    s.cycles.sample_clamp_indirect = 8.0  # kills fireflies from emissive gems
    if denoise_available():
        s.cycles.use_denoising = True; s.cycles.samples = samples
    else:  # no denoiser: buy quality with samples + adaptive sampling
        s.cycles.use_denoising = False; s.cycles.samples = int(samples * 2.5)
    s.cycles.use_adaptive_sampling = True; s.cycles.adaptive_threshold = 0.01
    try:
        s.view_settings.view_transform = 'AgX'
    except TypeError:
        s.view_settings.view_transform = 'Filmic'
    for look in ('AgX - Medium High Contrast', 'Medium High Contrast'):
        try: s.view_settings.look = look; break
        except TypeError: pass
    s.view_settings.exposure = exposure
    if bloom:
        if hasattr(s, 'compositing_node_group'):          # Blender 5.0+
            t = bpy.data.node_groups.new("ForgeCompositor", 'CompositorNodeTree')
            t.interface.new_socket(name="Image", in_out='OUTPUT',
                                   socket_type='NodeSocketColor')
            s.compositing_node_group = t
            out = t.nodes.new('NodeGroupOutput'); out_sock = out.inputs[0]
        else:                                             # 4.x
            s.use_nodes = True
            t = s.node_tree
            for n in list(t.nodes): t.nodes.remove(n)
            out = t.nodes.new('CompositorNodeComposite'); out_sock = out.inputs['Image']
        rl = t.nodes.new('CompositorNodeRLayers')
        gl = t.nodes.new('CompositorNodeGlare')
        _glare_bloom(gl, glare_threshold, glare_size, bloom_strength, bloom_size)
        t.links.new(rl.outputs['Image'], gl.inputs['Image'])
        t.links.new(gl.outputs['Image'], out_sock)
    elif hasattr(s, 'compositing_node_group'):            # detach an earlier bloom
        s.compositing_node_group = None
    else:
        s.use_nodes = False
    return s

def world_dark(color='#07080B', strength=1.0):
    w = bpy.data.worlds.new("StudioWorld"); bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = hex_lin(color); bg.inputs['Strength'].default_value = strength
    return w

def area_light(name, loc, target, energy, size, color='#FFFFFF', shape='RECTANGLE', size_y=None):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energy; d.color = hex_lin(color)[:3]
    d.shape = shape; d.size = size
    if size_y: d.size_y = size_y
    o = bpy.data.objects.new(name, d); bpy.context.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

def studio_rig(target, radius=2.2, rim='#E8A33C', key_energy=900, fill_ratio=0.2,
               rim_energy=700, hair_energy=120, height=1.0):
    """Product rig from the render block: softbox key upper-left 45°, cool fill
    camera-right at ~20%, coloured rim behind-right, faint top hairlight."""
    t = Vector(target)
    key = area_light("Key", t + Vector((-radius*0.95, -radius*0.95, radius*0.95+height*0.3)),
                     t, key_energy, 1.2)
    fill = area_light("Fill", t + Vector((radius*1.25, -radius*0.55, height*0.1)),
                      t, key_energy*fill_ratio, 2.0, color='#C9D4E6')
    rimL = area_light("Rim", t + Vector((radius*0.8, radius*1.1, radius*0.45)),
                      t, rim_energy, 0.6, color=rim, size_y=1.6)
    rimL["forge_rim_energy"] = rim_energy      # retier() scales from this base
    hair = area_light("Hair", t + Vector((0, 0.2, radius*1.35)), t, hair_energy, 0.8)
    return dict(key=key, fill=fill, rim=rimL, hair=hair)

def camera(target, loc, lens=100, dof_fstop=None, name="Cam"):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    co = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(co)
    co.location = loc; look_at(co, target)
    bpy.context.scene.camera = co
    if dof_fstop:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = dof_fstop
        cd.dof.focus_distance = (Vector(target) - Vector(loc)).length
    return co

def frame_camera(cam, objs, margin=1.12):
    """Push the camera back along its view axis until objs fit the frame."""
    s = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    cam_inv = cam.matrix_world.inverted()
    fov = cam.data.angle
    aspect = s.render.resolution_x / s.render.resolution_y
    fx = fov / 2 if aspect >= 1 else math.atan(math.tan(fov/2) * aspect)
    fy = math.atan(math.tan(fov/2) / aspect) if aspect >= 1 else fov / 2
    need = 0.0
    for p in pts:
        lp = cam_inv @ p
        depth = -lp.z
        need = max(need, abs(lp.x)/math.tan(fx) - depth, abs(lp.y)/math.tan(fy) - depth)
    fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    cam.location -= fwd * (need * margin + 0.02)

def frame_fill(cam, objs, fill=0.78):
    """Move the camera along its view axis — IN or OUT — until the objects'
    bounding-box corners fill `fill` of the frame in the limiting direction
    (item cards 0.75-0.8, lessons #3). frame_camera only ever pushes back, so
    a small asset under a far camera stays small. Call AFTER render_setup
    (needs the aspect). Returns the move in metres (+ = back)."""
    s = bpy.context.scene
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    cam_inv = cam.matrix_world.inverted()
    fov = cam.data.angle
    aspect = s.render.resolution_x / s.render.resolution_y
    fx = fov / 2 if aspect >= 1 else math.atan(math.tan(fov / 2) * aspect)
    fy = math.atan(math.tan(fov / 2) / aspect) if aspect >= 1 else fov / 2
    delta = max(max(abs(lp.x) / (math.tan(fx) * fill), abs(lp.y) / (math.tan(fy) * fill)) + lp.z
                for lp in (cam_inv @ p for p in pts))
    fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    cam.location -= fwd * delta
    bpy.context.view_layer.update()
    return delta

def backdrop_radial(center, cam_loc, color='#1A1510', edge='#040506', strength=1.0,
                    size=6.0, dist=1.6, falloff=0.55):
    """Item-card backdrop: a camera-facing plane behind the subject with a soft
    radial glow — the 'dark background with radial falloff' of the render block."""
    c = Vector(center); d = (c - Vector(cam_loc)).normalized()
    bpy.ops.mesh.primitive_plane_add(size=size, location=c + d*dist)
    bd = bpy.context.object; bd.name = "Backdrop"
    look_at(bd, cam_loc); bd.rotation_euler.rotate_axis('X', math.radians(180))
    mb = MB("BackdropMat"); nt = mb.nt; nt.nodes.remove(mb.p)
    tc = mb.n('ShaderNodeTexCoord'); gr = mb.n('ShaderNodeTexGradient', gradient_type='SPHERICAL')
    mp = mb.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1/(size*falloff),)*3
    mb.link(tc.outputs['Object'], mp.inputs['Vector']); mb.link(mp.outputs[0], gr.inputs['Vector'])
    col = mb.mix_col(gr.outputs['Fac'], hex_lin(edge), hex_lin(color))
    em = mb.n('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    mb.link(col, em.inputs['Color']); mb.link(em.outputs[0], mb.out.inputs['Surface'])
    bd.data.materials.append(mb.mat)
    bd.visible_shadow = False
    try: bd.visible_glossy = False
    except AttributeError: pass
    return bd

def bounds(objs):
    """World-space (center, size) of a set of objects — for staging and framing."""
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return (lo + hi) / 2, hi - lo

def floor(size=40, color='#0B0C10', rough=0.32, z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    f = bpy.context.object; f.name = "Floor"
    m = bpy.data.materials.new("FloorMat"); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    set_in(p, IN["base"], hex_lin(color)); set_in(p, IN["rough"], rough)
    f.data.materials.append(m)
    return f

# ─────────────────────────────── real-form modeling ─────────────────────────
def mesh_from_bm(bm, name):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    return ob

def loft(name, sections, closed_start=True, closed_end=True, tip=None):
    """Loft rings of 3D points (each a list of equal length) into a quad mesh.
    The core technique for blades, spars, limbs, handles: design a CROSS-SECTION,
    then vary it along the length (distal taper, profile taper, fuller)."""
    bm = bmesh.new(); rings = []
    for ring in sections:
        rings.append([bm.verts.new(p) for p in ring])
    n = len(rings[0])
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    if closed_start: bm.faces.new(list(reversed(rings[0])))
    if tip is not None:       # a true point: fan to one vertex (no degenerate micro-cap)
        tv = bm.verts.new(tip); last = rings[-1]
        for i in range(n): bm.faces.new((last[i], last[(i+1) % n], tv))
    elif closed_end:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_from_bm(bm, name)

def lathe(name, profile, segments=48, axis='Z', cap=True):
    """Revolve a 2D profile [(radius, height), ...] — pommels, gems, helm bowls,
    towers, finials. Radius 0 points close the pole cleanly."""
    bm = bmesh.new(); rings = []
    for r, h in profile:
        ring = []
        count = 1 if r < 1e-6 else segments
        for k in range(count):
            a = 2*math.pi*k/segments
            ring.append(bm.verts.new((r*math.cos(a), r*math.sin(a), h)))
        rings.append(ring)
    for a, b in zip(rings[:-1], rings[1:]):
        if len(a) == 1 and len(b) == 1: continue
        if len(a) == 1:
            for i in range(segments): bm.faces.new((a[0], b[i], b[(i+1) % segments]))
        elif len(b) == 1:
            for i in range(segments): bm.faces.new((a[i], a[(i+1) % segments], b[0]))
        else:
            for i in range(segments):
                j = (i+1) % segments
                bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap:                   # open ring ends -> n-gon caps (watertight)
        if len(rings[0]) > 1: bm.faces.new(list(reversed(rings[0])))
        if len(rings[-1]) > 1: bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_from_bm(bm, name)

def sweep(name, points, radius=0.004, res=6, taper=None, closed=False, bevel_caps=True):
    """Tube swept along a polyline (wire wraps, filigree, chains, lacing, straps).
    taper: optional list of radius multipliers per point."""
    cd = bpy.data.curves.new(name, 'CURVE'); cd.dimensions = '3D'
    cd.bevel_depth = radius; cd.bevel_resolution = res; cd.use_fill_caps = bevel_caps
    sp = cd.splines.new('POLY'); sp.points.add(len(points)-1)
    for i, p in enumerate(points):
        sp.points[i].co = (*p, 1)
        if taper: sp.points[i].radius = taper[i]
    sp.use_cyclic_u = closed
    ob = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(ob)
    m = to_mesh(ob)
    # curve fill-caps convert as separate n-gons: weld them to the tube (within
    # THIS part only — never weld across parts) so the part is watertight
    bm = bmesh.new(); bm.from_mesh(m.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(m.data); bm.free()
    return m

def helix(center, radius, z0, z1, turns, pts_per_turn=24, phase=0.0):
    out = []; total = max(2, int(turns*pts_per_turn))
    for i in range(total+1):
        t = i/total; a = phase + 2*math.pi*turns*t
        out.append((center[0]+radius*math.cos(a), center[1]+radius*math.sin(a), z0+(z1-z0)*t))
    return out

def to_mesh(ob):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True); bpy.context.view_layer.objects.active = ob
    bpy.ops.object.convert(target='MESH')
    return bpy.context.object

def hard_surface(ob, width=0.0015, segments=3, angle=30, weighted=True, smooth=True):
    """Pro hard-surface finish: angle-limited bevel so edges catch light,
    weighted normals so flat faces shade flat, smooth shading everywhere."""
    b = ob.modifiers.new("Bevel", 'BEVEL'); b.width = width; b.segments = segments
    b.limit_method = 'ANGLE'; b.angle_limit = math.radians(angle)
    b.harden_normals = True; b.profile = 0.7
    if smooth:
        for p in ob.data.polygons: p.use_smooth = True
        if V < (4, 1, 0):
            ob.data.use_auto_smooth = True; ob.data.auto_smooth_angle = math.radians(angle)
    if weighted:
        w = ob.modifiers.new("WeightedNormal", 'WEIGHTED_NORMAL'); w.keep_sharp = True
        w.weight = 50
    return ob

def subsurf(ob, levels=2):
    m = ob.modifiers.new("Subsurf", 'SUBSURF'); m.levels = levels; m.render_levels = levels
    for p in ob.data.polygons: p.use_smooth = True
    return ob

def flat(ob):
    for p in ob.data.polygons: p.use_smooth = False
    return ob

def assign(ob, mat):
    ob.data.materials.clear(); ob.data.materials.append(mat); return ob

def apply_mods(ob):
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    for m in list(ob.modifiers):
        try: bpy.ops.object.modifier_apply(modifier=m.name)
        except RuntimeError: ob.modifiers.remove(m)

# ─────────────────────────── construction operators ─────────────────────────
# Armourers' and jewellers' constructions, each producing WATERTIGHT parts
# (tests/test_operators.py). Orientation: +Z up, the face/front toward -Y.

def _v3(p):
    return Vector((p[0], p[1], p[2] if len(p) > 2 else 0.0))

def _cumlen(P):
    L = [0.0]
    for a, b in zip(P, P[1:]):
        L.append(L[-1] + (b - a).length)
    return L

def _at_length(P, L, s):
    j = min(max(bisect.bisect_right(L, s) - 1, 0), len(P) - 2)
    seg = L[j + 1] - L[j]
    return P[j].lerp(P[j + 1], 0.0 if seg < 1e-12 else (s - L[j]) / seg)

def resample(points, n, closed=False, smooth=True):
    """Resample a polyline to n points evenly spaced by arc length.
    smooth=True first runs it through a Catmull-Rom spline (passes through
    every input point). closed=True returns n distinct points around a loop."""
    P = [_v3(p) for p in points]
    m = len(P)
    if smooth and m > 2:
        dense, segs = [], (m if closed else m - 1)
        for i in range(segs):
            p0 = P[(i - 1) % m] if closed else P[max(i - 1, 0)]
            p1, p2 = P[i], P[(i + 1) % m]
            p3 = P[(i + 2) % m] if closed else P[min(i + 2, m - 1)]
            for k in range(16):
                t = k / 16; t2 = t * t; t3 = t2 * t
                dense.append(0.5 * ((2 * p1) + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                                    + (3 * p1 - p0 - 3 * p2 + p3) * t3))
        if not closed:
            dense.append(P[-1])
        P = dense
    if closed:
        P = P + [P[0].copy()]
    L = _cumlen(P); total = L[-1]
    return [_at_length(P, L, total * (k / n if closed else k / max(n - 1, 1))) for k in range(n)]

def path_frames(points, up=(0, 0, 1)):
    """Parallel-transport frames [(T, N, B), ...] along a polyline: N starts as
    `up` projected off the tangent and is carried along without twist flips;
    B = T x N. Straps, lacing, rolled edges and anything with a flat section."""
    P = [_v3(p) for p in points]; n = len(P)
    T = [(P[min(i + 1, n - 1)] - P[max(i - 1, 0)]).normalized() for i in range(n)]
    u = Vector(up); N = u - T[0] * u.dot(T[0])
    if N.length < 1e-6:
        alt = Vector((1, 0, 0)) if abs(T[0].x) < 0.9 else Vector((0, 1, 0))
        N = alt - T[0] * alt.dot(T[0])
    N.normalize()
    frames = [(T[0], N, T[0].cross(N))]
    for i in range(1, n):
        N = T[i - 1].rotation_difference(T[i]) @ frames[-1][1]
        N = (N - T[i] * N.dot(T[i])).normalized()
        frames.append((T[i], N, T[i].cross(N)))
    return frames

def _strip_uvs(ob):
    """Operators joining curve-derived parts (UVs) with lofted/lathed ones (no
    UVs) would hand on PARTIAL UVs — lessons #14. Leave none: the bake unwraps."""
    while ob.data.uv_layers:
        ob.data.uv_layers.remove(ob.data.uv_layers[0])
    return ob

def _shell(ob, thickness):
    """Give an open sheet real thickness INWARD (against its normals), watertight."""
    s = ob.modifiers.new("Thickness", 'SOLIDIFY'); s.thickness = thickness; s.offset = -1.0
    s.use_even_offset = True; s.use_quality_normals = True; s.use_rim = True
    apply_mods(ob)
    return ob

def helm_shell(name, radius=0.105, height=0.15, thickness=0.0018, segments=64, rings=36,
               squareness=2.0, apex=0.0, tail=0.0, tail_flare=0.0, tail_width=140.0,
               brim=0.0, brim_droop=0.25, roll=0.0022):
    """A raised helm bowl — one sheet of steel, as an armourer raises it.
    The bowl is a lathed superellipse profile (crown -> rim; squareness 2 =
    round, higher = flatter crown; apex > 0 draws the crown up into a bascinet
    point). Its lower edge is drawn out, per azimuth, into a TAIL at the back
    (sallet: drop `tail`, outward `tail_flare`, over `tail_width` degrees) or a
    BRIM all round (kettle hat: `brim`), so bowl and tail are ONE surface — no
    seam, no stacked parts. Real `thickness` (solidified inward) and an optional
    armourer's ROLLED rim (a tube along the edge). Face toward -Y, tail +Y.
    Openings, visor slits and sights: boolean_cut()."""
    R, H = radius, height
    ex = 2.0 / max(squareness, 1e-3)
    half = math.radians(max(tail_width, 1e-3)) / 2
    bowl = []
    for i in range(193):
        th = (math.pi / 2) * i / 192
        st = math.sin(th)
        bowl.append(Vector((R * st ** ex, 0.0, H * max(math.cos(th), 0.0) ** ex + apex * H * (1 - st) ** 2)))
    Lb = _cumlen(bowl)[-1]
    n_top = max(4, int(rings * 0.6)); n_low = max(3, rings - n_top)
    cut = 0.7 * Lb                        # upper 70% of the bowl: identical rings at every azimuth
    ring_pts = [[] for _ in range(n_top + n_low)]
    edge_n = []
    for j in range(segments):
        phi = 2 * math.pi * j / segments
        d = abs((phi - math.pi / 2 + math.pi) % (2 * math.pi) - math.pi)
        w = math.cos(d / half * math.pi / 2) ** 2 if (tail > 0 or tail_flare > 0) and d < half else 0.0
        prof = list(bowl)
        if brim > 0 or w > 0:
            for i in range(1, 49):
                v = i / 48
                prof.append(Vector((R + brim * v + tail_flare * w * v * v, 0.0,
                                    -brim * brim_droop * v ** 1.5 - tail * w * v)))
        L = _cumlen(prof); total = L[-1]
        c, s_ = math.cos(phi), math.sin(phi)
        samples = [cut * k / n_top for k in range(1, n_top + 1)]
        samples += [cut + (total - cut) * k / n_low for k in range(1, n_low + 1)]
        for k, sl in enumerate(samples):
            q = _at_length(prof, L, sl)
            ring_pts[k].append(Vector((q.x * c, q.x * s_, q.z)))
        tq = (prof[-1] - prof[-2]).normalized()            # outward normal at the edge (r-z plane)
        nr = Vector((-tq.z, 0.0, tq.x))
        if nr.x < 0: nr = -nr
        edge_n.append(Vector((nr.x * c, nr.x * s_, nr.z)).normalized())
    bm = bmesh.new()
    apex_v = bm.verts.new((0.0, 0.0, bowl[0].z))
    V = [[bm.verts.new(p) for p in ring] for ring in ring_pts]
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new((apex_v, V[0][i], V[0][j]))
        for a, b in zip(V[:-1], V[1:]):
            bm.faces.new((a[i], b[i], b[j], a[j]))          # outward winding
    ob = mesh_from_bm(bm, name)
    for p in ob.data.polygons: p.use_smooth = True
    _shell(ob, thickness)
    if roll > 0:
        rim = [p + n * (roll - thickness) for p, n in zip(ring_pts[-1], edge_n)]
        tube = sweep(name + "_Roll", resample(rim, segments * 2, closed=True), radius=roll, res=4, closed=True)
        for p in tube.data.polygons: p.use_smooth = True
        ob = join([ob, tube], name)
    _strip_uvs(ob)
    ob["forge_op"] = "helm_shell"
    return ob

def slot_cutter(name, length=0.06, width=0.006, depth=0.06, segments=10):
    """Cutter for boolean_cut(): a stadium-section prism (rounded-end slot)
    running along X, `width` tall in Z, `depth` through along Y. length ==
    width gives a round hole. Place and rotate it, then boolean_cut()."""
    r = min(width, length) / 2; half = max(0.0, length / 2 - r)
    out = []
    for cx, a0 in ((half, -math.pi / 2), (-half, math.pi / 2)):
        for k in range(segments + 1):
            a = a0 + math.pi * k / segments
            q = (cx + r * math.cos(a), r * math.sin(a))
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    if abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return loft(name, [[(x, y, z) for (x, z) in out] for y in (-depth / 2, depth / 2)])

def _shell_count(me):
    """Connected components of a mesh (union-find over edges)."""
    parent = list(range(len(me.vertices)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for e in me.edges:
        a, b = find(e.vertices[0]), find(e.vertices[1])
        if a != b: parent[a] = b
    return len({find(i) for i in range(len(me.vertices))})

def _bbox_world(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (Vector([min(p[i] for p in pts) for i in range(3)]),
            Vector([max(p[i] for p in pts) for i in range(3)]))

def _boxes_meet(a, b):
    return all(a[0][i] <= b[1][i] and b[0][i] <= a[1][i] for i in range(3))

def _apply_cut(ob, cutter, solver):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True); bpy.context.view_layer.objects.active = ob
    m = ob.modifiers.new("Cut", 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = cutter
    solvers = {i.identifier for i in m.bl_rna.properties['solver'].enum_items}
    m.solver = solver if solver in solvers else 'EXACT'
    idx = len(ob.modifiers) - 1
    if idx:                                # boolean FIRST: the bevel then rounds the new rims
        try:
            ob.modifiers.move(idx, 0)
        except (AttributeError, TypeError, RuntimeError):
            bpy.ops.object.modifier_move_to_index(modifier=m.name, index=0)
    bpy.ops.object.modifier_apply(modifier=m.name)

def boolean_cut(target, cutters, bevel=0.0005, segments=2, solver='EXACT', keep_cutters=False,
                weld=None):
    """Cut `cutters` (one object or a list) out of `target` — DIFFERENCE,
    applied in place at the TOP of the modifier stack so an existing
    hard_surface() bevel then rounds the new rims — and clean the result so it
    reads machined, not boolean'd. Visor slits, sights, breaths, rivet holes,
    arrow loops, crenels. Cutters are deleted unless keep_cutters.
    - A target made of SEVERAL closed shells (a helm with its rolled rim,
      lames, fittings) is cut shell by shell: EXACT on overlapping shells
      turned a rolled sallet inside out (volume up, 20 non-manifold edges).
    - weld (default max(0.1 mm, 20% of the bevel width)), applied ONLY near
      the cuts: the cut leaves 20-100 um edges where faceted cutter ends meet
      a curved shell, and a bevel turns them into degenerate micro-quads.
    - A target without a bevel gets hard_surface(bevel)."""
    cutters = list(cutters) if isinstance(cutters, (list, tuple)) else [cutters]
    bpy.context.view_layer.update()        # matrix_world is STALE after .location/.rotation edits
    bw = max([m.width for m in target.modifiers if m.type == 'BEVEL'] + [bevel or 0.0])
    weld = max(1e-4, 0.2 * bw) if weld is None else weld
    boxes = [_bbox_world(c) for c in cutters]
    pieces = [target]
    if _shell_count(target.data) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        target.select_set(True); bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
        pieces = [target] + [o for o in bpy.context.selected_objects if o is not target]
    for p in pieces:
        pb = _bbox_world(p)
        for c, cb in zip(cutters, boxes):
            if _boxes_meet(pb, cb):
                _apply_cut(p, c, solver)
    if len(pieces) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for p in pieces: p.select_set(True)
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.join()
    if not keep_cutters:
        for c in cutters:
            me = c.data if c.type == 'MESH' else None
            bpy.data.objects.remove(c, do_unlink=True)
            if me is not None and me.users == 0:
                bpy.data.meshes.remove(me)
    inv = target.matrix_world.inverted(); local = []
    for lo, hi in boxes:                   # cutter boxes in target space, padded
        cs = [inv @ Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
        local.append((Vector([min(c[i] for c in cs) - 2 * weld for i in range(3)]),
                      Vector([max(c[i] for c in cs) + 2 * weld for i in range(3)])))
    def near(co):
        return any(all(lo[i] <= co[i] <= hi[i] for i in range(3)) for lo, hi in local)
    bm = bmesh.new(); bm.from_mesh(target.data)
    bmesh.ops.dissolve_degenerate(bm, dist=weld, edges=[e for e in bm.edges
                                                        if near(e.verts[0].co) and near(e.verts[1].co)])
    bmesh.ops.remove_doubles(bm, verts=[v for v in bm.verts if near(v.co)], dist=weld)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(target.data); bm.free(); target.data.update()
    if bevel and not any(md.type == 'BEVEL' for md in target.modifiers):
        hard_surface(target, bevel, segments)
    return target

def plate(name, profile, height, thickness=0.0016, cols=36, rows=10, bulge=0.0, taper=0.0,
          roll=0.0, roll_edges=('top',), lames=1, overlap=0.28, gap=0.0004, lames_behind=True):
    """Armour plate from a PROFILE CURVE. `profile` is the plate's horizontal
    cross-section [(x, y), ...] drawn left -> right (open; e.g. an arc with a
    medial ridge); the outer face is to its right (toward -Y for +X). The
    sheet rises to `height` with a vertical belly (`bulge`) and `taper`
    (narrower at the top), gets real `thickness` (solidified inward), ROLLED
    edges ('top'/'bottom': armourer's roll, a tube along the edge), and can be
    split into `lames` — overlapping articulated strips (faulds, tassets,
    pauldrons), each lower lame behind the one above (lames_behind) so blows
    glance off. Returns one object of closed shells."""
    prof = resample([(p[0], p[1], 0.0) for p in profile], cols, smooth=True)
    cx = sum(p.x for p in prof) / len(prof)
    nrm = []
    for i in range(cols):
        t = (prof[min(i + 1, cols - 1)] - prof[max(i - 1, 0)]).normalized()
        nrm.append(Vector((t.y, -t.x, 0.0)))
    lames = max(1, int(lames))
    lame_h = height / (lames - (lames - 1) * overlap)
    step = lame_h * (1 - overlap)
    parts, edges = [], {}
    for k in range(lames):
        z_bot = height - k * step - lame_h
        off = k * (thickness + gap) * (-1.0 if lames_behind else 1.0)
        grid = []
        for r in range(rows + 1):
            z = z_bot + lame_h * r / rows
            hz = z / height
            w = 1.0 - taper * hz
            b = bulge * math.sin(math.pi * min(max(hz, 0.0), 1.0))
            grid.append([Vector((cx + (p.x - cx) * w, p.y, z)) + n * (b + off) for p, n in zip(prof, nrm)])
        bm = bmesh.new()
        Vg = [[bm.verts.new(p) for p in row] for row in grid]
        for r in range(rows):
            for i in range(cols - 1):
                bm.faces.new((Vg[r][i], Vg[r][i + 1], Vg[r + 1][i + 1], Vg[r + 1][i]))
        sheet = mesh_from_bm(bm, "%s_L%d" % (name, k))
        for p in sheet.data.polygons: p.use_smooth = True
        parts.append(_shell(sheet, thickness))
        edges[k] = (grid[0], grid[-1])
    if roll > 0:
        for which in roll_edges:
            if which == 'top':
                row = edges[0][1]
            elif which == 'bottom':
                row = edges[lames - 1][0]
            else:
                continue
            path = [p + n * (roll - thickness) for p, n in zip(row, nrm)]
            tube = sweep("%s_Roll_%s" % (name, which), resample(path, cols * 2), radius=roll, res=4)
            for p in tube.data.polygons: p.use_smooth = True
            parts.append(tube)
    ob = join(parts, name) if len(parts) > 1 else parts[0]
    ob.name = name; _strip_uvs(ob); ob["forge_op"] = "plate"
    return ob

def rivet(name="Rivet", head_r=0.004, head_h=0.0022, shank_r=None, shank_h=0.003, segments=16):
    """Round-head (snap) rivet, lathed and watertight: a domed head with a crisp
    underside and a shank to sink into the plate. Local +Z = head axis,
    z = 0 = underside of the head."""
    shank_r = shank_r or head_r * 0.45
    prof = [(0.0, head_h)] + [(head_r * math.sin(a), head_h * math.cos(a))
                              for a in [math.pi / 2 * k / 6 for k in range(1, 7)]]
    prof += [(shank_r, 0.0), (shank_r, -shank_h), (0.0, -shank_h)]
    ob = lathe(name, prof, segments)
    for p in ob.data.polygons: p.use_smooth = True
    return ob

def rivet_row(name, path, count=None, spacing=0.03, head_r=0.004, head_h=0.0022,
              normal=(0, -1, 0), surface=None, sink=0.0004, join=True, segments=16, inset=True):
    """Rivets along a polyline at equal arc-length spacing (inset: half a gap
    at each end), heads along `normal`, or along the surface normal of
    `surface` (snapped to its closest point), sunk `sink` so nothing floats.
    ONE rivet mesh is built and instanced: join=False returns linked
    duplicates sharing it; join=True (default) one object for bake/export.
    The object carries forge_rivet_pts / forge_rivet_nrm (flat xyz lists)."""
    P = [_v3(p) for p in path]
    L = _cumlen(P); total = L[-1]
    if count is None:
        count = max(2, int(round(total / spacing)) + (0 if inset else 1))
    if surface is not None:
        bpy.context.view_layer.update()    # a surface moved just before would have a stale matrix
    ts = [(k + 0.5) / count for k in range(count)] if inset else [k / max(count - 1, 1) for k in range(count)]
    dg = bpy.context.evaluated_depsgraph_get() if surface is not None else None
    if surface is not None:
        inv = surface.matrix_world.inverted()
        nmat = surface.matrix_world.to_3x3().inverted().transposed()
    place = []
    for t in ts:
        p = _at_length(P, L, t * total); n = Vector(normal).normalized()
        if surface is not None:
            ok, loc, nor, _ = surface.closest_point_on_mesh(inv @ p, depsgraph=dg)
            if ok:
                p = surface.matrix_world @ loc; n = (nmat @ nor).normalized()
        place.append((p, n))
    proto = rivet(name + "_proto", head_r, head_h, segments=segments)
    me = proto.data
    mats = [Matrix.Translation(p - n * sink) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4() for p, n in place]
    if not join:
        objs = []
        for k, M in enumerate(mats):
            o = bpy.data.objects.new("%s.%02d" % (name, k), me); bpy.context.collection.objects.link(o)
            o.matrix_world = M; objs.append(o)
        bpy.data.objects.remove(proto, do_unlink=True)
        return objs
    bv = [v.co.copy() for v in me.vertices]; bf = [tuple(p.vertices) for p in me.polygons]
    verts, faces = [], []
    for M in mats:
        off = len(verts)
        verts += [M @ v for v in bv]
        faces += [tuple(i + off for i in f) for f in bf]
    out = bpy.data.meshes.new(name); out.from_pydata(verts, [], faces); out.update()
    for poly in out.polygons: poly.use_smooth = True
    ob = bpy.data.objects.new(name, out); bpy.context.collection.objects.link(ob)
    bpy.data.objects.remove(proto, do_unlink=True); bpy.data.meshes.remove(me)
    ob["forge_rivet_pts"] = [c for p, _ in place for c in p]
    ob["forge_rivet_nrm"] = [c for _, n in place for c in n]
    ob["forge_op"] = "rivet_row"
    return ob

def _rounded_rect(hw, hh, rc, res):
    """Counter-clockwise rounded rectangle, half-extents hw x hh, corner rc."""
    rc = max(1e-7, min(rc, hw, hh))
    out = []
    for cx, cy, a0 in ((hw - rc, hh - rc, 0.0), (-hw + rc, hh - rc, 90.0),
                       (-hw + rc, -hh + rc, 180.0), (hw - rc, -hh + rc, 270.0)):
        for k in range(res + 1):
            a = math.radians(a0 + 90.0 * k / res)
            q = (cx + rc * math.cos(a), cy + rc * math.sin(a))
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    if abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out

def strap(name, path, width=0.025, thickness=0.003, up=(0, 0, 1), corner=0.6, res=3,
          step=0.004, tip='flat'):
    """Leather strap: a rounded-rectangle section (width x thickness, edges
    rounded by `corner`) lofted along a smoothed path with parallel-transport
    frames (no twist flips); `up` = the side the strap's face looks to at the
    start. tip='round' rounds the end like a cut belt tip. Watertight."""
    P = [_v3(p) for p in path]
    total = _cumlen(P)[-1]
    pts = resample(P, max(4, int(total / step) + 1), smooth=True)
    frames = path_frames(pts, up)
    sec = _rounded_rect(width / 2, thickness / 2, corner * thickness / 2, res)
    L = _cumlen(pts)
    sections = []
    for i, (p, (T, N, B)) in enumerate(zip(pts, frames)):
        sw = 1.0
        if tip == 'round':
            rem = L[-1] - L[i]
            if rem < width / 2:
                u = 1 - rem / (width / 2)
                sw = max(0.18, math.sqrt(max(0.0, 1 - u * u)))
        sections.append([p + B * (x * sw) + N * y for (x, y) in sec])
    ob = loft(name, sections, closed_start=True, closed_end=True)
    for poly in ob.data.polygons: poly.use_smooth = True
    ob["forge_op"] = "strap"
    return ob

def buckle(name, width=0.03, height=0.024, wire_r=0.0022, corner=0.35, prong=True):
    """Centre-bar buckle: a rounded-rectangle frame (a closed swept wire), a
    bar across its middle, and a tapered prong hinged on the bar resting on
    the far side. Frame in XY (strap runs along Y through it, width along X),
    prong on +Z. Watertight shells; forge_inner_width = the strap opening."""
    hw, hh = width / 2, height / 2
    loop = _rounded_rect(hw, hh, corner * min(hw, hh), 6)
    parts = [sweep(name + "_Frame", [(x, y, 0.0) for x, y in loop], radius=wire_r, res=4, closed=True),
             sweep(name + "_Bar", [(-hw, 0.0, 0.0), (hw, 0.0, 0.0)], radius=wire_r * 0.85, res=4)]
    if prong:
        pr = resample([(0.0, 0.0, wire_r * 0.9), (0.0, hh * 0.45, wire_r * 1.6),
                       (0.0, hh * 0.85, wire_r * 1.3), (0.0, hh + wire_r * 0.25, wire_r * 0.6)], 12)
        parts.append(sweep(name + "_Prong", pr, radius=wire_r * 0.7, res=4,
                           taper=[1.0 - 0.45 * k / 11 for k in range(12)]))
    for o in parts:
        for p in o.data.polygons: p.use_smooth = True
    ob = join(parts, name)
    _strip_uvs(ob)
    ob["forge_inner_width"] = width - 2 * wire_r
    ob["forge_op"] = "buckle"
    return ob

def strap_buckle(name, path, width=0.025, thickness=0.003, at=0.35, up=(0, 0, 1),
                 wire_r=None, tip='round'):
    """A strap along `path` with a centre-bar buckle seated on it at arc
    fraction `at`, sized so the strap passes through. Returns (strap, buckle)."""
    st = strap(name + "_Strap", path, width, thickness, up=up, tip=tip)
    wire_r = wire_r or max(0.0015, width * 0.085)
    bw = width + 2 * (wire_r + 0.0015)
    bk = buckle(name + "_Buckle", width=bw, height=width * 0.95, wire_r=wire_r)
    P = resample(path, 64, smooth=True); fr = path_frames(P, up)
    i = min(63, max(0, int(round(at * 63))))
    T, N, B = fr[i]
    rot = Matrix((B, T, N)).transposed().to_4x4()
    bk.matrix_world = Matrix.Translation(P[i] + N * (thickness / 2 + wire_r * 0.35)) @ rot
    return st, bk

def gem_brilliant(name, diameter=0.01, table=0.56, crown=0.162, pavilion=0.431, girdle=0.03,
                  star=0.5, lower_girdle=0.77, mains=8):
    """Round brilliant with the REAL facet plan (Tolkowsky proportions, as
    fractions of the diameter): table; 8 star + 8 bezel kites + 16 upper-girdle
    facets on the crown; a 16-facet girdle; 16 lower-girdle facets + 8
    pavilion mains to a pointed culet — 73 PLANAR faces (every kite is solved
    onto its facet plane), flat-shaded so each facet flashes on its own.
    Girdle centred on z = 0, table up. Pair with mat_gem()."""
    R = diameter / 2; g = girdle * diameter / 2
    z_t = g + crown * diameter; r_t = table * R; z_c = -g - pavilion * diameter
    n = mains; da = 2 * math.pi / n
    bm = bmesh.new(); nv = bm.verts.new
    def at(r, a, z): return nv((r * math.cos(a), r * math.sin(a), z))
    slope_c = (g - z_t) / (R - r_t)                       # bezel plane: z = z_t + (u - r_t) * slope_c
    apo = r_t * math.cos(da / 2)
    rho_s = apo + star * (R - apo)
    z_s = z_t + (rho_s * math.cos(da / 2) - r_t) * slope_c
    slope_p = (-g - z_c) / R                              # main plane: z = z_c + u * slope_p
    rho_m = lower_girdle * R
    z_m = z_c + rho_m * math.cos(da / 2) * slope_p
    T = [at(r_t, i * da, z_t) for i in range(n)]
    S = [at(rho_s, i * da + da / 2, z_s) for i in range(n)]
    Gt = [at(R, j * da / 2, g) for j in range(2 * n)]
    Gb = [at(R, j * da / 2, -g) for j in range(2 * n)]
    M = [at(rho_m, i * da + da / 2, z_m) for i in range(n)]
    C = nv((0.0, 0.0, z_c))
    f = bm.faces.new
    f(T)
    for i in range(n):
        j, a, b, c2 = (i + 1) % n, 2 * i, 2 * i + 1, (2 * i + 2) % (2 * n)
        f((T[i], S[i], T[j]))                              # star
        f((T[i], S[i - 1], Gt[a], S[i]))                   # bezel kite
        f((S[i], Gt[a], Gt[b])); f((S[i], Gt[b], Gt[c2]))  # upper girdle pair
        f((C, M[i - 1], Gb[a], M[i]))                      # pavilion main kite
        f((M[i], Gb[a], Gb[b])); f((M[i], Gb[b], Gb[c2]))  # lower girdle pair
    for j in range(2 * n):
        k = (j + 1) % (2 * n)
        f((Gt[j], Gb[j], Gb[k], Gt[k]))                    # girdle facets
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = mesh_from_bm(bm, name)
    flat(ob); ob["forge_op"] = "gem_brilliant"
    return ob

def gem_cabochon(name, rx=0.008, ry=0.006, height=0.005, base=0.0008, segments=48, rings=14, dome=1.0):
    """Cabochon: a smooth oval dome (rx x ry, `height`) on a short girdle wall
    (`base`) with a softly chamfered flat back — lathed, scaled to the oval,
    watertight, smooth-shaded. dome > 1 = fuller shoulders."""
    prof = [(0.0, base + height)]
    for k in range(1, rings + 1):
        th = (math.pi / 2) * k / rings
        prof.append((rx * math.sin(th), base + height * max(math.cos(th), 0.0) ** (1.0 / dome)))
    prof += [(rx, base * 0.25), (rx * 0.97, 0.0), (0.0, 0.0)]
    ob = lathe(name, prof, segments)
    ob.data.transform(Matrix.Diagonal((1.0, ry / rx, 1.0, 1.0)))
    for p in ob.data.polygons: p.use_smooth = True
    ob["forge_op"] = "gem_cabochon"
    return ob

# ─────────────────────────────── material system ────────────────────────────
class MB:
    """Tiny node-graph builder: MB(name) → .p (principled) … .mat"""
    def __init__(self, name):
        self.mat = bpy.data.materials.new(name); self.mat.use_nodes = True
        self.nt = self.mat.node_tree; self.p = self.nt.nodes["Principled BSDF"]
        self.out = self.nt.nodes["Material Output"]
    def n(self, t, **kw):
        node = self.nt.nodes.new(t)
        for k, v in kw.items():
            if k.startswith("in_"): node.inputs[k[3:].replace("_", " ")].default_value = v
            else: setattr(node, k, v)
        return node
    def link(self, a, b): self.nt.links.new(a, b)
    def math(self, op, a=None, b=None, clamp=False):
        m = self.n('ShaderNodeMath', operation=op, use_clamp=clamp)
        if isinstance(a, (int, float)): m.inputs[0].default_value = a
        elif a is not None: self.link(a, m.inputs[0])
        if isinstance(b, (int, float)): m.inputs[1].default_value = b
        elif b is not None: self.link(b, m.inputs[1])
        return m.outputs[0]
    def mix_col(self, fac, c1, c2):
        m = self.n('ShaderNodeMix', data_type='RGBA', blend_type='MIX')
        self._feed(fac, m.inputs[0]); self._feed(c1, m.inputs[6]); self._feed(c2, m.inputs[7])
        return m.outputs[2]
    def mix_f(self, fac, a, b):
        m = self.n('ShaderNodeMix', data_type='FLOAT')
        self._feed(fac, m.inputs[0]); self._feed(a, m.inputs[2]); self._feed(b, m.inputs[3])
        return m.outputs[0]
    def _feed(self, v, sock):
        if hasattr(v, "is_linked") or hasattr(v, "links"): self.link(v, sock)
        else: sock.default_value = v
    def map_range(self, src, a, b, c=0.0, d=1.0, smooth=True):
        m = self.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP' if smooth else 'LINEAR',
                   clamp=True)
        self._feed(src, m.inputs['Value'])
        m.inputs['From Min'].default_value = a; m.inputs['From Max'].default_value = b
        m.inputs['To Min'].default_value = c; m.inputs['To Max'].default_value = d
        return m.outputs['Result']
    def obj_axis(self, axis):
        tc = self.n('ShaderNodeTexCoord'); sp = self.n('ShaderNodeSeparateXYZ')
        self.link(tc.outputs['Object'], sp.inputs[0]); return sp.outputs[axis]
    def ramp(self, src, stops):
        r = self.n('ShaderNodeValToRGB'); self._feed(src, r.inputs[0])
        els = r.color_ramp.elements
        els[0].position, els[0].color = stops[0][0], (stops[0][1],)*3+(1,)
        els[1].position, els[1].color = stops[-1][0], (stops[-1][1],)*3+(1,)
        for pos, val in stops[1:-1]:
            e = els.new(pos); e.color = (val,)*3+(1,)
        return r.outputs[0]

def _edge_mask(mb, width=0.004, contrast=(0.30, 0.55)):
    """Convex-edge mask via AO 'inside' — where wear lives (Cycles/bake)."""
    ao = mb.n('ShaderNodeAmbientOcclusion', inside=True, samples=12)
    ao.inputs['Distance'].default_value = width
    inv = mb.math('SUBTRACT', 1.0, ao.outputs['AO'])
    return mb.ramp(inv, [(contrast[0], 0.0), (contrast[1], 1.0)])

def _cavity_mask(mb, dist=0.02):
    ao = mb.n('ShaderNodeAmbientOcclusion', samples=12)
    ao.inputs['Distance'].default_value = dist
    return mb.ramp(ao.outputs['AO'], [(0.35, 1.0), (0.85, 0.0)])

def _noise(mb, scale, detail=6, rough=0.55, coord='Object', stretch=None):
    tc = mb.n('ShaderNodeTexCoord')
    src = tc.outputs[coord]
    if stretch:
        mp = mb.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch
        mb.link(src, mp.inputs['Vector']); src = mp.outputs['Vector']
    nz = mb.n('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = detail; nz.inputs['Roughness'].default_value = rough
    mb.link(src, nz.inputs['Vector'])
    return nz.outputs['Fac']

def _bump(mb, height, strength=0.25, distance=0.002, extra_normal=None):
    b = mb.n('ShaderNodeBump'); b.inputs['Strength'].default_value = strength
    b.inputs['Distance'].default_value = distance
    mb.link(height, b.inputs['Height'])
    if extra_normal is not None: mb.link(extra_normal, b.inputs['Normal'])
    return b.outputs['Normal']

def _micro_bevel(mb, radius=0.0012):
    """Bevel shader node: rounded edge normals so every hard edge catches a
    thin highlight — the cheapest single realism upgrade in the kit."""
    bv = mb.n('ShaderNodeBevel', samples=8); bv.inputs['Radius'].default_value = radius
    return bv.outputs['Normal']

def mat_metal(name, base, rough=0.32, rough_var=0.12, brushed=True, wear=0.8,
              wear_color=None, cavity='#0E0C0A', cavity_amt=0.55, scratch=0.25,
              bevel_r=0.0012, aniso=0.0, brush_axis='Z'):
    """Layered metal: brushed roughness breakup + convex edge wear (brighter,
    smoother) + cavity dirt (darker, rougher) + micro-scratches + micro-bevel."""
    mb = MB(name); p = mb.p
    set_in(p, IN["metal"], 1.0)
    base_c = hex_lin(base); wear_c = hex_lin(wear_color) if wear_color else tuple(min(1, c*1.35) for c in base_c[:3])+(1,)
    edge = _edge_mask(mb); cav = _cavity_mask(mb)
    # streaks run ALONG brush_axis: compress the other two axes' features
    st = {'X': (1, 30, 30), 'Y': (30, 1, 30), 'Z': (30, 30, 1)}[brush_axis]
    nz = _noise(mb, 60 if brushed else 40, stretch=st if brushed else None)
    sc = _noise(mb, 900, detail=2, rough=0.9, stretch=(1, 30, 1))
    sc_m = mb.ramp(sc, [(0.62, 0.0), (0.66, 1.0)])
    col = mb.mix_col(mb.math('MULTIPLY', edge, wear), base_c, wear_c)
    col = mb.mix_col(mb.math('MULTIPLY', cav, cavity_amt), col, hex_lin(cavity))
    mb.link(col, get_in(p, IN["base"]))
    r = mb.math('ADD', rough - rough_var/2, mb.math('MULTIPLY', nz, rough_var))
    r = mb.mix_f(mb.math('MULTIPLY', edge, wear*0.7), r, max(0.05, rough*0.45))
    r = mb.mix_f(mb.math('MULTIPLY', cav, cavity_amt), r, min(1, rough+0.35))
    r = mb.mix_f(mb.math('MULTIPLY', sc_m, scratch), r, min(1, rough+0.18))
    mb.link(r, get_in(p, IN["rough"]))
    if aniso: set_in(p, IN["aniso"], aniso)
    nrm = _bump(mb, mb.math('MULTIPLY', sc_m, 0.5), strength=0.18, distance=0.0006,
                extra_normal=_micro_bevel(mb, bevel_r))
    mb.link(nrm, get_in(p, IN["normal"]))
    return mb

def mat_leather(name, base, rough=0.62, grain=900, wear=0.35, cavity_amt=0.5, edge=0.0025):
    """Leather: pore grain, burnished (lighter, smoother) edges, darker cavities.
    edge = burnish-mask distance ~15% of the part's thickness/radius (lessons
    #9): 2.5 mm suits a 16 mm grip; a 3 mm strap wants ~0.5 mm, or the whole
    strap reads as burnished edge (pink)."""
    mb = MB(name); p = mb.p
    set_in(p, IN["metal"], 0.0); set_in(p, IN["spec"], 0.35)
    vo = mb.n('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = grain
    tc = mb.n('ShaderNodeTexCoord'); mb.link(tc.outputs['Object'], vo.inputs['Vector'])
    pores = mb.ramp(vo.outputs['Distance'], [(0.0, 0.0), (0.35, 1.0)])
    edge = _edge_mask(mb, edge); cav = _cavity_mask(mb, 0.008)
    c = hex_lin(base); light = tuple(min(1, x*1.25) for x in c[:3])+(1,)
    dark = tuple(x*0.45 for x in c[:3])+(1,)
    col = mb.mix_col(mb.math('MULTIPLY', edge, wear), c, light)   # burnished edges
    col = mb.mix_col(mb.math('MULTIPLY', cav, cavity_amt), col, dark)
    mb.link(col, get_in(p, IN["base"]))
    r = mb.mix_f(mb.math('MULTIPLY', edge, wear), rough, rough*0.55)
    mb.link(r, get_in(p, IN["rough"]))
    mb.link(_bump(mb, pores, 0.35, 0.0006, _micro_bevel(mb, 0.0015)), get_in(p, IN["normal"]))
    set_in(p, IN["sheen"], 0.06)
    return mb

def mat_cloth(name, base, sheen=0.6, rough=0.85, weave=1400):
    mb = MB(name); p = mb.p
    set_in(p, IN["base"], hex_lin(base)); set_in(p, IN["rough"], rough)
    set_in(p, IN["sheen"], sheen); set_in(p, IN["sheen_rough"], 0.35)
    w = mb.n('ShaderNodeTexWave', wave_type='BANDS'); w.inputs['Scale'].default_value = weave
    tc = mb.n('ShaderNodeTexCoord'); mb.link(tc.outputs['Object'], w.inputs['Vector'])
    mb.link(_bump(mb, w.outputs['Fac'], 0.25, 0.0004), get_in(p, IN["normal"]))
    return mb

def mat_stone(name, base='#3A3834', rough=0.78, scale=6):
    mb = MB(name); p = mb.p
    n1 = _noise(mb, scale, detail=10, rough=0.62)
    vo = mb.n('ShaderNodeTexVoronoi', feature='F1'); vo.inputs['Scale'].default_value = scale*3
    tc = mb.n('ShaderNodeTexCoord'); mb.link(tc.outputs['Object'], vo.inputs['Vector'])
    c = hex_lin(base); dark = tuple(x*0.55 for x in c[:3])+(1,); lite = tuple(min(1, x*1.3) for x in c[:3])+(1,)
    mb.link(mb.mix_col(n1, dark, lite), get_in(p, IN["base"]))
    mb.link(mb.math('ADD', rough-0.08, mb.math('MULTIPLY', n1, 0.16)), get_in(p, IN["rough"]))
    h = mb.math('ADD', n1, mb.math('MULTIPLY', vo.outputs['Distance'], 0.6))
    mb.link(_bump(mb, h, 0.5, 0.004, _micro_bevel(mb, 0.004)), get_in(p, IN["normal"]))
    return mb

def mat_gem(name, color, emit_strength=6.0, heart='#FFF3C4', density=40):
    """Faceted gem: transmissive body + volume absorption for depth + an
    emissive heart that genuinely lights its surroundings in Cycles."""
    mb = MB(name); p = mb.p
    c = hex_lin(color)
    set_in(p, IN["base"], c); set_in(p, IN["trans"], 1.0); set_in(p, IN["rough"], 0.02)
    set_in(p, IN["ior"], 1.62)
    # emissive heart from facing-ratio: centre of each view-facing facet glows
    lw = mb.n('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.45
    heart_m = mb.ramp(lw.outputs['Facing'], [(0.0, 1.0), (0.55, 0.15), (1.0, 0.0)])
    mb.link(mb.mix_col(heart_m, c, hex_lin(heart)), get_in(p, IN["emit_col"]))
    mb.link(mb.math('MULTIPLY', heart_m, emit_strength), get_in(p, IN["emit_str"]))
    va = mb.n('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = c
    va.inputs['Density'].default_value = density
    mb.link(va.outputs[0], mb.out.inputs['Volume'])
    return mb

# ─────────────────────────────── rarity glow tiers ──────────────────────────
TIERS = {
    # The ladder: common/rare/epic/legendary = Castle Conquest's Issued/Sound/
    # Fine/Masterwork; mythic kept for the library. Strengths are calibrated
    # under AgX by render strip (art/forge/calibration/tier_sheet.png) — above
    # ~5 a saturated body colour paths to white. rim_gain scales the rig's rim
    # light; embers=False keeps the glow CONTAINED (no particles).
    # Calibrated 2026-09-26 on Blender 5.2 (768 px strips, bloom 0.40 @ 0.0625):
    # blue/violet/red body colours carry ~half the luminance of gold per unit
    # strength, so the cool tiers need more strength to read at 128 px; cores
    # of the contained tiers stay SATURATED (a near-white core reads as light,
    # not as sapphire/violet). Mythic above ~6 paths to pink-white under AgX.
    "common":    dict(core='#F2F2F2', body='#BFC3CA', haze='#2A2C30', strength=0.0, breathe=0.0,
                      rim='#D9DDE3', rim_gain=0.45, embers=False),
    "rare":      dict(core='#BCD0FF', body='#4F7FD6', haze='#16243F', strength=2.6, breathe=0.03,
                      rim='#6A8FD8', rim_gain=1.0, embers=False),
    "epic":      dict(core='#DEC4FF', body='#8F6ADB', haze='#2E2150', strength=4.0, breathe=0.05,
                      rim='#8F6ADB', rim_gain=1.0, embers=False),
    "legendary": dict(core='#FFF3C4', body='#E8A33C', haze='#4A2F10', strength=7.5, breathe=0.35,
                      rim='#E8A33C', rim_gain=1.0, embers=True),
    "mythic":    dict(core='#FFCFC4', body='#D6303F', haze='#3D0F16', strength=6.0, breathe=0.55,
                      rim='#D6303F', rim_gain=1.0, embers=True),
}

def _glow_ramp_colours(T):
    # stops at 0, .18, .50, .90, 1: black -> haze -> body (held) -> core
    return [(0, 0, 0, 1), hex_lin(T['haze']), hex_lin(T['body']), hex_lin(T['body']), hex_lin(T['core'])]

def add_glow(mb, mask, tier, hot_gradient=None, seed=0.0):
    """Wire a 3-layer emission into an existing material.
    mask: float socket 0..1 marking channels (1 = deepest cut).
    hot_gradient: optional float socket 0..1 boosting the 'hottest point'.
    Core/body/haze ramp + breathing noise; strength scaled per tier.
    The tier-dependent nodes carry 'forge:glow_*' labels so retier() can
    re-colour the finished asset in place."""
    T = TIERS[tier]
    colr = mb.n('ShaderNodeValToRGB'); mb._feed(mask, colr.inputs[0])
    colr.label = "forge:glow_ramp"
    el = colr.color_ramp.elements
    el[0].position = 0.0; el[1].position = 1.0
    for pos in (0.18, 0.50, 0.90):             # body holds until the deepest cut
        el.new(pos)
    for e, c in zip(el, _glow_ramp_colours(T)):
        e.color = c
    br = _noise(mb, 3.0, detail=2, rough=0.4)
    wob = mb.math('MULTIPLY', br, T['breathe']*2); wob.node.label = "forge:glow_breathe_mul"
    breathe = mb.math('ADD', 1.0 - T['breathe'], wob); breathe.node.label = "forge:glow_breathe_add"
    s = mb.math('MULTIPLY', mb.math('POWER', mask, 1.6), T['strength'])
    s.node.label = "forge:glow_strength"
    s = mb.math('MULTIPLY', s, breathe)
    if hot_gradient is not None:
        s = mb.math('MULTIPLY', s, mb.math('ADD', 1.0, mb.math('MULTIPLY', hot_gradient, 0.9)))
    mb.link(colr.outputs[0], get_in(mb.p, IN["emit_col"]))
    mb.link(s, get_in(mb.p, IN["emit_str"]))
    mb.mat["forge_tier"] = tier
    return mb

def ember(name, loc, tier, size=0.0025, stretch=4.0):
    """A floating ember: tiny emissive sphere stretched upward (fake motion blur).
    Hidden from render on tiers whose glow is contained (TIERS[t]['embers'])."""
    T = TIERS[tier]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=size, location=loc)
    o = bpy.context.object; o.name = name; o.scale = (1, 1, stretch)
    m = bpy.data.materials.new(name+"M"); m.use_nodes = True
    nt = m.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hex_lin(T['body'])
    em.inputs['Strength'].default_value = T['strength']*2.2
    em.label = "forge:ember"
    nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    o.data.materials.append(m); o.visible_shadow = False
    o["forge_ember"] = True
    return o

def retier(tier, objects=None, rig=None):
    """Re-tier a finished asset IN PLACE — the rarity-sheet rule: identical
    geometry, camera and rig; only glow colours/strength, embers and the rim
    light change. Rewires every add_glow() layer and ember() on `objects`
    (default: the whole scene); `rig` is studio_rig()'s dict. Returns the
    number of glow layers rewired (0 means the asset has no add_glow)."""
    T = TIERS[tier]
    objects = list(bpy.context.scene.objects) if objects is None else list(objects)
    mats = {sl.material for o in objects for sl in o.material_slots if sl.material}
    layers = 0
    for m in mats:
        if not m.node_tree:
            continue
        tagged = False
        for nd in m.node_tree.nodes:
            lab = nd.label
            if lab == "forge:glow_ramp":
                els = sorted(nd.color_ramp.elements, key=lambda e: e.position)
                for e, c in zip(els, _glow_ramp_colours(T)):
                    e.color = c
                layers += 1; tagged = True
            elif lab == "forge:glow_strength":
                nd.inputs[1].default_value = T['strength']
            elif lab == "forge:glow_breathe_mul":
                nd.inputs[1].default_value = T['breathe'] * 2
            elif lab == "forge:glow_breathe_add":
                nd.inputs[0].default_value = 1.0 - T['breathe']
            elif lab == "forge:ember":
                nd.inputs['Color'].default_value = hex_lin(T['body'])
                nd.inputs['Strength'].default_value = T['strength'] * 2.2
        if tagged:
            m["forge_tier"] = tier
    for o in objects:
        if o.get("forge_ember"):
            o.hide_render = not T.get('embers', False)
    if rig and rig.get('rim') is not None:
        rim = rig['rim']
        rim.data.color = hex_lin(T['rim'])[:3]
        rim.data.energy = rim.get("forge_rim_energy", rim.data.energy) * T.get('rim_gain', 1.0)
    return layers

# ─────────────────────────────── bake + export ──────────────────────────────
def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    for o in objs: apply_mods(o) if o.modifiers else None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); j = bpy.context.object; j.name = name
    return j

def uv_unwrap(ob, angle=66, margin=0.004):
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=margin)
    bpy.ops.object.mode_set(mode='OBJECT')

def _proxy_to_emission(mat, canon):
    """Route a Principled input into an Emission output so it can be baked
    exactly (fixes the classic 'metal base colour bakes black' trap)."""
    nt = mat.node_tree; p = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    em = nt.nodes.new('ShaderNodeEmission'); em.name = "__bake_proxy__"
    em.inputs['Strength'].default_value = 1.0
    if p is None:
        em.inputs['Color'].default_value = (0, 0, 0, 1)
    else:
        sock = get_in(p, IN[canon])
        if sock.is_linked:
            src = sock.links[0].from_socket
            nt.links.new(src, em.inputs['Color'])
        else:
            dv = sock.default_value
            em.inputs['Color'].default_value = tuple(dv) if hasattr(dv, '__len__') else (dv, dv, dv, 1)
    old = out.inputs['Surface'].links[0].from_socket if out.inputs['Surface'].is_linked else None
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    return (nt, em, out, old)

def _restore(state):
    nt, em, out, old = state
    if old is not None: nt.links.new(old, out.inputs['Surface'])
    nt.nodes.remove(em)

def make_bake_target(sources, name, decimate=None):
    """Duplicate sources, apply their modifiers, join the copies into one game
    mesh. The originals stay untouched as the high-detail bake SOURCES."""
    copies = []
    for o in sources:
        c = o.copy(); c.data = o.data.copy(); bpy.context.collection.objects.link(c)
        copies.append(c); apply_mods(c)
    bpy.ops.object.select_all(action='DESELECT')
    for c in copies: c.select_set(True)
    bpy.context.view_layer.objects.active = copies[0]
    bpy.ops.object.join(); t = bpy.context.object; t.name = name
    t.data.materials.clear()
    if decimate and decimate < 1.0:   # in-world LOD: detail survives in the baked normal map
        d = t.modifiers.new("Decimate", 'DECIMATE'); d.decimate_type = 'COLLAPSE'
        d.ratio = decimate; d.use_collapse_triangulate = True
        apply_mods(t)
    bm = bmesh.new(); bm.from_mesh(t.data)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-7)
    bm.to_mesh(t.data); bm.free()
    # Joined parts may carry partial UVs (curve conversions add them): faces
    # from UV-less parts collapse to a point and bake NOTHING. Always re-unwrap.
    while t.data.uv_layers: t.data.uv_layers.remove(t.data.uv_layers[0])
    uv_unwrap(t)
    return t

def _pixels(im):
    """(N, 4) float32 copy of an image's pixels (raw bytes/255 for byte images)."""
    a = np.empty(im.size[0] * im.size[1] * 4, np.float32)
    im.pixels.foreach_get(a)
    return a.reshape(-1, 4)

def bake_pbr(target, sources=None, size=2048, out_dir="/tmp/bake", margin=16,
             samples=16, extrusion=0.0015, ray_dist=0.006, device='CPU'):
    """Bake to ONE game texture set: albedo, metallic, roughness, normal
    (tangent), emission — the only material kind glTF/Godot can read.
    With `sources`, bakes selected-to-active: each original part's shading
    (object-space masks, AO wear, bevel-node normals) transfers exactly onto
    the joined target. Metal base colour is baked via an emission proxy —
    a plain DIFFUSE bake returns black for metals.
    Emission is measured in a RAW float buffer (Non-Color: no colourspace
    transform on any Blender version), normalised by its linear peak (the one
    strength factor -> KHR_materials_emissive_strength), and written as an
    8-bit PNG with EXPLICIT sRGB encoding. Blender 5.x bakes into a float image
    in that image's declared colourspace: the old 'sRGB' float buffer read the
    OETF of the peak (3.054 for a true 13.383) — lessons #18.
    device: 'CPU' (default) | 'GPU'. Measured on the real Sunforged 1024 bake
    (5.2.1, 20 cores vs RTX 3500 Ada OptiX): CPU 51 s, GPU 105 s, maps identical
    — selected-to-active bakes are CPU-bound; GPU is for renders.
    Returns material, emission_strength, emission_peak, files, channels
    (min/max/mean per map — inspect them; a black map is a FAIL, qa.md)."""
    os.makedirs(out_dir, exist_ok=True)
    s = bpy.context.scene; s.render.engine = 'CYCLES'; s.cycles.samples = samples
    s.cycles.use_denoising = False
    if device == 'GPU' and gpu_setup() == 'CPU':
        device = 'CPU'
    s.cycles.device = device
    s.render.bake.margin = margin
    if not target.data.uv_layers or uv_zero_area_faces(target) > 0.02 * len(target.data.polygons):
        while target.data.uv_layers: target.data.uv_layers.remove(target.data.uv_layers[0])
        uv_unwrap(target)
    imgs = {}
    for key, cs in (("albedo", 'sRGB'), ("metallic", 'Non-Color'), ("roughness", 'Non-Color'),
                    ("normal", 'Non-Color')):
        im = bpy.data.images.new(f"{target.name}_{key}", size, size)
        im.colorspace_settings.name = cs; imgs[key] = im
    raw = bpy.data.images.new(f"{target.name}_emission_raw", size, size, float_buffer=True)
    raw.colorspace_settings.name = 'Non-Color'    # raw scene-linear radiance, never encoded
    if sources:
        src_mats = list({sl.material for o in sources for sl in o.material_slots if sl.material})
        holder = MB(target.name + "_BakeHolder").mat
        target.data.materials.clear(); target.data.materials.append(holder)
        tgt_mats = [holder]
    else:
        src_mats = tgt_mats = [sl.material for sl in target.material_slots if sl.material]
    def activate(im):
        for m in tgt_mats:
            nt = m.node_tree
            tn = nt.nodes.get("__bake_target__") or nt.nodes.new('ShaderNodeTexImage')
            tn.name = "__bake_target__"; tn.image = im; nt.nodes.active = tn; tn.select = True
    def run(bake_type, **kw):
        bpy.ops.object.select_all(action='DESELECT')
        if sources:
            for o in sources: o.select_set(True)
        target.select_set(True); bpy.context.view_layer.objects.active = target
        if sources:
            kw.update(use_selected_to_active=True, cage_extrusion=extrusion, max_ray_distance=ray_dist)
        bpy.ops.object.bake(type=bake_type, use_clear=True, **kw)
    for key, canon in (("albedo", "base"), ("metallic", "metal"), ("roughness", "rough")):
        states = [_proxy_to_emission(m, canon) for m in src_mats]
        activate(imgs[key]); run('EMIT')
        for st in states: _restore(st)
    activate(imgs["normal"]); run('NORMAL', normal_space='TANGENT')
    activate(raw); run('EMIT')
    px = _pixels(raw)
    peak = float(px[:, :3].max()) if px.size else 0.0
    strength = max(1.0, peak)
    em = bpy.data.images.new(f"{target.name}_emission", size, size)   # 8-bit
    em.colorspace_settings.name = 'sRGB'
    enc = np.ones_like(px)
    enc[:, :3] = srgb_encode(px[:, :3] / strength)
    em.pixels.foreach_set(enc.astype(np.float32).ravel())
    imgs["emission"] = em
    bpy.data.images.remove(raw)
    channels = {}
    for key, im in imgs.items():
        im.filepath_raw = os.path.join(out_dir, f"{target.name}_{key}.png"); im.file_format = 'PNG'
        im.save()
        a = _pixels(im)[:, :3]
        channels[key] = (round(float(a.min()), 3), round(float(a.max()), 3), round(float(a.mean()), 4))
    for m in tgt_mats:
        tn = m.node_tree.nodes.get("__bake_target__")
        if tn: m.node_tree.nodes.remove(tn)
    mb = MB(target.name + "_Baked"); p = mb.p
    def tex(key):
        t = mb.n('ShaderNodeTexImage'); t.image = imgs[key]; return t
    mb.link(tex("albedo").outputs['Color'], get_in(p, IN["base"]))
    mb.link(tex("metallic").outputs['Color'], get_in(p, IN["metal"]))
    mb.link(tex("roughness").outputs['Color'], get_in(p, IN["rough"]))
    nm = mb.n('ShaderNodeNormalMap'); mb.link(tex("normal").outputs['Color'], nm.inputs['Color'])
    mb.link(nm.outputs['Normal'], get_in(p, IN["normal"]))
    mb.link(tex("emission").outputs['Color'], get_in(p, IN["emit_col"]))
    set_in(p, IN["emit_str"], strength)
    target.data.materials.clear(); target.data.materials.append(mb.mat)
    return dict(material=mb.mat.name, emission_strength=round(strength, 3),
                emission_peak=round(peak, 4), device=device, channels=channels,
                files={k: im.filepath_raw for k, im in imgs.items()})

def export_glb(objs, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_apply=True,
                              export_format='GLB', export_yup=True)
    return path

# ─────────────────────────────── quality gates ──────────────────────────────
def uv_zero_area_faces(ob):
    """Faces whose UV area is ~0 bake no pixels — the silent-black-map trap.
    (A join on 5.x can leave uv_layers with NO active layer: use the first.)"""
    me = ob.data
    if not me.uv_layers: return len(me.polygons)
    uv = (me.uv_layers.active or me.uv_layers[0]).data; bad = 0
    for p in me.polygons:
        pts = [uv[li].uv for li in p.loop_indices]; a = 0.0
        for i in range(len(pts)):
            x1, y1 = pts[i]; x2, y2 = pts[(i+1) % len(pts)]; a += x1*y2 - x2*y1
        if abs(a) < 1e-12: bad += 1
    return bad

def quality_report(ob, tri_budget=None):
    """Automated checks a pro runs before anything ships."""
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = ev.to_mesh(); bm = bmesh.new(); bm.from_mesh(me)
    tris = sum(len(f.verts) - 2 for f in bm.faces)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    boundary = sum(1 for e in bm.edges if e.is_boundary)
    loose = sum(1 for v in bm.verts if not v.link_edges)
    degenerate = sum(1 for f in bm.faces if f.calc_area() < 1e-10)
    dims = tuple(round(d, 4) for d in ob.dimensions)
    rep = dict(object=ob.name, triangles=tris, non_manifold_edges=non_manifold, open_boundary_edges=boundary,
               uv_zero_area_faces=(uv_zero_area_faces(ob) if ob.data.uv_layers
                                   else "n/a (no UVs yet; re-unwrapped at bake)"),
               loose_verts=loose, degenerate_faces=degenerate, dimensions_m=dims,
               uv_layers=len(ob.data.uv_layers), materials=len(ob.material_slots))
    if tri_budget: rep["within_budget"] = tris <= tri_budget
    bm.free(); ev.to_mesh_clear()
    return rep

def render(path):
    s = bpy.context.scene; s.render.filepath = path
    s.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    return path
