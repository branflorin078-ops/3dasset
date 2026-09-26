# Easing — named curves, comfort caps, springs and paths

"Smooth" is not a spec. Every motion in this skill names one curve from §1,
one duration in ms and 60 fps frames, and passes the comfort caps in §4. The
same Penner curve names exist in Godot's `Tween` and in Blender's keyframe
interpolation, so a gate clip and a camera move speak one vocabulary.

## 1. The house curves

`peak` = highest speed as a multiple of the average speed (distance ÷ time);
`t90` / `t99` = fraction of the duration at which 90% / 99% of the move is
done (measured numerically). The peak factor is what the comfort check uses.

| Name | Definition | Godot | Blender key | peak | at | t90 | t99 | Use | Never |
|---|---|---|---|---|---|---|---|---|---|
| `LINEAR` | `t` | `TRANS_LINEAR` | `'LINEAR'` | 1.00 | — | 0.90 | 0.99 | constant-speed follow, the braked portcullis run | any start or stop |
| `SINE_IO` | `−(cos πt − 1)/2` | `TRANS_SINE`, `EASE_IN_OUT` | `'SINE'`, `'EASE_IN_OUT'` | 1.57 | 0.50 | 0.80 | 0.94 | big log-space zooms, van Wijk jumps, settle-backs, crossfades, heavy doors | — |
| `SINE_IN` / `SINE_OUT` | quarter sine | `TRANS_SINE`, `EASE_IN` / `EASE_OUT` | `'SINE'` | 1.57 | end / start | 0.94 / 0.71 | 0.99 / 0.91 | dip in / dip out | — |
| `QUAD_OUT` | `1 − (1 − t)²` | `TRANS_QUAD`, `EASE_OUT` | `'QUAD'`, `'EASE_OUT'` | 2.00 | 0.00 | 0.68 | 0.90 | tap responses: moves on the next frame (focus pan, zoom step, cold-open dolly) | moves > 1 doubling |
| `QUAD_IN` | `t²` | `TRANS_QUAD`, `EASE_IN` | `'QUAD'`, `'EASE_IN'` | 2.00 | 1.00 | 0.95 | 0.99 | gravity (`s = ½at²` is exactly quadratic): falls, slams, impacts | camera |
| `CUBIC_OUT` | `1 − (1 − t)³` | `TRANS_CUBIC`, `EASE_OUT` | `'CUBIC'`, `'EASE_OUT'` | 3.00 | 0.00 | 0.54 | 0.78 | rubber-band return (small distances) | camera moves > 0.25 screen |
| `CUBIC_IO` | Penner | `TRANS_CUBIC`, `EASE_IN_OUT` | `'CUBIC'`, `'EASE_IN_OUT'` | 3.00 | 0.50 | 0.71 | 0.86 | UI only (ui-forge) | zooms (3× peak) |
| `CAM_ARRIVE` | CSS `cubic-bezier(0.35, 0, 0.25, 1)` | code (§2) | Bézier handles or sample | 2.43 | 0.29 | 0.65 | 0.88 | jump-to, focus + zoom, the battle dive: gentle start, early peak, long readable arrival | — |
| `CAM_SETTLE` | back-out, `s = 0.65` → **1.49% overshoot** | code (§2) | `'BACK'`, `keyframe.back = 0.65` | — | — | — | — | the one allowed camera overshoot (focus arrival, full motion only) | reduced motion |
| `EXPO_OUT` | `1 − 2^(−10t)` | `TRANS_EXPO` | `'EXPO'` | 6.93 | 0.00 | 0.33 | 0.66 | UI flashes | **camera** (7× jerk; Penner form also jumps 0.1% at t = 1) |
| `CIRC_OUT` | `√(1 − (t − 1)²)` | `TRANS_CIRC` | `'CIRC'` | ∞ | 0.00 | 0.56 | 0.86 | — | **anything**: infinite start speed |
| `BACK_OUT` (Godot) | fixed `s = 1.70158` | `TRANS_BACK` | `'BACK'` default | 4.70 | 0.00 | 0.30 | 0.36 | UI pops (ui-forge) | **camera**: 10% overshoot |
| `SPRING_CRIT` | critically damped spring (§8) | code | — | — | — | — | 98% at `t98` | follow cam, retargets, anything that can be interrupted | — |
| `DECAY` | `v·e^(−t/τ)` | code | — | — | — | — | — | pan / zoom inertia after a fling | authored shots |

