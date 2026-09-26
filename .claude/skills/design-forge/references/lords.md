# Lords — roles, ranks, Orders, talents, pairs, sets, Seals

How the eight lords (commanders) work as a system: what each one is for, how they grow, how two
of them share a march, what their four-piece sets do, how duplicates become an upgrade currency
with published math, how every lord is reached without paying, and how we stop power creep.
Implementation: **gameplay-forge** (rules, data, save, resolver hooks), **commander-forge** (the
lords end to end: portrait, hall figure, kit, map token, lord screens — it follows THIS file for
rules and numbers), **battle-forge** (Order beats), **report-forge** (why you won), **story-forge**
(voices, names), **ui-forge** (lord hall), **qa-forge** (harness). Genre facts: [benchmark.md](benchmark.md).

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Check the shipped data
first (`data/equipment.gd` exists; lord and talent data: path to confirm). A shipped sacred
balance constant keeps its value and this file's value becomes a proposal to the owner.
Units: **E** = one E-point (§6); `R_med` = rounds in a median field battle (combat.md sets it;
the examples use **R_med = 24**, verify against the frozen resolver).

## 0. The four questions

- **Want**: a lord who wins the fight you care about; the next rank, the next skill level, the
  next set piece; the whole hall of eight sworn.
- **Obstacle**: lord XP (time: camp hunts), Seals (duplicates, from play), set pieces (iron and
  Armoury time), talent choices (34 points for 60 slots — you cannot take everything).
- **Wait (free player)**: first lord sworn at minute 2; three lords by day 7; all eight by
  day 24–28; the first lord at Masterwork rank with every skill at 5 by day 32 and level 50 by
  day 57; all eight complete by day 213. Heavy spender: 19 / 40 / 139 days (§11).
- **Witness**: the gilt rim of a Sworn lord on the map token; the hall figure wearing the real
  kit; the set's name in battle reports; the lord's sigil on the march banner.

## 1. Genre pattern → where it hurts → our move

| Genre does | Where it hurts players | Our move (section) |
|---|---|---|
| 4 commander rarities; low ones become fodder by week 2 | the roster shrinks to a few "real" commanders | no rarity on lords; the four tiers are the lord's RANK (§3) |
| stars raise the level cap by 10 per star, level cap 60 | fine as a gate | kept as a pattern: rank caps level 20/30/40/50 (§4) |
| 4 skills, levels 1–5, a capstone when all are maxed | ~690 duplicate tokens per top commander; no pity found | 4 skills, 260 Seals to max, hard pity 20 (§5, §10) |
| rage meter: ~100 per attack, first cast ≈ round 11 [community estimate] | rage above the cap is wasted | the war drum: fixed gain per round, first Order at R_med/3, nothing wasted (§5) |
| 3 of 15 talent trees, up to 74 points | newcomers cannot read the tree | 3 branches × 8 nodes, 34 points, one capstone (§7) |
| primary + secondary; only the primary's talents and gear apply | good: squares build space without doubling content | kept; the secondary gives its Order and first passive only (§8) |
| a counter of +5% damage under stacks of talent and gear bonuses | "PvP is raw power, not tactics" | the lord budget stays BELOW one counter; no lord source changes a counter (§6) |
| exclusive commanders in paid bundles; winner-take-most token races | "stuck" after missing one commander | every lord has a free channel; milestone rewards only (§11) |
| new top commanders each season; old talent trees reworked | investment wiped out | fixed ceiling, sidegrade rule, Seal transfer on every nerf (§12) |

## 2. The eight lords — roles (PROPOSAL, derived from portraits.md)

A **role** is the question a lord answers best. Every lord leads a line or a situation; no lord
is "the strongest". Scenario ids refer to the balance harness (§14).

| Lord | Portrait cue (portraits.md) | Role | Line | Talent branches (§7) | Set (§9) | Best scenario |
|---|---|---|---|---|---|---|
| Edwin | older, grey temples, crimson mantle (shipped anchor) | holds the front | infantry | Shieldwall · Garrison · Hunt | Edwin's | S2 field defence |
| Alric | "wins quickly or not at all", wolf-pelt | shock: wins in the first rounds, fades | any (cavalry, infantry) | Assault · Charge · Road | Alric's | S6 short fight |
| Elena | archer-commander, dark braid, green hood | strikes first, from range | archers | Longshot · Garrison · Hunt | Elena's | S1 field attack |
| Rowan | young cavalier, plume, kite shield | speed and interception | cavalry | Charge · Road · Hunt | Rowan's | S6 / S8 camp hunt |
| Godric | siege master, stylus, bronze instruments | breaks walls; engines | crossbows + siege | Windlass · Siegecraft · Road | Godric's | S3 castle assault |
| Maud | stern matron in black, tower shield | defence and the wall | spearmen | Pike Hedge · Garrison · Shieldwall | Maud's | S4 garrison |
| Faber | the King's Armourer, apron over mail | makes the primary's gear count | support | Armoury · Shieldwall · Hunt | none (PROPOSAL) | best secondary for a geared primary |
| Fable | the Chronicler, chained ledger | knowledge: XP, reports, drum denial | support | Chronicle · Road · Hunt | none (PROPOSAL) | S7 long fight; best secondary for levelling |

