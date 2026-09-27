# QA — the transition probe, the frame-by-frame review, the verdicts

The genre's reference title reviewed its zoom frame by frame (research §6).
We do the same, with numbers: every transition is measured in real time on
the device (frame times, comfort, input block) and reviewed frame by frame
from a fixed-step recording (pops, sync, cause before effect). "Feels smooth"
is not a verdict; the lines below are.

## 1. What "done" means for a transition

A transition change is done when all five are pasted into the ledger row:
1. `TRANSITION PROBE …` line from the device or windowed run (§2).
2. `TRANSITION REPORT OK …` from the analyser over that CSV (§3).
3. `POP CHECK OK …` for each changed shot, full and reduced motion (§5).
4. The contact sheet, opened and checked against the 12 points (§5).
5. For gate or prop clips: the blender-forge round-trip `anims=[…]` line and
   the build QA prints ([castle-enter-exit.md](castle-enter-exit.md) §4.8).

## 2. The transition probe (qa-forge installs it; paths to confirm)

A scene run windowed — like the owner's `session_audit` — so autoloads and
rendering behave exactly as in the game:
`& $g --path godot --resolution 1080x1920 res://tests/transition_probe.tscn`.
It boots the real game scene, plays every shot `CameraDirector.probe_ids()`
returns five times (run 1 = cold, first appearance after boot; runs 2–5 =
warm), records every frame, writes a CSV and prints a verdict.

```gdscript
# res://tests/transition_probe.gd on the root Node of transition_probe.tscn
extends Node

const RUNS := 5
const TAIL_US := 500_000                      # keep recording 500 ms after a shot ends
const MAX_FRAMES := 900                       # 15 s guard per run
const TARGET_MS := 1000.0 / 60.0
const OUT := "user://transition_probe.csv"
var _rows := PackedStringArray()
var _stalls := 0
var _block_repeat_ms := 0.0

func _ready() -> void:
	var main := (load("res://main.tscn") as PackedScene).instantiate()   # the game's entry scene (path to confirm)
	add_child(main)
	_run.call_deferred()

func _run() -> void:
	for i in 180:                              # boot and idle-time streaming settle
		await get_tree().process_frame
	var cd: Node = get_node("/root/CameraDirector")                    # autoload name to confirm
	var vp := get_viewport().get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(vp, true)
	_rows.append("id,run,repeat,frame,t_ms,dt_ms,cpu_ms,gpu_ms,draws,focus_x,focus_z,yaw,pitch,dist,fov,roll,level,input_blocked,moving,spec_ms")
	var ids: PackedStringArray = cd.probe_ids()
	for id in ids:
		for run in range(1, RUNS + 1):
			await _record(cd, vp, id, run)
			cd.probe_reset()
			for i in 30:
				await get_tree().process_frame
	var fa := FileAccess.open(OUT, FileAccess.WRITE)
	fa.store_string("\n".join(_rows) + "\n")
	fa.close()
	var ok := _stalls == 0 and _block_repeat_ms <= 400.0
	print("TRANSITION PROBE %s - %d shots x %d runs, %d stalls, max repeat block %d ms -> %s" % [
		"OK" if ok else "FAIL", ids.size(), RUNS, _stalls, int(_block_repeat_ms),
		ProjectSettings.globalize_path(OUT)])
	get_tree().quit(0 if ok else 1)

func _record(cd: Node, vp: RID, id: String, run: int) -> void:
	var info: Dictionary = cd.probe_play(id)
	var cam := get_viewport().get_camera_3d()
	var t0 := Time.get_ticks_usec()
	var last := t0
	var end_us := -1
	var block := 0.0
	for f in MAX_FRAMES:
		await get_tree().process_frame
		var now := Time.get_ticks_usec()
		var dt := (now - last) / 1000.0
		var moving: bool = cd.is_shot_running()
		if not moving and end_us < 0:
			end_us = now
		if dt >= 2.0 * TARGET_MS + 2.0:
			_stalls += 1
		block = block + dt if cd.input_blocked else 0.0
		if info.repeat:
			_block_repeat_ms = maxf(_block_repeat_ms, block)
		var st: Dictionary = cd.rig_state()
		var roll := rad_to_deg(asin(clampf(cam.global_transform.basis.x.y, -1.0, 1.0)))
		_rows.append(",".join(PackedStringArray([id, str(run), str(int(info.repeat)), str(f),
			"%.3f" % ((now - t0) / 1000.0), "%.3f" % dt,
			"%.3f" % (Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0),
			"%.3f" % RenderingServer.viewport_get_measured_render_time_gpu(vp),
			str(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)),
			"%.3f" % st.focus.x, "%.3f" % st.focus.z, "%.4f" % st.yaw, "%.4f" % st.pitch,
			"%.4f" % st.distance, "%.3f" % st.fov, "%.5f" % roll, str(st.level),
			str(int(cd.input_blocked)), str(int(moving)), "%.1f" % info.spec_ms])))
		last = now
		if end_us >= 0 and now - end_us >= TAIL_US:
			break
```

