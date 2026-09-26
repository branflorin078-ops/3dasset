# World — the realm map: rings, gates, landmarks, camps, marches, zoom, cost

The RULES of the shared map: how big a realm is, how its geography paces progress, what can be
fought over and when, what every player sees at every zoom, and what it costs to serve.
Implementation: **world-forge** (map, simulation surfaces, rendering), **cloud-forge** (storage,
streams, arrival jobs), **transition-forge** (camera, zoom thresholds, hysteresis), **battle-forge**
(the march and battle experience), **blender-forge** (set-pieces, `references/architecture.md`),
**ui-forge** (HUD per zoom), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md), world section.

**Every number here is a PROPOSAL** unless it quotes a canonical fact or a sibling reference.
Read the shipped map first (world-forge scope, all paths to verify): `godot/world/world_map.gd`
(TerrainField, realm seed), `camera_rig.gd` (fixed 55° pitch), `march_out.gd`, the camp ladder
(`tools/blender/generators/barbarians.py`, 6 stages), AI lords (routines, grudges, raid pressure
held to the balance corridor). A shipped sacred constant keeps its value; this file's value becomes
an owner proposal. Quoted, never redefined: Resolve, banners, war windows ([core-loop.md](core-loop.md));
line speeds, loss rows, scouting and warning tiers, breach ([combat.md](combat.md)); Hall, banners'
cost and cap, pacts ([alliance.md](alliance.md)); realm age arc, campaigns, merges ([liveops.md](liveops.md));
nodes and veins yields ([economy.md](economy.md)); peace ward ([onboarding.md](onboarding.md)).

