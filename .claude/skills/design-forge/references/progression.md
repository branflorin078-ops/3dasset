# Progression — the keep, the key graph, six ages, the curve

How a castle grows from a stockade to a crowned castle: the spine that gates everything, the keys each level asks for, research, troop tiers, the timer curve, catch-up. Owners: **gameplay-forge** (rules, data, save), **castle-forge** (castle view), **blender-forge** (six visual tiers, [architecture.md §4](../../blender-forge/references/architecture.md)), **ui-forge** (§11), **feel-forge** (age-up), **qa-forge** (§13). Genre: [benchmark.md](benchmark.md). Plates: [core-loop.md](core-loop.md).

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Verify against `data/buildings.gd`, `data/troops.gd` and the research data (paths to confirm). A dial that is a sacred balance constant keeps its shipped value; this file's value becomes a proposal to the owner.

**Shipped vs proposed.** The shipped game has **34 archetypes × 6 tiers** (canonical). The **30 keep levels in six ages of five** used below are a PROPOSAL and an **OWNER DECISION (§14.2)**; whether the shipped data has levels inside a tier is unknown (check `data/buildings.gd`). Until the owner decides, read one age as one shipped tier: every rule holds with 6 steps instead of 30; adopting 30 needs the save migration of §13.

**Day counts are model estimates, not measurements.** Every "day" figure (§0, §3, §5, §6, §7 calendar note, §9, §10, §13 example lines) comes from the toy calendar model of §9 — an unpublished scratch script whose assumptions are listed there. The progression sim (§13) must replace them before any of them is quoted as a result.

