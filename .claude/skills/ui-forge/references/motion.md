# Motion — the panel tokens, and who owns which movement

Motion in the UI answers "what changed, and where did it come from?" Then it gets out of the
way. Every duration here is a token: a screen uses the token, never a new number. **PROPOSAL
values**, measured in frames at 60 fps on the reference phone (ship-forge names it).

## 1. Who owns which motion

| Motion | Owner | ui-forge's part |
|---|---|---|
| Control tweens: panels, sheets, drawers, modals, toasts, rows, badges, bars, counts | **ui-forge** (this file) | — |
| Camera3D moves: castle ⇄ realm zoom, focus on a building, march-out, entering a battle view | transition-forge | the panel starts on the shot's clock |
| The HUD mode flip at B2, world layers by zoom level | transition-forge (`level_changed`) | the 150 ms crossfade of the elements that differ (hud.md §4) |
| Ceremonies: tier-up, victory, claim bursts, the swearing | feel-forge (≤ 1.5 s, skippable after 300 ms, core-loop A9) | the surface the ceremony lands on, and the input rule |
| Battle presentation | battle-forge | — |
| Sounds and haptics | audio-forge | the cue moments (§6) |

**When a panel opens together with a camera move** (the building card: the camera frames the
building in the top 30% while the sheet rises), the transition-forge shot is the master clock.
The sheet starts on the shot's first frame and uses the shot's duration if it lies within
200–300 ms, otherwise its own 240 ms. The panel never waits for the camera to finish before it
accepts input.

## 2. The tokens

"Frames" = at 60 fps. Godot: `create_tween().set_trans(T).set_ease(E)`.

| Token | Motion | ms | Frames | Trans / ease | Notes |
|---|---|---|---|---|---|
| `press` | button scale 1 → 0.96 | 50 | 3 | QUAD / OUT | the pressed texture swaps at frame 0 |
| `release` | 0.96 → 1.0 | 90 | 5 | BACK / OUT | overshoot ≤ 1.02 |
| `sheet_in` | sheet rises from the bottom | 240 | 14 | CUBIC / OUT | scaled by the distance left (§3.3) |
| `sheet_out` | sheet falls | 180 | 11 | CUBIC / IN | |
| `snap` | drag release to a snap height | 200 | 12 | CUBIC / OUT | fling ≥ 1800 px/s picks the direction (as chat-forge) |
| `full_in` | full screen rises 154 px (8%) + fades in | 260 | 16 | QUART / OUT | the 3D world pauses at the end (§5) |
| `full_out` | full screen fades out + drops 154 px | 200 | 12 | CUBIC / IN | the world resumes on the first frame |
| `drawer_in` / `drawer_out` | tracker drawer from the hand-side edge | 200 / 160 | 12 / 10 | CUBIC / OUT, IN | |
| `modal_in` | scale 0.94 → 1 + fade; scrim 0 → 60% over 150 ms | 180 | 11 | BACK / OUT | overshoot ≤ 1.01 |
| `modal_out` | fade + scale 1 → 0.98 | 120 | 7 | CUBIC / IN | |
| `toast_in` / `toast_out` | drop 24 px + fade / rise 16 px + fade | 200 / 160 | 12 / 10 | QUART / OUT, CUBIC / IN | |
| `tab` | content crossfade | 140 | 8 | SINE / IN_OUT | no slide |
| `stagger` | rows appear: each 160 ms, +30 ms per row, first 8 rows only | ≤ 400 total | ≤ 24 | QUART / OUT | the rest appear at once |
| `count` | number count-up | 800 | 48 | QUART / OUT | core-loop A1 |
| `bar` | progress fill change | 300 | 18 | CUBIC / OUT | |
| `badge` | dot or pill appears | 200 | 12 | BACK / OUT | never loops |
| `bubble_new` | a new bubble: scale 0.6 → 1 + fade | 180 | 11 | CUBIC / OUT | |
| `bubble_level` | bubbles at a zoom-level change: in / out | 150 / 120 | 9 / 7 | linear | transition-forge zoom-model §6 |
| `hud_mode` | elements that differ between castle and realm | 150 | 9 | linear | on `level_changed` at B2 |
| `batch_tab` | a batch tab slides out of its chip | 200 | 12 | CUBIC / OUT | |
| `shake` | invalid input: 3 cycles of ±12 px | 240 | 14 | SINE / IN_OUT | replaced in reduced motion |
| `pointer` | the guide pointer's press loop | 1200 loop | 72 | SINE / IN_OUT | the ONLY loop in the UI |

Plain-word easing names map to Godot as "ease-out cubic" = `TRANS_CUBIC` + `EASE_OUT`,
"ease-in-out sine" = `TRANS_SINE` + `EASE_IN_OUT`, and so on. Specs use the plain name, the
code uses the constants.

## 3. Interaction rules

1. **Input is never blocked by a UI tween.** A panel's controls take taps from its first
   frame. Code never does `await tween.finished` before enabling input. The only input hold
   in the game is feel-forge's ≤ 300 ms at the start of a ceremony (core-loop A9).