**Terms.** *tile* = the map's placement cell (a castle covers 3 × 3). *chunk* = 10 × 10 tiles
(fog, territory and static data unit). *sector* = 80 × 80 tiles (live-stream unit). `v_ref` = 10
tiles per minute (a march at speed factor 1.0). *Age* `A` = ⌈keep level / 5⌉ = spine stage S1–S6
([progression.md](progression.md)). *Ring* = outer / middle / inner zone (economy.md's word).
*Tier* 1–4 = landmark tier with liveops hold values 1 / 2 / 4 / 8. *Home war day* = Saturday of
contest weeks (Tue/Thu/Sat before a realm's first campaign) inside the realm's window pair ([liveops.md](liveops.md) §3.2–3.3).
Word collisions kept apart: *fog* here is fog of war, not the atmospheric fog of `lighting.gd`;
*region* (a named area) is not *region zoom*; the boards' "dark pine marches" are called the
**Pinewood** here so the word *march* means only an army on the move.

## 0. The four questions

- **Want**: a castle in a good place; the alliance's banner on a landmark everyone sees; the crown seat and its offices; the next ring's richer camps, nodes and veins; a charted realm.
- **Obstacle**: distance in march minutes; gates (taken early by conquest or opened by the calendar); holders who fight back in war windows; camp levels won one by one; Resolve; fog.
- **Wait**: first camp march ≈ 25 s; own region charted by realm day 7; tier-1 landmarks from day 8; passes open to all on day 22; the First Crown on day 27, then every home war day.
- **Witness**: public march lines and tokens; holder banners and territory at realm zoom; the crown's chronicle line; the Crown Regent's title and the offices on profile cards.

## 1. Realm capacity — how many players share one map

[liveops.md](liveops.md) §1.1 fills a realm with `N_fill` = 8,500 registrations over ≤ 21 days
(peak DAU₇ ≈ 1,700 by its retention model) and asks this file for the map capacity `A_design`.

| Dial | PROPOSAL | Why |
|---|---|---|
| `A_design` (peak DAU₇ the map holds) | **2,000** | 1,700 peak + 15% headroom; merges and migration stop at it (liveops §7–8) |
| `C_design` (castles on the map at once) | **6,000** | peak on-map ≈ 4,000 at day 21 once day-1 churners are archived (§15 A8); 50% headroom |
| Map | **800 × 800 tiles** = 640,000; 6,400 chunks; 100 sectors | 85 passable tiles per castle at `C_design` (≤ 20% impassable) → neighbours ≈ 9 tiles (54 s) apart |
| Other capacities | side = 800 × √(C_design / 6,000) | `N_fill` 12,000 needs `A_design` 2,600 and ≈ 900 × 900 |

| `N_fill` | Peak DAU | DAU day 90 / 180 | Alliances with ≥ 15 daily actives, day 90 | Viewers at the crown in a home window (peak) | Verdict |
|---|---|---|---|---|---|
| 3,000 | 600 | 150 / 105 | ≈ 2 | ≈ 60 | dying (DAU₇ < 300) from ≈ day 30; the ladder is empty |
| **8,500** | 1,700 | 425 / 300 | ≈ 7 | ≈ 170 | **recommended**: 6–10 contenders for 180 days |
| 12,000 | 2,400 | 600 / 420 | ≈ 10 | ≈ 240 | acceptable with a 900-tile map |
| 25,000 | 5,000 | 1,250 / 875 | ≈ 20 | ≈ 500 | blocs form; naive hot-spot traffic ×70 of `N_fill` 3,000 |

**Cost does not choose N** once §16's rules hold: marches are functions of time and a viewer
receives a capped stream, so map cost grows with players, not with players per realm. Two terms
move with N: per-realm jobs (realm summary ≤ 1,440 writes per day, calendar, AI lords) favour fewer,
larger realms but are < 2% of map cost; the hot-spot term favours smaller realms only if crowd mode
(§16) is missing — then deliveries grow with viewers² per contested landmark. **Social density
chooses N**: ≥ 4 alliances with ≥ 15 daily actives (liveops' dying line) until day 180.

| Fails when | Caught by |
|---|---|
| Peak on-map castles > `C_design`, or DAU₇ > 0.9 × `A_design` | [ ] realm dashboard alert (liveops §1 row) · realm_sim on-map line |
| Map cost per player grows with realm size | [ ] map load test at 1,700 and 2,600 DAU (§18) |

## 2. Geography is progression — rings, gates, the founding calendar

Pattern (benchmark.md): concentric zones gated by passes, richer inward. Our moves: gates are
taken **early by conquest** but open to **everyone by the calendar**, so no ring stays locked
behind one alliance; and the realm's geography is one story — two rivers rise in the Crown Vale,
cut a gorge around it, run out through the hills and split the Heartlands, and end in the Fens.

| Ring (region count) | Band (tiles from centre) | Area | Castles (design share) | Camp levels | Nodes (economy.md) | Strongholds | Entered by |
|---|---|---|---|---|---|---|---|
| Outer — **the Heartlands**, green river lowlands (8 open + 2 **Fens**) | > 250 | 69% | 60% | 1–12 | N 1–3 | L1–2 | spawn; **fords** between regions |
| Middle — **the Hill Country**, stone hills, the Pinewood on its inner slopes (4) | 105–250 | 25% | 32% | 10–22 | N 3–5; seams | L3–4 | 8 **passes** through the escarpment |
| Inner — **the Crown Vale**, inside the river gorge (1) | ≤ 105 | 6% | 8% | 20–30 | N 5–6; seams, most veins | L5–6 | 4 **bridges** over the gorge |

**The Fens** (2 outer regions at the river mouths) are **reserve land**, sealed as flooded fen until
the first merge or migration wave needs a block (liveops §8 rule 3), then drained with a chronicle
line. Capacity ≈ 1,450 castles placed by alliance in blocks. New castles never spawn there.

**Terrain factor** (combat.md §4 asks this file): open ground 1.0 · Pinewood 0.85 · a ford crossing
0.6 for its 3 tiles · pass and bridge 1.0 (they are roads) · drained fen 0.9. Mountains, the gorge
and river channels outside fords and bridges are impassable; ≤ 20% impassable per ring.

**Distances are designed in minutes** (numbers.md §1 applied to space):

| Trip | Minutes at `v_ref` | Tiles |
|---|---|---|
| Castle → own-level camp; castle → neighbour | 1–3 | 10–30 |
| Hall or gate rally point → contested landmark (core-loop §8.3's 60–180 s) | 1–3 | 10–30 |
| Castle → a node of the player's level | 2–6 | 20–60 |
| Across one outer region | ≈ 20 | ≈ 200 |
| Map edge → Crown Vale rim (no seat move) | ≈ 30 | ≈ 300 |

**Founding calendar (home map; realm days per liveops §1):**

| Realm day | Opens |
|---|---|
| 1 (Mon) | castles land in the 8 open Heartland regions; every gate closed ("the spring flood"); great places charted on the parchment (§7) |
| 8 | tier 1 contestable (watch-posts, fords) on war days |
| 15 | tier 2 (chapels, passes); **fords open to all** |
| 22 | tiers 3–4 (abbeys, bridges, hillforts); **passes open to all** |
| 27 (Sat) | **the First Crown**: alliances holding a bridge reach the Vale; contested in both windows |
| 36 | **bridges open to all** |
| first contest week | home fighting moves to Saturdays; Tue/Thu go to the Debatable Land (§14) |

Before a gate opens to all, only its holder's members path through it; everyone else sees "No
road — <the ford> is held by [TAG]" or "…flooded until day 15" (battle-forge flows.md §3). After
opening, a held gate is a **rally point**: the holder's rallies form there.

| Fails when | Caught by |
|---|---|
| An alliance keeps a ring closed to others past its calendar day | [ ] pathfinder unit test on days 15 / 22 / 36 |
| A castle's nearest own-level camp is > 3 min away | [ ] realm_sim camp-distance line (§4) |

## 3. The landmark ladder

Pattern: a ladder of contested places so every alliance size has a goal, the top visible to all.
Our moves: every rung is worth holding at its size; **no landmark grants combat stats** (counters
stay readable, [combat.md](combat.md) §5); the top pays in standing, not Treasury (below).

| Tier (value) | Landmark — set-piece (blender-forge) | Count | Ring | Grants the holder alliance (economy.md §6: +3–8% city output of ONE resource) | Cap per alliance |
|---|---|---|---|---|---|
| 1 (1) | **Watch-post** — timber tower, brazier at the top | 24 (3 per open region) | outer | +3% wood; vision 20 tiles | 4 of tier 1 |
| 1 (1) | **Ford** — stepping stones, toll hut, marker post | 12 | outer | +3% food; crossing before day 15; rally point | (shared cap) |
| 2 (2) | **Chapel** — stone chapel with a bell-cote | 12 (1 per open region + 4 hill) | outer, middle | +4% food | 3 of tier 2 |
| 2 (2) | **Pass** — gatehouse in a rock cleft | 8 | outer/middle edge | +4% stone; crossing before day 22; rally point | (shared) |
| 3 (4) | **Abbey** — cloister, scriptorium, church tower | 8 (2 per hill region) | middle | +6% gold | 2 of tier 3 |
| 3 (4) | **Bridge** — fortified bridge, gate tower mid-span | 4 | gorge | +6% iron; crossing before day 36; rally point | (shared) |
| 4 (8) | **Hillfort** — old royal earthwork and stone hall on a crag | 4 (1 per hill region) | middle | +8% iron; vision 30 tiles; rally point | 1 |
| crown (16) | **Crown seat** — the old royal hall inside a ring wall | 1 | inner | the **Crown Regent** and the five offices | 1 |

Total 172 points; the caps allow one alliance at most 42 (24%). Each set-piece is a distinct
silhouette at region zoom and a distinct 32 px icon at realm zoom, carries the holder's banner (tint
mask, architecture.md §7), sits in the ground with real construction (architecture.md §5–6: 3–8k
tris, LOD2 300–800).

1. **Contest**: only inside home war windows, from the tier's opening day. Beat the garrison (neutral guardians, then the holder's reinforcements; strength and losses: combat.md row 6), and the holder **at window close** keeps it. Captures and holds feed liveops §3.4 standings.
2. **Guardians** (neutral) are sized to a rally of 3 / 5 / 8 / 12 marches of the realm's median castle for tiers 1–4, and 15 marches plus walls for the crown (gameplay-forge tunes; siege-forge walls).
3. **The crown term** is one week. Each home war day, the alliance that held the seat **longest summed over both windows** wins the term — time zone does not decide it (liveops §3.3). The holder's Liege becomes **Crown Regent** and appoints five offices within 12 h: Master of Works (+10% build speed), Chancellor (+10% research), Master of Musters (+10% training), Almoner (+10% healing), Master of Roads (+10% march speed, home map). Rules: ≥ 2 of 5 go to players outside the Regent's alliance; nobody holds an office two terms in a row; no debuff offices exist; nothing combat.
4. **Treasury** ([alliance.md](alliance.md) §4 asks for the rate): held points `P` pay **50·P marks per day** and cost **8·P^1.5 per day** to hold (both functions of time, settled on any Treasury read).

| Points held `P` | 4 | 8 | 17 (best) | 25 | 32 | 39 | 42 (cap) |
|---|---|---|---|---|---|---|---|
| Net marks per day | +136 | +219 | **+289** | +250 | +152 | +2 | **−78** |

Read it: a median alliance's landmark income is ≈ 5% of its Treasury income (alliance.md implies
≈ 6,150 per day); sprawl past 39 points costs marks. The crown is held for glory, not income.

| Fails when | Caught by |
|---|---|
| A landmark grants attack, defence, health or march size | [ ] data lint: landmark effects ⊂ {output, vision, crossing, rally point, office} |
| One alliance holds > 42 points or two of a tier-4 | [ ] capture unit test: over-cap capture refused with a message |
| The crown term goes to the alliance of the later window by rule | [ ] crown unit test: time-held tie cases |

## 4. Barbarian camps — the PvE ladder

1. **Levels 1–30** in the shipped **6 visual stages** of 5 levels each (verify barbarians.py maps this way); each stage changes silhouette (architecture.md §4). Each camp shows its main line — the counter hint (onboarding.md, combat.md).
2. **Unlock**: a win against level L opens L+1 (onboarding.md). Catch-up floor: levels ≤ 5·(A − 1) open automatically (age II → 5, VI → 25); 26–30 are always earned.
3. **Spawn is seeded**: `hash(realm seed, chunk, 30-min epoch)` places 2 camps per chunk (3 in the inner ring) — 0 spawn writes, like nodes (economy.md §5). 70% follow the ring's band; 30% are **wandering bands** at the sector's median unlocked level ±1 (sector summary, daily), so an outer-ring player is never capped by geography.
4. **Density target**: ≥ 5 camps of levels [U−2, U] within 30 tiles (3 min) for ≥ 95% of castles (U = highest unlocked). Headroom at `C_design`: ≈ 56 slots × 48 epochs = 2,688 kills per day in that radius vs ≈ 790 demanded.
5. **First camp**: each new castle gets a personal level-1 camp 4–5 tiles away (≈ 25 s march, onboarding.md step 6), seeded by castle id, visible to its owner for 24 h.
6. **Resolve** 10 per camp; hunt orders take up to 5 camps (core-loop §3). A camp killed by someone else first: the march re-targets the next hunt camp or returns, Resolve refunded. Camps never attack.
7. Rewards: [economy.md](economy.md) (camps ≥ level 5 drop iron) and [lords.md](lords.md) (XP). The attack validates the camp server-side by recomputing the hash — a client cannot invent one.

| Fails when | Caught by |
|---|---|
| < 95% of castles have 5 own-level camps within 3 min | [ ] realm_sim camp line, per ring |
| An outer-ring player at age VI finds no camp above level 12 | [ ] realm_sim wandering-band line |

## 5. Strongholds (ash-holds) — rally-only alliance PvE

| Level | Ring | Per realm | Respawn after a kill | Min marches | Leader Resolve |
|---|---|---|---|---|---|
| 1–2 | outer | 16 (2 per open region) | 6 h | 3 | 20 |
| 3–4 | middle | 12 | 8 h | 5 | 20 |
| 5–6 | inner | 6 | 12 h | 8 | 30 |

Seeded positions per region and epoch; a kill writes one record that suppresses it until respawn.
Level L+1 opens for an alliance after it kills L. Never inside any territory. Join window ≤ 60 min
(combat.md §9); Spoils and gifts: alliance.md §6.

**Reward split** = [alliance.md](alliance.md) §8 (50% equal, 50% by damage), then liveops R8
(floor 40% / cap 3× the median share; clamp, rescale the rest). Worked, 8 marches, pool 100:
damage 35/20/15/10/8/6/4/2 → **23.8 / 16.3 / 13.8 / 11.3 / 10.3 / 9.3 / 8.3 / 7.3** (pure
damage share gives 35 … 2; smallest ÷ largest 0.31 vs 0.06). One dominant march (damage 70/10/6/5/4/3/1/1)
→ 41.3 capped at 25.5, rescaled: **25.5 / 14.3 / 11.7 / 11.1 / 10.5 / 9.8 / 8.6 / 8.6**.
PROPOSAL to alliance.md: the equal half needs a march ≥ 20% of the rally's median march (stops
one-troop leeching). Reward shares ≤ 5 per player per day (alliance.md's paid rallies).

**Crown columns** (onboarding.md FTM "Lead a rally", progression.md "The Muster"): when a
stronghold rally is below its minimum at 50% of the join window, up to 2 NPC columns sized at the
leader's median march fill it — for a leader's first 3 stronghold rallies, or an alliance with < 10
members active in the last hour. Their damage counts for the kill; players share 100% of the pool.
**The Warlord's Hold** (liveops §4.2): Wed 00:00 on the open site nearest the Hall, 2–4 chunks
outside the alliance's border (20 tiles from the Liege's castle without a Hall); only that alliance
may attack it; gone Fri 23:59.