**The probe contract** — `CameraDirector` must provide `probe_ids()`,
`probe_play(id) -> {spec_ms, repeat}`, `probe_reset()`, `is_shot_running()`,
`rig_state()` and `input_blocked` ([shot-library.md](shot-library.md) §1).
`probe_play` plays the shot exactly as the game does (same streaming, same
curves), with `repeat = true` for every shot except first-time ceremonies.

**On the device**: dev builds carry the same recorder behind a debug toggle; it
writes `user://transition_probe.csv` during real play (every shot the player
triggers). Pull it with `adb pull` (Android `user://` path to confirm with
ship-forge), then run the analyser. The windowed PC run finds logic faults;
only the reference phone proves frame times.

CSV columns: `id, run, repeat, frame, t_ms, dt_ms, cpu_ms, gpu_ms, draws,
focus_x, focus_z, yaw, pitch, dist, fov, roll, level, input_blocked, moving,
spec_ms`.

## 3. The analyser — `tools/transition_report.py`

```
py tools/transition_report.py report transition_probe.csv [--fps 60] [--hfov 30]
py tools/transition_report.py pops   art/transitions/CASTLE_LEAVE/ [--allow 40-46]
py tools/transition_report.py sheet  art/transitions/CASTLE_LEAVE/ --out sheet.png --every 3
py tools/transition_report.py selftest
```

`report` prints a table per (shot, run) — duration vs spec, max and p95 frame
time, dropped frames, stalls, GPU ms, zoom rate (doublings/s), pan rate
(screen widths/s), view rotation (°/s), roll, input block, distance overshoot —
one `FAULT <id> run <n>: …` line per breach, and one verdict:
`TRANSITION REPORT OK - 16 shots x 5 runs, 0 stalls, 0 comfort faults, max block 0 ms`
or `TRANSITION REPORT FAIL - <n> faults …` (exit code 1). Kinematics use
central differences over moving frames, so frame-time jitter does not fake a
speed spike. `selftest` builds a good 700 ms CASTLE_LEAVE (measured zoom peak
7.36 doublings/s, analytic 7.36), a bad shot and a popping sequence, and
proves every check fires: run it after editing the tool.

## 4. Pass thresholds (the tool's `LIMITS`, mirrored from [easing.md](easing.md) §4)

| Metric | Warm (runs 2–5) | Cold (run 1) | Why |
|---|---|---|---|
| Stalls: frame ≥ 2 × target + 2 ms (35.3 ms at 60 fps) | **0** | **0** | a whole refresh lost is a visible hitch |
| Dropped: frame ≥ 1.5 × target (25 ms) | ≤ 1 per shot | ≤ 2 per shot | one late vsync is tolerable, two in a row is not |
| p95 frame time | ≤ 17.5 ms | ≤ 17.5 ms | steady 60 fps |
| GPU time, heaviest frame | ≤ 12 ms (PROPOSAL) | ≤ 12 ms | headroom for thermals |
| Zoom / pan / rotation peaks | 8 dbl/s · 3 SW/s · 60°/s | same | comfort |
| Roll | < 0.01° | same | the rig has no roll |
| Input block, repeat actions | 0 ms expected; **> 400 ms fails** | same | owner rule |
| Input block, first-time ceremony | ≤ 3,500 ms | same | once per account |
| Distance overshoot | ≤ 1.5% | same | `CAM_SETTLE` only |
| Duration vs spec | ± max(1 frame, 3%) | same | the spec is the design |

At the 30 fps battery setting every frame-time number doubles. The first run
after boot IS what players see every session: cold failures are real failures.

## 5. Frame-by-frame review (fixed-step recording)

Godot's Movie Maker renders at a fixed step, so the recording shows the
intended motion on any machine (it does not measure performance — §2 does):

