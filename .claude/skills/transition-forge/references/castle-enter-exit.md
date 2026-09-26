# Castle enter / exit — leaving, entering, the gate, marching out, coming home

Seven moves between the castle and the realm, and the gate asset they all
depend on. §4 is the **build contract for blender-forge**: the gate's parts,
pivots and every key of its `open` and `close` clips, frame by frame. Build it
exactly; the game code reads the passable frames and cue frames from here.

Frames: shots are in **60 fps game frames (f60)**; Blender clips are authored at
**30 fps (f30)** per blender-forge [animation.md](../../blender-forge/references/animation.md)
rule 3. Durations are in ms beside every frame count. Curves are the named
curves of [easing.md](easing.md). Distances and levels: [zoom-model.md](zoom-model.md).

## 1. CASTLE_LEAVE — castle → region (the toggle button)

Path: van Wijk zoom-pan ([easing.md](easing.md) §6), `SINE_IO` on the path
parameter, `T = clamp(0.41 × S, 700 ms, 1,000 ms)`; target R_near centred on
the own town. From C2 rest that is 3.28 doublings → **700 ms (42 f60)**, peak
7.4 doublings/s; from `d_min` 4.98 doublings → 1,000 ms (60 f60), peak 7.8.

| f60 | ms | Camera | World | UI (ui-forge) | Audio (audio-forge) |
|---|---|---|---|---|---|
| 0 | 0 | start; yaw offset → 0 on the same curve | realm ring already resident ([streaming.md](streaming.md) §2) | castle HUD out 120 ms | `cam_rise_wind`, 800 ms |
| ≈14 | ≈233 | crosses B2↑ (249 m) | `level_changed(C2, R)`: town HLOD swap at the veil peak; bubbles out 120 ms; lines and tokens in 200 ms; shadow step | realm HUD in, 150 ms, from the commit frame | beds crossfade by distance |
| 42 | 700 | arrives at R_near (1,400 m, 60°) | — | toggle now shows "castle" | — |

Commit frame for any start distance: `f = N × acos(1 − 2q) / π`,
`q = log2(B2↑ / d0) / log2(R_near / d0)`, N = shot length in frames.
Input is live from f0: a touch-down stops the move on that frame and hands the
camera to the finger at the current distance. Reduced motion: the 250 ms
parchment dip cut ([easing.md](easing.md) §7).

## 2. CASTLE_ENTER — region or realm → castle

Trigger: the toggle, or a tap on the own castle cluster/icon. Target: C2 rest,
focus = the last castle focus if the player left the castle < 10 min ago,
else the keep. Path: van Wijk, `SINE_IO`, `T = clamp(0.41 × S, 700, 1,500 ms)`;
S > 3.66 (T would pass 1,500 ms) → dip cut instead of a fly.

| Start | Doublings | Duration | B2↓ commit |
|---|---|---|---|
| R_near (1,400 m) | 3.28 | 700 ms (42 f60) | f31 (517 ms) |
| B3 (4,199 m) | 4.87 | 978 ms (59 f60) | f47 (79%) |
| M rest (22.4 km) | 7.28 | 1,463 ms (88 f60) | f73 (83%) |

The own town's LOD1 never unloads ([streaming.md](streaming.md) §6), so the
commit never waits; LOD0 streams in during C2 → C1. Same input, veil, HUD and
reduced-motion rules as §1.

## 3. COLD_OPEN and RESUME — a live realm has no title screen

**COLD_OPEN** (app launch): the loading painting (game-art-director T-* vignette)
sits on a CanvasLayer above the world while the castle loads. The world
renders ≥ 3 frames under the painting (pipeline and texture warm-up,
[streaming.md](streaming.md) §5), camera at 1.02 × C2 rest on the keep.
Then: painting `modulate.a` 1 → 0 in 400 ms (24 f60) `SINE_IO`; camera dolly
to C2 rest in 1,200 ms (72 f60) `QUAD_OUT`; the digest (design-forge core-loop
§8.1) at f24. Input is live from f0; a tap during the fade finishes it in
100 ms. Budget: resume to first input ≤ 2.0 s (core-loop §8.1).

