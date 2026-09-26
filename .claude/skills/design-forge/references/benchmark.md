# Benchmark — the genre teardown, system by system

The genre reference the owner named is **Rise of Kingdoms** (Lilith Games; launched 24 May 2018 as
"Rise of Civilizations", renamed 5 Mar 2019; > $2B revenue by Jun 2022 and $3.5B lifetime per
Sensor Tower; at the $2B point US 25.6%, China 14.4%, Korea 12.6%; 15 civilizations [snippet]).
We study it because its systems answer the four questions of [SKILL.md](../SKILL.md) precisely,
not because its content is ours. Read your system's section at design-loop step 3. Every table has
the four columns of SYSTEM.md §3 ([spec-template.md](spec-template.md)), so a row moves into a spec
whole, tags included. The register of weak spots we fix is §13; sources are §14.

## 0. Method, tags and the content rule

**Method.** One research pass, dated **2026-09-26**. The egress proxy blocked WebFetch on every
site tried, so every fact below comes from search-result snippets of the pages in §14. No page was
read in full and no game client was played. The developer rebalances often and several guides are
years old: each number is a calibration point from a date, never a current fact about the game.

**Tags.** A tag covers every clause since the previous tag in the same cell.

| Tag | Meaning | A spec may use it as |
|---|---|---|
| [snippet] | stated in a snippet of a §14 source; no conflict seen | a calibration point, quoted with tag and date |
| [unverified] | plausible but not confirmed, or sources conflict | direction only, never a target |
| [one guide] / [older guide] | one (older) source only | direction only |
| [community estimate] | measured by players, not published by the developer | an order of magnitude |
| [observational] | general knowledge of the game, not re-checked this session | a description of shape, never a number |
| [derived] | our arithmetic on the tagged inputs; as weak as its weakest input | a worked illustration (command or formula given) |

**Pattern, never content** ([SKILL.md](../SKILL.md) rule 1):
1. This is the ONLY file in the studio that names the benchmark's content: events, items, buildings, titles, currencies, civilizations, the company and its reviewers. Every other file states the pattern in our words: "the genre's top spine upgrade runs about four months base [snippet]" is right; naming that building is not. The game's title appears elsewhere only where the owner used it (trigger phrases in SKILL.md descriptions).
2. A pattern leaves this file only together with its "Our move": the fix for its weak spot plus at least one deliberate difference.
3. Genre numbers calibrate; they never become our targets. Our numbers come from player time ([numbers.md](numbers.md) §1), `tools/curve.py`, `tools/econ_sim.py` and our harnesses.
4. A genre fact reused in another file keeps its tag.

Quarantine check, run from `.claude/skills` — it must print nothing:
```
grep -rniE "lilith|rise of civilizations|lost temple|ark of osiris|sunset canyon|mightiest governor|lucerne|starlight|book of covenant|wheel of fortune|olympia|season of conquest|lost kingdom|\bkvk\b|city hall|lyceum|courier station|holy site|governor|crystal tech|chengdu|uderzo" --include=*.md . | grep -v "design-forge/references/benchmark.md"
```

| Fails when | Caught by |
|---|---|
| A benchmark name appears outside this file | [ ] quarantine check prints 0 lines |
| A spec's §5 number is a genre number copied as a target | [ ] reviewer: every §5 number traces to player time, curve.py, econ_sim.py or a harness |
| A genre fact appears in another file without its tag | [ ] reviewer: every genre number there carries a tag |
| A spec §3 row has an "Our move" without a number or an owning file | [ ] row returned in the reviewer pass ([spec-template.md](spec-template.md)) |

## 1. Core loop and session structure

Decides what a player does in 30 s, 5 min, a day and a week, and how much keeps working while they are away.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Build queue 1; a 2nd builder for 2 days by item (one given at start) or permanent at VIP 6 [snippet]; research 1 queue, training 1 per military building, healing 1 queue [observational]; march queues 1 at start, +1 at City Hall 5, 11, 17, 22 → max 5 [snippet]. | A few parallel plates (≤ 5 timers, ≤ 5 marches) that all restart in one short visit; plate count grows with the spine building. | The 2nd builder behind a paid status tier reads as a paywall on a core queue [snippet]. | Plate count is never sold: 2 crews from minute one, a 3rd by play; marches 2 → 5 by spine tier — [core-loop.md](core-loop.md) §2; [monetization.md](monetization.md). |
| Action Points: cap 1,000, ~1 AP per 45 s → full in ~12.5 h, regen stops at the cap [community estimate]; barbarian attack 50 AP, −2 AP per chained attack, capped [snippet]. One visit per 24 h keeps 1,000 of 1,920 daily regen: −48% [derived]. | Energy sized to fill in about half a day → two sessions a day; it also rate-limits bots and PvE server load. | Regen wasted at the cap feels punitive [snippet]; it punishes sleep and busy days [derived]. | An energy bar of 100 + a reserve of 50 at 10 per hour — "nothing is lost for 15 hours"; ≤ 24 camp attacks per day from regen — [core-loop.md](core-loop.md) §3. |
| Each help removes max(1% of remaining, 1 min); alliance tech raises the floor to 3 min; 5 helps per task at Alliance Center L1, +1 per level → ~29–30 at L25; helpers earn individual credits [snippet]. At 29 helps of max(1%, 3 min): 5 h → 3 h 33 m (−87 min), 126 d → 94 d 03 h (−25%); timers under ~1.5 h erased [derived: `python tools/curve.py --levels 2 --first 5h --last 126d --shape geometric --helps 29 --help-floor 180s`]. | A social speed-up that pays both sides; `max(cut·R, floor)` erases short timers and trims long ones. | Help decides the early game but trims only ~25% late, so the late game runs on speed-ups [snippet]. | Floor 2 min from day 1 (3 min after research); 10 → 30 helps by alliance-building tier; a top alliance takes ≤ 30% off a 14 d timer; one server write per "help all" tap — [core-loop.md](core-loop.md) §6; [alliance.md](alliance.md). |
| Typed speed-ups (build, research, train, heal) + universal, 1 min to multi-day [unverified list]; the main earned-and-bought commodity; events reward spending them [snippet]. | Speed-ups are a currency counted in minutes. | Month-long timers make speed-ups the only lever → speed-up hoarding [snippet]; events that score speed-ups spent turn a stockpile into rank [derived]. | Seven hourglass sizes priced `p(m) = k·m^0.9`; unused minutes given back; honest inventory; events score work finished, never hourglasses spent — [core-loop.md](core-loop.md) §5; [liveops.md](liveops.md). |
| Random daily quests → activity points; chests at 20/40/60/80/100; the 100-point chest = 100 gems + gold key + magic box; reset 00:00 UTC; VIP login points 40 per day, +20 per consecutive day, to 200 [snippet] → the top rate needs 9 days in a row [derived]. | One daily point bar with staged chests; a streak that pays for returning. | The loop becomes chores, a "second job" [snippet]; a streak that grows only on consecutive days suggests a reset after one missed day [unverified]. | A fixed list + 2 rotating slots, 150 points offered and 100 counted; chests at 30/60/100; a missed day moves the streak back ONE step; the weekly top chest needs 5 of 7 days — [core-loop.md](core-loop.md) §7. |
| "Playable in five-minute bursts": collect, help all, refill queues, send gatherers, spend AP; plus scheduled long sessions — rallies, KvK fights, Ark of Osiris at exactly 60 min [snippet]. | Short check-ins keep the habit; scheduled long sessions carry the social stakes. | Long sessions tied to fixed hours shut out time zones [snippet]; the "second job" [snippet]. | Check-in ≤ 5 min and ≤ 30 taps, 0 idle plates at exit; war sessions of 30 min inside ≤ 60-min windows, two a day 12 h apart; anti-chore rules A1–A10 — [core-loop.md](core-loop.md) §8–§9. |