| Fails when | Caught by |
|---|---|
| The smallest qualifying joiner earns < 40% of the median share | [ ] reward-split unit test, 5 distributions |
| A crown column takes a reward share | [ ] same test, NPC case |

## 6. AI lords — what they are for

12 AI lords (1 per open Heartland region + 1 per hill region), each with a castle (rally-only;
walls, gate, towers — siege-forge; level = realm median age + 1, ≤ 6), 3 outposts (solo) and
seeded **hosts** that patrol between them ([lords.md](lords.md) counts host kills). Resolve 20 per
outpost or host; castle rally leader 20 ([core-loop.md](core-loop.md) §3).

| Role | Rule | Number |
|---|---|---|
| Teacher | only onboarding.md's two scripted raids (step 1, chapter 6); nothing else hits a warded castle | 2 per player |
| Living map | hosts are seeded functions of time computed on clients (0 writes); a kill writes one suppression record | per sector: hosts = max(0, 6 − player marches per hour), ≤ 6 |
| Grudge | outpost / host / castle attacks add 1 / 1 / 3 grudge; at ≥ 5 in 7 days one raid lands in 2–24 h, warned ≥ 10 min ahead, at 50–70% of the castle's defence; home never kills (combat.md rule 1) | ≤ 1 per player per day; 0 unprovoked |
| Siege school | AI castles are the safe place to learn engines vs walls | loss context: camp (combat.md) |
| Filler | in a Thinning realm (liveops §8) host density ×2 | dead-screen rate ≤ 5% |

