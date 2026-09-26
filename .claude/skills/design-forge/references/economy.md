# Economy — five stock resources, two bound currencies, one measuring hour

Where resources come from, where they go, what can be taken, and what stops the economy from
inflating or being farmed. Implementation: **gameplay-forge** (rules, data, save), **cloud-forge**
(server state, caravans, account links, cost), **world-forge** (nodes, seams, veins, territory),
**shop-forge** (goods, gem rate `k`), **ui-forge** (resource bar, warehouse card), **qa-forge**
(harness). Genre patterns: [benchmark.md](benchmark.md) §3. **Every number here is a PROPOSAL**
unless it quotes a canonical fact; check shipped data first (`data/buildings.gd`, `data/troops.gd`,
`data/items.gd` — paths to confirm). A dial that is a sacred balance constant keeps its shipped
value and this file's value goes to the owner (§16). `S1–S6` = keep stage ([progression.md](progression.md)).

## 0. The four questions

- **Want**: the next upgrade's cost in hand; later the t6+ troops and Masterwork gear that iron buys.
- **Obstacle**: income per hour (city + map), exposure of saved surplus above the warehouse, iron from t6.
- **Wait**: week 1 — any upgrade costs ≤ 4 h of income (affordable after one gap); month 1 ≤ 12 h; endgame — a spine upgrade costs 2–5 days of income, saved under a pledge (§7).
- **Witness**: plunder in reports and the alliance feed; territory on the map; prestige works on the keep (§3 layer 6).

## 1. Resources and the measuring hour

| Resource | In the realm | Opens | Weight (value units per unit = cart load) | Plunder | Caravan (§9) | Market (NPC, §10) |
|---|---|---|---|---|---|---|
| food | bread and fodder | S1 | 1 | above allowance | yes | 2 : 1 |
| wood | timber, shafts, bows | S1 | 1 | above allowance | yes | 2 : 1 |
| stone | masonry, wall repair, siege shot | S2 | 1.5 | above allowance | yes | 2 : 1 |
| iron | arms, armour, fittings | S2 (mine); throttle from t6 (§4) | 2 | above allowance | sender S4+ | buy 4 : 1 (≤ 2 H/day), sell 2 : 1 |
| gold | coin: wages, research, lords, fees | S1 | 4 | above allowance | yes | 2 : 1 |
| gems | premium, bound to the account | — | — | never | never | — |
| rp | research ink, bound to the account | S1 | — | never | never | never |

Weight = value: 1 vu = 1 food; a cart carries the same value whatever it holds, so gathering and
plunder balance on one number. Market ratios are in value (2 vu in → 1 vu out). Gold is **not
gathered** on the map (its home is people: taxes, trade, plunder) — each resource has one home channel.

**Two hours** (one definition each, used everywhere):
- `P(r)` = the player's own city output of `r` per hour, before upkeep. Sizes **goods** (paid,
  [monetization.md](monetization.md) §2), **donations** (15 min, [alliance.md](alliance.md) §4) and **sheds** (15 h).
- `H(r) = max(P(r), ½ · I_med(S, r))`, where `I_med(S, r)` = the stage-median total hourly income of
  `r` for a free player (tuning table from §12, then telemetry). Sizes **rewards** (chests, events),
  the **warehouse allowance**, **transfer**, **market** and **plunder caps**. **Camps** pay in the
  `I_med` of the stage their level serves ([world.md](world.md) ladder), never the attacker's H —
  a strong castle farming low camps earns low loot.

Why two: iron and gold come mostly from outside the city, so `P(iron)` is ~20% of iron income late.
Earned iron is measured generously (`H`), bought iron strictly (`P`) — so the shop can never buy
past the throttle (§4). Every H-reward is converted to units **at delivery**, never later: holding
an unopened reward must never grow its value.

## 2. Sources and sinks (free player, model §12, days 61–90)

