# Beats — from the resolver's log to a timed presentation

The resolver (gameplay-forge, frozen shape; `godot/core/battle_engine.gd` per the studio
mapping notes — path to confirm) decides the battle at one moment and emits **beats**.
battle-forge turns beats into a timeline of animation, VFX, sound and camera cues. It never
changes a result, never invents an event, and never reorders cause and effect.

Every number in this file is a **PROPOSAL** (verify against the shipped data and the frozen
beat vocabulary). Rules and magnitudes (counter bonus, loss buckets, wall durability) are
`design-forge/references/combat.md`; this file only decides how long and how loud they are.

## 1. The input contract (what battle-forge needs from a beat log)

battle-forge reads; it does not define the resolver's storage. `report-forge` owns the stored
schema (its `schema.md`). The minimum the presentation needs:

| Field | Meaning | If the shipped log lacks it |
|---|---|---|
| header `seed`, `resolver_version` | combat.md §8 rule 6: seed = hash(march id, arrive); both stored in the cause ledger (combat.md §12) | never from the clock |
| header `ctx` | context: camp, outpost, field, intercept, castle, rally, stronghold — plus the combat.md §6 loss row (1–9) | from the march kind and target |
| header `start` | per side: lord pair, line × tier counts, structures (wall, gate, towers, tools) | from the report's start block |
| beat `i` | order index | array order |
| beat `ph` | resolver phase (the resolver has six phases per the mapping notes — names to verify) | map by kind (§2 column "Act") |
| beat `k` | kind | map shipped names to §2 kinds; an unmapped kind fails `beat_coverage_test` |
| beat `a`, `t` | actor and target: side + line, a structure, or a lord | — |
| beat `v` | value: troops removed (split by bucket if given), durability removed | — |
| beat `f` | flags: counter, Order id, tool id | **counter flag**: derive client-side from combat.md §2's counter ring (the actor's line hunts the target's line). Never ask for a resolver change to get it. |

Rule: the presentation is a pure function `timeline = compose(log, speed)`; the seeded
`RandomNumberGenerator` (`rng.seed = seed`) picks every variant (sound take, debris count,
figure that falls). Same log → same timeline, frame for frame, on every device.