Notation: `L` = keep level 1–30 · `A` = age 1–6 = ⌈L/5⌉ (core-loop's `S`) · `ℓ` = another building's level · `tier(ℓ)` = ⌈ℓ/5⌉ · `K(L)` = keep timer (§7) · `f` = a building family's timer factor (§3) · `G` = resource gate ratio (§7) · **days** = elapsed days since the realm opened (or the account started); elapsed day 0 = [liveops.md](liveops.md)'s realm day 1.

## 0. The four questions

- **Want**: the next keep level and what it opens; the next age's castle (a render, ART SHOWN BIG); the next troop tier.
- **Obstacle**: two keys (§2), the cost (`G`), the timer, and once per age an Age Trial that money cannot buy.
- **Wait** (§9 model estimates): Age II in the first session; Age IV after 1.5 days (engaged free) to 3.8 days (casual free); keep 30 after ≈ 70 days (engaged free) or ≈ 86 days (casual free). Keep 30 is never started before elapsed day 42 (the charter, §9).
- **Witness**: the city's cluster sprite on the realm map changes per age; the alliance feed posts each age; troop kit follows the same material ladder (§6).

## 1. The spine — the keep

The spine is the **fortress** archetype, shown to players as *the keep*: its proportion is an engine contract (`KEEP_ASPECT 1.50`), it is the tallest silhouette in the city, and it already has the landmark bake budget ([architecture.md §6](../../blender-forge/references/architecture.md)). If the shipped game gates on another archetype, that one stays the spine: moving a gate is an owner decision (SKILL.md rule 4).

1. **The keep gates everything**: no building's level exceeds `L`; archetypes open by `A` (§3); troop tiers by `L` (§6); research rows by `A` (§5); plates by `A` (core-loop §2: banners +1 at A3/A4/A5, 2nd desk A4, 3rd crew A5).
2. **30 levels, six ages of five** (PROPOSAL, §14.2). Level 1 of an age swaps the tier model: one new silhouette element plus one material step (architecture.md §4). Levels 2–5 each add one detail that breaks the outline — banner pole, pennon, weather vane, chimney stack, hoist beam, crenel shields, awning, lantern bracket — from ONE shared prop kit placed at anchors `lvl_2`…`lvl_5` (PROPOSAL to blender-forge / castle-forge; anchor names to confirm). No dead levels ([numbers.md](numbers.md) §9).
3. **Every building uses the same banding**, `tier(ℓ) = ⌈ℓ/5⌉`, so each dial core-loop writes per tier (hospital beds, helps `H = 10 + 4·(E − 1)`) keeps working unchanged.
4. **Every age honours `KEEP_ASPECT 1.50`**: silhouette steps come from caps, hoardings, towers and banners inside that frame; `cv_keep_reconcile` stays green after any keep model change.

| Age (names: story-forge) | Keep L | Visual tier (architecture.md §4) | Keep silhouette step | Opens (plates: core-loop) | Troop tiers (§6) | Resource opens ([economy.md](economy.md) §1) | Age Trial (opens at) |
|---|---|---|---|---|---|---|---|
| I Stockade | 1–5 | 1: posts, wattle, thatch | motte, palisade, timber tower | 2 crews, 1 desk, 2 banners | t1 L1, t2 L3 | food, wood, rp; gold (camps, chests) | — |
| II Timber Hall | 6–10 | 2: frame on rubble plinth, shingle | framed hall, first gable, banner pole | — | t3 L6, t4 L9 | stone (quarry), iron (mine); city gold (houses) | The First Counter (L4) |
| III Framed Keep | 11–15 | 3: dressed plinth, clay tile | 2 storeys, jettied floor, dormers | banner 3; free finish 7 min node | t5 L12, t6 L15 | — (iron ≥ 30% of troop cost from t6) | Join the Banner (L9) |
| IV Stone Keep | 16–20 | 4: dressed stone base, slate | arched gate, tower stub | desk 2, banner 4 | t7 L18 | — | Hold the Gate (L14) |
| V Castle | 21–25 | 5: ashlar, lead roofs | capped towers, buttresses | crew 3, banner 5; free finish 10 min node | t8 L21, t9 L24 | — | The Muster (L19) |
| VI Crowned Castle | 26–30 | 6: fine ashlar, gilt finials | hoardings, eight caps, heraldry | — | t10 L27, cavalry t11 L30 | — | The Tourney (L24) |

**Age Trials** — each teaches the system its age opens, the genre's untaught late systems ([onboarding.md](onboarding.md) §7 rule 7: the trial proves a skill; the first real use teaches it). *First Counter* — beat a level-3 raider camp of infantry with archers; the report names the counter. *Join the Banner* — join a rally on a camp. *Hold the Gate* — garrison a lord and hold a scripted siege. *The Muster* — lead a rally of ≥ 3 marches on a stronghold ([world.md](world.md)). *The Tourney* — one bout in the Lists, the loss-free equal-troops mode ([liveops.md](liveops.md) §4.3), where only lords' skills, talents and gear decide ([lords.md](lords.md)). Rules: ≤ 10 min including marches; loss-free (casualties return lightly wounded); unlimited free retries; a solo route always exists (NPC crown columns fill the rally, [world.md](world.md) §5); never sold, never skipped with gems.

| Fails when | Caught by |
|---|---|
| A level adds a number but nothing visible | [ ] age strip + `lvl_*` anchor check (§13) |
| Two neighbouring ages look alike from the game camera at 25% size | [ ] architecture.md §4 six-tier strip |
| A trial blocks a player with no alliance | [ ] sim profile "no alliance" passes all 5 trials solo |

## 2. The key graph — breadth without tax

The genre makes each spine level require several other buildings at nearly the same level; guides teach "raise everything to the spine level first", so players pay for levels they never use ([benchmark.md](benchmark.md)). Our rule: **a key must itself grant something the player uses, and there are never more than two.**

- **G1** Keep `L` needs exactly **two keys at level `L − 1`**: the age's *pillar* (fixed, table below) and *any one* line hall of the player's choice (barracks, encampment, archery, arsenal or stable — the line they field).
- **G2** Age entry (L6, 11, 16, 21, 26) also needs the Age Trial; it opens at the 4th level of the age before (L4, 9, 14, 19, 24) and is played while the 5th level builds. From L14 on that adds 0 minutes; the L4 and L9 trials add ≤ 10 min each in the first session, where helps and the free finish erase the timers.
- **G3** Every key level grants **≥ +3% of that building's output or a new unlock**, shown as a delta ("beds 11,200 → 12,000"). A level whose grant is 0 cannot be a key (lint).
- **G4** **Depth ≤ 2**: keep → key → (keep, already met). The whole requirement fits on one card.
- **G5** **Keys fit inside the keep's timer**: two keys kept one level behind cost `(f_pillar + f_hall) · K(L − 1)` crew time, which must be ≤ 1.0 × `K(L)` on ONE side crew. With §3's factors: 0.57 (Age I) · 0.63 (II) · 0.77 (III) · 0.85 (IV) · 0.77 (V) · 0.97 (VI; 0.49 per crew with the 3rd crew). The keep never waits for keys while crews are busy.
- **G6** Everything else is **growth, not tax**: capped at `L`, never required by the keep.
- **G7** Each pillar serves ONE age: no building is a bottleneck for more than 5 keep levels, except the player's own line hall.
- **G8** The next age's pillar and trial show from the first level of the current age ("Age IV needs Hospital 15 — yours: 9"): a lagging pillar is never a surprise.

| Age (keep levels) | Pillar | What each pillar level grants — the use | Why this age |
|---|---|---|---|
| I (L2–5) | farm | food per hour (collected on open, core-loop A1) | the first loop: produce → build |
| II (L6–10) | warehouse | protected storage ([economy.md](economy.md)) | raids start to matter when the newcomer ward ends ([onboarding.md](onboarding.md)) |
| III (L11–15) | academy | research rows (Works row III: 7-min free finish), rp output, research speed | the research age: t5–t6 need Drill nodes (§6) |
| IV (L16–20) | hospital | beds ([combat.md](combat.md): one lost field march heals ≤ 8 h) | rallies and sieges begin |
| V (L21–25) | embassy | helps per request `H`, reinforcement capacity ([alliance.md](alliance.md)) | the alliance age: rallies of ≥ 3 marches |
| VI (L26–30) | tower | warning lead time, scout detail tier, wall archers ([combat.md](combat.md), [world.md](world.md)) | the war age: landmarks and seasons |

**Tax share** = required build-minutes spent on buildings the player does not open or use in the following 7 days ÷ all required build-minutes. Target ≤ 10% (telemetry, §13).

| Fails when | Caught by |
|---|---|
| A keep level needs 3+ buildings, or a key grants nothing | [ ] PREREQ LINT keys ≤ 2, grant ≠ 0 |
| The keep crew idles while a key is still building (G5 broken) | [ ] sim: keep-waits-for-key hours = 0 at steady state |
| Tax share > 10% | [ ] telemetry per cohort, weeks 1–8 |

## 3. The building roster — each age brings new verbs

A new archetype is itself a progression beat. An engaged free player meets 32 of the 34 within ≈ 4.3 days (§9 model); after that the beats are levels, troop tiers, research rows and Age VI's two prestige buildings. **Roles are PROPOSALS read from the names — replace each with the shipped role from `data/buildings.gd` before use; the pacing is the deliverable.** Resource entry follows [economy.md](economy.md) §1 (stone and iron at A2).

| Age | Archetypes opening (proposed role) | Count |
|---|---|---|
| I | fortress (spine) · farm (food) · lumber (wood) · barracks (infantry) · archery (archers) · warehouse (protection) · hospital (beds) · academy (research desk) | 8 |
| II | quarry (stone) · mine (iron) · house (gold rents) · encampment (spearmen) · stable (cavalry) · embassy (alliance help) · tavern (lord recruitment, lords.md) · smithy (lords' gear, lords.md) · market (trade, economy.md caps) | 9 |
| III | arsenal (crossbows) · milacademy (troop drill) · tower (watch, walls) · mill (+food) · sawmill (+wood) · well (fire and repair of a burning castle, combat.md §10) · huntlodge (camp scouting, lord XP) | 7 |
| IV | townhall (civic rights: gold, trade caps) · stonemason (+stone) · victualler (march supplies) · library (research speed, rp) · church (role to confirm) | 5 |
| V | university (advanced research, rp) · laboratory (healing speed) · monument (realm milestones) | 3 |
| VI | palace (titles, prestige) · wonder (prestige; realm or alliance role to confirm) | 2 |

**Line halls teach the counter ring in order** ([combat.md](combat.md) §2 rule 8): Age I infantry + archers (the bow breaks the blade); Age II spearmen + cavalry (the pike stops the horse, the blade gets inside the pike); Age III crossbows (the bolt beats the bow, the horse rides down the bolt) — the ring is whole. Each new line = one new counter lesson.

**Timer families** — `T(ℓ) = f · K(ℓ)`:

| Family | f | Top timer (ℓ 30) | Members |
|---|---|---|---|
| Keep | 1.0 | 10 d 00 h | fortress |
| Military and defence | 0.6 | 6 d 00 h | barracks, encampment, archery, arsenal, stable, milacademy, hospital, tower |
| Knowledge, alliance, storage, gear | 0.5 | 5 d 00 h | academy, library, university, laboratory, embassy, warehouse, smithy, tavern |
| Production and civic | 0.4 | 4 d 00 h | farm, lumber, quarry, mine, mill, sawmill, stonemason, huntlodge, victualler, house, well, market, townhall, church |
| Prestige (stat-free levels: titles, feasts — economy.md §3 layer 6) | 0.7 | 7 d 00 h | palace, wonder, monument |

City complete (all 34 at level 30) = `Σf · 46.1 d` + keep = 16.5 × 46.1 + 46.1 ≈ **807 crew-days base**. Estimate: 807 ÷ 3 crews = 269 days, minus helps (−17% on long timers at H 18), plus idle crew time → an engaged free player completes the city around **day 250–300**: the long tail is breadth the player chooses, not a wall.

## 4. Build queues (crews)

Plate counts and refill rules are [core-loop.md §2](core-loop.md): 2 masons' crews from minute one, the 3rd at Age V, **never sold**. Progression adds:

- **B1** Any crew takes any building, the keep included; the tracker marks which crew builds a key.
- **B2** **An upgrade never switches a building off**: the hospital heals, the warehouse protects, the embassy helps, the line hall trains — at the current level until the new one lands.
- **B3** Cancel: full refund within 60 s of the start (mis-tap), 50% of resources after; minutes already run are lost.
- **B4** The scaffold kit ([architecture.md §7](../../blender-forge/references/architecture.md)) stands on every building under upgrade: the city visibly works, for the owner and for visitors.
- **B5** Crew budget: keys use ≤ 1 side crew (G5); from Age V they take 39% (Age V) and 49% (Age VI) of the two side crews' time — the rest is growth.

## 5. Research tree — wide, shallow, never wrong

The genre runs a long economy tree and a long military tree, and its top troop tier needs the whole economy tree ([benchmark.md](benchmark.md)). Ours:

| Branch (names: story-forge) | Host | Covers | Keystones |
|---|---|---|---|
| Husbandry | academy | production, storage, gathering yield, gold | — |
| Works | academy | build and research speed, free-finish threshold | free finish 7 min (row III), 10 min (row V) — core-loop §4 |
| Drill | academy in Ages I–III; milacademy from Age IV | troop tiers ("Drill I…X", cavalry "Drill XI"), line bonuses, march capacity | one node per troop tier (§6) |
| Wayfaring | academy in Ages I–V; university from Age VI | march speed, scouting tiers, camp levels, hunt order length | — |

- **R1** **Rows = ages**: one row per branch per age (4 × 6 = 24 rows); a row opens at its age's first keep level and needs its host at ≥ that level − 1 (G1's rule). A host that opened late takes over one age later, so its first row never waits on a level-1 building.
- **R2** **6 node-levels per row, 8 in Age V rows** (3 nodes: unlocks 1 level, stat nodes 2–3 levels) → 152 node-levels.
- **R3** **Chains ≤ 3 inside a row; 0 cross-branch prerequisites.** A troop tier never needs a Husbandry node.
- **R4** Every node-level gives **≥ +3%** on a stat the player uses, or an unlock, shown as a delta.
- **R5** **Never wrong**: every node is reachable by everyone; no exclusive picks, no respec. Build identity lives in lords' talents ([lords.md](lords.md)), where changing it is cheap.
- **R6** Timer of a node-level in row `A` = `0.6 · K(L)` for L running across that age's five levels (top: 0.6 × 10 d = 6 d). Cost: rp (research ink) and gold — research is rp's only sink and ≈ 55% of gold spend ([economy.md](economy.md) §2 sets the mix).
- **R7** Content per age = 0.7–1.1 × the engaged free player's desk-days in that age (§9 model): less → idle desks; more → the rows spill into the next age (≤ 30%).

| Row | Node-level timers | Node-levels | Desk-days of content (base) | Engaged free desk-days in the age (§9 model) | Ratio |
|---|---|---|---|---|---|
| I–II | 6 s – 16 m | 48 | 0.1 | inside day 1 | free finishes |
| III | 22 m – 1 h 30 m | 24 | 0.8 | 1.2 (1 desk) | 0.70 |
| IV | 2 h 08 m – 8 h 41 m | 24 | 4.9 | 5.6 (2 desks) | 0.87 |
| V | 12 h 21 m – 2 d 02 h | 32 | 37.5 | 38 | 0.99 |
| VI | 2 d 14 h – 6 d 00 h | 24 | 98.8 | 92 | 1.07 |

## 6. Troop-tier bands — one new tier every three keep levels

Tier `t` opens at keep level `L_t = max(1, 3·(t − 1))`: t1 L1, t2 L3, t3 L6 … t10 L27; cavalry t11 at L30. **Three keys per tier and line**: keep ≥ `L_t`, that line's hall ≥ `L_t`, and the Drill node for tier `t` (shared by all five lines; t1 needs none). Iron enters troop costs at t4 and is ≥ 30% of the cost from t6 ([economy.md](economy.md) §4, the late throttle). Display names: [units.md](../../game-art-director/references/units.md).

| Age | Tiers | Infantry · cavalry examples | Kit look (the castle's material ladder) | Engaged / casual free, days (§9 model; keep level only) |
|---|---|---|---|---|
| I | t1–t2 | Peasant, Levy · Peasant Outrider, Mounted Scout | padded gambeson, kettle helm | first session / first session |
| II | t3–t4 | Axeman, Swordsman · Hobelar, Light Cavalry | mail shirt, timber shield | first session / first session |
| III | t5–t6 | Man-at-Arms, Heavy Infantry · Mounted Warrior, Knight | mail plus first plate | t5 0.5 / 1.8 · t6 1.3 / 3.3 |
| IV | t7 | Veteran Infantry · Heavy Cavalry | plate harness | 1.9 / 4.8 |
| V | t8–t9 | Elite Infantry, Royal Guard · Veteran Knight, Elite Knight | full plate; royal livery at t9 | t8 4.3 / 6.8 · t9 11.3 / 14.3 |
| VI | t10 (+ cav t11) | King's Champion · Royal Knight, Legendary Knight | maintained plate, gilt fittings | t10 31.5 / 39.3 · t11 69.5 / 86.3 |

- **T1** Tier steps follow [numbers.md](numbers.md) §3 (`k` ≈ 1.35–1.5) and [combat.md](combat.md) §2's rule t(n) + counter ≈ t(n+1): a one-tier gap is answerable by choosing the counter line. Target: heavy spender vs engaged free player of the same account age ≤ 1 tier apart on ≥ 95% of days 0–120 (§9 model: 99%, with or without the charter; heavy vs casual free: 96% with the charter, 93% without).
- **T2** **Promotion** (PROPOSAL; combat.md §3 rule 5 and economy.md set cost and time): when a tier opens, existing troops of the tier below can be promoted by paying the cost difference — no investment is lost to a new tier.
- **T3** The first muster of a new tier is a feel-forge moment and an alliance feed line (witness).

## 7. The timer curve by phase

Designed from player time ([numbers.md](numbers.md) §1), then produced by the tool (run from the design-forge folder):

```
python tools/curve.py --levels 30 --first 10s --last 10d --shape phased
python tools/curve.py --levels 30 --first 10s --last 10d --shape phased --helps H --help-floor F
python tools/curve.py --levels 30 --first 10s --last 10d --shape phased --csv keep.csv
```

(H, F) = (10, 120s), (18, 120s), (30, 180s): the [core-loop.md §6](core-loop.md) dials — each help removes `max(1% · R, f)`; `H = 10 + 4·(E − 1)` = 10 … 30 by the asker's embassy tier `E`; `f` = 120 s, 180 s after one alliance research node. curve.py applies helps at request time (`--help-cut` 0.01 is its default). "0" = erased by helps plus the free finish of 5 min, 7 min from Age III, 10 min from Age V:

| L | Age | K(L) | ratio | cumulative | 10 helps, 2 m floor | 18 helps, 2 m | 30 helps, 3 m |
|---|---|---|---|---|---|---|---|
| 1 | I | 10s | – | 10s | 0 | 0 | 0 |
| 5 | I | 1m34s | 1.753 | 3m27s | 0 | 0 | 0 |
| 6 | II | 2m46s | 1.753 | 6m12s | 0 | 0 | 0 |
| 10 | II | 26m03s | 1.753 | 1h00m | 6m03s | 0 | 0 |
| 11 | III | 37m00s | 1.420 | 1h37m | 17m00s | 0 (1m00s) | 0 |
| 15 | III | 2h30m | 1.420 | 8h01m | 2h10m | 1h54m | 1h00m |
| 16 | IV | 3h33m | 1.420 | 11h34m | 3h13m | 2h57m | 2h03m |
| 20 | IV | 14h29m | 1.420 | 2d00h | 13h06m | 12h05m | 10h43m |
| 21 | V | 20h35m | 1.420 | 2d21h | 18h37m | 17h11m | 15h13m |
| 25 | V | 3d11h | 1.420 | 11d18h | 3d03h | 2d21h | 2d13h |
| 26 | VI | 4d07h | 1.234 | 16d02h | 3d21h | 3d14h | 3d04h |
| 28 | VI | 6d13h | 1.234 | 27d23h | 5d22h | 5d11h | 4d20h |
| 30 | VI | 10d00h | 1.234 | 46d01h | 9d01h | 8d08h | 7d09h |

`TOTAL 46d01h to max (46.1 days of build queue)`. Age sums (base days): I 0.002 · II 0.04 · III 0.29 · IV 1.69 · V 9.76 · VI 34.29.

| Phase (numbers.md §1) | Target upgrade length | Keep levels | Ours |
|---|---|---|---|
| First session | 5 s – 3 min | 1–5 | 10 s – 1 m 34 s |
| First week | 5 min – 4 h | 6–16 | 2 m 46 s – 3 h 33 m (L6–9 erased by 10 helps + free finish) |
| First month | 4 h – 2 d | 17–24 | 5 h 03 m – 2 d 10 h |
| Endgame | 2 – 14 d | 25–30 | 3 d 11 h – 10 d 00 h |

Calendar note (§9 model): an engaged free player meets timers > 4 h from day ~2 and > 1 d from day ~5, earlier than the phase names. If week-1 telemetry shows stalls, shorten the middle with `--first 5s` (L16 3 h 33 m → 2 h 45 m, L20 14 h 29 m → 12 h 13 m, total 44.1 d); never lengthen the top.

**Resource gate `G`** = hours of the median free player's income needed for keep level L ÷ `K(L)` in hours: **I 0.3 · II 0.5 · III 0.8 · IV 1.0 · V 1.2 · VI 1.4**. `G < 1` (Ages I–III): time is the gate; a player who collects is never blocked by cost. `G ≥ 1` (IV–VI): resources become the gate ([numbers.md](numbers.md) §2), so gathering, camps and trade shorten the calendar and a passive player waits up to `G · K`. [economy.md](economy.md) turns `G` into costs with its income curves and proves them with `tools/econ_sim.py` (day-30 band 0.90–1.10).

### Why there is no four-month wall

The genre's reference game puts 126 days 3 h of base timer on its final spine level, with most of all spine cost in the last 3–4 levels ([benchmark.md](benchmark.md)). The same tool with a 126-day top rung (`--levels 25 --first 10s --last 126d --shape phased`) gives **429 days of queue, 337 of them in the last four levels**: the late game becomes a wallet check, hourglass hoarding and a rush meta.

- **W1** Ceilings: keep ≤ 10 d, prestige buildings ≤ 7 d, other buildings ≤ 6 d, research ≤ 6 d. **The lower cap wins** ([core-loop.md](core-loop.md) §4 rule 2): on these ladders these caps bind, not core-loop's 14 d; core-loop's 14 d still caps every other plate.
- **W2** The top is still the big part: the last 5 levels hold 34.3 of 46.1 base days (74%) — earned, but each step is one plan of ≤ 10 days, not a season.
- **W3** Width instead of height: Age VI adds 24 research node-levels (99 desk-days), t10 and cavalry t11, palace and wonder; the city (807 crew-days) outlasts the keep by months.
- **W4** Resources, not hourglasses, gate the late keep (`G ≥ 1`): active play is the lever.
- **W5** One upgrade absorbs at most 14,400 hourglass minutes (10 d); events score finished work, not hourglasses spent (core-loop §5, §10), so a hoard has nowhere to go.

## 8. Hand-off to art — what each age must show

At the three read distances of [architecture.md §2](../../blender-forge/references/architecture.md): **city close (180–320 px)** — the material step, the new element, one `lvl_*` detail per level; **overview (60–120 px)** — a new keep silhouette, age named in 1 s on the 25% strip; **realm map (48–96 px)** — one of six city cluster sprites, age named in 1 s. The next-age preview (N2) is an **engine render** of the real model (`core/build_thumbs.gd`, [buildings.md](../../game-art-director/references/buildings.md)), same camera as the city — never a painted promise the model does not keep.

## 9. The calendar — who reaches what, when (toy model)

**The toy calendar model** (unpublished scratch script; the progression sim of §13 replaces it). Its outputs are **estimates to check, not measurements**. Assumptions:
- **Keep path only**: keys are ready when needed (G5 holds); a troop tier counts as open when the keep reaches `L_t` (hall and Drill node assumed ready); trials take 0 min; research, raids, losses and lords are not modelled. Days = elapsed days since the account started (= realm age for founders).
- **Visits** at fixed hours every day (2 visits: 08:00, 20:00; 4: 08:00, 12:30, 18:30, 22:30; 5 and 9 spread over 07:00–23:00); the keep restarts only at a visit; levels that helps and the free finish erase chain inside one visit.
- **Helps**: `H` and floor per profile, fixed from the first visit (alliance joined at once), applied at the start of each level. In the game `H` follows the asker's embassy tier (10 at tier 1, 22–26 once the Age V pillar stands), so the model is fast early and slow late.
- **Free finish** 5 min (L ≤ 10), 7 min (L11–20), 10 min (L ≥ 21): the Works nodes are assumed researched on time.
- **Hourglasses**: up to the profile's daily allowance, spent only on the keep at a visit (a share of the ≈ 10 h/day chests give, core-loop §7; heavy = 168 h/week, inside [monetization.md](monetization.md) §4's peace allowance).
- **Resources**: income accrues continuously at the profile's multiple of the median free income, all of it for the keep, from 00:00 of day 0 (the first visit finds 8 h banked, standing in for starter stock); level L costs `G · K(L)` hours of income, paid at the start.

| Profile | Visits/day | Helps (floor) | Hourglass h/day to keep | Income ×free | Age II | III | IV | V | VI | Keep 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| Casual free | 2 | 10 (2 m) | 1 | 0.8 | 0.3 | 1.3 | 3.8 | 6.8 | 28.8 | 86 |
| Engaged free | 4 | 18 (2 m) | 2 | 1.0 | 0.3 | 0.3 | 1.5 | 4.3 | 23.3 | 70 |
| Light spender | 5 | 26 (3 m) | 4 | 1.3 | 0.3 | 0.3 | 0.8 | 2.9 | 18.3 | 54 |
| Heavy spender, no charter | 9 | 30 (3 m) | 24 | 2.5 | 0.3 | 0.3 | 0.5 | 1.4 | 9.3 | 28 |
| Heavy spender, realm charter | 9 | 30 (3 m) | 24 | 2.5 | 0.3 | 0.3 | 0.5 | 3.4 | 15.5 | 46 |

Rows 1–4 run without the charter; with it, only the light spender (Age V 2.9 → 3.9) and the heavy spender move. With core-loop's A-gates, an engaged free player holds every plate (3 crews, 2 desks, 5 banners) after ≈ 4.3 days, and Ages I–V land in the first ≈ 4.3 days (casual ≈ 6.8); Age VI carries weeks 4–10. For later age-ups raise `G` in Ages III–V — never the timer ceiling. **Rush ratio** = heavy days to keep 30 ÷ engaged free days: 0.41 without the charter, **0.66 with it** (target ≥ 0.6; [monetization.md](monetization.md) §8.1 allows ≥ 0.56).

**Realm charter** (PROPOSAL): the highest keep level that may be *started* rises with realm age — **L20 on elapsed days 0–2, L25 from day 3, L27 from day 14, L29 from day 28, L30 from day 42** (liveops numbering: realm days 4, 15, 29, 43; the last three are Mondays). How the dates were set (§9 model): the charter delays the casual and engaged free profiles by 0.0 days at every level and the light spender by ≤ 1 day; it binds only rushers. Tier gap heavy vs casual ≤ 1 on 96% of days 0–120 (93% without). The roadmap shows the dates ("Keep 29 opens on realm day 29 — in 3 d 4 h"). Existing realms start with every cap open; a merged realm takes the older realm's charter ([liveops.md](liveops.md) §8); nobody ever loses a level; a Writ of Passage into a realm whose charter is below the migrant's keep level is refused (PROPOSAL for liveops.md §7 rule 3, beside its tier check 3b).

**One realm-age gate, not two.** [liveops.md](liveops.md) §1.2 proposes troop-tier ceilings by realm age (`D_k`). Tiers follow the keep (§6), so the charter already caps them: t8–t9 from elapsed day 3, t10 from day 14, cavalry t11 from day 42 (t7 is never capped). Recommended: ship the charter and set liveops' `D_k` = the charter date of `L_t`; a second, separate tier cap is an owner decision (§14.4). Model inputs for `D_k` (engaged / casual free): t7 1.9 / 4.8 · t8 4.3 / 6.8 · t9 11.3 / 14.3 · t10 31.5 / 39.3 days.

## 10. Catch-up — late joiners, returners, slow players

The genre routes beginners to new servers and otherwise lets late starters fall behind for good; migration caps can trap them ([benchmark.md](benchmark.md)). Ours:

- **C1** Routing is [liveops.md](liveops.md) §1.1's: a fresh install lands in the newest open realm automatically (no realm menu), never in one older than 35 days. An invite link places the player in the friend's realm at any age, and a warded newcomer may move once, free ([onboarding.md](onboarding.md) §8, liveops §7 rule 1). So late joiners in an old realm are invitees, movers and returners — the players C2 serves.
- **C2** **Settled ground** (PROPOSAL): each realm records `settled_day[L]`, the realm day on which the median active player (opened the game in the last 7 days) reached keep level L. For every player, keep level L, its two keys and research rows of ages ≤ the median's age (a row uses its age's first level) cost less, in time AND resources: `d(L) = 0.5 · min(1, (realm_day − settled_day[L]) / 14)` for levels the median has reached; 0 otherwise.
- **C3** It never lifts anyone above the median, never touches training, healing, war costs, trade caps or rewards. It lowers sinks and adds no source, so a farm account has nothing to pass on.
- **C4** The same rule serves returners and slow players: whoever is ≥ 2 weeks of realm time behind the median pays half.
- **C5** Promotion (§6 T2) keeps old troops useful; the peace ward for newcomers is [onboarding.md](onboarding.md)'s.

