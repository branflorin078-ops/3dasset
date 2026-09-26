# World — the realm map: rings, gates, landmarks, camps, marches, zoom, cost

The RULES of the shared map: how many players share one realm, how its geography paces progress, what can be fought over and when, what every player sees at every zoom, and what it costs to serve. Implementation: **world-forge** (map, simulation surfaces, rendering), **cloud-forge** (storage, streams, arrival jobs), **transition-forge** (camera, zoom thresholds, hysteresis), **battle-forge** (the march and battle experience), **blender-forge** (set-pieces, `references/architecture.md`), **ui-forge** (HUD per zoom), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md), world section.

**Every number here is a PROPOSAL** unless it quotes a canonical fact or a sibling reference. Read the shipped map first (world-forge scope; paths to verify): `godot/world/world_map.gd` (TerrainField, realm seed), `camera_rig.gd` (fixed 55° pitch), `march_out.gd`, the camp ladder (`tools/blender/generators/barbarians.py`, 6 stages), AI lords (routines, grudges, raid pressure held to the balance corridor). A shipped sacred constant keeps its value; this file's value becomes an owner proposal. Quoted, never redefined: Resolve, banners (= march slots), war windows ([core-loop.md](core-loop.md)); line speeds, loss rows, scouting and warning tiers, breach ([combat.md](combat.md)); Hall, standards, pacts, Treasury ([alliance.md](alliance.md)); realm age arc, campaigns, merges ([liveops.md](liveops.md)); node and vein yields ([economy.md](economy.md)); the peace ward ([onboarding.md](onboarding.md)).

**Terms.** *tile* = the placement cell (a castle covers 3 × 3). *chunk* = 10 × 10 tiles (fog, territory, static data). *sector* = 80 × 80 tiles (live stream). `v_ref` = 10 tiles per minute (speed factor 1.0). *Age* `A` = ⌈keep level ÷ 5⌉ = spine stage S1–S6 ([progression.md](progression.md)). *Ring* = outer / middle / inner zone (economy.md's word). *Tier* 1–4 = landmark tier with liveops hold values 1 / 2 / 4 / 8. *Home war day* = Saturday of contest weeks, and Tue/Thu/Sat before a realm's first campaign, inside the realm's window pair ([liveops.md](liveops.md) §3.2–3.3). Kept apart: *fog* here is fog of war, not the atmospheric fog of `lighting.gd`; a *region* (named area) is not *region zoom*; the boards' "dark pine marches" are called **the Pinewood** so *march* means only an army on the move; physical flags on set-pieces are *flags*, territory markers are *standards* (alliance.md).

## 0. The four questions

- **Want**: a castle in a good place; the alliance's flag on a landmark everyone sees; the crown seat and its offices; the next ring's richer camps, nodes and veins; a charted realm.
- **Obstacle**: distance in march minutes; gates (taken early by conquest, opened to all by the calendar); holders who fight back in war windows; camp levels won one by one; Resolve; fog.
- **Wait**: first camp march ≈ 25 s; own region charted by realm day 7; tier-1 landmarks from day 8; passes open to all on day 22; the First Crown on day 27, then every home war day.
- **Witness**: public march lines and tokens; holders' flags and territory at realm zoom; the crown's chronicle line; the Crown Regent's title and the offices on profile cards.

## 1. Realm capacity — how many players share one map

[liveops.md](liveops.md) §1.1 fills a realm with `N_fill` = 8,500 registrations over ≤ 21 days (peak DAU₇ ≈ 1,700 in its retention model) and asks this file for the capacity `A_design`.

| Dial | PROPOSAL | Why |
|---|---|---|
| `A_design` (peak DAU₇ the map holds) | **2,000** | 1,700 peak + 15%; migration and merges stop at it (liveops §7–8) |
| `C_design` (castles on the map at once) | **6,000** | estimated peak ≈ 4,000 on day 21 once day-1 churners are archived (§15 A8); realm_sim measures it |
| Map | **800 × 800 tiles**: 6,400 chunks, 100 sectors; side = 800 × √(C_design ÷ 6,000) | 107 tiles per castle at `C_design` (≤ 20% impassable) → neighbours ≈ 9 tiles (54 s) apart. `N_fill` 12,000 needs `A_design` 2,600 and ≈ 900 × 900 |

| `N_fill` | Peak DAU | DAU day 90 / 180 | Alliances with ≥ 15 daily actives, day 90 (50% of DAU in alliances of ~30 actives) | Viewers at the crown in a home window (≈ 10% of peak DAU) | Verdict |
|---|---|---|---|---|---|
| 3,000 | 600 | 150 / 105 | ≈ 2 | ≈ 60 | dying (DAU₇ < 300) from ≈ day 30; an empty ladder |
| **8,500** | 1,700 | 425 / 300 | ≈ 7 | ≈ 170 | **recommended**: 6–10 contenders for 180 days |
| 12,000 | 2,400 | 600 / 420 | ≈ 10 | ≈ 240 | acceptable on a 900-tile map |
| 25,000 | 5,000 | 1,250 / 875 | ≈ 20 | ≈ 500 | blocs form; naive hot-spot traffic ≈ 70× that of 3,000 |

**Cost does not choose N** once §16's rules hold: marches are functions of time and every viewer gets a capped stream, so map cost grows with players, not with players per realm. Per-realm jobs (realm summary ≤ 1,440 writes per day, calendar, AI lords) favour fewer, larger realms but are < 2% of map cost; the hot spot favours small realms only when crowd mode (§16) is missing — deliveries then grow with viewers² per contested landmark. **Social density chooses N**: ≥ 4 alliances with ≥ 15 daily actives (liveops' dying line) until day 180.

