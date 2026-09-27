# Shot library — every camera move, who may trigger it, how long, what loads

Each shot: trigger → path → duration in ms and 60 fps frames (f60) → named
curve ([easing.md](easing.md)) → input rule → what streams during it
([streaming.md](streaming.md)) → sound → reduced-motion variant. Castle ↔
realm moves, the gate and the march out/in are in
[castle-enter-exit.md](castle-enter-exit.md); the zoom levels in
[zoom-model.md](zoom-model.md). Panel tweens are ui-forge's
(`motion.md`); battle shots after the handoff are battle-forge's
(`presentation.md` §1).

## 1. CameraDirector — one owner, clear priorities

Autoload `CameraDirector` (path to confirm; ui-forge `godot.md` places it under
`Main`). Nothing else writes the camera. Suggested surface (GDScript):

```gdscript
enum Level { CASTLE_CLOSE, CASTLE_OVERVIEW, REGION, REALM }
enum Prio { AMBIENT, UI, CEREMONY, EXTERNAL }      # a finger outranks AMBIENT and UI
signal level_changed(old_level: int, new_level: int)
signal shot_started(id: StringName)
signal shot_finished(id: StringName, interrupted: bool)
var input_blocked := false                          # read by the UI and by the probe
var reduced_motion := false                         # Settings → "Reduce camera motion"
func play(id: StringName, params := {}) -> void
func frame_building(building: Node3D, world_rect: Rect2) -> void
func handoff(owner: StringName) -> bool             # battle-forge takes the rig
func release(owner: StringName) -> void             # rig returns to the stored pose
func is_shot_running() -> bool
func rig_state() -> Dictionary                      # {focus, yaw, pitch, distance, fov, level}
func probe_ids() -> PackedStringArray               # qa.md §2 — the probe contract
func probe_play(id: StringName) -> Dictionary       # {"spec_ms": float, "repeat": bool}
func probe_reset() -> void                          # C2 rest on the keep, no shot running
```

**Priority rules**
1. **The camera belongs to the player.** A touch-down on the world stops every
   AMBIENT (follow, inertia) and UI shot on the same frame, keeping the current
   rig state; the finger takes over.
2. **Background events never move the camera** — a march returning, a building
   finishing, an ally attacked, a chat line. They toast (ui-forge) with a
   tap-to-jump (JUMP_TO). One exception: the player is FOLLOWING a march, or its
   contact point is on screen, when it makes contact → BATTLE_ENTER (auto)
   (battle-forge `flows.md` §7): the player is already watching.
3. A new UI shot replaces a running one and starts from the CURRENT rig state.
   A second tap on the world toggle during CASTLE_LEAVE / ENTER reverses it
   from the current point (ui-forge `architecture.md` §1).
4. **CEREMONY** shots (first time only) own camera and input for ≤ 3.5 s. The
   "seen" flag is server-side (cloud-forge) so a reinstall does not replay
   them; a replay from settings is skippable by a tap after 150 ms.
5. **EXTERNAL**: after `handoff("battle-forge")` battle-forge owns shots and
   input until `release`; the rig limits (pitch 42–72°, yaw ±15°, no roll)
   still apply. `Camera3D.h_offset` / `v_offset` are battle-forge's shake
   channel; transitions never write them and `release` zeroes them.

**Input-block budget**

| Shot class | Camera input block | Rule |
|---|---|---|
| Player-triggered moves (focus, menu, jump, leave, enter, zoom step) | **0 ms** | touch interrupts (rule 1) |
| Session gate shot (MARCH_OUT_SESSION) | ≤ 150 ms, then a tap skips | battle-forge `flows.md` §4 |
| Panels (ui-forge) | ≤ 400 ms including their motion | ui-forge `motion.md` |
| First-time ceremony | ≤ 3.5 s, once per account | MARCH_OUT_FIRST 2.75 / 3.12 s, REALM_FIRST 1.8 s |
| Battle dive | 0 ms | a touch cancels the dive |
| Cold open | 0 ms | a tap finishes the fade in 100 ms |

**Sound rule**: moves that repeat many times a session (focus, menu, jump,
zoom step) have NO camera sound — a whoosh per tap tires the ear in one
evening. Only level-crossing moves (leave, enter, battle dive) and ceremonies
carry a cue; the distance-driven beds do the rest (audio-forge).

## 2. The catalogue

`s` = pan distance in screen widths; `S` = `ZoomPath.length()` ([easing.md](easing.md) §6).

