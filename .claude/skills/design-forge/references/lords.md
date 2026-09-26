# Lords — roles, ranks, Orders, talents, pairs, sets, Seals

The eight lords (commanders) as a system: what each is for, how they grow, how two share a march, what the four-piece sets do, how duplicates become currency with published math, how every lord is reached without paying, and how power creep is stopped. Implementation: **gameplay-forge** (rules, data, save, resolver hooks), **commander-forge** (lords end to end — portrait, hall figure, kit, map token, lord screens; it follows THIS file for rules and numbers), **battle-forge** (Order beats), **report-forge** (the cause ledger), **story-forge** (names, voices), **ui-forge**, **qa-forge**. Genre facts: [benchmark.md](benchmark.md) §5.

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Read the shipped data first (`data/equipment.gd` exists; lord and talent data: path to confirm). A shipped sacred balance constant keeps its value; this file's value then becomes a proposal to the owner. **Units** are [combat.md](combat.md)'s: 1 TS = the strength of one troop tier; **cTS** = 0.01 TS. `R_med` = rounds in a median field battle (the frozen resolver sets it; examples use **R_med = 24**, verify).

## 0. The four questions

- **Want**: a lord who wins the fight you care about; the next rank, skill level or set piece; a hall of eight sworn lords.
- **Obstacle**: lord XP (time: camp hunts), Seals (from play), set pieces (iron and anvil time), talent choice (34 points for 60 slots).
- **Wait (free)**: first lord at minute 2; 3 lords by day 7; all 8 by day 24–28; the first lord at Masterwork with every skill at 5 by day 32, level 50 by day 57; its four pieces at Masterwork by day ~160; all 8 lords complete by day 211 (§11).
- **Witness**: the gilt rim of a Sworn lord on the map token; the hall figure wearing the real kit; the set's name in reports; the lord's sigil on the march banner; "Lord strength 0.42 / 0.50 tier" on the lord screen.

## 1. Genre pattern → where it hurts → our move

| Genre does | Where it hurts players | Our move (§) |
|---|---|---|
| 4 commander rarities; the low ones are fodder by week 2 | the roster shrinks to a few "real" commanders | no rarity on lords; the four tiers are the lord's RANK (§3) |
| stars raise the level cap by 10 each, cap 60 | a sound gate | kept as a pattern: rank caps level at 20 / 30 / 40 / 50 (§4) |
| 4 skills at levels 1–5; a capstone when all are maxed | ~690 duplicate tokens per top commander; no pity timer found | 4 skills, 260 Seals to max, hard pity at 20 (§5, §10) |
| rage ~100 per attack, first cast ≈ turn 11, overflow wasted [community estimate] | lost rage; a long wait for the first cast | the war drum: fixed gain per round, first Order at R_med/3, nothing wasted (§5) |
| 3 of 15 talent trees, up to 74 points | newcomers cannot read the tree | 3 branches × 8 nodes, 34 points, one capstone (§7) |
| primary + secondary; only the primary's talents and gear apply | good: squares build space without new content | kept; the secondary gives its Order and first passive only (§8) |
| a +5% counter under talent, gear and status stacks | "PvP is raw power, not tactics" | the lord pool ≤ 0.50 TS = half a counter (combat.md §5); no lord source touches a counter (§6) |
| exclusive commanders in paid bundles; winner-take-most token races | "stuck" after missing one commander | every lord has a free channel; milestone rewards only (§11) |
| new top commanders each season; talent trees reworked | investment wiped out | fixed ceiling, sidegrade rule, Seal transfer on every nerf (§12) |

## 2. The eight lords — roles (PROPOSAL, from portraits.md)

A **role** is the question a lord answers best. S1–S8 are the harness scenarios (§14).

| Lord | Portrait cue (portraits.md) | Role | Line | Talent branches (§7) | Set (§9) | Best at |
|---|---|---|---|---|---|---|
| Edwin | older, grey temples, crimson mantle (shipped anchor) | holds the front | infantry | Shieldwall · Garrison · Hunt | Edwin's | S2 field defence |
| Alric | "wins quickly or not at all", wolf-pelt | shock: wins early, fades late | any | Assault · Charge · Road | Alric's | S6 short fight |
| Elena | archer-commander, dark braid, green hood | strikes first, from range | archers | Longshot · Garrison · Hunt | Elena's | S1 field attack |
| Rowan | young cavalier, plume, kite shield | speed, interception | cavalry | Charge · Road · Hunt | Rowan's | S6; S8 camp hunt |
| Godric | siege master, stylus, bronze instruments | breaks walls; engines | crossbows + siege | Windlass · Siegecraft · Road | Godric's | S3 castle assault |
| Maud | stern matron in black, tower shield | defence, the wall | spearmen | Pike Hedge · Garrison · Shieldwall | Maud's | S4 garrison |
| Faber | the King's Armourer, apron over mail | makes the primary's gear count | support | Armoury · Shieldwall · Hunt | none | secondary to a geared primary |
| Fable | the Chronicler, chained ledger | XP, reports, drum denial | support | Chronicle · Road · Hunt | none | S7 long fight; levelling |

