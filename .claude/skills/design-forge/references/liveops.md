# Live ops — the realm's life, campaign seasons, the event calendar

How a realm lives from its first day to its merge: the age arc, the cross-realm campaign seasons,
the events inside them, the calendar that shows them, and the rules that stop live ops from
turning into noise. Implementation: **gameplay-forge** (rules, scoring, data), **story-forge**
(chronicle, season frames, names), **ui-forge** (Herald's Board, event rail), **cloud-forge**
(realm router, migration, merges), **world-forge** (landmarks, the campaign map), **mail-forge**
(reward delivery), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md) §8.

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Check shipped data first
(`data/*.gd`, paths to confirm); a dial that is a sacred balance constant keeps its shipped value
and this file's value becomes a proposal to the owner. `S` = spine tier 1–6 ([core-loop.md](core-loop.md)).
`DAU₇` = 7-day average of players with ≥ 1 session that day. All clocks: 00:00 UTC reset (core-loop §7).

## 0. The four questions

- **Want**: a named place in the realm's chronicle; a campaign won by our realm and alliance; every milestone of this week's events.
- **Obstacle**: other realms on war days; milestone thresholds scaled to the player's own spine tier; the Truce calendar.
- **Wait**: event stage 24 h; race 72 h; campaign 35 days; tier ceilings open on known realm days.
- **Witness**: the chronicle names players; pennants and banner trims on the city; the Herald's Board; campaign standings.

## 1. The realm age arc

A realm is a story with chapters that open by **realm age** (days since it opened), so every
realm lives the same arc and every player can see the next chapter's date.

| Realm day | Chapter (in-world) | What opens | Owner |
|---|---|---|---|
| 0 | The Founding opens | new cities land here; newcomer peace ward ([onboarding.md](onboarding.md)); Firsts of the Realm (§9) | cloud-forge |
| 1–7 | The Founding (§2) | one race per day, each open 72 h; one guided system per day | gameplay-forge |
| 8 | The Settling | the weekly frame (§6.3); landmark tier 1 contestable ([world.md](world.md)) | world-forge |
| 14 | — | landmark tier 2; first Warlord's Hold; Banner League entry | world-forge |
| 21–35 | — | registration closes by the rule in §1.1 | cloud-forge |
| 28 | The First Crown | the realm's crown seat contested for the first time (two windows, §3.3) | world-forge |
| 35 | Founding chapter | chronicle chapter 1 names the realm's first crown and its Firsts | story-forge |
| first Truce at age ≥ 28 | Campaigns | enters the campaign draw (§3.5); first contest at realm age 31–65 | gameplay-forge |
| D₇ … D₁₀ (§1.2) | Ceilings rise | troop tiers t7 → t10 (cavalry t11) trainable in this realm | gameplay-forge, owner |
| 90 | Mature | merge watch starts (§8); the realm is a migration destination | cloud-forge |
| 365 | Year One | anniversary chapter; Founders' mark on cities founded in days 1–7 that are still active | story-forge |

**1.1 Opening realms.** A live realm has no title menu: a new player lands in the newest open realm
automatically; realm choice appears only in the Writ of Passage flow (§7).

1. Open a new realm when the newest has `N_fill` registrations, OR is 21 days old with ≥ 0.5·`N_fill`,
   OR is 35 days old. A newcomer never lands in a realm older than 35 days (late-joiner fix).