Limits: AI lords never hold tier ≥ 2 landmarks, never rank, never get offices, never move, never
target a castle whose owner has not attacked them. The shipped raid-pressure corridor stays the
ceiling; this file proposes grudge-only pressure inside it.

## 7. Fog of war and scouting

1. **Unit** = chunk: 6,400 per realm → an 800-byte bitset in the save, written ≤ once per 5 min while it changes. Clearing is permanent.
2. **The parchment**: fog is painted cartographer's parchment (PARCHMENT family) with sketched contours — never grey smoke. **Great places are printed on it from day 1**: region names, gates, landmarks, the crown seat (the next goal is visible). Fog hides terrain detail, castles, camps, nodes, veins, strongholds, AI lords, finds, and marches — except marches aimed at you or your alliance.
3. **Starts cleared**: 5 × 5 chunks around the castle. Every own march clears the chunks its path crosses (rides the next save).
4. **Scouts** (a plate under core-loop §2 rules; no banner, battle-forge flows.md §2): 2 at start, a 3rd with the huntlodge (age III, progression.md). Speed 3 × `v_ref`. Target: a fogged chunk within 3 chunks of cleared ground; clears 3 × 3 chunks, 5 × 5 with the Wayfaring research row. **Scout the frontier** = 1 tap sends all idle scouts toward the nearest fog in the direction of the region's gates and landmarks.
5. **Finds**: ≈ 40 per outer region (cairns, hermit huts, lost wagons, roadside shrines): 1-tap claim once cleared; own-production hours ([economy.md](economy.md)), lord XP and a chronicle line (story-forge).
6. **Pace**: an outer region ≈ 440 chunks. 2 scouts × 4 check-ins × 9 chunks × 60% new + march paths ≈ 58 chunks per day → **≥ 80% charted by realm day 7**.
7. **Alliance share**: joining reveals (as icons) every landmark, stronghold, AI castle and member castle any member has charted.
8. **Server truth**: every order validates that its target chunk is charted in the server's copy of the bitset; a modified client that draws through fog cannot act on it.
9. Scout reports of castles and marches: combat.md §11 levels L1–L5 and report-forge.

| Fails when | Caught by |
|---|---|
| < 80% of day-7 actives have charted 80% of their region | [ ] telemetry per cohort · realm_sim fog line |
| An order targets an uncharted chunk | [ ] server rule test |

