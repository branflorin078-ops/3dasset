# Lessons — real mistakes from the Sunforged Greatsword build

Every item here happened. Each cost a full render iteration. Check them BEFORE
the first render.

1. **Stacked primitives read as toys.** The first commander figure (boxes and
   cylinders) was rejected on sight. Fix: design cross-sections and loft them;
   revolve profiles; sweep curves. See forms.md.

2. **Edge-on hero shot.** A sword turned 38° about Z presented its thin edge to
   the camera — the flat, the fuller, and the glow all vanished. Rule: the
   decorated face must face the camera, turned 20–35° for three-quarter. Compute
   the face normal against the view vector before rendering (dot > 0.8).

3. **Asset too small in frame.** A vertical 1.4 m sword in a portrait frame is
   a thin line. Item cards are square; weapons go diagonal (pommel lower-left,
   point upper-right) at 45–55° and fill 75% of the frame.

4. **Glow clipped to white.** Under AgX, saturated emission above ~5 paths to
   white — the three layers collapse into one white line. Tier strengths in
   `TIERS` are calibrated; do not raise them to "make it pop."

5. **Pale glow on pale metal = invisible.** The fix was never more emission —
   it was a DARKER SUBSTRATE (blade base #7E7466 instead of #C9B596). Light
   needs darkness to read. This is the single most important glow lesson.

6. **Ornament at the wrong scale.** Sunburst rays at 3–5 cm on a 1.4 m sword
   read as glitch spikes. Tertiary detail must survive the card resolution:
   test at 256 px. Scale ornaments up ~1.6x from what looks right in isolation.

7. **Overexposed gems and embers read as UI dots.** Gems: emission ≤ 1.5,
   saturated body colour, dense volume absorption. Embers: body colour, not
   core colour; graded sizes; few of them.

8. **Floor spill.** A low rim light painted an orange blob on the floor. For
   floating item cards, drop the floor; use `backdrop_radial`.

9. **Burnish masks on small cylinders.** AO-inside edge masks with a large
   distance classify a whole thin grip as "edge" → pink leather. Scale mask
   distance to the part: ~15% of the part's radius.

10. **Metal albedo bakes black.** A DIFFUSE bake of a metallic material returns
    black. `bake_pbr` routes each channel through an emission proxy instead.

11. **Object-space masks break when parts are joined.** Glow masks built in each
    part's local space shift after a join. Bake SELECTED-TO-ACTIVE from the
    untouched originals onto a joined copy (`make_bake_target`).

12. **Pivot in the wrong place.** The first export left the origin at the
    guard. A weapon attaches to a hand bone — pivot at the grip centre. Move the
    origin only AFTER the bake (moving the target before baking misaligns it
    with its sources).

13. **Assume one CPU core until checked.** Run `nproc` first. On a single core
    never run renders/bakes in parallel — chain them in one background script
    and poll the logs.

14. **Inherited partial UVs bake a black map — silently.** Curve-converted parts
    (wire wraps) arrive WITH a UV layer; lofted/lathed parts arrive without.
    After a join the mesh "has UVs", unwrapping is skipped, and every UV-less
    face collapses to a point in UV space. Zero-area UV faces bake no pixels: the
    emission map came out pure black while albedo LOOKED fine (the wire colour +
    bake margin flooded the texture). Fix: `make_bake_target` deletes all UV
    layers and re-unwraps; `bake_pbr` refuses UVs with >2% zero-area faces;
    `quality_report` reports `uv_zero_area_faces`. Never trust a bake you have
    not inspected channel by channel.

15. **Micro-caps and open rings fail QA.** A loft ending in a 0.15 mm ring,
    then bevelled at 0.6 mm, produces degenerate faces; lathe profiles that do
    not start/end at radius 0 leave open ring edges (512 non-manifold edges on
    the first joined export). Fix: `loft(..., tip=point)` fans to a true vertex;
    `lathe(cap=True)` closes open ends; `make_bake_target` dissolves degenerates.

16. **Debug a pipeline by bisection, on the real data, at tiny resolution.**
    Every stage tested fine in isolation; only calling the real function on the
    real scene at 128 px reproduced the fault in seconds. And disable denoising
    in any bake test — without a denoiser, Cycles discards the bake result and
    a correct pipeline looks broken.

17. **Tight framing reads as a crop.** margin=1.04 left the pommel touching the
    card's edge in the 1600 px final. Default to 1.08 for diagonal weapons;
    check all four frame edges in the critique, not just the subject.

## Blender 5.x port (2026-09-26, Blender 5.2.1 LTS, Windows, RTX 3500 Ada)

18. **5.x bakes into a float image IN THAT IMAGE'S COLOURSPACE.** The
    Sunforged baked `emission_strength` 3.054 on 5.2 where 4.0 gave 13.383.
    Bisected on the real data: every glow node was unchanged (noise Fac
    0.33–0.57, each Map Range 0..1, POWER max 1, ColorRamp R max 1, strength
    socket max 13.36); sample count irrelevant (1/8/32 samples: 13.383/13.381/
    13.381). The cause was `bake_pbr`'s float buffer declared 'sRGB': 5.x
    writes the sRGB OETF of the radiance into it — OETF(13.383) = 3.0542
    exactly (a plane of known strength 13.383 read 3.0542 as 'sRGB', 13.3830
    as 'Linear Rec.709' or 'Non-Color'). Worse, `Image.save()` of a float
    image writes a 16-bit PNG in the declared space, so mid-tones were wrong
    too. Fix: measure emission in a 'Non-Color' float buffer, normalise by the
    linear peak, write an 8-bit PNG with EXPLICIT sRGB encoding (numpy) —
    version-proof. Real Sunforged now 13.381 (round trip 13.381). Any GLB
    baked on 5.x before the fix must be re-exported.

19. **`scene.node_tree` is gone in 5.0.** The compositor is a node group:
    `bpy.data.node_groups.new(.., 'CompositorNodeTree')`, an `Image` output
    socket on its interface, a `NodeGroupOutput` node, assigned to
    `scene.compositing_node_group` (set it to None to detach — a later
    `render_setup(bloom=False)` used to leave the bloom attached). 4.x keeps
    `scene.use_nodes` + `CompositorNodeComposite`.

20. **Glare settings are input sockets on 4.5+** (Type / Quality are MENU
    sockets set by name — 'Bloom', 'High'; Threshold, Strength, Size...).
    Size is RELATIVE to the frame and Strength is ADDITIVE (4.0's Mix −0.55
    was 1.124·image + 0.326·glare). The documented mapping 2^(size−9) put
    size 7 at 0.25 of the frame: a third of the lift landed 24–96 px from the
    highlights (mid/near 0.35) — a warm veil. Calibrated by render strip:
    Size 0.0625, Strength 0.40 keeps the near halo (0.0755 vs 0.0767 mean
    lift within 24 px) with 4.3x less veil and zero far-field lift.

21. **Every forge script takes `<mode> <outdir>` positionally.** `run_chain.sh`
    passed one argument; `verify_glb.py` reads the out-dir from the second,
    fell back to its default folder, and the "round-trip proof" did not look
    at the GLB just exported. Pass both, and read the `IMPORT {'glb': ...}`
    line: it names the file that was verified.

22. **User add-ons load into `--background` jobs unless `--factory-startup`.**
    The MCP bridge and the human-generator add-ons started inside production
    renders (non-determinism, slower start). `forge_run` always passes
    `--factory-startup`, and `--python-exit-code 1` — without it a script
    that raises still exits 0 and a chain runs on past the crash.

23. **`reset_scene()` wipes the Cycles device preferences.** A cached
    'OPTIX' then asked for a GPU the preferences no longer enabled — the
    render silently ran on CPU. `gpu_setup()` now re-applies the backend.
    And GPU is for renders, not bakes: the Sunforged 1024 five-map
    selected-to-active bake took 51 s on 20 CPU cores vs 105 s on OptiX,
    maps identical — `bake_pbr` defaults to `device='CPU'`.

24. **The denoiser probe needs a camera.** `render_setup()` called before
    the camera existed made the 8 px probe fail ("no camera"), which was
    cached as "no denoiser" for the whole process: denoising off, 2.5x
    samples. The probe now brings its own camera — still create the camera
    before `render_setup`.

25. **"Emission > 1" is not a test.** 3.054 passed it while the real value
    was 13.383. Gate on the analytic value: a known strength S must bake to
    S (±2%), and the PNG's mid-tones must decode back to S/2
    (`tests/test_bake.py`).

26. **`matrix_world` is STALE after editing `.location` / `.rotation_euler`**
    until `bpy.context.view_layer.update()`. `boolean_cut` computed the
    cutters' boxes at the origin, so its clean-up missed the cuts: 98
    degenerate faces. Update before reading `matrix_world` or world-space
    `bound_box` of anything you just moved.

27. **Never boolean an object made of overlapping closed shells as one.** A
    sallet with its rolled rim (two intersecting shells) came out of EXACT
    inside-out (volume UP 39%, 20 non-manifold edges, blades sticking out of
    the face); `use_self=True` was worse (95 non-manifold, 200 degenerate,
    5–10x slower); MANIFOLD failed too. `boolean_cut` separates loose parts,
    cuts only the shells the cutter touches, and rejoins. Then weld ~0.1 mm
    LOCALLY: the cut leaves 20–100 µm edges that a 0.5 mm bevel turns into
    micro-quads (8 degenerate faces at a 25 µm weld, 0 at 100 µm).

28. **`frame_camera` only pushes back.** It starts from need = 0, so a small
    asset under a far camera stays small — the probe finial filled 51% of the
    frame height. `frame_fill(cam, objs, 0.78)` moves in OR out.

29. **Tier colours are not equally bright.** Per unit emission strength, the
    blue/violet/red bodies carry ~0.21 luminance against gold's 0.44, so the
    cool tiers need MORE strength to read at 128 px (rare 2.6, epic 4.0 vs
    legendary 7.5), and their cores must stay saturated — a near-white core
    reads as light, not as sapphire. Mythic above ~6 paths to pink-white
    under AgX. Calibrate by strip + `tools/rarity_sheet.py --thumb 128`.

30. **A join can leave UV layers with NO active layer (5.x).**
    `uv_layers.active` returned None and `quality_report` crashed on a lathe
    joined with a curve sweep. The gate now reads the first layer — and
    reports the partial UVs (92 zero-area faces in the test), which is the
    lessons #14 trap made visible before any bake.

31. **A wide still life in a square frame is a third empty.** The armour kit
    (sallet + fauld side by side, belt and gems in front) lies ~1.5:1;
    `frame_fill` fills the LIMITING direction only, so the square card came
    out 76% full across and ~50% down, with the lower third black, and the
    73-facet brilliant was an unreadable blue dot. Match the frame to the
    arrangement (3:2 here), and aim at the centre of the parts' PROJECTED
    silhouette (mesh vertices), not a hand-picked point
    (`aim_at_silhouette` in `examples/armour_kit.py`; re-aim once after
    `frame_fill`, since the dolly shifts the parallax). Same geometry, same
    QA numbers: the facets, sights and lame rivets all read.