| Weak spot returns if | Caught by |
|---|---|
| A plate, bed or march-slot count appears on any paid surface | [ ] offer-data grep returns 0 ([core-loop.md](core-loop.md) §2) |
| A player with 2 visits a day loses energy | [ ] loop sim: loss 0% for the 2-visit profile |
| The late check-in needs > 30 taps or > 5 min | [ ] `core/session_audit.gd` check-in pass |

## 2. City progression

Decides what the player builds next, what it unlocks, and how long the whole climb takes.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| City Hall, max 25, gates every building and troop tier [snippet]; ages Stone (CH 1–4), Bronze (5–10), Iron (11–16), Dark (17–21), Feudal (22–25) [boundaries inferred from march unlocks; unverified]; the city's look changes per age [snippet]. | One spine building gates everything; every 5–6 levels an age bundles a mechanical unlock with a visible change of the whole city. | Tier 4 needs CH 21 + Academy 21 + research; tier 5 needs CH 25 + Academy 25 + the full economic tree + military prerequisites [snippet] → the long gap to the top tier splits spenders from free players for months [snippet]. | The keep is our spine; troop-tier bands t1–10 (cavalry t1–11) spread over its levels, each band tied to a visible castle age (6 visual tiers, [architecture.md](../../blender-forge/references/architecture.md) §4) — [progression.md](progression.md). |
| CH 10 ~24 h; CH 25 = 126 d 3 h base plus 82.25M food, 82.25M wood, 36M stone; most of the total cost sits in the last 3–4 levels; a new city's power is 1,033 [snippet]; with 29 helps CH 25 still takes ≈ 94 d [derived, §1 help row]. | A phased timer curve: minutes at first, about a day by level 10, long at the top. | The 126-day base timer turns the final levels into a speed-up and wallet check with a "rush" meta [snippet]. | No single timer above 14 d base ([core-loop.md](core-loop.md) §4); depth grows by breadth (more parallel goals), not by longer timers; `curve.py --shape phased` table per ladder — [progression.md](progression.md); [numbers.md](numbers.md) §1. |
| CH 25 needs Wall 24 + Trading Post 24 plus others [exact set unverified]; guides: raise everything to the CH level before each CH upgrade [snippet]. | Prerequisite chains force breadth, so the city grows as a whole. | Upgrading buildings nobody uses, only as prerequisites, feels like a tax [snippet]. | Rule: a prerequisite must itself grant something the player uses — [progression.md](progression.md). |
| ~26 buildings; several own one number each: Castle = rally capacity, Wall = garrison commanders, Watchtower = warnings and scouting, Alliance Center = help count, Storehouse = raid protection; plus a history-quiz building at CH 10 [snippet]. | Each building owns one number the player cares about. | Buildings that own nothing the player uses become the prerequisite tax above [snippet]. | 34 archetypes × 6 tiers ([buildings.md](../../game-art-director/references/buildings.md)); each tier changes the silhouette and one owned number — [progression.md](progression.md); castle-forge. |

| Weak spot returns if | Caught by |
|---|---|
| Any single timer above 14 d base ships | [ ] `curve.py` table per ladder: top rung ≤ 14 d |
| A prerequisite level grants nothing the player uses | [ ] prerequisite graph check: every edge names what it grants ([progression.md](progression.md)) |
| A troop-tier band opens with no visible castle change | [ ] red-team #5 + the six-tier silhouette test ([architecture.md](../../blender-forge/references/architecture.md) §4) |

## 3. Economy

Decides where resources come from, where they go, and what is at risk.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Food, wood, stone, gold + gems (premium); gold barely matters early and becomes the late bottleneck [snippet]; healing 100k tier-4 troops ≈ 72M food, 72M wood, 54M stone, 7.2M gold, tier 5 ≈ 192M, 192M, 144M, 144M gold → gold ×20 per tier step [one guide; unverified]. | The resource mix rotates by tier; a late tier gets its own limiting resource. | The top-tier heal cost makes players avoid fighting [snippet]. | Five resources (gold, food, wood, stone, iron) + gems + rp; iron as the t6+ throttle (PROPOSAL, verify shipped costs); healing always cheaper than training ([numbers.md](numbers.md) §5) — [economy.md](economy.md); [combat.md](combat.md). |
| Small passive city output; map gathering is the main source; loot from barbarians, forts, villages, caves; dailies and events; pack items; raiding inactive cities; alliance territory; gem deposits on the map, so free players gather premium currency [snippet]. | Map gathering as main income gives land economic value; a free, visible route to premium currency. | Gathering is idle busywork; raiding inactive cities is a norm [snippet]. | Gathering vs city production balance; map gem veins for free players; time-first gathering batches ("until I'm back") — [economy.md](economy.md); [core-loop.md](core-loop.md) §9 A3; [world.md](world.md). |
| +25% gathering on alliance-owned resource points inside territory; siege carries most load, cavalry gathers fastest; richer nodes in Zones 2–3; node levels and yields not found [snippet]. | Where you gather depends on who holds the land. | Lopsided zones and inactive cities make the map feel settled, not alive [snippet]. | Territory has economic value in resource terms — [economy.md](economy.md); [world.md](world.md); [alliance.md](alliance.md). |
| The Storehouse protects a fixed amount, the rest is raidable [snippet]; resources held as ITEMS cannot be raided [observational]. | Surplus above protection is at risk, so hoarding is risky and raiding has a target. | Item-stored resources make the storehouse pointless [observational]. | Items count against protection when opened, or stay unraidable only up to a cap — [economy.md](economy.md). |
| Resource transfer between allies with a tax [observational]; farm accounts are standard practice and guides teach them [snippet]. | Allies can move resources to each other. | Farm accounts feed main accounts, so multi-accounting becomes expected play [snippet]. | Transfer tax, trade caps by keep level, alliance-only transfers, same-device heuristics; chest rewards bound to the account — [economy.md](economy.md); [core-loop.md](core-loop.md) §7. |
| Apparently no hourly food upkeep; armies cost only at training and healing [unverified]; inflation held by exponential costs, tier-gated gold, heal costs, migration power caps, transfer tax [observational]. | Layered sinks, each tier and activity with its own drain, instead of a running tax that punishes absence. | The biggest late sink sits on healing, so it falls on the act the game wants — fighting [derived, row 1]. | The upkeep decision (light food upkeep or none) argued in [economy.md](economy.md); sinks/sources 0.90–1.10 at day 30 for the median free player (`tools/econ_sim.py`, [numbers.md](numbers.md) §6). |