**Checks**: [ ] realm dashboard + realm_sim on-map line — fails when: on-map castles > `C_design` or DAU₇ > 0.9 × `A_design` · [ ] map load test at 1,700 and 2,600 DAU (§18) — fails when: map cost per player rises with realm size.

## 2. Geography is progression — rings, gates, the founding calendar

Pattern ([benchmark.md](benchmark.md)): concentric zones gated by passes, richer inward. Our moves: gates are taken **early by conquest** but open to **everyone by the calendar**, so no ring stays locked behind one alliance; and the geography is one story — two rivers rise in the Crown Vale, cut a gorge around it, run out through the hills, split the Heartlands and end in the Fens.

| Ring (regions) | Band (tiles from centre) | Area | Castle share (target) | Camp levels | Nodes and veins (economy.md) | Strongholds | Entered by |
|---|---|---|---|---|---|---|---|
| Outer — **the Heartlands**, green river lowlands (8 open + 2 **Fens**) | > 250 | 69% | 60% | 1–12 | N 1–3; veins on N 3 ground | L1–2 | spawn; **fords** between regions |
| Middle — **the Hill Country**, stone hills, the Pinewood on its inner slopes (4) | 105–250 | 25% | 32% | 10–22 | N 3–5; iron seams; veins | L3–4 | 8 **passes** through the escarpment |
| Inner — **the Crown Vale**, inside the river gorge (1) | ≤ 105 | 5% | 8% | 20–30 | N 5–6; seams; veins | L5–6 | 4 **bridges** over the gorge |

Veins per ring follow the castle share (60 / 32 / 8%), so no ring lacks the free gem route ([economy.md](economy.md) §11). **The Fens** (2 outer regions at the river mouths) are **reserve land**: flooded until the first merge or migration wave needs blocks (liveops §8 rule 3), then drained with a chronicle line; ≈ 1,450 castles placed by alliance in blocks; new castles never spawn there.

**Terrain factor** (combat.md §3 asks this file): open ground 1.0 · Pinewood 0.85 · a ford crossing 0.6 for its 3 tiles · pass and bridge 1.0 (roads) · drained fen 0.9. Mountains, the gorge and river channels away from fords and bridges are impassable; ≤ 20% impassable per ring.

**Distances are designed in minutes** at `v_ref` (numbers.md §1 applied to space): castle → own-level camp or neighbour 1–3 min (10–30 tiles) · rally point → contested landmark 1–3 min (core-loop §8.3's 60–180 s) · castle → a node of the player's level 2–6 min · across one outer region ≈ 20 min · map edge → Crown Vale rim ≈ 30 min (300 tiles) without a seat move.

| Realm day | Opens on the home map |
|---|---|
| 1 (Mon) | castles land in the 8 open Heartland regions; every gate closed ("the spring flood"); great places charted on the parchment (§7) |
| 8 | tier 1 contestable (watch-posts, fords) on war days |
| 15 | tier 2 (chapels, passes); **fords open to all** |
| 22 | tiers 3–4 (abbeys, bridges, hillforts); **passes open to all** |
| 27 (Sat) | **the First Crown**: alliances holding a bridge reach the Vale; contested in both windows |
| 36 | **bridges open to all** |
| first contest week (realm day 36–64) | home fighting moves to Saturdays; Tue/Thu go to the Debatable Land (§14) |

Before a gate opens to all, only its holder's members path through it; others see "No road — <the ford> is held by [TAG]" or "…flooded until day 15" (battle-forge `flows.md` §3). After opening, a held gate is a **rally point**: the holder's rallies form there.

**Checks**: [ ] pathfinder unit test on days 14/15, 21/22, 35/36 — fails when: a ring stays closed past its calendar day · [ ] realm_sim camp-distance line — fails when: a castle's nearest own-level camp is > 3 min away.

## 3. The landmark ladder

Pattern: a ladder of contested places so every alliance size has a goal and the top is visible to all. Our moves: every rung pays at its size; **no landmark grants combat stats** (counters stay readable, [combat.md](combat.md) §5); the top pays in standing, not in Treasury.

| Tier (value) | Landmark — set-piece (blender-forge) | Count | Ring | Grants the holder alliance (economy.md §6: +3–8% city output of ONE resource) | Cap per alliance |
|---|---|---|---|---|---|
| 1 (1) | **Watch-post** — timber tower, brazier at the top | 24 (3 per open region) | outer | +3% wood; vision 20 tiles | 4 of tier 1 |
| 1 (1) | **Ford** — stepping stones, toll hut, marker post | 12 | outer | +3% food; crossing before day 15; rally point | (shared) |
| 2 (2) | **Chapel** — stone chapel with a bell-cote | 12 (8 outer, 4 middle) | outer, middle | +4% food | 3 of tier 2 |
| 2 (2) | **Pass** — gatehouse in a rock cleft | 8 | outer/middle edge | +4% stone; crossing before day 22; rally point | (shared) |
| 3 (4) | **Abbey** — cloister, scriptorium, church tower | 8 (2 per hill region) | middle | +6% gold | 2 of tier 3 |
| 3 (4) | **Bridge** — fortified bridge, gate tower mid-span | 4 | gorge | +6% iron; crossing before day 36; rally point | (shared) |
| 4 (8) | **Hillfort** — old royal earthwork and stone hall on a crag | 4 (1 per hill region) | middle | +8% iron; vision 30 tiles; rally point | 1 |
| crown (16) | **Crown seat** — the old royal hall inside a ring wall | 1 | inner | the **Crown Regent** and five offices | 1 |

Total 172 points; the caps hold one alliance to 42 (24%). Each set-piece is a distinct silhouette at region zoom and a distinct 32 px icon at realm zoom, flies the holder's flag (tint mask, architecture.md §7) and is built with real construction (architecture.md §5–6: 3–8k tris, LOD2 300–800).

1. **Contest** only inside home war windows, from the tier's opening day: beat the garrison (neutral guardians, then the holder's reinforcements; losses combat.md §6 row 6); the holder **at window close** keeps it. Holds and captures feed liveops §3.4 standings.
2. **Guardians** are sized to a rally of 3 / 5 / 8 / 12 marches of the realm's median castle for tiers 1–4, and 15 marches plus walls for the crown (gameplay-forge tunes; siege-forge walls).
3. **The crown term** is one week. Each home war day, the alliance that held the seat **longest summed over both windows** wins it, so the time zone of the later window does not decide; guardians holding → no Regent that week. The holder's Liege becomes **Crown Regent** and appoints within 12 h: Master of Works (+10% build speed), Chancellor (+10% research), Master of Musters (+10% training), Almoner (+10% healing), Master of Roads (+10% march speed, home map). ≥ 2 of 5 go to players outside the Regent's alliance; nobody holds an office two terms running; no debuff offices; nothing combat.
4. **Treasury** (alliance.md §4 asks for the rate): held points `P` pay **50·P marks per day** and cost **8·P^1.5 per day** to hold — functions of time, settled on any Treasury read.

