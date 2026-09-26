# QA — probes, fixtures, captures, the review rubric and lessons

Nothing in battle-forge is done without pasted evidence (game-director hard rule 3). This file
lists the harnesses that already exist, the battle probes to write (qa-forge writes them; the
names and verdict lines here are PROPOSALS — qa-forge fixes the wording), the canned fixtures,
the capture and frame-review protocol, the scoring rubric, and the lessons log.

## 1. Existing harnesses a battle change must keep green

| Harness | Owner | What it guards for battle-forge |
|---|---|---|
| `attack_audit`, `balance_test` | gameplay-forge | the resolver and the balance corridor are untouched: battle-forge changes must leave both outputs byte-identical |
| `march_probe`, `realm_probe`, `map_trap_probe` | world-forge | marches, the map, camera traps on the realm |
| `ux_flow_probe`, `ux_touch_probe`, `layout_audit`, `menu_test` | ui-forge / qa-forge | tap counts, touch targets ≥ 48 dp, layout |
| `w1f_aspect_sweep` | ui-forge | `ASPECT SWEEP OK - 6 shapes, 0 faults` with the battle HUD, form and cards open |
| `a11y_audit`, `contrast_test` | qa-forge | text sizes, contrast of badges, bars and cards |
| `session_audit` | qa-forge | the war session timeline (core-loop §8.3) including battle presentation length |
| `sd_cost_probe` | cloud-forge | reads and writes per battle; spectators add 0 reads |
| core gate | game-director | the headless battery + real boot test after every change set |

Run pattern (PowerShell 5.1, no `&&`; `$g` as in game-director SKILL.md):
```powershell
& $g --headless --path godot --script res://core/attack_audit.gd
& $g --headless --path godot --script res://core/battle_timeline_probe.gd   # new, path to confirm
& $g --path godot --resolution 1080x1900 --script res://core/ux_flow_probe.gd
```

## 2. New battle probes (for qa-forge)

| Probe (path to confirm) | Mode | Input | Asserts | Verdict line |
|---|---|---|---|---|
| `beat_coverage_test` | headless | every beat kind the resolver can emit (read from the frozen shape, not hand-listed) | each kind has a beats.md row: clip, VFX id, SFX id, camera, 1× ms, min 2×, priority; every id resolves to a real resource | `BEAT COVERAGE OK - 18 kinds, 0 unmapped, 0 missing resources` |
| `battle_timeline_probe` | headless | fixtures §3 | 1× length inside the context budget; skip time; 2× floors; A beats in the log = Σ ×N of A beats shown; `i` order kept; 0 hits inside holds; full lord moments ≥ 6,000 ms apart; ≤ 1 camera move per 3 s outside A beats; live-watch timelines end within 100 ms of `T_fight` (or regroup after the outcome) | `TIMELINE OK - 10 fixtures, field 20.6s, siege 32.5s, rally 41.0s, 0 dropped A beats` |
| `battle_determinism_probe` | headless | each fixture × 3 runs × {1×, 2×} | identical cue lists (hash of `t_ms, kind, actor, variant`) | `DETERMINISM OK - 60 runs, 1 hash per fixture-speed` |
| `beat_latency_probe` | headless | log delivery delayed 0 / 1.2 / 4 / 8 s | act I covers ≤ 1.6 s; hold ≤ 3 s; fallback plate at 4.6 s; no outcome before the log | `LATENCY OK - hold max 3.0s, fallback at 4.6s, 0 early outcomes` |
| `counter_readability_probe` | windowed | a fixture with every counter pair in both directions | Σ badge ×N = counter-flagged beats; badge ≥ 72 px at peak; contrast ≥ 4.5:1 against the field; three state icons with alpha-mask IoU < 0.6; ≤ 2 badges at once | `COUNTERS OK - 10 pairs x 2 directions, min contrast 5.1, max IoU 0.42` |
| `vfx_budget_probe` | windowed, Movie Maker | every fixture | per beat: cover %, emitters, particles, dynamic lights vs presentation.md §7; flashes ≤ 3 per any 60 frames | `VFX BUDGET OK - peak cover 38% (breach), max particles 470, flashes <= 2/s` |
| `battle_frame_probe` | windowed, reference phone | heaviest fixture (castle + rally 20 joiners + 3 engines) | p95 frame ≤ 16.7 ms, no frame > 33.3 ms at beat boundaries, draw calls ≤ 150, skinned figures ≤ 70, 0 sync loads | `BATTLE FRAME OK - p95 14.2ms, worst 29.8ms, draws 131, figures 64` |
| `march_eta_probe` | headless (extends `march_probe`) | 200 random marches, intercepts, recalls | shown ETA, contact and recall times within ±1 s of the server functions | `MARCH ETA OK - 200 marches, max error 0.4s` |
| `warning_probe` | headless | hostile marches at ETA 30 s / 90 s / 10 min; 5 attackers; quiet hours; an offline return after 3 attacks | bands at the right times ±1 s; pushes grouped ≤ 1 per 60 s, ≤ 6 war pushes a day; ward blocked while targeted; offline return = 1 digest line, 0 modals | `WARNING OK - 4 bands, pushes 1 per 60s, ward blocked 5/5` |
| `defence_flow_probe` | windowed | new castle; each failing readiness check | setup ≤ 12 taps / 60 s; each banner response ≤ 3 taps; bubble shows only below 4/4 or under threat | `DEFENCE FLOW OK - setup 12 taps 54s, responses <= 3 taps, bubble 4/4 hidden` |
| `rally_flow_probe` | windowed + headless | launch, join from 4 entry points, 50 random joiner positions | launch ≤ 4 taps, join ≤ 3 taps, 0 late arrivals, expected vs actual share gap ≤ 2 points | `RALLY FLOW OK - launch 4 taps, join 3 taps, 0 late, share gap max 1.1` |
| `outcome_probe` | windowed | win / loss for every context; overflow; reduced motion | ceremony ≤ 108 frames, skip at 18; plate parity (0 px diff); safe line first; lost never animates; ≥ 2 next actions; heal time = infirmary; 0 purchase nodes | `OUTCOME OK - 14 cards, 108 frames, skip at 18, 0 buy nodes` |
| `battle_flows_probe` (a `ux_flow_probe` suite) | windowed | flows A–G of flows.md §9 | taps per flow ≤ budget | `BATTLE FLOWS OK - 7 flows, max taps 6 (B)` |
| money-law check | headless grep | battle scenes and scripts (battle view, form, cards, banners, report entry) | 0 references to shop / offer / gem-price entry points (names to confirm with shop-forge) | `BATTLE MONEY-LAW OK - 0 buy entry points` |