| Weak spot returns if | Caught by |
|---|---|
| Resources leave protection through items without a limit | [ ] economy test: opening items cannot lift stock above the protected cap ([economy.md](economy.md)) |
| A young account can move more to a main than its keep level allows | [ ] server test of transfer caps by keep level |
| Day-30 sinks/sources outside 0.90–1.10 with no named reason | [ ] `econ_sim.py` HOARD / WALL verdict |

## 4. Troops and combat

Decides who wins a fight, what it costs, and whether choices beat raw size. Our moves are PROPOSALS
until checked against the shipped counter table and the sacred constants; gameplay-forge owns the
frozen resolver, battle-forge the presentation.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Infantry, cavalry, archers in a triangle: cavalry > archers > infantry > cavalry at +5% damage; all three +5% vs siege; talents can raise it; a mixed march moves at its slowest unit (cavalry > archers > infantry > siege) [snippet]. | A small, readable counter cycle; siege outside it with its own job (structures, load). | "PvP isn't about tactics, just raw power" (MMOHuts); a 5% counter is buried under talent, equipment and VIP stacks [snippet]. | Five-line graph (e.g. spearmen brace vs cavalry, cavalry run down archers and crossbows, archers vs infantry, crossbows vs armoured, infantry vs spearmen) at +20–50%, so t(n) + counter ≈ t(n+1); lords' contribution capped so stacks never cancel a counter; siege engines outside the cycle — [combat.md](combat.md); [lords.md](lords.md); siege-forge. |
| Tiers T1–T5; power per unit T4 = 4, T5 = 10 [snippet]; T1–3 often quoted as 1/2/3 [unverified]; a T4 → T5 upgrade adds 6 power for the cost of a fresh T5; kill points T4 10, T5 20; weekly-event training points T1 5, T2 10, T3 20, T4 40, T5 100 [snippet]. | One monotonic power number to compare and pick targets. | The top power ranking is openly a spending contest [snippet]. | `p_t = p1·k^(t−1)`, k 1.35–1.5 over 10 tiers (t10 ≈ 15–38× t1); power shown as a guide, counters and lords decide ([numbers.md](numbers.md) §3) — [combat.md](combat.md). |
| Damage formula known only from community models; older models scale with √troops (2× army ≈ 1.41× damage), disputed; skill modifiers dominate [community estimate]. | Sub-linear mass: doubling an army is strong but not decisive. | An unpublished formula leaves players guessing why they lost [derived: only community models exist]. | damage ∝ q·N^α, α 0.5–0.8, fixed once in the frozen resolver ([numbers.md](numbers.md) §4); the resolver emits "why you won / lost" data for report-forge — [combat.md](combat.md). |
| Slightly wounded (healed free on return), severely wounded (hospital; die if it is full), dead. Defending own city → all severely wounded; field → hospital; defending an ally's city or alliance building → half die; attacking a city or alliance building → all die; shrines and level-2 passes → half die; Lost Temple and level-3 passes → all die [snippet]; hospital ~7,500 at L1, ~75,000 at L25 [one guide; per-hospital unclear]. | Loss severity by context: defence and PvE cheap, attack costly — protects casual players and makes aggression a commitment. | Hospital overflow → death spirals; players who are zeroed quit [snippet]. | Three buckets with our own context table (own castle, field, attacking a castle, camps, alliance structures); beds sized so one lost full march fits and heals ≤ 8 h without speed-ups — [combat.md](combat.md); [core-loop.md](core-loop.md) §2. |
| Real-time field combat on the map [snippet], ~1 turn per second [community estimate]; each army attacks once per turn and counterattacks every attacker; several armies on one target → "Surrounded ×N" (it counterattacks all, gains rage faster, takes more damage); each attacker gets its own PvE reward; retreat or reinforce at any time [snippet]; most active skills cost 1,000 rage, ~100 per normal attack, ~91 per turn → first cast after ~11 turns, then ~10; overflow wasted [community estimate]. | Combat as a persistent, joinable, visible event on the map; skill casts on a ~10 s rhythm. | No player complaint documented; the cost is ours: a per-second server simulation of every fight breaks the €200/month budget (SKILL.md rule 5). | Marches as functions of time (start, end, path); deterministic resolution at arrival; beats replayed on the client by battle-forge; skill moments on a tempo meter ([lords.md](lords.md)) — [combat.md](combat.md). |
| Castle level = rally capacity; rally wait 5 or 10 min up to 8 h; reinforceable en route; the Wall holds a primary + secondary garrison commander; CH caps reinforcement; if watchtower and garrison fall the wall burns; at 0 durability the city is teleported randomly [snippet]; march capacity ~110k at CH 22 [unverified]. | Group attacks with a join window; defence = garrison lord + reinforcements + a wall with durability. | Rallies bound to one time zone [snippet]; zeroed players quit [snippet]; a random teleport can land a player far from their alliance [derived]. | Rally windows and auto-join; garrison and reinforcement rules; wall at zero → a burning state with repair, or relocation near the alliance (PROPOSAL) — [combat.md](combat.md); [alliance.md](alliance.md); battle-forge. |

| Weak spot returns if | Caught by |
|---|---|
| t(n) + counter loses clearly to t(n+1) (the counter is too small to see) | [ ] resolver harness, seeded mirror fights per line pair (gameplay-forge; qa-forge writes it) |
| One lord + gear build cancels a counter | [ ] contribution-cap check on the strongest build ([combat.md](combat.md)) |
| One lost full march of a median player overflows the hospital | [ ] hospital sizing test ([combat.md](combat.md)) |
| A fight is ticked per second on the server | [ ] `core/sd_cost_probe.gd` march and resolution lines |

## 5. Lords (commanders)

