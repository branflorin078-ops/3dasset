---
name: battle-forge
description: The attack and defence experience of Castle Conquest — choosing a target, scouting, forming a march (lords, five lines, siege), the march on the realm map (ETA, interception), field battles, castle assaults (walls, gate, towers, traps, garrison lord), defence setup, watchtower warnings, reinforcements and rallies, the battle presentation built from the resolver's beats (beat-to-animation/VFX/sound/camera timings, token squads, counter badges, lord skill moments, VFX restraint), the outcome ceremony that respects losers, the infirmary hand-off and replay data for reports. Use for "battles are hard to read", "why did I lose", "attack flow", "defence setup", "rally flow", "battle replay", "counter feedback", "the battle looks empty". Not for combat rules or numbers (design-forge), the resolver (gameplay-forge), report content (report-forge), siege engines (siege-forge), cameras (transition-forge) or lord art (commander-forge).
---

# battle-forge — the resolver's truth, told so a player can learn from it

The resolver (gameplay-forge, frozen shape) decides every battle at one moment and emits
**beats**. battle-forge owns everything the player does and sees around that moment: picking
a target, scouting, forming and sending the march, watching it walk, the battle itself, the
defence, the rally, and the minute after the result. The standard is pillar 5 of the
game-director scorecard — **"the player can say why they won or lost"** — reached with
numbers: milliseconds per beat, taps per flow, percent of screen per effect.

## Hard rules

1. **Present, never decide.** battle-forge never changes an outcome, a sacred balance
   constant, the frozen resolver shape or a rule. Rules and magnitudes are design-forge
   `references/combat.md`; a rule question goes there as a proposal, never into
   presentation code. `attack_audit` and `balance_test` outputs stay byte-identical.
2. **Truth on screen.** The presentation is a pure function of the beat log and its seed
   ([beats.md](references/beats.md) §1). Nothing is invented (no fake near-miss, no hit inside
   a filler), nothing causal is reordered, no slow motion. The compositor may merge, shorten
   or drop only cosmetic beats; deciding beats (counters, Orders, breaches, routs, outcome)
   always play — identical ones may merge into one beat marked "×N", still counted.
3. **Counters are shown every time they land**, in both directions: flash + badge (attacker
   line → chevron → target line) + sting, the same medallions as the march form and the
   report ([presentation.md](references/presentation.md) §4). combat.md makes the counter a
   constant worth one tier; the genre's ~5% counter, buried under stat stacks and never shown,
   is the failure we exist to fix.
4. **Time budgets at 1×**: camp in a hunt order 4 s marker (no battle view); single camp
   10–16 s; field 20–30 s; castle 28–45 s; rally 30–45 s. Skip at 3 s (PvE 2 s); 2× speed with
   readable floors; outcome ceremony ≤ 1,800 ms, skippable after 300 ms; a repeat action never
   blocks input for more than 400 ms. (The war band "20–45 s, skip after 3 s" is design-forge
   `core-loop.md` §8.3.)
5. **Token squads, not crowds**: ≤ 5 squads a side (one per line) at any army or rally size;
   ≤ 70 skinned figures; strength is a bar and a number; attrition drops figures in steps;
   no blood and no bodies left on the field (age rating to confirm).
6. **VFX restraint, measured**: screen cover ≤ 15% for a normal beat, ≤ 35% for a lord's Order,
   ≤ 40% for a breach, never > 50%; ≤ 500 particles; ≤ 3 luminance flashes per second; every
   effect lights what it touches (game-art-director `effects.md`).
7. **Losers are respected** ([outcome.md](references/outcome.md)): same plate, size and
   loudness as victory; the first line is what is safe; the top cause in plain words; ≤ 3 next
   actions. **No purchase on any battle surface** — battle view, march form, warning banners,
   outcome card, report entry: 0 buy buttons, 0 offers, 0 gem prices (money-law).
8. **Live realm**: no battle scene, no loading screen; the battle plays where it happened. The
   server resolves, the client presents after the log arrives; spectators read 0 extra data;
   presentation metadata is recomputed on view and never stored.
9. **Taps**: attack a known target 3, intercept 3, join a rally 3, launch a rally ≤ 4, respond
   to an incoming attack ≤ 3 from the banner, first defence setup ≤ 12 / 60 s. Touch targets
   ≥ 48 dp.
10. **Honest information**: unknown intel is "?" with the tier that reveals it; ETAs come from
    server time; a reinforcement or rally join that cannot arrive in time says so before Send.