| Res | City | Map | Camps | Chests | Sinks (share of this resource's spend) | Day-30 / window 61–90 |
|---|---|---|---|---|---|---|
| food | 51% farms, mill | 29% fields | 6% | 13% | training 74 · upkeep 17 · healing 9 | 0.93 / 0.97 |
| wood | 47% lumber, sawmill | 35% woods | 5% | 12% | construction 71 · training 26 · donations 3 | 0.99 / 0.99 |
| stone | 33% quarry, stonemason | 54% outcrops | 6% | 7% | construction 93 · donations, wall repair 7 | 0.96 / 1.01 |
| iron | 20% mine | 54% seams | 20% | 6% | t4+ training 66 · arms and gear 21 · S5+ fittings 14 | 0.94 / **1.13 named** |
| gold | 63% houses, market | 0% | 27% | 10% | research 55 · lords 26 · t4+ wages 11 · fees 9 | 1.03 / 1.04 |
| gems | — | veins | — | events, milestones | hourglass finishes, goods, cosmetics | 0.92 / 1.17 |
| rp | 100% library, academy, university | — | — | — | research 100 | 0.93 by design (the timer binds first) |

All five in value: city 58% / map 21% / camps 9% / chests 12% in days 1–30 → 44 / 36 / 10 / 10 in
days 61–90. Archetype roles are PROPOSALS (verify which archetype yields what in `data/buildings.gd`).

## 3. Layered sinks

| Layer | Sinks | Free share (vu, 61–90) | Grows with | Its job | Valve |
|---|---|---|---|---|---|
| 1 Growth | construction, research | 46% | levels (`C(L) = C1·r^(L−1)`, [numbers.md](numbers.md) §2) | the spine of progress | cost ratio `r` |
| 2 Army | training, healing, upkeep, arms and gear | 49% | army size × tier, fights | ties war to the economy | upkeep `D(t)`, heal share |
| 3 Lords | lord levels and skills (gold) | 3% | lords ([lords.md](lords.md)) | investment in people | lord costs |
| 4 Social | alliance donations, rally provisions | 3% with layer 5 (one model line) | alliance | collective goods from small acts | donation Merit |
| 5 Friction | market spread, caravan tax, plunder spoil, moving the seat | (in layer 4's 3%) | trade and raid volume | anti-inflation, anti-farm | tax % |
| 6 Prestige | works on the monument, wonder, palace: stat-free tiers, realm titles, feasts | 0% free; open-ended | surplus | absorbs the top without power | — |

1. From its opening stage, every resource has ≥ 2 sink layers (stone: construction + wall repair and siege shot, [combat.md](combat.md) §10, siege-forge).
2. Layer 6 never grants a stat (money-law; [monetization.md](monetization.md) cosmetics).
3. When layer 1 ends (max levels), layers 2 + 6 must absorb ≥ 90% of income, or the account HOARDs.

**Checks**: [ ] sink table per stage in SYSTEM.md §5 — fails when: a resource has one sink layer
(it dies when that layer ends) · [ ] telemetry held ÷ daily income — fails when: max-level median > 4 days.

## 4. Iron — the t6+ throttle

**Why iron, not gold** (the genre's late wall; its top tier heals for ~20× the gold of the tier
below [one guide; unverified], and players avoid fighting): (1) iron is a **map** resource, so a
late throttle pushes players onto contested land — a gold wall rewards staying home; (2) iron
gates **growth, not fighting**: heal cost is ≤ 10% iron; (3) it exists already in the game and the
fiction; (4) money cannot lift it (goods sized in `P`, §1).

Troop cost mix — share of one unit's value (same total value per tier across lines, [combat.md](combat.md) rule 1):

| Band | food | wood | iron | gold | Line signature at t6–t8 (food/wood/iron/gold) |
|---|---|---|---|---|---|
| t1–t3 | 55 | 45 | 0 | 0 | infantry 35/15/40/10 · spearmen 35/30/25/10 |
| t4–t5 | 45 | 30 | 20 | 5 | archers 35/35/20/10 · crossbows 30/20/40/10 |
| t6–t8 | 35 | 20 | 35 | 10 | cavalry 45/10/35/10 (fodder, barding, shoes) |
| t9–t10 (cavalry t11) | 30 | 15 | 40 | 15 | siege engines: wood 50 / stone 20 / iron 20 / gold 10 (siege-forge) |
| heal, any tier: 30% of training value | 60 | 10 | ≤ 10 | 20 | within combat.md H6 (≤ 40%) |

Heal bound ([combat.md](combat.md) H4, beds 1.25 × the largest march): 30% × 1.25 × X ≤ 24 h of own
output → **training one full march of stage S costs ≤ 64 h of the median free player's output**.
An iron-poor player leans on spearmen and archers: the throttle is a choice, not a wall. Lord gear
draws on the same iron ([lords.md](lords.md) rule 3): **craft Issued 0.25 d · temper Sound 0.5 d ·
Fine 1.25 d · Masterwork 3 d** of `I_med(S, iron)` → a four-piece Masterwork set ≈ 20 days of iron.

Supply rules: mine ≤ 30% of a free t6+ player's iron demand (model 20%); seams (rings with node
level ≥ 3) ≥ 50% (54%); camps ≥ level 5 drop iron (20%); market buy ≤ 2 H/day; goods in `P`;
caravans only from S4 senders; donations in iron = 15 min of own mine output.

Model result (§12, window 61–90): daily iron demand passes supply on **day 48**; free 1.13, light
1.31, heavy 1.55, no-map 2.45. Heavy wants 1.8× the free pace and reaches 1.8 / 1.55 = 1.16 against
the free 1 / 1.13 = 0.88 → **money buys ≤ 1.31× the free t6+ pace**, not 1.8×.

Verify before proposing: [ ] `data/troops.gd` iron share per tier by the §1 weights (t1–t3 = 0,
t6+ ≥ 30%) · [ ] which archetype makes iron (mine?) and its share of t6+ demand · [ ] heal iron ≤ 10% ·
[ ] iron's first cost at S2 (the "new resource" beat, numbers.md §2) and its bar icon shown only
from then · [ ] troop costs sacred? → this section is an owner proposal.

**Checks**: [ ] econ_sim free iron day-30 ≤ 1.00 (model 0.94) — fails when: iron blocks t4–t5 for a
player who gathers · [ ] CSV window 61–90 in 1.05–1.20 — fails when: no throttle, or a hard wall ·
[ ] heavy window ≥ 1.35 (model 1.55) — fails when: money lifts the throttle (heavy/free pace > 1.5).

## 5. City production vs map gathering

1. **City = the floor**: safe, offline, no decision after the build. ≥ 40% of total income at every stage, so a castle in a hostile zone still grows: the no-map player keeps 76% / 68% / 48% / 42% of the intended pace on food / wood / stone / iron (model day 90, 1 / ratio).
2. **Map = the variable**: needs banners, choices and exposure. Target share of income: ~20% in month 1 → 35–40% late (model 21% → 36%).
3. **Yield rule**: an 8 h march on a node of the player's own stage returns 15–20% of the player's daily city output (vu). Rate `ρ · 1.2^(N−1)` per node level N (1–6); a march gathers at `min(N, S + 1)`. Node capacity = 1.5 × one 8 h load, so two marches share a node.
4. **Load**: a full march of stage S carries ≥ 10 h of rate at N = S (loads per line: combat.md §3; engine wagons 4.0×), so "until I'm back" ([core-loop.md](core-loop.md) A3) is never cut by load.
5. **Function of time**: `gathered(t) = min(load, rate · (t − arrive))`, settled when the march leaves, is attacked or is resent — 0 ticks. Nodes are seeded `hash(realm, day, chunk)` → 0 spawn writes.
6. **A decision, not busywork**: the node card shows yield per hour, travel time and danger (hostile marches within 10 tiles in the last hour) in one read; richer nodes lie farther and in contested rings. Resend all = 1 tap (A2).
7. **Gathering bonuses add inside one category** (numbers.md §9): research ≤ +60%, lord ≤ +30%, territory +20%, gathering writ +20% for 8 h ([alliance.md](alliance.md) Quartermaster) → cap +130%.

**Checks**: [ ] model channel shares per stage — fails when: map < 25% of late income (territory is
decoration) or > 50% (the city stops mattering) · [ ] core-loop loop sim — fails when: median banner
idle > 25% of waking hours · [ ] unit test load ≥ 10 h of rate per stage — fails when: a load ends
an "until I'm back" batch early.

## 6. Territory value

| Effect | PROPOSAL | Note |
|---|---|---|
| Gathering inside own alliance territory | +20% rate | genre +25% [benchmark.md §3]; our map already carries 36% of late income |
| Ring richness | outer N 1–3, middle 3–5, inner 5–6 | seams and veins only at N ≥ 3 ([world.md](world.md) draws the rings) |
| Held landmarks ([world.md](world.md) ladder) | +3% to +8% city output of ONE resource to members, by landmark tier | Treasury rates: [alliance.md](alliance.md) §4 |
| Cap | territory ≤ +25% of a member's total income; ≤ +35% with inner-ring nodes | worth a fight, never decisive |
| Design test | a median territorial alliance member earns +10–20% over an unaligned player | 36% map × 20% + landmarks ≈ +12% |

## 7. Protection — allowance, sheds, pledge, plunder

**Warehouse allowance** `Wp(r) = h_w · H(r)`:

| Warehouse tier | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `h_w` (hours of H) | 12 | 14 | 16 | 18 | 21 | 24 |

1. **Sheds** hold 15 h of `P` per building ([core-loop.md](core-loop.md) 15-hour promise) and are never plundered; collect-on-open moves them to the yard.
2. **Yard** stock `Y(r)` above the allowance is plunderable: `L(r) = max(0, Y(r) − max(0, Wp(r) − I(r)))`.
3. **Items — the genre loophole closed.** New content creates **no holdable resource item**: chests, events, camps and goods ([monetization.md](monetization.md) §2) land in the yard at delivery (core-loop §7's "protected storage" = the allowance). If shipped resource items exist (`data/items.gd`), their unopened value `I(r)` uses the allowance first, and any value above `Wp` opens into the yard after a 7-day notice. Total untouchable per resource = `Wp` + one pledge — never more.
4. **Pledge — an honest way to save** (the item loophole was the genre's only one). On a building card, "Save for this" (2 taps) moves stock into a pledge: one pledge at a time; ≤ the remaining cost of one startable upgrade; only once ≥ 50% of that cost is held; ≤ 72 h; consumed when the upgrade starts; after cancel or expiry, 24 h before the next. Pledged stock is not plunderable and not spendable elsewhere.
5. **Plunder** on a won castle assault: takes `50% · L(r)` per resource, up to the survivors' load; the attacker receives **75%**, **25% is destroyed** (spoiled in the sack — a sink and a tax on raid-feeding).
6. **Sacked**: only the first 2 won assaults on one castle in 12 h plunder; then 8 h with plunder 0. A breach adds no plunder ([combat.md](combat.md) §10 rule 5). Worst 12 h: −75% of `L`, 0% of the allowance.
7. **Attacker cap**: plunder received ≤ 24 H(r) of the attacker per resource per day; above it the carts come home empty and the defender loses nothing.
8. **Plunder 0** from: peace ward and newcomer ward ([onboarding.md](onboarding.md)), accounts linked to the attacker (§9 F8), same alliance or left it < 7 d, 14-day caravan partners. A defeated gathering march loses 50% of its cart by the same split. Gems and rp: never. Wounded in beds: never.
9. **Honesty**: the scout report shows `L` ±20% (combat.md scout tier 2); the warehouse card shows "Safe: 210,000 · At risk: 290,000"; a goods offer shows how much of it will sit above the allowance.

Worked (S5, `H(food)` = 10,000/h, warehouse tier 5 → `Wp` = 210,000; yard 500,000, no items):
`L` = 290,000 → plunder 1 takes 145,000 (attacker +108,750, 36,250 destroyed) → plunder 2 takes
72,500 → sacked 8 h. Loss 217,500 (43% of the yard). With a 250,000 pledge for the keep upgrade:
`L` = 40,000 → loss 20,000 + 10,000 = 30,000 (6%).

| Fails when | Caught by |
|---|---|
| Opening items lifts untouchable stock above `Wp` + pledge ([benchmark.md](benchmark.md) check) | [ ] plunder unit test, items case |
| One castle loses > 75% of `L` in 12 h, or anything under `Wp` | [ ] plunder unit test, 3-assault case |
| A pledge outlives 72 h, exceeds one upgrade, or chains with no 24 h gap | [ ] pledge unit test |

## 8. Upkeep — light rations, no deaths (the decision)

| Option | For | Against | Model (free food, d30 / d90) |
|---|---|---|---|
| None (genre: apparently none [unverified]) | simplest | food HOARDs late; idle troop stacks cost nothing → power inflation | 0.77 / 0.80 HOARD |
| Heavy (older browser 4X: starving troops die) | strong sink | deaths while away break the 15-hour promise | — |
| **Light rations, no deaths (recommended)** | the only sink that scales with army SIZE; lost troops stop eating; food keeps a job to the end | one more line on the resource bar | 0.93 / 0.96 |

Why not just cut farm output 17%: that taxes every castle alike; rations tax standing armies.
1. A unit eats its own food training cost in `D(t) = 150 + 15·(t − 1)` days (t1 150 d, t10 285 d, cavalry t11 300 d). With food cost ∝ power, upkeep per power at t10 = 150/285 = 53% of t1: quality over mass.
2. Target: median free army's upkeep = 10–20% of food income (model 15–16%); max army ≤ 35%. Outside the band, move `D`.
3. Wounded in beds, routed troops and engines eat 0; reinforcements at an ally are fed by their owner.
4. Closed form, 0 ticks: net `n = P(food) − U`. `n ≥ 0`: `shed(t) = min(15·P, s0 + n·Δt)`. `n < 0`: shed 0, `Y(t) = max(0, Y0 + n·Δt)`.
5. **Short rations** at food 0: training and healing that need food wait; no desertion, no stat loss. The bar reads "+12,400/h after rations 2,100/h" — two numbers, never a hidden drain.

## 9. Farm accounts — countermeasures

| # | Measure | PROPOSAL | Stops |
|---|---|---|---|
| F1 | Caravans only between members of one alliance, both ≥ 7 d in it | 7 d | cross-alliance feeding, join-drain-leave |
| F2 | Caravan tax (a sink) | 20%; 15% with Market Rights ([alliance.md](alliance.md) §5) | cheap funnels |
| F3 | Receive cap per resource per day, all senders together | ≤ 8 H(r) of the RECEIVER | all alts together add ≤ +33% of a main's own city output |
| F4 | Send cap by keep stage | S1–S2: none · S3: ≤ 12 H of own, no iron · S4+: ≤ 12 H incl. iron | fresh alts send nothing; an alt sends ≤ half a day of its own output |
| F5 | Sender account age | ≥ 7 d | throwaway alts |
| F6 | Travel | 30–90 min by distance; the server may hold and reverse | instant funnels |
| F7 | Never transferable | gems, rp, hourglasses, Resolve, lord items | bound value |
| F8 | Device link: same install id or device-fingerprint hash within 30 d | caravans blocked, plunder 0, help pays 0 ([alliance.md](alliance.md)), one vein cap per device | several accounts on one phone |
| F9 | Shared network: same public IP with overlapping sessions ≥ 3 days in 7 | flag + F3/F4 caps halved; never a ban on IP alone | families, schools, carrier NAT stay safe |
| F10 | Flow audit, nightly over caravan + plunder ledgers | flag a pair when one sender's outflow to one receiver > 50% of its income for 14 d and the sender built nothing | caps 0 for 14 d + human review |
| F11 | Moving realms ([onboarding.md](onboarding.md) passage, [liveops.md](liveops.md) migration) | passage: ≤ `Wp`; voluntary migration: ≤ 72 H per resource; realm merges: in full | the feeder guard |

Device ids stored only as salted hashes, kept 90 days (cloud-forge; privacy law). Chest rewards are
bound ([core-loop.md](core-loop.md) §7); new or S1–S2 accounts add 0 Treasury ([alliance.md](alliance.md) §4).

| Fails when | Caught by |
|---|---|
| A young account moves more than its stage allows | [ ] caravan server test by stage (benchmark.md check) |
| Linked accounts plunder each other for > 0 | [ ] plunder unit test, linked case |
| > 2% of active accounts flagged by F10 in a week (heuristic too loose) or 0 flags (too tight) | [ ] cloud-forge weekly flag report |

## 10. Inflation control

1. **Rewards in H, fixed at delivery**; goods in `P` under the weekly allowance `Ag` ([monetization.md](monetization.md) §4). No fixed-amount resource reward in new data ([ ] data check).
2. **Friction sinks**: NPC market (the market archetype) 2 : 1 in value, ≤ 12 H received per day, iron buy 4 : 1 ≤ 2 H; caravan tax 20%; plunder spoil 25%.
3. **Exposure**: surplus above `Wp` + pledge is plunderable — hoarding has a price.
4. **Prestige works** (layer 6) take unlimited surplus for stat-free tiers and titles.
5. **Event budget**: resources injected by events per realm-week ≤ 15% of the realm's production ([liveops.md](liveops.md) sets event rewards in H).
6. **Watch**: median held stock ≤ 2 days of income at day 30 (free); alert at > 4 days → add a sink or cut a source (numbers.md §6).

## 11. Gems for free players — gem veins

Pattern: free players reach premium currency through map play. Our move: a daily cap that makes
bots and farms pointless, and gems that are never loot. Gem numbers at `k` = 1 (the gem price of a
1-minute hourglass, core-loop §5); shop-forge sets `k`, scale every gem number by it.

| Source (free) | Gems | Rule |
|---|---|---|
| Gem veins | ≤ 90/day per player (model 60 average) | a vein holds 180, gathers 30/h flat — no research, lord or territory bonus: presence is the only lever |
| Milestones (one-time) | 150/day falling 3% per day → ≈ 3,000 in 30 d, ≈ 4,700 in 90 d | keep stages, first clear of each camp level, first banner, lord milestones |
| Events and milestone chests ([liveops.md](liveops.md)) | ≈ 25/day average | milestone rewards, never rank-only |
| Daily and weekly chests | 0 | core-loop §7 pays time and goods, not gems |

1. Veins sit only at N ≥ 3; supply per realm per day = `0.35 × eligible players` veins (70% of the cap demand), so veins are contested.
2. Eligible: S2+, account ≥ 72 h, one vein cap per device per day (F8), one vein march at a time, no standing order (2 deliberate taps) — a bot earns ≤ 90 per day.
3. A march beaten on a vein keeps its gems and goes home; the vein passes to the winner.
4. Steady free income after month 2 ≈ 85–110 gems/day = the price of 2.3–3.1 h of hourglass (`m = (G/k)^(1/0.9)`) — about +25% on the ≈ 10 h/day of hourglasses the chests give.

## 12. The worked model — `tools/econ_sim.py`

```
python tools/econ_sim.py design/economy/econ.json --days 1,7,30,60,90 --csv design/economy/econ.csv
```
Scale: day-1 free city output ≈ 100,000 vu/day (40,000 food, 34,000 wood, 9,000 stone, 600 iron,
3,500 gold); set the bases from shipped data and keep the ratios. Player fields used by `scale`:
`gather` (0 = never marches), `pace` (a spender builds faster), `upkeep` (0 = the variant without
rations), `gemspend`, `pack_mult` (heavy 6 ≈ 160 h of own output per week ≤ `Ag` 168 h). econ_sim
has no start day per line: a late resource starts small and grows fast (iron). Window ratio =
`(sinks90 − sinks60) / (sources90 − sources60)` from the CSV.

```json
{
  "resources": ["food", "wood", "stone", "iron", "gold", "gems", "rp"],
  "players": {
    "free": {"pack_mult": 0, "gather": 1.0, "pace": 1.0, "upkeep": 1, "gemspend": 1},
    "free_no_map": {"pack_mult": 0, "gather": 0.0, "pace": 1.0, "upkeep": 1, "gemspend": 1},
    "free_no_upkeep": {"pack_mult": 0, "gather": 1.0, "pace": 1.0, "upkeep": 0, "gemspend": 1},
    "light": {"pack_mult": 1, "gather": 1.0, "pace": 1.2, "upkeep": 1, "gemspend": 3.5},
    "heavy": {"pack_mult": 6, "gather": 1.2, "pace": 1.8, "upkeep": 1, "gemspend": 15}
  },
  "sources": [
    {"name": "farms+mill", "res": "food", "base": 40000, "growth": 0.032},
    {"name": "gathering fields", "res": "food", "base": 8000, "growth": 0.046, "scale": "gather"},
    {"name": "camps", "res": "food", "base": 4000, "growth": 0.035},
    {"name": "chests", "res": "food", "base": 8100, "growth": 0.035},
    {"name": "packs", "res": "food", "base": 4500, "growth": 0.035, "scale": "pack_mult"},
    {"name": "lumber+sawmill", "res": "wood", "base": 34000, "growth": 0.032},
    {"name": "gathering woods", "res": "wood", "base": 9000, "growth": 0.046, "scale": "gather"},
    {"name": "camps", "res": "wood", "base": 3000, "growth": 0.035},
    {"name": "chests", "res": "wood", "base": 6900, "growth": 0.035},
    {"name": "packs", "res": "wood", "base": 5500, "growth": 0.035, "scale": "pack_mult"},
    {"name": "quarry+mason", "res": "stone", "base": 9000, "growth": 0.036},
    {"name": "gathering outcrops", "res": "stone", "base": 7000, "growth": 0.046, "scale": "gather"},
    {"name": "camps", "res": "stone", "base": 1200, "growth": 0.04},
    {"name": "chests", "res": "stone", "base": 1450, "growth": 0.04},
    {"name": "packs", "res": "stone", "base": 1750, "growth": 0.04, "scale": "pack_mult"},
    {"name": "mine", "res": "iron", "base": 600, "growth": 0.055},
    {"name": "gathering seams", "res": "iron", "base": 1100, "growth": 0.06, "scale": "gather"},
    {"name": "camps", "res": "iron", "base": 400, "growth": 0.06},
    {"name": "chests", "res": "iron", "base": 180, "growth": 0.055},
    {"name": "packs", "res": "iron", "base": 100, "growth": 0.055, "scale": "pack_mult"},
    {"name": "houses+market", "res": "gold", "base": 3500, "growth": 0.035},
    {"name": "camps", "res": "gold", "base": 1500, "growth": 0.035},
    {"name": "chests", "res": "gold", "base": 560, "growth": 0.035},
    {"name": "packs", "res": "gold", "base": 800, "growth": 0.035, "scale": "pack_mult"},
    {"name": "gem veins", "res": "gems", "base": 60, "scale": "gather"},
    {"name": "milestones", "res": "gems", "base": 150, "growth": -0.03},
    {"name": "events", "res": "gems", "base": 25},
    {"name": "packs", "res": "gems", "base": 400, "scale": "pack_mult"},
    {"name": "library+academy", "res": "rp", "base": 2800, "growth": 0.035},
    {"name": "packs", "res": "rp", "base": 400, "growth": 0.035, "scale": "pack_mult"}
  ],
  "sinks": [
    {"name": "training", "res": "food", "base": 40000, "growth": 0.0365, "scale": "pace"},
    {"name": "healing", "res": "food", "base": 5000, "growth": 0.0365, "scale": "pace"},
    {"name": "upkeep", "res": "food", "base": 9000, "growth": 0.0365, "scale": "upkeep"},
    {"name": "construction", "res": "wood", "base": 33500, "growth": 0.0375, "scale": "pace"},
    {"name": "training", "res": "wood", "base": 16000, "growth": 0.034, "scale": "pace"},
    {"name": "fees+donations", "res": "wood", "base": 2000, "growth": 0.035},
    {"name": "construction", "res": "stone", "base": 15800, "growth": 0.0425, "scale": "pace"},
    {"name": "fees+donations", "res": "stone", "base": 1500, "growth": 0.04},
    {"name": "training t4+", "res": "iron", "base": 900, "growth": 0.067, "scale": "pace"},
    {"name": "arms+equipment", "res": "iron", "base": 1000, "growth": 0.05, "scale": "pace"},
    {"name": "construction s5+", "res": "iron", "base": 200, "growth": 0.066, "scale": "pace"},
    {"name": "research", "res": "gold", "base": 3400, "growth": 0.034, "scale": "pace"},
    {"name": "lords", "res": "gold", "base": 1500, "growth": 0.035, "scale": "pace"},
    {"name": "training t4+", "res": "gold", "base": 300, "growth": 0.045, "scale": "pace"},
    {"name": "fees+donations", "res": "gold", "base": 500, "growth": 0.035},
    {"name": "hourglass finishes", "res": "gems", "base": 185, "growth": -0.006, "scale": "gemspend"},
    {"name": "research", "res": "rp", "base": 2600, "growth": 0.035, "scale": "pace"}
  ]
}
```
Real output (2026-09-26), the free player at day 30 and 90, and the verdict line:
```
== free
  day  res             sources          sinks        balance   ratio
   30  food            3086930        2857455         229476    0.93  ok
   30  wood            2740528        2718022          22506    0.99  ok
   30  stone           1055307        1008199          47108    0.96  ok
   30  iron             175087         164586          10501    0.94  ok
   30  gold             287022         294204          -7182    1.03  ok
   30  gems               5545           5093            452    0.92  ok
   30  rp               144543         134219          10325    0.93  ok
   90  iron            6453143        7134533        -681390    1.11  WALL
RED-TEAM #6: free player at day 30 within 0.90-1.10 on every resource with a sink
```
Same run, other players (day-30 ratio / window 61–90): **free_no_map** food 1.10/1.37, wood
1.25/1.54, stone 1.62/2.20, iron 1.87/2.45, gems 1.36/2.88 · **free_no_upkeep** food 0.77/0.81 ·
**light** iron 1.08/1.31, rest 0.97–1.11 · **heavy** iron 1.26/1.55, rp 0.90/0.90, rest 0.95–1.08.
Read it: every free resource sits in band at day 30; iron's day-90 WALL is the named t6+ throttle
(§4); the map is worth +37% to +145% of pace outside gold (no_map); rations are what keeps food in
band (no_upkeep); money cannot lift iron (heavy).

## 13. Server cost

State per player: per resource `Y0`, `s0` + one shared `t0` (≈ 70 bytes), pledge 16 bytes; rates are
derived from buildings, never stored. Production, rations, sheds, gathering, sacked timers and
pledge expiry are functions of time: **0 server ticks**. Clients compute stock locally: 0 polling reads.

| Write | Per engaged player per day | Note |
|---|---|---|
| Spends, collects, chest resources | 0 extra | ride on the plate start or claim write (core-loop §11) |
| Gathering result | 0 extra | settled inside the next march order |
| Plunder | 0.6 | attacker + defender, ≈ 0.3 won assaults per player per day |
| Caravan | 0.9 | sender + receiver + ledger append, ≈ 0.3 per day |
| Market, pledge | 0.7 | one player-document write each |
| Gem vein | 1.0 | occupy rides on the march order; leave = 1 |
| Device link, flow flags | ≈ 0.1 | only when changed; the nightly audit reads the ledgers |
| **Total** | **≈ 3.3** | 50,000 × 3.3 ≈ 165,000 per day ≈ 5 M per month = 5.7% of core-loop's 87 M |

Budget line: at core-loop's break-even price (€2.30 per million writes uses the whole €200) the
economy's 5 M would cost ≤ €11.50; real store prices must be far lower. Measure with
`core/sd_cost_probe.gd` before tuning; ledgers kept 30 days.

## 14. Harness and metrics

| Proof | Verdict line (PROPOSED wording; qa-forge fixes it) |
|---|---|
| `tools/econ_sim.py` on SYSTEM.md's model | `RED-TEAM #6: free player at day 30 within 0.90-1.10 on every resource with a sink` + iron window 1.05–1.20 |
| econ probe (new, headless; qa-forge; path to confirm): the model's lines recomputed from `data/*.gd` costs and outputs | `ECON PROBE OK - free d30 7/7 in band, iron w61-90 1.13, no-map pace >= 0.40` |
| plunder unit tests (gameplay-forge + cloud-forge) | `PLUNDER OK - ward, linked, sacked, pledge, items, cap: 0 faults` |
| caravan server tests | `CARAVAN OK - caps by stage 6/6, linked 0, tax 20%` |
| `core/sd_cost_probe.gd` | economy writes ≤ 4 per engaged player per day |

**After ship**: median held stock ≤ 2 days of income (free, day 30); ≥ 60% of free S5+ players
gather iron weekly; F10 flags 0.2–2% of actives per week; plunder loss per defender ≤ 10% of daily
income at the median; heal of full beds ≤ 24 h of own production ([combat.md](combat.md) H4).

**Save migration** (gameplay-forge): stock and buildings load unchanged; `t0` = load time; sheds
start empty; shipped resource items keep their value under §7 rule 3 with a 7-day notice; no pledge.

## 15. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md) §3) | Our fix | Number |
|---|---|---|
| Resources held as items cannot be plundered, so the storehouse is moot [observational] | no holdable resource items; shipped items use the allowance first; the pledge | untouchable ≤ `Wp` + 1 pledge |
| Farm accounts are standard practice | F1–F11; bound chests; linked accounts plunder 0 | alts add ≤ +33% of own city output |
| Gathering is idle busywork | one-read node choice; Resend all; time-first batches | 1 tap for all banners |
| Top-tier heal costs → fight avoidance | heal 30% of training, ≤ 10% iron; throttle on growth | full beds ≤ 24 h of own output |
| Gold barely matters early, then walls the top | every resource has a job from its opening stage; the late throttle is on the map | iron window 1.13 |
| Zeroed players quit | 50% per plunder, sacked after 2, sheds never plundered | worst 12 h: −75% of `L`, 0 of `Wp` |
| Money wins persistent war | goods in `P`; iron goods ≤ mine output | heavy t6+ pace ≤ 1.31× free |

## 16. Owner decisions required

1. Iron as the t6+ throttle and the cost mix of §4 (troop costs may be sacred constants).
2. Light rations (§8) — a new standing rule players will feel.
3. The pledge (§7 rule 4) and the plunder split 50% / 75% / 25%.
4. Device-link blocks and salted hash storage (privacy; cloud-forge).
5. Gem veins: cap 90/day, supply 0.35 per eligible player, and the free gem target; MON-001 (owner ledger) wins if it differs.
6. Gold not gathered on the map; market spreads and the iron buy cap.
7. Migration carry cap 72 H per resource (liveops.md / onboarding.md feeder guard).
8. In-world names (story-forge): yard, sheds, pledge, rations, caravans, gem veins, iron seams, prestige works.