Decides who leads a march, how a player builds them, and whether yesterday's investment survives today's release.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Rarities Legendary, Epic, Elite, Advanced; each civilization has a starting commander; level cap 60; stars 1–6, each +10 level cap; stars fed by rarity-specific Starlight Sculptures (regular, blessed, bundle) that give XP and "luck" [snippet]. | Rarity sets the ceiling; a duplicate-style upgrade currency raises it step by step. | "Luck" hides the true cost; no pity timer was found [snippet]. | Four tiers Issued → Sound → Fine → Masterwork; duplicates → an upgrade currency with PUBLISHED math and a pity counter — [lords.md](lords.md). |
| 4 skills, levels 1–5, raised with commander-specific sculptures; Expertise unlocks when all four are maxed; sculptures to max: Legendary 690 (+10 to unlock), Epic 440, Elite 340, Advanced 240 [snippet]. | A capstone earned by completing the kit. | A 690-sculpture grind per legendary [snippet]; a rank-1 weekly finish (180) covers 26% of one [derived]. | Skill counts, the tempo meter and the capstone in [lords.md](lords.md), with a free path to max per rarity written in days. |
| 3 of 15 specialty trees per commander (red = troop type, yellow = role, blue = combat style); up to 74 points (1 per level + extras at 5–6 stars) [snippet]. | Build variety from a small choice per lord. | Talent complexity scares newcomers [snippet]; dense talent screens [observational]. | ≤ 3 branches, ≤ 30–40 points; a guided first talent point when talents unlock — [lords.md](lords.md); [onboarding.md](onboarding.md); [ux.md](ux.md). |
| Primary + secondary; both contribute skills; only the primary's talents and equipment apply [snippet]; the primary needs ≥ 3 stars before the secondary's skills apply [unverified]. | Pairing squares build space without doubling content. | Menus stack deep: skills, talents, stars, equipment, pairing [observational]. | Primary + secondary, only the primary's talents and gear apply; saved pair presets for the war session ([core-loop.md](core-loop.md) §8.3) — [lords.md](lords.md); commander-forge. |
| Equipment is crafted at the Blacksmith [snippet]: 6 armour slots + accessories [slot count unverified]; 5 rarity grades; 4 materials, combine 4 → next grade; 30 blueprints per craft [snippet]. | A material ladder: lower grades combine into higher ones. | Equipment stats stack on top of counters and bury them [snippet]. | 24 items = 6 four-piece sets, one per lord ([equipment.md](../../game-art-director/references/equipment.md)); set bonuses inside the lords' contribution cap — [lords.md](lords.md); [combat.md](combat.md). |
| Tavern silver keys (Elite/Advanced) and gold keys (Legendary/Epic/Elite), a free gold chest ~every 2 days; legendary sculpture ~3.023% of gold-chest drops; VIP 10 daily gold key, VIP 14 daily legendary sculpture purchase; Wheel of Fortune exclusives ~every 2 weeks for 3 days, 1 free spin; weekly event of 6 days: rank 1 = 180 sculptures, rank 2 = 90, ranks 46–50 = 1; Expedition shop (70 PvE stages, 300 medals per day cap) with a weekly featured Epic; VIP-bundle exclusives; KvK shops; a 4-player boss event [snippet]. | Each rarity has its own channel tied to a different activity: PvE, competition, chance, spend, time. | Weekly rewards are winner-take-most (rank 1 = 2× rank 2 = 180× rank 46–50 [derived]) and spend-driven; some commanders only in paid bundles [snippet]; free chests alone give ≈ 5.5 legendary sculptures a year vs 690 to max [derived; assumes 1 sculpture per drop]. | Channels mapped to PvE, alliance, events, time and purchase; no lord sold exclusively; milestone rewards instead of rank ladders — [lords.md](lords.md); [monetization.md](monetization.md); [liveops.md](liveops.md). |
| New legendaries gated by kingdom season; stars in young kingdoms fall behind season commanders + crystal tech; the developer reworked old talent trees, fixed creep in one damage type, nerfed outliers (a slow on 5 targets at 50% → single-target stacking) [snippet]. | Release by realm age; periodic rework instead of silent creep. | Power creep wipes out investment: "miss a meta commander → stuck" [snippet]. | New lords are sidegrades; a fixed rework cadence; investment refunded or moved when a lord is rebalanced — [lords.md](lords.md). |

| Weak spot returns if | Caught by |
|---|---|
| A rarity has no free path to max, or its length is not written | [ ] free-path table, one row per rarity ([lords.md](lords.md)) |
| Upgrade odds are unpublished, or a chance draw has no pity counter | [ ] compliance check ([monetization.md](monetization.md)) |
| A new lord beats every lord of its role on every axis | [ ] sidegrade check against the role table ([lords.md](lords.md)) |

## 6. World map

Decides where players live, what they fight over, and what everyone can see.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| ~1200 × 1200 units bounded by impassable mountains [snippet]; 3 zones: 6 outer Zone-1 regions, 3 Zone-2, 1 central Zone-3 [one guide]; passes of level 1–3 gate the zones [snippet]. | Geography is progression: taking passes opens inner regions. | Zone-1 players fall behind; lopsided zones [snippet]. | Passes, bridges and fords gate inner regions; realm size N per shard costed for 50,000 players — [world.md](world.md). |
| Holy sites (shrines, altars, sanctums) give alliance-wide buffs; owned passes allow targeted teleports between the regions they join; the Lost Temple opens every 7 days and must be held 8 h; its holder's leader becomes King and grants titles — Architect (build speed), Scientist (research + gold gathering), Duke (training speed + troop defence), Justice (war) — and debuff titles (Traitor, Fool) [snippet]. | A contested ladder so every alliance size has a goal; the top grants titles others can see. | Late kingdoms freeze under one dominant alliance; truces make the map static [snippet]. | Our ladder (watch-post → chapel → abbey → high seat → crown seat; names PROPOSAL); dominant-alliance decay and landmark rotation — [world.md](world.md); [liveops.md](liveops.md). |
| Pinch zoom city → region → world with no loading screens; inspired by diving drone shots and phone pinch-to-zoom; marketed as the first mobile unlimited-zoom map; the team reviewed the zoom transition frame by frame; all action on one map, no separate battle scenes [snippet]. | One continuous space; fights happen where they are. | None documented; the research calls it the defining innovation [snippet]; the risk is ours: streaming cost at every zoom band. | Zoom levels castle ↔ region ↔ realm and what shows at each — [world.md](world.md); [ux.md](ux.md); transition-forge (frame-by-frame review). |
| Map starts fogged; Scout Camp 1 scout and 5 × 5 blocks → 3 scouts, 15 × 15 blocks, +125% scout speed at max; only fog next to cleared ground can be explored; clearing is permanent [snippet]; march lines visible to all, green self / blue ally / red enemy; the watchtower warns and gives better scout reports with level [snippet]. | Fog clearing is early PvE with a permanent reward; public march lines make the map shared information and a place to bluff. | Colour-only relationship coding fails colour-blind players [derived; no source]. | Fog and scouting information tiers; a reserved self/ally/enemy/neutral palette plus shape coding — [world.md](world.md); [combat.md](combat.md); [readability.md](../../game-art-director/references/readability.md). |
| A new city attacks only level-1 barbarians; each level unlocks by beating the previous [snippet]; L1–12 spawn near cities, Zone 2 up to ~20, Zone 3 up to ~25 [older guide]; barbarian forts are rally-only, rewards scale with each participant's damage share [snippet]. | Camps unlocked level by level; rally-only strongholds as alliance PvE with damage-share rewards. | None documented; a pure damage share pays the biggest marches most [derived]. | Barbarian camps level by level; rally-only strongholds with damage-share rewards, checked so the smallest joiner still earns — [world.md](world.md). |
| Centre fortress → more fortresses → up to 500 flags; first flag 50,000 alliance credits, price rises every 10 flags; +1 member slot per 10 flags; resource points inside territory are alliance-owned with +25% gathering [snippet]. | Territory as a costed alliance project that pays in gathering and member slots. | Land → slots → members lets the leading alliance grow further [derived]; kingdoms freeze [snippet]. | Banners (our fiction) with growth limits and decay — [world.md](world.md); [alliance.md](alliance.md). |
| Teleports: random (anywhere), territorial (into own territory, ignores zone locks), targeted (anywhere in a reachable region; crossing regions needs an owned pass); none while an attack is incoming [snippet]. | Relocation types graded by power; never away from an incoming attack. | Gem-bought teleports are a paid advantage [snippet]. | Relocation rules with no gem-only advantage in war seasons — [world.md](world.md); [monetization.md](monetization.md). |