## 3. Fixtures — canned beat logs

Stored as JSON beside the probes (path to confirm, e.g. `godot/core/fixtures/battle/`). Each is
a real resolver output captured once (for example from the `attack_audit` scenarios), never hand-typed, so the
fixtures follow the frozen shape. Re-capture when gameplay-forge versions the shape.

| Fixture | Why it exists |
|---|---|
| `camp_hunt5` | 5 camps in one hunt order: map markers only, grouped report |
| `camp_single_first` | a player's first PvE battle (auto-watch) |
| `field_even_counters` | 5 v 5 lines, 2 counters each way: the counter badge both directions |
| `field_onesided` | a crushing win: holds must not show fake hits; the loser's card |
| `intercept` | a march caught on the road |
| `castle_breach` | engines, ram, breach, garrison lord, reinforcements: the longest castle case |
| `castle_held` | towers and tools win before the walls: defender-win framing |
| `castle_overflow` | defender loses with a full infirmary: overflow line |
| `rally_20` | 20 joiners, 3 engine types: ≤ 5 squads a side, pennons, gilt corners |
| `max_length` | the longest log the resolver can emit: the compositor's drop pass |

## 4. Captures and the frame-by-frame review

Godot's Movie Maker renders at a fixed frame rate regardless of device speed, so the same
fixture gives the same frames every time:
```powershell
& $g --path godot --resolution 1080x1900 --fixed-fps 60 --write-movie art/battle_forge/captures/castle_breach/f.png --script res://core/battle_capture.gd -- --fixture castle_breach
```
(`battle_capture.gd` is a small qa-forge script, path to confirm: it loads the fixture, plays
`BattleDirector`, and quits after the outcome card. User args are read with
`OS.get_cmdline_user_args()`.) Frame times cannot be measured in Movie Maker mode; use
`battle_frame_probe` on the device for that.

Review the numbered PNG sequence at these frames and LOOK at every one:

| Key frame | Check |
|---|---|
| act I last frame | both armies framed; lines readable in greyscale at 64 px |
| every counter impact + 11 frames (badge peak) | badge readable, direction right, rim GILT or IRON correctly |
| every full lord moment at +30 frames | portrait big, name one line, field still visible at 75% |
| breach impact + 6 frames | cover ≤ 40%; the gate state changed; cause visible before it |
| `outcome` beat start + 108 frames | card order: headline, safe, lost, why, next |
| the same frames in reduced motion | same content, no shake or push |