| Points held `P` | 4 | 8 | 17 (best) | 25 | 32 | 39 | 42 (cap) |
|---|---|---|---|---|---|---|---|
| Net marks per day | +136 | +219 | **+289** | +250 | +152 | +2 | **−78** |

Read it: at its best a landmark portfolio is ≈ 5% of a median alliance's Treasury income (alliance.md §7 implies ≈ 6,150 per day); past 39 points holding costs marks. The crown is held for standing, not income.

**Checks**: [ ] data lint — fails when: a landmark effect is outside {output, vision, crossing, rally point, office} · [ ] capture unit test — fails when: an over-cap capture is accepted or refused without a message · [ ] crown unit test (tie and split-window cases) — fails when: the later window wins by rule.

## 4. Barbarian camps — the PvE ladder

1. **Levels 1–30** in the shipped **6 visual stages** of 5 levels (verify that barbarians.py maps this way); each stage changes silhouette (architecture.md §4). Each camp shows its main line — the counter hint (onboarding.md, combat.md §2).
2. **Unlock**: a win against level L opens L+1 (onboarding.md). Catch-up floor: levels ≤ 5·(A − 1) open by themselves (age II → 5, age VI → 25); 26–30 are always earned.
3. **Seeded spawn**: `hash(realm seed, chunk, 30-min epoch)` places 2 camps per chunk (3 in the inner ring) — 0 spawn writes, as nodes (economy.md §5). 70% follow the ring's band; 30% are **wandering bands** at the sector's median unlocked level ±1 (daily sector summary), so geography never caps an outer-ring player.
4. **Density**: ≥ 5 camps of levels [U−2, U] within 30 tiles (3 min) for ≥ 95% of castles (U = highest unlocked). Headroom at `C_design`: 56 slots × 48 epochs = 2,688 kills per day in that radius vs ≈ 640 demanded (26 castles × 24).
5. **First camp**: each new castle gets a personal level-1 camp 4–5 tiles away (≈ 25 s, onboarding.md step 6), seeded by castle id, visible to its owner for 24 h.
6. **Resolve** 10 per camp; hunt orders take up to 5 (core-loop §3). A camp killed first by someone else: the march re-targets the next hunt camp or returns, Resolve refunded. Camps never attack. The server re-computes the hash at attack time — a client cannot invent a camp.
7. Rewards: [economy.md](economy.md) (camps ≥ level 5 drop iron) and [lords.md](lords.md) (XP).

**Checks**: [ ] realm_sim camp line per ring — fails when: < 95% of castles have 5 own-level camps within 3 min, or an age-VI outer-ring player finds none above level 12.

## 5. Strongholds (ash-holds) — rally-only alliance PvE

| Level | Ring | Per realm | Respawn after a kill | Min marches | Leader Resolve |
|---|---|---|---|---|---|
| 1–2 | outer | 16 (2 per open region) | 6 h | 3 | 20 |
| 3–4 | middle | 12 | 8 h | 5 | 20 |
| 5–6 | inner | 6 | 12 h | 8 | 30 |

Seeded per region and epoch; a kill writes one record that suppresses the hold until respawn. Level L+1 opens for an alliance after it kills L. Never inside any territory. Join window ≤ 60 min (combat.md §9); Spoils and gifts: alliance.md §6.

**Reward split** = alliance.md §8 (50% equal, 50% by damage), then liveops R8 (floor 40%, cap 3× the median share; clamp, rescale the rest). Worked, 8 marches, pool 100 — damage 35/20/15/10/8/6/4/2 → **23.8 / 16.3 / 13.8 / 11.3 / 10.3 / 9.3 / 8.3 / 7.3** (pure damage share: 35 … 2; smallest ÷ largest 0.31 vs 0.06). One dominant march, damage 70/10/6/5/4/3/1/1 → 41.3 capped at 25.5, the rest rescaled: **25.5 / 14.3 / 11.7 / 11.1 / 10.5 / 9.8 / 8.6 / 8.6**. PROPOSAL to alliance.md: the equal half needs a march ≥ 20% of the rally's median march (stops one-troop leeching). ≤ 5 reward shares per player per day (alliance.md's paid rallies).