11. **The asset lanes hold**: troop figures are the `hero3d` rig + soldier kit; engines and
    defensive tools are siege-forge through blender-forge; wall and gate states are
    castle-forge; UI icons (medallions, badges) are Blender-made art, never white, monochrome
    or line glyphs; portraits are the painted lane. No code-built people, no primitive shapes.
12. **Every number here is a PROPOSAL** until checked against the shipped data. Shipped values
    win; unknown paths are written "(path to confirm)". Facts from the studio's repo mapping
    notes (`battle_engine.gd` six phases, `UI.reduced_motion`, feel-forge's 1,800 ms
    battle-won rule, PEGI 7) are cited as such and verified first. Rules already written by
    sibling skills win over this skill's drafts: design-forge `combat.md` (counter ring, losses,
    rallies, walls, scouting), `lords.md` (Orders), `alliance.md` (rally scheduling),
    `onboarding.md` (scripted first battles), transition-forge `zoom-model.md` (the rig).
13. **Evidence or it did not happen**: the probes for the change type, a Movie Maker capture
    looked at frame by frame, and the rubric at ≥ 17/20 with no zero
    ([qa.md](references/qa.md)).

## Key numbers at a glance (all PROPOSALS — the references hold the full tables)

| Thing | Number | Where |
|---|---|---|
| Beat durations | volley 900 ms · charge 1,400 · brace 1,100 · clash 1,100 · full Order moment 2,000 · breach 2,200 | beats.md §3 |
| Counter badge | 72 px, pop 140→100% in 180 ms, hold 700 ms (450 at 2×) | presentation.md §4 |
| Full Order moments | ≤ 2 per battle, ≥ 6 s apart; world dim to 75%; portrait 280 px | presentation.md §5 |
| Camera | via transition-forge's `CameraDirector`; FOV 30° fixed; ≤ 1 move per 3 s; shake ≤ 10 px via `h_offset`/`v_offset` | presentation.md §1 |
| Late beat log | act I hides 1.6 s; clash loop ≤ 3.4 s; retry + "Awaiting word" at 5.0 s (combat.md §8) | beats.md §6 |
| Warning bands | Detected (any ETA) · Near ≤ 60 s · Contact | defence.md §2 |
| Rally windows | combat.md §9: 5 / 10 / 30 min vs players, ≤ 60 on PvE strongholds, ≤ 15 joiners; each chip shows who is in reach | rally.md §4 |
| Frame budget | p95 ≤ 16.7 ms, draw calls ≤ 150, 0 sync loads | presentation.md §9 |

## Workflow

1. **Frame** — which part is asked (target/scout/form/march, beat, presentation, defence,
   rally, outcome) and which pillar it moves (5 battles understood; 7 belonging; 10 one-hand
   readability). Read the ledger rows for battle first (game-director rule 5).
2. **Read the truth** — the shipped beat kinds and phases (grep the resolver; quote file:line),
   the combat.md rule involved, the current presentation code and data. A gap in the rules is
   sent to design-forge as a question; it is not solved here.
3. **Measure the present** — capture the matching fixture with Movie Maker
   ([qa.md](references/qa.md) §4), run the flow probe for its taps, score the rubric. This
   baseline is what the change must beat.
4. **Design in the reference's format** — table rows with ms, frames at 60 fps, taps, sizes
   in px at the 1080 px short side, every failure state with its message and next action,
   and the "Fails when | Caught by" checklist rows.
5. **Route the build** (table below) with one writer per file and a checkpoint of every file
   that will change (game-director rule 2).
6. **Prove** — the release gate for the change type ([qa.md](references/qa.md) §6), verdict
   lines pasted; the capture reviewed at the key frames; rubric ≥ 17/20, no zero. Red → fix or
   restore from the checkpoint; after 5 loops, stop and report the residual gap.
7. **Record and teach** — a ledger row with the evidence; a lessons row in
   [qa.md](references/qa.md) §7 (predicted vs measured); the reference updated with the
   numbers that worked.

## Routing — who owns what around a battle