| Weak spot returns if | Caught by |
|---|---|
| One alliance holds the top landmark for more cycles in a row than the decay rule allows | [ ] realm telemetry + the decay rule's unit test ([world.md](world.md)) |
| A relocation away from an incoming attack succeeds | [ ] server rule test |
| Marches or map scans tick on the server | [ ] `core/sd_cost_probe.gd`; map queries by tile chunk ([world.md](world.md)) |

## 7. Alliance systems

Decides why players join, stay and give, and what it costs the people who lead.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| R5 leader; R4 officers (kick, promote/demote, accept, schedule, build flags and structures, see member coordinates); R1–R3 used as trial / standard / core [snippet]. | Five ranks with real power delegated to officers. | Leader burnout: diplomacy, schedules, discipline [snippet]. | Five ranks with our names; officer delegation, scheduled announcements, succession after N inactive days — [alliance.md](alliance.md). |
| Alliance credits (collective; R4/R5 spend them on tech, flags, fortresses, shop stock) and individual credits (from helping, donating, alliance chests; spent on speed-ups, keys, VIP points, shields) [snippet]. | Collective goods funded by many small acts, each contributor paid privately — free-riding stops paying. | Alliance hopping [snippet]; personal credit earned in one alliance leaves with the player [derived]. | Alliance vs personal currency; hopping cooldown and contribution reset — [alliance.md](alliance.md). |
| Every member gets a gift whenever any member buys a bundle, kills a barbarian fort or defeats the boss; gift level rises (better every 10 levels); key points fill a big chest [snippet]. | One member's success becomes a visible gift to all. | Bundle gifts normalise spending [snippet]. | Gifts from PvE kills and member achievements; gifts from purchases capped or cosmetic — [alliance.md](alliance.md); [monetization.md](monetization.md). |
| Help, rallies, territory, tech funded by donated resources; 300 gems for joining a first alliance [snippet]. | An early join reward, because alliance members retain; research as a shared project. | Rallies bound to one time zone [snippet]. | A concrete join reward ([onboarding.md](onboarding.md)); rally windows and auto-join across time zones — [alliance.md](alliance.md). |
| Member cap raised by alliance techs, fortresses and +1 per 10 flags [snippet]; base and max ~150 [unverified]. | Size grows with the alliance's shared projects. | The leading alliance absorbs the realm (§6) [snippet]. | Size cap and growth rules — [alliance.md](alliance.md); [world.md](world.md). |

| Weak spot returns if | Caught by |
|---|---|
| A leader is absent N days and nobody takes over | [ ] succession test ([alliance.md](alliance.md)) |
| A purchase gives other members non-cosmetic value above the cap | [ ] offer-data check ([monetization.md](monetization.md)) |
| A rally can be joined only inside one time zone's evening | [ ] rally-window schedule check ([alliance.md](alliance.md)) |

## 8. Seasons, events and realm lifecycle

Decides what changes week to week, and how a realm is born, peaks and ends.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Kingdoms open in pairs every ~12 h [snippet], now ~30 h [unverified]; new-kingdom event of 8 days, 3 side events unlocked daily for the first 5 days [snippet]. | Content unlocks by realm age, so every realm lives a story arc. | Dying kingdoms [snippet]. | Realm age arc (days 0–7 with daily unlocks, then 30, 60, 90); merges for dying realms — [liveops.md](liveops.md). |
| Pre-KvK at kingdom age 75–95 days; KvK ~50 days + pre-phase; honor points → individual and alliance rankings; staged unlocks; a central objective; ~8 kingdoms [snippet; format varied]; KvK 2 and 3 ~50 days each; later Season of Conquest: multi-chapter, crystal tech, coalitions, season coins [snippet]; ~10 kingdoms [unverified]; the King picks the kingdom's story [snippet]. | Cross-realm seasons refresh competition before one realm's leaders set hard. | KvK fatigue: 50-day wars, time-zone coordination, a "second job" [snippet]. | Far shorter seasons (PROPOSAL ≤ 4–6 weeks) with time-zone-fair windows: ≤ 60 min, two a day 12 h apart ([core-loop.md](core-loop.md) §8.3); the chronicle ties in (story-forge) — [liveops.md](liveops.md). |
| Migration only into kingdoms > 120 days old; power caps rise by season (10M / 15M / 25M / 35M); beginners may move into newer kingdoms if CH ≤ 8, within 10 days, or before season-1 pre-KvK [snippet]. | Power-capped migration protects small realms; beginners are routed to fresh ones. | Migration caps trap players [snippet]. | Fair caps with no trapping; late-joiner routing — [liveops.md](liveops.md); [onboarding.md](onboarding.md). |
| Weekly competitive event of 6 stages × 24 h, Mon–Sat; Wheel ~every 2 weeks for 3 days; alliance league of 512 alliances in 32 divisions on Sundays; 70-stage PvE expedition; 80-level battle pass; an in-game event calendar, one of the first in mobile games [snippet]. | A fixed weekly rhythm, published ahead in a calendar. | Too many events → red-dot overload [snippet]; winner-take-most weekly rewards (§5) [snippet]. | Event taxonomy with MILESTONE rewards; a hard cap on concurrent events; calendar visible ≥ 2 weeks ahead — [liveops.md](liveops.md); [ux.md](ux.md). |
| Arena: 5 armies with IDENTICAL tier-3 troops, only commander skills, talents and equipment count, 5 free attempts a day, 7-day seasons; 30v30 of exactly 60 min, NO troop losses, 3 phases, the first captured objective grants 8 teleports; 5v5 of 10 min, 3 marches each, event-assigned troops, a morale bar, ~every 2 weeks [snippet]. | Loss-free, standardized modes give a skill outlet beside the money-heavy persistent war. | In the identical-troop arena commander investment still counts [snippet], so spend still shows [derived]. | Tourneys, jousts and trial grounds with identical troops; lord investment normalized or capped there (PROPOSAL) — [liveops.md](liveops.md). |

| Weak spot returns if | Caught by |
|---|---|
| An event pays mainly by rank instead of by milestones | [ ] reward-shape lint on the event data ([liveops.md](liveops.md)) |
| Concurrent events exceed the cap, or the calendar shows < 14 days ahead | [ ] calendar lint ([liveops.md](liveops.md)) |
| A war window runs > 60 min, or a day has only one window | [ ] calendar lint against [core-loop.md](core-loop.md) §8.3 |

## 9. Monetization

