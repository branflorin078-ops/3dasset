# Zoom model — one camera, four levels, one continuous space

The genre's reference title zooms from the city to the whole world with a
pinch and no loading screen, and its team reviewed that zoom frame by frame
(research §6). Players read it as "one living place" (research §11: close =
detailed city, mid = marches and troop icons, far = city icons with alliance
tags [observational]). The pattern: **one camera, one world, content that
changes by distance, never a scene cut.** Our version adds four things the
genre does not do well: a log-space zoom that feels the same at every
height, a painted cloud veil that hides the one big content swap, the realm
level drawn as the lord's painted war-map (PROPOSAL to world-forge), and a
rule that the camera only dives into places that are fully built (your own
castle, or a battle you chose to watch).

Map rules (what exists on the realm, fog, camps, territory) are
design-forge [world.md](../../design-forge/references/world.md) and
world-forge's. This file owns HOW the camera moves through them and WHEN each
layer appears.

## 1. The rig — roll is not a degree of freedom

```
CameraRig (Node3D)        position = focus point on the ground (y = 0 plane)
└─ Yaw (Node3D)           rotation.y = house yaw + yaw_offset (authored shots only)
   └─ Pitch (Node3D)      rotation.x = -pitch (pitch from the curve, §5)
      └─ Camera3D         position = Vector3(0, 0, distance); looks down -Z
```

- State is five numbers: `focus: Vector3`, `yaw_offset_deg`, `pitch_offset_deg`,
  `distance: float`, `fov` (fixed, §2). Every shot writes these, never the
  Camera3D transform. Slerping two camera transforms can introduce roll; tweening
  yaw, pitch and distance separately cannot.