## 2. Godot 4 patterns

**A committed shot** is one `Tween` driving a progress value; the shot maps
progress to rig state (so pitch stays a function of distance and distance
stays in log space):

```gdscript
var _tween: Tween

func run_shot(shot: CamShot) -> void:
	if _tween and _tween.is_valid():
		_tween.kill()                        # an interrupted shot stops dead; the finger takes over
	_tween = create_tween()
	_tween.set_process_mode(Tween.TWEEN_PROCESS_IDLE)   # rig moves in _process, never physics
	_tween.tween_method(_apply.bind(shot), 0.0, 1.0, shot.duration_s) \
		.set_trans(Tween.TRANS_LINEAR)       # progress stays linear; the shot applies its named curve
	_tween.finished.connect(_on_shot_finished.bind(shot))

func _apply(p: float, shot: CamShot) -> void:
	var e := shot.ease(p)                    # SINE_IO, CAM_ARRIVE, QUAD_OUT ... (below)
	var w := shot.path.at(e)                 # ZoomPath (§6): x, z, visible width
	rig.set_state(Vector3(w.x, 0.0, w.y), w.z / VIEW_K)   # VIEW_K = 2·tan(15°) = 0.5359
```

Penner curves inside `shot.ease()`: `Tween.interpolate_value(0.0, 1.0, p, 1.0,
Tween.TRANS_SINE, Tween.EASE_IN_OUT)`. Custom curves:

```gdscript
static func cubic_bezier(t: float, x1: float, y1: float, x2: float, y2: float) -> float:
	# CSS cubic-bezier: solve x(u) = t by bisection (16 steps, error < 2e-5), return y(u)
	var lo := 0.0
	var hi := 1.0
	var u := t
	for i in 16:
		u = (lo + hi) * 0.5
		var x := 3.0 * (1.0 - u) * (1.0 - u) * u * x1 + 3.0 * (1.0 - u) * u * u * x2 + u * u * u
		if x < t:
			lo = u
		else:
			hi = u
	return 3.0 * (1.0 - u) * (1.0 - u) * u * y1 + 3.0 * (1.0 - u) * u * u * y2 + u * u * u

static func cam_arrive(t: float) -> float:
	return cubic_bezier(t, 0.35, 0.0, 0.25, 1.0)

static func cam_settle(t: float, s := 0.65) -> float:
	var q := t - 1.0
	return 1.0 + (s + 1.0) * q * q * q + s * q * q
```

Several channels with different curves (camera + veil + HUD) run in one
`create_tween().set_parallel(true)`; never stack two tweens on one property.

## 3. Blender mapping (prop clips)

Per key: `kp.interpolation = 'SINE'`, `kp.easing = 'EASE_IN_OUT'`; the pair
applies from that key to the next. `'BACK'` takes `kp.back` (0.65 → 1.5%
overshoot). With `export_force_sampling=True` the curve is sampled at 30 fps
into the GLB; Godot interpolates linearly between samples at display rate.
Holds are `'CONSTANT'`. Author clips as tables of keys
([castle-enter-exit.md](castle-enter-exit.md) §4.4), never by hand-dragging
handles: tables can be reviewed and re-derived.

## 4. Comfort caps (automated camera motion)

Player-driven motion (pinch, pan, fling) is exempt: the hand predicts it.

| Quantity | Cap | Measured as |
|---|---|---|
| Zoom rate | **peak ≤ 8 doublings/s**, average ≤ 5 | `|Δ log2 distance| / Δt` |
| Pan (ground flow at screen centre) | **peak ≤ 3 screen widths/s** | focus step ÷ visible width ÷ Δt |
| View rotation (yaw + pitch) | **peak ≤ 60°/s** | angle between view directions ÷ Δt |
| Yaw offset from house yaw | ≤ 15°, back to 0 before control returns | — |
| Pitch | 45–72° gameplay, 42° floor in authored shots | [zoom-model.md](zoom-model.md) §2 |
| Pitch slope vs distance | ≤ 6° per doubling | pitch curve |
| Roll | **0.00°** (the rig has no roll axis) | probe asserts < 0.01° |
| FOV | constant 30° in gameplay; authored ±4° at ≤ 8°/s | — |
| Overshoot | ≤ 1.5% of the move (log space for distance), one only | `CAM_SETTLE` |
| Start speed | only `QUAD_OUT` tap responses start at speed (2× average) | — |
| Screen shake | 0 in every transition (battle-forge / feel-forge own shake) | — |