Decides what money buys, and whether a free player who plays well can still reach the top.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| $0.99 starter (commander, VIP, gems); 8 initial $4.99 offers (one one-time, the rest timed); offers adapt to progress and events [snippet]. | A cheap first purchase; offers matched to the player's current goal. | Offers crowd core navigation [observational]. | An offer ladder of goods, works and journeys, never on core navigation; no war imagery over a buy button (money-law) — [monetization.md](monetization.md); shop-forge. |
| VIP points: 40–200 per day from login streaks, 1 per gem spent, 100-point items for 50k individual alliance credits; VIP 6 permanent 2nd builder, VIP 10 daily gold key + legendary sculpture in the daily chest, VIP 14 daily legendary sculpture purchase [snippet]; top ~VIP 17–18 + "SVIP" [unverified]; packages cheap at VIP 1 and climbing; commanders exclusive to VIP bundles — a sunk-cost ladder (GameRefinery) [snippet]. | A persistent status ladder fed by play as well as payment. | Convoluted VIP (MMOHuts); a core queue and exclusive commanders behind it [snippet]. | A patron ladder fed by play and payment that sells no plate count, no lord and no PvP stats — [monetization.md](monetization.md); [core-loop.md](core-loop.md) §2. |
| Battle pass of 80 levels at $4.99, or $19.99 with +10 levels and +50% progress points [snippet]. | A season pass as a daily reason to return. | Paid +50% progress widens the gap inside a competitive season [derived]. | A chronicle pass with a full free track, free-track top at 70% of days ([core-loop.md](core-loop.md) §7); the paid track sells no progress speed in PvP seasons (PROPOSAL) — [monetization.md](monetization.md). |
| City skins carry stats; a later "transmog" keeps one skin's stats under another's look [snippet]; anecdotes of five-figure spends on city themes [unverified]. | Visible cosmetics are a spend other players can see. | Stat-bearing skins blur cosmetic and power [snippet]. | Cosmetics never carry stats — [monetization.md](monetization.md). |
| Gold-key chests: legendary sculpture at ~3.023% of drops; no pity timer found [snippet]. | Chance draws with published odds. | Without pity, an unlucky player's cost has no ceiling [derived]. | Odds disclosed per store rules; a pity counter on every chance draw; age-rating compliance — [monetization.md](monetization.md); [lords.md](lords.md). |
| Pay-gated: queue count, exclusive commanders, compressing month-long timers, KvK healing, teleports, shields; time-gated: kingdom-age content, KvK schedule, AP regen, VIP login points, daily gold chests; fairness valves: identical-troop arena, no-loss 30v30, event-assigned 5v5 [snippet]. | Time gates bind everyone; fairness modes exist where money cannot win. | No spending cap; the top power ranking is a spending contest; top-server whales at $10–20k+ are common; "$200/month for dailies" counts as a light spender; "cannot see a way to dominate without tons of time or serious cash" (MMOHuts, 2/5); counter-view: free players have real roles in gathering, filling rallies and scouting [snippet]. | A spending ceiling or diminishing effect in PvP seasons (PROPOSAL); gem finishes on muster and infirmary capped per war window (recommended ≤ 480 min, [core-loop.md](core-loop.md) §5); fairness metric = free share of top-100 power; free path per system (SKILL.md rule 6) — [monetization.md](monetization.md). |

| Weak spot returns if | Caught by |
|---|---|
| A plate count, an exclusive lord, a stat on a cosmetic, or a shield during an attack is on sale | [ ] offer-data grep against the red-lines list ([monetization.md](monetization.md)) |
| War imagery appears on or behind a buy button | [ ] screenshot review of every paid surface (money-law) |
| The free share of top-100 power falls below target | [ ] season telemetry ([monetization.md](monetization.md)) |

## 10. Onboarding (first session, first week)

Decides whether a new player understands the game before the systems that keep them arrive.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| First real decision: a civilization (bonuses, special unit, starting Epic commander); free change at CH 10 [snippet]. | One reversible identity choice up front. | Early investments are often "wrong" (power-crept) and paid to redo [snippet]. | One reversible identity choice with a free change later — [onboarding.md](onboarding.md). |
| Scripted tutorial: Stone Age village, a barbarian fight, build / train / heal, then the zoom-out to the kingdom map, then chapter quests [observational]; early upgrades take minutes, CH 10 ~1 day [snippet]. | Teach by doing; the zoom-out to the world is the tutorial's reveal. | It never teaches the systems that decide retention — rallies, garrisons, KvK, talent planning — so players learn from YouTube and wikis [snippet]. | First 10 minutes minute by minute, first win ≤ 60 s; guided "first time" moments for rallies, garrison, seasons and lord talents when each unlocks — [onboarding.md](onboarding.md); onboarding-forge. |
| New cities start shielded [duration unverified]; "don't break it by attacking"; a free 2-day 2nd builder at start [snippet]. | Safe PvE and a peace shield while learning. | The shield breaks on the player's own attack [snippet], so a learner who fights loses protection [derived]. | A newcomer peace ward; its length and what breaks it — [onboarding.md](onboarding.md). |
| 300 gems for joining an alliance; a $0.99 offer early; an 8-day new-kingdom event races players through CH, power and gathering with daily unlocks [snippet]. | Early alliance nudge with a concrete reward; a daily unlock arc. | Too many event icons at once [snippet]. | Early alliance nudge; a day 1–7 unlock arc under the icon cap — [onboarding.md](onboarding.md); [liveops.md](liveops.md); [ux.md](ux.md). |
| Beginner move to newer kingdoms if CH ≤ 8, within 10 days [snippet]. | Route late starters to fresh realms. | After the window, a late joiner is locked into an old realm; migration caps trap players [snippet]. | Late-joiner routing — [onboarding.md](onboarding.md); [liveops.md](liveops.md). |

| Weak spot returns if | Caught by |
|---|---|
| A late system unlocks with no guided first-time moment | [ ] unlock table vs the system list in [SKILL.md](../SKILL.md) ([onboarding.md](onboarding.md)) |
| First win takes > 60 s from first input | [ ] FTUE timing capture (onboarding-forge) |
| Tutorial completion or D1 under target | [ ] FTUE metrics ([onboarding.md](onboarding.md); [numbers.md](numbers.md) §8) |

## 11. UI / UX (mostly [observational])

Decides whether a player finds everything in one hand, in a 10-second visit and in a 20-minute one.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Top-left avatar / power / VIP / AP; top resource bar + gems; right edge stacked collapsible event and offer icons; left edge sliding queue + march tracker and recommended quest; bottom-left map/city toggle + search; bottom chat ticker; bottom-right expanding menu; inbox top-right [observational]. | Fixed zones: status top, queues left, events right, navigation bottom. | Icon clutter; offers crowding core navigation [observational]. | HUD zones as % of a 1080 × 1920 screen; thumb zones; ≤ 3 taps to any core action — [ux.md](ux.md); ui-forge. |
| Floating status bubbles over buildings (collect, help hand, idle queue); "help all" in one tap [observational]. | State shown where it lives; one-tap social actions. | Collect bubbles make harvesting a tap chore [derived]. | Status bubbles; production collected on open ([core-loop.md](core-loop.md) §9 A1) — [ux.md](ux.md). |
| Red dots on anything claimable; settings to turn off screen flashing and title notifications [observational]. | One signal for "something to claim". | Red-dot fatigue [observational]. | A red-dot budget (≤ 3 at open for the median player, [core-loop.md](core-loop.md) §9 A7), priority and auto-expiry; notification tiers — [ux.md](ux.md). |
| One space (map / city zoom), not separate scenes [snippet]; deep menus (commander screens: skills, talents, stars, equipment, pairing) [observational]. | One continuous space with two modes. | Dense, beginner-hostile talent and equipment screens [observational]. | One continuous castle ↔ realm space; the ≤ 3-tap rule — [ux.md](ux.md); transition-forge; ui-forge. |
| Close zoom = detailed city; mid = marches, lines, troop icons; far = city icons with alliance tags and territory colours [observational]; green / blue / red relationship colours [snippet]. | Each zoom band shows one layer of information. | Colour-only relationship coding fails colour-blind players [derived; no source]. | Read distances, minimum text sizes, tap targets ≥ 44–48 dp, relationship shown by shape as well as colour — [ux.md](ux.md); [readability.md](../../game-art-director/references/readability.md). |