Contact sheets: tile the key frames with blender-forge's `tools/rarity_sheet.py` (it tiles any
labelled PNGs): `py .claude/skills/blender-forge/tools/rarity_sheet.py sheet.png f00096.png f00412.png … --labels "act I,counter 1,…" --cols 3`.

## 5. The battle rubric — score every change

Ten criteria, 0–2 each. Ship at **≥ 17 / 20 with no 0**; otherwise iterate (≤ 5 loops, then
stop and report the residual gap honestly).

| # | Criterion | 2 | 1 | 0 |
|---|---|---|---|---|
| 1 | Cause readable | 5 of 5 testers name the main cause ≤ 10 s after the card | 3–4 of 5 | ≤ 2 of 5 |
| 2 | Counters visible | every counter badged, both directions | missing in one direction | badges absent or wrong |
| 3 | Lord moments | each lord's moment named by testers; ≥ 6 s apart | named but crowded | indistinct |
| 4 | Restraint | all presentation.md §7 limits met, flashes ≤ 3/s | one limit exceeded by ≤ 10% | any "Never" column hit |
| 5 | Timing | inside the context budget; skip on time | ≤ 10% outside | outside by more |
| 6 | Truth | shown beats = log; 0 invented hits; order kept | a cosmetic mismatch | an invented or reordered deciding beat |
| 7 | Muted read | the whole battle reads with sound off | one cue lacks a visual twin | depends on sound |
| 8 | Loser respect | plate parity; safe line first; ≥ 2 next actions | wording harsh in one case | smaller/darker defeat or an offer |
| 9 | Performance | budgets met on the reference phone | p95 over by ≤ 2 ms | hitches > 2 frames |
| 10 | Identity | warm key upper-left, cool shadow, gold-first accents, painted kit, no neon | one off-palette effect | reads as another game's look |

**Tester script for criterion 1** (5 people who did not build it; no coaching): show the
`field_even_counters` replay at 1×, then the card; ask "Why did this side win?" and time the
answer. A correct answer names the counter or the lord skill the report ranks first.

## 6. Release gate by change type

| Change | Must be green (verdict lines pasted) |
|---|---|
| Beat row, compositor, speeds | `beat_coverage_test`, `battle_timeline_probe`, `battle_determinism_probe`, `attack_audit` + `balance_test` unchanged |
| VFX, camera, squads, sound | `vfx_budget_probe`, `counter_readability_probe`, `battle_frame_probe`, capture review, rubric |
| Flows, forms, cards, HUD | `battle_flows_probe`, `ux_touch_probe`, `w1f_aspect_sweep`, `layout_audit`, `a11y_audit`, `contrast_test` |
| Defence | `warning_probe`, `defence_flow_probe` |
| Rally | `rally_flow_probe`, `march_eta_probe` |
| Outcome | `outcome_probe`, money-law check |
| Anything that reads or writes the server | `sd_cost_probe`, `beat_latency_probe` |

| Fails when | Caught by |
|---|---|
| A probe was not run and "looks fine" is reported | [ ] the change record quotes every gate line above for its type |
| A fixture was hand-edited to pass | [ ] fixtures re-captured from `attack_audit`; git-free checkpoint diff (game-director rule 2) |

## 7. Lessons log

Real lessons go to the bottom of this file (game-director rule 7: every improvement is written
back into the owning skill). Format — one row each:

```
| date | area (flow/beat/presentation/defence/rally/outcome) | predicted | measured | fix | files changed |
```

Seed lessons from the genre research (design-forge `benchmark.md`; tags kept) — to be replaced
by our own measured rows:

1. A counter bonus of about 5% is invisible under talent, gear and status stacks; reviewers
   concluded that PvP "isn't about tactics, just raw power". A counter must be big enough to
   matter (combat.md) AND shown when it lands (presentation.md §5).
2. Armies drawn as a small squad + banner + troop-type icon + health bar keep mass battles
   readable at mid zoom [observational]; count-true crowds do not scale.
3. About one combat turn per second and a skill every ~10 turns [community estimate] give a
   ~10 s skill rhythm; our full lord moments sit ≥ 6 s apart for the same reason.
4. A full hospital turns one lost fight into dead troops and a quitting player; the forecast in
   the march form and the safe-first card exist for this.
5. Rally waits of up to 8 hours tie players to a clock and to time zones; windows ≤ 10 min plus
   scheduled rallies inside war windows are our answer.
6. Relocation is barred while an attack is incoming; we extend the same fairness to wards
   (defence.md §7, owner decision).
7. Public march lines turn the map into shared information and bluff; our warning bands build on
   them rather than hiding marches.

| date | area | predicted | measured | fix | files changed |
|---|---|---|---|---|---|
| (first real row lands here after the first shipped change) | | | | | |