1. Each lord is top-2 (as primary or secondary) in ≥ 1 of the 8 scenarios, or it is buffed in the next balance window. No lord is top-1 in more than 2 scenarios.
2. The role reads in one line on the card: "Holds the front. Infantry."
3. Lords never die, are never captured, never lose XP; a beaten march brings its lords home.

| Fails when | Caught by |
|---|---|
| A lord is top-2 in no scenario (a lord nobody fields) | [ ] lord_balance_probe: `every lord top-2 in >=1 scenario` |
| One lord holds > 30% of primary slots at day 30+, or one < 5% | [ ] telemetry: primary share per lord |

## 3. Rarity — one four-tier ladder, four uses

FOUR tiers: **Issued → Sound → Fine → Masterwork** (never five). Lords have NO rarity of their own: with eight hand-painted lords, a low-rarity lord is a lord nobody fields — that breaks pillar 6 ("each lord has a role, a path, and a reason to be fielded"). A lord arrives at Issued when sworn.

| Use | Issued | Sound | Fine | Masterwork |
|---|---|---|---|---|
| Lord RANK: level cap | 20 | 30 | 40 | 50 |
| Lord RANK: skill level cap | 2 | 3 | 4 | 5 (+ Oath) |
| Lord RANK: ceiling on the pair's lord strength (primary's rank) | 0.06 TS | 0.12 TS | 0.25 TS | 0.50 TS |
| Gear FINISH: strength per piece | 0.25 cTS | 0.75 cTS | 1.75 cTS | 4.0 cTS |
| Gear FINISH: rune light (the 3D rune dial, equipment.md) | 0 | 0.7 | 1.5 | 2.6 |
| Portrait FRAME metal (equipment.md register) | plain field metal | clean steel, one bronze fitting | etched lines, gilt border | gold inlay, one set gem |

The rank ceiling is shown, never silent: "Lord strength 0.12 / 0.12 — Capped. Fine rank raises it to 0.25" (combat.md §5 rule 2).

## 4. Levels and XP

- **XP unit = one minute of standard play** for a focused lord. Standard play = 24 camp kills a day (Resolve 240 per day ÷ 10 per attack, [core-loop.md](core-loop.md) §3). **A camp kill at or above the recommended level = 60 XP to EACH lord in the march** (below it: 30). A standard day = 1,440 XP.
- Tomes (**field journals**) are priced in the same minutes: 60 / 480 / 1,440 XP (1 h / 8 h / 24 h), like speed-ups in [numbers.md](numbers.md) §7; the alliance store's "Lord XP tome" ([alliance.md](alliance.md)) is the 480 size. The daily 100-point chest (core-loop §7) gives 240 XP. Free focus lord: 1,680 XP per day.
- Curve: `python tools/curve.py --levels 49 --first 3m --last 7d --shape phased`; row L's duration in minutes = the XP for level L → L+1. Total to L50: 95,888 XP.

| Reach level | XP of the step | Cumulative | Free focus lord | The level grants |
|---|---|---|---|---|
| 2 | 3 | 3 | first battle | a talent point is banked for L10 |
| 10 | 21 | 86 | first hour | talents open with 9 points (first-time moment, [onboarding.md](onboarding.md) §7) |
| 20 | 182 | 996 | day 1 | Issued cap; 19th point |
| 30 | 833 | 5,608 | day 3.3 | Sound cap |
| 40 | 3,809 | 26,710 | day 15.9 | Fine cap |
| 45 | 6,388 | 53,544 | day 31.9 | — |
| 50 | 10,080 | 95,888 | day 57.1 | Masterwork cap; 34th point |

1. **Every level grants one thing**: a talent point (levels 2–20 and even levels 22–50) or a stat step (odd levels 21–49: +0.05% damage and +0.05% defence = 0.2 cTS; 3 cTS in total). No empty level.
2. **XP at a cap is banked, never lost**; it applies the moment the rank rises.
3. **Hall drills (catch-up)**: a lord in no march gains 25% of the XP the fielded lords earn, up to (highest lord level − 5); credited when the hall opens — one write, not one per kill.
4. XP comes from PvE, rallies on camps and strongholds, tomes, chests and chronicle quests ([liveops.md](liveops.md)). **PvP gives no lord XP.**

| Fails when | Caught by |
|---|---|
| XP lost at a cap; a benched lord > 10 levels behind the top lord | [ ] seal_path: banked XP 100%, drills gap ≤ 5 levels |
| Free focus lord reaches L50 before day 45 or after day 70 | [ ] seal_path, free profile |