| Id | Trigger | Path / curve | Duration | Input | Streams during it | Reduced motion |
|---|---|---|---|---|---|---|
| CASTLE_LEAVE | toggle at C1/C2 | van Wijk, `SINE_IO`, T = clamp(0.41 S, 700, 1,000) | 700 ms (42 f60) from C2 rest | 0 | realm ring must already be resident | dip cut 250 ms |
| CASTLE_ENTER | toggle, tap own castle | van Wijk, `SINE_IO`, T = clamp(0.41 S, 700, 1,500); S > 3.66 → dip | 700–1,463 ms (42–88 f60) | 0 | own LOD1 resident; LOD0 on C2 → C1 | dip cut |
| COLD_OPEN | app launch | painting fade `SINE_IO` + dolly 2% `QUAD_OUT` | fade 400 ms (24 f60), dolly 1,200 ms (72 f60) | 0 | castle boot set + 3 warm frames | no dolly |
| FOCUS_BUILDING | tap a building | pan `QUAD_OUT`, only if outside the comfort box | 300 + 400·s ms, ≤ 540 ms (≤ 32 f60) | 0 | menu art requested on touch-down | kept, × 0.8 |
| MENU_OPEN | open a building's card | van Wijk, `CAM_ARRIVE`, T = clamp(0.62 S, 380, 700) | 380–700 ms (23–42 f60) | 0 (sheet ≤ 400 ms) | card art LOADED by sheet 50% | dip if > 1 doubling |
| MENU_CLOSE | close the card | undo the stored delta, `SINE_IO` | 320 ms (19 f60) | 0 | — | kept |
| MENU_NEXT | next building, sheet open | pan `SINE_IO` | 300 + 300·s ms, ≤ 600 ms | 0 | next building's art | kept |
| PANEL_FULL_OPEN | a full screen opens | push-in 4% `QUART_OUT`, matched to ui-forge `full_in` | 260 ms (16 f60), then 3D paused | ui-forge | head-piece art from `button_down` | no push-in |
| PANEL_FULL_CLOSE | the full screen closes | 3D on + snap back to the stored distance on `full_out` frame 0 | 0 ms (hidden under the panel) | ui-forge | — | same |
| JUMP_TO | tracker row, Find row, search, toast, ping | van Wijk, `CAM_ARRIVE`, T = clamp(0.62 S, 450, 1,000); S > 1.61 → dip; short pan: `SINE_IO` 300 + 300·s ms | 450–1,000 ms (27–60 f60) | 0 | destination chunks requested at the tap | dip if > 1 doubling |
| FOLLOW_MARCH | "Follow" on a march card | JUMP_TO, then spring t98 600 ms | until a pan or arrival | 0 | chunks ahead of the march (1 ring) | spring t98 300 ms |
| ZOOM_STEP | double-tap in / two-finger tap out | 1 doubling about the tap point, `QUAD_OUT` | 280 ms (17 f60) | 0 | LOD of the next level | kept |
| RUBBER_BAND | release past a limit or floor | `CUBIC_OUT` back to the limit | 240 ms (14 f60) | 0 | — | kept |
| BATTLE_ENTER (auto) | contact while following / on screen | van Wijk, `SINE_IO`, T = clamp(0.41 S, 500, 700) | 500–700 ms (30–42 f60) | 0 (touch cancels) | site data from the march's approach | dip cut |
| BATTLE_ENTER (Watch) | "Watch" on a toast or chip | van Wijk, `CAM_ARRIVE`, T = clamp(0.62 S, 700, 1,000); S > 1.61 → dip; + hover ≤ 1,500 ms | 700–2,500 ms | 0 (touch cancels) | site data + instancing from the tap | dip cut |
| BATTLE_EXIT | battle-forge `release` | van Wijk, `SINE_IO`, T = clamp(0.41 S, 600, 1,000); S > 2.44 → dip | 600–1,000 ms | 0 | site detail unloaded 30 s later | dip cut |
| REALM_FIRST | first zoom-out ever (onboarding-forge) | `SINE_IO` C2 → R_near + yaw 0 → 12° → 0 | 1,800 ms (108 f60) | ceremony | realm ring | dip cut |
| MARCH_OUT, MARCH_OUT_SESSION, MARCH_OUT_FIRST, RETURN_HOME | march events | [castle-enter-exit.md](castle-enter-exit.md) §6–8 | | | | |

## 3. Framing — put a building exactly where the UI leaves room

ui-forge publishes the screen rect not covered by HUD chrome or an open sheet
(`HudLayout.world_rect()`, name to agree with ui-forge; for the building card
it is the top ≈ 30% — ui-forge `screens.md` S1). Framing target: the
building's visual centre (anchor + 40% of its height) at the rect's centre, its
projected height = **45% of the rect's height**.

