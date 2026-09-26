"""figure_kit.py - commander-forge helpers for HUMAN FIGURES, on top of blender-forge.

It never sculpts a face and never builds a body. It imports a licensed base
(references/figure-lane.md section 1), shades skin / cornea / hair, fits kit to
the body, lights and frames the figure, and writes the mask + metadata that
tools/figure_check.py measures. Runs inside a blender-forge job only:

    py <skills>/blender-forge/tools/forge_run.py run <build.py> <mode> <outdir>

and in build.py:

    import sys, os
    sys.path.insert(0, os.environ.get("FORGE_LIB") or "<skills>/blender-forge/lib")
    sys.path.insert(0, "<skills>/commander-forge/tools")
    import forge as F, figure_kit as FK

Blender 4.0 - 5.x (Principled v2 sockets; tested on 4.0.2 by
examples/figure_probe.py). Anything here that a second skill needs is proposed
to blender-forge's skill-engineer (TEAM.md library change protocol); never
paste it into forge.py by hand.
"""
import json
import math
import os

import bpy
import bmesh
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

import forge as F

GILT_LIT = '#E0BC6A'      # the SWORN rim (palette token GILT, lit)
NEUTRAL_RIM = '#D9DDE3'   # unsworn rim (forge TIERS common rim)
TORCH = '#FFD9A8'         # house key light: warm torchlight, upper left
COOL_FILL = '#C9D4E6'     # forge studio fill
KICK = '#9FB0C8'          # cool kicker that separates the shadow side


# ---------------------------------------------------------------- base import
def import_base(path):
    """Import a licensed human base (.blend / .fbx / .obj / .glb / .gltf).
    Returns the new objects; prints QA_BASE (meshes, triangles, height, armature)."""
    ext = os.path.splitext(path)[1].lower()
    before = set(bpy.data.objects)
    if ext == '.blend':
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.objects = list(src.objects)
        for o in dst.objects:
            if o is not None:
                bpy.context.collection.objects.link(o)
    elif ext == '.fbx':
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == '.obj':
        if hasattr(bpy.ops.wm, 'obj_import'):
            bpy.ops.wm.obj_import(filepath=path)
        else:
            bpy.ops.import_scene.obj(filepath=path)
    elif ext in ('.glb', '.gltf'):
        bpy.ops.import_scene.gltf(filepath=path)
    else:
        raise ValueError("import_base: unsupported file type %r" % ext)
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == 'MESH']
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in meshes)
    height = F.bounds(meshes)[1].z if meshes else 0.0
    print("QA_BASE", dict(file=os.path.basename(path), meshes=len(meshes), triangles=tris,
                          height_m=round(height, 3),
                          armature=any(o.type == 'ARMATURE' for o in new)))
    return new


def vgroup_points(ob, group, min_weight=0.5):
    """World positions of the vertices in a vertex group (e.g. a head group)."""
    gi = ob.vertex_groups[group].index
    mw = ob.matrix_world
    return [mw @ v.co for v in ob.data.vertices
            for g in v.groups if g.group == gi and g.weight >= min_weight]


