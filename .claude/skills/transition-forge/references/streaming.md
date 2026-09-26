# Streaming — what loads during each transition, and why nothing hitches

Every transition is cover time: 250 ms to 1.5 s in which the eye is busy and
the loader can work. This file says what must already be resident before each
shot, what loads during it (with a deadline inside the shot), how geometry
swaps by distance, and the per-frame budget that keeps every frame under
16.7 ms on the reference phone (ship-forge names it). Measured by the probe
([qa.md](qa.md)); budgets marked PROPOSAL until the probe has run on device.

## 1. Before and during each shot

| Shot | Must be resident BEFORE f0 | Loads DURING (deadline) | If late |
|---|---|---|---|
| CASTLE_LEAVE | realm ring, veil, token pool | nothing | never late (resident by rule, §2) |
| CASTLE_ENTER | own LOD1 + cluster | own LOD0 of buildings in view (by C2 → C1) | LOD1 stays; LOD0 fades in 200 ms |
| COLD_OPEN | castle boot set, 3 warm frames | realm ring (idle time after f0) | painting holds (≤ 2.0 s to input, core-loop §8.1) |
| FOCUS_BUILDING | building LOD0/1 | card art (by MENU_OPEN's sheet 50%) | ui-forge loading state |
| MENU_OPEN | card surface (ui-forge pre-instances it) | card art | ui-forge loading state, never a blank rect |
| PANEL_FULL_OPEN | — | panel (from `button_down`, ui-forge) | ui-forge |
| JUMP_TO | war-map, veil | destination chunks (by 70% of T) | chunks fade in 200 ms; the camera never waits |
| BATTLE_ENTER | veil | battle site data + instancing (by the B2↓ crossing) | hover ≤ 1,500 ms, then region-level battle |
| MARCH_OUT, RETURN_HOME | gate GLB (band), token pool | nothing | — |
| Dip cuts | dip cover | destination (while covered) | hold covered ≤ 500 ms |

## 2. Resident sets and boot order

1. **Boot, behind the painting**: kit atlas; own buildings at current tiers
   (LOD0 for the C2 rest view, LOD1, the merged cluster); the gate GLB for the
   band; bubble and villager pools (ui-forge / feel-forge); HUD; the dip cover.
   Render ≥ 3 frames hidden (§5), then COLD_OPEN.
2. **Idle time after the first live frame** (≤ 2 ms per frame, §7): the realm
   ring (terrain chunks inside R_near's view + one ring), the war-map texture
   (PROPOSAL, zoom-model §7), veil textures, the token pool (≤ 20 tokens),
   march-line meshes. Deadline: before the player can reach the toggle after
   input goes live (≈ 1 s); CASTLE_LEAVE's first frame asserts it.
3. **Always resident afterwards**: own LOD1 + cluster, the realm ring, the
   war-map, veil, dip cover, gate. They are what makes the two most frequent
   transitions (leave, enter) load-free.
4. **On demand**: LOD0 of buildings in view (C2 → C1), chunks elsewhere
   (JUMP_TO, pan at R), battle sites, card art and full screens (ui-forge).

## 3. Geometry swaps — visibility ranges and HLOD

Godot 4: `GeometryInstance3D.visibility_range_begin/_end`,
`visibility_range_begin_margin/_end_margin`, `visibility_range_fade_mode`, and
`visibility_parent` (HLOD). With fade mode `VISIBILITY_RANGE_FADE_DISABLED`
the margin is a **hysteresis** distance; with `FADE_SELF` / `FADE_DEPENDENCIES`
it is a fade distance (the node renders in the transparent pass while fading —
no shadows, sorting cost). Default here: **fade disabled + margin as
hysteresis + the veil** hides the swap at B2. Use fades only where the probe
shows headroom, and check them on the renderer the game ships (Mobile or
Compatibility).

**The own town — a three-step HLOD chain** (worked distances from
[zoom-model.md](zoom-model.md) §4; compute from `H_b`, `W_town` at runtime):

| Node (GeometryInstance3D) | `visibility_parent` | begin / margin | end / margin | Visible when |
|---|---|---|---|---|
| Town cluster (one merged mesh of every building's LOD2) | — | B2 225 m / 25 m | B3 4,199 m / 450 m | R |
| Building LOD1 mesh | the town cluster | B1 91.6 m / 10 m | — | C2 (cluster too close → children show) |
| Building LOD0 mesh | its LOD1 mesh | — | — | C1 (LOD1 too close → LOD0 shows) |
| Own castle icon (Sprite3D, `fixed_size = true`) | — | B3 / 450 m | — | M |

HLOD rule used: a child shows only while its parent is hidden because the
camera is CLOSER than the parent's `visibility_range_begin`. One distance
check (camera to cluster) swaps the whole town at once — no half-swapped
town. Verify on device with the probe's per-level object counts
(`RENDER_TOTAL_OBJECTS_IN_FRAME`).

- **The cluster is merged at runtime** from each building's LOD2 at its
  transform (`ArrayMesh` via `SurfaceTool.append_from`, one surface, the kit
  material): one draw call at R. Rebuild on every tier change while the camera
  is at C1/C2 (the cluster is hidden there): ≤ 5 ms, spread over frames.
- Camera-to-cluster distance equals the rig distance only when the town is at
  the focus. The castle magnet (zoom-model §8) makes that true at B2, so the
  swap and the HUD flip land within ~5%.

**Other classes**

| Class | Range (worked example) | Mode | Note |
|---|---|---|---|
| Villagers (feel-forge) | end 180 m (building 75 px) / 15 m | `FADE_SELF` | few pixels, cheap alpha |
| Forest MultiMesh cells (128 m) | LOD0 end 450 m / 40 m; LOD1 450 m → B3 × 1.23 | disabled | a MultiMesh fades as ONE node: split forests into cells |
| Neighbour castle clusters (by stage, world-forge) | begin the 672 m floor, end B3 / 450 m | disabled | icons beyond B3 |
| Realm terrain chunks | end B3 × 1.23 (dissolve end) | — | hidden once the war-map covers (zoom-model §7) |
| Mesh detail inside a range | Godot's automatic mesh LOD (import-generated), `lod_bias` 1.0 | — | triangles only; forms swap by range |

## 4. Draw calls and triangles per level (PROPOSAL — verify on the reference phone)

| Level | Draw calls | Triangles in frame | Notes |
|---|---|---|---|
| C1 | ≤ 250 | ≤ 350k | LOD0 for ~6–12 buildings in view |
| C2 | ≤ 300 | ≤ 300k | LOD1 for the whole town, bubbles, villagers |
| R | ≤ 250 | ≤ 250k | cluster + neighbours + chunks + tokens (MultiMesh) |
| M | ≤ 120 | ≤ 60k | war-map plane + icons |
| Swap frames (B2, B3 bands) | ≤ 1.3 × the larger level | ≤ 1.3 × | both forms resident for ≤ 0.3 doublings |

Read with `Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)`
and `RENDER_TOTAL_PRIMITIVES_IN_FRAME` in the probe.

## 5. First-use hitches — warm before you show

- Godot 4.4+ compiles rendering pipelines when resources load instead of on
  first draw (confirm on the owner's 4.7.2 build with the COLD probe run).
  Any material, particle system or shader still hitching on first appearance
  is drawn once under cover: behind the loading painting at boot, or under the
  dip cover.
- **Warm frames**: at boot, place the camera at C2 rest and render ≥ 3 frames
  under the painting; also draw once, off to the side, the veil quads, gate
  dust particles (`fx_dust_gate`) and the war-map plane.
- **Show ≥ 2 frames after `add_child`**: add hidden (`visible = false`), let
  textures upload and `_ready` cascades finish, then show inside a fade.
- New particle systems in a transition use `preprocess` or start 1 frame
  early, hidden.

## 6. Memory — method, budgets, unload hysteresis

VRAM of a texture = `w × h × bytes/px × 1.33` (mips). Bytes per pixel: ASTC
4×4 1.0 · ASTC 6×6 0.445 · ASTC 8×8 0.25 · ETC2 RGB 0.5 · ETC2 RGBA 1.0.
Example: the 2048² kit atlas (albedo, normal, ORM — blender-forge
architecture.md §6) = 16.7 MB at ASTC 4×4, 7.4 MB at 6×6.

| Set | Unload rule |
|---|---|
| Own LOD1 + cluster, realm ring, war-map, veil, gate | never |
| Own LOD0 | 30 s after the camera leaves C1/C2 |
| Chunks outside view + 1 ring | 20 s after leaving (LRU) |
| Battle site full detail | 30 s after BATTLE_EXIT (a re-watch reloads nothing) |
| Card art, full screens | ui-forge LRU of 4, freed 30 s after close |

Peak at the B2 band = castle set + realm ring (both resident):
**≤ 1.25 × the larger set** (PROPOSAL; ship-forge owns the device VRAM cap).
Unloading with a delay is hysteresis for memory: a quick zoom back reloads
nothing.

## 7. The loader — threaded, time-sliced, never blocking

```gdscript
extends Node   # autoload StreamQueue (path to confirm)
const FRAME_BUDGET_US := 2000                    # instancing budget per frame
var _pending: Dictionary = {}                    # path -> Callable(resource)
var _spawn: Array[Callable] = []                 # small instancing jobs

func request(path: String, on_ready: Callable) -> void:
	if ResourceLoader.has_cached(path):
		_spawn.append(func(): on_ready.call(ResourceLoader.load(path)))
		return
	if not _pending.has(path):
		ResourceLoader.load_threaded_request(path, "", false)   # no sub-threads: keeps cores for the main thread
	_pending[path] = on_ready

func _process(_dt: float) -> void:
	for path in _pending.keys():
		var st := ResourceLoader.load_threaded_get_status(path)
		if st == ResourceLoader.THREAD_LOAD_LOADED:
			var cb: Callable = _pending[path]
			_pending.erase(path)
			var res := ResourceLoader.load_threaded_get(path)   # safe: LOADED, returns at once
			_spawn.append(func(): cb.call(res))
		elif st == ResourceLoader.THREAD_LOAD_FAILED or st == ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
			push_warning("StreamQueue: failed " + path)
			_pending.erase(path)
	var t0 := Time.get_ticks_usec()
	while not _spawn.is_empty() and Time.get_ticks_usec() - t0 < FRAME_BUDGET_US:
		_spawn.pop_front().call()
```

Rules:
1. `load_threaded_get` before `THREAD_LOAD_LOADED` blocks the main thread —
   the classic transition hitch. Only call it after the status says LOADED.
2. No `load()` of an uncached scene and no `preload` of big scenes in any
   frame of a transition.
3. Callers split big work into small jobs (one building, one chunk, one
   squad): every job ≤ 1 ms on the reference phone, measured.
4. `use_sub_threads = false` by default (4–8 core phones: the render and main
   threads need their cores); try `true` only for boot, measured.
5. Request early: touch-down (`button_down`), the tap, a march 10 s before
   contact — each 80 ms of head start is 5 frames of work not done during the
   shot.

## 8. Network in transitions (cloud-forge, world-forge)

- Map data for a JUMP_TO destination is a tile-chunk query (world-forge,
  design-forge world.md cost model) sent at the tap; the move covers
  450–1,000 ms. Entities that arrive late fade in over 200 ms; the camera never
  waits for the network.
- A battle site (BATTLE_ENTER) is fetched at the tap ("Watch") or 10 s before
  contact (auto). The hover (≤ 1,500 ms) is the only place a transition waits,
  and it has a fallback.
- Timeouts: 3 s, one quiet retry; nothing modal in a transition.

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| 1-frame freeze at the start of a zoom-out | realm ring loaded on the toggle | idle-time preload after boot (§2) |
| Freeze when a menu opens | `load_threaded_get` before LOADED | check status first (§7 rule 1) |
| Half the town swaps before the rest | ranges per building, no HLOD parent | the chain in §3 |
| Whole forest pops at once | one MultiMesh for the forest | 128 m cells |
| Shadows vanish on nodes near the band | fade mode puts them in the alpha pass | fade disabled + veil |
| Spike on first gate dust or veil | shader or particles first used in the shot | warm draw under cover (§5) |
| Zoom back into the castle reloads everything | immediate unload | 30 s unload hysteresis (§6) |
| Spike when a battle site appears | site instanced in one frame | ≤ 2 ms per frame jobs |
| Cluster shows an old tier at R | cluster not rebuilt on upgrade | rebuild while at C1/C2 (§3) |
| VRAM warning after a long war session | chunks never released | LRU with 20 s unload |

## 10. Checklist

- [ ] §1 table implemented: every shot asserts its BEFORE set at f0 (probe logs misses).
- [ ] Realm ring, war-map, veil, dip cover and gate resident within ≈ 1 s of the first live frame.
- [ ] Own town HLOD chain (cluster → LOD1 → LOD0) with hysteresis margins; object counts verified per level.
- [ ] Cluster merged at runtime, rebuilt on tier change while hidden.
- [ ] Forests split into 128 m MultiMesh cells.
- [ ] StreamQueue: no `load_threaded_get` before LOADED; ≤ 2 ms instancing per frame.
- [ ] Warm frames at boot; new materials/particles drawn once under cover.
- [ ] Unload delays: LOD0 30 s, chunks 20 s, battle site 30 s.
- [ ] Draw calls and triangles per level within §4 (probe columns).