1. Distance from the size: `d = 1080 · H · cos(p) / (0.5359 · px)` with
   `px = 0.45 × rect height` scaled to 1080 wide; take the pitch from the curve
   at that d and solve once more; clamp to `[d_min, C2 rest]`.
2. Focus from the screen point — exact in one step, because at fixed yaw,
   pitch and distance a focus shift translates the whole image:

```gdscript
# Evaluate at the DESTINATION rig state: set it, compute, restore — same frame, nothing renders between.
func focus_for_screen_point(target: Vector3, px: Vector2) -> Vector3:
	var o := camera.project_ray_origin(px)
	var n := camera.project_ray_normal(px)
	var hit = Plane(Vector3.UP, target.y).intersects_ray(o, n)
	if hit == null:
		return rig.focus
	return rig.focus + (target - hit)      # same height, so the shift stays horizontal
```

3. The **comfort box** for FOCUS_BUILDING is the middle 60% × 50% of the world
   rect: a tapped building already inside it does not move the camera
   (minimal movement: the world stays where the finger left it). Outside it,
   pan only to the nearest box edge — the shortest honest move.

## 4. Shot lists

**FOCUS_BUILDING.** f0: selection rim on (feel-forge / ui-forge), name label in
120 ms, `load_threaded_request` for the card's next-tier render (ART SHOWN BIG,
768 px — ui-forge S1) started on touch-DOWN, 80–150 ms before the tap ends.

**MENU_OPEN (the building card).** f0: framing solve (§3); store `Δfocus` and
`Δlog2 d`. The shot is the master clock (ui-forge `motion.md` §1): the sheet
starts on f0 with its own `sheet_in` 240 ms (the shot is longer than 300 ms),
and accepts input without waiting for the camera; time to interactive
≤ 400 ms. The art must be LOADED when the sheet is 50% in; otherwise
ui-forge's loading state shows (painted frame, shimmer after 200 ms), never a
blank rect. Opened from R/M (tracker): the framing pose is reached by one
`ZoomPath`; S > 1.61 → dip cut, then the sheet.

**MENU_CLOSE.** If the player did not move the camera while the sheet was open,
undo exactly the stored delta (`SINE_IO`, 320 ms, starting with `sheet_out`);
if they did, do nothing. Closed by tapping another building → MENU_NEXT (the
sheet stays, content swaps).

**PANEL_FULL_OPEN / CLOSE** (lords, alliance, research, shop, settings).
1. `button_down` → ui-forge requests the panel; transition-forge does nothing
   before the open.
2. Open: the world pushes in 4% of distance over ui-forge's `full_in`
   (260 ms, `QUART_OUT`: both settle together; peak 0.9 doublings/s). Dims and
   scrims are ui-forge's.
3. When `full_in` ends: `get_viewport().disable_3d = true` and the world root
   `process_mode = PROCESS_MODE_DISABLED` (marches and timers are functions of
   time: nothing is lost); audio-forge ducks the world −9 dB.
4. Close, on frame 0 of `full_out`: `disable_3d = false`, processing on, and
   the distance snaps back to the stored value in the same frame. `full_out`
   is `CUBIC_IN` over 200 ms, so the panel is ≥ 98% opaque for its first 3
   frames: the first visible world frame is fresh and already framed.
5. If turning 3D back on costs > 1 frame on the reference phone (probe),
   keep 3D on and set `Camera3D.cull_mask = 0` while the panel is opaque
   (ui-forge `motion.md` §5 reports this case here).

**JUMP_TO.** f0: request destination chunks. `ZoomPath` (zoom out while
travelling, then in). Lands with `CAM_SETTLE` (1.5%) on a building or castle,
plain `CAM_ARRIVE` on open ground. Longer than the clamp → dip cut: a 3-second
fly across the realm is slower than a cut and makes people ill.

**FOLLOW_MARCH.** Focus springs to the token (t98 600 ms); the token stays at
screen centre ± 5%; zoom unchanged; ends on any pan gesture or at arrival
(then a toast offers the report — report-forge).

**ZOOM_STEP.** Double-tap = 1 doubling in about the tap point (the tapped
ground stays under the finger); two-finger tap = 1 doubling out about the
midpoint. At a floor: a 0.05-doubling bump and back in 180 ms.