# ---------------------------------------------------------------- materials
def mat_skin(name, base='#C8967A', albedo=None, rough=(0.38, 0.52), rough_scale=40.0,
             rough_map=None, sss_weight=1.0, radius=(1.0, 0.37, 0.19), scale=0.004,
             sss_ior=1.4, spec=0.5, mottle=0.06, pores=1800.0, pore_depth=0.12,
             normal_map=None):
    """Layered skin for Cycles renders (key-art, cards, look-dev).
    - Random-walk SKIN subsurface. radius is the per-channel scatter ratio
      (red travels furthest), scale is metres: 0.004 = 4 mm for a real-size
      head. Above ~0.008 skin turns to candle wax; below ~0.002 it is plastic.
    - roughness broken up between rough[0] (oily T-zone) and rough[1] (cheeks);
      a rough_map (Non-Color, 0 = oily) drives the zones when the source has one.
    - mottle: low-frequency redness/value variation (0.04-0.08); 0 = vinyl toy.
    - pores: object-space voronoi bump (1800 per metre = cells ~0.55 mm);
      a sculpt/scan normal_map, when given, is chained under it.
    Returns the forge MB builder (mb.mat is the material)."""
    mb = F.MB(name)
    p = mb.p
    try:
        p.subsurface_method = 'RANDOM_WALK_SKIN'
    except TypeError:
        p.subsurface_method = 'RANDOM_WALK'
    # base colour: texture from the licensed source, else the hex + mottling
    if albedo:
        tx = mb.n('ShaderNodeTexImage')
        tx.image = bpy.data.images.load(albedo, check_existing=True)
        col = tx.outputs['Color']
    else:
        c = F.hex_lin(base)
        red = (min(1.0, c[0] * 1.08), c[1] * 0.90, c[2] * 0.88, 1.0)
        dark = (c[0] * 0.86, c[1] * 0.84, c[2] * 0.84, 1.0)
        blot = F._noise(mb, 8.0, detail=3, rough=0.5)
        m1 = mb.map_range(blot, 0.40, 0.62, 0.0, mottle * 6.0)
        col = mb.mix_col(m1, c, red)
        fine = F._noise(mb, 60.0, detail=2, rough=0.6)
        col = mb.mix_col(mb.map_range(fine, 0.45, 0.60, 0.0, mottle * 3.0), col, dark)
    F.set_in(p, F.IN["base"], (1, 1, 1, 1))
    mb.link(col, F.get_in(p, F.IN["base"]))
    # subsurface (Principled v2: weight, radius, scale in metres, IOR)
    F.set_in(p, F.IN["sss"], sss_weight)
    F.set_in(p, F.IN["sss_rad"], tuple(radius))
    F.set_in(p, ["Subsurface Scale"], scale)
    F.set_in(p, ["Subsurface IOR"], sss_ior)
    F.set_in(p, F.IN["ior"], 1.4)
    F.set_in(p, F.IN["spec"], spec)
    # roughness breakup
    nz = F._noise(mb, rough_scale, detail=4, rough=0.55)
    if rough_map:
        rt = mb.n('ShaderNodeTexImage')
        rt.image = bpy.data.images.load(rough_map, check_existing=True)
        rt.image.colorspace_settings.name = 'Non-Color'
        zone = rt.outputs['Color']
        r = mb.math('ADD', mb.map_range(zone, 0.0, 1.0, rough[0], rough[1], smooth=False),
                    mb.map_range(nz, 0.3, 0.7, -0.03, 0.03, smooth=False))
    else:
        r = mb.map_range(nz, 0.30, 0.70, rough[0], rough[1])
    mb.link(r, F.get_in(p, F.IN["rough"]))
    # pores (+ optional sculpt/scan normal map underneath)
    extra = None
    if normal_map:
        nt = mb.n('ShaderNodeTexImage')
        nt.image = bpy.data.images.load(normal_map, check_existing=True)
        nt.image.colorspace_settings.name = 'Non-Color'
        nmap = mb.n('ShaderNodeNormalMap')
        mb.link(nt.outputs['Color'], nmap.inputs['Color'])
        extra = nmap.outputs['Normal']
    vo = mb.n('ShaderNodeTexVoronoi')
    vo.inputs['Scale'].default_value = pores
    tc = mb.n('ShaderNodeTexCoord')
    mb.link(tc.outputs['Object'], vo.inputs['Vector'])
    pits = mb.ramp(vo.outputs['Distance'], [(0.0, 0.0), (0.30, 1.0)])
    mb.link(F._bump(mb, pits, pore_depth, 0.0002, extra), F.get_in(p, F.IN["normal"]))
    mb.mat["figure_mat"] = "skin"
    return mb


def mat_cornea(name, ior=1.376):
    """Clear wet cornea over a painted/scanned iris: the catchlight lives here.
    A cornea with roughness above ~0.05 kills the catchlight (dead eyes)."""
    mb = F.MB(name)
    p = mb.p
    F.set_in(p, F.IN["base"], (1, 1, 1, 1))
    F.set_in(p, F.IN["trans"], 1.0)
    F.set_in(p, F.IN["rough"], 0.02)
    F.set_in(p, F.IN["ior"], ior)
    mb.mat["figure_mat"] = "cornea"
    return mb