**RESUME** (back from background): no camera move. Everything that is a
function of time (marches, gate, timers) is re-evaluated at server time; away
> 15 s → the production count-up (core-loop A1, feel-forge).

## 4. The gate — build contract for blender-forge (and castle-forge)

### 4.1 Bands (PROPOSAL — map to castle-forge's wall tiers, path to confirm)

| Band | Wall tiers | Gate | Moving parts | `open` f30 | Passable | `close` f30 |
|---|---|---|---|---|---|---|
| A | 1–2 | palisade gate, two light timber leaves on strap hinges | `Door_L`, `Door_R` | 0–30 (1,000 ms) | **f15 (500 ms)** | 0–21 (700 ms) |
| B | 3 | timber gatehouse, two iron-strapped oak leaves | `Door_L`, `Door_R` | 0–39 (1,300 ms) | **f26 (867 ms)** | 0–36 (1,200 ms) |
| C | 4–6 | stone gatehouse: portcullis + two oak leaves + roof windlass | `Portcullis`, `Windlass`, `Door_L`, `Door_R` | 0–90 (3,000 ms) | **f68 (2,267 ms)** | 0–87 (2,900 ms) |

Part names are identical in every band, so one controller drives all of them.
4 moving parts ≤ 8 → object hierarchy, no armature (animation.md "Rig scope").

### 4.2 Parts, sizes, pivots

Blender metres, Z up. The gate's OUTSIDE faces −Y (Blender front view; arrives
in Godot facing +Z; castle-forge rotates the instance into the wall).
Passage 3.0 × 4.0 m (architecture.md §5); passage depth `D_p` (castle-forge;
PROPOSAL 8 m band C, 6 m band B, 1 m band A).

| Part | Form (blender-forge forms.md) | Pivot (object origin) | Motion |
|---|---|---|---|
| `Door_L` | leaf 1.40 m (hinge to centre) × 4.0 m, arched head cut to the arch, 0.12 m thick (two cross-laid board layers), 3 strap hinges (`strap`), clinch nails (`rivet_row`) | on the pintle axis, x = −1.40 (0.10 m in from the passage wall), z = 0 | rot Z = **+θ** (free edge swings to +Y, inward) |
| `Door_R` | mirror of `Door_L` | x = +1.40 | rot Z = **−θ** |
| `Portcullis` (C) | grid 3.2 × 4.4 m; oak 0.12 × 0.12 m, verticals at 0.28 m, rails at 0.35 m; iron straps + rivets at crossings; iron-shod spike tips 0.30 m | bottom centre on the tip line | loc Z = **z** (tips height above the sill) |
| `Windlass` (C) | drum Ø 0.60 m (r = 0.30 m) × 2.4 m + two hand wheels Ø 1.6 m, **6 spokes**, one rigid object, under an open penthouse on the gatehouse roof | on the drum axis centre | rot X = **θ_w = 190.99 × z** degrees |

- Leaves hang 0.6 m behind the portcullis groove (band C) and open INTO the
  passage; a stone rebate stops them at 0°. Grooves are 0.10 m deep each side
  and run to ≥ 8.2 m, so the raised grid hides in the chamber except a 0.6 m
  band of teeth under the 4.0 m arch crown (it reads "open, but guarded").
- Chains: the visible span from the drum to the floor slot has constant
  length (extra chain wraps on the drum as static geometry) — no chain
  animation. Pawl and ratchet: modelled, not animated (sub-pixel at every game
  distance; their clicks are audio).
- `Windlass` sign: check in the 4-frame strip that the chain winds ONTO the
  drum while the grid rises; flip the sign if it unwinds.

### 4.3 Motion laws

1. **Rolling constraint**: `θ_w = z / r` at every frame of both clips. Key the
   `Windlass` on the SAME frames with the SAME interpolation as the
   `Portcullis`, values × 190.99 °/m — proportional keys give an exact match.