**Crown columns** (onboarding.md "Lead a rally", progression.md "The Muster"): a stronghold rally still below its minimum at 50% of the join window gets up to 2 NPC columns at the leader's median march size — for a leader's first 3 stronghold rallies, or an alliance with < 10 members active in the last hour. Their damage counts for the kill; players share 100% of the pool.
**The Warlord's Hold** (liveops §4.2): appears Wed 00:00 on the open site nearest the Hall, 2–4 chunks outside the alliance's border (20 tiles from the Liege's castle without a Hall); only that alliance may attack it; gone Fri 23:59.

**Checks**: [ ] reward-split unit test, 5 distributions + the NPC case — fails when: the smallest qualifying joiner gets < 40% of the median share, or a crown column takes a share.

## 6. AI lords — what they are for

12 AI lords (1 per open Heartland region + 1 per hill region), each with a castle (rally-only; walls, gate, towers — siege-forge; level = realm median age + 1, ≤ 6), 3 outposts (solo) and seeded **hosts** patrolling between them ([lords.md](lords.md) counts host kills). Resolve 20 per outpost or host; castle rally leader 20 ([core-loop.md](core-loop.md) §3).

| Role | Rule | Number |
|---|---|---|
| Teacher | only onboarding.md's two scripted raids (step 1, chapter 6); nothing else hits a warded castle | 2 per player |
| Living map | hosts are seeded functions of time computed on clients (0 writes); a kill writes one suppression record | per sector: hosts = max(0, 6 − player marches per hour), ≤ 6 |
| Grudge | outpost / host / castle attacks add 1 / 1 / 3 grudge; at ≥ 5 in 7 days one raid lands in 2–24 h, warned ≥ 10 min ahead, at 50–70% of the castle's defence; home never kills (combat.md §6 rule 1) | ≤ 1 raid per player per day; 0 unprovoked |
| Siege school | AI castles are where engines meet walls without PvP losses | camp loss context (combat.md §6) |
| Filler | in a Thinning realm (liveops §8), host density × 2 | dead screens ≤ 5% |

Limits: AI lords never hold tier ≥ 2 landmarks, never rank, never get offices, never move, never raid a castle whose owner has not attacked them. The shipped raid-pressure corridor stays the ceiling; this file proposes grudge-only pressure inside it.
**Checks**: [ ] ward_test (onboarding.md) — fails when: an AI raid lands on a warded castle outside the two lessons · [ ] AI unit test — fails when: an unprovoked raid, or a second raid in 24 h, is scheduled.

## 7. Fog of war and scouting

1. **Unit** = chunk: 6,400 per realm → an 800-byte bitset in the save, written ≤ once per 5 min while it changes. Clearing is permanent.
2. **The parchment**: fog is painted cartographer's parchment (PARCHMENT family) with sketched contours, never grey smoke. **Great places are printed on it from day 1** — region names, gates, landmarks, the crown seat — so the next goal is visible. Fog hides terrain detail, castles, camps, nodes, veins, strongholds, AI lords, finds and marches, except marches aimed at you or your alliance.
3. **Starts cleared**: 5 × 5 chunks around the castle. Every own march clears the chunks its path crosses (rides the next save).
4. **Scouts** (a plate under core-loop §2 rules; no banner, battle-forge `flows.md` §2): 2 at start, a 3rd with the huntlodge (age III, progression.md). Speed 3 × `v_ref`. Target: a fogged chunk within 3 chunks of cleared ground; clears 3 × 3 chunks, 5 × 5 with the Wayfaring research row. **Scout the frontier** = 1 tap sends every idle scout to the nearest fog in the direction of the region's gates and landmarks.
5. **Finds**: ≈ 40 per outer region (cairns, hermit huts, lost wagons, roadside shrines): 1-tap claim once charted; own-production hours (economy.md), lord XP, a chronicle line (story-forge).
6. **Pace**: an outer region ≈ 440 chunks; 2 scouts × 4 check-ins × 9 chunks × 60% new + march paths ≈ 58 chunks per day → **≥ 80% charted by realm day 7**.
7. **Alliance share**: joining reveals, as icons, every landmark, stronghold, AI castle and member castle any member has charted.
8. **Server truth**: every order checks its target chunk against the server's copy of the bitset; a modified client that draws through fog cannot act on what it draws. Scout reports: combat.md §11 levels L1–L5 and report-forge.

**Checks**: [ ] cohort telemetry + realm_sim fog line — fails when: < 80% of day-7 actives have charted 80% of their region · [ ] server rule test — fails when: an order targets an uncharted chunk.

## 8. Alliance territory — the map rules

[alliance.md](alliance.md) §7 owns who places, cost, cap (`min(200, 3 × 7-day actives)`), upkeep and fading.

1. The **Hall** claims 3 × 3 chunks; each **standard** claims 1 chunk sharing an EDGE with own territory. Median 60 standards ≈ 69 chunks; the cap ≈ 209 chunks = 3.3% of the map.
2. Placement: the Hall ≥ 3 chunks and standards ≥ 1 chunk from any tier ≥ 2 landmark; ≥ 1 empty chunk between two alliances' land.
3. **Cut off**: a standard with no edge path to the Hall gives nothing and fades after 24 h unless reconnected — supply lines matter.
4. Standards and the Hall are attacked only in home war windows (combat.md §6 row 6); a burned standard's chunk turns neutral at once; the Hall never fades, a sacked Hall pauses benefits for 24 h.
5. Territory never evicts a castle and never blocks a path. Strongholds and gem veins never spawn inside any territory; camps and nodes do (+20% gathering inside for members, economy.md §6).
6. **Border warning**: members see "Hostile march crossing <border> in 0:30" 30 s before a hostile path enters (+30 s per Beacons level, alliance.md §5).
7. **Look**: the border is smoothed (marching squares, 1.5-tile corner radius) so the chunk grid never shows; standards are real set-pieces (pole, cloth in the alliance's tinctures, a small palisade ring).

**Checks**: [ ] territory unit test — fails when: a cut-off standard still pays, a claim touches another alliance's land, or a vein seeds inside territory · [ ] realm-zoom screenshot — fails when: a chunk step is visible on a border.

## 9. Seat moves (relocation)

| Move | Where to | Source | Limit |
|---|---|---|---|
| Newcomer's passage | another realm | free, once, while the ward holds ([onboarding.md](onboarding.md) §8) | — |
| **Charted move** | a chosen open site in any ring whose gate is open to you, outside other alliances' land | seat-move writ: season track (2 per campaign), events; hold ≤ 2 | cooldown **72 h** (Summons −12 h per level, alliance.md §5) |
| **Hall summons** | an open site inside own territory (ignores gates) | Quartermaster, 1,000 Merit, 1 per week (alliance.md §4) | same cooldown |
| Breach move | own territory or own region | free, once, in the 8 h breach truce ([combat.md](combat.md) §10) | no cooldown |
| Arrival move | own region | free, once within 7 days of migration or merge ([liveops.md](liveops.md) §7–8) | — |
| Return | an open site in the old region | automatic when an archived player comes back (§15 A8) | return ward (onboarding.md) |

There is **no random move**: combat.md §10 rejected it — a scatter throws a player away from the alliance.

1. **Never away from an attack**: blocked from the launch of any hostile march or rally march at your castle until 30 min after the last arrival ([monetization.md](monetization.md) §3 row 7), while any own march is out, and in every war window.
2. After a move, the castle cannot launch a castle attack for 10 min, and castles within 30 tiles see "A lord has settled nearby".
3. **No gem advantage**: writs are never sold in contest weeks; if at all, only in Truce weeks (monetization.md owner decision 5). The 72 h cooldown binds payer and free player alike.
4. Landing: an open 3 × 3 site, not inside another alliance's land, not within 2 chunks of a tier ≥ 2 landmark. The peace ward survives seat moves (onboarding.md §4).

**Checks**: [ ] march_probe seat-move cases — fails when: a move succeeds with a hostile march on the road, inside a war window, or before the cooldown ends · [ ] shop-forge offer grep — fails when: a writ SKU is live in a contest week.

## 10. Lawful targets by time (home map)

| Target | Outside war windows | Home war windows |
|---|---|---|
| Camps, strongholds, AI lords, empty nodes and veins | yes | yes |
| Another player's gathering march (combat.md §6 row 5); a warded player's marches on camps and nodes ≤ level 2 are refused (onboarding.md §4) | yes | yes |
| Another player's castle — plunder only, walls untouched | yes, at combat.md §6 **row 8** losses (60% of the attacker's casualties die) | row 7; walls take damage, breach possible |
| Standards, the Hall, landmarks, the crown seat | no | yes, from their opening day |
| Castles of realm-mates on campaign days (Tue/Thu of contest weeks) | no — the realm musters as one | no |

**Checks**: [ ] server rule test, one case per row — fails when: a forbidden target resolves.

## 11. Marches on the map

1. **Record**: combat.md §8, plus the time at each waypoint (≤ 8 × u32), because terrain factors make speed piecewise; `pos(t)` interpolates between the two waypoints around `t`. No server tick moves a march; combat.md §8's arrival job is the only trigger (alliance.md's pledged departures are future-dated records).
2. **Speed** = slowest line (combat.md §3; cavalry 1.5) × (1 + pool ≤ 0.5; Roadwardens inside own territory counts in the pool) × terrain (§2).
3. **Paths**: one deterministic, versioned pathfinder on client and server — A* on the chunk graph with gates as mandatory nodes, then tile smoothing, ≤ 8 waypoints. Impassable ground, castles and closed gates block; armies and territory never do. Clients rebuild paths from (from, to, gate-state version), so the stream carries no path bytes.
4. **A castle attack arrives ≥ 90 s after its order**: a march that would arrive sooner waits at its gate, visibly mustering, so combat.md §11's warnings always have 90 s to matter.
5. **Interception** (combat.md §8) needs vision of the target at order time: 20 tiles around own castles, 5 around own marches, own territory, held watch-posts (20) and hillforts (30). Eyes decide ambushes.
6. **Public** (anyone whose view shows a charted chunk): line, direction, relationship style, ETA and battle-forge's token (3 figures of the largest line, the lord banner, the line medallion). **Not public**: counts, tiers, the second lord, engines — only scouting (combat.md §11, L1–L5) and warnings (E1–E6) reveal them. The live stream carries public fields; the rest is fetched on tap with a rights check.