def mat_hair_strands(name, melanin=0.80, redness=0.30, rough=0.30, radial=0.35,
                     coat=0.08, random_color=0.12, random_rough=0.10):
    """Principled Hair (Chiang) for CURVE hair in Cycles renders only.
    melanin: 0.05 white/blond ... 0.35 light brown ... 0.8 dark brown ... 1.0 black.
    Game hair is cards (mat_hair_cards): curve hair never reaches the GLB."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    h = nt.nodes.new('ShaderNodeBsdfHairPrincipled')
    try:
        h.parametrization = 'MELANIN'
    except TypeError:
        pass
    vals = {"Melanin": melanin, "Melanin Redness": redness, "Roughness": rough,
            "Radial Roughness": radial, "Coat": coat, "Random Color": random_color,
            "Random Roughness": random_rough}
    for k, v in vals.items():
        if k in h.inputs:
            h.inputs[k].default_value = v
    nt.links.new(h.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    mat["figure_mat"] = "hair_strands"
    return mat


def mat_hair_cards(name, albedo, alpha=None, rough=(0.35, 0.50), aniso=0.6, uv="UVMap"):
    """Alpha-card hair (the only hair that reaches Godot). albedo: RGBA strand
    atlas (alpha in its A channel, or a separate `alpha` image). Anisotropic
    highlight along the card's V direction (strands run along V)."""
    mb = F.MB(name)
    p = mb.p
    tx = mb.n('ShaderNodeTexImage')
    tx.image = bpy.data.images.load(albedo, check_existing=True)
    mb.link(tx.outputs['Color'], F.get_in(p, F.IN["base"]))
    if alpha:
        ta = mb.n('ShaderNodeTexImage')
        ta.image = bpy.data.images.load(alpha, check_existing=True)
        ta.image.colorspace_settings.name = 'Non-Color'
        a_out = ta.outputs['Color']
    else:
        a_out = tx.outputs['Alpha']
    mb.link(a_out, F.get_in(p, ["Alpha"]))
    nz = F._noise(mb, 90.0, detail=2, rough=0.5, coord='UV')
    mb.link(mb.map_range(nz, 0.3, 0.7, rough[0], rough[1]), F.get_in(p, F.IN["rough"]))
    F.set_in(p, F.IN["aniso"], aniso)
    tg = mb.n('ShaderNodeTangent', direction_type='UV_MAP')
    tg.uv_map = uv
    mb.link(tg.outputs['Tangent'], F.get_in(p, ["Tangent"]))
    try:
        mb.mat.blend_method = 'HASHED'      # EEVEE / viewport only; Cycles reads Alpha
    except (AttributeError, TypeError):
        pass
    mb.mat["figure_mat"] = "hair_cards"
    return mb


# ---------------------------------------------------------------- kit fitting
def _loops(bm_edges):
    """Group cut edges into connected loops of ordered 2D points."""
    adj = {}
    for e in bm_edges:
        a, b = e.verts
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for start in adj:
        if start in seen:
            continue
        loop, prev, cur = [], None, start
        while cur is not None and cur not in seen:
            seen.add(cur)
            loop.append((cur.co.x, cur.co.y))
            nxt = [v for v in adj[cur] if v is not prev and v not in seen]
            prev, cur = cur, (nxt[0] if nxt else None)
        if len(loop) >= 3:
            loops.append(loop)
    return loops


def _area(loop):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(loop, loop[1:] + loop[:1])))