2. `N_fill = D_live / r(180)`: the realm reaches the dying line (§8) no earlier than day 180 without
   migrants. `D_live` = 300 DAU₇ (§8). Planning model: retention `R(d) = 0.40·d^−0.473` (through
   numbers.md §8's D1 40% / D30 8%), registrations spread evenly over 21 days, no migration.
   Replace it with cohort data after launch.

| Realm day | 7 | 20 (peak) | 30 | 90 | 180 | 365 |
|---|---|---|---|---|---|---|
| DAU per 1,000 registrations (model) | 126 | 199 | 100 | 50 | 35 | 25 |

| `N_fill` | Peak DAU (map must hold it, world.md) | DAU₇ falls below 300 | Installs/day to fill in 21 d / 35 d |
|---|---|---|---|
| **8,500 (recommended)** | ≈ 1,700 | ≈ day 180 | 405 / 243 |
| 12,000 | ≈ 2,400 | ≈ day 360 | 571 / 343 |

Read it: a realm keeps about 25% of its peak DAU at day 90 and 18% at day 180. Merges (§8) are a
normal chapter of every realm, not an emergency. Below 243 installs/day rule 1 opens under-filled
realms: plan their merge earlier (§8).

**1.2 Tier ceilings by realm age (owner decision).** Troop tier k ≥ 7 can be trained in a realm
from realm day `D_k` = the day the 75th-percentile free player reaches tier k's gate in
[progression.md](progression.md)'s path model. The ceiling binds only the fastest 25% of free players
and spenders, so nobody leads a two-week-old realm by four tiers. Troops already owned are never
removed. The Herald's Board shows "t8 opens in this realm on day 60 (in 12 days)".

| Fails when | Caught by |
|---|---|
| A newcomer lands in a realm older than 35 days | [ ] realm-router unit test (cloud-forge) |
| Peak DAU₇ exceeds world.md's design capacity `A_design` | [ ] realm dashboard alert at 90% of `A_design` |
| A ceiling binds > 25% of free players on its opening day | [ ] telemetry: free players waiting at the gate that day |

## 2. The Founding — realm days 1–7

Genre pattern: a new-server event races players through week 1 with daily unlocks. Our move: every
race is a milestone ladder (§5), each race stays open **72 h** (day N 00:00 → day N+2 23:59 UTC) so a
player who arrives on day 3 finds 3 open races, and each day one system gets its guided first-time
moment ([onboarding.md](onboarding.md) owns the teaching).

| Day | Chapter | Race (scores, §4.1) | Guided that day | Firsts of the Realm |
|---|---|---|---|---|
| 1 | Raise the Walls | Build: work minutes | build crews, help all | first city at S2, S3 |
| 2 | Muster the Levy | Muster: power added | muster yards, standing orders | first 1,000 troops mustered |
| 3 | Clear the Roads | Hunt: 10 × camp level | hunt orders, Resolve | first camp of level 10 |
| 4 | Swear Fealty | Fealty: helps given, gifts, donations | join an alliance, help | first alliance of 30 members |
| 5 | Fill the Granaries | Harvest: own-production minutes gathered | gathering, protection | first 24 h of output gathered in one day |
| 6 | The Lords' Muster | Lords: lord XP | lord pairing, Trial Grounds ch. 1 | first lord at the Sound rarity step, if lords.md grants one |
| 7 | The First Tourney | the Lists opens (§4.3) | counters in the Lists | first Lists champion |

Founding-week event value ≤ 1.5× a standard week (§5 R6): generous, but checked with econ_sim.

| Fails when | Caught by |
|---|---|
| A day-3+ arrival finds fewer than 3 open races | [ ] calendar audit, realm days 3–7 |
| A First or a rank carries power (resources, hourglasses, XP) | [ ] reward-id grep: firsts and bands hold cosmetic ids only |

## 3. Campaign seasons — cross-realm competition

**3.1 Length: 35 days = 1 Truce week + 4 Contest weeks** (owner decision).

| Length | Shape | War days | Seasons / year | Verdict |
|---|---|---|---|---|
| 4 weeks | Truce + 3 contest | 9 | 13.0 | four landmark tiers do not fit; 13 story frames a year |
| **5 weeks** | **Truce + 4 contest** | **12** | **10.4** | recommended: one landmark tier per contest week; one rest week in five |
| 6 weeks | Truce + 5 contest | 15 | 8.7 | acceptable; contest weeks 4–5 carry the burnout risk |
| 8 weeks | Truce + 7 contest | 21 | 6.5 | rejected: the genre's long-war fatigue (~50-day wars [unverified]) |

Season track top = 0.70 × 35 × 100 → **2,500** (25 full days of 35; core-loop §7 formula).

**3.2 War days.** Tue, Thu and Sat of contest weeks. Cross-realm fighting is lawful only inside the
two war windows of a war day (60 min each, 12 h apart); "the Truce holds" on the other days (fiction:
the medieval Truce of God limited fighting by weekday). One window per war day counts for a player,
so scheduled war is **≤ 3 h per week, ≤ 12 h per season**. Home cities are never attackable by
another realm: players fight in the campaign map (working name "the Debatable Land", world.md) from
a field camp; a lost camp sends survivors home under [combat.md](combat.md)'s field context. No realm
can burn or zero another realm's city (owner decision). Median war-day losses heal in ≤ 8 h without
speed-ups (core-loop §8.3).

**3.3 Time-zone fair windows.** The window pair (t, t+12 h) is fixed per campaign group at the draw,
chosen from the group's active-player time-zone histogram (last 14 days) to maximise mean quality:
start 17:00–22:00 local = 1.0; 08:00–17:00 or 22:00–23:00 = 0.6; 23:00–08:00 = 0. For ANY t, every
UTC offset has exactly one window starting between 08:00 and 20:00 local (two windows 12 h apart).
```python
def q(h):                                   # quality of a window starting at local hour h
    h %= 24
    return 1.0 if 17 <= h < 22 else 0.6 if (8 <= h < 17 or 22 <= h < 23) else 0.0
def pick(hist):                             # hist = {utc_offset_h: share of active players}
    return max((sum(w*max(q(t+z), q(t+z+12)) for z, w in hist.items()), t)
               for t in [x/2 for x in range(24)])   # -> (mean quality, t in UTC)
```
Worked (EU-heavy 65% UTC 0/+1, 30% Americas, 15% Asia): 05:30 and 17:30 UTC, mean 0.85, 63% get an
evening window. Americas-heavy: 11:30 and 23:30 UTC, 0.90, 75%. Asia-heavy: 11:30 and 23:30 UTC, 0.96, 90%.

**3.4 Scoring — we score ground, not corpses.** Points = landmarks held at window end (hold value by
landmark tier 1 / 2 / 4 / 8) + captures. Kills of player troops score 0 (the genre's kill points reward
zeroing weak players). Realm and alliance war-day score = **max(window A, window B)**, so a
one-time-zone alliance is not behind a global one. Personal honour per war day is capped at `H_day`,
reachable in ≈ 40 min of one window. Contest-week weights **1 / 1.5 / 2 / 3**: the last week is 40% of
the season, so a realm behind after two weeks still plays for the win (67% of the weight remains).
Group standing 1–4 gives realm colours in the chronicle and a pennant for members with ≥ 3 war days
or ≥ 1,500 season-track points; alliance standing gives banner trims; personal honour gives
milestones (§5). No standing gives power.

**3.5 The draw (Truce day 5).** Groups of 4 realms (3 allowed; a lone realm runs a home campaign on
its own crown seat). Strength `S_realm` = Σ power of its 200 strongest players active in the last 72 h.
Sort eligible realms by `S_realm`, cut consecutive groups of 4 inside an age band (< 90 d, 90–365 d,
> 365 d) when the pool allows; target max/min `S_realm` ≤ 1.25 per group, and a group above it is
flagged to ops before publication.

**3.6 What the Truce resets.** Resets: campaign-map holdings, season scores and honour, the season
track, the season rule (§9), the home crown seat (→ neutral; world.md decides). Never touched: city,
troops, lords, gear, items, resources, research, alliance, cosmetics, titles, chronicle. **No
season-only power**: no season tech, no stats that exist only in a season, so a realm in its first
campaign fights on the same stat sheet as a veteran realm.

| Fails when | Caught by |
|---|---|
| Any UTC offset lacks a window starting 08:00–20:00 local | [ ] TZ sweep in the calendar audit (§11) |
| Scheduled war > 3 h per week for a player who wants full honour | [ ] `H_day` reachable in one window: war-session replay |
| A group's `S_realm` max/min > 1.25 ships unflagged | [ ] draw report line per group |
| Kills change a standing | [ ] scoring unit test: kill-only log → 0 points |

## 4. Event taxonomy

| Type | Our event (in-world) | Scored window | Cadence | Scores | Losses | Rewards |
|---|---|---|---|---|---|---|
| Point race | **the Crown's Labours** | 6 stages × 24 h, Mon–Sat | contest weeks | work done (§4.1) | none | milestones per stage + weekly |
| Alliance PvE boss | **the Warlord's Hold** | Wed 00:00 – Fri 23:59 | contest weeks | rally damage | camp context, never dead | alliance milestones + share with floor |
| Loss-free solo PvP | **the Lists** | Mon 00:00 – Sun 20:00 | weekly, all year | bouts, wins | none | milestones; bands cosmetic |
| Loss-free team PvP | **the Grand Melee** | 30-min match, window A or B | league Sundays | banners held | none | league points |
| Alliance league | **the Banner League** | 4 match Sundays | per campaign | Melee results | none | trims + alliance currency milestones |
| Loss-free PvE lessons | **the Trial Grounds** | always open | +2 stages per contest week | stars | none | one-time per stage |
| Story | chronicle quests | 7 days | 3 per campaign | quest steps | none | lord XP, chronicle line |
| Realm firsts | Firsts of the Realm | realm days 0–90 | once each | first to a goal | none | chronicle line + pennant |

**Never**: paid-only events; an event that needs a purchase to finish; gacha events on the rail
([monetization.md](monetization.md)); kill-point events; points for gems or hourglasses spent or held;
power in rank rewards; a scored window < 24 h (except the two-window synchronous modes); progress lost
for missing a day.

**4.1 Labours scoring.** Milestones per spine bracket S1–2 / S3–4 / S5–6 (§5).

| Stage | Day | 1 point = |
|---|---|---|
| Masons | Mon | 1 minute of construction work done |
| Muster | Tue | 1 power added by training ([numbers.md](numbers.md) §3 `p_t`) |
| Scriptorium | Wed | 1 minute of research work done |
| Harvest | Thu | 1 minute of the player's own production gathered (gathered ÷ own output per minute) |
| Hunt | Fri | 10 × level of each camp cleared (Resolve-bound, bot-resistant) |
| Lords | Sat | 1 lord XP gained |
| — | Sun | no stage; the weekly chest auto-claims at 23:59 |

**Work done** = minutes a timer ran during the stage + minutes removed by helps, hourglasses and gem
finishes. Accelerated minutes (hourglasses, gem finishes) score at most **1/3 of the top milestone**.
Worked (S3–4, 2 crews): crews busy 24 h = 2,880 min; a median free player keeping them busy ≈ 62%
gives `P_ref` ≈ 1,800; top = 1.5 × 1,800 = 2,700 → crews busy ≥ 90% plus helps, 3 check-ins a day, no
hourglasses. A payer reaches 2,700 earlier with ≤ 900 accelerated minutes, never higher.

**4.2 The Warlord's Hold.** One hold per alliance, placed near its territory (world.md), rally-only,
72 h. HP = κ × Σ power of the alliance's 30 strongest members active in 72 h; κ set so a median
alliance clears 100% in ≈ 12 rallies (4 per day). Alliance milestones at 25 / 50 / 75 / 100% HP pay every
member who joined ≥ 1 rally. Personal damage share: floor 40% of the median participant's reward, cap
3×. A 12-member alliance clears its own hold: HP scales with its members, not the realm's.

**4.3 The Lists (tourney).** Identical troops: 5 companies of equal size at the Tourney standard tier
(t5 proposed), lines chosen freely. Lords at Tourney standard: fixed level, skills fixed, gear stats
off, talents from 3 published presets; all 8 lords lent by the Crown (try before investing; lords.md
decides). Winning choices: lord pair, line mix, rows, target priority, so counters decide
(combat.md). 5 bouts a day, banked up to 10, never sold. Rating: Elo K = 32, choose 1 of 3 opponents
within ±100. Weekly milestones: bouts 5 / 15 / 30 and wins 3 / 8 / 15 (bout milestones ≥ 50% of the
value). Bands top 1% / 5% / 20% → pennants. Presentation: battle-forge plays the resolver's beats,
20–45 s at 1×, skippable after 3 s.

**4.4 The Grand Melee and the Banner League.** 12 v 12, 30 min, loss-free: each player gets 3
identical companies; a beaten company returns to the muster point after 30 s; 5 banners score every
10 s; first to 1,000 or the most at 30:00. League: divisions of 8 alliances by league rating, across all
realms; 4 match Sundays per campaign, Swiss pairing, 3 / 1 / 0 points, top 2 up, bottom 2 down.
Sign-up 48 h before (the alliance picks window A or B), roster lock 1 h before; eligibility ≥ 12
members active in 7 days. Every member who played ≥ 2 matches gets the member chest.

**4.5 The Trial Grounds.** Fixed armies in fixed scenarios, one rule per stage (a counter, a
pairing, a ram against a gate, rally timing, a garrison swap); 3 stars; one-time rewards; no energy.
20 stages at launch; when a late system unlocks, its trial opens as the guided moment (onboarding.md).

## 5. Reward rules — milestones, never winner-take-most

| # | Rule | Number |
|---|---|---|
| R1 | Milestones carry 100% of power value (resources, hourglasses, lord XP, Resolve); ranks, bands and Firsts carry cosmetics, titles, chronicle lines only | genre: rank 1 = 180 units vs 1 for ranks 46–50 [benchmark.md] |
| R2 | Six milestones at 0.10 / 0.25 / 0.50 / 0.80 / 1.10 / 1.50 × `P_ref`; `P_ref` = median points of free players who scored ≥ 1 in the last run, per spine bracket; first run: loop sim (core-loop §11) | log-normal σ ≈ 0.6: 1.5 × median ≈ 75th percentile |
| R3 | Value split across M1–M6 | 8 / 10 / 14 / 18 / 22 / 28% |
| R4 | Tuning band, checked after each run (never mid-run) | ≥ 90% of participants reach M1; 20–35% of free participants reach M6 |
| R5 | Money finishes a ladder sooner, never higher | accelerated minutes ≤ 1/3 of M6; nothing above M6 |
| R6 | Rewards use the 7 hourglass sizes and own-production hours (core-loop §5, §7); all events of a standard week ≤ 1.0× that week's daily chests + writ for the 75th-percentile free player | ≈ 4,185 hourglass-minutes (7 × 255 + 2,400) + resources; econ_sim band 0.90–1.10 |
| R7 | Reached rewards arrive by mail ≤ 1 h after the end (mail-forge); unclaimed mail keeps ≥ 30 days | 0 lost |
| R8 | Share-based rewards (hold damage, league) have a floor and a cap | floor 40%, cap 3× the median participant |

## 6. The calendar and the limits

**6.1 The Herald's Board** (ui-forge; a board at the castle gate, ≤ 2 taps from the event rail):
21 days ahead; each row = name, type icon (Blender-made art, never a line glyph), tags (PvE / PvP /
alliance / loss-free / story), start and end in local time with the offset shown, "what counts" in
≤ 12 words, the full milestone list, and "Top reward: about 3 visits a day". Nothing is added inside
14 days (the freeze) except fixes and compensation, each posted as a board notice.

**6.2 Limits** (the calendar audit checks C1–C12, §11):

| # | Limit | Number |
|---|---|---|
| C1 | Concurrent scoring events per player (season track and daily orders are not events) | ≤ 3 |
| C2 | Event rail icons: season first, then events by end time; never an offer | ≤ 4 |
| C3 | Days an event is on the Herald's Board before it starts | ≥ 14 (shown 21) |
| C4 | Scored window length, unless two synchronous windows 12 h apart | ≥ 24 h |
| C5 | Race-free days per week | ≥ 1 (Sunday) |
| C6 | Power value in rank rewards | 0 (R1) |
| C7 | Accelerated minutes toward any top milestone | ≤ 1/3 (R5) |
| C8 | Event badges at one time: claimable only — never "new", "started", "rank changed" | ≤ 1 ([ux.md](ux.md) owns the global budget; core-loop A7 ≤ 3 at open) |
| C9 | Event pushes: opt-in by type (war call −10 min, Hold opens, league match −10 min), quiet hours | ≤ 1 per day (inside core-loop A8's ≤ 4) |
| C10 | Event starts per week / new event TYPES per campaign | ≤ 4 / ≤ 1 |
| C11 | Scheduled war per player (§3.2) | ≤ 3 h per week |
| C12 | Unclaimed rewards delivered after the end (R7) | ≤ 1 h |

**6.3 The standard contest week** (Truce week: only the Lists, the Trial Grounds and one chronicle quest).

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| Labours | Masons | Muster | Scriptorium | Harvest | Hunt | Lords | rest; weekly chest |
| Warlord's Hold | — | — | opens | open | closes 23:59 | — | — |
| The Lists | open | open | open | open | open | open | closes 20:00 |
| War (campaign) | new landmark tier | war day | — | war day | — | war day | — |
| League | — | — | — | — | — | sign-up locks | Melee, window A or B |
| Scoring events | 2 | 2 | **3** | **3** | **3** | 2 | 2 |

| Fails when | Caught by |
|---|---|
| More than 3 scoring events overlap on any day | [ ] calendar audit C1 |
| An event appears or changes inside the 14-day freeze without a board notice | [ ] calendar diff between published versions |
| > 1 event badge or a badge on an offer | [ ] ux_flow_probe screenshot at session open |

## 7. Migration — the Writ of Passage

Genre weak spot: power caps by server age trap strong players; moves are sold. Our rules:

1. **Newcomer move**: free, once, within 7 days of account creation while at S ≤ 2, to any realm
   ≤ 35 days old that is open for registration.
2. **The Writ**: earned once per campaign at 1,500 season-track points; hold ≤ 1; used only on Truce
   days 1–4; account ≥ 14 days old; no attack sent or received in the last 72 h (no escaping a war);
   cooldown one campaign. Never sold (owner decision: a move changes who a player fights, so it is
   power, not a journey).
3. **Destination fit** (all must hold): (a) arrivals this Truce ≤ 5% of the destination's DAU₇ (10%
   when it is Thinning, §8); (b) the player's highest troop tier ≤ the destination's ceiling (§1.2);
   (c) the player's power ≤ 1.5 × the destination's 90th-percentile active power (nobody drops into a
   weaker realm to prey); (d) destination DAU₇ + arrivals ≤ `A_design`.
4. **No trap**: every eligible player sees ≥ 3 destinations; when fewer pass, rule (c) relaxes to the
   3 realms with the highest 90th-percentile power. The strongest realms are always open to the strongest.
5. **What travels**: everything personal, resources in full ([economy.md](economy.md) may cap items);
   membership ends under [alliance.md](alliance.md)'s hopping rules.
6. **Alliance move**: an officer may move members together under rules 3a–3d counted as one group;
   they land in one block.
7. **Arrival**: a 24 h arrival ward that breaks if the player attacks; one free local relocation within 7 days.

| Fails when | Caught by |
|---|---|
| An eligible player sees < 3 destinations | [ ] migration check over all players on Truce day 1 |
| A player migrates within 72 h of an attack | [ ] server lock unit test (cloud-forge) |

## 8. Dying realms and merges

| State | Rule (`D_live` = 300, 14-day window) | Effect |
|---|---|---|
| Healthy | DAU₇ ≥ 600 and ≥ 4 alliances with ≥ 15 daily actives | — |
| Thinning | DAU₇ 300–599 | priority migration destination: listed first, arrival cap 10% |
| Dying | DAU₇ < 300 for 14 consecutive days, OR < 4 alliances with ≥ 15 daily actives for 14 days | merge candidate at the next Truce |

`D_live` = 300 because the draw measures the 200 strongest active players (§3.5) and four
alliances of 15 is the smallest field in which a landmark changes hands. world.md may raise it.

1. **Timeline**: health checked on campaign day 15 → announced on the Herald's Board and by mail the
   same day (21 days' notice) → dry run on a copy by day 29 → executed on Truce day 1 at the pair's
   lowest-activity hour; both realms read-only ≤ 30 min.
2. **Pairing**: same age band; `S_realm` ratio ≤ 1.5; post-merge DAU₇ between 600 and `A_design`;
   prefer two Dying or Thinning realms; the realm with more DAU₇ hosts (its map and name stay).
3. **Placement**: cities land by alliance in blocks on the host's reserve land (world.md keeps it);
   cities inactive ≥ 30 days AND at S ≤ 3 are archived, not placed, and return with nothing lost to an
   open slot when the owner comes back (no ghost cities, no farm targets).
4. **People**: names stay; a clash adds the old realm's short tag. A 72 h merge ward for every
   arrival (breaks on attack); one free local relocation within 7 days. Nothing claimable is lost.
5. **Story**: the absorbed realm's chronicle is bound into the host's as a named chapter; its last
   crown holder keeps the title "Last Crown of <realm>" (cosmetic).

| Fails when | Caught by |
|---|---|
| A merge with < 21 days' notice | [ ] calendar audit: merge row ≥ 21 days before execution |
| Post-merge DAU₇ > `A_design`, overlapping cities, or a lost reward or mail | [ ] merge dry run (§11) |

## 9. The chronicle and the season frame (story-forge)

Fable, the King's Chronicler, keeps each realm's chronicle at his lectern in the castle.
Entries: Firsts of the Realm, crown seat changes, campaign results, merges, anniversaries, and the
**most helpful alliance** of each campaign (help minutes given, core-loop §6): cooperation is written
down like conquest. Each campaign chapter names ≥ 10 players who won nothing by rank (most helpful,
most trials cleared, longest-held landmark). Limits: ≤ 1 feed entry per realm per day; one chapter
per campaign on Truce day 1; entries are template id + parameters (l10n keys), ≈ 200 bytes, ≤ 60 per
realm per campaign ≈ 12 KB.

**Season frames**: a rotating pool of 5 (each year repeats the pool with new chapters, so 5 splash
paintings total, game-art-director environments.md). Each frame = a name, a threat, 3 chronicle
quests, and ONE season rule that changes maps, timers or scoring, **never combat stats** (the
resolver's shape is frozen, gameplay-forge).

| Frame (PROPOSAL names) | Season rule (campaign map only) | Art |
|---|---|---|
| The Season of Sieges | siege engines build 25% faster; tier-3+ landmarks walled (siege-forge) | splash exists (siege dusk) |
| The Season of Beacons | tier-1 landmarks reveal marches within 10 tiles to their holders | new splash |
| The Season of Floods | two river fords close in alternate contest weeks | new splash |
| The Season of the Lists | Lists wins add up to 10% of `H_day` | new splash |
| The Season of the Long Winter | campaign-map marches 15% slower; field camps hold 20 h of supplies | new splash |

## 10. Ops calendar template

Copy to `design/liveops/campaign_<n>.md` (path to confirm); the data lives in one calendar file per
campaign (`data/liveops/campaign_<n>.json`, path to confirm), shipped as data, read by client and server.

```markdown
# Campaign <n> — "<frame name>"   days 1–35, day 1 = Mon <date> 00:00 UTC   status: DRAFT | FROZEN | LIVE | CLOSED
Frame: threat · season rule (maps/timers/scoring only) · splash id · 3 chronicle quests (weeks 1, 3, 5)
Groups: <realm ids ×4, S_realm max/min> · windows <t> and <t+12h> UTC · mean quality <q>
| Day | Date | Week | Labours stage | Hold | Lists | League | War (landmark tier) | Story | Ops |
|---|---|---|---|---|---|---|---|---|---|
| 1–7 | … | Truce | — | — | open | — | — | quest 1 | chapter, rewards mail, migration d1–4, draw d5 |
| 8–14 | … | Contest 1 (×1) | Mon–Sat | Wed–Fri | open | Sun | tier 1; Tue/Thu/Sat | — | merge check d15 |
(one row per day once dated)
Reward budget: | event | M1–M6 per bracket | value (hourglass-min) | econ_sim ratio | P_ref source |
Gates: T−35 draft · T−28 frame + art order · T−21 published, merges announced · T−14 FREEZE ·
       T−7 econ_sim + calendar audit green · T−3 staging clock run · T0 live · T+1 telemetry ·
       T+7 milestone reach vs R4 · T+35 predictions vs results → lessons.md
```

Calendar row fields (one per event): `id, type, frame, scope (realm | group | league | global),
start_unix, end_unix, stages[], scoring_key, brackets{S1-2,S3-4,S5-6: P_ref}, milestones[6],
bands[], rail_icon, push_type, tags[]`. Everything is a function of time: start/end are data, the
server never ticks an event.

## 11. Harness, server cost, metrics

| Proof | Measures | Verdict line (PROPOSED wording; qa-forge fixes it) |
|---|---|---|
| calendar audit (new, headless; qa-forge; path to confirm) | C1–C12, the 21-day merge notice, the TZ sweep, 3 open races on realm days 3–7 | `LIVEOPS CALENDAR OK - 35 days, max 3 concurrent, 0 faults` |
| staging clock run (cloud-forge) | the campaign at 1 day = 60 s: every start, end, auto-claim and mail fires once | `LIVEOPS CLOCK OK - 35 days, <n> transitions, 0 missed, 0 double` |
| merge dry run (cloud-forge) | placement, archive count, rewards and mail before/after | `MERGE DRYRUN OK - <n> cities placed, 0 overlaps, 0 lost rewards` |
| migration check | destinations per eligible player | `MIGRATION OK - 100% of eligible players have >= 3 destinations` |
| `tools/econ_sim.py` | events as `per: "day"` sources at M6 for the free player | day-30 ratio 0.90–1.10 (numbers.md §6) |
| `core/sd_cost_probe.gd` | writes per player per day | inside €200 at 50,000 players |

**Server cost** (estimate, all 50,000 players counted as daily active — upper bound): event points
ride on the action's own write (0 extra); milestone and chest claims ≤ 3 writes per player per day;
war orders 30% of players × 25 orders per war day ≈ 375,000 per war day ≈ 160,000 per day averaged;
Melee ≈ 2,900 orders per match; leaderboards = cached snapshots every 15 min per board; the calendar
file is fetched only when its version changes. Total ≈ 150,000 + 160,000 ≈ 0.3 M writes per day,
about 11% of core-loop §11's 2.9 M. Chronicle ≤ 1 write per realm per day. Measure before tuning.

**After ship**: ≥ 60% of DAU₇ score in each campaign; R4 bands per event; median scheduled war
≤ 3 h per week; every realm's DAU₇ state known daily; D30 6–10% and D90 tracked per realm cohort.

## 12. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| ~50-day cross-server wars, daily fighting | 35-day campaign: Truce week + 12 war days | ≤ 3 h scheduled war per week |
| Wars bound to one time zone | two windows 12 h apart; best window counts | every offset has a window 08:00–20:00 local |
| Winner-take-most weekly event | milestones hold all power value | rank power = 0 |
| Events reward spending speed-ups | work done; accelerated minutes capped | ≤ 1/3 of the top |
| Kill points push zeroing weak players | ground, not corpses; home cities safe from other realms | kills = 0 points |
| Season-only tech leaves young realms behind | no season-only power; tier ceilings by realm age | 0 season stats |
| Too many events, red-dot fatigue | concurrency, rail, badge and push caps | ≤ 3 / ≤ 4 / ≤ 1 / ≤ 1 per day |
| Migration caps trap players; moves sold | destination-relative fit; no-trap rule; never sold | ≥ 3 destinations |
| Dying servers | health states, merges with notice | 21 days' notice |
| Late starters in old servers | registration closes by day 35; newcomer move | ≤ 35 days |
| Arena where commander investment decides | Lists: identical troops AND lords at a standard | 0 paid bouts |

## 13. Owner decisions required

1. Campaign length 35 days (vs 4, 6 or 8 weeks); one global campaign clock for all realms.
2. Home cities never attackable by another realm; campaign fighting from field camps.
3. Tier ceilings by realm age (§1.2) — touches progression pace; may meet a sacred constant.
4. The Writ of Passage never sold (the money-law allows journeys; this file argues a move is power).
5. War days Tue / Thu / Sat and the 00:00 UTC reset (also core-loop owner decision 6).
6. Lords lent at Tourney standard in the Lists (lords.md; affects lord acquisition value).
7. `N_fill` (8,500 or 12,000) with world.md's map capacity `A_design`.
8. In-world names (story-forge canon): the Founding, the Settling, the Truce, the Debatable Land,
   the Crown's Labours, the Warlord's Hold, the Lists, the Grand Melee, the Banner League, the Trial
   Grounds, the Writ of Passage, the Herald's Board, Firsts of the Realm, the five season frames.