## 8. Alliance territory — map rules

[alliance.md](alliance.md) §7 owns who places, cost, cap (`min(200, 3 × 7-day actives)`) and upkeep.

1. The **Hall** claims 3 × 3 chunks; each **banner** claims 1 chunk sharing an EDGE with own territory. Median 60 banners ≈ 69 chunks; the cap ≈ 209 chunks = 3.3% of the map.
2. Placement: Hall ≥ 3 chunks and banners ≥ 1 chunk from any tier ≥ 2 landmark; ≥ 1 empty chunk between two alliances' land.
3. **Cut off**: a banner with no edge path to the Hall gives nothing and fades after 24 h unless reconnected — supply lines matter.
4. Banners and the Hall are attacked only in home war windows (combat.md row 6); a burned banner's chunk turns neutral at once; the Hall never fades (alliance.md), a sacked Hall pauses benefits for 24 h.
5. Territory never evicts a castle and never blocks a path. Strongholds and gem veins never spawn inside any territory; camps and nodes do (nodes inside: +20% gathering for members, economy.md §6).
6. **Border warning**: members see "Hostile march crossing <border> in 0:30" 30 s before a hostile path enters (+30 s per Beacons level, alliance.md).
7. **Look**: border smoothed (marching squares, 1.5-tile corner radius) so the chunk grid never shows; banners are real set-pieces (pole, cloth in the alliance's tinctures, a small palisade ring).

## 9. Seat moves (relocation)

| Move | Where to | Source | Limit |
|---|---|---|---|
| Newcomer's passage | another realm | free, once, while the ward holds ([onboarding.md](onboarding.md) §8) | — |
| **Charted move** | a chosen open site in any ring whose gate is open to you, outside other alliances' land | seat-move writ: season track (2 per campaign), events; hold ≤ 2 | cooldown **72 h** (Summons charter −12 h per level, alliance.md) |
| **Hall summons** | an open site inside own territory (ignores gates) | Quartermaster, 1,000 Merit, 1 per week (alliance.md) | same cooldown |
| Breach move | own territory or own region | free, once, in the 8 h breach truce ([combat.md](combat.md) §10) | no cooldown |
| Arrival move | own region | free, once within 7 days of migration or merge ([liveops.md](liveops.md) §7–8) | — |
| Return | an open site in the old region | automatic when an archived player comes back (§15 A8) | return ward (onboarding.md) |

There is **no random move**: combat.md rejected random relocation; a scatter throws the player away from the alliance.

1. **Never away from an attack**: blocked from the launch of any hostile march or rally march at your castle until 30 min after the last arrival ([monetization.md](monetization.md) §3 row 7), while any own march is out, and in every war window.
2. After a move, the castle cannot launch a castle attack for 10 min, and castles within 30 tiles see "A lord has settled nearby".
3. **No gem advantage**: writs are never sold in contest weeks; if the owner allows sales at all, only in Truce weeks (monetization.md owner decision 5). The 72 h cooldown binds payer and free player alike.
4. Landing: an open 3 × 3 site, not inside another alliance's territory, not within 2 chunks of a tier ≥ 2 landmark.
5. The peace ward survives seat moves (onboarding.md §4).

## 10. Lawful targets by time (home map)

| Target | Outside war windows | Home war windows |
|---|---|---|
| Camps, strongholds, AI lords, empty nodes and veins | yes | yes |
| Another player's gathering march (field, combat.md row 5); warded players' marches on camps and nodes ≤ level 2 are refused (onboarding.md §4) | yes | yes |
| Another player's castle — plunder only, walls untouched | yes, at combat.md **row 8** losses (60% of the attacker's casualties die) | row 7; walls take damage, breach possible |
| Banners, Hall, landmarks, the crown seat | no | yes, from their opening day |
| Castles of realm-mates on campaign days (Tue/Thu of contest weeks) | no — the realm musters as one | no |

## 11. Marches on the map