2. **Wagon-wheel limit**: a spoked part turns ≤ 0.4 × spoke gap per 30 fps
   frame (6 spokes → ≤ 24°/frame = 720°/s). Measured: open 607°/s (0.34),
   close 672°/s (0.37). Faster and the wheel appears to turn backwards.
3. **No free fall**: the crew brakes the drop — 0.77 g acceleration to
   3.52 m/s, then constant speed. Free fall of 3.40 m would take 0.83 s and
   spin the wheel at 1,400°/s.
4. **Two crews, not twins**: every `Door_R` key is `Door_L`'s key **+2 frames**.
   The passable frame uses the later leaf.
5. **Heavy is slow, light snaps** (animation.md rule 6): band B/C leaves peak
   167°/s; band A leaves 339°/s open, 427°/s slam; portcullis peak 3.18 m/s
   in 0.674 m heaves with a **4-frame hesitation** per section (rule 6).
6. **Overshoot sizes**: heavy leaves 3° past rest-open (88° → 85°); light
   leaves 6° (106° → 100°); closing rebound 1.5° heavy, 3° light; portcullis
   pawl catch 6 cm drop, 2.5 cm rebound; impact bounce 5 cm then 1 cm.
7. **No interpenetration**: at 88° a heavy leaf stays ≥ 0.02 m off the passage
   wall; the grid never touches the groove faces; leaves never cross 0°.

### 4.4 Clip keys (f30)

Read each row as `frame: value INTERP`, where INTERP applies from that key to
the next (Blender `keyframe.interpolation` / `keyframe.easing`:
`QUAD/OUT` = `'QUAD'`/`'EASE_OUT'`, `SINE/IO` = `'SINE'`/`'EASE_IN_OUT'`,
`CONST` = `'CONSTANT'`, `LIN` = `'LINEAR'`). Door values are θ in degrees
(`Door_R` stores −θ). Every part carries a key on the clip's last frame.

**Band A `open` (0–30)** — latch lift, hold, snap, settle.
| Part | Keys |
|---|---|
| `Door_L` | 0: 0 QUAD/OUT · 3: 4 CONST · 5: 4 QUAD/OUT · 23: 106 SINE/IO · 28: 100 CONST · 30: 100 |
| `Door_R` | 0: 0 CONST · 2: 0 QUAD/OUT · 5: −4 CONST · 7: −4 QUAD/OUT · 25: −106 SINE/IO · 30: −100 |

**Band A `close` (0–21)** — pushed shut, slam, one rebound.
| Part | Keys |
|---|---|
| `Door_L` | 0: 100 QUAD/IN · 14: 0 QUAD/OUT · 16: 3 QUAD/IN · 19: 0 CONST · 21: 0 |
| `Door_R` | 0: −100 CONST · 2: −100 QUAD/IN · 16: 0 QUAD/OUT · 18: −3 QUAD/IN · 21: 0 |

**Band B `open` (0–39)** — unbar jolt, crew takes the weight, heavy swing, settle.
| Part | Keys |
|---|---|
| `Door_L` | 0: 0 QUAD/OUT · 4: 3 CONST · 7: 3 SINE/IO · 31: 88 SINE/IO · 37: 85 CONST · 39: 85 |
| `Door_R` | 0: 0 CONST · 2: 0 QUAD/OUT · 6: −3 CONST · 9: −3 SINE/IO · 33: −88 SINE/IO · 39: −85 |

**Band B `close` (0–36)** — swing shut, thud into the rebate, rebound, settle.
| Part | Keys |
|---|---|
| `Door_L` | 0: 85 SINE/IO · 24: 1 QUAD/IN · 26: 0 QUAD/OUT · 29: 1.5 SINE/IO · 34: 0 CONST · 36: 0 |
| `Door_R` | 0: −85 CONST · 2: −85 SINE/IO · 26: −1 QUAD/IN · 28: 0 QUAD/OUT · 31: −1.5 SINE/IO · 36: 0 |