§9 model, engaged free joiner; the discount applies to the keep's timer and cost; the realm median = the founders' engaged free path:

| Joins on realm day (elapsed) | Median keep then | Days to reach the median: no catch-up | 40%, 14-d ramp | **50%, 14-d ramp** | 60%, 21-d ramp |
|---|---|---|---|---|---|
| 30 | 26 | 70 | 38 | **24** | 36 |
| 60 | 29 | 70 | 42 | **35** | 31 |
| 90 | 30 | 70 | 42 | **35** | 28 |

Target: an engaged late joiner reaches the realm median in ≤ 45 days. The model's median is the engaged free profile; the real median is lower, so the real discount is smaller — retune from telemetry, never above 60%.

## 11. The next goal is always visible — the UI contract (ui-forge builds it)

- **N1** **0 taps**: the queue tracker's top row always shows the next keep goal in one line: "Keep 17 · needs Hospital 16 · ~2 h" (the single blocking item and its time) or "Keep 17 · ready — Upgrade".
- **N2** **1 tap** (the keep card) shows three horizons. NOW: the Advisor's action with its Start button (≤ 2 more taps). NEXT: keep L+1 — both keys (met / level needed), the cost with the missing resource named ("short 42,000 stone — ~5 h of your output"), the timer after expected helps. FAR: the next age — the engine render of the next-age keep at ≥ 40% of screen height, ≤ 6 unlock icons (Blender-made art, never line glyphs), the Age Trial, and "~9 days at your pace" (from the player's last 7 days, rounded up).
- **N3** **Locked means named**: every locked building, row, tier or plate shows its exact keys ("Keep 21 · Stable 21 · Drill VIII"). Never "???", "soon", or a shape with no requirement.
- **N4** **Numbers, not adjectives**: every upgrade shows `old → new` and the % ("food 12,400 → 13,020 / h, +5%").
- **N5** **The Advisor** is deterministic: (1) an unmet key of the next keep level, shortest first; (2) the next age's pillar if it lags its requirement by > 3 levels; (3) the player's line hall if a troop tier is ≤ 1 level away; (4) the largest grant per crew-minute. Its reason fits in ≤ 6 words ("Key for Keep 17"). It never points at a shop surface.
- **N6** No red dot for "could upgrade" (core-loop A7: dots only for claimable items and idle plates).
- **N7** At keep 30 the goal switches to breadth: "City 612 / 1,020 levels", "Cavalry t11: Stable 29 → 30", research % — never an empty "max".
- **N8** **The roadmap** (in-world: the master mason's plan; 1 tap from the keep card): 30 levels, 6 ages, unlocks, trials, charter dates, the player's position. It shows what exists, never "coming soon".
- **N9** **Age-up**: a feel-forge ceremony ≤ 4.0 s (240 frames at 60 fps), skippable after 300 ms — the one exception to core-loop A9's 1.5 s, 5 times per account; the camera frames the whole castle (transition-forge); an alliance feed line; the realm-map sprite switches.

| Fails when | Caught by |
|---|---|
| The next goal needs a tap to find | [ ] ux_flow_probe: tracker row present on every castle screen |
| A locked item shows no requirement | [ ] string scan of lock labels for "?" / "soon" = 0 |
| The Advisor's pick disagrees with the rule order | [ ] unit test over 50 saved city states |

## 12. Red-team checks — progression (SKILL.md's ten still apply)

| # | Check | Pass | Caught by |
|---|---|---|---|
| 1 | Timer ceilings | keep ≤ 10 d, prestige ≤ 7 d, other ≤ 6 d, research ≤ 6 d (lower than core-loop's 14 d: these win) | PREREQ LINT |
| 2 | No dead level | every (building, level) has grant ≠ 0 and a visible change | PREREQ LINT + age strip |
| 3 | Graph shape | keys ≤ 2 per keep level, depth ≤ 2, 0 cycles, each pillar one age; troop tier keys = 3 (§6) | PREREQ LINT |
| 4 | Keys fit the keep timer | side work ≤ 1.0 · K(L) on one side crew | PREREQ LINT |
| 5 | Tax | tax share ≤ 10% | telemetry |
| 6 | Ages read | each age changes the silhouette at 25%; `KEEP_ASPECT 1.50` at all 6 | architecture.md §4 strip, `cv_keep_reconcile` |
| 7 | Free path | keep 30: engaged free ≤ 90 d, casual free ≤ 120 d | progression sim |
| 8 | Rush bound | rush ratio ≥ 0.6; charter delays free profiles 0.0 d | progression sim |
| 9 | Tier gap | heavy vs engaged free ≤ 1 tier on ≥ 95% of days 0–120 | progression sim |
| 10 | Catch-up | late joiner reaches the median in ≤ 45 d | progression sim |
| 11 | Next goal | 0 taps to see, ≤ 3 taps to start (core-loop §8.2 step 4) | ux_flow_probe |
| 12 | Money opens no gate | no crew, desk, trial, key, charter date or discount on a paid surface | shop-forge offer grep = 0 |
| 13 | Exploits | farm accounts: settled ground lowers sinks only, trade caps need account age (economy.md); sandbagging: event brackets use power + top troop tier, not keep level (liveops.md); migrants vs charter: refused; hollow keep: pillars keep warehouse, hospital, tower in step | review + sim |
| 14 | Model vs sim | no §9 model figure quoted as measured; the sim reproduces §9/§10 within ±10% or the tables are replaced | review |

## 13. Harness, data, save, server cost

| Proof | Measures | Verdict line (PROPOSED wording; qa-forge fixes it; example values = §9 model) |
|---|---|---|
| progression sim (new; qa-forge; path to confirm) | 4 profiles × 120 days, no-alliance profile, late joiners at days 30/60/90; §9 and §10 tables | `PROGRESSION SIM OK - keep30 casual 86d free 70d light 54d heavy 46d (rush 0.66), charter delay free 0.0d, tier gap<=1 99%, late-join to median <= 35d` |
| PREREQ LINT (new; qa-forge; levels per §14.2) | `data/buildings.gd` + research + troop data | `PREREQ LINT OK - 34 archetypes x 30 levels, 0 cycles, keys<=2, depth<=2, dead levels 0, max timer keep 10d00h other 7d00h research 6d00h, side work <= 0.97 K` |
| age strip (blender-forge `tools/rarity_sheet.py`) | 6 keep tiers + 6 cluster sprites at 25% | every neighbour pair differs; `cv_keep_reconcile`, `structure_audit`, `placement_test` stay green |
| `tools/curve.py` · `tools/econ_sim.py` | §7 tables; `G` → costs (economy.md) | tables reproduce exactly |
| ux_flow_probe, session_audit | N1–N5 taps | existing lines |

**Data** (gameplay-forge): per building `level` (1–30, or 1–6 if §14.2 keeps tiers) and `upgrade {start_unix, duration_s, target}`; research node levels; `trials_passed` (5-bit mask); per realm the static charter table and `settled_day[1..30]`.
**Save migration**: old saves load with the trials of every age already reached marked passed; if 30 levels are adopted over shipped 6-tier data, `ℓ_new = 5 · T` (top of the same visual tier: nobody sees a smaller castle and no next step gets harder); running upgrades finish at the mapped level.
**Server cost** (budget: €200/month at 50,000 players): no new write type — upgrade and research starts are core-loop plate starts (≈ 15 per player per day, inside core-loop's ≈ 2.9 M writes/day at 50,000 players). Added: ≤ 1 trial resolution per player per day (a camp-type resolution) and 1 snapshot job per realm per day (median + `settled_day`: 31 integers). Timers, discounts and charter caps are computed, never ticked. Measure with `core/sd_cost_probe.gd`.
**After ship**: age reached by day per cohort vs §9 (±25%; replace the model rows with cohort data); share of keep starts from the Advisor; tax share; keep-crew idle ≤ 15% of waking hours in weeks 1–2; D7 of players reaching Age IV by day 3 vs later.

## 14. Owner decisions required

1. The spine archetype: fortress (the keep) — or the one the shipped data already gates on.
2. 30 levels in six ages of five over the shipped 34 archetypes × 6 tiers, and the `ℓ = 5 · T` migration if adopted (the alternative: keep 6 steps; every rule here still holds).
3. Age Trials as unbuyable keep gates (one per age entry, five in all).
4. The realm charter dates (they slow spenders: a spend decision), and whether liveops.md §1.2's tier ceilings ship beside it (recommended: the charter only, §9).
5. Settled ground size: 50% with a 14-day ramp.
6. Timer ceilings: keep 10 d, other buildings 6–7 d, research 6 d (lower than core-loop's 14 d; the lower cap wins).
7. The age-up ceremony exception (≤ 4.0 s) to core-loop A9.
8. Names (story-forge canon): ages, trials, research branches, Settled ground, Realm charter (alliance.md's research is also called "Charters": one must change), the master mason's plan.
9. Any dial here that collides with a shipped sacred constant (the shipped value wins until decided).