**Checks**: [ ] march_probe — fails when: client and server `pos(t)` differ in fixed point, or a castle attack arrives < 90 s after its order · [ ] packet audit — fails when: a stream record carries counts or tiers.

## 12. Relationship colours — the reserved channel

The single source of the four values (alliance.md §7 names this file); ux.md, game-art-director `readability.md` and chat-forge `ui.md` cite it and never restate it.

| Class | Who | Colour | Hex | Marker (chat-forge set) | March line (1080 px short side) |
|---|---|---|---|---|---|
| Self | you | Hearth white | `#FAF6EA` | circle | 6 px, long dash 24/8 |
| Ally | own alliance; Accord partner (alliance.md §12) | Ally blue | `#2042D8` | heater shield (Accord: shield with a bar) | 6 px long dash (Accord: dash-dot) |
| Enemy | anything aimed at you or at your alliance's castles, standards, Hall or held landmarks; for 24 h, every march and castle of an alliance whose member attacked yours; other realms on the Debatable Land | Foe vermilion | `#FF4F19` | crossed blades | 6 px chevron dashes; 8 px with a pulse ≤ 1 Hz when aimed at you (battle-forge `flows.md` §5) |
| Neutral | everyone else: other players, barbarians, AI lords, guardians | Fallow grey | `#786868` | square | 4 px dots, 60% opacity |