**Check a shot on paper before building it**: `peak = peak_factor × total / T`.
Minimum duration for a cap: `T ≥ peak_factor × total / cap`.

| Move | Total | Curve | Min T | Chosen |
|---|---|---|---|---|
| C2 rest → R_near | 3.28 doublings | `SINE_IO` | 644 ms | 700 ms → 7.4 dbl/s |
| `d_min` → R_near | 4.98 doublings | `SINE_IO` | 978 ms | 1,000 ms → 7.8 dbl/s |
| Zoom step (double-tap) | 1.00 doubling | `QUAD_OUT` | 250 ms | 280 ms → 7.1 dbl/s |
| Focus pan 0.6 screen widths | 0.60 SW | `QUAD_OUT` | 400 ms | 540 ms → 2.2 SW/s |
| Pitch 50° → 60° inside a 700 ms zoom | 10° | follows distance | — | peak 28°/s |

The analyser checks the same caps from the probe CSV
([qa.md](qa.md) §3, `tools/transition_report.py`).

## 5. Anticipation, overshoot, settle — camera vs props

| | Anticipation | Action | Overshoot | Settle |
|---|---|---|---|---|
| Camera (full motion) | none — a camera that backs up before moving reads as lag | `SINE_IO` / `CAM_ARRIVE` | ≤ 1.5%, only on focus arrivals | inside the curve (t90 → t99 is the settle) |
| Heavy prop (gate leaves, portcullis) | 3–4 f30 jolt + 3 f30 hold (the crew takes the weight) | `SINE_IO`, 24 f30 swing | 3° / 6 cm | 4–6 f30 |
| Light prop (palisade leaf, shutter) | 3 f30 | `QUAD_OUT`, 18 f30 | 6° | 5 f30 |
| Impact (slam, drop) | — | `QUAD_IN` (gravity) | rebound 1.5–3° or 5 cm, then 1 cm | 2–5 f30 |
| UI panels | ui-forge motion.md | | | |

The camera arrives into action: start a prop's clip before the camera settles
(MARCH_OUT_FIRST starts the gate at 350 ms of a 700 ms move), so the eye lands
on motion, not on a still.

## 6. Paths — log space and the van Wijk zoom-pan

Pure zoom: `d(t) = d0 · (d1/d0)^e(t)`. Pan + zoom: the van Wijk & Nuij (2003)
optimal path (zoom out while travelling, then in) — the perceived speed is
constant along it. Port of d3-interpolate's `interpolateZoom`:

```gdscript
class_name ZoomPath extends RefCounted
# Points are Vector3(x, z, w): focus on the ground plane, visible ground width w = 2·d·tan(hfov/2).
const RHO := 1.41421356      # sqrt(2); the paper's users preferred about 1.42
var p0: Vector3
var dx: float
var dz: float
var d1: float
var r0: float
var S: float                 # path length; RHO·|S| = e-folds of zoom on a pure zoom

func _init(a: Vector3, b: Vector3) -> void:
	p0 = a
	dx = b.x - a.x
	dz = b.y - a.y
	var d2 := dx * dx + dz * dz
	d1 = sqrt(d2)
	if d2 < 1e-6:
		S = log(b.z / a.z) / RHO                  # signed: negative = zoom in
		return
	var r2 := RHO * RHO
	var b0 := (b.z * b.z - a.z * a.z + r2 * r2 * d2) / (2.0 * a.z * r2 * d1)
	var b1 := (b.z * b.z - a.z * a.z - r2 * r2 * d2) / (2.0 * b.z * r2 * d1)
	r0 = log(sqrt(b0 * b0 + 1.0) - b0)
	S = (log(sqrt(b1 * b1 + 1.0) - b1) - r0) / RHO

func length() -> float:
	return absf(S)

func at(t: float) -> Vector3:
	if d1 < 1e-3:
		return Vector3(p0.x + t * dx, p0.y + t * dz, p0.z * exp(RHO * t * S))
	var s := t * S
	var u := p0.z / (RHO * RHO * d1) * (cosh(r0) * tanh(RHO * s + r0) - sinh(r0))
	return Vector3(p0.x + u * dx, p0.y + u * dz, p0.z * cosh(r0) / cosh(RHO * s + r0))
```