- **House yaw** is fixed (castle-forge's value, path to confirm): the camera sees
  the lit south-east faces (blender-forge architecture.md §1). Authored shots may
  offset yaw by at most ±15° and must return it to 0 before handing the camera
  back to the player.
- Update the rig in `_process`, never `_physics_process`: phones run 90/120 Hz
  displays while physics ticks at 60 Hz; a camera moved in physics judders.
- One owner: the autoload `CameraDirector` (path to confirm) owns the rig. Input,
  shots, onboarding and battle-forge all go through it
  ([shot-library.md](shot-library.md) §1). `Camera3D.h_offset` / `v_offset` are
  reserved for battle-forge's shake and stay 0 in every transition.

## 2. The lens — one lens for the whole realm

| Property | Value | Why |
|---|---|---|
| `Camera3D.projection` | `PROJECTION_PERSPECTIVE` | depth cues and a real "dive"; orthographic cannot fake the height change |
| `Camera3D.keep_aspect` | `KEEP_WIDTH` | portrait: the width is fixed across the 6 aspect shapes, taller phones see more ground |
| `Camera3D.fov` | **30° horizontal**, constant in gameplay | long lens, near-orthographic painted read (architecture.md §1) |
| `near` / `far` | `near = 0.02 × distance`, `far = distance × sin(p) / sin(p − vfov/2) × 1.15` | keeps depth precision at 44 m and at 22 km; recomputed every frame |
| FOV changes | only in authored shots, ≤ 4°, ≤ 8°/s, never while distance moves the opposite way | distance down + FOV up is a dolly-zoom: the ground warps |

**Horizon rule: the sky never enters the frame.** The top edge of the screen
must look ≥ 10° below the horizon: `pitch − vfov/2 ≥ 10°`, with
`vfov = 2·atan(tan(15°) × height/width)`.

| Shape (portrait) | vfov | Minimum pitch |
|---|---|---|
| 4:3 tablet | 39.3° | 29.7° |
| 16:9 | 50.9° | 35.5° |
| 19.5:9 | 60.3° | 40.1° |
| 20:9 | 61.5° | 40.8° |
| 21:9 | 64.0° | 42.0° |

So the gameplay floor is **pitch 45°** and authored shots may go to **42°**,
never lower (the `w1f_aspect_sweep` shapes to confirm; recompute this table if
a taller shape is added). Far plane: at pitch 45° on 21:9 the top-edge ray is
3.15 × distance long, at 60° it is 1.85 × — the formula above covers both.

## 3. Distance lives in log space

- Normalised zoom `z = log2(d / d_min) / log2(d_max / d_min)`; every
  interpolation of distance is `d(t) = d0 · (d1 / d0)^e(t)` with `e` a named
  curve ([easing.md](easing.md)). Linear interpolation of metres is banned: it
  crawls at the start of a zoom-out and rushes at the end of a zoom-in.
- **Pinch is 1:1 and anchored.** Fingers moving apart by ratio `s` divide the
  distance by `s`; the ground point under the pinch centroid stays under the
  centroid (move the focus by `hit_before − hit_after`, both from
  `Camera3D.project_ray_origin/normal` on the ground plane). Player-driven
  motion has no comfort cap: the hand predicts it.
- **Pan** is 1:1 with the finger on the ground plane (the ray hit under the
  finger stays under the finger). Touch slop before a pan starts: 8 dp
  (Android's default), so taps on buildings survive.
- **Inertia (PROPOSAL, tune with `ux_touch_probe`)**: pan velocity from the last
  80 ms of samples (≥ 3 samples), decay `v·e^(−t/0.30 s)`, stop below
  0.02 screen widths/s. Zoom inertia in log space, τ = 0.15 s, initial rate
  capped at 6 doublings/s. A touch-down stops inertia on the same frame.
- **Rubber band** at `d_min`, `d_max` and every floor (§8): overscroll up to
  0.11 doublings (8% distance) with resistance `x / (1 + 3x)`; on release,
  spring back in 240 ms (14 f) `CUBIC_OUT`.

## 4. The four levels — defined by pixels, not metres

Levels are defined by how big things PROJECT, so they hold when castle-forge
changes building heights or world.md changes the realm size. Reference width
1080 px; `w(d) = 2·d·tan(15°) = 0.5359·d` is the ground width at the focus.

| Level | Defined by (at 1080 px wide) | Job |
|---|---|---|
| **C1 castle close** | ordinary building projects 150–320 px tall | inspect a building: construction, tier trims, villagers (ART SHOWN BIG) |
| **C2 castle overview** | building 54–150 px; rest at 90 px | the working view: bubbles, queues, taps on buildings |
| **R region** | own town 48–897 px wide (below the B2 swap) | marches, camps, neighbours, scouting |
| **M realm** | own town < 48 px (it becomes an icon) | territory, landmarks, the whole realm |

Distance for a projected size: building `d = 1080·H_b·cos(p) / (0.5359·px)`;
town `d = 1080·W_town / (0.5359·px)`. `H_b` = median ordinary building height,
`W_town` = town footprint width (castle-forge, to confirm), realm width `R_w`
(world.md). These match blender-forge architecture.md §2's three read
distances (close 180–320 px, overview 60–120 px, realm 48–96 px).

**Worked example — PROPOSAL values `H_b` = 10 m, `W_town` = 100 m, `R_w` = 12 km:**

| Anchor | Defined by | Distance | Pitch | Ground width | Building px | Town px |
|---|---|---|---|---|---|---|
| `d_min` | building 320 px | 44.5 m | 45° | 24 m | 320 | 4,526 |
| B1 (C1 ↔ C2) | building 150 px | 91.6 m | 47° | 49 m | 150 | 2,199 |
| C2 rest | building 90 px | 144 m | 50° | 77 m | 90 | 1,400 |
| B2 (C2 ↔ R) | building 54 px | 225 m | 53° | 120 m | 54 | 897 |
| R_near (button target) | town 144 px | 1,400 m | 60° | 750 m | 7 | 144 |
| B3 (R ↔ M) | town 48 px | 4,199 m | 66° | 2,250 m | 2 | 48 |
| M rest = `d_max` | realm fits the width | 22.4 km | 70° | 12 km | — | 9 |

**Hysteresis.** Each boundary B switches up at `B × 2^0.15` (+11%) and down
at `B / 2^0.15` (−10%): B1 at 101.7 / 82.6 m, B2 at 249.2 / 202.4 m, B3 at
4,659 / 3,784 m. A level also needs **≥ 250 ms dwell** before the same boundary
may switch back, so a shaky pinch on the band edge cannot flicker the HUD.
`CameraDirector` emits `level_changed(old, new)` once per commit; HUD mode,
layers and audio listen to that signal, never to raw distance.

## 5. Pitch follows distance

Pitch is a function of distance, sampled from a `Curve` resource
(`pitch_curve.sample_baked(z)`), anchored at the table above: 45° at `d_min`,
47° at B1, 50° at C2 rest, 53° at B2, 60° at R_near, 66° at B3, 70° at `d_max`.

- **Slope limit: ≤ 6° per doubling of distance** anywhere on the curve
  (measured: 1.9 / 4.6 / 4.7 / 2.7 / 3.8 / 1.7 °/doubling between anchors).
  Steeper and a zoom reads as a tilt.
- Never 90°: straight down flattens the painted buildings into roofs only and
  makes yaw undefined. Never above 72°.
- Authored shots add a `pitch_offset` of at most ±6° that decays to 0 over
  ≥ 600 ms `SINE_IO` when the shot ends.

## 6. What appears and disappears

Two mechanisms, never mixed for one layer:
- **Semantic layers** (HUD, bubbles, labels, lines, tint, fog, audio) switch on
  `level_changed` — the whole layer at once, with a timed fade.
- **Geometry** (building LODs, town → cluster, forests) swaps by
  `visibility_range_*` per node, with HLOD (`visibility_parent`) where a whole
  group must swap together ([streaming.md](streaming.md) §3).

| Layer | C1 | C2 | R | M | Switch | Fade in / out |
|---|---|---|---|---|---|---|
| Own buildings LOD0 (full detail) | ● | — | — | — | HLOD range B1 | margin = hysteresis |
| Own buildings LOD1 | — | ● | — | — | HLOD range B1–B2 | veil hides B2 |
| Own town as LOD2 cluster | — | — | ● | — | HLOD parent, begin B2 | veil hides B2 |
| Own castle icon (fixed 56 px) | — | — | — | ● | level M | 200 / 150 ms |
| Villagers (feel-forge life, ≤ 40) | ● | ● until building < 75 px | — | — | distance, own group | 300 / 200 ms dither |
| Status bubbles (ui-forge) | ● | ● | — | — | level | 150 / 120 ms |
| Building name label | on focus only | on focus only | — | — | tap | 120 / 120 ms |
| Construction scaffold, smoke, flags | ● | ● | — | — | HLOD with LOD0/1 | — |
| Own marches | column at the gate, real size | column at the gate, real size | one realm token, size follows distance | chevron + line | level (collapse under the veil) | 200 / 150 ms |
| Other marches (tokens) | — | — | ● | chevrons + lines | level | 200 / 150 ms |
| March lines (relationship colours) | — | — | ● | ● (self, ally, incoming only) | level | 200 / 150 ms |
| Neighbour castles | — | cluster form if in view | cluster form | icon + tag | level + range | 200 / 150 ms |
| Camps, resource sites | — | — | model | icon (my level ±2) | level | 200 / 150 ms |
| Terrain | castle patch (high) | castle patch | realm chunks (mid) | war-map (PROPOSAL §7) | range + dissolve | distance-driven |
| Forests | MultiMesh LOD0 | LOD0 | LOD1 chunks | in the war-map | range per 128 m cell | margin |
| Fog of war | — | — | ● | ● | level | 250 / 250 ms |
| Territory tint | — | — | borders only | ● | level | 250 / 250 ms |
| HUD mode (ui-forge) | castle | castle | realm | realm | level at B2 only | 150 ms crossfade |
| Shadows | ● | ● | fade to 0 across the B2 band | — | distance | continuous |
| Audio bed (audio-forge) | town | town | field wind | war-room | distance | continuous |

Rules behind the table: only the own castle and a watched battle ever load full
detail (memory stays bounded); ambient labels are banned at C1/C2 (clutter —
they appear on focus); the HUD mode flips at B2 and nowhere else, on the same
frame as the town swap.

## 7. The two swap bands

**B2 — the cloud veil (C2 ↔ R).** Four to six camera-facing painted cloud
quads (unshaded, alpha texture from game-art-director), placed at 35–60% of
the camera distance. Opacity `0.35 × max(0, 1 − |log2(d / B2)| / 0.7)`: 35%
at B2, gone ±0.7 doublings away. Drift 2% of screen width per second
(0 with reduced motion). Overdraw ≤ 1.5 screens. It must look right as a
still: a pinch can park the camera inside the band.

**B3 — the war-map (R ↔ M), PROPOSAL to world-forge / world.md.** Beyond B3 the
realm is drawn as the lord's painted war-map: one ground plane with the painted
map texture and fixed-size icons. The 3D terrain dissolves into it across
`B3 / 1.23 … B3 × 1.23` (±0.3 doublings), progress driven by distance:

```glsl
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, depth_test_disabled, cull_back;
uniform sampler2D map_tex : source_color, filter_linear_mipmap;
uniform sampler2D paper_noise : filter_linear, repeat_enable; // tiling paper-fibre noise, 512 px
uniform float progress : hint_range(0.0, 1.0) = 0.0; // smoothstep of log distance
uniform float edge_width = 0.04;
uniform vec3 edge_ink : source_color = vec3(0.118, 0.090, 0.071); // INK #1E1712
void fragment() {
	float n = texture(paper_noise, UV * 6.0).r;
	float p = mix(-edge_width, 1.0 + edge_width, progress);
	float a = smoothstep(n - edge_width, n, p);
	float edge = a - smoothstep(n, n + edge_width, p);
	ALBEDO = mix(texture(map_tex, UV).rgb, edge_ink, edge * 0.6);
	ALPHA = a;
}
```

- While the dissolve runs, the terrain vertex shader scales height by
  `(1 − progress)` so hills flatten into the map; otherwise relief × cot(pitch)
  misregisters rivers by up to 4% of the screen (200 m relief at 66°).
- At `progress = 1` hide the terrain chunks (`visible = false`): the GPU cost
  of M is one textured plane plus icons.
- Fallback if world.md rejects the war-map: at B3 swap cluster forms to icons
  and raise fog density; keep terrain at its lowest LOD.

## 8. Where the camera may go

1. **Only the own castle can be entered.** B2↓ is crossed only when the focus
   is inside the own town bounds + 15%. The only other full-detail dive is
   battle-forge's "Watch" ([shot-library.md](shot-library.md) BATTLE_ENTER).
2. **The neighbour floor.** Elsewhere the zoom stops at the distance where a
   100 m town projects 300 px (672 m in the example): cluster forms never fill
   the screen. Rubber band at the floor.
3. **The castle magnet.** Pinching in below the floor with the own town's
   centre inside the middle 60% of the screen glides the focus to the town
   centre: `focus += (town_centre − focus) × w`, `w = smoothstep(floor, B2, d)`.
   The player lands on their castle without aiming.
4. **Pan bounds.** C1/C2: focus inside the town bounds + 15% (rubber band 8%);
   R/M: the realm bounds. Between B2↓ and B2↑ the bound interpolates with the
   same smoothstep, so zooming out never snaps the focus.

## 9. Light, fog and sound by level

- **Shadows**: `DirectionalLight3D.directional_shadow_max_distance = 1.5 × d`,
  changed in **four steps only** (one per level, at the commit, inside the
  fade) — a max distance that changes every frame refits the shadow map and
  the shadows swim. `Light3D.shadow_opacity` fades 1 → 0 across the B2 band.
- **Fog**: `Environment.fog_density ∝ 1 / d` so the top of the frame keeps the
  same haze at every level; colour from the time-of-day preset
  (game-art-director environments.md: campaign dawn, working noon, siege dusk,
  chronicle night).
- **Audio beds** (audio-forge owns assets and mix): town bed gain 1 up to C2
  rest, 0 at B2 × 2; field wind bed its complement to B3; war-room bed (fire,
  distant wind, a quill) beyond B3. Continuous with log distance, never
  switched on the level commit.

## 10. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Sky or horizon visible on a tall phone | pitch below the §2 minimum for that shape | raise the pitch floor; rerun `w1f_aspect_sweep` |
| Zoom-out crawls, then rushes | distance interpolated in metres | log-space interpolation (§3) |
| Camera tilts noticeably while zooming | pitch curve slope > 6°/doubling | re-anchor the curve (§5) |
| HUD flickers at a band edge | no hysteresis or no dwell | ±0.15 doublings and 250 ms dwell (§4) |
| Half the town swaps before the other half | per-building ranges without an HLOD parent | `visibility_parent` to the cluster ([streaming.md](streaming.md) §3) |
| Shadows jump or swim during a zoom | shadow max distance changed every frame | four steps, inside the level fade (§9) |
| Player lands in empty terrain at close zoom | no neighbour floor / magnet | §8 rules 2 and 3 |
| Z-fighting on far roofs at realm level | fixed near plane | near = 0.02 × distance (§2) |
| Camera judders on a 120 Hz phone | rig updated in `_physics_process` | move the rig in `_process` (§1) |
| Neighbour castle fills the screen as a crude cluster | no floor | the 300 px floor (§8) |

## 11. Checklist

- [ ] Rig is focus → yaw → pitch → boom; no code writes the Camera3D transform directly.
- [ ] `KEEP_WIDTH`, 30° horizontal FOV; horizon test passes on all 6 aspect shapes.
- [ ] Near/far recomputed from distance every frame.
- [ ] All distance interpolation in log space; pinch anchored under the centroid.
- [ ] Level thresholds computed from `H_b`, `W_town`, `R_w` at runtime, printed by the probe.
- [ ] Hysteresis ±0.15 doublings + 250 ms dwell; one `level_changed` per commit.
- [ ] Pitch curve slope ≤ 6°/doubling; pitch within 45–72° (42° in authored shots).
- [ ] Every row of the §6 table implemented with its mechanism and fade times.
- [ ] Veil peaks at B2 (±2 frames in the frame-by-frame review, [qa.md](qa.md)).
- [ ] Only the own castle (and a watched battle) crosses B2↓; floor and magnet active.
- [ ] Shadow distance changes in four steps; fog density ∝ 1/d.
