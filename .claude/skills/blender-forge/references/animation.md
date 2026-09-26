# Animation — prop motion, clips and rigging scope

blender-forge animates OBJECTS, not people. Characters, gaits and faces belong
to the `hero3d` skill's rig; this file covers what a crafted object does in the
game: a chest lid opening, a gate raising, a banner stirring, a trebuchet arm
throwing, a rarity glow breathing.

## First question: does this motion belong in Blender at all?

| Motion | Where it lives | Why |
|---|---|---|
| Rarity glow "breathing", flicker | **Godot** — tween `emission_energy` | engine-side is free, per-instance, tier-aware (export.md) |
| Spin, bob, hover on a reward card | **Godot** — `Tween` / `AnimationPlayer` on the node | no GLB change, tunable live |
| Hinged parts: chest lid, gate, drawbridge, shutters, visor | **Blender clip** in the GLB | pivots and arcs must match the geometry |
| Mechanisms: trebuchet, ballista, mangonel, windmill, waterwheel, crane | **Blender clip**, simple armature or object hierarchy | multi-part timing is authored once |
| Cloth: banner, pennon, awning | **Blender clip** (baked shape keys, loop) or Godot vertex shader for map-scale flags | a shader is cheaper for 100 flags on the map |
| Particles: smoke, sparks, embers in-game | **Godot** `GPUParticles3D` / `CPUParticles3D` | never baked into a GLB |

If Godot can do it with a tween, do not author a clip.

## Rig scope (hard-surface only)

- **Object hierarchy first.** A chest is `Base` + `Lid` parented, lid origin ON
  the hinge axis. Object-level transforms export as glTF node animation with no
  skinning cost. Use it for ≤ 8 moving parts.
- **Armature only when parts deform or exceed ~8 rigid parts** (a trebuchet
  with a sling, a banner). Rigid parts get 100% weight to one bone (no blending).
- **Pivots are design, not afterthought.** Put every moving part's origin on its
  real hinge/axle before animating — a lid rotating about its centre is the #1
  prop animation tell. Hinge pins, axles and pintles are MODELLED (forms.md
  `lathe` pins, `sweep` straps) so the pivot is visibly justified.
- **Bake-then-animate order**: the game mesh is ONE joined mesh (export.md). For
  animated props, keep each moving part as its own mesh+material slot sharing
  ONE texture set: `make_bake_target` per rigid group, bake into a shared atlas
  (`bake_pbr` per group, same `size`, UV-packed), then parent. Draw calls =
  moving groups, not source parts.

## Clip rules

1. **Name clips by verb, snake case, no object prefix**: `open`, `close`,
   `idle`, `fire`, `reload`, `raise`, `lower`, `loop`. Godot's `AnimationPlayer`
   lists them by these names; gameplay code calls them by name.
2. **Rest pose = frame 0 = the closed / idle state** the static GLB shows.
3. **30 fps**, whole-frame keys. Short: UI reveal 12–18 frames (0.4–0.6 s),
   mechanism cycle 45–90 frames.
4. **Anticipation → action → overshoot → settle.** A chest lid: 3 frames of
   creep (lock releasing), 9 frames fast swing, 3 frames 6° overshoot past
   rest-open, 4 frames settle. Linear keys read as mechanical — use Bézier with
   ease-out on the action, and one overshoot on anything with mass.
5. **Loops are seamless**: first and last key identical, cyclic F-curve
   modifier, and checked by rendering frames 0 and N side by side.
6. **Heavy things are slow, light things snap.** A portcullis rises over
   60–90 frames with a 4-frame hesitation per chain link section; a shutter
   pops in 6.
7. **Mechanisms tell cause and effect.** A trebuchet: counterweight drops →
   arm rotates → sling whips (lags the arm by 3–4 frames) → release at arm
   ~45° past vertical. If the order is wrong players feel it even if they
   cannot say why.

## Export

- `bpy.ops.export_scene.gltf(..., export_animations=True,
  export_animation_mode='ACTIONS', export_force_sampling=True,
  export_frame_range=False)` — one glTF animation per action.
- Remove unused actions before export (`bpy.data.actions` with 0 users);
  stray actions ship as dead clips.
- Round trip: re-import and print every animation's name and frame range
  (`IMPORT anims=[('open', 0, 19), …]`) beside the usual `QA_GAME` line.
- Godot: the GLB imports with an `AnimationPlayer`; set loop mode on `loop`/
  `idle` clips in the import dock (Advanced Import → Animation → Loop).

## QA for animated props (add to the 12-point visual list)

- A. Every pivot sits on a modelled hinge/axle (render a 4-frame strip).
- B. No interpenetration at any keyed frame (lid through base, arm through frame).
- C. Clip names and ranges printed by the round trip match this file's rules.
- D. The mechanism reads with sound off: cause precedes effect.
- E. Loops: frame 0 ≡ frame N (pixel diff of the two renders ≈ 0).
