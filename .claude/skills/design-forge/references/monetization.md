# Monetization — the money-law, the allowance, the chronicle

How Castle Conquest earns money without selling power. Implementation: **shop-forge** (catalogue, prices,
offers, billing, shop police tests), **ui-forge** (screens), **cloud-forge** (receipts, allowance on the server),
**qa-forge** (harness), **game-art-director** / **blender-forge** (art), **story-forge** (names), **l10n-forge**
(money strings). Genre patterns: [benchmark.md](benchmark.md).

**Every number here is a PROPOSAL** unless it quotes a canonical fact; prices and spend are owner decisions
(SKILL.md rule 2). Owner-ledger facts this folder cannot see — verify before citing: the published gem rate,
MON-001 (free-viable gem map), MON-002 (billing blocked), FEAT-003 (the Fair, `FAIR_STALLS`), PEGI-7, the
refused BND-siege / BND-warlord paintings, `core/offers_test.gd`, `core/iap.gd`, `core/offers.gd` (paths to confirm).

## 0. The four questions (the shop as a system)

- **Want**: less waiting (works), fuller stores (goods), a road travelled (journeys), a look others see.
- **Obstacle**: price; the weekly allowance on power-relevant purchases (§4).
- **Wait**: a purchase is instant; the allowance resets Monday 00:00 UTC (core-loop's reset clock).
- **Witness**: cosmetics on the keep and on the realm map — never a price, a spend total or a spend rank.

Shop-header promise (story-forge words it): **"Coin can buy each workplace one extra shift a week — in a war week, a quarter shift. All other strength is earned."**

## 1. The laws this file rests on

| # | Law | Source | Proof |
|---|---|---|---|
| L1 | No war imagery over a buy button; paid surfaces sell goods, works and journeys | money-law (canonical; game-art-director environments.md) | art tags §10 |
| L2 | Gems buy time and goods, never power; equipment is structurally unsellable | shop-forge (verify wording) | grant whitelist |
| L3 | Every bundle states its free route truthfully | shop-forge | `free_route` non-empty |
| L4 | One published gem rate; no fake discounts, no fake scarcity | shop-forge | value-claim unit test |
| L5 | Limited offers withhold nothing and state their return | shop-forge | `return_at` set |
| L6 | PEGI-7 | owner ledger | §9 |
| L7 | Plate count is never sold (crews, desks, yards, beds, banners) | [core-loop.md](core-loop.md) §2 | grant whitelist |
| L8 | Sacred constants stay; spend changes are owner proposals | SKILL.md rule 2 | §13 |

Terms: **Goods** — the five resources and rp, shown as things (sacks, bound logs, dressed blocks, ingots, coin, sealed scrolls; art SHP-*), always sized in **hours of the player's own production**. **Works** — hourglasses (Works / Muster / Universal, core-loop §5) and the direct gem finish `p(m) = k · m^0.9`; never a crew, desk, yard, bed or banner. **Journeys** — travel and trade: a caravan's haul, an in-realm seat move in a Truce week ([world.md](world.md) rules), a pilgrim's return with goods (art JRN-*; to confirm with shop-forge). **Cosmetics** — a look with zero stats: keep dressings / seat skins, banners, march pennants, lord portrait frames, hall decor, chat seals (sticker packs: owner decision, chat-forge). **Bought** — acquired with money or gems, whatever the gems' origin. **War week** — each of the 4 contest weeks of the 35-day campaign, plus a realm's Founding week; the Truce week is a peace week ([liveops.md](liveops.md) §2, §3.1). **War window** — core-loop §8.3.

## 2. What may be sold

| Line | Examples | Against the allowance (§4) | In a war week | Free route (L3) |
|---|---|---|---|---|
| Goods | crates of 1–24 h own output; rp scrolls | yes, own-output hours | allowance × 0.25 | sheds, gathering, camps, chests |
| Production boosts | +50% mill output for 24 h | yes, at expected yield (= 12 h of that resource) | as goods | research, events |
| Works | hourglasses 1 m–24 h; gem finish | yes, when USED | cap × 0.25; muster + infirmary ≤ 480 min per window (core-loop §5 rule 6) | daily chests, weekly writ, alliance Merit store |
| Journeys | caravan haul; in-realm seat move | haul as goods; move: no | move not sold | own caravans ([economy.md](economy.md)); seat-move writs from the season track ([world.md](world.md) §9); Hall summons (alliance.md §4) |
| Cosmetics | dressings, banners, pennants, frames | no | sold | plain versions on the chronicle free track |
| Illuminated chronicle | §7 | its goods and works: yes | sold | the free track |
| Month's purse | gems each day for 30 days | when converted | sold | gems are also earned (MON-001) |
| Gems | 6 packs at the published rate | when converted | sold | gem veins, one-time milestones, event milestones (economy.md §11); the join purse, worth 1 h Universal, if the owner keeps it ([alliance.md](alliance.md) §10, §16) |

Every SKU lists exact contents and quantities (no mystery, no random). Bought goods land in the yard, never
as openable items, with no extra raid protection (economy.md §7). Goods sized in own-output hours scale with
the city, so no offer inflates out of relevance or overpays a small keep.

| Fails when | Caught by |
|---|---|
| A SKU grants a type outside {resource, rp, boost_production, hourglass, gems, cosmetic, caravan, seat_move} | [ ] offers_test grant whitelist |
| A SKU has no free-route line, or a line naming a source that does not exist | [ ] offers_test: every route maps to a live source id |
| Goods are sized in fixed amounts, not own-output hours | [ ] data check: goods fields are `hours_own_output` |

## 3. Never sold — the red lines

| # | Never on a paid surface | Why | Caught by |
|---|---|---|---|
| 1 | Plate count, permanent or rented | the genre's most resented sale: a core queue behind a status rung | grant whitelist |
| 2 | A lord; a lord first seen or exclusive on a paid surface; talent points, respecs, random draws. Seals and lord XP: recommended never — if the owner accepts [lords.md](lords.md) §17 #2, only a named lord's Seals or Plain Seals and XP tomes, deterministic (lords.md §10 rule 4), ≤ 35 Seals + 5,040 XP per week | lord power is power (L2); exclusives make a sunk-cost ladder | whitelist; lords.md acquisition table: 0 paid-only rows |
| 3 | Equipment, sets and their crafting materials (whetstones, gold leaf; iron is goods under §4) | structurally unsellable (L2) | whitelist |
| 4 | Troops, troop tiers, combat stats, combat boosts (attack, defence, health, march size) | power | whitelist |
| 5 | Stats on cosmetics, including "set bonuses" on looks | blurs look and power | `skin_contract_test`; cosmetic `stats == {}` |
| 6 | War imagery on a buy screen; a buy button on a war screen | money-law (L1) | art tags; ux_flow_probe (§10) |
| 7 | Wards of any kind ("a ward on sale is a shield on sale", onboarding.md §4; §13 #5); the Writ of Passage or any cross-realm move (liveops.md §7); a seat move in a war week, or while a hostile march is inbound (launch → 30 min after the last arrival; world.md §9, combat.md) | buying out of an attack | cloud-forge rule test |
| 8 | Random items for money or gems: chests, keys, wheels, card flips | gambling law and PEGI-7 (§9) | no `random` grant on any paid SKU |
| 9 | Earned honours: titles, landmark crests, season-victory banners, war honours, alliance rank — and their reserved laurel-and-seal motif | status must mean deeds | art register: motif only on earned (EVR/RNK) rows |
| 10 | Activity points, chronicle levels, level skips, point boosters; favour past the weekly cap (§6) | ONE activity counter (core-loop §7) | whitelist |
| 11 | Information: scouting, fog, enemy positions, battle intel | war advantage | whitelist |
| 12 | The free-finish threshold; Resolve (recommended never, core-loop §12) | earned perks stay earned | whitelist |
| 13 | Spend-scored events, spend rankings, "spend €X, get Y" tiers, chained offers (buy A to unlock B) | spend escalation | liveops event schema has no spend score; no prerequisite SKU field |
| 14 | Purchases gifted to another player | farm feeding and laundering | no recipient field; alliance gifts per [alliance.md](alliance.md) |
| 15 | A sale voiced by the steward or herald helpers (onboarding-forge STW/HRD, verify) | a trusted guide must never sell | dialogue lint: 0 offer ids in helper lines |

## 4. The allowance — the ceiling on bought power (PROPOSAL)

Time is the gate every army and every tower passes: resources become troops and buildings only
through plates. Bounding **bought time** therefore bounds bought power even when goods pile up.

```
per plate: bought time ≤ (R − 1) · 168 h per week  (one extra shift at R 2.0)
Pw = crews + desks (+1 per other timed plate, e.g. the anvil, lords.md §9)
Pm = muster yards + 1 (infirmary)
Aw = (R − 1) · 168 h · Pw     Am = (R − 1) · 168 h · Pm     (sums of the plate caps)
Ag = (R − 1) · 168 h          goods allowance, in hours of own production P (economy.md §1)
R  = 2.0 in the Truce week, 1.25 in war weeks (contest weeks and a realm's Founding week)
```
1. **Use cap**: bought time applied per week (bought hourglasses + gem finishes) ≤ the plate's cap, so
   ≤ `Aw` / `Am` in total; Universal counts on the plate it is used on; war windows keep core-loop's
   ≤ 480 min. Per plate, because a pooled `Am` pours the infirmary's share into five yards (2.2×).
2. **Hold cap**: bought time held ≤ one Truce week's `Aw + Am`; a purchase past it is refused with
   one line. Truce-week stockpiles cannot be dumped into a war week.
3. Earned time is never capped. The picker spends bought time first until the use cap, then earned
   (switchable); change given back keeps its origin. Cosmetics never count.
4. The € value of `Aw + Am + Ag` at the published rate is the weekly power-spend ceiling: shop-forge prints
   it, the owner approves it. [progression.md](progression.md)'s realm charter (§9) and liveops.md's tier
   ceilings (§1.2) bind payers too; the lower limit wins.

| Profile (week 1: core-loop §2 start; mid, late: core-loop §8) | Pw | Pm | Aw / Am / Ag, Truce week | Aw / Am / Ag, war week |
|---|---|---|---|---|
| Week 1 (2 crews, 1 desk, 1 yard) | 3 | 2 | 504 / 336 / 168 h | 126 / 84 / 42 h |
| Mid (2 crews, 1 desk, 3 yards) | 3 | 4 | 504 / 672 / 168 h | 126 / 168 / 42 h |
| Late (3 crews, 2 desks, 5 yards) | 5 | 6 | 840 / 1,008 / 168 h | 210 / 252 / 42 h |

**Worked ratio (late profile, works, equal activity).** Both players keep 5 plates busy (5 × 168 h = 840 plate-hours a week) and take every chest; the earned hourglasses a free player can put on works add ≈ 62 h (daily chests 4 h 15 m × 7 + the writ's 8 h Works and 24 h Universal, core-loop §7) → **902 h** of timer time. Help (−17% at H 18, core-loop §6) cuts every timer of both players by the same share, so it cancels out. Max allowance: 902 + 840 = 1,742 h → **1.93×**; war week: 902 + 210 = 1,112 h → **1.23×**; a 35-day campaign (1 Truce + 4 contest weeks) averages (1 + 4 × 0.25) ÷ 5 = 0.40 shift → **1.37×**. Upper bounds: a free player's vein gems (economy.md §11) count as bought and lower them; per plate the ratio is always < R. Goods keep step: doubled works need about one more week of own output — `Ag` at R 2.0.

| R (Truce week) | Aw late | Max ÷ free | Earned-share floor `E_min` | Read |
|---|---|---|---|---|
| 1.5 | 420 h | 1.47× | 0.68 | fairest; offers carry less |
| **2.0 (recommended)** | 840 h | 1.93× | 0.52 | "one extra shift" — explainable in one line |
| 3.0 | 1,680 h | 2.86× | 0.35 | breaks the ≤ 2.0× cap of §8 |
| **1.25 (war, recommended)** / 1.10 / 1.50 | 210 / 84 / 420 h | 1.23× / 1.09× / 1.47× | 0.81 / 0.91 / 0.68 | 1.25 keeps a war week a contest of play; 1.50 breaks the 1.25× cap |

UI: the shop and the speed-up picker show "Bought time this week: Works 212 h of 840 h · Muster 0 h of 1,008 h — resets Monday (2 d 4 h)"; a plate at its own cap says "This crew: weekly limit reached". At the cap the button stays visible with that line (never hidden); cosmetics stay buyable.

Rejected: **overtime pricing** hides the rule inside prices; **down-weighting bought resources in season scores** — resources are fungible; **a cap in war weeks only** — Truce stockpiles would decide the war (hence the hold cap: one Truce week's stock drains in exactly 4 war weeks at 0.25 a week).

| Fails when | Caught by |
|---|---|
| Max-allowance profile > 2.0× the free profile at equal activity (Truce week) or > 1.25× (war week) | [ ] fair_money_probe (§12) |
| A purchase or use passes the hold, use or war-window cap | [ ] cloud-forge server test, fuzzed |
| The cap is hit and the button disappears or the reason is missing | [ ] ux_flow_probe screenshot at cap |

## 5. The offer ladder

| Rung | Offer | Shown from | Price tier | Contents | Limit | Window and return line |
|---|---|---|---|---|---|---|
| 0 | The Fair (FEAT-003) | always | earned currencies | goods, works | daily stock | — |
| 1 | First purse | shop from session 2; one pop-up after 72 h | €0.99 | 6 h own output + 2 h Universal | once per account | no timer: stays until bought |
| 2 | Illuminated chronicle | each season | €4.99 or gems (owner) | §7 | 1 per season | season; "returns next season" |
| 3 | Month's purse | after 72 h | €4.99 | gems each day × 30; missed days delivered at the next visit | 1 active + 1 queued | none |
| 4 | Milestone crate | a new keep age (progression.md §1); new troop tier | €4.99–€19.99 | goods + works ≤ 25% of the next milestone's cost | 1 per milestone | 7 d; "returns at your next milestone" |
| 5 | Event works | build / research events ([liveops.md](liveops.md)) | €9.99–€19.99 | works + goods in the event's theme | 1 per event | event length; "returns with the next <event>" |
| 6 | Gem packs | always | €0.99 / 4.99 / 9.99 / 19.99 / 29.99 / 49.99 | published rate | — | — |
| 7 | Cosmetic shelf | always; 6–8 items rotate | gems or money | stat-free looks | — | each item states its return (≤ 180 d) |

1. **Pop-ups**: ≤ 1 per day, ≤ 3 per week; none in an account's first 72 h or inside a guided
   step (onboarding.md §1 rule 7); none in a session's first 60 s (the glance, core-loop §8.1); none
   within 30 min after a lost battle, a raid or a wall at zero; none on a war screen; never a push (core-loop A8).
2. **Personalised by progress only** (keep age, lines trained, milestone reached) — never by spend history,
   predicted spend, days since the last purchase or a recent loss. Same goods, same price at the same progress.
3. **Windows ≥ 48 h**; countdowns in days and hours ("2 d 4 h"), never seconds, never pulsing; every
   limited offer carries its return line (L5).
4. **Value claims** come only from the published gem rate, rounded down, reproduced by a unit test. A
   struck-through "was" price only if it was the lowest price of the prior 30 days (§9).
5. Largest single SKU €49.99 (owner). Pack sizes: any gem-priced item can be bought with a leftover ≤ 20%
   of the smallest pack that covers it (§9, currency principles).
6. **Personal budget**: a monthly limit (none / €10 / €25 / €50 / €100 / custom); lowering is immediate,
   raising takes effect after 72 h.

| Fails when | Caught by |
|---|---|
| A pop-up inside 72 h, the first 60 s, 30 min after a defeat, or on a war screen | [ ] ux_flow_probe scripted session with a staged defeat |
| Offer eligibility reads a spend field | [ ] offers_test: eligibility inputs ⊆ progress fields |
| A countdown shows seconds or a window < 48 h | [ ] offers_test on `window_h` and the label format |
| A value claim not reproducible from the published rate | [ ] value-claim unit test |

## 6. Guild patronage — the VIP-like ladder, fed by play (PROPOSAL)

Fiction: the masons', merchants' and scribes' guilds favour the lord who keeps them busy — with work or
with coin. Name: **Guild Patronage**, ranks I–X, points = **Favour** ("charter" is left to progression.md).

1. Favour from play = activity points 1:1 (core-loop §7, ≤ 100 per day) + the alliance Merit store's
   100-Favour item (≤ 2 per week, [alliance.md](alliance.md) §4) — no new point system.
2. Favour from coin = `f_e` per € (owner sets), **capped at 700 per week** = one week of full daily orders:
   a payer who never plays climbs no faster than a daily player; money at most doubles the pace
   (1,400 ÷ 700 per week; 1,600 ÷ 900 = 1.78× with the Merit Favour).
3. Never decays, needs no "activation" item, never expires.
4. Perks: cosmetics, non-war conveniences, a small daily chest. Never stats, plates, the free-finish threshold,
   Resolve, wards, or anything that saves a tap on a war screen (presets are for everyone).
5. The rank shows on the profile card, can be hidden, and never appears in rankings or chat names.
6. The rank X daily chest ≤ the daily 100-point chest (core-loop §7): play always pays more. Chest
   grants carry the `play` tag (§8.2): every rank is reachable by play alone.

| Rank | Favour total | ≈ 5 of 7 days (70/day) | Every day (100/day) | + Merit Favour (900/week) | + Merit + coin cap (1,600/week) | Perk |
|---|---|---|---|---|---|---|
| I | 0 | day 0 | 0 | 0 | 0 | profile seal; daily chest 30 m own output |
| II | 300 | 5 | 3 | 3 | 2 | hall tapestry (cosmetic) |
| III | 1,000 | 15 | 10 | 8 | 5 | guild banner trim (cosmetic) |
| IV | 2,100 | 30 | 21 | 17 | 10 | mail archive × 2.5 |
| V | 3,500 | 50 | 35 | 28 | 16 | daily chest 1 h own output + 15 m Works |
| VI | 5,600 | 80 | 56 | 44 | 25 | keep gate dressing (cosmetic) |
| VII | 8,400 | 120 | 84 | 66 | 37 | second chat seal; profile motto line |
| VIII | 11,900 | 170 | 119 | 93 | 53 | daily chest 2 h own output + 30 m Works |
| IX | 16,100 | 230 | 161 | 126 | 71 | lord portrait frame set (cosmetic) |
| X | 21,000 | 300 | 210 | 164 | 92 | guild-seal title; full dressing set; daily chest 3 h own output + 1 h Universal |

| Fails when | Caught by |
|---|---|
| A perk changes an outcome (stat, plate, timer, Resolve) | [ ] perk whitelist test (same whitelist as §2) |
| Coin favour > 700 or Merit Favour > 200 in a week | [ ] cloud-forge cap test |
| A 5-of-7-days free player needs > 300 d for rank X | [ ] fair_money_probe patronage line |

## 7. The chronicle — a season pass with a full free track (PROPOSAL)

Fiction: the season track (core-loop §7) is the player's own pages in the realm's chronicle (liveops.md §9,
story-forge). The free track is the plain chronicle; the paid track is the **illuminated** one — gilt
margins (GILT #C9A04C), painted initials, the player's deeds in gold leaf.

```
S = 35 season days (1 Truce + 4 contest weeks, liveops.md §3.1)
L = ceil(0.70 · S) = 25 levels × 100 activity points (core-loop §7 rule 5); top = 71% of days
overflow = floor((S − L) · 100 / 200) = 5 pages, one per 200 points after the top
whole-week alternatives: S 28 / 42 d → L 20 / 30, overflow 4 / 6 (5 levels per week, 1–9 weeks)
```

| Per 35-day season (25 levels) | Plain (free) | Illuminated (paid) |
|---|---|---|
| Each level | 1 h own output (odd levels, 13 h) or 1 h Universal (even levels, 12 h) | the same again (13 h + 12 h) |
| Cosmetics | plain pennant 5, banner 10, portrait frame 20, keep dressing 25 | illuminated pieces at 5 / 10 / 15 / 20 / 25; the illuminated keep dressing at 25 |
| Journeys | 2 seat-move writs (world.md §9); the Writ of Passage at 1,500 points (level 15; earned, never sold — liveops.md §7) | nothing more |
| Lords | 40 Plain Seals per season ([lords.md](lords.md) §11, 1.14 per day) and Fable's free step | Seals only if paid Seals are accepted (§3 #2) |
| Overflow page | 1 h own output | + an illuminated marginal flourish |

1. Points are activity points: never sold, never boosted (no "+50% points"), no level skips.
2. Buying late unlocks every illuminated reward already earned ("You receive the rewards of 18
   levels now; 7 more up to level 25"). Unclaimed rewards arrive by mail at season end (mail-forge).
3. **Story is free**: every chapter, quest and event sits on the free side; illumination adds art,
   never text or content. The "chronicle finished" honour at the free top is earned-only (§3 #9).
4. Illuminated goods and works ≤ the free track's (money doubles at most); they count against the
   allowance when claimed, and a claim past the cap waits in the chronicle.
5. One price tier (€4.99 proposed), no "premium plus" with levels; payable with gems at the
   published rate (recommended: a free player saving MON-001 gems can illuminate a season).

| Fails when | Caught by |
|---|---|
| Free top needs > 72% of season days | [ ] fair_money_probe chronicle line |
| A paid item speeds points or skips levels | [ ] grant whitelist |
| Paid-track goods + works > free-track goods + works | [ ] data check on the season table |
| Season text, quest or event only on the paid side | [ ] story-forge content map: 0 paid-only ids |

## 8. Fairness metrics

**8.1 Free path lengths** — upper bounds; the owning reference's simulation must print them
(SKILL.md rule 6). Ratio = free days ÷ max-allowance days at equal activity.

| System | Top | Engaged free ≤ | Max-allowance path | Ratio cap | Owner of the sim |
|---|---|---|---|---|---|
| Spine | keep L30 | 90 d; casual 120 d (progression.md §12 #7; sim 70 / 86 d) | ≥ free ÷ 1.93 (heavy + charter sim: 46 d) | 2.0 | progression.md §9 |
| Troops | t10 opens (cavalry t11) | sim t10 day 32, t11 day 70 (progression.md §6) | ≤ 1 tier ahead on ≥ 95% of days 0–120 | 2.0 | progression.md, combat.md |
| A lord | first lord complete, L50 | 60 d (lords.md §11: 32 d, 57 d) | = free; paid Seals: 19 d, 40 d | 1.0 (2.0) | lords.md |
| A lord's four-piece set | all four at Masterwork | 90 d (PROPOSAL; lords.md §9 has no day yet) | = free while whetstones and gold leaf bind | 1.0 | lords.md |
| Guild patronage | rank X | 300 d (5 of 7 days); 164 d (daily + Merit) | 92 d | 2.0 | §6 |
| Chronicle | free top | 25 of 35 days (71%) | = free | 1.0 | §7 |
| War-week score | season median | — | ≤ free × 1.25 | 1.25 | liveops.md |
| Earned honours | any | earnable | cannot be bought | — | §3 #9 |

Lord ratio 1.0 holds while Seals and lord XP stay unsold and no lord step costs a sellable resource; with
paid Seals, lords.md's figures apply (heavy 1.4–1.7× by path; its rule ≤ 2× on every lord path).
progression.md §9's heavy profile (income × 2.5) is above what §4 allows (goods × 2.0 in a Truce week,
× 1.25 in a war week): re-run it at the §4 caps before quoting its rush ratio.

**8.2 Earned share and the top 100.** Every grant and every plate-hour carries a source tag
(`play` | `bought`), in one unit, **work-hours**: plate hours elapsed, hourglass minutes ÷ 60,
goods in own-output hours at grant time. Earned share `E = play ÷ all`, lifetime per account.
At the cap `E_min` = 0.52 (Truce week), 0.81 (war week), 0.73 over a campaign — works line, late
profile (§4). A realm under 5,000 players uses its top 2%.

| Metric (per realm, weekly) | Target | Alarm (2 weeks running) | Action |
|---|---|---|---|
| Power-weighted `E` of the top 100 by power | ≥ 0.70 | < 0.62 | freeze new power-relevant SKUs; design review |
| Non-payers in the top 100, realm day 90 | ≥ 20 | < 10 | same |
| Max-allowance ÷ engaged-free median power, day 90 | ≤ 1.8× | > 2.0× | allowance bug hunt (cloud-forge) |
| Max-allowance ÷ engaged-free season score | ≤ 1.2× | > 1.25× | review R war |

**8.3 Watch, never target**: payer share of monthly actives; chronicle attach rate among D30 actives; median
day of first purchase; refund rate per SKU (> 5% → SKU pulled for review); "pay to win" tickets per 1,000
DAU; top-1% payers' revenue share (> 50% = whale dependence, owner flag).

## 9. Store compliance and age rating

Store and legal facts below come from general knowledge (2026-09), not a sourced research file: every row is
confirmed with counsel and the current store policy before launch (owner item — game-director rule 6);
`[verify]` marks the least certain.

| Topic | Rule (source) | Our implementation | Check |
|---|---|---|---|
| Paid random items | Apple App Review Guideline 3.1.1 and Google Play Payments policy: odds shown before purchase; PEGI "In-game purchases (includes paid random items)" and ESRB "In-Game Purchases (Includes Random Items)" notices (2020); Belgium treats paid loot boxes as gambling (2018); South Korea's odds-disclosure law (2024) [verify] | none sold (§3 #8): no odds duty, no notice, no per-country switch | whitelist |
| Earned random chests and draws | trust, future-proofing | a contents sheet with % per item, 1 tap from the chest; a pity counter on every rare result (lords.md §10) | ux_flow_probe |
| Age rating | IARC questionnaire in Play Console → PEGI, ESRB, USK…; owner: PEGI-7 | declare in-game purchases; no simulated-gambling look (wheel, reel, card flip, roulette) even for free rewards [verify PEGI criteria] | art register |
| Children | EU Unfair Commercial Practices Directive, Annex I No. 28: no direct exhortation to children to buy | descriptive copy ("Price €4.99", "Contents"); never "Buy now!", "Don't miss out"; per-locale review (l10n-forge; TASK_BOARD W7 i18n wave) | string lint, banned-phrase list |
| "Was" prices | EU price-indication rule (Omnibus): prior price = lowest of the last 30 days [verify for in-app items] | strike-through only from price history | offers_test |
| Virtual currency | EU consumer-protection network principles on in-game currencies (2025) [verify] | gem prices also show "≈ €x.xx" (store price ÷ published rate); §5 rule 5 | shop screen probe |
| Real prices | the store's localized price only (Google Play Billing product details; StoreKit on iOS) | prices read from the store at runtime | grep: no "€" / "$" literals in offer data |
| Validation | Google Play refunds purchases not acknowledged within 3 days | server validates the token (Play Developer API) → grants → acknowledges | iap_test (shop-forge) |
| Refunds | Play Voided Purchases API; App Store server notifications (REFUND) | revoke unspent goods; spent gems become a gem debt that blocks gem use until repaid; no ban on a first case | cloud-forge daily job |
| Subscriptions | auto-renewal must be a store subscription with stated terms | Month's purse ships as 30-day non-renewing, or as a true subscription — never renewal on an in-app product (TASK_BOARD bug, verify) | shop-forge billing check |
| Dark patterns | US FTC: Epic Games 2022 ($245 M refunds), HoYoverse 2025 [verify] | buy button ≥ 16 dp from any frequently tapped control and never where "Claim" or "Help all" sit on other screens; the store sheet is the confirm | ux_touch_probe |
| Minors | store parental controls | neutral year-of-birth screen at first purchase; under 18: default monthly limit €50 (owner + counsel) | owner decision |
| Data | Play Console Data safety form | declare purchase history; no spend-based personalisation (§5 rule 2) | ship-forge checklist |
| Billing | MON-002: billing blocked | owner item, never faked | — |

## 10. Money-law screens and art

- **War screens** (no buy button, gem button or offer): battle presentation and replays, reports, march and
  rally dispatch, scout reports, the war-window tally, the realm map while a hostile march targets the
  player. A report links to the infirmary, where the gem finish shows hourglass art only.
- **Buy screens** (no war imagery anywhere — backgrounds, head-pieces, offer icons): the shop, offer cards
  and pop-ups, the chronicle sheet, gem-finish confirms, the purse.
- **Allowed**: goods as things (SHP-*); works (masons on scaffolds, a turning hourglass, scribes); journeys
  (JRN-*: a laden caravan, a barge at a quay); the cosmetic on the player's own keep; frame previews on an
  empty ground or a court portrait. Light (game-art-director environments.md presets): working noon or
  campaign dawn, chronicle night for the chronicle sheet; never siege dusk.
- **Forbidden**: drawn or raised weapons, troops in formation, siege engines, fire or smoke over buildings,
  the wounded or dead, blood, enemy banners, march lines, an armed lord. BND-siege and BND-warlord were
  refused for exactly this (owner ledger; environments.md: "two bundle paintings were refused").
- **Card**: the goods render fills ≥ 50% of the card (ART SHOWN BIG), price clear of the focal band; Close
  visible from the first frame, ≥ 48 dp, as tall as Buy, labelled "Close" (no shaming copy); no red dots on
  offers; offer icons are Blender-made art (ui-forge); ≤ 1 offer icon on the HUD ([ux.md](ux.md)).
- **Cosmetics** (built through blender-forge) leave the ownership tint-mask areas untouched (blender-forge
  architecture.md §7), never use relationship colours decoratively, keep KEEP_ASPECT 1.50 and the tier
  silhouette readable at region zoom, and carry `stats == {}`.

| Fails when | Caught by |
|---|---|
| A buy screen carries war imagery | [ ] every BND/SHP/JRN row in `tools/assets.json` tagged `money_ok`, reviewed against the forbidden list |
| A war screen carries a buy or gem button | [ ] ux_flow_probe walk of every war screen: 0 purchase nodes |
| A cosmetic breaks the read or the contract | [ ] `skin_contract_test`, `cv_keep_reconcile`, `structure_audit`, `contrast_test` |
| Close smaller than Buy, or delayed | [ ] ux_touch_probe on every offer layout |

## 11. Genre weak spots → our move

| Genre pattern ([benchmark.md](benchmark.md)) | Where it hurts | Our move | Number |
|---|---|---|---|
| A status ladder fed by login streaks and 1 point per premium currency spent; a permanent second builder at a mid rung | a core queue sold; status = spend | patronage fed by play (points 1:1 + Merit); coin favour capped; no stat or plate perks | ≤ 700 coin favour per week |
| Leaders exclusive to status-tier or bundle offers | sunk-cost ladder; "stuck without the meta leader" | no lord or lord advancement on a paid surface | 0 paid rows |
| Cosmetic city skins carrying stats | look and power blur | stat-free cosmetics, tested | `stats == {}` |
| No spending ceiling; top ranking an open spending contest (top-server spenders "$10–20k+", reviews) | free players leave the top | the per-plate allowance | ≤ 1.93× Truce week, ≤ 1.23× war week, 1.37× per campaign |
| Pass sells extra levels and +50% progress points | paid ranks on a shared track | points never sold; paid track ≤ free track | 1.0× on points |
| Chance chests opened by keys that a spend-fed status tier also grants (≈ 3% of drops a top-rarity leader token; no pity found) | gambling risk, rating risk | no paid random items | 0 |
| Paid relocation and shields during war | buying out of attacks | wards and the Writ of Passage never sold; no seat move in war weeks or with an inbound march | 0 wards sold |
| Offers crowding navigation, red-dot fatigue [observational] | offer blindness, resentment | pop-up and icon budget; no dots on offers | ≤ 1 per day, ≤ 3 per week |
| Purchases gifting the alliance | spending normalised socially | anonymous cosmetic Patron tokens only ([alliance.md](alliance.md) §6); buyer and price never named | ≤ 3 per alliance per day, 0 gift XP |
| Paid shortcuts decide persistent war | strategy erased | war-week R and war-window cap | 1.25; ≤ 480 min |

## 12. Harness, save, server cost

| Proof | Measures | Verdict line (PROPOSED — qa-forge fixes wording) |
|---|---|---|
| `core/offers_test.gd` + shop police (shop-forge; extend) | grant whitelist, `free_route`, `return_at`, value claims, `money_ok` art tags, progress-only eligibility, no currency literals | `OFFERS OK - 0 forbidden grants, 0 missing free routes, 0 untagged art` |
| `fair_money_probe` (new; qa-forge; path to confirm) | §4 ratios, `E_min`, patronage and chronicle paths; 90 days × free / light / max | `FAIR MONEY OK - truce 1.93x <= 2.00, war 1.23x <= 1.25, campaign 1.37x, E_min 0.52, patronage X 300d/164d/92d` |
| allowance server test (cloud-forge) | per-plate use, hold, war-window and favour caps; seat-move blocks; 0 ward SKUs | `ALLOWANCE OK - 0 over-cap grants in 10000 fuzzed purchases` |
| `ux_flow_probe`, `ux_touch_probe`, `menu_test`, `a11y_audit` | pop-up timing, Close/Buy parity, war-screen scan | existing lines |
| `tools/econ_sim.py` | bought goods as `pack_mult` sources (economy.md §12: heavy 6 ≈ 160 h a week = the Truce-week bound; campaign average ≈ 67 h, pack_mult ≈ 2.5) | day-30 band, [numbers.md](numbers.md) §6 |
| weekly telemetry job (cloud-forge) | §8.2 table per realm | dashboard row per realm |

**Save migration**: held items load as `play` origin (billing is blocked, MON-002 — if any real purchase
exists, tag its grants `bought`); Favour seeds from stored daily points, else 0; allowance counters start
at 0 on the first Monday after load.
**Server cost** (estimate; measure with `core/sd_cost_probe.gd`): the source tag is 1 byte on grants already
written; the per-plate counters ride on the plate-start write; a purchase = 1 token validation + 2 writes.
5% payers × 0.3 purchases per day (assumed) × 50,000 players = 750 purchases ≈ 1,500 writes per day,
< 0.1% of the loop's 2.9 M (core-loop §11), plus 1 top-100 query per realm per day.

## 13. Owner decisions required

1. **R** = 2.0 in the Truce week, 1.25 in war weeks incl. a realm's Founding week (§4); the per-plate cap; the € weekly ceiling shop-forge derives from it.
2. Guild Patronage: the name; coin favour yes or no; `f_e` (favour per €); the Merit Favour item (alliance.md §16 #4).
3. Illuminated chronicle price (€4.99 proposed); payable with gems (recommended yes).
4. Largest SKU €49.99; the personal budget tool; the under-18 default limit (€50) and the age screen, with counsel; the Play Console target-audience declaration (Families policy applies if under-13 is included).
5. Wards never sold (recommended, matches onboarding.md §4); the Writ of Passage never sold (liveops.md §13 #4); in-realm seat moves sold in Truce weeks only, or never.
6. Resolve never sold; ≤ 480 min war-window gem finish — the same decisions as core-loop §12.
7. Paid random items: never (recommended). Paid Seals (lords.md §17 #2): recommended no; if yes, as §3 #2.
8. Names (story-forge): Guild Patronage / Favour, the illuminated chronicle, First purse, Month's purse, the shop-header promise.