def body_section(ob, z):
    """The largest closed cross-section of a mesh at world height z - the torso,
    not an arm or a hand hanging beside it. Returns (loop [(x, y)], centroid)."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    ev.to_mesh_clear()
    bm.transform(ob.matrix_world)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                                 dist=1e-6, plane_co=(0, 0, z), plane_no=(0, 0, 1))
    cut = [g for g in res['geom_cut'] if isinstance(g, bmesh.types.BMEdge)]
    loops = _loops(cut)
    bm.free()
    if not loops:
        raise ValueError("body_section: no section of %s at z=%.3f" % (ob.name, z))
    loop = max(loops, key=_area)
    cx = sum(p[0] for p in loop) / len(loop)
    cy = sum(p[1] for p in loop) / len(loop)
    return loop, (cx, cy)


def _ray_radius(loop, c, ang):
    """Largest distance from c along direction ang at which the ray meets the loop."""
    dx, dy = math.cos(ang), math.sin(ang)
    best = 0.0
    for (x0, y0), (x1, y1) in zip(loop, loop[1:] + loop[:1]):
        ex, ey = x1 - x0, y1 - y0
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((x0 - c[0]) * ey - (y0 - c[1]) * ex) / den
        u = ((x0 - c[0]) * dy - (y0 - c[1]) * dx) / den
        if t > 0 and 0.0 <= u <= 1.0:
            best = max(best, t)
    return best


def body_profile(ob, heights, offset=0.02, arc=(185.0, 355.0), n=25):
    """A clearance-safe plate profile around a body: for n angles across `arc`
    (degrees; 180 = -X, 270 = -Y front, 360 = +X), the LARGEST body radius
    over every sampled height, plus `offset` (padding + clearance, metres).
    Front arcs (180-360) run left -> right, back arcs (0-180) right -> left,
    so the outer face lands on the side forge.plate() expects.
    Returns (profile [(x, y)], centroid) in world XY."""
    secs = [body_section(ob, z) for z in heights]
    c = (sum(s[1][0] for s in secs) / len(secs), sum(s[1][1] for s in secs) / len(secs))
    prof = []
    for i in range(n):
        a = math.radians(arc[0] + (arc[1] - arc[0]) * i / (n - 1))
        r = max(_ray_radius(loop, c, a) for loop, _ in secs) + offset
        prof.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    return prof, c


def plate_on_body(body, name, z_bottom, height, offset=0.02, arc=(185.0, 355.0), n=25,
                  samples=3, **plate_kw):
    """forge.plate() fitted to a body: profile sampled at `samples` heights
    between z_bottom and z_bottom + height (max radius wins), then the plate
    is raised to z_bottom. Offsets (figure-lane.md): mail 0.004-0.006,
    plate over mail 0.010-0.015, plate over a gambeson 0.020-0.030."""
    hs = [z_bottom + height * (0.15 + 0.7 * k / max(1, samples - 1)) for k in range(samples)]
    prof, _ = body_profile(body, hs, offset=offset, arc=arc, n=n)
    ob = F.plate(name, prof, height, **plate_kw)
    ob.location.z = z_bottom
    bpy.context.view_layer.update()
    return ob


def clearance(kit, body, samples=400):
    """Minimum distance (metres) from kit vertices to the body surface, sampled.
    Negative = a kit vertex sits INSIDE the body (clipping). Prints QA_FIT."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    bev = body.evaluated_get(dg)
    mw = bev.matrix_world
    inv = mw.inverted()
    nmat = inv.transposed().to_3x3()
    verts = kit.data.vertices
    step = max(1, len(verts) // samples)
    worst = 1e9
    for v in list(verts)[::step]:
        wp = kit.matrix_world @ v.co
        ok, loc, nrm, _ = bev.closest_point_on_mesh(inv @ wp)
        if not ok:
            continue
        d = wp - mw @ loc                       # world space: scale-safe
        dist = d.length if d.dot(nmat @ nrm) >= 0 else -d.length
        worst = min(worst, dist)
    print("QA_FIT", dict(kit=kit.name, body=body.name, min_clearance_mm=round(worst * 1000, 2)))
    return worst


# ---------------------------------------------------------------- light + camera
def hero_rig(target, dist=2.0, key=150.0, fill_ratio=0.18, yaw=0.0, sworn=False, eye_light=True,
             kicker=True):
    """The hall/portrait rig, CAMERA-RELATIVE (pass the camera's yaw): warm torch
    key upper-left (the house light), cool fill camera-right at fill_ratio of key
    (0.18 = 5.5:1, ~2.5 stops), a rim behind-right that carries the SWORN state
    (gilt 2.2x key) or not (neutral 0.6x key), a cool kicker behind-left, a faint
    top light, and a small eye light beside the lens for catchlights.
    Figure faces -Y at yaw 0. Energies are watts at dist=2.0 m; they scale with
    dist^2. Defaults calibrated with figure_check on examples/figure_probe.py."""
    t = Vector(target)
    s = dist / 2.0
    k = key * s * s
    R = Matrix.Rotation(math.radians(yaw), 3, 'Z')

    def at(x, y, z):
        return t + R @ (Vector((x, y, z)) * s)
    rig = dict(
        key=F.area_light("FigKey", at(-1.25, -1.35, 1.05), t, k, 1.0 * s, color=TORCH),
        fill=F.area_light("FigFill", at(1.6, -1.0, -0.1), t, k * fill_ratio, 2.0 * s, color=COOL_FILL),
        rim=F.area_light("FigRim", at(1.15, 1.3, 0.55), t, k, 0.3 * s, color=NEUTRAL_RIM, size_y=1.6 * s),
        top=F.area_light("FigTop", at(0.0, 0.35, 1.6), t, k * 0.12, 0.8 * s),
    )
    if kicker:
        rig["kicker"] = F.area_light("FigKick", at(-1.1, 1.2, 0.3), t, k * 0.25, 0.4 * s, color=KICK,
                                     size_y=1.2 * s)
    if eye_light:
        rig["eye"] = F.area_light("FigEye", at(0.05, -2.0, 0.18), t, k * 0.03, 0.3 * s, color=TORCH)
    rig["rim"]["figure_rim_base"] = k
    set_sworn(rig, sworn)
    return rig


RIM_GAIN = {False: 0.6, True: 2.2}     # rim energy / key energy (unsworn, sworn)


def set_sworn(rig, on):
    """SWORN = gilt rim at RIM_GAIN[True] x key; unsworn = neutral rim at
    RIM_GAIN[False] x key. The rim is the sworn channel ONLY - rarity never
    uses it on a lord (references/design.md, channel table)."""
    rim = rig["rim"]
    base = rim.get("figure_rim_base", rim.data.energy)
    rim.data.color = F.hex_lin(GILT_LIT if on else NEUTRAL_RIM)[:3]
    rim.data.energy = base * RIM_GAIN[bool(on)]
    return rim


def bust_camera(eye, head_h=0.24, fill=0.45, lens=85.0, fstop=4.0, yaw=0.0, res=(1024, 1280)):
    """Head-and-shoulders camera: the head (crown to chin, head_h metres) fills
    `fill` of the frame height, the eyes sit on the upper-third line (level
    camera aimed H/6 below the eyes), 85 mm, focus on the eyes. yaw (degrees)
    swings the camera around the figure: + = camera to the figure's left (+X),
    so the figure faces slightly LEFT on screen (the house portrait direction).
    Build hero_rig with the same yaw.
    Pass the SAME res to forge.render_setup (it sets the resolution again)."""
    scn = bpy.context.scene
    scn.render.resolution_x, scn.render.resolution_y = res
    e = Vector(eye)
    frame_h = head_h / fill
    fov_v = 2 * math.atan(18.0 / lens) if res[1] >= res[0] else 2 * math.atan(18.0 / lens * res[1] / res[0])
    d = (frame_h / 2) / math.tan(fov_v / 2)
    aim = e - Vector((0, 0, frame_h / 6))
    a = math.radians(yaw)
    loc = aim + Vector((math.sin(a) * d, -math.cos(a) * d, 0.0))
    cam = F.camera(aim, loc, lens=lens, dof_fstop=fstop, name="BustCam")
    cam.data.sensor_fit = 'AUTO'
    cam.data.dof.focus_distance = (e - loc).length
    print("QA_CAMERA", dict(distance_m=round(d, 3), frame_h_m=round(frame_h, 3), lens=lens, fstop=fstop))
    return cam


# ---------------------------------------------------------------- outputs for figure_check
def _is_bg(o):
    return o.get("figure_bg") or o.name.startswith(("Backdrop", "Floor"))


def render_with_mask(path, mask_samples=4):
    """Render `path`, then a silhouette mask `<stem>_mask.png` (transparent
    film, backdrop and floor hidden) for tools/figure_check.py."""
    F.render(path)
    scn = bpy.context.scene
    keep = (scn.render.film_transparent, scn.cycles.samples, scn.cycles.use_denoising)
    hidden = [o for o in scn.objects if _is_bg(o) and not o.hide_render]
    for o in hidden:
        o.hide_render = True
    scn.render.film_transparent = True
    scn.cycles.samples = mask_samples
    scn.cycles.use_denoising = False
    fmt = scn.render.image_settings.color_mode
    scn.render.image_settings.color_mode = 'RGBA'
    stem = os.path.splitext(path)[0]
    F.render(stem + "_mask.png")
    scn.render.image_settings.color_mode = fmt
    scn.render.film_transparent, scn.cycles.samples, scn.cycles.use_denoising = keep
    for o in hidden:
        o.hide_render = False
    return stem + "_mask.png"


def write_meta(path, cam, face_pts=None, kind="bust", sworn=False, extra=None):
    """<stem>_meta.json beside a render: the projected face box (image
    fractions, y down) from world points (e.g. a FaceBox's corners or a head
    vertex group), the render kind and the sworn state. figure_check reads it."""
    scn = bpy.context.scene
    meta = dict(kind=kind, sworn=bool(sworn), res=[scn.render.resolution_x, scn.render.resolution_y])
    if face_pts:
        uv = [world_to_camera_view(scn, cam, Vector(p)) for p in face_pts]
        xs = [max(0.0, min(1.0, q.x)) for q in uv]
        ys = [max(0.0, min(1.0, 1.0 - q.y)) for q in uv]
        meta["face"] = [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]
    if extra:
        meta.update(extra)
    out = os.path.splitext(path)[0] + "_meta.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
    return out


def box_corners(ob):
    """World-space corners of an object's bounding box (e.g. an empty FaceBox cube)."""
    bpy.context.view_layer.update()
    return [ob.matrix_world @ Vector(c) for c in ob.bound_box]