Verified: `at(0)` and `at(1)` return the end points exactly; a 1-screen-width
pan has `S = 1.25` and zooms out to 1.41× at mid-path.

**Duration from path length** (cap: 8 doublings/s = 5.55 e-folds/s):
`T ≥ RHO × peak_factor × S / 5.55` → **`T = 0.41 × S` with `SINE_IO`**,
**`T = 0.62 × S` with `CAM_ARRIVE`**, clamped per shot
([shot-library.md](shot-library.md)). A path too long for the clamp becomes a
dip cut (§7) — never a longer fly, never a faster one.

## 7. Reduced motion (Settings → "Reduce camera motion")

Godot 4 has no API for the phone's system reduce-motion flag; ship-forge may
read Android's `ANIMATOR_DURATION_SCALE` through a plugin (PROPOSAL); the
in-game toggle is the source of truth.

| Full motion | Reduced motion |
|---|---|
| Any move > 1 doubling or > 0.5 screen widths | **dip cut**: ColorRect (PARCHMENT #E8D9B5) on a CanvasLayer above the HUD, 0 → 100% in 100 ms (6 f60) `SINE_IN`, camera jumps and levels commit on the covered frame, 100% → 0 in 140 ms (8 f60) `SINE_OUT` — **250 ms (15 f60)** total. If the destination is not ready, hold covered ≤ 500 ms. |
| Short pans and zooms (≤ 1 doubling, ≤ 0.5 SW) | kept, `SINE_IO`, duration × 0.8 |
| `CAM_SETTLE` overshoot, push-ins, yaw offsets | removed |
| Veil drift | 0 (opacity still follows distance) |
| Pinch, pan, fling | unchanged (player-driven) |
| Prop clips (gate) | unchanged (object motion, not camera motion) |

## 8. The critically damped spring (follow, retarget)

Tweens cannot keep velocity when the target moves; a follow cam or a shot
retargeted mid-way uses a spring. Frame-rate independent form (Game
Programming Gems 4, "Critically Damped Ease-In/Ease-Out Smoothing"):

```gdscript
# returns Vector2(new_value, new_velocity); t98 = time to 98% ≈ 2.92 × smooth_time
static func smooth_damp(cur: float, target: float, vel: float, smooth_time: float, dt: float) -> Vector2:
	var omega := 2.0 / smooth_time
	var x := omega * dt
	var k := 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
	var change := cur - target
	var temp := (vel + omega * change) * dt
	return Vector2(target + (change + temp) * k, (vel - omega * temp) * k)
```

Settle times (98%): follow a march 600 ms (`smooth_time` 0.205 s); rig
retarget after a UI change 400 ms (0.137 s). Apply per axis of the focus, and
to log2(distance) — never to raw metres. Clamp the `dt` fed to the camera to
33 ms: one 100 ms hitch then slows the move instead of jumping it 6 frames
(the probe logs every clamp).

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Zoom-out crawls, zoom-in slams | metres interpolated linearly | log space (§6) |
| Arrival feels like a stop sign | `CUBIC_IO` or `EXPO_OUT` on a zoom | `SINE_IO` / `CAM_ARRIVE`, check peak (§4) |
| Camera wobbles after arriving | `TRANS_BACK` (10%) on the camera | `CAM_SETTLE` 1.5% or none |
| Follow cam jerks when the march turns | tween restarted on every waypoint | spring (§8) |
| Long jumps across the realm nauseate | fly longer than the clamp | dip cut (§7) |
| Two tweens fight over one property | new tween without `kill()` | one tween per channel, kill on interrupt |
| Motion differs at 30 vs 60 fps | per-frame lerp `a = lerp(a, b, 0.1)` | time-based curves or the spring (§8) |
| Gate clip in Godot looks steppy | clip resampled to fewer frames on import | import FPS 30, optimizer off |

## 10. Checklist

- [ ] Every shot names a curve from §1 and a duration in ms and f60.
- [ ] `peak = factor × total / T` computed for zoom, pan and rotation; all under §4.
- [ ] No `TRANS_EXPO`, `TRANS_CIRC`, `TRANS_BACK` or `CUBIC_IO` on the camera.
- [ ] Distance always interpolated in log space; jumps use `ZoomPath` with `T = 0.41 S` or `0.62 S`.
- [ ] Interruptible motion uses the spring; committed shots use one tween.
- [ ] Reduced-motion variant defined for every shot (§7).
- [ ] Camera `dt` clamped to 33 ms and clamps logged.