**Replay source.** A replay needs the beats. If report-forge stores them, use them. If it stores
only the ledger and the start block (storage is report-forge's choice), the client re-runs the
frozen resolver of the stored `resolver_version` on the stored inputs and seed — the resolver
is a pure function (combat.md §8 rule 6) — for presentation only. The re-run's outcome must
equal the stored outcome, or the replay is refused and the report stands alone; a client
without that resolver version shows "Replay not available for battles before this update".
The live first view always uses the server's beats (rule below), never a client re-run.

Runtime safety: a kind with no row (a resolver version the client does not know yet) plays as a
neutral `hit` on its target with its losses applied, and logs `BATTLE_UNMAPPED <kind>` once per
battle. It never crashes the view and never drops losses silently; `beat_coverage_test` exists
so this path is never reached in a shipped build.

## 2. The six acts

The presentation groups beats into six acts. Map each act to the resolver's six phases once
their names are verified; if the resolver phases differ, the act is taken from the beat kind.

| Act | Field battle | Castle / stronghold | Resolver phase (verify) |
|---|---|---|---|
| I Approach | squads close | squads close; engines deploy | 1 |
| II Missiles | volleys, bolts | tower fire, traps, attacker volleys | 2 |
| III Engines | — (skipped, 0 ms) | engine shots, ram, assault ladders, breach | 3 |
| IV Contact | charge, brace, clash, Orders | garrison lord, reinforcements, charge, brace, clash, Orders | 4 |
| V Break | rout | rout, last breach | 5 |
| VI Outcome | outcome pose | outcome pose, wall state | 6 |

Chapter marks on the replay scrub bar are the act boundaries (§5).

## 3. Beat → presentation table

Durations at 1×, 60 fps (frames in brackets). "Min 2×" is the floor at double speed — text and
badges below this cannot be read. Priority: **A** deciding — never dropped; it may merge ONLY
with identical A beats (same kind, actor, target and act) into one beat marked "×N", so every
one is still counted on screen; **B** important (may be shortened to its min); **C** cosmetic
(may be merged, overlapped or dropped).
Clip names follow blender-forge `references/animation.md` (verb, snake case); troop figure
clips come from the `hero3d` rig, engine clips from `siege-forge`.

| Kind | Animation | VFX (budget) | Sound cue (audio-forge names) | Camera | 1× ms | Min 2× | Pri |
|---|---|---|---|---|---|---|---|
| `approach` | squads `march` to the contact line; banners forward | dust wake per squad, ≤ 8% cover | `bt_bed_in` (400 ms fade), `bt_horn_advance` | establishing frame, both sides inside the central 70%; push 4% over the beat | 1,600 (96) | 800 | B |
| `volley` | archers `volley`: draw 150 ms, loose; target `hit` | 8–14 arrow streaks on an arc, flight 350 ms; ≤ 6 impact puffs | `bt_bow_loose` ×3 takes, `bt_arrow_hit` | none | 900 (54) | 450 | C |
| `bolt` | crossbows `shoot`: level 120 ms, release; flat path | 4–6 bolt streaks, flight 220 ms; 1 spark per hit on armour | `bt_xbow_crack`, `bt_bolt_hit` | none | 750 (45) | 400 | C |
| `charge` | cavalry `charge`: lean 250, gallop 600, impact 300 ms; target knock-back 0.4 m | hoof dust wake; impact ring ≤ 12% | `bt_hooves_roll` (rising), `bt_charge_impact` | shake 4 px, 180 ms at impact | 1,400 (84) | 750 | B |
| `brace` | spearmen `brace` 200 ms before contact; riders `hit` and stop | spark line along the spear points | `bt_spear_brace`, `bt_horse_rear` | hit-stop 3 frames at contact | 1,100 (66) | 650 | A |
| `clash` | both squads `attack` loop, 2 swings; losers' figures `fall` | ≤ 4 sparks, low dust | `bt_melee_bed` + 1 `bt_clash` per exchange | lateral drift 2% | 1,100 (66) per exchange | 550 | C |
| `order` | a lord's Order (active skill, war drum — lords.md §5): caster squad lit; lord chip; signature effect | ≤ 35% cover, ≤ 1,200 ms | lord motif (commander-forge) + effect cue | full: world dim to 75% brightness, push 5% | 2,000 (120) full · 900 (54) short | 1,000 · 600 | A |
| `rout` | banner dips 300 ms; figures `rout`, fall back 1.5 m; squad greys to 50% saturation | none | `bt_rout_horn` (low) | none | 1,000 (60) | 500 | A |
| `tower_fire` | tower-top archers `volley` | streaks from the tower top | `bt_tower_loose` | none | 700 (42) | 350 | C |
| `trap` | the defence tool reveals and fires (siege-forge defensive tools: drop-stones, murder holes, hoardings) | ≤ 15% cover, ≤ 800 ms | tool cue | frame the hit squad | 900 (54) | 500 | A first · C repeat |
| `engine_shot` | engine `fire` (siege-forge timing: cause before effect); projectile arc; structure `hit` state | stone dust ≤ 15%; 3–6 debris pieces | `bt_engine_release`, `bt_projectile_whistle`, `bt_stone_crack` | first shot: follow the projectile, pan ≤ 20°/s; repeats: static | 2,200 (132) first · 1,200 (72) repeat | 1,100 · 600 | B |
| `ram_hit` | ram `swing` ×3, 400 ms apart; gate `hit` | 3–5 splinters per hit | `bt_ram_boom` ×3 | shake 3 px per hit | 1,500 (90) | 800 | B |
| `assault` | ladders or belfry `raise` (siege-forge); 2 figures climb | none | `bt_ladder_thunk`, `bt_shouts` | frame the wall section | 1,600 (96) | 800 | B |
| `breach` | gate or wall section swaps to its breached state (castle-forge mesh) | dust volume ≤ 40% for ≤ 1,500 ms; haze ≤ 15% opacity for 3 s | `bt_breach_boom`, `bt_timber_groan` | hit-stop 3 frames; push 8% over 600 ms; shake 10 px, 250 ms | 2,200 (132) | 1,200 | A |
| `garrison_lord` | defending lord chip; garrison squad gets the sworn gilt rim | rim light only | lord motif, short | none | 1,200 (72) | 700 | B |
| `reinforce` | ally squad enters from the keep side with the ally's pennons (≤ 6, then "+N") | none | `bt_horn_ally` | none | 1,200 (72) | 600 | B |
| `wall_state` | the Walls & Gate bar (combat.md §10) crosses 67 / 34 / 0% → mesh or decal state step | dust puff ≤ 6% | `bt_stone_creak` | none | 400 (24), inside its causing beat | — | B |
| `outcome` | winner `cheer`, loser `fall_back`; winner's banner rises | no confetti, no full-screen flash | `bt_outcome_win` / `bt_outcome_loss` (same loudness) | ease out 6% over 800 ms | 800 (48), then the ceremony (outcome.md) | 500 | A |

Flags on any damage beat:

| Flag | Adds | ms added | Pri |
|---|---|---|---|
| `counter` | counter badge + target flash + larger number + `bt_counter_sting` (presentation.md §4); hit-stop 2 frames | +250 hold | A |
| `decisive` (derived: the largest loss beat of the battle, and the beat that drops the loser under its break point) | number shown even if C; 1 frame white-gold flash on the target | +0 | A |

| Fails when | Caught by |
|---|---|
| A kind the resolver can emit has no row (a silent beat) | [ ] `beat_coverage_test`: `BEAT COVERAGE OK - <n> kinds, 0 unmapped` |
| A counter lands and nothing on screen says so | [ ] `counter_readability_probe` badge capture for every counter pair |
| A 2× floor is below the time a badge or name needs to be read | [ ] timeline probe: every A beat ≥ its "Min 2×" |

## 4. The compositor — fitting beats into the budget

Budgets per context (1×). The war-session band from `design-forge/references/core-loop.md` §8.3
("20–45 s at 1×, skippable after 3 s, 2× speed") is the outer frame; PvE is shorter on purpose.

| Context | Default at contact | 1× budget | Skip appears | `T_fight` (PROPOSAL, §6) |
|---|---|---|---|---|
| Camp inside a hunt order | map clash marker only, no battle view | 4 s marker | — | 4 s |
| First battle of the game (onboarding.md step 7) | battle view | 20–30 s | 3 s | 24 s |
| Single camp, AI outpost | battle view for the player's first 10 PvE battles, then a result chip with "Watch" | 10–16 s | 2 s | 12 s |
| Field battle, interception | offer "Watch" (auto if following the march) | 20–30 s | 3 s | 24 s |
| Castle attack or defence | offer "Watch" | 28–45 s | 3 s | 36 s |
| Rally on a castle or stronghold | offer "Watch" to every participant | 30–45 s | 3 s | 40 s |

The compositor runs these passes, in order, and stops at the first pass that fits:

1. **Natural**: sum of 1× durations. Overlaps allowed only between C beats that share no actor
   and no target (two archer squads firing at different squads may overlap by ≤ 50% of the
   earlier beat).
2. **Merge**: consecutive same-kind C beats of the same actor inside one act become a salvo:
   one animation, impacts staggered 120 ms, at most 3 impacts shown; their losses sum into the
   last impact. Clash: at most 3 exchanges per pair per act; engine repeats: at most 3 per
   engine type per act. Identical A beats (e.g. the same counter volley 4 times, the same
   lord's Order twice in one act) merge into one beat marked "×N" with the badge or chip held
   once.
3. **Shorten**: B beats go to their "Min 2×" value × 1.4.
4. **Drop**: remaining C beats are dropped, oldest act first; their losses fold into the next
   shown beat of the same target. A beats and the first beat of each kind are never dropped.
5. **Still long**: the Contact act plays at 1.25× (melee loops only; text holds keep 1×).
6. **Short**: if under the budget floor, add `hold` fillers at act boundaries (banners in the
   wind, squads dressing ranks), ≤ 1,500 ms each, ≤ 3 per battle. A hold never shows a hit.

Worked timeline — castle attack with a breach (1×, after pass 2):

| Act | Beats shown | ms |
|---|---|---|
| I | approach | 1,600 |
| II | tower_fire ×2 (salvo) 1,400 · trap (first) 900 · volley ×2 1,800 | 4,100 |
| III | engine_shot first 2,200 + 3 repeats 3,600 · ram_hit 1,500 · breach 2,200 (the fourth won assault of a war window takes Walls & Gate from 20% to 0 — combat.md §10) | 9,500 |
| IV | garrison_lord 1,200 · reinforce 1,200 · charge 1,400 · brace+counter 1,350 · order full ×2 (each primary's first) 4,000 · order short ×4 (two are "×2" merges) 3,600 · clash ×4 4,400 | 17,150 |
| V | rout ×2 | 2,000 |
| VI | outcome | 800 |
| | **Total** | **35,150** (inside 28–45 s; `T_fight` 36 s) |

Worked timeline — field battle, 5 lines each side, 2 counters, 8 Orders at a median 24 rounds
(1×): approach 1,600 · volley salvo 900 · bolt 750 · charge 1,400 · brace+counter 1,350 ·
counter volley 1,150 · order full ×2 4,000 · order short ×4 3,600 · clash ×3 per 2 pairs 6,600 ·
rout 1,000 · rout 1,000 · outcome 800 = **24,150 ms** (inside 20–30 s; `T_fight` 24 s).

| Fails when | Caught by |
|---|---|
| A long battle overruns 45 s, or a one-sided battle is padded with fake hits | [ ] `battle_timeline_probe` fixtures: max, min, and 0 hits inside holds |
| Merging hides a counter or an Order | [ ] probe: A beats in the log = Σ ×N of A beats shown |
| Two beats with a cause→effect link swap order (breach shown before the ram hits) | [ ] probe: for every shown pair, `i` order is kept |

## 5. Speed, skip, pause, replay

| Control | Rule | Number |
|---|---|---|
| 2× | `Tween.set_speed_scale(2.0)` on the timeline tween; `AnimationPlayer.speed_scale = 2.0` on every squad; `speed_scale` on live particles. Never `Engine.time_scale` (it also speeds the UI and the realm) | text holds keep their "Min 2×" floor |
| Skip | shows at the context's skip time (§4); jumps to the final state (final strengths, structure states) with a 250 ms crossfade, then the outcome ceremony. The outcome card is never skipped | ≤ 1 tap, input free ≤ 100 ms after the tap |
| Pause | a pause button (bottom-left); while paused, tapping a squad shows its exact counts | 0 ms response target, ≤ 1 frame |
| Remembered | 2× and "auto-watch" choices persist per player (`ConfigFile` in `user://`) | — |
| Replay (from a report) | same `compose()`; scrub bar with the six act marks and gilt highlight ticks (counter, Order, breach); a tick jumps to 1,000 ms before its beat | ≤ 2 taps from the report |
| Late join | a player who opens a live battle after contact starts at the current act's first beat, with "From the start" offered | never mid-beat |

## 6. Latency, authority and the live realm

1. **The server resolves; the client presents.** The client never computes an outcome ahead of
   the server (anti-cheat; cloud-forge's server-authority design). Beats are requested at
   contact.
2. **Hide the fetch inside act I.** Assets for the battle load at contact − 10 s with
   `ResourceLoader.load_threaded_request` (squad scenes, the target castle state, engine GLBs).
   Beats are requested at contact; act I (1,600 ms) plays on the start block alone.
3. **Late beats** (combat.md §8 rule 7: result written ≤ 1 s p95 after arrival; after 5 s the
   client retries and shows "Awaiting word"): if the log has not arrived when act I ends, squads
   play the clash loop `idle_ready` for up to 3,400 ms more. At 5,000 ms after contact the client
   retries once, the plate "Awaiting word" replaces the field, the camera returns to the map, and
   the result arrives as the normal report toast. No spinner longer than that.
4. **`T_fight` (PROPOSAL for combat.md / world-forge)**: a fixed per-context fight length on the
   server, written into the march record's `return_arrive` (combat.md §8: `return_arrive =
   arrive + T_fight + time home`). The surviving march departs at `contact + T_fight`; spectators on the map see the
   clash marker for exactly `T_fight`. When watching live, the compositor fits the timeline to
   `T_fight` (it lies inside every budget band): longer → passes 2–5; shorter by ≤ 4.5 s →
   holds (pass 6: 3 × 1.5 s); shorter by more → after the outcome the winner regroups in
   `idle_ready`, the player may leave, and the map token still departs at `T_fight`. Replays
   use the natural fit.
5. **Spectators cost nothing extra**: third parties never fetch beats. The map marker is drawn
   from the two march records (contact time is known — both marches are functions of time) and
   the result flag arrives with the normal map update. 0 additional reads per spectator.
6. **Storage**: the timeline, act marks and highlight ticks are recomputed from the log on
   view. Nothing presentation-only is stored server-side (report-forge's `storage.md` costs).

| Fails when | Caught by |
|---|---|
| The outcome shows on the client before the server decided it | [ ] code review: `compose()` only runs on a received log; `beat_latency_probe` |
| A player waits > 5.0 s on a frozen field | [ ] `beat_latency_probe` with 0 / 1 / 4 / 8 s injected delay |
| The map token leaves while the watcher still sees fighting | [ ] live-watch fixture: last shown beat ≤ `T_fight` |

## 7. Implementation pattern (Godot 4)

- `BattleDirector` (a Node; path to confirm): `compose(log, speed) -> Array[Dictionary]` of cues
  `{t_ms, kind, actor, target, clip, vfx, sfx, cam, hold_ms}`; `play()` builds ONE sequential
  `create_tween()` chain of `tween_interval()` + `tween_callback()`; parallel C overlaps use
  `tween.parallel()`. `kill()` + `apply_final_state()` implements Skip.
- Squads are nodes with an `AnimationPlayer` per figure group; clips play with `play(name)` and
  the director's `speed_scale`. Far squads (map zoom) run `callback_mode_process =
  ANIMATION_CALLBACK_MODE_PROCESS_MANUAL` and `advance()` at 15 Hz.
- Flashes use a per-instance shader parameter (`instance uniform float flash;`,
  `GeometryInstance3D.set_instance_shader_parameter`) — no material duplicates (verify support
  on the renderer the game ships with).
- Shake moves `Camera3D.h_offset` / `v_offset`, never the camera transform (culling and the
  rig stay stable; same idea as feel-forge's "shake the CanvasLayer offset, not the position").
- Floating numbers: a pool of 12 `Label`s on a `CanvasLayer`, placed with
  `Camera3D.unproject_position()` each frame.
- A `RandomNumberGenerator` seeded from the log picks every variant; nothing calls `randf()`.

## 8. Checklist — adding or changing a beat row

- [ ] The shipped beat kind name is quoted with file:line (or "(path to confirm)").
- [ ] Animation clip, VFX id, sound cue, camera move, 1× ms, frames, Min 2×, priority — all filled.
- [ ] VFX cover and burst length inside presentation.md §6 limits.
- [ ] Merge / drop behaviour stated; A beats merge only with identical A beats, shown as ×N.
- [ ] Cause precedes effect on screen (engine release before impact; ram swing before the gate cracks).
- [ ] `beat_coverage_test` and `battle_timeline_probe` re-run; verdict lines pasted.