| Weak spot returns if | Caught by |
|---|---|
| > 3 red dots at open, or any dot on a paid surface | [ ] `ux_flow_probe` screenshot at session open |
| The event rail exceeds its cap, or a tap target is under the minimum | [ ] `layout_audit`; `ux_touch_probe` |
| Relationship is shown by colour alone anywhere | [ ] `a11y_audit` colour-blind pass |

## 12. Art direction

Decides whether the realm reads at every zoom and whether the art looks like one world.

| Genre does | Transferable pattern | Where it hurts players | Our move |
|---|---|---|---|
| Stylized "3D-cartoon", painterly, pastel-leaning colour; reviewers: "utterly cartoonish… as if Albert Uderzo had been a Pixar animator", "adorably cute, easy on the eye", some call it generic; commander portraits are semi-realistic painted illustrations with exaggerated features [snippet]; designs grew from sketches made on visits to the Chengdu Museum; the team's most-used word for its approach: "simple" [snippet; source not pinned]. | One simple style, applied everywhere, that reads at small sizes. | A cute look against a brutal war theme; generic to some [snippet]. | Keep OUR painted identity, not their look; lords semi-realistic, "calm and worn rather than posed" ([portraits.md](../../game-art-director/references/portraits.md)); value plan before materials — [art-direction.md](../../blender-forge/references/art-direction.md); [readability.md](../../game-art-director/references/readability.md). |
| Each civilization has its own architecture and changing it changes the city's style [snippet]; in practice regional families (East-Asian curved tile roofs, European stone and timber, Middle-Eastern domes) [unverified detail]; building models swap per age (thatch and palisades → stone keeps and walls), the age change is the "graduation" reward; skins layer on top, with stats [snippet]. | City age stages aligned to gameplay unlocks; architecture varied by culture family to scale factions cheaply. | Stat-bearing skins blur cosmetic and power [snippet]. | 6 visual tiers per building aligned to unlock bands, each step a new silhouette ([architecture.md](../../blender-forge/references/architecture.md) §4); house families of architecture — [art-direction.md](../../blender-forge/references/art-direction.md); [progression.md](progression.md). |
| Armies shown as a SMALL SQUAD of a few soldier models + commander banner + troop-type icon + health bar, not a count-true crowd [observational]; later "new 3D troop models" [snippet]; at far zoom cities, forts and holy sites become large readable icons with tags [observational]. | Token squads: readability and performance independent of army size. | None documented; for us a token squad without line identity reads as an empty figurine (the owner's standard) [derived]. | Token squad + banner + line icon in the line accents (infantry #B4432E, spearmen #8B8F95, archers #4F7A4A, crossbows #6D8AA8, cavalry #C9A76A) — [readability.md](../../game-art-director/references/readability.md); [units.md](../../game-art-director/references/units.md). |
| Relationship colours green / blue / red on public march lines [snippet]; skill casts are short bursts with damage numbers; mass battles stay readable at mid zoom [observational]. | Relationship colour is a reserved channel, never decoration; VFX restraint keeps battles readable. | None documented; the risk is decorative reuse of the reserved hues and colour-only coding [derived]. | Reserved self / ally / enemy / neutral channel with shape coding; VFX restraint numbers (burst length, max screen coverage) — [readability.md](../../game-art-director/references/readability.md); [effects.md](../../game-art-director/references/effects.md); battle-forge. |
| UI art: ornamental wood, parchment and gold frames, large clear icons, painted portraits; UI heavier than world art [observational]. | Silhouette and colour carry information far away; paint detail pays only up close. | UI chrome fights the painted world on small screens [observational]. | Chrome (OAK #4A2E1B, PARCHMENT #E8D9B5, GILT #C9A04C) never out-contrasts the art; ART SHOWN BIG; UI icons are Blender-made art, never line glyphs; contrast measured from renders — [readability.md](../../game-art-director/references/readability.md); [art-direction.md](../../blender-forge/references/art-direction.md); ui-forge. |

| Weak spot returns if | Caught by |
|---|---|
| A reserved relationship hue appears as decoration | [ ] critique rubric ([readability.md](../../game-art-director/references/readability.md)) |
| Chrome has higher local contrast than the art it frames | [ ] render contrast measurement ([art-direction.md](../../blender-forge/references/art-direction.md)); `contrast_test` |
| Two neighbouring castle ages share a silhouette | [ ] six-tier strip at 25% ([architecture.md](../../blender-forge/references/architecture.md) §4) |

## 13. Weak-spot register — what we fix, where, and by how much

| Genre weak spot (evidence) | Our fix | Number | File |
|---|---|---|---|
| Pay-to-win at the top, no spending cap (§9) | ceiling or diminishing effect in PvP seasons; war-window finish cap | ≤ 480 min gem finishes per window (recommended) | [monetization.md](monetization.md); [core-loop.md](core-loop.md) §5 |
| Core queue sold (§1, §9) | plate count earned only | 2 → 3 crews, 2 → 5 marches, by play | [core-loop.md](core-loop.md) §2 |
| 5% counters buried by stacks (§4) | bigger counters; lords' contribution cap | +20–50%; t(n) + counter ≈ t(n+1) | [combat.md](combat.md); [lords.md](lords.md) |
| 126-day timer wall (§2) | single-timer ceiling; breadth instead of length | ≤ 14 d base | [core-loop.md](core-loop.md) §4; [progression.md](progression.md) |
| Power creep; 690-item grind (§5) | sidegrades; published math + pity; refunds | free path to max per rarity, in days | [lords.md](lords.md) |
| War-season burnout (§8) | short seasons; two short windows a day | ≤ 60-min windows 12 h apart; seasons ≤ 4–6 weeks (PROPOSAL) | [liveops.md](liveops.md); [core-loop.md](core-loop.md) §8.3 |
| Red-dot and event overload (§8, §11) | dot budget; event cap; calendar | ≤ 3 dots at open; calendar ≥ 14 days ahead | [ux.md](ux.md); [liveops.md](liveops.md) |
| Farm accounts; item-stored resources (§3) | transfer caps; items count against protection; bound rewards | caps by keep level | [economy.md](economy.md) |
| Tutorial never teaches late systems (§10) | guided first-time moments | 1 per late system | [onboarding.md](onboarding.md) |
| Heal cost → fight avoidance; hospital death spiral (§3, §4) | heal cheaper than train; beds fit one lost march | heals ≤ 8 h without speed-ups | [combat.md](combat.md); [economy.md](economy.md) |
| One alliance freezes the realm (§6) | decay, landmark rotation, season resets | decay after N cycles held | [world.md](world.md); [liveops.md](liveops.md) |
| Leader burnout; alliance hopping (§7) | delegation, succession, cooldowns | succession after N inactive days | [alliance.md](alliance.md) |
| Stat cosmetics; paid-exclusive lords (§9) | red lines | 0 on sale | [monetization.md](monetization.md) |

## 14. Sources (claims from search snippets of these pages, 2026-09-26)

- **Snapshot**: https://en.wikipedia.org/wiki/Rise_of_Kingdoms · https://www.bluestacks.com/blog/game-guides/rise-of-kingdoms/name-change-rise-of-civilizations-2019-en.html · https://wnhub.io/news/finance/item-43560 · https://app2top.com/news/analysts-revenue-from-rise-of-kingdoms-exceeded-3-5-billion-267142.html · https://gamingonphone.com/news/lilith-games-rise-of-kingdoms-crosses-2-billion-in-lifetime-revenue/ · https://rok.lilith.com/
- **§1 Core loop**: https://www.appgamer.com/rise-of-kingdoms/strategy-guide/unlocking-the-2nd-builder-queue · https://riseofkingdoms.fandom.com/wiki/Troop_Dispatch_Queue · https://riseofkingdoms.fandom.com/wiki/Items/Speedup · https://riseofkingdomsguides.com/rise-of-kingdoms-action-points/ · https://riseofkingdoms.fandom.com/wiki/Quests/Daily_Objectives · https://riseofkingdoms.fandom.com/wiki/Buildings/Alliance_Center · https://www.rok.guide/alliance-guide/
- **§2 Progression**: https://riseofkingdoms.fandom.com/wiki/Buildings/City_Hall · https://www.pocketgamer.com/rise-of-kingdoms/city-hall/ · https://riseofkingdomsguides.com/rise-of-kingdoms-ages/ · https://riseofkingdoms.fandom.com/wiki/Buildings · https://www.ajackof.com/games/rise-of-kingdoms-lost-crusade/rok-t4-rush-guide-in-rise-of-kingdoms/ · https://riseofkingdomsguides.com/how-to-unlock-tier-5-units-fast/
- **§3 Economy**: https://riseofkingdoms.fandom.com/wiki/Resources · https://www.rok.guide/farming-guide/ · https://www.packsify.com/blogs/rise-of-kingdoms-t5-troops-guide · https://riseofkingdomsguides.com/is-gold-important-in-rise-of-kingdoms/
- **§4 Combat**: https://riseofkingdoms.fandom.com/wiki/Troop_Counters · https://riseofkingdoms.fandom.com/wiki/Troop_Guide · https://www.topuplive.com/news/rise-of-kingdoms-troops-tier-list.html · https://riseofkingdomsguides.com/rise-of-kingdoms-troop-guide/ · https://riseofkingdomsguides.com/rise-of-kingdoms-upgrading-troops-guide/ · https://riseofkingdoms.fandom.com/wiki/Buildings/Hospital · https://www.rok.guide/healing/ · https://theriagames.com/guide/rise-of-kingdoms-hospital-guide/ · https://rokdbot.com/en/blog/rage-mechanics-skill-uptime-guide-rok-2026 · https://www.bluestacks.com/blog/game-guides/rise-of-kingdoms/rok-combat-guide-en.html · https://www.appamped.com/rise-of-civilizations-how-to-send-two-commanders-in-battle-at-the-same-time/ · https://riseofkingdoms.fandom.com/wiki/War · https://riseofkingdoms.fandom.com/wiki/Rally
- **§5 Lords**: https://riseofkingdoms.fandom.com/wiki/Commander_Guide · https://riseofkingdomsguides.com/talent-tree/ · https://riseofkingdoms.fandom.com/wiki/Items/Starlight_Sculpture · https://riseofkingdoms.fandom.com/wiki/Buildings/Blacksmith · https://riseofkingdoms.fandom.com/wiki/Buildings/Tavern · https://riseofkingdoms.fandom.com/wiki/Events/Wheel_of_Fortune · https://www.rok.guide/the-mightiest-governor-event/ · https://riseofkingdoms.fandom.com/wiki/Expedition · https://lootbar.gg/blog/en/rise-of-kingdoms-new-update-is-here-huge-changes-to-talents-and-more.html
- **§6 World**: https://www.f2p.org/free-to-play/strategy/rise-of-kingdoms-battle-for-dominance-across-a-single-seamless-world-map/ · https://www.rok.guide/map/ · https://riseofkingdoms.fandom.com/wiki/Holy_Sites · https://riseofkingdoms.fandom.com/wiki/Scouting · https://riseofkingdoms.fandom.com/wiki/Barbarians · https://riseofkingdoms.fandom.com/wiki/Territory · https://riseofkingdomsguides.com/how-to-teleport-in-rise-of-kingdoms/ · https://www.rok.guide/kingdom-title-buffs/
- **§7 Alliance**: https://riseofkingdoms.fandom.com/wiki/Alliance_Gift · https://riseofkingdomsguides.com/how-to-get-alliance-and-individual-credits-in-rise-of-kingdoms/ · (help: the §1 Alliance Center and alliance-guide pages)
- **§8 Seasons**: https://riseofkingdoms.fandom.com/wiki/Lost_Kingdom · https://www.rok.guide/season-of-conquest/ · https://www.pocketgamer.com/rise-of-kingdoms/passport-migration/ · https://www.rok.guide/ark-of-osiris/ · https://www.rok.guide/sunset-canyon-tips/ · https://riseofkingdomsguides.com/champions-of-olympia-guide-in-rok/ · https://riseofkingdoms.fandom.com/wiki/Events/Rise_of_Kingdoms
- **§9 Monetization**: https://riseofkingdoms.fandom.com/wiki/VIP · https://www.rok.guide/lucerne-scrolls/ · https://touchscreengaming.com/rise-of-kingdoms-city-hall-transmog-guide/ · https://www.blog.udonis.co/mobile-marketing/mobile-games/rise-of-kingdoms-monetization · https://www.gamerefinery.com/rise-of-kingdoms-a-player-perspective-on-monetization/ · https://mmohuts.com/news/rise-kingdoms-review · https://riseofkingdomsguides.com/is-rise-of-kingdoms-pay-to-win-game-pay-to-win-vs-free-to-play/ · https://eternal-kingdom.net/why-players-quit-rise-of-kingdoms (a competitor's site; likely biased)
- **§10–§12 Onboarding, UX, art**: https://riseofkingdoms.fandom.com/wiki/Civilizations · the snapshot, §6 zoom (f2p.org) and review (mmohuts) pages above. The museum-sketch and "simple" statements were not pinned to one URL in the research notes; most §11–§12 facts are [observational].