Rules. (1) Each lord is top-2 (as primary or secondary) in at least one of the 8 harness
scenarios, or it is buffed in the next balance window. (2) No lord is top-1 in more than 2
scenarios. (3) A lord's role is visible in one line on its card ("Holds the front. Infantry.").
(4) Lords never die, are never captured and never lose XP; a beaten march brings its lords home.

| Fails when | Caught by |
|---|---|
| A lord is top-2 in no scenario (a lord nobody fields) | [ ] lord_balance_probe: `every lord top-2 in >=1 scenario` |
| One lord leads > 30% of all primary slots at day 30+ | [ ] telemetry: primary share per lord ≤ 30%, each ≥ 5% |

## 3. Rarity — one four-tier ladder, three uses

The game has FOUR tiers: **Issued → Sound → Fine → Masterwork** (never five). Lords have NO
rarity of their own: with eight hand-painted lords, a low-rarity lord is a lord the player
stops using — that breaks pillar 6 ("each lord has a role, a path, and a reason to be fielded").

| Use | Issued | Sound | Fine | Masterwork |
|---|---|---|---|---|
| Lord RANK: level cap | 20 | 30 | 40 | 50 |
| Lord RANK: skill level cap | 2 | 3 | 4 | 5 (+ Oath) |
| Gear FINISH: stat per piece | 0.40 E | 0.65 E | 0.90 E | 1.25 E |
| Gear FINISH: rune light (blender-forge RUNE_ENERGY) | 0 | 0.7 | 1.5 | 2.6 |
| Portrait FRAME metal (equipment.md register) | plain field metal | clean steel, one bronze fitting | etched lines, gilt border | gold inlay, one set gem |

A lord arrives at Issued rank when sworn. If the shipped data already gives lords a rarity,
this is an owner decision (§17), not a silent change.

## 4. Levels and XP

- **XP unit = one minute of standard play** for a focused lord. Standard play = 24 camp kills a
  day (core-loop Resolve: 240 per day ÷ 10). **A camp kill at or above the recommended level =
  60 XP to EACH lord in the march** (below it: 30). So a standard day = 1,440 XP.
- Tomes (in-world: **field journals**) are priced in the same minutes: 60 / 480 / 1,440 XP
  (1 h / 8 h / 24 h), like speed-ups in numbers.md §7. The daily 100-point chest (core-loop §7)
  gives 240 XP. Free focus lord: 1,680 XP per day.
- **Curve**: `python tools/curve.py --levels 49 --first 3m --last 7d --shape phased`; each row's
  duration in minutes = the XP of that step (row L = level L → L+1).

| Reach level | XP of the step in | Cumulative XP | Free focus lord reaches it | What the level grants |
|---|---|---|---|---|
| 2 | 3 | 3 | first battle | +0.04% damage, +0.04% defence (every level) |
| 10 | 21 | 86 | first hour | talents open, 9 points waiting (guided moment, onboarding.md §7) |
| 20 | 182 | 996 | day 1 | Issued cap; 19th talent point |
| 30 | 833 | 5,608 | day 3.3 | Sound cap |
| 36 | 2,073 | 14,404 | day 8.6 | 26th talent point |
| 40 | 3,809 | 26,710 | day 15.9 | Fine cap |
| 45 | 6,388 | 53,544 | day 31.9 | — |
| 50 | 10,080 | 95,888 | day 57.1 | Masterwork cap; 34th talent point |

1. **XP at a cap is banked, never lost**; it applies the moment the rank rises.
2. **Hall drills (catch-up)**: a lord who is in no march gains 25% of the XP the fielded lords
   earn, up to (highest lord level − 5). Credited when the hall opens: one write, not one per kill.
3. XP comes from PvE, rallies on camps and strongholds, tomes and chests. **PvP kills give no lord
   XP** (no feeding XP through farm accounts).
4. Level stats are small on purpose (+2% damage, +2% defence at L50 = 4 E): levels gate the ranks
   and talents; they are not the power.