**BATTLE_ENTER — the dive, then the handoff.** Battles play where they happened,
in the one world (battle-forge `presentation.md` §1; live-realm ruling).
1. f0: request the battle site (cloud-forge; PROPOSAL p95 ≤ 300 ms) and
   battle-forge's `battle_open_pose(site)` (focus, distance, yaw offset ≤ 15°,
   pitch from the curve). Realm HUD out 150 ms. For the auto variant the
   request starts when the march comes within 10 s of contact.
2. Dive along `ZoomPath`. Site instancing time-sliced (≤ 2 ms per frame).
3. Crossing B2↓ needs the site ready. If not: hover at `B2 × 1.3`, veil at 35%,
   yaw drift 3°/s, ≤ 1,500 ms; still not ready → battle-forge presents at
   region level with tokens (no stall, no spinner).
4. Arrival: `handoff("battle-forge")`. A touch-down during the dive cancels it
   (the battle continues on the map; ui-forge shows a "Watch" chip).

**BATTLE_EXIT.** Return to the pose stored at BATTLE_ENTER f0 (`SINE_IO`);
the site's full detail unloads 30 s later (a re-watch within 30 s reloads
nothing).

**REALM_FIRST (ceremony).** C2 → R_near in 1,800 ms `SINE_IO` (peak 2.9
doublings/s) with a yaw orbit 0 → +12° (900 ms `SINE_IO`) → 0 (900 ms
`SINE_IO`), peak 21°/s: the neighbours slide past the castle in parallax,
which sells "this is a shared world". Veil drift doubled; realm HUD at the B2
commit; `sting_realm_reveal` (audio-forge).

**Two-world cross-fade (SubViewport) — not used in the live game.** Rendering
a second `World3D` in a `SubViewport` (`own_world_3d = true`) and fading its
`SubViewportContainer` over the main view doubles GPU and memory for the fade
and breaks "one world". Allowed only for a future owner-approved ceremony, at
≤ 300 ms (18 f60) `SINE_IO`, with main + second GPU time ≤ 14 ms on every
fade frame (probe), and `disable_3d = true` on the hidden view afterwards.

## 5. Interrupt matrix

| Running ↓ / Event → | Touch-down on world | New UI shot | Level commit | Panel opens | Server event |
|---|---|---|---|---|---|
| AMBIENT (follow, inertia) | stop, finger owns | replace | continue | freeze with world | ignore |
| UI shot | stop, finger owns | replace from current state | continue | finish instantly, then freeze | ignore (except rule 2's battle) |
| CEREMONY | swallowed (first time) | queued after | continue | blocked | queued toast |
| EXTERNAL (battle) | battle-forge UI | refused | continue | battle-forge decides | battle-forge decides |
| Dip cut (covered) | ignored ≤ 250 ms | queued | happens under cover | queued | ignore |

## 6. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Camera fights the finger | shot not killed on touch-down | rule 1, same frame |
| Camera jumps back on a second tap | new shot started from the old shot's start | start from the current rig state (rule 3) |
| Building hidden under the sheet | framed to the screen centre | frame to `world_rect()` (§3) |
| World "jumps" when a card closes | undo applied after the player moved | undo only if the camera was untouched |
| Stale world flashes when a full screen closes | 3D re-enabled late | frame 0 of `full_out`, under ≥ 98% cover |
| Hitch when a full screen closes | `disable_3d` toggle reallocates buffers | fallback `cull_mask = 0` (§4) |
| Camera moves when an ally is attacked | background event drives a shot | rule 2: toast + tap-to-jump |
| Battle dive stops in mid-air | site not ready, no fallback | hover ≤ 1.5 s, then region-level battle |
| Frame spikes during the battle dive | site instanced in one frame | ≤ 2 ms per frame time-slicing |
| Ceremony replays after reinstall | seen-flag stored locally | server-side flag |
| Shake left on after a battle | h/v offset not reset | `release` zeroes `h_offset`, `v_offset` |

## 7. Checklist

- [ ] Every shot in §2 exists in `CameraDirector` with the listed curve, clamp and frames.
- [ ] Touch-down stops AMBIENT/UI shots on the same frame (probe: 0 ms block on repeats).
- [ ] No camera move is triggered by a background event (rule 2's one exception only).
- [ ] Framing uses ui-forge's world rect; building at 45% of its height.
- [ ] Full screens: 3D paused when `full_in` ends, back on `full_out` frame 0.
- [ ] JUMP_TO / BATTLE clamps enforced; long jumps become dip cuts.
- [ ] BATTLE_ENTER has the hover and the region-level fallback; handoff/release tested.
- [ ] Ceremonies ≤ 3.5 s, once per account (server flag), replays skippable.
- [ ] Reduced-motion column implemented for every row.