2. **Every tween can be interrupted.** A tap on close during `sheet_in` kills the tween and
   starts `sheet_out` from the current position (godot.md §5). Tweens are never queued
   behind each other.
3. **Distance-proportional time**: an interrupted move takes `token × distance left ÷ full
   distance`, minimum 60 ms. A reversal right after the start is short, not a full 180 ms.
4. **At most 2 motion groups at once** (e.g. a toast + a count-up). A third waits ≤ 200 ms or
   starts without its motion.
5. **Claim sequence**: server ack → the resource count-up starts (`count`) → a toast on the
   same frame → feel-forge's burst if any. The sound and the haptic fire on the ack, not on
   the tap, so the game never cheers for a claim the server refused.
6. **No motion during a camera move** except the HUD crossfade and the bubbles. Toasts that
   arrive during a zoom wait until it ends (≤ 700 ms).

## 4. Reduced motion (Settings → Accessibility)

| Normal | Reduced |
|---|---|
| every slide and scale | a 120 ms linear opacity fade |
| `stagger` | off: all rows at once |
| `count` | the value is set; the label fades 120 ms |
| `shake` | a 2 px WAX border on the field for 1 s, no movement, no flash |
| `pointer` loop | static pointer |
| `bubble_new` | fade only |
| `release` overshoot | none |
| transition-forge veil drift, camera moves | transition-forge's own reduced-motion rules |

Always, in both modes: nothing flashes more than 3 times per second (WCAG 2.3.1); offers
never pulse (monetization.md §5.3); the HUD has no loop except the pointer. Progress rings
move with time, which is not a loop.

## 5. Frame time and first-open cost

| Budget (PROPOSAL; ship-forge owns the device list) | Target | Measured by |
|---|---|---|
| A frame during any UI tween | ≤ 16.7 ms (60 fps), ≤ 33.3 ms in the 30 fps setting | qa.md §4 frame-time capture |
| First open of a surface in a session | ≤ 1 hitch frame ≤ 33 ms | same, per route |
| Warm open (second time) | 0 hitch frames | same |
| UI script time at HUD rest | ≤ 1.0 ms per frame | Godot profiler |

How to meet it:
1. **Pre-instance the 6 most used surfaces** at boot, hidden: building card, tracker drawer,
   resource sheet, speed-up picker, chronicle, toast. They cost memory, not frames.
2. **Others load ahead of the tap**: on `button_down`, call
   `ResourceLoader.load_threaded_request(path)`. A tap lasts ≈ 80–150 ms from press to
   release, so the scene is usually ready at `pressed`. Instance on release.
3. **Keep closed surfaces warm** in an LRU of 4 and free one 30 s after close.
4. **Full screens pause the world**: after `full_in` ends, set `get_viewport().disable_3d =
   true` (or transition-forge's equivalent). Restore it on the first frame of `full_out`. Check
   with the profiler that the toggle itself causes no hitch. If it does, keep 3D on and
   report it to transition-forge.
5. **Animate cheap properties**: `position`, `modulate`, `scale` (with `pivot_offset` set).
   Never animate a Container's `size`, a font size or `custom_minimum_size` inside a list:
   each one relayouts or reshapes text on every frame.

## 6. Cue moments (audio-forge makes the sounds)

| Moment | When | Haptic (if on) |
|---|---|---|
| Tap | press-down, ≤ 50 ms latency | none |
| Sheet or full screen opens | frame 0 of the tween; the sound is not longer than the tween | none |
| Commit (Upgrade, Send, Heal all) | server ack | 10 ms |
| Claim | server ack (§3.5) | 10 ms |
| Error state appears | its first frame | 20 ms |
| Social toast ("Allies saved you 42 m") | its first frame | none |
| Toggle | on change | 10 ms |

`Input.vibrate_handheld(10)` for the 10 ms tick. Haptics default ON for commits and claims
only.

## 7. Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| Input waits for a tween to finish | "the game is slow" on every panel | [ ] `ux_flow_probe` taps at frame 2 of each open |
| Tweens queue up | a double tap opens and closes, then reopens | [ ] the interruption test (godot.md §5) |
| A panel waits for the camera | a 700 ms dead period | [ ] frame capture of the building-card open |
| A new duration invented per screen | the UI feels uneven | [ ] grep for tween durations outside the token table |
| Size or font-size animated | a hitch on mid phones | [ ] profiler during the open |
| Reduced motion still slides | vestibular discomfort | [ ] `a11y_audit` with the setting on |
| An offer countdown pulses | money-law breach | [ ] `ux_flow_probe` capture |

- [ ] Every tween uses a token from §2; durations scale with the distance left.
- [ ] No input lock; a reversal works from any frame.
- [ ] Camera-linked opens follow the transition-forge clock.
- [ ] Reduced motion replaces every slide, scale, stagger, shake and loop.
- [ ] First-open and warm-open frame times recorded for every changed route.
- [ ] Cues fire on the server ack for commits and claims.