1. **Record**: [combat.md](combat.md) §8, plus the time at each waypoint (≤ 8 × u32) because terrain factors make speed piecewise; `pos(t)` interpolates between the two waypoints around `t`. No server tick moves a march; the arrival job of combat.md §8 is the only trigger (alliance.md's pledged departures are future-dated records).
2. **Speed** = slowest line (combat.md §4; cavalry 1.5) × (1 + pool ≤ 0.5; Roadwardens inside own territory counts in the pool) × terrain (§2). `v_ref` = 10 tiles per minute.
3. **Paths**: one deterministic, versioned pathfinder on client and server — A* on the chunk graph with gates as mandatory nodes, then tile smoothing, ≤ 8 waypoints. Impassable ground, castles and closed gates block; armies and territory never do. Clients rebuild paths from (from, to, gate-state version), so the stream carries no path bytes.
4. **Castle attacks arrive ≥ 90 s after the order**: a march that would arrive sooner waits at its gate, visibly mustering — combat.md §11's warnings always get 90 s to matter.
5. **Interception** (combat.md §8 rule 3) needs vision of the target at order time: 20 tiles around own castles, 5 around own marches, own territory, held watch-posts (20) and hillforts (30). Eyes decide ambushes.
6. **Public** (anyone whose view shows a charted chunk): line, direction, relationship style, ETA, and battle-forge's token (3 figures of the largest line, the lord banner, the line medallion). **Not public**: counts, tiers, second lord, engines — only scouting (combat.md L1–L5) and warnings (E1–E6) reveal them. The live stream carries public fields only; the rest is fetched on tap with a rights check.

## 12. Relationship colours — the reserved channel

This table is the single source of the four values (alliance.md §7 names this file; ux.md,
game-art-director readability.md and chat-forge ui.md should cite it, never restate it).

| Class | Who | Colour | Hex | Marker (chat-forge set) | March line (1080 px short side) |
|---|---|---|---|---|---|
| Self | you | Hearth white | `#FAF6EA` | circle | 6 px, long dash 24/8 |
| Ally | own alliance; Accord partner (alliance.md §12) | Ally blue | `#2042D8` | heater shield (Accord: shield with a bar) | 6 px long dash (Accord: dash-dot) |
| Enemy | anything aimed at you or at your alliance's castles, banners, Hall or held landmarks; for 24 h, every march and castle of an alliance whose member attacked yours; other realms on the Debatable Land | Foe vermilion | `#FF4F19` | crossed blades | 6 px chevron dashes; 8 px with a pulse ≤ 1 Hz when aimed at you (battle-forge flows.md §5) |
| Neutral | everyone else: other players, barbarians, AI lords, guardians | Fallow grey | `#786868` | square | 4 px dots, 60% opacity |

**Measured** (Machado 2009 full-severity simulation, CIEDE2000): the four are ≥ 30.2 apart for
normal vision, 23.7 protan, 30.3 deutan, 26.5 tritan; each is ≥ 17 from every palette token, line
accent and rarity colour, except Hearth white vs PARCHMENT (10) — hence the keyline.

1. **Stroke recipe**: colour core + 2 px INK keyline + 1 px PARCHMENT halo at 60%. INK carries it on light ground, the halo on dark Pinewood — the mark never sinks into terrain.
2. **Red is earned by a threat**, not by strangers: a calm map is mostly Fallow, so vermilion always means "this concerns you".
3. **Never colour alone**: every class has its marker shape and line pattern; the greyscale test (§18) must tell all five patterns apart.
4. **Reserved**: never in UI chrome, rarity, events, offers or decoration; alliance tinctures sit ≥ 15 ΔE00 from all four. On buildings, the ground ring and pole finial show the relationship; the banner cloth shows the alliance's tinctures (alliance.md §7).
5. The stream carries alliance ids; the client computes the class (viewer alliance, pacts, threat list) — one stream serves every viewer.

## 13. Zoom levels — the content contract

Level names and camera are **transition-forge**'s (thresholds, hysteresis, streaming); HUD per
level is ui-forge's (`references/architecture.md` §1). This table is what each level must SHOW.
Sizes at the 1080 px short side.

| Object | Castle close | Castle overview | Region | Realm |
|---|---|---|---|---|
| Own castle | full 3D (castle-forge) | full 3D, walls, gate, Self ring | 3D cluster 48–96 px (architecture.md §2) + ring + name | crest 28 px + ring, always |
| Other castles | — | within 10 tiles, with rings | 3D cluster + relationship ring | alliance members as 6 px dots; others as density shading |
| Token squads | the march-out at the gate (battle-forge) | own squads 60–90 px | 40–56 px (battle-forge flows.md §5); ≤ 60 animated, the rest 32 px banner chips | own, own rallies, hostile-to-own: 16 px pips |
| March lines | — | own only | every public line in its class style | own, own rallies, hostile-to-own: 3 px |
| Camps, strongholds, AI | — | within 10 tiles | set-pieces + level plate 28 px + main-line hint | own-alliance strongholds and AI castles: 20 px icons |
| Nodes, veins | — | within 10 tiles | set-pieces + level + occupant ring | charted veins: 14 px glints |
| Landmarks, gates | — | — | set-piece 80–140 px + holder banner + name | 32 px icon (crown 44 px) + holder ring + holder sigil, through fog |
| Territory | — | own border as a ground decal | border 4 px + 10% fill | 30% fill + 2 px border + sigil 40 px (≥ 20 chunks) |
| Labels | — | — | ≤ 40, priority: self > aimed at me > own alliance > landmarks > bookmarks > camps at my level; others on tap | 15 region names; tier ≥ 3 and own holdings |
| States | HUD warning with exact ETA | incoming: ring breathes 0.5 Hz | burning smoke + "Burning" (combat.md §10), ward dome | burning / warded icons for own and alliance castles |

Budgets: region ≤ 150 markers, 0 label overlaps (battle-forge merges ≥ 4 tokens within 60 px into a
chip); realm ≤ 400 icons as MultiMeshInstance3D, one draw call per icon family. **No dead screens**:
a region view shows ≥ 3 moving things and ≥ 1 place of interest in ≥ 95% of random samples (AI hosts
top up, §6) — the owner's "no empty looks" on the map.

## 14. The Debatable Land — the campaign map

[liveops.md](liveops.md) §3 sends cross-realm war here: home castles are never attackable by another realm.

| Item | Rule (PROPOSAL) |
|---|---|
| Map | one per campaign group (4 realms; 3 allowed), fresh each campaign; 240 × 240 tiles, 9 sectors; each realm's **entry march** is a 60 × 60 corner; two rivers cross the middle with 8 fords |
| Ladder | tier 1: 8 watch-posts + 8 fords · tier 2: 8 chapels · tier 3: 4 abbeys · tier 4: 2 hillforts — **each tier worth 16 points**, so the week weights (1 / 1.5 / 2 / 3) do the escalating; tier k opens in contest week k |
| Field camp | pitched in own entry march on a campaign war day (00:00–23:59 UTC), holds the player's banners; supplies 30 h (20 h in the Long Winter frame); strikes at 23:59 and troops walk home, 0 taps |
| Travel | castle ↔ field camp: a fixed 10 min "King's road" (a function of time, not drawn) |
| Lawful | attacks only inside the group's two war windows; a lost field camp sends survivors home (combat.md field context) |
| Distance | entry edge → centre ≈ 85 tiles ≈ 8.5 min; tier 1 within 2–3 min of an entry; own realm's held landmarks are rally points |
| Fog | none: the field is charted |
| Relationship | Ally = own realm (own alliance solid, realm-mates dashed); Enemy = other realms, told apart by realm sigil, never by a fifth colour |
| Capacity | ≤ 1,000 players per window (≈ 30% of four realms' DAU split over two windows); crowd mode from minute one (§16) |
| Season frames | Floods close 2 of the 8 fords in alternate weeks; Beacons: tier-1 holders see marches within 10 tiles; Sieges: tier 3+ walled (liveops §9) |

## 15. Anti-stagnation — the realm must keep changing hands

| # | Rule | Number |
|---|---|---|
| A1 | Hold caps per tier (§3) | top alliance ≤ 42 of 172 points (24%) |
| A2 | Treasury curve 50·P − 8·P^1.5 (§3) | best at 17 points; negative above 39 |
| A3 | **Restless**: a landmark held through 3 home war days in a row pays half output and no marks until it changes hands | 3 war days |
| A4 | **Crown rotation**: ≤ 3 terms in a row; on the 4th war day the holder alliance and its Accord partner cannot target the seat | hard limit (benchmark.md "decay after N cycles") |
| A5 | Pacts do not apply at the crown seat and within 2 chunks of it in home windows (alliance.md §12 rule 3) | — |
| A6 | **Truce reset**: crown seat and tiers 3–4 → neutral guardians; offices end; tiers 1–2 keep holders; territory stays (alliance.md upkeep follows activity) | every Truce week |
| A7 | **Bloc cap**: an Accord pair's combined holdings ≤ 1.5 × one alliance's caps | server-enforced |
| A8 | **Inactive castles**: shuttered after 72 h offline (shutters closed; plunder yield halves per further day, PROPOSAL to economy.md); **archived** (off the map, nothing lost) when < 7 days old and 72 h offline, or age ≤ III and 14 d offline, or 30 d offline at any age | the map shows players, not farms |
| A9 | Late joiners: gates open by calendar; wandering camp bands; settled ground (progression.md C2); newcomers routed to new realms (liveops §1.1) | ≤ 35-day-old realms only |

**Targets** (realm_sim and telemetry): top alliance ≤ 25% of points held at window close (season
median); ≥ 6 alliances hold a tier ≥ 2 landmark on day 60; ≥ 20% of tier ≥ 2 landmarks change hands
per home war day; ≥ 3 different crown holders per 8 weeks.

## 16. Server cost — the hot spot decides it

Rules: (1) marches are functions of time, resolved by arrival jobs — 0 ticks; (2) camps, nodes,
veins, strongholds and AI hosts are **seeded** — only kills write; (3) static map data per sector
is a versioned bundle (castles, holdings, suppression records; ≤ 20 KB gzip) fetched only when its
version changes; (4) **interest management**: a client subscribes to the ≤ 4 sectors its view
touches (+ its personal channel: marches aimed at it, own marches, alliance rallies) and drops a
sector 10 s after leaving it; realm zoom reads one realm summary (ownership raster of 6,400 chunks
at 1 byte + holdings, ≈ 2 KB gzip) regenerated ≤ once per minute when it changes; (5) **crowd
mode** — a sector with ≥ 60 live marches, or holding a contested landmark in a war window, switches
from per-march updates to a server-written batch every **5 s** (≤ 200 compact 28-byte records + flow
arrows, "≈ 40 marches → the Abbey"); the client draws ≤ 60 of them (§13). The readability budget
and the cost budget are the same budget.

Worked month (base: 50,000 accounts, 20,000 DAU as chat-forge's base case, 13 war days, 30% of DAU
fight, one window each → 3,000 viewers per window, 30 active minutes). Illustrative unit prices,
**not quotes** (sd_cost_probe holds the real ones): €0.05 per 100k reads, €0.15 per 100k writes, €1 per GB.

| Line | Formula | Per month | € (illustrative) |
|---|---|---|---|
| War windows, **crowd mode** | 3,000 viewers × (1,800 s ÷ 5 s) × 2 windows × 13 days | 28 M reads | ≈ 14 |
| War windows, **naive** (every event to every viewer) | 10 hot sectors × 300 senders × 15 marches × 3 events × 300 viewers × 26 windows | 1.05 B reads | ≈ 527 |
| Quiet map reads | 20,000 × (3 bundles + 6 sector updates + 4 summaries + 5 personal) × 30 | 10.8 M reads | ≈ 5 |
| Map-only writes | fog ≤ 4 + holdings 0.3 + summaries (20 realms × 1,440 ÷ 20,000 DAU) ≈ 6 per DAU-day | 3.6 M writes | ≈ 5 |
| **Designed map total** | march orders and arrivals are in core-loop §11 and combat.md §15 | | **≈ 25** |

Read it: the naive stream costs 2.6× the whole €200 budget; the designed one ≈ 12%. Everyone-daily
stress (50,000 DAU) ≈ €62 → set crowd batches to 10 s → ≈ €45. On a stream relay (WebSocketPeer,
billed per GB) the war line is ≈ 3.7 GB per month. **Budget line**: the map ≤ €50 per month at the
base case, measured by `core/sd_cost_probe.gd` (cloud-forge chooses the backend shape).

| Fails when | Caught by |
|---|---|
| Any map object moves by a server tick, or a spawn writes | [ ] sd_cost_probe: 0 ticks, spawn writes 0 |
| A viewer receives > 200 records per sector batch, or crowd mode fails to switch at 60 | [ ] map load test (§18) |
| Map cost > €50 per month at the base case | [ ] sd_cost_probe map line |

## 17. Genre weak spots → our fix

| Weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| Late realms freeze under one dominant alliance | caps, Treasury curve, restless, crown rotation, Truce reset (§15) | ≤ 24% of points; ≤ 3 terms |
| Outer-zone players fall behind | calendar opens every gate; wandering camp bands; catch-up unlock floor | all gates open by day 36 |
| Gem-bought teleports win wars | no sales in contest weeks; 72 h cooldown for all; no moves in windows | 0 paid moves in war |
| Inactive-city raiding as a norm | shuttered at 72 h, archived by age (A8) | plunder yield → ≈ 0 in a week |
| Truces make the map static | bloc cap, pacts void at the crown (alliance.md) | ≤ 1.5 × caps |
| Colour-only relationship coding | shapes + line patterns + keyline; measured CVD distances | ≥ 23.7 ΔE00 |
| Fog grind | great places charted from day 1; marches clear fog; 1-tap scouting | 80% of region by day 7 |
| Pure damage share pays the biggest | 50/50 split + floor/cap | smallest ÷ largest ≥ 0.3 |
| Map traffic grows with crowd² | crowd mode, 5 s batches, ≤ 60 drawn | €25 vs €527 per month |
| An empty-looking map | dead-screen rule; AI hosts top up; real set-pieces | ≤ 5% dead screens |

## 18. Harness, save migration, metrics

| Proof | Measures | Verdict line (PROPOSED; qa-forge fixes the wording) |
|---|---|---|
| `realm_sim` (new, headless; qa-forge) | 90 days on liveops' registration model; alliances per alliance.md: points share, holders, handovers, crown terms, camp distance, fog pace, on-map castles, dead screens | `REALM SIM OK - top 23% pts, 7 holders tier2+, 22%/war day change hands, crown <= 3 terms, camps 96%, dead 3%` |
| `march_probe` (exists per world-forge scope; extend) | client vs server `pos(t)` in fixed point, terrain factors, 90 s rule, seat-move blocks | `MARCH PROBE OK - 1000 marches, drift 0, 0 illegal moves` |
| zoom content probe (windowed; with transition-forge's frame-time probe) | per level: squads, labels, overlaps, markers; greyscale pattern test | `ZOOM CONTENT OK - region 58 squads 38 labels 0 overlaps, 5/5 patterns` |
| relation palette check (qa-forge; ui-forge reuses) | CVD ΔE00 of §12 and the tincture set | `RELATION PALETTE OK - min 23.7 protan, tokens >= 17` |
| map load test (cloud-forge) | 3,000 viewers in a simulated window | `MAP LOAD OK - 3000 viewers, 1.1M reads/window, p95 lag 5.5 s` |
| `map_trap_probe`, `ux_touch_probe`, `a11y_audit`, `fenv_b_weather_probe` (existing) | no dead ends ("No road" paths), tap targets, colour-blind pass, weather unaffected by the parchment layer | their shipped lines |
| `core/sd_cost_probe.gd` | map reads and writes per player per day | map ≤ €50 per month at 50,000 players |

**Save migration** (world-forge + gameplay-forge): existing castles keep their tiles (the realm
map is laid around them; a castle on new impassable ground moves to the nearest open site with a
notice); fog bitset = the 5 × 5 start area + every chunk within 20 tiles of past targets; camp
unlocks = the shipped record, raised to the age floor; no holdings, no crown.
**After ship**: ≥ 95% of first sessions clear the first camp; ≥ 50% of DAU in an alliance holding
a landmark by day 30; dead screens ≤ 5%; seat moves with an attack inbound = 0.

## 19. Owner decisions required

1. `A_design` 2,000 / `C_design` 6,000 / 800 × 800 tiles, paired with liveops' `N_fill` 8,500 (or 2,600 / 900 tiles for 12,000).
2. Castle plunder outside war windows allowed at combat.md row 8 losses (§10), or war windows only.
3. Crown rotation hard limit of 3 terms (A4) and the Truce reset of tiers 3–4 (A6).
4. Seat-move writs never sold, or sold in Truce weeks only (monetization.md decision 5); the 72 h cooldown.
5. Archiving inactive castles (A8) and grudge-only AI raids (§6) — both change shipped behaviour.
6. The relationship palette (§12) as the single source; it conflicts with architecture.md §7 (owner colour on banners) — this file puts relationship on rings and tinctures on cloth.
7. Screen orientation: ux.md/hud.md design 1080 × 1920 portrait; an older studio note says "landscape-only" — every px here is on the 1080 px short side either way.
8. Names (story-forge canon): Heartlands, Hill Country, Crown Vale, the Fens, the Pinewood, watch-post, ford, chapel, pass, abbey, bridge, hillfort, crown seat, Crown Regent and the five offices, ash-holds, crown columns, finds, the King's road, the spring flood.