| Need | Owner | battle-forge's part |
|---|---|---|
| Counter graph, magnitudes, loss buckets, capacities, wall durability, scouting tiers, ward rules | design-forge `combat.md` (+ `world.md`, `alliance.md`, `monetization.md`) | shows them; sends questions |
| The resolver, its beats and phases, the balance corridor | gameplay-forge | reads the log |
| Report schema, "why" explanation engine, scout reports, share cards' content, storage | report-forge | replays from the report; shares the counter derivation |
| Siege engines, defensive tools: models, clips (`fire`, `reload`, `move`), timings | siege-forge | places them in the timeline |
| Enter/leave battle view, march-out camera, castle ↔ realm zoom, motion comfort | transition-forge | states what the frame must hold |
| Lord portraits, emblems, signature effects, per-lord briefs | commander-forge | the Order-moment template |
| Screens, HUD components, tracker, status bubbles, icon kit | ui-forge | layouts and tap budgets |
| Marches on the map, paths, speeds, map markers | world-forge | what a march tells the player |
| Walls, gates, towers and their damage and burning states | castle-forge | picks the state from beat values |
| Troop figures, rig, clips | hero3d | the clip list and screen sizes |
| 3D props, icons, kit pieces | blender-forge | briefs with read sizes |
| Painted effect stills, portraits' art rules | game-art-director | applies `effects.md` per beat |
| Sound assets, buses, loudness | audio-forge | cue names and mix rules |
| Ceremony motion rules, banned easings | feel-forge | the outcome timeline |
| Server resolution, latency, cost, idempotent sends | cloud-forge | latency hiding, 0 spectator reads |
| Wording and voice; strings | story-forge; l10n-forge | placeholder lines and keys |
| First-session script, chapters, first-time moments | onboarding-forge (design: design-forge `onboarding.md`) | presents the raid at the gate, the first battle, the first rally and the raid on the walls (flows.md §10) |
| Probes and fixtures | qa-forge | the probe specs in qa.md |

## Reference index

| File | Holds |
|---|---|
| [references/flows.md](references/flows.md) | target choice, target card, scouting, the march form, march-out, the march on the map, interception, watching, coming home, tap budgets A–G, the four onboarding battles |
| [references/beats.md](references/beats.md) | the log contract, six acts, the beat → animation/VFX/sound/camera table with ms and frames, the compositor, speed/skip/replay, latency, `T_fight`, Godot pattern |
| [references/presentation.md](references/presentation.md) | camera rules, token squads and clips, battle HUD, counter badges, lord moments, VFX limits, sound mix, reduced motion, frame budgets |
| [references/defence.md](references/defence.md) | defence layers, warning bands, watchtower information tiers, defence setup flow, readiness bubble, reinforcements, wall states, wards, response budget |
| [references/rally.md](references/rally.md) | launch and join flows, windows, the rally march and battle, shares, failure states, teaching the first rally |
| [references/outcome.md](references/outcome.md) | ceremony timeline, headlines, the card, the infirmary hand-off, next actions, the report hand-off and telemetry |
| [references/qa.md](references/qa.md) | existing harnesses, new battle probes with verdict lines, fixtures, Movie Maker capture and review, rubric, release gate, lessons log |

## Output contract

Every battle-forge task ends with:
1. The rows changed or added (beat table, flow table, limits), each with its numbers, in the
   reference files here and in `design/battle/<topic>/` (path to confirm) for the build team.
2. Measured taps and seconds for every flow touched, before and after.
3. The verdict lines of every probe in the release gate for the change type.
4. The capture sheet path (`art/battle_forge/captures/<fixture>/…`, path to confirm) and the
   rubric score with one line of evidence per criterion.
5. Files touched, each with its owning skill; the checkpoint folder.
6. **Owner decisions required** — listed separately; empty is a valid answer, missing is not.

## Owner decisions pending (from this skill's first draft)

1. Screen orientation: design-forge `core-loop.md` (1080×1900) and transition-forge
   `zoom-model.md` (portrait, width fixed at 1080) assume portrait; the older studio mapping
   notes say landscape-only. This skill sizes everything at a 1080 px short side so both work.
2. `T_fight` per context (field 24 s, castle 36 s, rally 40 s): a server constant for when the
   surviving march departs and how long spectators see the clash (beats.md §6).
3. An early "Launch now" for rally leaders (rally.md §2; combat.md sends rallies at window
   end today).
4. Auto-watch defaults: PvE battle view only for the first 10 battles (beats.md §4).
5. Age rating (PEGI 7 per the studio notes) → no blood, fallen figures fade (presentation.md §2).
6. A protective rule after repeated lost defences beyond combat.md's breach truce, if any
   (outcome.md §6).
7. No offers for 10 minutes after a lost battle anywhere in the game (shop-forge rule; this
   skill only guarantees its own surfaces).
8. Where replays come from: stored beats (storage cost) or a client re-run of the pinned
   resolver version (client ships old resolver versions) — report-forge and gameplay-forge
   decide together (beats.md §1).