**Band C `open` (0–90)** — doors first (still behind the lowered grid), then
the windlass crew takes the strain and heaves the grid up in five sections.
| Part | Keys |
|---|---|
| `Door_L`, `Door_R` | band B `open` keys, plus a hold key at 90 |
| `Portcullis` z (m) | 0: 0 CONST · 12: 0 QUAD/OUT · 15: 0.030 CONST · 18: 0.030 SINE/IO · 28: 0.704 CONST · 32: 0.704 SINE/IO · 42: 1.378 CONST · 46: 1.378 SINE/IO · 56: 2.052 CONST · 60: 2.052 SINE/IO · 70: 2.726 CONST · 74: 2.726 SINE/IO · 84: 3.400 QUAD/IN · 86: 3.340 QUAD/OUT · 88: 3.365 SINE/IO · 90: 3.360 |
| `Windlass` θ_w (deg) | same frames and interpolation: 0 · 0 · 5.73 · 5.73 · 134.45 · 134.45 · 263.18 · 263.18 · 391.90 · 391.90 · 520.63 · 520.63 · 649.35 · 637.89 · 642.67 · 641.71 |

Beats: f0–4 bar drawn, leaves jolt 3°; f7–31 swing; f12–15 chain takes the
strain (+3 cm); f18–84 five heaves, hesitations at f28, f42, f56, f70; f84–86
grid drops onto the pawl; f86–90 rebound and settle.

**Band C `close` (0–87)** — lever lifts the grid off the pawl, braked drop,
impact, then the doors.
| Part | Keys |
|---|---|
| `Portcullis` z (m) | 0: 3.36 QUAD/OUT · 3: 3.40 CONST · 6: 3.40 QUAD/IN · 20: 2.58 LIN · 42: 0.00 QUAD/OUT · 44: 0.05 QUAD/IN · 47: 0.00 QUAD/OUT · 49: 0.01 QUAD/IN · 51: 0.00 CONST · 87: 0.00 |
| `Windlass` θ_w (deg) | same frames: 641.71 · 649.35 · 649.35 · 492.74 · 0 · 9.55 · 0 · 1.91 · 0 · 0 |
| `Door_L` | 0: 85 CONST · 51: 85 SINE/IO · 75: 1 QUAD/IN · 77: 0 QUAD/OUT · 80: 1.5 SINE/IO · 85: 0 CONST · 87: 0 |
| `Door_R` | 0: −85 CONST · 53: −85 SINE/IO · 77: −1 QUAD/IN · 79: 0 QUAD/OUT · 82: −1.5 SINE/IO · 87: 0 |

### 4.5 Passable frame and clearance

Passable = the first frame at which a token squad (a two-file column 1.4 m wide
— PROPOSAL, battle-forge owns formations) passes untouched:
- leaves ≥ **71°** (clear width ≥ 1.6 m between leaf faces), and
- portcullis tips ≥ `CLEAR_H = H_token + 0.20 m`, where `H_token` is the top of
  the tallest map token at castle scale (the cavalry banner finial; PROPOSAL
  2.40 m, to confirm with battle-forge / game-art-director units.md).

| `CLEAR_H` | Band C passable | Note |
|---|---|---|
| 2.40 m | f66 (2,200 ms) | |
| **2.60 m** | **f68 (2,267 ms)** | default |
| 2.80 m | f77 (2,567 ms) | falls in heave 5 |
| 3.00 m | f79 (2,633 ms) | |
| > 3.20 m | redesign | teeth margin < 0.2 m: raise travel and the chamber |

Code constants (seconds): `PASSABLE = {A: 15/30, B: 26/30, C: 68/30}`.

### 4.6 Empties (exported as glTF nodes)

`npc_gate_inner` (inner end of the passage, floor centre) · `npc_gate_outer`
(1.0 m outside the grid or leaf line) · `fx_dust_gate` (sill centre: impact
dust, feel-forge particles) · `sfx_gate_mech` (windlass centre in C, passage
centre at 2 m in A/B: the `AudioStreamPlayer3D` anchor) · `cam_gate_L` or
`cam_gate_R` (look-at point: passage centre, 2.0 m high, 1.0 m outside; the
suffix names the road side the gate shot yaws toward).