```
& $g --path godot --resolution 1080x1920 --write-movie art/transitions/CASTLE_LEAVE/f.png --fixed-fps 60 res://tests/transition_rec.tscn -- CASTLE_LEAVE
```

`transition_rec.tscn` (qa-forge) plays the shot id from
`OS.get_cmdline_user_args()` once and quits. The PNG sequence comes with a
WAV of the same base name: the cue frames can be checked against the picture.
Record every changed shot twice: full motion and reduced motion.

1. `pops` over the sequence → `POP CHECK OK - 0 pops in N frames`. Planned
   cuts (dip frames) are passed with `--allow a-b`; anything else flagged is a
   LOD pop, a late stream, a stale frame or a missing fade.
2. `sheet --every 3` → open the contact sheet; step single frames around every
   event (commit, swap, passable, arrival).
3. Check all 12:

| # | Check | Pass |
|---|---|---|
| 1 | Sky or horizon | never visible, tallest aspect shape included |
| 2 | Roll | ground plane level; towers lean symmetrically (3-point perspective only) |
| 3 | Subject | inside the central 80% × 70% of the frame on every frame of the move |
| 4 | Speed profile | no jerk at the start (except `QUAD_OUT` tap responses); the last 30% decelerates; ≤ 1 overshoot ≤ 1.5% |
| 5 | Pops | none outside `--allow` ranges |
| 6 | Veil and swap | veil peak on the commit frame ±2; the town swap invisible at 100% crop |
| 7 | HUD | mode flips on the commit frame ±1 with ui-forge's 150 ms crossfade |
| 8 | UI during camera moves | nothing slides in (ui-forge `motion.md` rule 6) |
| 9 | Shadows | no jump or swim across the level steps |
| 10 | Gate | unbar before swing; wheel turns before the grid rises; squad crosses at passable, teeth ≥ 0.2 m above the banner; WAV cue peaks ±1 frame of castle-enter-exit §4.9 |
| 11 | Arrival | the subject can be named 150 ms after the move ends |
| 12 | Reduced motion | the variant passes 1–11 (dip frames allowed) |

## 6. When to run what

| Change | Run |
|---|---|
| Any `CameraDirector`, curve, clamp or shot change | probe (windowed) + report + frame review of the changed shots |
| Zoom thresholds, pitch curve, lens | probe + review of CASTLE_LEAVE / ENTER / ZOOM_STEP + `w1f_aspect_sweep` (horizon on 6 shapes) |
| Streaming, HLOD, visibility ranges, new assets on the map | probe on the reference phone (cold + warm) |
| Gate or prop clip | blender-forge round trip + §4.8 prints + frame review of MARCH_OUT_SESSION |
| HUD mode or panel timing (ui-forge) | review #7 and #8 on CASTLE_LEAVE and MENU_OPEN |
| Before a release | everything above on the reference phone |

PROPOSAL to game-director: add `transition_probe` to the windowed suites of
the core gate whenever camera, streaming or HUD-mode code changed.

## 7. Failure modes of the measurement itself

| Symptom | Cause | Fix |
|---|---|---|
| Probe passes on PC, stutters on the phone | desktop GPU hides the cost | only the reference-phone run proves frame times |
| Movie Maker frames look perfect, device hitches | fixed-step recording ignores time | recordings for motion, the probe for timing |
| Speed spikes on frames with jitter | per-frame differences | central differences (the tool) |
| Cold hitch never seen | probe ran shots only warm | run 1 is cold by design; never pre-warm in the probe |
| "0 ms block" but the player cannot tap | `input_blocked` not set by the UI layer | the flag covers every layer that swallows input |
| A pop flagged on a planned cut | dip frames not allowed | `--allow` the dip frame range |
| GPU column always 0 | measurement not enabled | `viewport_set_measure_render_time(vp, true)` |

## 8. Checklist

- [ ] Probe installed (qa-forge); `CameraDirector` implements the probe contract.
- [ ] CSV analysed; `TRANSITION REPORT OK` pasted with the table.
- [ ] Cold run passes (0 stalls, ≤ 2 dropped per shot).
- [ ] Every changed shot recorded full + reduced motion; `POP CHECK OK` pasted.
- [ ] Contact sheet opened; the 12 checks written down with frame numbers.
- [ ] Reference-phone run before release; numbers in the ledger.
- [ ] `tools/transition_report.py selftest` prints `SELFTEST PASS` after any tool edit.
