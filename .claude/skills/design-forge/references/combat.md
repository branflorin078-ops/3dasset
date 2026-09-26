# Combat — the counter ring, tier-steps, losses that cost time, marches as functions of time

The RULES and NUMBERS of fighting. Owners: **gameplay-forge** (frozen resolver, troop data, save), **battle-forge** (the attack and defence experience, played from the resolver's beats), **siege-forge** (engines, inside the class limits of §4), **report-forge** (the "why", from the cause ledger of §12), **world-forge** (marches on the map), **cloud-forge** (march storage, arrival jobs), **qa-forge** (the combat probe, §14). Genre patterns: [benchmark.md](benchmark.md) §combat.

**Every number here is a PROPOSAL** unless it quotes a canonical fact. The counter table, tier stats and resolver constants may be sacred balance constants: measure the shipped game first (§14 step 0); where it differs, the shipped value stays and the gap goes to the owner (§15). Quoted, never redefined: banners (march slots), infirmary, war windows (≤ 60 min, two a day, 12 h apart), Resolve — [core-loop.md](core-loop.md); spine stages `S1–S6` and troop-tier bands — [progression.md](progression.md); the peace ward — [onboarding.md](onboarding.md) §4; lord pairing and skills — [lords.md](lords.md); plunder and protection — [economy.md](economy.md); visibility and relocation — [world.md](world.md).

## 0. The four questions

- **Want**: win the fight you chose, and know in one line WHY you won or lost.
- **Obstacle**: the enemy's composition (counters), tier, numbers, lord pair and walls.
- **Wait**: a war march 60–180 s; a battle 20–45 s at 1×; a lost war session heals in ≤ 8 h without speed-ups; a breached castle is out of the war for 8 h, not for good.
- **Witness**: march lines, the burning castle on the realm map, the shared report (report-forge), honour in the alliance feed.

## 1. The unit of account — tier-steps (TS)

Every advantage — a tier, a counter, a lord pair, walls, more troops — is measured in ONE unit, so it can be compared, capped and explained. **1 TS = the strength of one troop tier.**

Reference model (for tuning; the frozen resolver's shape wins and the probe measures it): per round a side deals damage `∝ q · N^α` ([numbers.md](numbers.md) §4), so strength is `S = q · N^(1+α)` (N troops, q = attack × HP × multipliers per troop); a fight draws when `S_A = S_B`. The draw condition holds for fights to the end and to a shared rout threshold, and to first order for fixed round counts judged by fraction lost.

| Symbol | Meaning | PROPOSAL | Measured by (§14) |
|---|---|---|---|
| α | mass exponent of the frozen resolver | 0.6 (0.5–0.8) | doubling test |
| r | draw ratio: t(n) troops per t(n+1) troop, same line, no modifiers | 1.40 | tier test |
| Q = r^(1+α) | quality step per tier (attack × HP per troop) | 1.71 (attack and HP ×1.31 each) | — |
| TS of a multiplier M; of a troop ratio x | `ln M / ln Q`; `ln x / ln r` | 2× troops = +2.06 TS | ablation |
| E-point ([lords.md](lords.md) §6: % extra troops for a draw) | `TS = ln(1 + E/100) / ln r` | 1 TS = 40 E; 30 E = 0.78 TS | mirror test |
| R_med | rounds in a median field battle (lords.md's Order cadence uses it) | 24 (verify) | median over the LOSS battery |

| TS | q multiplier | e.g. attack / damage taken | same as troops × |
|---|---|---|---|
| 0.25 | 1.14 | +7% / −7% | 1.09 |
| 0.50 | 1.31 | +14% / −13% | 1.18 |
| 1.00 | 1.71 | +31% / −24% | 1.40 |
| 2.00 | 2.94 | +71% / −42% | 1.96 |

Why this unit: any resolver can be measured in it (bisect the troop count until the fight draws); factors add in log space, so a battle's causes sum to its margin (§12); a player reads "worth one tier" without a formula. The tables below come from the reference model: per side and round, damage `K · N^α · mean attack`, split by attacker weight × target share × the pair's counter factor, losses = damage / HP. qa-forge keeps it beside the probe (path to confirm).

## 2. The five lines and the counter ring

**Spearmen → Cavalry → Crossbows → Archers → Infantry → Spearmen** ("→" = hunts). Said aloud: *the pike stops the horse, the horse rides down the bolt, the bolt beats the bow, the bow breaks the blade, the blade gets inside the pike.*

| Line (accent) | Hunts | Why (historical flavour, approximate) | Hunted by | The art must show ([units.md](../../game-art-director/references/units.md)) |
|---|---|---|---|---|
| Spearmen #8B8F95 | Cavalry | horses refuse a braced hedge of points 3–5.5 m long | Infantry | the long weapon, butt set, braced |
| Cavalry #C9A76A | Crossbows | a heavy crossbow spans in 10–30 s; a horse covers 100 m in about 8 s | Spearmen | speed: mane, cloak, lean |
| Crossbows #6D8AA8 | Archers | the pavise stops arrows; the bolt goes through padded cloth | Cavalry | the bolt being seated, the pavise |
| Archers #4F7A4A | Infantry | volleys fall on men who must cross open ground to reach them | Crossbows | the bow drawn |
| Infantry #B4432E | Spearmen | shield men step inside the point, where a long shaft cannot turn | Archers | shield and short blade |

1. **One hunt, one hunter** per line: 5 of the 10 pairings are counters, 5 are neutral. Five facts, one sentence, one ring icon (Blender-made, in the five accents — ui-forge; never a line glyph).
2. **A counter is worth exactly 1.0 TS** in a pure-line fight: t(n) hunters draw t(n+1) prey at equal count (`t(n) + counter ≈ t(n+1)`, numbers.md §4); against t(n+2) prey they lose by 1 TS.
3. **Two-sided, one dial**: the hunter deals `+c` damage to its prey and takes `c` less damage from it, so `(1+c)/(1−c) = Q` and `c = (Q−1)/(Q+1)`. Read c from the MEASURED α and r, never by feel. All values sit inside numbers.md's +20–50% band; a one-sided counter would need +57% to +107% for the same 1 TS.

   | α \ r | 1.35 | 1.40 | 1.50 |
   |---|---|---|---|
   | 0.5 | 22% | 25% | 30% |
   | 0.6 | 24% | **26%** | 31% |
   | 0.7 | 25% | 28% | 33% |
   | 0.8 | 26% | 29% | 35% |

4. **The counter is a constant**, the same for every player, shown as "worth one tier". No talent, gear, research, title, item or event changes c — a counter you can buy up is a spending stat. It is its own multiplicative category, never added into a bonus pool: +26% added to a pool already at +150% is worth 10%. The genre's 5% counter, invisible under stacks, is exactly this mistake.
5. **Cavalry t11** (Legendary Knight) is the one apex rung; Dragoon Pikemen (spearmen t10) at the brace draw it by rule 2. Any other 11th tier is an owner decision.
6. **Mixed marches dilute counters.** Matchup index `MI = Σ_i Σ_j sA_i · sB_j · C_ij` (s = troop share; C = +1 hunts, −1 hunted, 0 neutral). In the reference model the counter swing in TS equals MI within ±7%. Worked, t5, equal counts:

   | Ours ↓ / enemy → | even 5 × 20% | cavalry 60%, others 10% | crossbows 40, archers 40, infantry 20 |
   |---|---|---|---|
   | even 5 × 20% | 0.00 | +0.01 | +0.01 |
   | spearmen 60%, others 10% | −0.01 | +0.25 | −0.10 |
   | spearmen 100% | −0.02 | +0.47 | −0.21 |
   | cavalry 50, crossbows 30, infantry 20 | −0.01 | −0.15 | +0.24 |
   | cavalry 100% | −0.02 | −0.01 | +0.38 |

   Read it: an even split is safe and gains nothing; a scouted counter-pick gains +0.25 to +0.5 TS; a wrong guess costs as much. That is what scouting buys (§11), and why money-driven stat gaps are capped inside it (§5).
7. The send and rally screens show MI from the latest scout as "+0.4 tier" with the scout's age (battle-forge presents; the value comes from this rule).
8. **The ring is whole only when all five lines are open.** Until crossbows open, cavalry has no prey and archers no hunter. progression.md opens crossbows in Age III (engaged free: day 1–3), inside the 7-day peace ward, so no PvP runs on a broken ring; Age II camps ([world.md](world.md)) field ≤ 40% archers. Line halls teach the ring in this order: archers hunt infantry (Age I); spearmen stop cavalry, infantry get inside spearmen (Age II); crossbows beat archers, cavalry rides down crossbows (Age III).

Rejected: each line hunting two (10 relations, no single sentence); crossbows hunting cavalry "because bolts pierce armour" (with cavalry hunting crossbows it makes a mutual pair — no rule left); a pierce trait that ignores tier armour (breaks rule 2); a three-line triangle with spearmen and crossbows as sub-types (wastes two canonical lines).

| Fails when | Caught by |
|---|---|
| Any hunter pair is off 1.0 TS by > 0.1 (45 pairs t1–t9, plus spear t10 vs cav t11) | [ ] combat probe COUNTER |
| One line is < 10% or > 35% of all troops sent, weeks 2–8 | [ ] telemetry, line share per realm |
| "Counter" is the top cause in < 20% of lost PvP reports (counters invisible) | [ ] report cause telemetry (report-forge) |

## 3. Tiers, power, mass versus quality

Power per troop `p_t = 10 · r^(t−1)` — numbers.md §3 with `k = r`, so equal power means an even fight between neutral lines with equal stacks. Display names: units.md.

| Tier | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 (cav) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Power per troop | 10 | 14 | 20 | 27 | 38 | 54 | 75 | 105 | 148 | 207 | 289 |
| Quality q (× t1) | 1 | 1.71 | 2.94 | 5.03 | 8.6 | 14.8 | 25.3 | 43.3 | 74.2 | 127 | 218 |
| Cost per power (× t1) | 1.00 | 1.04 | 1.07 | 1.11 | 1.15 | 1.19 | 1.23 | 1.28 | 1.32 | 1.37 | 1.42 |

1. **Equal quality per tier across lines** (±5%). Lines differ in counters, speed and load, never in raw strength.
2. **Power is legible**: equal power, equal stacks, neutral lines → a draw within ±10%. Tooltip: "Power is exact only between neutral lines — counters, lords and walls move it; see the estimate."
3. **Quality buys slots, mass buys resources.** Banners, rally capacity, reinforcement caps and beds count TROOPS: a t10 fills one slot with 20.7× the power of a t1. Training cost per troop grows `g = 1.45` per tier (> r), so cost per power rises 3.6% per tier; training time per troop ∝ `p_t`, so a muster yard makes constant power per hour. A new tier is a capacity reward; a big low-tier army is cheap power for garrisons and rally fill.
4. **Doubling troops = +2.06 TS.** Mass matters; capacity caps keep it bounded.
5. **Promotion** t → t+1 (progression.md T2): pay the cost difference, time = the time difference, no fee — no investment is lost to a new tier.

| Line | March speed × | Load × | Its job in one line |
|---|---|---|---|
| Infantry | 1.0 | 1.0 | holds the front; hunts spearmen |
| Spearmen | 1.0 | 1.0 | stops cavalry |
| Archers | 1.0 | 0.8 | breaks infantry |
| Crossbows | 0.9 | 0.8 | beats archers |
| Cavalry | 1.5 | 0.6 | fastest march, interception; rides down crossbows |
| Engines (§4) | 0.6 | 4.0 | structures and load |

A march moves at its slowest line × (1 + speed pool, ≤ +50%) × terrain (world.md).

## 4. Siege engines — a line outside the ring

1. Engines are not a sixth line: no hunter, no prey. Against troops they deal ≤ 10% of what the same capacity of troops would. Their job is structures (walls and gate, alliance structures) and load.
2. Three classes; siege-forge sorts its catalogue into them and sets per-engine numbers inside these limits:

| Class | Catalogue examples (siege-forge) | Effect | When it lands |
|---|---|---|---|
| Breakers | counterweight and traction trebuchets, springald | wall durability damage | before the melee; 50% of it even on a lost assault |
| Breachers | ram under a roofed penthouse, mine | durability damage, 1.5× a breaker per capacity | only on a won assault |
| Scalers | ladders, belfry, mantlets and pavises | cut the structure bonus (§10) by up to 50% for this assault | during the assault |

3. Engines take ≤ 20% of a march's capacity; the escort is ≥ 80%.
4. Engines are hit only after the escort falls below 25%. A routed march loses its engines: 50% destroyed, 50% return damaged (repaired at the siege workshop — siege-forge). Engines never use beds.
5. Engine trains bring wagons: 4.0× load per capacity (plunder and gathering — economy.md).

## 5. Modifier stacks and the lord cap — stats never bury the counter

| Pool | What is in it | Max | q × at max |
|---|---|---|---|
| Counter | ring position (§2) — its own category, never modified | ±1.0 TS pure; MI in a mix | 1.71 |
| Lords | the maxed pair of [lords.md](lords.md) §6: primary level, talents, four-piece set, skills + the secondary's skills | 0.78 TS (30 E) | 1.52 |
| Realm | research, buildings, titles, alliance charters (+1.5% attack, defence, health ≈ 0.05 TS — [alliance.md](alliance.md)) | 0.30 TS | 1.18 |
| Temporary | earned items, event boosts, war-window buffs — never sold ([monetization.md](monetization.md)) | 0.15 TS | 1.08 |
| Structures (defender) | walls and towers, §10 | 0.50 TS × W/W_max | 1.31 |
| **All non-counter pools** | | **1.25 TS** | 1.96 |

1. Additive inside a pool, multiplicative across pools (numbers.md §9), clamped at resolve time. The clamps are entries in gameplay-forge's clamp ledger (names to confirm). Lord utilities (march speed, structure damage, dead → severe ≤ 10 points) sit outside E under lords.md §6 rule 3 caps.
2. **Visible caps**: the lord screen shows "Lord strength 0.62 / 0.78 tier"; a capped pool says "Capped". No investment silently does nothing.
3. **I1 — counter beats stack** (lords.md §6 rule 1 in TS): pure lines, equal tier and count, a counter army with NO lords beats the prey with a maxed pair, +1.0 − 0.78 = +0.22 TS; at the median free day-30 stack it beats the prey at the MAXIMUM stack, +1.0 − (1.23 − 0.60) = +0.37 TS.
4. **I2 — scouting answers money**: on the same day the heavy spender's lead over the median free player's main march is ≤ 0.30 TS — inside a scouted counter-pick (+0.25 to +0.5 TS).
5. **I3 — said honestly**: in MIXED marches a maxed pair against an unbuilt one (0.78) outweighs the composition swing (≤ 0.5); once both pairs are built, counters decide. The free focus pair is built by day ≈ 57 (lords.md §0), so this window is the first two months.

Stack targets, main march (TS, lords + realm; lords.md, progression.md, alliance.md and monetization.md land inside them):

| Day | Free (median) | Heavy | Heavy − free |
|---|---|---|---|
| 7 | 0.20 | 0.45 | 0.25 |
| 30 | 0.60 | 0.88 | 0.28 |
| 90 | 0.93 | 1.03 | 0.10 |
| 180 | 1.03 | 1.08 | 0.05 — money buys time to the cap, never a higher cap |

Free path (SKILL.md rule 6): lord cap by day ≈ 57 (lords.md), realm cap by day ≈ 240 (progression.md and alliance.md confirm with their curves); other marches' pairs follow lords.md's all-eight path (day 213).

| Fails when | Caught by |
|---|---|
| A maxed pair > 0.78 TS (30 E), or all pools > 1.25 TS | [ ] combat probe STACK (ablation) + lord_balance_probe |
| Heavy − free median > 0.30 TS at day 7, 30 or 90 | [ ] stack telemetry by cohort (gameplay-forge) |
| Any data row modifies c | [ ] grep of lord, research and item data for counter fields = 0 |

## 6. Losses — three buckets, by context

**Light**: walk home with the march, or rejoin the garrison right after the fight; free. **Severe**: go to the owner's infirmary beds at the moment of resolution; healed for resources and time. **Dead**: gone. The split applies to casualties (troops the resolver removed from the fight). Beds full → the row's overflow rule.

| # | Context | Light | Severe | Dead | Beds full → | Why |
|---|---|---|---|---|---|---|
| 1 | Camp hunt (PvE) | 90 | 10 | 0 | Light | the core loop never kills (onboarding.md §4) |
| 2 | Rally on a stronghold or AI-lord hold (PvE) | 60 | 40 | 0 | Light | alliance PvE costs only time |
| 3 | Defending your own castle | 30 | 70 | 0 | **Routed** | home never kills (rule 1) |
| 4 | Reinforcing an ally; defending an alliance structure | 25 | 60 | 15 | Dead | help costs a little |
| 5 | Field battle: march vs march, a gathering party hit, a campaign field camp ([liveops.md](liveops.md) §3.2) | 35 | 55 | 10 | Dead | map fights mostly recoverable |
| 6 | Attacking an alliance structure or landmark (war window) | 25 | 50 | 25 | Dead | objective war |
| 7 | Attacking a castle in a war window | 20 | 50 | 30 | Dead | aggression is a commitment |
| 8 | Attacking a castle outside war windows (if world.md allows it) | 10 | 30 | 60 | Dead | raids move into the fair windows |
| 9 | Tourneys and trial grounds ([liveops.md](liveops.md)) | 100 | 0 | 0 | — | loss-free standard modes |

1. **Home never kills.** Troops defending their own castle cannot die. Beds full → **Routed**: back free after 24 h (not speedable, not healable). A castle can be beaten, plundered and breached (§10), never zeroed — the genre's overflow at home is its main quit trigger ([benchmark.md](benchmark.md)).
2. **PvE never kills** (rows 1–2); a warded player's fights follow onboarding.md §4. Lord utilities may move ≤ 10 points of dead into severe (lords.md §6).
3. **Wounded in beds are safe**: never killed, never plundered.
4. **Overflow warning before every send**: expected severe = troops × the row's severe share; above free beds the send card says "May overflow your beds by ~6,500 — they would die" (icon + words, never colour alone; 0 extra taps).
5. **Honour** (the casualty tally in reports and the alliance feed) = Σ enemy (severe + dead) × power per troop (routed count 0), × the weak-target factor `clamp((P_def/P_att − 0.3)/0.3, 0, 1)` (0 below 30% of your power, full from 60%), × `0.5^(n−1)` for the n-th fight between the same two houses inside 24 h. Events score ground, never honour ([liveops.md](liveops.md) §3.4) — nothing pays for corpses.

Worked (row 5): a lost field march of 25,000 → 8,750 walk home, 13,750 to beds, 2,500 dead.

## 7. Infirmary sizing — defeat costs one night

| # | Rule | Number |
|---|---|---|
| H1 | Beds at stage S = β × C_march(S); C_march = the largest single march (gameplay-forge data) | β = 1.25 (1.0–1.5) |
| H2 | The worst normal day fits: max(lost field march 0.55; two lost window castle assaults 2 × 0.50; lost home defence of 1.25 marches × 0.70) × C_march | 1.00 ≤ 1.25 |
| H3 | Full beds of the stage's top tier heal with 0 speed-ups in | ≤ 8 h ([core-loop.md](core-loop.md) §2) |
| H4 | Healing full beds costs, in the median free player's own production at that stage | ≤ 24 h (economy.md checks) |
| H5 | Beds grow only from the infirmary tier and research (alliance charters included) — never sold (core-loop rule 1) | — |
| H6 | Heal cost per troop vs training (economy.md sets 30%); heal time per troop vs training | ≤ 40%; ≤ 25% |

Worked (C_march 25,000 at S4 is an EXAMPLE value): beds 31,000. A lost field march puts 13,750 in beds; two lost castle assaults 25,000; a lost home defence with 40,000 at home 28,000 — all fit. A third lost assault would add 12,500 to the 6,000 free: the §6 warning shows "~6,500" before that send. Heal time per top-tier troop ≤ 28,800 s / 31,000 = 0.93 s; lower tiers `∝ p_t`. Above 1.5 × C_march losses become free and fights weightless; below 1.0 × the genre's overflow spiral returns.

| Fails when | Caught by |
|---|---|
| Median losses of a lost war session take > 8 h to heal without speed-ups | [ ] war-session sim per S (qa-forge) |
| Overflow deaths hit > 5% of week-2 players | [ ] telemetry (onboarding.md, "Infirmary near full") |
| PvP sends drop > 30% for 3 days after a lost war session (fight avoidance) | [ ] cohort telemetry |

## 8. Marches — functions of time, resolved at arrival

Record (cloud-forge; sizes PROPOSED): `id u64 · owner u32 · kind u8 (gather, hunt, attack, rally, reinforce, scout) · target (tile u32 or object u64) · path ≤ 8 waypoints · depart u32 · arrive u32 · return_arrive u32 · speed fixed-point u16 · lords 2 × u8 · troops sparse (line, tier, count u32) · engines sparse · rally_id · state u8 · resolver_version u16` ≈ 60–140 bytes.

1. **Position is computed**: `pos(t) = path.point_at(clamp((t − depart)/(arrive − depart), 0, 1))` on client and server. No server tick moves a march.
2. **Writes only at events**: send 1; recall 1 (new path from `pos(now)`); arrival 1 outcome + 1 per participant. The way home lives in the same record (home when `now ≥ return_arrive`; 0 writes).
3. **Interception**: a march may target a moving march it can see (world.md owns visibility). The server solves the meeting point once per path segment (`|P + v·(t − t_s) − T(t)| = 0`, a quadratic, earliest root); a change to the target's path recomputes its pursuers (event-driven).
4. **Resolution at arrival**: a job scheduled at `arrive` (a timer queue, not a tick) reads both sides AS OF `arrive`, not as of the send: marches home by then defend; reinforcements arrived by then fight.
5. **Same-second order**: (arrive, depart, id); each resolution sees the state the previous one left.
6. **Determinism**: the resolver is a pure function (inputs, seed, resolver_version) → outcome + beats + cause ledger; seed = hash(march id, arrive); integer or fixed-point math only; `N^α` from a lookup table in data, no float `pow` at resolve. A stored battle keeps its resolver_version; a re-run under another version is refused.
7. **Latency**: result written ≤ 1 s p95 after `arrive`. The client plays the march to contact from its own clock and holds a clash loop until the result lands (battle-forge); after 5 s it retries and shows "Awaiting word". The client never resolves; it replays beats.

## 9. Rallies, garrisons, reinforcements

**Rallies** (ranks and scheduling: [alliance.md](alliance.md)):
1. The leader picks a target and a join window: 5 / 10 / 30 min against players; up to 60 min on PvE strongholds (scheduled rallies and pledges: alliance.md §8). Capacity = 4 × C_march when rallies open (progression.md; camp rallies are taught in week 1, onboarding.md), 6 × at S6; ≤ 15 joiners.
2. **One army, one command**: the leader's lord pair fights; joiners bring troops only. The report credits every joiner by name.
3. **Requested mix**: the leader may post a composition from the latest scout; joiners see the rally's live MI ("+0.3 tier") and join with a preset in ≤ 3 taps.
4. The rally leaves at window end with the marches that arrived; late marches turn home by themselves (0 taps, 0 cost). It moves at its slowest line. Cancel before departure: all go home, 0 cost.
5. Losses pro rata by troops given (per line and tier); severe go to each joiner's own beds under that joiner's overflow rule.
6. A march giving < 2% of rally capacity is not a participant (no reward share, no credit) — token joins cannot farm alliance.md's equal half. Reward splits: alliance.md §8 and liveops.md §4.2; honour by damage share. Joiners pay no Resolve (core-loop §3).

**Garrison**: defenders = troops at home (not in beds, not routed) + reinforcements + the structure bonus (§10). The owner sets the garrison lord pair; unset or away → the highest-level lords at home stand in — never a castle without a command. Assaults are fought in arrival order: light rejoin after each fight, severe go to beds, routed leave — repeated assaults meet a shrinking garrison, so reinforcements matter. No ward or shield can START while a hostile march targets the castle (launch → 30 min after the last arrival, monetization.md); the breach truce (§10) is the one exception — it starts by rule.

**Reinforcements**: cap by the host's embassy tier, 1.0 × C_march at tier 1 → 3.0 × at tier 6; they fight under the host's garrison lord; loss row 4; recall any time. One arriving mid-fight joins the next.

## 10. Walls and gate — the breach and the burning castle

One durability bar, **Walls & Gate**, W from 0 to W_max (W_max grows with the fortress tier) — two bars would ask the same decision twice. The structure bonus is computed on W AFTER the breakers' volley.

| Dial | PROPOSAL | Why |
|---|---|---|
| Structure bonus | +0.5 TS × W/W_max to the garrison | home advantage; engines exist to remove it |
| Won assault, no engines | −8% W_max | 13 wins to breach — engines are required |
| Won assault, standard train (breakers at 10% of a full rally, engine tier = wall tier) | −30% | breach in 3–4 won rallies |
| Lost assault, same train | −15% | breakers fire before the melee; breachers add 1.5× per capacity on wins only |
| Auto-repair | +12.5% W_max per hour after 15 min without an assault (20%/h at well tier 6, progression.md); stored as (W0, t0) | full from 0 in 8 h; 0 ticks |
| Repair button | +10% at once for 1 h of own stone output ([economy.md](economy.md) stone sink); 30-min cooldown | a defender's action in the war session |
| Lord utilities | structure damage ≤ +20%, wall loss −8% (lords.md §5–6) | Godric breaks, Maud holds |

Worked war window (engines; rallies 5 min apart): 100 → 70 (min 10) → repair 80 (min 11) → 50 (min 15) → 20 (min 20) → 0 (min 25). Four won assaults in 15 minutes breach a castle; one lucky hit never does.

**At W = 0 — Breached (burning)**:
1. **8 h breach truce**: no attacks or rallies on it; scouting stays open; hostile marches already on the road turn home on arrival, unharmed. The realm map shows it burning — smoke plume + the word "Burning" (world-forge; the realm zoom already reads burning and shielded).
2. Walls restart at 25% when the truce ends; auto-repair continues (the well puts the fire out: progression.md).
3. **The owner chooses** (1 tap, any time in the truce): stay, or relocate once, free, to an open site in the own alliance's territory or own region. Never random.
4. The truce ends if the owner attacks or scouts a player; camps, gathering, healing and reinforcing allies keep it. Once per 24 h: a second breach inside 24 h gives no truce.
5. **A breach adds no plunder**: plunder follows economy.md §7 (only the first 2 won assaults in 12 h plunder). Troops and production are untouched: a breach costs the wall and 8 h out of the war.

Rejected: forced random relocation at zero (the genre's rule) — it throws the player away from the alliance, a quit trigger; burning that drains durability over time — a server tick for a state a formula gives.

## 11. Scouting and warnings — information tiers

Scout level `L = clamp(3 + E_s − E_t, 1, 5)`, E = watchtower tier (the tower archetype — verify in `data/buildings.gd`) of the scout's castle and of the target. Equal towers give L3: the composition — the counter decision.

| L | Reveals (± = band shown) |
|---|---|
| 1 | owner, alliance, spine stage, wall %, state (ward, truce, burning), troops ±50% |
| 2 | + troops ±20%, garrison lord names, plunderable resources ±20%, reinforcement count |
| 3 | + troops per line ±10% (the MI input), engines present |
| 4 | + per line per tier exact, lord and skill levels, reinforcements per line |
| 5 | + lord gear and talents, stack pools in TS, exact structure bonus |

1. A scout is a march (function of time); its report is a snapshot at arrival and shows its age ("12 min old"). Armies change after a scout — bluffing is part of the game.
2. The target is always told: "Scouted by <house> (level 3)". Scouting a player breaks the peace ward.
3. **Incoming warnings** by the defender's own watchtower tier E: E1 exact ETA; E2 + attacker and kind (single or rally); E3 + size ±20%; E4 + lines ±10%; E5 + lords; E6 + engines by class. The ETA is always exact (battle-forge presents).

## 12. Why you won or lost — the cause ledger

The resolver emits per battle a ledger that report-forge turns into sentences (report-forge owns schema, templates and storage; this is the minimum content):

| Field | Size | Meaning |
|---|---|---|
| outcome, margin_ts | u8, i16 (1/100 TS) | win / loss / draw; strength margin in TS |
| factor_ts × 8 | 8 × i16 | tier, count, counter (MI), lords, realm, temporary, structures, engines (scalers) |
| casualties per side | sparse (line, tier, light, severe, dead, routed) | the §6 split |
| overflow | 2 × u32 | overflow dead, overflow routed |
| counter pairs, top 3 | 3 × (hunter, prey, TS share) | which counters landed |
| skill casts, top 5 | 5 × (lord, skill, round, value) | lord moments |
| walls | W before, W after, per engine class | the breach story |
| rounds, decisive round, end reason | 3 × u8 | rout, annihilation, round cap, wall held |
| scout age used, honour, weak-target factor | u32, u32, u8 | fairness context |
| resolver_version, seed | u16, u32 | replay and audit |

1. **Decomposition**: margin_ts = Σ factor_ts. Analytic if the frozen shape is multiplicative; otherwise by ablation (re-run with one factor neutral; ≤ 8 re-runs, lazily when the report is first opened, then cached — the cost falls only on reports that are read).
2. **Sum check**: |Σ factors − margin| ≤ 0.10 TS, or the ledger is rejected (probe).
3. **Cause threshold**: a factor is a cause if |TS| ≥ 0.20; ranked by |TS|; top 3 shown; the headline names the first ("Their spearmen caught your cavalry: −0.6 tier").
4. **Every cause has one next step** (one button): counter → scout / muster the hunter line; tier → the progression goal; count → rally or reinforce; lords → the lord screen; walls → engines or repair; overflow → the infirmary.

## 13. Genre weak spots, exploits → our answer

| Genre weak spot ([benchmark.md](benchmark.md)) or exploit | Our answer | Number |
|---|---|---|
| A 5% counter buried by talent and equipment stacks | counter = 1 tier, own category, never modified; pools capped | 1.0 TS vs ≤ 1.25 TS |
| PvP decided by raw power and spending | scouted composition (MI) answers the money gap | lead ≤ 0.30 TS |
| Overflow at home → death spirals; zeroed players quit | home never kills (routed 24 h); overflow warning; beds 1.25 × march | 0 dead at home |
| Top-tier heal bills make players avoid fighting | heal ≤ 40% of training; full beds ≤ 24 h of own output | ≤ 8 h heal |
| Castle at zero teleported at random | breach truce + the owner's free choice of site | 8 h truce |
| Raiding the weak and inactive as a norm | weak-target factor on honour; plunder caps (economy.md §7) | 0 below 30% |
| Honour farming between friends or alts | routed count 0; pair decay `0.5^(n−1)` per 24 h; weak-target factor | 3rd fight 25% |
| Self-breach for a truce or a free move | costs 4 won assaults with engines (attackers lose 30% dead); once per 24 h | 1 per 24 h |
| Token joins to leech rally rewards | < 2% of rally capacity is not a participant | 2% floor |
| Shield raised as the attack lands | no ward or shield starts with a hostile march on the road (only the breach truce, by rule) | 0 |

## 14. Harness, server cost, save

**Step 0 — measure the shipped game** before any tuning: the probe in measure mode prints r per line and tier, α (the q multiplier M that balances 2× troops gives `α = log2(M) − 1`), c in TS per hunter pair, and the TS of a max lord pair.

| Check (combat probe, qa-forge; path to confirm) | Pass |
|---|---|
| TIER: draw ratio per step, every line | r within 1.35–1.50, spread ≤ 0.03 |
| COUNTER: t(n) hunter vs t(n+1) prey, equal count; 45 pairs t1–t9 + spear t10 vs cav t11 | 46/46 at 1.0 ± 0.1 TS |
| LINES and POWER: neutral pairs, equal tier and count; equal-power random tier mixes | draw ±5%; draw ±10% |
| STACK: ablation of a maxed lord pair / all pools; I1 in 5 pairs | ≤ 0.78 (30 E) / ≤ 1.25 TS; 5/5 |
| LOSS: 10,000 random battles per context | splits sum 100; rows 1–3 dead = 0 |
| BEDS: worst normal day per S | fits; heal ≤ 8 h |
| DETERMINISM: same inputs + seed, 1,000 runs | identical beats hash |
| WHY: sum check; 20 canned battles with one injected cause | ≤ 0.10 TS; top cause = injected 20/20 |
| BREACH: assaults to breach at equal tiers | engines 3–4; none ≥ 12 |

Verdict (PROPOSED wording): `COMBAT PROBE OK - r 1.40, counter 46/46 within 0.1 TS, stack max 1.22 TS, home dead 0, determinism 1000/1000, why 20/20`. Also report-forge's report probe (canned beats → explanation), `ward_test` ([onboarding.md](onboarding.md)) and `core/sd_cost_probe.gd`.

**Server cost** (estimate — measure with `core/sd_cost_probe.gd`): writes per day = sends + recalls + Σ resolutions × (1 + participants) + scouts × 2. At 50,000 players: PvP 30% engaged × 5 engagements × ~4 writes ≈ 300,000; scouts 2 per player × 2 writes ≈ 200,000; camp resolutions are already in core-loop's 2.9 M. Total ≈ +0.5 M writes/day and 0 ticks. CPU ≤ 2 ms × ≈ 1.5 M resolutions/day ≈ 50 CPU-min/day; ablation adds ≤ 8× only for opened reports.

**Save migration** (gameplay-forge): castles load with W = W_max, `(W0, t0)` = load time, `truce_end = 0`, no routed batch; stack pools recomputed and clamped (a clamp that lowers a shipped value is an owner decision, §15); old reports keep their format (report-forge).

## 15. Owner decisions required

1. **Home never kills** (routed 24 h instead of dead) — the largest departure from the genre.
2. The counter ring (who hunts whom) and its size (1 TS, c ≈ 26%) — likely sacred constants.
3. Stack caps: lords 0.78 (lords.md's 30 E), realm 0.30, temporary 0.15, total 1.25 TS; heavy − free ≤ 0.30 TS on any day.
4. Loss splits per context (§6), including whether castle attacks outside war windows exist (row 8).
5. Breach: 8 h truce, once per 24 h, free relocation by choice; no random teleport.
6. Honour: weak-target factor (0 below 30% power) and pair decay; never an event currency.
7. Cavalry t11 as the only apex rung.
8. Any dial here that collides with a shipped sacred constant (the shipped value wins until decided).