### 4.7 Export and round trip

- Each part's action (`Door_L_open`, `Portcullis_close` …) sits on an NLA track
  named exactly `open` or `close` (`obj.animation_data.nla_tracks.new()`,
  `track.strips.new("open", 0, action)`), then clear the active action.
  Export with `export_animation_mode='NLA_TRACKS'`, `export_force_sampling=True`:
  same-named tracks merge into ONE glTF animation per clip. (This extends
  animation.md's `'ACTIONS'` export line for multi-object clips.)
- The round trip must print exactly — band A `anims=[('close', 0, 21), ('open', 0, 30)]`,
  band B `[('close', 0, 36), ('open', 0, 39)]`, band C `[('close', 0, 87), ('open', 0, 90)]`.
  A per-part name in the print means the merge failed; a shorter range means a
  part lacks its last-frame key.
- Static GLB pose = frame 0 of `open` = closed (animation.md clip rule 2).
- Godot import dock: loop mode None on both clips; **animation optimizer off**
  for this scene (it deletes the 2.5 cm and 1.5° settles); animation FPS 30.

### 4.8 Build QA (with animation.md A–E)

Render frames 0, 4, 18, 28, 32, 68, 84, 90 (`open`) and 0, 6, 20, 42, 44, 51, 77, 87
(`close`) from (a) the game camera at C2 rest (pitch 50°, 30° horizontal FOV,
144 m, cropped to the gatehouse) and (b) the gate-shot camera (pitch 46°, yaw
+10°, gatehouse 45% of frame width). Print and paste:
1. `|θ_w − 190.99 × z| ≤ 0.5°` at every frame of both clips.
2. Leaf free edges at y > 0 (inside) at every frame after f4; ≥ 0.02 m wall gap at 88°.
3. `z(68) ≥ 2.60` (or the chosen `CLEAR_H` at its passable frame).
4. Largest per-frame `Windlass` step ≤ 24°.
5. The three `anims=[…]` lines above.

### 4.9 Audio cue frames (f30; audio-forge owns assets and mix)

| Band | `open` | `close` |
|---|---|---|
| A | 0 `gate_latch` · 5 / 7 `gate_creak_light` L/R | 14 / 16 `gate_slam_light` L/R |
| B | 0 `gate_unbar` · 7 / 9 `gate_hinge_groan` L/R | 24 / 26 `gate_door_thud` L/R · 28 `gate_bar_drop` |
| C | B's cues + 12 `gate_chain_strain` · 18, 32, 46, 60, 74 `gate_windlass_heave` · 28, 42, 56, 70 `gate_pawl_clack` · 84 `gate_pawl_catch` | 0 `gate_brake_lever` · 6 `gate_chain_run` (1.2 s, pitch follows speed) · 42 `gate_portcullis_impact` + `fx_dust_gate` · 75 / 77 `gate_door_thud` · 79 `gate_bar_drop` |

Players at `sfx_gate_mech`; `max_distance` = the B2 distance (silent at R/M).
A departure adds battle-forge's `bt_horn_depart` at f0 of `open`.

## 5. GateController (Godot 4) — the gate is a function of time

- Stores the last command (`open`/`close`) and its start time on the server
  clock. Pose = clip at `now − start`. On becoming visible, on resume, after a
  zoom-in: `anim.play(clip)` then `anim.seek(clampf(now - start, 0.0, length), true)`.
  Never restart from 0 when late.
- **Schedule from marches** (functions of time): departure → `open` at the
  send time; arrival → `open` starts at `t_arrive − PASSABLE[band] − 0.25 s`.
  **Close** only when no own march is due within the next 8 s, ≥ 60 s after
  the last departure (battle-forge `flows.md` §4: repeat march-outs find it
  open) and ≥ 8 s after the last arrival. A request during a running clip is
  `anim.queue()`d, never cut.
- **Incoming enemy**: battle-forge starts `close` ≥ 3.0 s before the enemy's
  arrival (band C close lasts 2.9 s).
- Never `play_backwards("open")` as a close: reversed heaves read as a rewind.
- Cues: each frame fire the cues whose time lies in `(prev_pos, pos]`; after a
  seek, drop cues older than 100 ms (no burst of stale sounds).
- Animate only at C1/C2 with the gate inside the frustum + 10%; otherwise keep
  only the command and time (zero cost).
- API: `request_open(at_s)`, `request_close(at_s)`, `passable_time() -> float`,
  `is_passable(now_s) -> bool`, signal `passable`.

## 6. MARCH_OUT — the choreography of every march-out (no camera move)

1. t_send = the Send tap (optimistic; if the server refuses, the squad turns
   and fades within 400 ms). The gate opens if closed.
2. The token squad spawns in the passage shadow (150 ms dither in) as a 1.4 m
   column and walks at **3.0 m/s** (PROPOSAL; gait is battle-forge / hero3d)
   from t_gate + 0.15 s (t_gate = the moment `open` started).
3. Spawn depth behind the gate line = `clamp(3.0 × (T_pass_rem − 0.15), 1.5 m, D_p)`,
   so the banner crosses the line exactly at passable, never earlier, and
   never later than 0.65 s after the tap when the gate is already open.
   Band A: 1.05 m, out at 500 ms · B: 2.15 m, out at 867 ms · C: 6.35 m, out
   at 2,267 ms.
4. **Handoff at `npc_gate_outer`** (t_exit, 0.33 s after the gate line): the server march started at t_send,
   so its true position is ahead by `Δ = v_m × (t_exit − t_send)`. Display the
   squad at `pos(t) − Δ_rem`, closing Δ at `v_m` (the squad walks at 2 × march
   speed), speed changes eased over 300 ms `SINE_IO`, gait `speed_scale` =
   displayed speed / nominal (cap 2.2). It catches up after `t_exit − t_send`.
   The ETA on screen is always the server's.
5. **The column** (battle-forge `flows.md` §4 owns order and spacing: cavalry
   vanguard → infantry with the lord's banner → spearmen → archers and
   crossbows → siege train; one squad every 250 ms on the first march-out of a
   session, 125 ms on repeats): squad 1 crosses at passable, each next one
   `spacing` later. The horn `bt_horn_depart` plays on the gate's first open frame.
6. At the B2 commit (under the veil) the column collapses into the one realm
   token (battle-forge `flows.md` §5); the token's size then follows distance
   continuously (battle-forge owns its pixel minimum), so it never pops.
7. Sent from the realm view (the common case — targets live on the map) or
   gate off-screen: no choreography; the token appears at the gate point at
   `pos(t)` with battle-forge's 400 ms banner-raise.

**MARCH_OUT_SESSION** — the first march-out of a session sent from C1/C2
(battle-forge `flows.md` §4). f0: the gate `open` starts at the tap; camera to
`cam_gate_*` framing by `ZoomPath` + `CAM_ARRIVE` in 500 ms (30 f60), no yaw
offset. The shot ends at min(first squad crossing + 600 ms, 2,500 ms): band A
1,100 ms, B 1,467 ms, C 2,500 ms (squad 1 emerges at 2,267 ms). Input is
blocked 150 ms, then any tap ends the shot. The camera stays at the gate
framing (no automatic zoom-out: the player sent it from the castle and may
stay). Later march-outs in the session find the gate open (§5: 60 s linger)
and play §6 with no camera move.

## 7. MARCH_OUT_FIRST — once per account (the first march)

Plays only for band A or B gates (passable ≤ 867 ms) so it fits the 3.5 s
first-time cap; otherwise it is marked seen and §6 plays.

| f60 | ms | Camera | Gate / squad | UI / audio |
|---|---|---|---|---|
| 0 | 0 | van Wijk + `CAM_ARRIVE`, 700 ms, to `cam_gate_*`: gatehouse 45% of screen width, pitch 46°, yaw offset +10° toward the road | squad spawns inside | HUD hides in 150 ms; `sting_march_out` |
| 21 | 350 | moving | gate `open` starts | gate cues |
| 42 | 700 | arrives; push-in 3% over 1,200 ms `SINE_IO` | leaves swing | — |
| 51 (A) / 73 (B) | 850 / 1,217 | — | squad crosses the gate line | — |
| +0 | | focus follows the squad (spring, 98% in 600 ms); yaw offset → 0 over 1,200 ms `SINE_IO` | — | — |
| +72 | +1,200 | CASTLE_LEAVE path (700 ms) with the focus on the squad | march line appears at the B2 commit | realm HUD in |
| end | 2,750 (A) / 3,117 (B) | camera returned to the player | — | — |

Input is swallowed for the shot (first time only). Reduced motion: no push-in,
no yaw offset, both moves become dip cuts.

## 8. RETURN_HOME — the camera never moves

The lead squad reaches `npc_gate_outer` at t_arrive (the gate became passable
0.25 s earlier, §5). Each squad walks from `npc_gate_outer` to 1 m inside the
gate line (2 m, 667 ms at 3.0 m/s) and dither-fades over its last 300 ms in
the passage shadow; a 5-squad column at 125 ms spacing ends at 1,167 ms
(battle-forge `flows.md` §8: ≤ 1,200 ms). The loot count-up and toast are
feel-forge / ui-forge. Gate not visible → the token fades at the town cluster
or icon edge in 200 ms.

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Leaf rotates about its centre | origin not on the pintle axis | origin on the hinge (§4.2) |
| Leaves move as mirror twins | same keys on both | `Door_R` +2 frames (§4.3 law 4) |
| Wheel appears to spin backwards | > 0.5 spoke gap per frame | braked drop, ≤ 24°/frame (laws 2–3) |
| Grid rises, nothing turns | windlass unkeyed or not proportional | keys × 190.99 on the same frames |
| Godot shows `Door_L_open` etc. | NLA merge failed | tracks named `open`/`close`, `NLA_TRACKS` mode |
| Clip shorter than spec, passable drifts | a part lacks its last-frame key | hold keys at the end |
| Close looks like a rewind | `play_backwards` | author `close` |
| Banner clips the teeth | passable computed for a shorter token | `CLEAR_H` table (§4.5) |
| Squad waits at a closed gate | gate opened at arrival | open at `t_arrive − passable − 0.25 s` |
| Gate shows closed while a march leaves | clip restarted from 0 on zoom-in | seek to `now − start` |
| Burst of gate sounds on zoom-in | seeked range fired | drop cues older than 100 ms |
| Settles vanish in Godot | import optimizer | optimizer off; compare key counts |
| Squad sprints for 10 s after the gate | unbounded catch-up | 2 × march speed, closes in `t_exit − t_send` |
| First live frame flashes grey on cold open | painting faded before warm-up | ≥ 3 hidden warm frames |

## 10. Checklist

- [ ] CASTLE_LEAVE 700 ms from C2 rest; commit frame inside the veil peak (±2 f60).
- [ ] CASTLE_ENTER durations match §2; S > 3.66 → dip cut.
- [ ] COLD_OPEN: input live at f0; ≥ 3 warm frames under the painting.
- [ ] Gate built to §4.2 with origins on hinge, tip line, drum axis.
- [ ] All clip keys as §4.4; `Door_R` +2 f30; hold key at the last frame on every part.
- [ ] Rolling constraint ≤ 0.5° error; windlass ≤ 24°/f30.
- [ ] Round trip prints the §4.7 `anims=[…]` line for the band.
- [ ] Godot import: no loop, optimizer off, FPS 30.
- [ ] GateController seeks by time, queues requests, drops stale cues.
- [ ] MARCH_OUT handoff closes the gap at 2 × march speed; ETA unchanged.
- [ ] MARCH_OUT_SESSION ≤ 2,500 ms, tap ends it after 150 ms, no automatic zoom-out.
- [ ] MARCH_OUT_FIRST ≤ 3.5 s, band A/B only, once per account.
- [ ] Gate lingers open 60 s after a departure; column order and spacing from battle-forge.
- [ ] RETURN_HOME never moves the camera.