| Fails when | Caught by |
|---|---|
| XP is lost at a cap, or a benched lord falls > 10 levels behind the top lord | [ ] seal_path sim: banked XP 100%; drills gap ≤ 5 levels |
| A free focus lord reaches L50 before day 45 or after day 70 | [ ] seal_path sim, free profile |

## 5. Skills — four per lord; Orders on the war drum

| Skill | Unlocks | Levels | Acts when the lord is | Budget at L5 |
|---|---|---|---|---|
| **Order** (active) | sworn | 1–5 | primary or secondary | 4.5 E primary / 2.5 E secondary |
| **Passive I** (the line or role) | sworn | 1–5 | primary or secondary | 1.5 E |
| **Passive II** (a situation) | Sound rank | 1–5 | primary only | 1.0 E |
| **Oath** (capstone) | Masterwork rank + the other three at 5 | one level | primary only | 1.0 E |

Skill value by level: L1 60%, L2 70%, L3 80%, L4 90%, L5 100% of the L5 value.

**The war drum (the tempo meter)**. Each lord in a march has a drum of 1,000. The primary's
drum gains `1000 ÷ (R_med / 3)` per round (125 at R_med 24: Orders at rounds 8, 16, 24); the
secondary's drum gains half (one Order at round 16). At 1,000 the lord gives its Order (one
battle beat) and the drum resets to 0; gains are fixed per round, so nothing overflows. Effects
that add to a drum carry any remainder past 1,000 to the next fill. The report shows "Next
Order in 3 rounds", never a raw drum number.
- **Order unit**: every Order at L5 is worth about **0.35 of one normal round** of the whole
  march (a strike of 35%, or −15% damage taken for 2 rounds, or the same in another form).
  The harness tunes the value, never the cadence.
- **Drum denial cap**: all enemy effects together remove ≤ 300 drum per 8 rounds and slow the
  gain by ≤ 15%. Drum start bonuses cap at 50%.

**The eight kits (L5 values, PROPOSAL)**

| Lord | Order | Passive I | Passive II | Oath |
|---|---|---|---|---|
| Edwin | Close the Ranks: damage taken −15% for 2 rounds | Old Soldier: infantry +3% defence | Hold Fast: below 50% troops, +5% damage | The Crimson Line: Close the Ranks lasts 3 rounds |
| Alric | Wolf's Rush: strike 0.35 round; ×1.6 before round 6 | First Blood: +8% damage rounds 1–5; −4% from round 13 | Pack Hunter: +5% damage vs a target already engaged by another march | No Second Charge: drum starts at 50% |
| Elena | Loose!: volley 0.35 round; +30% if ≥ 50% of the march are archers | Green Hood: archers +3% damage | High Ground: defending a castle or held tile, archers +4% damage | First Light: a free volley of 0.2 round before round 1 |
| Rowan | Break Them: charge 0.30 round; target's drum −100 | Plume and Kite: cavalry +3% damage | Outrider: march speed +8% (utility) | Spur: Break Them removes 200 drum |
| Godric | Measured Shot: strike 0.30 round; ×2 vs walls, gates, towers | Stylus and Rule: structure damage +8% (utility) | Windlass Drill: crossbows +3% damage | Engine Master: siege engines assemble 15% faster (siege-forge) |
| Maud | Tower Shield: damage taken −12% for 2 rounds (−18% defending her castle) | Brace: spearmen +3% defence | Mistress of the Wall: as garrison lord, wall durability loss −8%, 8 points of dead become severely wounded | Black Vigil: defending the castle, drum starts at 50% |
| Faber | Field Forge: 1.5% of the march's troops return from lightly wounded to the fight | Armourer's Eye: the PRIMARY's gear-piece stats +20% | Spare Rivets: below 50% troops, damage taken −3% | The King's Armourer: the primary's pieces count one finish higher (Masterwork stays) |
| Fable | Set It Down: enemy primary's drum −250 + strike 0.15 round | The Ledger: both lords +20% XP; the report shows the enemy's full lord breakdown | Old Roads: enemy drum gain −10% | Foretold: Set It Down also fires once at battle start |

Names are working names for story-forge. **No skill, talent or set bonus reads "+X% versus
<line>"**: counters belong to combat.md alone (§6).

| Fails when | Caught by |
|---|---|
| An Order never fires in a median battle, or fires > 4 times | [ ] lord_balance_probe: Orders per S1 battle, primary 2–4 |
| Two Order beats land in the same round (unreadable) | [ ] resolver rule: a secondary Order due with the primary's waits 1 round |
| Any lord data field modifies a counter | [ ] grep lord/talent/set data for `vs_line` fields = 0 |