**Measured** (Machado 2009 full-severity simulation on linear RGB, CIEDE2000): the four are ≥ 30.2 apart for normal vision, 23.7 protan, 30.3 deutan, 26.5 tritan; each sits ≥ 17 from every palette token, line accent and rarity colour, except Hearth white vs PARCHMENT (10) — hence the keyline.

1. **Stroke recipe**: colour core + 2 px INK keyline + 1 px PARCHMENT halo at 60%. INK carries the mark on light ground, the halo on the dark Pinewood — it never sinks into terrain.
2. **Red is earned by a threat**, not by strangers: a calm map is mostly Fallow, so vermilion always means "this concerns you".
3. **Never colour alone**: each class has its marker shape and line pattern; the greyscale test (§18) must tell all five patterns apart.
4. **Reserved**: never in UI chrome, rarity, events, offers or decoration; alliance tinctures sit ≥ 15 ΔE00 from all four. On buildings, the ground ring and pole finial carry the relationship; flag cloth carries the alliance's tinctures (alliance.md §7).
5. The stream carries alliance ids; the client computes the class (viewer's alliance, pacts, threat list), so one stream serves every viewer.

**Checks**: [ ] relation palette check (§18) — fails when: any pair < 20 ΔE00 in any simulation, or a tincture < 15 from a relationship colour · [ ] a11y_audit colour-blind pass — fails when: a class is told apart by colour alone.

## 13. Zoom levels — the content contract

Level names and the camera are **transition-forge**'s (thresholds, hysteresis, streaming); HUD per level is ui-forge's (`references/architecture.md` §1). This table is what each level must SHOW, at the 1080 px short side.

| Object | Castle close | Castle overview | Region | Realm |
|---|---|---|---|---|
| Own castle | full 3D (castle-forge) | full 3D, walls, gate, Self ring | 3D cluster 48–96 px (architecture.md §2) + ring + name | crest 28 px + ring, always |
| Other castles | — | within 10 tiles, with rings | 3D cluster + relationship ring | alliance members as 6 px dots; others as density shading |
| Token squads | the march-out at the gate (battle-forge) | own squads 60–90 px | 40–56 px (battle-forge `flows.md` §5); ≤ 60 animated, the rest 32 px banner icons | own, own rallies, hostile-to-own: 16 px pips |
| March lines | — | own only | every public line in its class style | own, own rallies, hostile-to-own: 3 px |
| Camps, strongholds, AI | — | within 10 tiles | set-pieces + level plate 28 px + main-line hint | own-alliance strongholds and AI castles: 20 px icons |
| Nodes, veins | — | within 10 tiles | set-pieces + level + occupant ring | charted veins: 14 px glints |
| Landmarks, gates | — | — | set-piece 80–140 px + holder flag + name | 32 px icon (crown 44 px) + holder ring + sigil, through fog |
| Territory | — | own border as a ground decal | border 4 px + 10% fill | 30% fill + 2 px border + sigil 40 px (≥ 20 chunks) |
| Labels | — | — | ≤ 40; self > aimed at me > own alliance > landmarks > bookmarks > camps at my level; others on tap | 15 region names; tier ≥ 3 and own holdings |
| States | HUD warning with exact ETA | incoming: ring breathes at 0.5 Hz | burning smoke + "Burning" (combat.md §10), ward dome | burning / warded icons for own and alliance castles |

Budgets: region ≤ 150 markers and 0 label overlaps (battle-forge merges ≥ 4 tokens within 60 px into a chip); realm ≤ 400 icons drawn as MultiMeshInstance3D, one draw call per icon family. **No dead screens**: ≥ 95% of random region views show ≥ 3 moving things and ≥ 1 place of interest (AI hosts top up, §6) — the owner's "no empty looks" applied to the map.

**Checks**: [ ] zoom content probe (§18) — fails when: a budget is exceeded, a label overlaps, or a dead screen appears in > 5% of samples.

## 14. The Debatable Land — the campaign map

[liveops.md](liveops.md) §3 sends cross-realm war here; home castles are never attackable by another realm.

| Item | Rule (PROPOSAL) |
|---|---|
| Map | one per campaign group (4 realms; 3 allowed), fresh each campaign; 240 × 240 tiles, 9 sectors; each realm's **entry march** is a 60 × 60 corner; two rivers cross the middle with 8 fords |
| Ladder | tier 1: 8 watch-posts + 8 fords · tier 2: 8 chapels · tier 3: 4 abbeys · tier 4: 2 hillforts — **each tier worth 16 points**, so the week weights (1 / 1.5 / 2 / 3) do the escalating; tier k opens in contest week k |
| Field camp | pitched in own entry march on a campaign war day (00:00–23:59 UTC); holds the player's banners; supplies 30 h (20 h in the Long Winter frame); strikes at 23:59 and troops walk home, 0 taps |
| Travel | castle ↔ field camp: a fixed 10 min on "the King's road" (a function of time, not drawn) |
| Lawful | attacks only inside the group's two war windows; a lost field camp sends survivors home (combat.md field context) |
| Distance | entry edge → centre ≈ 85 tiles ≈ 8.5 min; tier 1 within 2–3 min of an entry; own realm's held landmarks are rally points |
| Fog, colours | no fog; Ally = own realm (own alliance solid, realm-mates dashed); Enemy = other realms, told apart by realm sigil, never by a fifth colour |
| Capacity | ≤ 1,000 players per window (≈ 30% of four realms' DAU over two windows); crowd mode from minute one (§16) |
| Season frames | Floods close 2 of the 8 fords in alternate weeks; Beacons: tier-1 holders see marches within 10 tiles; Sieges: tier 3+ walled (liveops §9) |

**Checks**: [ ] staging clock run (liveops §11) — fails when: a field camp outlives its war day or troops fail to walk home · [ ] realm_sim campaign mode — fails when: one tier's points exceed another's.

## 15. Anti-stagnation — the realm keeps changing hands

| # | Rule | Number |
|---|---|---|
| A1 | Hold caps per tier (§3) | top alliance ≤ 42 of 172 points (24%) |
| A2 | Treasury curve 50·P − 8·P^1.5 (§3) | best at 17 points; negative above 39 |
| A3 | **Restless**: a landmark held through 3 home war days in a row pays half output and no marks until it changes hands | 3 war days |
| A4 | **Crown rotation**: ≤ 3 terms in a row; on the 4th war day the holder alliance and its Accord partner cannot target the seat | hard limit ([benchmark.md](benchmark.md) "decay after N cycles") |
| A5 | Pacts do not apply at the crown seat or within 2 chunks of it in home windows (alliance.md §12 rule 3) | — |
| A6 | **Truce reset**: the crown seat and tiers 3–4 → neutral guardians; offices end; tiers 1–2 keep holders; territory stays (alliance.md upkeep follows activity) | every Truce week |
| A7 | **Bloc cap**: an Accord pair's combined holdings ≤ 1.5 × one alliance's caps | server-enforced |
| A8 | **Inactive castles**: shuttered after 72 h offline (plunder yield halves per further day — PROPOSAL to economy.md); **archived** (off the map, nothing lost) when < 7 days old and 72 h offline, or age ≤ III and 14 d offline, or 30 d offline at any age | the map shows players, not farms |
| A9 | Late joiners: gates open by calendar; wandering camp bands; settled ground (progression.md C2); newcomers routed to new realms (liveops §1.1) | only realms ≤ 35 days old take newcomers |

**Targets** (realm_sim, telemetry): top alliance ≤ 25% of points held at window close (season median); ≥ 6 alliances hold a tier ≥ 2 landmark on day 60; ≥ 20% of tier ≥ 2 landmarks change hands per home war day; ≥ 3 different crown holders per 8 weeks.

## 16. Server cost — the hot spot decides it

Rules. (1) Marches are functions of time, resolved by arrival jobs: 0 ticks. (2) Camps, nodes, veins, strongholds and AI hosts are **seeded**; only kills write. (3) Every map query is keyed by chunk or sector, never a radius scan over castles; static data per sector is a versioned bundle (castles, holdings, suppression records; ≤ 20 KB gzip) fetched only when its version changes. (4) **Interest management**: a client subscribes to the ≤ 4 sectors its view touches plus its personal channel (marches aimed at it, own marches, alliance rallies) and drops a sector 10 s after leaving it; realm zoom reads one realm summary (1-byte ownership raster of 6,400 chunks + holdings, ≈ 2 KB gzip) regenerated ≤ once per minute when it changes. (5) **Crowd mode**: a sector with ≥ 60 live marches, or holding a contested landmark in a war window, switches from per-march updates to a server-written batch every **5 s** (≤ 200 compact 28-byte records + flow arrows, "≈ 40 marches → the Abbey"); the client draws ≤ 60 of them (§13). The readability budget and the cost budget are the same budget.

Worked month — base case: 50,000 accounts, 20,000 DAU (chat-forge's base), 13 war days, 30% of DAU fight in one window each → 3,000 viewers per window, 30 active minutes. Unit prices are illustrative, **not quotes** (sd_cost_probe holds the real ones): €0.05 per 100k reads, €0.15 per 100k writes, €1 per GB.

| Line | Formula | Per month | € (illustrative) |
|---|---|---|---|
| War windows, **crowd mode** | 3,000 viewers × (1,800 s ÷ 5 s) × 2 windows × 13 days | 28 M reads | ≈ 14 |
| War windows, **naive** (every event to every viewer) | 10 hot sectors × 300 senders × 15 marches × 3 events × 300 viewers × 26 windows | 1.05 B reads | ≈ 527 |
| Quiet map reads | 20,000 × (3 bundles + 6 sector updates + 4 summaries + 5 personal) × 30 | 10.8 M reads | ≈ 5 |
| Map-only writes | fog ≤ 4 + holdings 0.3 + summaries (20 realms × 1,440 ÷ 20,000) ≈ 6 per DAU-day | 3.6 M writes | ≈ 5 |
| **Designed map total** | march orders and arrivals are costed in core-loop §11 and combat.md §14 | | **≈ 25** |

Read it: the naive stream costs 2.6× the whole €200 budget; the designed one ≈ 12% of it. At everyone-daily stress (50,000 DAU) ≈ €62 → set crowd batches to 10 s → ≈ €45. On a stream relay (WebSocketPeer, billed per GB) the war line is ≈ 3.7 GB per month. **Budget line**: the map ≤ €50 per month in the base case, measured by `core/sd_cost_probe.gd`; cloud-forge chooses the backend shape.

**Checks**: [ ] sd_cost_probe — fails when: any map object moves by a server tick, a spawn writes, or the map line > €50 per month · [ ] map load test — fails when: a sector batch carries > 200 records or crowd mode does not switch at 60 marches.

## 17. Genre weak spots → our fix

| Weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| Late realms freeze under one dominant alliance | caps, Treasury curve, restless, crown rotation, Truce reset (§15) | ≤ 24% of points; ≤ 3 terms |
| Outer-zone players fall behind | every gate opens by calendar; wandering camp bands; catch-up unlock floor | all gates open by day 36 |
| Gem-bought teleports win wars | no writ sales in contest weeks; 72 h cooldown for all; no moves in windows | 0 paid moves in war |
| Raiding inactive cities as a norm | shuttered at 72 h, archived by age (A8) | plunder yield ≈ 0 within a week |
| Truces freeze the map | bloc cap; pacts void at the crown (alliance.md) | ≤ 1.5 × caps |
| Relationship by colour alone | shapes, line patterns, keyline; measured colour-blind distances | ≥ 23.7 ΔE00 |
| Fog as a grind | great places charted from day 1; marches clear fog; 1-tap scouting | 80% of region by day 7 |
| Pure damage share pays the biggest | 50/50 split + floor and cap | smallest ÷ largest ≥ 0.3 |
| Map traffic grows with crowd² | crowd mode, 5 s batches, ≤ 60 drawn | €25 vs €527 per month |
| A map that looks empty | dead-screen rule; AI hosts top up; real set-pieces | ≤ 5% dead screens |

## 18. Harness, save migration, metrics

| Proof | Measures | Verdict line (PROPOSED; qa-forge fixes the wording) |
|---|---|---|
| `realm_sim` (new, headless; qa-forge) | 90 days on liveops' registration model, alliances per alliance.md: points share, holders, handovers, crown terms, camp distance, fog pace, on-map castles, dead screens | `REALM SIM OK - top 23% pts, 7 holders tier2+, 22%/war day change hands, crown <= 3 terms, camps 96%, dead 3%` |
| `march_probe` (in world-forge's scope; extend) | client vs server `pos(t)` in fixed point, terrain factors, the 90 s rule, seat-move blocks | `MARCH PROBE OK - 1000 marches, drift 0, 0 illegal moves` |
| zoom content probe (windowed; beside transition-forge's frame-time probe) | per level: squads, labels, overlaps, markers, dead screens; the greyscale pattern test | `ZOOM CONTENT OK - region 58 squads 38 labels 0 overlaps, 5/5 patterns` |
| relation palette check (qa-forge; ui-forge reuses it) | CVD ΔE00 of §12 and of the tincture set | `RELATION PALETTE OK - min 23.7 protan, tokens >= 17` |
| map load test (cloud-forge) | 3,000 simulated viewers in one window | `MAP LOAD OK - 3000 viewers, 1.1M reads/window, p95 lag 5.5 s` |
| `map_trap_probe`, `ux_touch_probe`, `a11y_audit`, `fenv_b_weather_probe` (existing) | no dead ends ("No road" paths), tap targets, colour-blind pass, weather unaffected by the parchment layer | their shipped verdict lines |
| `core/sd_cost_probe.gd` | map reads and writes per player per day | map ≤ €50 per month at 50,000 players |

**Save migration** (world-forge + gameplay-forge): realms opened after ship get this layout. An existing realm keeps its shipped map and castle positions: world-forge's placer adds landmarks on open ground (tier by distance from the centre) but **no gates** (a gate added around settled castles would trap them); fog bitset = the 5 × 5 start area + every chunk within 20 tiles of a past target; camp unlocks = the shipped record raised to the age floor; no holdings, no crown until its first home war day.
**After ship**: ≥ 95% of first sessions clear the first camp; ≥ 50% of DAU in an alliance holding a landmark by day 30; dead screens ≤ 5%; seat moves with an attack inbound = 0; map line ≤ €50 per month.

## 19. Owner decisions required

1. `A_design` 2,000 / `C_design` 6,000 / 800 × 800 tiles, paired with liveops' `N_fill` 8,500 (or 2,600 / 900 tiles for 12,000).
2. Castle plunder outside war windows at combat.md row 8 losses (§10), or war windows only.
3. The crown rotation limit of 3 terms (A4) and the Truce reset of tiers 3–4 (A6).
4. Seat-move writs never sold, or sold in Truce weeks only (monetization.md decision 5); the 72 h cooldown.
5. Archiving inactive castles (A8) and grudge-only AI raids (§6) — both change shipped behaviour.
6. The relationship palette (§12) as the single source. It conflicts with blender-forge `architecture.md` §7 (owner colour on banners, pennons and roof trims); this file puts the relationship on rings and finials and the alliance's tinctures on cloth.
7. Screen orientation: ux.md and ui-forge `hud.md` design 1080 × 1920 portrait; an older studio note says "landscape-only". Every px here is given on the 1080 px short side, so it holds either way.
8. Names (story-forge canon): Heartlands, Hill Country, Crown Vale, the Fens, the Pinewood, watch-post, ford, chapel, pass, abbey, bridge, hillfort, crown seat, Crown Regent and the five offices, ash-holds, crown columns, finds, the King's road, the spring flood.
