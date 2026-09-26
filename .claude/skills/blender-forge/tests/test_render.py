"""render_setup on this Blender: compositor bloom, GPU device, denoiser probe."""
import os
import bpy
import forge as F
from _util import check, outdir


def _glare_node():
    s = bpy.context.scene
    tree = getattr(s, "compositing_node_group", None) or getattr(s, "node_tree", None)
    check(tree is not None, "no compositor tree after render_setup(bloom=True)")
    gl = [n for n in tree.nodes if n.bl_idname == 'CompositorNodeGlare']
    check(len(gl) == 1, "expected one Glare node, found %d" % len(gl))
    return gl[0]


def test_render_setup_compositor():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
    F.world_dark()
    cam = F.camera((0, 0, 0), (0, -1.5, 0.2), lens=50)
    F.render_setup(res=(32, 32), samples=2, bloom=True)
    gl = _glare_node()
    if 'Type' in gl.inputs:                                   # 4.5+ / 5.x: sockets
        check(gl.inputs['Type'].default_value in ('Bloom', 'Fog Glow'),
              "glare type %r" % gl.inputs['Type'].default_value)
        check(abs(gl.inputs['Size'].default_value - F.BLOOM_SIZE_AT_7) < 1e-6,
              "glare_size=7 must map to the calibrated %.4f, got %.4f" % (
                  F.BLOOM_SIZE_AT_7, gl.inputs['Size'].default_value))
        check(abs(gl.inputs['Strength'].default_value - F.BLOOM_STRENGTH) < 1e-6, "bloom strength")
        info = "Type=%s Size=%.4f Strength=%.2f Threshold=%.2f" % (
            gl.inputs['Type'].default_value, gl.inputs['Size'].default_value,
            gl.inputs['Strength'].default_value, gl.inputs['Threshold'].default_value)
    else:                                                     # 4.0-4.4: properties
        check(gl.glare_type in ('BLOOM', 'FOG_GLOW'), "glare type %r" % gl.glare_type)
        info = "glare_type=%s size=%d mix=%.2f" % (gl.glare_type, gl.size, gl.mix)
    path = F.render(os.path.join(outdir("render"), "bloom32.png"))
    check(os.path.isfile(path), "render not written")
    return info


def _active_glare():
    s = bpy.context.scene
    if hasattr(s, "compositing_node_group"):
        tree = s.compositing_node_group
    else:
        tree = s.node_tree if s.use_nodes else None
    return tree is not None and any(n.bl_idname == 'CompositorNodeGlare' for n in tree.nodes)


def test_render_setup_no_bloom():
    F.render_setup(res=(16, 16), samples=1, bloom=False)
    check(not _active_glare(), "bloom=False still built a Glare node")
    F.render_setup(res=(16, 16), samples=1, bloom=True)
    check(_active_glare(), "bloom=True built no Glare node")
    F.render_setup(res=(16, 16), samples=1, bloom=False)
    check(not _active_glare(), "bloom=False after bloom=True left the bloom compositor attached")


def test_render_setup_bloom_overrides():
    F.render_setup(res=(16, 16), samples=1, bloom=True, bloom_strength=0.25, bloom_size=0.125)
    gl = _glare_node()
    if 'Type' in gl.inputs:
        check(abs(gl.inputs['Strength'].default_value - 0.25) < 1e-6, "bloom_strength ignored")
        check(abs(gl.inputs['Size'].default_value - 0.125) < 1e-6, "bloom_size ignored")
        return "4.5+ sockets"
    return "4.0-4.4 properties (overrides n/a)"


def test_frame_fill_both_ways():
    """frame_camera only ever pushes back (need starts at 0) — a small asset
    under a far camera stays small (lessons #3). frame_fill pulls in too."""
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    bpy.ops.mesh.primitive_cube_add(size=0.2); cube = bpy.context.object
    s = bpy.context.scene
    for start, sign in (((0, -6.0, 0.0), -1), ((0, -0.25, 0.0), 1)):   # too far, then too close
        cam = F.camera((0, 0, 0), start, lens=50, name="Cam%d" % sign)
        F.render_setup(res=(512, 512), samples=1, bloom=False)
        d = F.frame_fill(cam, [cube], fill=0.8)
        check((d < 0) if sign < 0 else (d > 0), "camera moved the wrong way (%.3f)" % d)
        pts = [world_to_camera_view(s, cam, cube.matrix_world @ Vector(c)) for c in cube.bound_box]
        ext = max(max(abs(p.x - 0.5), abs(p.y - 0.5)) for p in pts)
        check(abs(ext - 0.4) < 0.01, "fill %.3f of the half-frame, expected 0.40" % ext)
        bpy.data.objects.remove(cam, do_unlink=True)
    return "fills 0.80 from both sides"


def test_denoise_probe_independent_of_camera():
    """The probe renders 8 px; with no camera yet it used to fail, cache False
    for the whole process, and silently switch off denoising (2.5x samples)."""
    F._DENOISE_OK = None
    no_cam = F.denoise_available()
    F._DENOISE_OK = None
    F.camera((0, 0, 0), (0, -1, 0))
    with_cam = F.denoise_available()
    check(no_cam == with_cam, "denoise probe: %s without a camera, %s with one" % (no_cam, with_cam))
    check(not any(o.type == 'CAMERA' for o in bpy.context.scene.objects if o.name.startswith("__forge")),
          "probe left a temporary camera behind")
    return "denoiser=%s" % with_cam


def test_gpu_setup_survives_reset():
    """reset_scene() (read_factory_settings) wipes the Cycles device preferences;
    a cached backend name must not leave render_setup asking for a GPU that the
    preferences no longer enable (silent CPU fallback)."""
    backend = F.gpu_setup()
    F.reset_scene()
    F.render_setup(res=(16, 16), samples=1, bloom=False)
    s = bpy.context.scene
    if backend == 'CPU':
        check(s.cycles.device == 'CPU', "no GPU backend but device=%s" % s.cycles.device)
        return "CPU only"
    prefs = bpy.context.preferences.addons['cycles'].preferences
    check(prefs.compute_device_type == backend,
          "after reset_scene prefs.compute_device_type=%s, cached backend %s" % (prefs.compute_device_type, backend))
    check(any(d.use and d.type == backend for d in prefs.devices), "no %s device enabled after reset" % backend)
    check(s.cycles.device == 'GPU', "scene device %s" % s.cycles.device)
    return backend