## 6. The lord budget — lords can pull even with a counter, never flip it

**E-point (measured, not guessed)**: in the resolver mirror test, march A carries the lords and
march B the same troops with no lords; E = the % of extra troops B needs to end the fight even.

| Source (maxed pair: primary Masterwork L50 + secondary) | Max E |
|---|---|
| Primary level (L50) | 4 |
| Primary talents (34 points) | 8 |
| Primary gear (4 Masterwork pieces 5 + set bonuses 1) | 6 |
| Primary skills (Order 4.5, Passive I 1.5, Passive II 1, Oath 1) | 8 |
| Secondary skills (Order 2.5, Passive I 1.5) | 4 |
| **Total — the cap for a maxed pair** | **30** |

1. **The counter rule**: the lord cap is ≤ 0.85 × E of one clean counter measured in the same
   test (combat.md sets the counter; a counter worth 35 E allows 30). A maxed pair on the wrong
   side of a counter against an un-invested pair on the right side, same tier and troops, ends
   about even. Counters decide equal fights; lords decide equal counters.
2. Lord bonuses stack additively inside the lord category and multiply with other categories
   (numbers.md §9). One rally or garrison side counts ONE pair: the leader's.
3. **Utility effects are outside E but capped** (lords' total): march speed ≤ +15%; structure
   damage ≤ +20%; dead → wounded shift ≤ 10 points; XP ≤ +35%; engine assembly ≤ −25%.
4. Lord power (numbers.md §3) is proportional to the lord's E, on the same scale as troop power.

| Fails when | Caught by |
|---|---|
| A maxed pair measures > 30 E, or > 0.85 × a clean counter | [ ] lord_balance_probe: `max pair E <= 30, counter E` printed |
| A utility total exceeds its cap with every source stacked | [ ] data audit sums the worst stack per cap |

## 7. Talents — three branches, 34 points, one capstone

- **Points**: 1 per level from 2 to 20, then 1 per even level from 22 to 50 = **34**. Talents
  open at L10. Same for every lord.
- **A branch = 8 nodes, 20 points**: 6 minor nodes × 3 ranks (18) + a keystone (1 point, needs 8
  in the branch) + a capstone (1 point, needs 18 in the branch). 3 branches = 60 slots.
- 34 of 60 means a real choice: one full branch (capstone) + 14 in a second (keystone), or three
  keystones and no capstone. **At most one capstone per lord.**
- Minor rank ≈ 0.2 E (e.g. +0.5% on one line's damage per rank). Branch template, Shieldwall:
  row 1 infantry damage, infantry defence; row 2 damage taken below 50% troops, Order strength;
  row 3 garrison defence, march speed; keystone; capstone.
- **Pages and resets**: 2 pages per lord (field, wall), a 3rd at Fine. Reset and page switch are
  **free, always** (not only to day 14, as onboarding.md promised as a floor), but locked while
  the lord is marching or garrisoning a castle under attack. Never sold.

| Branch (kind) | Keystone | Capstone |
|---|---|---|
| Shieldwall (infantry) | Locked Shields: march ≥ 50% infantry → damage taken −3% | Unbroken: once, when troops fall below 40%, damage taken −20% for 2 rounds |
| Pike Hedge (spearmen) | Set Pikes: spearmen +3% defence rounds 1–3 | Hedge: attackers hitting spearmen take back 5% of that damage |
| Longshot (archers) | Range: march ≥ 50% archers → archers +3% damage | Second Volley: every Order adds an archer strike of 0.1 round |
| Windlass (crossbows) | Heavy Bolts: crossbows ignore 3% of defence | Pavise Line: crossbows take −8% damage rounds 1–4 |
| Charge (cavalry) | Couched Lance: cavalry +4% damage rounds 1–3 | Run Down: +6% damage vs marches below 50% troops |
| Garrison (role) | Walls: as castle garrison, damage taken −3% | Last Gate: garrison dead → wounded +5 points (utility) |
| Assault (role) | Opening: +4% damage rounds 1–5 | Drum Roll: drum starts at 20% |
| Siegecraft (role) | Sappers: structure damage +6% (utility) | Breach: gate damage +10%, engine assembly −10% (utility) |
| Armoury (role) | Well Kept: this lord's gear stats +8% | Three-Piece Harness: a set's 4-piece bonus works with 3 of its pieces |
| Chronicle (role) | Notes: both lords +10% XP (utility) | Foresight: the enemy primary's drum starts at −250 |
| Hunt (utility) | Tracker: +8% damage vs camps and AI-lord hosts | Clean Kill: −20% losses vs camps |
| Road (utility) | Marching Order: march speed +5% | Forced March: return trips +20% speed, gathering load +10% |

12 branch kinds written once, used in 24 slots (§2 table). The tree is readable in one screen: 3
columns, 4 rows, keystone and capstone drawn as larger nodes; "recommended for the role" path lit.

| Fails when | Caught by |
|---|---|
| A new player cannot say what a branch does | [ ] each node = one line, ≤ 60 characters (l10n-forge) |
| One branch is in > 60% of builds for its lord at day 30 | [ ] telemetry per lord; rework the losing branches |

## 8. Pairing — primary and secondary

1. A march has one **primary** and may add one **secondary**. A lord is in one march at a time.
2. **Primary**: level stats, all four skills, talents, gear, set bonuses.
3. **Secondary**: its Order (on the half-speed drum) and its Passive I, at its own skill levels.
   Nothing else — its gear, talents, Passive II and Oath do nothing (shown greyed "primary only").
4. A secondary slot opens with the second sworn lord (onboarding.md day 4, "The Lord's Road").
5. Adding a secondary never removes anything: a solo primary fires the same Orders.
6. Presets: up to 5 saved pairs (one per march banner) with their talent page (core-loop §8.2).
7. Both lords earn full march XP. The garrison pair is the pair set on the wall; if it is away,
   the highest-level idle lord defends alone.

| Fails when | Caught by |
|---|---|
| The best pair beats the median pair of its scenario by > 6 E | [ ] lord_balance_probe: 56 ordered pairs × 8 scenarios |
| Players do not field pairs | [ ] onboarding.md lesson metric: ≥ 60% field a pair |

## 9. Kits — the six four-piece sets

Canonical: 24 items = 6 four-piece sets, one per lord (equipment.md; game-director lessons #6).
Slots: **weapon, armour, helm, token**. The mapping below is a PROPOSAL built from the portrait
cues; `data/equipment.gd` is the truth and commander-forge's kit sheet must match it.

| Set | Weapon | Armour | Helm | Token | 2 pieces | 4 pieces |
|---|---|---|---|---|---|---|
| Edwin's | Arming Sword | Oathplate | Crown Helm | War Standard | infantry damage taken −2% | Last Stand: below 50% troops, damage taken −4% |
| Alric's | Greatsword | Mail Hauberk | Nasal Helm | Wolf-fur Cloak | +3% damage rounds 1–5 | drum starts at 25% |
| Elena's | War Bow | Gambeson | Archer's Hood | Signet Ring | archers +2% damage | Order strikes +15% |
| Rowan's | Lance | Cuirass | Great Helm | War Horn | march speed +5% (utility) | round 1: cavalry +8% damage |
| Godric's | Engineer's Warhammer | Brigandine | Kettle Helm | Engineer's Rule | structure damage +5% (utility) | siege engine load +10% (utility) |
| Maud's | Tower Pike | Full Plate | Bascinet | Reliquary | spearmen +2% defence | as garrison: wall durability loss −6% (utility) |

1. **Any lord may wear any piece**; only the primary's pieces act. Two 2-piece bonuses of two
   sets both apply (2 + 2). A set on its own lord adds NO stat — only the look (§13).
2. **Faber and Fable have no set** (8 lords, 6 sets): their kits are the Armoury and the Chronicle.
   Verify in `data/equipment.gd` which lord each set names.
3. **Making a piece** (the Armoury anvil — a plate in core-loop §2): swearing a lord unlocks that
   set's 4 patterns. Craft at Issued (30 m), temper to Sound (4 h), Fine (16 h), Masterwork (48 h);
   help and free finish apply. Fine and Masterwork tempering open when Faber is sworn.
   Costs: iron + whetstones (camps) + gold leaf (Fine and up; events, alliance store) — amounts
   in [economy.md](economy.md), sized so one Masterwork temper ≈ 3 days of a free player's iron
   income at that stage. A piece may be made again (copies for more marches).
4. **Refit**: turn a piece into another piece of the same slot and finish for 20% of its temper
   materials. Free for 14 days after any rebalance of that set (§12).
5. A set on one lord with all four at Masterwork "has a name": the set's name shows in the
   report header. No stat.

| Fails when | Caught by |
|---|---|
| One set is on > 50% of primaries at day 30 | [ ] telemetry set share; rework window (§12) |
| A piece's `desc` names something the art does not show | [ ] commander-forge kit check (reference-forge analysis) |

## 10. Seals — duplicates become currency, with published math

- **Lord's Seals** (wax seals of one lord's house): 10 swear the lord; a duplicate lord = 10 Seals.
- **Plain Seals**: act as any lord's Seals, 1:1. Seals of a lord at full Masterwork turn into
  Plain Seals 1:1 automatically — no Seal is ever wasted.

| Step | Seals | Cumulative (rank + skills to that rank's cap) |
|---|---|---|
| Swear (Issued) | 10 | Issued complete: 22 (skills to 2: 3 × 4) |
| Issued → Sound | 20 | Sound complete: 66 (skills to 3: 3 × 8) |
| Sound → Fine | 40 | Fine complete: 142 (skills to 4: 3 × 12) |
| Fine → Masterwork | 70 | Masterwork complete: **260** (skills to 5: 3 × 16) |
| Skill level 2 / 3 / 4 / 5 (Order, Passive I, Passive II) | 4 / 8 / 12 / 16 | 120 of the 260 |
| Oath | 0 | unlocks by condition |

**The Herald's Summons** (random draw; free: 1 per day, banked up to 3). The odds, the pity
counter and this table are one tap from the Summons board:

| Result | Chance |
|---|---|
| 1 Seal | 55% |
| 2 Seals | 25% |
| 5 Seals | 15% |
| 10 Seals (or the lord, if not yet sworn) | 5% |

1. **Favoured lord**: the player names one lord; each result goes to the Favoured lord with 50%
   chance, else to one of the other 7 at random.
2. **Hard pity**: the 20th draw since the last 10-Seal result IS a 10-Seal result for the
   Favoured lord. The counter shows "10 Seals within 7 draws", never resets between events or
   seasons, and belongs to the account.
3. **Published math**: a 10-Seal result every 12.8 draws on average, never more than 20; 2.53
   Seals per draw (2.30 before pity); 1.41 per draw to the Favoured lord, 0.16 to each other.
4. **Paid Seals are never random** (PROPOSAL): the shop sells a named lord's Seals or Plain
   Seals, not draws — the money-law sells goods, and no paid loot box means no odds-law exposure
   ([monetization.md](monetization.md); shop-forge). Paid Seals + paid tomes cap: 35 Seals and
   5,040 XP per week.

| Fails when | Caught by |
|---|---|
| Shown odds differ from served odds | [ ] summons_probe: 100,000 draws within ±0.5 pp; pity at ≤ 20 always |
| A Seal is lost (a maxed lord, a full bank) | [ ] seal_path sim: waste = 0 |

## 11. Acquisition and the free path

| Lord | Free channel | Activity | Free day (target) |
|---|---|---|---|
| First of Edwin / Elena / Rowan | the identity pick (onboarding.md §3) | first session | minute 2 |
| Second of the three | chapter 4 chest (onboarding.md) | first week | day 4 |
| Third of the three | the 100th camp kill (hunt ladder) | PvE | day 7–9 |
| Maud | 3 days in one alliance + 30 helps given: she swears at the alliance hall | alliance | day 6–8 |
| Godric | the siege workshop built (progression.md; verify the building) | castle | day 8–10 |
| Faber | the first 4 pieces crafted at the Armoury | crafting | day 9–12 |
| Alric | the first AI-lord host defeated ([world.md](world.md)) | PvE / realm | day 12–18 |
| Fable | season track free step (story-forge chronicle chapter) | season (time) | day 20–28 |

Every lord also swears at 10 of its Seals (Favoured + pity: ≤ 20 free Summons). **No lord is ever
sold, exclusive to a bundle or first available on a paid surface — not even for 24 hours.**

**Seal income per day (steady state from day 8)**

| Source | Free | Goes to | Owning file |
|---|---|---|---|
| Herald's Summons, 1 per day | 2.53 | 1.41 Favoured, 0.16 each other | this file |
| Hunt tally: 1 Seal per 10 camp kills the lord leads (24 per day) | 2.4 | the leading lord | [core-loop.md](core-loop.md) Resolve |
| Weekly writ 500 chest: 5 Plain | 0.71 | any | core-loop.md §7 |
| Alliance store: 5 per week for personal credits | 0.71 | any | [alliance.md](alliance.md) |
| 2 milestone events a month: 20 featured + 10 Plain at full milestones | 2.0 | featured lord / any | [liveops.md](liveops.md) |
| Season track free: 60 Plain per 8 weeks | 1.07 | any | liveops.md |
| New-realm week (days 1–7 only): 30 Plain | 4.3 | any | onboarding.md |
| **Free total** | **9.4** | **7.0 to one chosen lord** | |
| Light spender (+ paid track and a small bundle) | +2.5 | any | monetization.md |
| Heavy spender (the weekly cap) | +5.0 | any | monetization.md |

**Free path per rank** (days; first lord = the focus, then the model moves focus lord by lord)

| Profile | First lord: Issued / Sound / Fine / Masterwork complete | First lord L50 | All 8 sworn | All 8 complete |
|---|---|---|---|---|
| Free | 2 / 6 / 15 / 32 | 57 | 24–28 | 213 |
| Light | 1 / 5 / 12 / 24 | 50 | 24–28 | 168 |
| Heavy | 1 / 4 / 9 / 19 | 40 | 24–28 | 139 |

Heavy ÷ free speed: 1.7× on the first lord's Seals, 1.4× on level 50, 1.5× on the whole hall.
**Rule: paid acceleration ≤ 2× the free rate on every lord path; paying never reaches anything
the free path does not.** Checkpoints (free): day 1 = 1 lord, L20; day 7 = 3 lords, focus at
Sound, L30 (XP banked); day 30 = 8 lords, focus at Fine complete, L44; day 90 = 2 lords complete.
Loss-free modes (liveops.md trial grounds) field every lord at one template (L40, Fine, Fine
gear, free talents) so there skill beats investment.

| Fails when | Caught by |
|---|---|
| Heavy ÷ free > 2.0 on any path, or a free lord path > 240 days | [ ] seal_path sim: `free 213 d, heavy/free 1.53` |
| An event ranks players for Seals (winner-take-most) | [ ] liveops calendar audit: Seal rewards are milestones only |

## 12. Power creep — the ceiling is fixed; new lords go sideways

1. **Fixed ceiling for the realm's life**: L50, Masterwork, 34 talent points, 4 skills, 4 gear
   slots, 30 E per pair. Raising any of it is an owner decision and lifts every lord at once
   with the materials to reach it.
2. **Sidegrade rule for a new lord**: its E in its best scenario ≤ the current best lord's E in
   that scenario; it must open a new question (a new scenario or situation) instead of answering
   an old one harder. Free channel from day 1; same pity; announced ≥ 14 days ahead in the
   calendar; ≤ 1 new lord per 2 seasons.
3. **Balance windows** at season breaks only; ≤ 2 lords changed per window; no change smaller
   than 3 E (no churn); announced 14 days ahead with the numbers.
4. **Investment return on a nerf** (any change that lowers a lord's E by > 5%, or a set's):
   (a) up to 100% of the Seals spent on that lord move once to one lord of the player's choice
   within 14 days; (b) talents reset free (already free); (c) refit of that set's pieces free
   for 14 days; (d) the mail says what changed in numbers (mail-forge). Buffs return nothing.
5. **No abandoned lord**: a lord top-2 in no scenario for 2 windows running is reworked next.
6. **No stat outside the ladder**: events never grant permanent E ("+5% event gear" is banned).

| Fails when | Caught by |
|---|---|
| A new lord beats the best existing lord in its own best scenario | [ ] lord_balance_probe on the release candidate |
| A nerf ships without the Seal transfer open | [ ] release checklist (ship-forge): transfer flag on |

## 13. The visual promise (commander-forge delivers; this file promises)

| Design state | What the player (and others) see | Built by |
|---|---|---|
| Unsworn | portrait in shadow in the hall, its channel line ("Swears at the alliance hall — day 2 of 3"); never a padlock glyph over a face | commander-forge + ui-forge |
| Sworn | the shipped gilt rim light, upper left — never a colour-coded aura | commander-forge (portrait lane) |
| Rank | portrait frame metal per §3 | ui-forge with commander-forge |
| Gear equipped | the hall figure wears EACH equipped piece at its finish; rune light 0 / 0.7 / 1.5 / 2.6; light, never particles | commander-forge (figure lane, blender-forge kit) |
| Own set, 4 pieces | the lord "in harness"; the set's name in reports | commander-forge + report-forge |
| Oath | the lord's SKL emblem; gilt edge on the march banner | game-art-director + commander-forge |
| Order in battle | one beat, one Order on screen at a time; status on a lord is LIGHT (effects.md law) | battle-forge |
| On the map | banner + line icon + small squad token, the rim when Sworn | commander-forge (map lane), world-forge |

1. ART SHOWN BIG: the lord card portrait ≥ 30% of screen height; the swearing ≥ 60% (onboarding.md).
2. A lord whose portrait `art_status` is `stand_in` (Faber, Fable today) is never the featured
   lord of an event or of a paid surface until its painted batch is installed.
3. Money-law: a paid Seal offer shows the lord at peace (portrait, hall, workshop), never a
   battle image over the buy button.

## 14. Data, save, server cost, harness

- **Data** (paths to confirm): lords (role, line, skills, branches), talents (12 branches),
  `data/equipment.gd` (sets, finishes), summons (odds, pity), tuning in `design/lords/tuning.json`.
- **Save per player**: per lord `level, xp, xp_banked, rank, skill[4], talent_pages[3], preset
  refs`; per piece `id, finish, worn_by`; account `seals{lord}, plain, favoured, pity_count,
  drills_t0`. Migration: owned lords → Sworn; a level above the new rank cap raises the RANK
  (never lowers a level); existing duplicates convert at 10 Seals; talents reset free.
- **Writes per player per day** ≤ 8 (summons claim with pity in the same write 1–3, Seal spends
  2, gear 2, talents 1). Camp XP and hunt tally ride on the camp resolution write; drills on hall
  open. 50,000 × 8 = 400,000 writes/day — cost it with `core/sd_cost_probe.gd`.
- **Harness** (new ones via qa-forge; names are proposals):
  - `lord_balance_probe` (headless, the frozen resolver): 8 lords, 56 ordered pairs, 8 scenarios
    S1 field attack, S2 field defence, S3 castle assault, S4 garrison, S5 rally lead on a
    stronghold, S6 short fight ≤ 8 rounds, S7 long fight ≥ 30 rounds, S8 camp hunt. Verdict:
    `LORD BALANCE OK - 8 lords, 56 pairs, 8 scenarios, max pair 29.4 E <= 30, counter 36 E, 0 faults`.
  - `seal_path` (design tool, `design/lords/`): the §11 model; prints days per rank for free,
    light and heavy, waste and heavy ÷ free.
  - `summons_probe`: served odds vs shown odds; pity bound.
  - `ux_flow_probe`: lord hall → rank up / skill / talent / equip ≤ 3 taps each.
- **After ship**: primary share per lord (5–30%), pairs fielded (≥ 60%), talent points unspent
  (≤ 10% of players hold > 3), D30 of players who reached one Masterwork lord.

## 15. Exploits

| Abuse | Answer |
|---|---|
| Farm accounts feeding Seals, XP or pieces | all are account-bound; no trade; alliance store uses personal credits earned by own actions |
| XP feeding through PvP with alts | PvP gives no lord XP (§4) |
| Bots hunting camps for the tally | bounded by Resolve: ≤ 2.4 Seals per day (core-loop §3) |
| Buy, spend, refund | refunded Seals clawed back to a negative balance ([monetization.md](monetization.md)) |
| Respec per target to dodge counters | allowed (it is play); locked while marching (§7) |
| Stacking drum denial on one target | denial cap §5: ≤ 300 per 8 rounds, gain ≤ −15% |
| Re-rolling the Favoured lord to reset pity | pity counts draws, not lords; changing Favoured keeps the count |

## 16. Review checklist (a lord spec, before handoff)

1. [ ] Each lord has a role in one line and is top-2 in ≥ 1 harness scenario.
2. [ ] Maxed pair ≤ 30 E and ≤ 0.85 × one counter; no `vs_line` field in lord data.
3. [ ] Every Order ≈ 0.35 round at L5; primary fires 2–4 times in a median battle.
4. [ ] Talents: ≤ 3 branches, 34 points, ≤ 1 capstone, free reset outside marches.
5. [ ] Seal costs, odds, pity and the free path table shown in-game, one tap from the board.
6. [ ] Free path: all 8 sworn ≤ day 28; first lord complete ≤ day 35; heavy ÷ free ≤ 2.0.
7. [ ] No lord, set or Order on a paid-only channel; paid Seals deterministic and capped.
8. [ ] Nerf → Seal transfer, free refit, numbers in the mail.
9. [ ] Visual states of §13 exist for every lord (commander-forge sign-off).
10. [ ] Save migration named; writes per day costed with sd_cost_probe.

## 17. Owner decisions required

1. **No rarity on lords** (the four tiers become the lord's rank). If lords ship with a rarity, keep or migrate?
2. **Paid Seals cap** 35 per week and 5,040 XP per week (heavy ≈ 1.5× free); and **no paid random draws**.
3. **Set ownership**: six field lords own the six sets; Faber and Fable none — confirm against `data/equipment.gd`.
4. **"Sworn" = the lord has joined you** (onboarding.md uses it so). If the shipped trigger means more, keep it.
5. **Lord budget 30 E ≤ 0.85 × a counter** — touches combat balance; sacred constants stay if they conflict.
6. **Seal transfer on nerfs** (100%, once, 14 days).