## 5. Skills — four per lord; Orders on the war drum

| Skill | Unlocks | Levels | Acts when the lord is | Budget at L5 |
|---|---|---|---|---|
| **Order** (active) | sworn | 1–5 | primary or secondary | 8 cTS primary / 3 cTS secondary |
| **Passive I** (line or role) | sworn | 1–5 | primary or secondary | 3 cTS |
| **Passive II** (a situation) | Sound rank | 1–5 | primary only | 2 cTS |
| **Oath** (capstone) | Masterwork + the other three at 5 | one | primary only | 1 cTS |

Value by level: L1 20%, L2 35%, L3 50%, L4 70%, L5 100% — the last level is the big one. Budgets are measured in the probe's standard fight (combat.md §5).

**The war drum (tempo meter).** Each lord in a march has a drum of 1,000. The primary's drum gains `1000 ÷ (R_med / 3)` per round (125 at R_med 24: Orders at rounds 8, 16, 24); the secondary's gains half (round 16). When both are due in one round, the secondary gives its Order one round later (17): one Order beat per round, always. At 1,000 the Order fires and the drum resets; gain is fixed per round, so nothing overflows; bonus drum past 1,000 carries to the next fill. Reports say "next Order in 3 rounds", never a drum number; the cause ledger lists the top 5 casts (combat.md §12).
- **Order unit**: every Order at L5 ≈ **0.35 of one normal round** of the whole march (a strike of 35%, or −15% damage taken for 2 rounds). 3 casts in 24 rounds = +4.4% damage ≈ 8 cTS. The harness tunes the value, never the cadence.
- **Caps**: enemy effects remove ≤ 300 drum per 8 rounds and slow gain by ≤ 15%; drum start bonuses ≤ 50%.

| Lord | Order (L5) | Passive I | Passive II | Oath |
|---|---|---|---|---|
| Edwin | Close the Ranks: damage taken −15% for 2 rounds | Old Soldier: infantry +3% defence | Hold Fast: below 50% troops, +5% damage | The Crimson Line: Close the Ranks lasts 3 rounds |
| Alric | Wolf's Rush: strike 0.35 round; ×1.6 before round 6 | First Blood: +8% damage rounds 1–5; −4% from round 13 | Pack Hunter: +5% damage vs a target another march already fights | No Second Charge: drum starts at 50% |
| Elena | Loose!: volley 0.35 round; +30% if ≥ 50% of the march are archers | Green Hood: archers +3% damage | High Ground: defending a castle or held tile, archers +4% damage | First Light: a free 0.2-round volley before round 1 |
| Rowan | Break Them: charge 0.30 round; target's drum −100 | Plume and Kite: cavalry +3% damage | Outrider: march speed +8% (utility) | Spur: Break Them removes 200 drum |
| Godric | Measured Shot: strike 0.30 round; ×2 vs walls, gates, towers | Stylus and Rule: structure damage +8% (utility) | Windlass Drill: crossbows +3% damage | Engine Master: siege engines assemble 15% faster (siege-forge) |
| Maud | Tower Shield: damage taken −12% for 2 rounds (−18% at her own castle) | Brace: spearmen +3% defence | Mistress of the Wall: as garrison lord, wall durability loss −8%, 8 points of severe → light (utility) | Black Vigil: defending the castle, drum starts at 50% |
| Faber | Field Forge: 1.5% of the march's troops return from lightly wounded to the fight | Armourer's Eye: the primary's gear-piece strength +20% | Spare Rivets: below 50% troops, damage taken −3% | Master's Eye: Armourer's Eye rises to +30% |
| Fable | Set It Down: enemy primary's drum −250 + strike 0.15 round | The Ledger: both lords +20% XP; the report shows the enemy's full lord breakdown | Old Roads: enemy drum gain −10% | Foretold: Set It Down also fires once at battle start |

Names are working names for story-forge. **No skill, talent or set bonus reads "+X% versus <line>"**: the counter is combat.md's own category, never modified (§6).

| Fails when | Caught by |
|---|---|
| A primary fires < 2 or > 4 Orders in a median battle | [ ] lord_balance_probe: Orders per S1 battle |
| Two Order beats land in one round | [ ] resolver audit: one Order beat per round |
| A lord, talent or set data row modifies a counter | [ ] grep of lord data for counter fields = 0 (combat.md §5) |

## 6. The lord pool — half a counter, and a timeline inside combat.md's stack

combat.md §5 puts everything a lord brings into ONE pool, capped at **0.50 TS = half a counter** (rule I3: lords matter, never alone), measured by ablation in the combat probe. This file adds level steps and piece strength to that pool (combat.md lists talents, the set and skills) and splits the cap:

| Source (maxed pair: primary Masterwork L50 + a secondary) | cTS |
|---|---|
| Primary level steps (odd levels 21–49) | 3 |
| Primary talents (34 points, combat nodes only) | 8 |
| Primary gear: 4 Masterwork pieces 16 + set bonuses 3 | 19 |
| Primary skills: Order 8, Passive I 3, Passive II 2, Oath 1 | 14 |
| Secondary skills: Order 3, Passive I 3 | 6 |
| **Cap for a maxed pair** | **50 = 0.50 TS** |

1. Lord bonuses add inside the pool and multiply with other pools (numbers.md §9); the clamp applies at resolve time. A rally or a garrison side counts ONE pair: the leader's (combat.md §9).
2. **Utility effects sit outside TS but are capped** (all lord sources together): march speed ≤ +15%; structure damage ≤ +20%; severe → light shift ≤ 10 points; XP ≤ +35%; engine assembly ≤ −25%.
3. Lord power (numbers.md §3) is proportional to the lord pool, on the troops' power scale.
4. **Timeline** (focus pair, `seal_path` model of §11, rank ceilings of §3 applied): lords are the early visible power; the realm pool (research, buildings — [progression.md](progression.md)) fills the rest of combat.md's totals later.

| Day | Lord pool, free median | Heavy: paid Seals (§17 #2) + bought iron (0.19 / 0.36 / 0.43 without iron) | combat.md §5 total, free median | Left for the other pools |
|---|---|---|---|---|
| 7 | 0.12 (Sound ceiling) | 0.21 | 0.15 | 0.03 |
| 30 | 0.28 | 0.39 | 0.35 | 0.07 |
| 90 | 0.43 | 0.48 | 0.60 | 0.17 |
| 180 | 0.50 (cap; last Masterwork piece ≈ day 160) | 0.50 | 0.85 | 0.35 |

| Fails when | Caught by |
|---|---|
| A maxed pair measures > 0.50 TS | [ ] combat probe STACK (ablation), combat.md §14 |
| Lord pool at day 7 / 30 / 90 above the table by > 0.03 | [ ] seal_path timeline vs stack telemetry by cohort |
| A utility total passes its cap with every source stacked | [ ] data audit: worst stack per cap |

## 7. Talents — three branches, 34 points, one capstone

- **Points**: 1 per level from 2 to 20, then 1 per even level from 22 to 50 = **34**. Talents open at L10 with 9 points waiting. The same for every lord.
- **A branch = 8 nodes, 20 points**: 6 minor nodes × 3 ranks + a keystone (1 point, needs 8 spent in the branch) + a capstone (1 point, needs 18 spent). 3 branches = 60 slots. 34 of 60 forces a choice: one full branch + 14 in a second (its keystone), or three keystones and no capstone. **At most one capstone per lord.**
- A combat minor rank ≈ 0.24 cTS (e.g. +0.5% to one line's damage). Branch template (Shieldwall): row 1 infantry damage, infantry defence; row 2 damage taken below 50% troops, Order strength; row 3 garrison defence, march speed; then keystone, capstone.
- **Pages and resets**: 2 pages per lord (field, wall), a 3rd at Fine. Reset and page switch are **free, always** (onboarding.md's "free to day 14" is only the floor), locked while the lord marches or garrisons a castle under attack. Never sold.

| Branch | Keystone | Capstone |
|---|---|---|
| Shieldwall (infantry) | Locked Shields: march ≥ 50% infantry → damage taken −3% | Unbroken: once, below 40% troops, damage taken −20% for 2 rounds |
| Pike Hedge (spearmen) | Set Pikes: spearmen +3% defence rounds 1–3 | Hedge: attackers hitting spearmen take back 5% of that damage |
| Longshot (archers) | Range: march ≥ 50% archers → archers +3% damage | Second Volley: each Order adds a 0.1-round archer strike |
| Windlass (crossbows) | Heavy Bolts: crossbows ignore 3% of defence | Pavise Line: crossbows take −8% damage rounds 1–4 |
| Charge (cavalry) | Couched Lance: cavalry +4% damage rounds 1–3 | Run Down: +6% damage vs marches below 50% troops |
| Garrison (role) | Walls: as garrison, damage taken −3% | Last Gate: garrison severe → light +5 points (utility) |
| Assault (role) | Opening: +4% damage rounds 1–5 | Drum Roll: drum starts at 20% |
| Siegecraft (role) | Sappers: structure damage +6% (utility) | Breach: gate damage +10%, engine assembly −10% (utility) |
| Armoury (role) | Well Kept: this lord's gear-piece strength +8% | Three-Piece Harness: a set's 4-piece bonus works with 3 pieces |
| Chronicle (role) | Notes: both lords +10% XP (utility) | Foresight: the enemy primary's drum starts at −250 |
| Hunt (utility) | Tracker: +8% damage vs camps and AI-lord hosts | Clean Kill: −20% losses vs camps |
| Road (utility) | Marching Order: march speed +5% | Forced March: return trips +20% speed, gathering load +10% |

12 branch kinds written once, used in 24 slots (§2). One screen: 3 columns × 4 rows, keystone and capstone drawn larger, the role's recommended path lit.

| Fails when | Caught by |
|---|---|
| A node needs more than one line to explain | [ ] every node text ≤ 60 characters (l10n-forge) |
| One branch is in > 60% of a lord's builds at day 30 | [ ] telemetry per lord → rework the losing branches |

## 8. Pairing — primary and secondary

1. A march has one **primary** and may add one **secondary**; a lord is in one march at a time.
2. **Primary**: level steps, all four skills, talents, gear, set bonuses, the rank ceiling.
3. **Secondary**: its Order (half-speed drum) and its Passive I, at its own skill levels. Nothing else: its gear, talents, Passive II and Oath show greyed, "primary only".
4. The secondary slot opens with the second sworn lord (onboarding.md §6, chapter 4). Adding a secondary never removes anything: a solo primary fires the same Orders.
5. Up to 5 saved pairs (one per march banner), each with its talent page ([core-loop.md](core-loop.md) §8).
6. Both lords earn full march XP. The garrison pair is the pair the owner sets on the wall; unset or away → the highest-level lords at home stand in (combat.md §9).

| Fails when | Caught by |
|---|---|
| The best pair of a scenario beats its median pair by > 0.10 TS | [ ] lord_balance_probe: 56 ordered pairs × 8 scenarios |
| Players do not field pairs | [ ] onboarding.md §7 metric: ≥ 60% field a pair |

## 9. Kits — the six four-piece sets

Canonical: 24 items = 6 four-piece sets, one per lord (equipment.md; game-director lessons #6). Slots: **weapon, armour, helm, token**. The mapping is a PROPOSAL from the portrait cues; `data/equipment.gd` is the truth, and commander-forge's kit sheet must match whichever is shipped.

| Set | Weapon | Armour | Helm | Token | 2 pieces | 4 pieces |
|---|---|---|---|---|---|---|
| Edwin's | Arming Sword | Oathplate | Crown Helm | War Standard | infantry damage taken −2% | Last Stand: below 50% troops, damage taken −4% |
| Alric's | Greatsword | Mail Hauberk | Nasal Helm | Wolf-fur Cloak | +3% damage rounds 1–5 | drum starts at 25% |
| Elena's | War Bow | Gambeson | Archer's Hood | Signet Ring | archers +2% damage | Order strikes +15% |
| Rowan's | Lance | Cuirass | Great Helm | War Horn | march speed +5% (utility) | round 1: cavalry +8% damage |
| Godric's | Engineer's Warhammer | Brigandine | Kettle Helm | Engineer's Rule | structure damage +5% (utility) | siege engine load +10% (utility) |
| Maud's | Tower Pike | Full Plate | Bascinet | Reliquary | spearmen +2% defence | as garrison: wall durability loss −6% (utility) |

1. **Any lord may wear any piece**; only the primary's pieces act. Two sets' 2-piece bonuses both apply (2 + 2). A set on its own lord adds NO strength — only the look (§13).
2. **Faber and Fable have no set** (8 lords, 6 sets): the Armoury and the Chronicle are their kits.
3. **Making a piece** at the smithy anvil (progression.md: smithy = lords' gear; a plate under core-loop §2 rules): swearing a lord unlocks that set's 4 patterns. Craft at Issued (30 m); temper to Sound (4 h), Fine (16 h), Masterwork (48 h); help and free finish apply. Fine and Masterwork tempering open when Faber is sworn. Costs: iron + whetstones (camps) + gold leaf (Fine and up; events, alliance store) — amounts in [economy.md](economy.md), sized so a free player's four pieces reach Sound by day 14, Fine by day 42, and Masterwork one by one at about days 70 / 100 / 130 / 160 (the long tail of the lord path; §6 timeline). Copies may be made for more marches.
4. **Refit**: turn a piece into another of the same slot and finish for 20% of its temper materials. Free for 14 days after a rebalance of that set (§12).
5. A set on its own lord, all four at Masterwork, "has a name": shown in the report header. No strength.

| Fails when | Caught by |
|---|---|
| One set is on > 50% of primaries at day 30 | [ ] telemetry set share → balance window (§12) |
| A piece's `desc` names something the art does not show | [ ] commander-forge kit check (reference-forge analysis) |

## 10. Seals — duplicates become currency, with published math

- **Lord's Seals** (the wax seal of one lord's house): 10 swear the lord; a duplicate lord = 10 Seals.
- **Plain Seals** act as any lord's Seals, 1:1. Seals of a lord already complete turn into Plain Seals 1:1 automatically — no Seal is ever wasted.

| Step | Seals | Cumulative: rank + all three skills to that rank's cap |
|---|---|---|
| Swear (Issued) | 10 | Issued complete: 22 (skills to 2: 3 × 4) |
| Issued → Sound | 20 | Sound complete: 66 (skills to 3: 3 × 8) |
| Sound → Fine | 40 | Fine complete: 142 (skills to 4: 3 × 12) |
| Fine → Masterwork | 70 | Masterwork complete: **260** (skills to 5: 3 × 16) |
| Skill level 2 / 3 / 4 / 5 (Order, Passive I, Passive II) | 4 / 8 / 12 / 16 | 120 of the 260; the Oath costs 0 |

**The Herald's Summons** (a random draw at the tavern — progression.md: tavern = lord recruitment; free: 1 per day, banked up to 3). Odds, pity counter and the table above are one tap from the Summons board.

| Result | 1 Seal | 2 Seals | 5 Seals | 10 Seals (or the lord, if not sworn) |
|---|---|---|---|---|
| Chance | 55% | 25% | 15% | 5% |

1. **Favoured lord**: the player names one lord; each result goes to it with 50% chance, else to one of the other 7 at random. Default: the first unsworn lord.
2. **Hard pity**: the 20th draw since the last 10-Seal result IS a 10-Seal result for the Favoured lord. The counter shows "10 Seals within 7 draws"; it never resets between events or campaigns; changing the Favoured lord keeps the count.
3. **Published math**: one 10-Seal result per 12.8 draws on average, never more than 20; 2.53 Seals per draw (2.30 before pity); 1.41 per draw to the Favoured lord, 0.16 to each other lord.
4. **Paid lord goods** ([monetization.md](monetization.md) recommends none): never random draws, never a lord, talent points or respecs. IF the owner accepts §17 #2: only a named lord's Seals, Plain Seals and XP tomes, deterministic, ≤ 35 Seals + 5,040 XP per week.

| Fails when | Caught by |
|---|---|
| Served odds differ from shown odds; a 21st draw without a 10 | [ ] summons_probe: 100,000 draws within ±0.5 pp; pity ≤ 20 |
| A Seal is wasted (a complete lord, a full bank) | [ ] seal_path: waste = 0 |

## 11. Acquisition and the free path

| Lord | Free channel | Activity | Free day |
|---|---|---|---|
| First of Edwin / Elena / Rowan | the identity pick (onboarding.md §3) | first session | minute 2 |
| Second of the three | chapter 4 chest (onboarding.md §6) | first week | day 4 |
| Third of the three | the 100th camp kill (hunt ladder) | PvE | day 7–9 |
| Maud | 3 days in one alliance + 30 helps given: she swears at the alliance hall | alliance | day 6–8 |
| Godric | the arsenal built (progression.md tier III: crossbows) | castle | day 8–10 |
| Faber | the first 4 pieces crafted at the smithy | crafting | day 9–12 |
| Alric | the first AI-lord host defeated ([world.md](world.md)) | PvE, realm | day 12–18 |
| Fable | a season-track free step (story-forge chronicle chapter) | campaign, time | day 20–28 |

Every lord also swears at 10 of its Seals (Favoured + pity: ≤ 20 free Summons). **No lord is ever sold, bundle-exclusive or first shown on a paid surface — not even for 24 hours.**

| Seal source (steady state from day 8) | Per day | Goes to | Reward lives in |
|---|---|---|---|
| Herald's Summons, 1 free per day | 2.53 | 1.41 Favoured, 0.16 each other | this file |
| Hunt tally: 1 Seal per 10 camp kills the lord leads (24 kills/day) | 2.4 | the leading lord | core-loop.md §3 (Resolve bounds it) |
| Weekly writ 500 chest: 5 Plain | 0.71 | any | PROPOSAL to core-loop.md §7 |
| Alliance store (the Quartermaster): 5 per week for Merit | 0.71 | any | PROPOSAL to alliance.md |
| Milestone events, 2 a month: 20 featured + 10 Plain at full milestones | 2.0 | featured / any | PROPOSAL to liveops.md R1 |
| Season track free: 40 Plain per 35-day campaign | 1.14 | any | liveops.md, monetization.md |
| New-realm week: 30 Plain over an account's first 7 days (by account age) | 4.3 | any | onboarding.md |
| **Free total** | **9.5** | **7.0 can go to one chosen lord** | |
| Heavy, only if §17 #2 is accepted: 35 Seals + 5,040 XP a week | +5.0 | any | monetization.md |

**Free path, one row per rank** (days; the model puts every chooseable Seal on one lord until it is complete, then the next; `seal_path` reproduces it). Complete = the rank plus all three skills at its cap.

| Rank complete | Seals | First lord: free / heavy* | Second lord: free / heavy* |
|---|---|---|---|
| Issued | 22 | 2 / 1 | 21 / 19 |
| Sound | 66 | 6 / 4 | 36 / 22 |
| Fine | 142 | 15 / 9 | 47 / 28 |
| Masterwork | 260 | 32 / 19 | 63 / 37 |
| Level 50 (XP) | — | 57 / 40 | ≈ 61 / ≈ 61 (secondary XP; tomes go to the focus) |
| All 8 complete | 2,080 | 211 / 138 | |

*Heavy only if paid Seals are accepted; otherwise heavy = free on every lord path (ratio 1.0, monetization.md). With paid Seals: heavy ÷ free = 1.7× on the first lord's Seals, 1.4× to level 50, 1.5× for the hall. **Rule: paid acceleration ≤ 2× the free rate on every lord path; paying reaches nothing the free path does not.** Free checkpoints: day 1 = 1 lord at L20; day 7 = 3 lords, focus at Sound, L30 with XP banked; day 30 = 8 lords, focus Fine-complete at Masterwork rank, L44; day 90 = 2 lords complete.

**The loss-free template** (the Lists, the Grand Melee — liveops.md): every lord, owned or not, at L40, Fine rank, skills at 4, any four Fine pieces, talents chosen freely — so skill beats investment, and a player can try a lord before investing in it.

| Fails when | Caught by |
|---|---|
| Heavy ÷ free > 2.0 on any path, or all-8 free > 240 days | [ ] seal_path: `free 211 d, heavy/free 1.53` |
| An event ranks players for Seals (winner-take-most) | [ ] liveops calendar audit: Seal rewards are milestones only |

## 12. Power creep — the ceiling is fixed; new lords go sideways

1. **Fixed ceiling for the realm's life**: L50, Masterwork, 34 talent points, 4 skills, 4 gear slots, 0.50 TS per pair. Raising any of it is an owner decision and lifts every lord at once, with the materials to reach it.
2. **Sidegrade rule**: a new lord's strength in its best scenario ≤ the current best lord's there, and it must open a new question (a new scenario or situation) instead of answering an old one harder. Free channel from day 1, same pity, announced ≥ 14 days ahead on the Herald's Board, ≤ 1 new lord per 2 campaigns.
3. **Balance windows**: changes land only on Truce day 1, posted ≥ 14 days before (liveops.md); ≤ 2 lords per window; no change under 2 cTS (no churn).
4. **Investment return on a nerf** (a lord's or a set's strength lowered by ≥ 2 cTS or ≥ 10% of its share): (a) up to 100% of the Seals spent on that lord move once to a lord of the player's choice within 14 days; (b) talent reset (already free); (c) free refit of that set's pieces for 14 days; (d) a mail with the changed numbers (mail-forge). Buffs return nothing.
5. **No abandoned lord**: top-2 in no scenario for 2 windows running → reworked in the next one.
6. **No stat outside the ladder**: events never grant permanent strength ("+5% event gear" is banned; liveops.md: no season-only power).

| Fails when | Caught by |
|---|---|
| A new lord beats the best existing lord in its own best scenario | [ ] lord_balance_probe on the release candidate |
| A nerf ships without the Seal transfer open | [ ] release checklist (ship-forge): transfer flag on |

## 13. The visual promise (commander-forge delivers; this file promises)

| Design state | What the player and others see | Built by |
|---|---|---|
| Unsworn | portrait in shadow in the hall, with its channel line ("Swears at the alliance hall — day 2 of 3"); never a padlock glyph over a face | commander-forge + ui-forge |
| Sworn | the shipped gilt rim light, upper left — never a colour-coded aura | commander-forge (portrait lane) |
| Rank | portrait frame metal per §3 | ui-forge + commander-forge |
| Gear | the hall figure wears EACH equipped piece at its finish; rune light 0 / 0.7 / 1.5 / 2.6; light, never particles | commander-forge (figure lane; kit via blender-forge) |
| Own set, 4 pieces | the lord "in harness"; the set's name in reports | commander-forge + report-forge |
| Oath | the lord's SKL emblem; a gilt edge on the march banner | game-art-director + commander-forge |
| Order | one beat, one Order on screen at a time; status on a lord is LIGHT (effects.md) | battle-forge |
| Map | banner + line icon + small squad token; the rim when Sworn | commander-forge (map lane), world-forge |

1. ART SHOWN BIG: portrait ≥ 30% of screen height on the lord's own screen; the pick and the swearing follow onboarding.md (≥ 30% / ≥ 60%).
2. Each lord card shows ONE next goal with its distance ("Fine rank: 34/40 Seals"); the hall icon carries at most one badge, only when a step is affordable now ([ux.md](ux.md) red-dot budget).
3. A lord whose portrait `art_status` is `stand_in` (Faber and Fable today) is never the featured lord of an event or of a paid surface until its painted batch is installed.
4. Money-law: any lord offer shows the lord at peace (portrait, hall, workshop), never battle.

## 14. Data, save, server cost, harness

- **Data** (paths to confirm): lords (role, line, skills, branches), talents (12 branches), `data/equipment.gd` (sets, finishes), summons (odds, pity); tuning in `design/lords/tuning.json`.
- **Save**: per lord `level, xp, xp_banked, rank, skill[4], talent_pages[3]`; per piece `id, finish, worn_by`; account `seals{lord}, plain, favoured, pity_count, drills_t0, presets[5]`. **Migration**: owned lords → Sworn; a level above the new rank cap raises the RANK (a level is never lowered); duplicates held convert at 10 Seals each; talents reset free.
- **Writes per player per day ≤ 8** (Summons claim with pity 1–3, Seal spends 2, gear 2, talents 1); camp XP and the hunt tally ride on the camp resolution write; drills on hall open. 50,000 × 8 = 400,000 writes/day — cost it with `core/sd_cost_probe.gd` against the €200 budget.
- **Harness** (new ones via qa-forge; names are proposals):
  - `lord_balance_probe` (headless, the frozen resolver; the cap itself is the combat probe's STACK check): 8 lords, 56 ordered pairs, 8 scenarios — S1 field attack, S2 field defence, S3 castle assault, S4 garrison, S5 rally lead on a stronghold, S6 short fight ≤ 8 rounds, S7 long fight ≥ 30 rounds, S8 camp hunt. Verdict: `LORD BALANCE OK - 8 lords, 56 pairs, 8 scenarios, max pair 0.49 TS <= 0.50, every lord top-2 in >=1 scenario, 0 faults`.
  - `seal_path` (design tool, `design/lords/`): the §11 income model; prints days per rank for free and heavy, the §6 timeline, Seal waste and heavy ÷ free.
  - `summons_probe`: served vs shown odds; pity bound. `ux_flow_probe`: hall → rank up, skill, talent, equip ≤ 3 taps each.
- **After ship**: primary share per lord 5–30%; ≥ 60% field pairs; ≤ 10% of players hold > 3 unspent talent points; D30 of players with one Masterwork-complete lord vs without.

## 15. Exploits

| Abuse | Answer |
|---|---|
| Farm accounts feeding Seals, XP or pieces | all account-bound, no trade; the alliance store uses Merit earned by own actions |
| XP feeding through PvP with alts | PvP gives no lord XP (§4) |
| Bots hunting camps for the tally | bounded by Resolve: ≤ 2.4 Seals per day (core-loop §3) |
| Buy, spend, refund (if paid Seals exist) | refunded Seals clawed back to a negative balance (monetization.md) |
| Respec per target to dodge counters | allowed (it is play); locked while marching (§7) |
| Stacking drum denial on one target | caps in §5: ≤ 300 per 8 rounds, gain ≤ −15% |
| Switching the Favoured lord to reset pity | pity counts draws, not lords |

## 16. Review checklist (a lord spec, before handoff)

1. [ ] Each lord has a one-line role and is top-2 in ≥ 1 harness scenario.
2. [ ] Maxed pair ≤ 0.50 TS (combat probe STACK); rank ceilings shown; no counter field in lord data.
3. [ ] Every L5 Order ≈ 0.35 round; a primary fires 2–4 Orders in a median battle; one Order beat per round.
4. [ ] Talents: ≤ 3 branches, 34 points, ≤ 1 capstone, free reset outside marches.
5. [ ] Seal costs, odds, pity and the free path shown in game, one tap from the Summons board.
6. [ ] Free: all 8 sworn ≤ day 28; first lord complete ≤ day 35; lord pool within the §6 timeline; heavy ÷ free ≤ 2.0.
7. [ ] No lord, set or Order on a paid-only channel; paid lord goods (if any) deterministic and capped.
8. [ ] A nerf opens the Seal transfer and free refit, and mails the numbers.
9. [ ] Every §13 visual state exists for every lord (commander-forge sign-off).
10. [ ] Save migration named; writes per day costed with sd_cost_probe.

## 17. Owner decisions required

1. **No rarity on lords** — the four tiers become the lord's rank. If lords ship with a rarity: keep or migrate?
2. **Paid lord goods**: none (monetization.md's recommendation), or named Seals + XP tomes only, ≤ 35 Seals + 5,040 XP per week (heavy ≈ 1.5× free). Never random draws.
3. **Set ownership**: the six field lords own the six sets; Faber and Fable none — confirm in `data/equipment.gd`.
4. **"Sworn" = the lord has joined you** (onboarding.md uses it so). If the shipped trigger means more, it wins.
5. **Rank ceilings on lord strength** (0.06 / 0.12 / 0.25 / 0.50 TS) and lords taking most of combat.md's early stack (§6) — touches balance; sacred constants win any conflict.
6. **Seal transfer on nerfs** (100%, once, 14 days) — a live-ops cost the owner accepts or trims.
