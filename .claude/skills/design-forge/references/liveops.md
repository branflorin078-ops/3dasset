# Live ops — the realm's life, campaign seasons, the event calendar

How a realm lives from its first day to its merge: the age arc, the cross-realm campaign seasons, the events inside them, the calendar that shows them, and the limits that stop live ops from becoming noise.
Implementation: **gameplay-forge** (rules, scoring, data), **story-forge** (chronicle, season frames, names), **ui-forge** (Herald's Board, event rail, match HUD), **battle-forge** (Lists bouts and Melee fights as beats), **cloud-forge** (realm router, migration, merges), **world-forge** (landmarks, campaign map), **mail-forge** (reward delivery), **game-art-director** (season splashes), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md) §8.

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Check shipped data first (`data/*.gd`, paths to confirm); a dial that is a sacred balance constant keeps its shipped value, and this file's value becomes a proposal to the owner.
`S` = spine tier 1–6 ([core-loop.md](core-loop.md)). `DAU₇` = 7-day average of players with ≥ 1 session that day. One clock: 00:00 UTC reset (core-loop §7). Realm day 1 and campaign day 1 are always a Monday.

## 0. The four questions

- **Want**: a named line in the realm's chronicle; a campaign won by our realm and alliance; every milestone of this week's events.
- **Obstacle**: other realms on war days; milestone thresholds scaled to the player's own spine tier; the calendar itself (what opens when).
- **Wait**: event stage 24 h; Founding race 72 h; campaign 35 days; keep-level caps (the realm charter, §1.2) open on dates shown weeks ahead.
- **Witness**: the chronicle names players; pennants and banner trims on the city; the Herald's Board; campaign standings.
- **Free path** (SKILL.md rule 6): every event's top milestone with ≈ 3 check-ins a day and no hourglasses (§4.1); the season-track top in 25 of 35 days; full campaign renown in one 60-min window per war day; the Lists and the Grand Melee take no paid input at all. Free, light and heavy players share one calendar; money only reaches the same top sooner (§5 R5).

## 1. The realm age arc

A realm is a story whose chapters open by **realm age** (days since it opened), so every realm lives the same arc and every player can see the next chapter's date.

| Realm day | Chapter (in-world) | What opens | Owner |
|---|---|---|---|
| 1 (Mon) | The Founding (§2) | new cities land here; newcomer peace ward ([onboarding.md](onboarding.md)); Firsts of the Realm (§9); one race per day, each open 72 h | cloud-forge, gameplay-forge |
| 3 / 14 / 28 / 42 | Charter steps | keep cap L25 / L27 / L29 / L30 (§1.2): t8–t9 trainable from day 3, t10 from day 14, cavalry t11 from day 42 | gameplay-forge |
| 8 (Mon) | The Settling | the weekly frame (§6.3); landmark tier 1 contestable on war days with the realm's own window pair (§3.3, [world.md](world.md)) | world-forge |
| 15 / 17 / 22 | — | landmark tier 2 (Mon 15); first Warlord's Hold (Wed 17); tiers 3–4 (Mon 22; [world.md](world.md) §2 founding calendar) | world-forge |
| 21–35 | — | registration closes (§1.1 rule 1) | cloud-forge |
| 27 (Sat) | The First Crown | the realm's crown seat contested for the first time, in both war windows | world-forge |
| 35 (Sun) | Founding chapter | chronicle chapter 1 names the first crown and the realm's Firsts | story-forge |
| 33–61 | Campaigns | first campaign draw on a Friday at realm day ≥ 28 (§3.5); first contest week starts on realm day 36–64 | gameplay-forge |
| 90 | Mature | merge watch starts (§8; at 35 for a realm that closed under 0.5·`N_fill`); the realm counts as a Writ destination (§7 rule 3e) | cloud-forge |
| 365 | Year One | anniversary chapter; Founders' mark on still-active cities founded in days 1–7 | story-forge |

An arc date after day 7 that falls in a Truce week (§3) moves 7 days later: the Truce holds in every realm, young ones included (the Founding and the charter steps never move).

**1.1 Opening realms.** A live realm has no title menu: a new player lands in the newest open realm automatically; realm choice appears only in the Writ of Passage flow (§7).

1. Realms open on a Monday 00:00 UTC. Open the next one on the Monday before the newest realm is projected to reach `N_fill` registrations, or when it turns 21 days with ≥ 0.5·`N_fill`, or at 35 days. A newcomer never lands in a realm older than 35 days (late-joiner fix; an invite link to a friend's realm is the one exception, [onboarding.md](onboarding.md) §8). A faster cadence (a new realm every 7 days) reaches `N_fill` only above 8,500 ÷ 7 ≈ 1,200 installs a day; below that its realms die young (model, registrations over 7 days: at 405 installs a day a realm gets 2,835 registrations and falls under the dying line on day 20; at 1,000 a day, on day 116).
2. `N_fill = D_live / r(180)`, with `r(180)` = DAU at day 180 per registration (0.035 in the model below): without migrants, the realm stays above the dying line (§8) until day 180. Planning model: retention `R(d) = 0.40·d^−0.473` (fitted through numbers.md §8's D1 40% and 8%, the middle of its D30 6–10%; it gives D7 = 15.9%, inside the 15–20% target), registrations spread evenly over 21 days, no migration. Replace it with cohort data after launch.

| Realm day | 7 | 20 (peak) | 30 | 90 | 180 | 365 |
|---|---|---|---|---|---|---|
| DAU per 1,000 registrations (model) | 126 | 199 | 100 | 50 | 35 | 25 |

| `N_fill` | Peak DAU (the map must hold it, world.md) | DAU₇ falls below 300 | Installs/day to fill in 21 d / 35 d |
|---|---|---|---|
| **8,500 (recommended)** | ≈ 1,700 | ≈ day 180 | 405 / 243 |
| 12,000 | ≈ 2,400 | ≈ day 360 | 571 / 343 |

Read it: a realm keeps about 25% of its peak DAU at day 90 and 18% at day 180. Merges (§8) are a normal chapter of every realm, not an emergency. Below 243 installs per day, rule 1 opens under-filled realms: plan their merge earlier.

**1.2 Ceilings by realm age = [progression.md](progression.md) §9's realm charter** (one mechanism, owned there; its dates are progression.md owner decision 4). The highest keep level that may be started rises with realm age: L20 on days 0–2, L25 from day 3, L27 from day 14, L29 from day 28, L30 from day 42. Troop tier t opens at keep `L_t = 3·(t − 1)`, so t8–t9 are trainable from realm day 3, t10 from day 14 and cavalry t11 from day 42. The charter binds only rushers (0.0 days of delay for the free profiles in progression.md's model); nobody loses a level or a troop. This file uses it three times: the Herald's Board shows the next step ("Keep 29 opens in this realm on day 28 — in 3 days"); migration fit (§7 rule 3b); a merged realm takes the older realm's charter.

| Fails when | Caught by |
|---|---|
| A newcomer lands in a realm older than 35 days without an invite | [ ] realm-router unit test (cloud-forge) |
| Peak DAU₇ exceeds world.md's design capacity `A_design` | [ ] realm dashboard alert at 90% of `A_design` |
| > 5% of free players wait at a charter cap on any day (it should bind only rushers) | [ ] telemetry: free players at the cap level, per charter step |

## 2. The Founding — realm days 1–7

Genre pattern: a new-server event races players through week 1 with daily unlocks. Our move: every race is a milestone ladder (§5); each race stays open **72 h** (day N 00:00 → day N+2 23:59 UTC), so a player who arrives on day 3 finds 3 open races; each race features one system, and [onboarding.md](onboarding.md) §7 teaches it with a first-time moment when the player can first use it (by progress, never by calendar day).

| Day | Chapter | Race (scores as §4.1) | Featured system | Firsts of the Realm |
|---|---|---|---|---|
| 1 | Raise the Walls | Build: work minutes | build crews, help all | first city at S2, first at S3 |
| 2 | Muster the Levy | Muster: power added | muster yards, standing orders | first 1,000 troops mustered |
| 3 | Clear the Roads | Hunt: 10 × camp level | hunt orders, Resolve | first camp of level 10 cleared |
| 4 | Swear Fealty | Fealty: 1 per help given (the first 30 a day, core-loop §6), 10 per gift or donation | join an alliance, help | first alliance of 30 members |
| 5 | Fill the Granaries | Harvest: own-production minutes gathered | gathering, protection | first player to gather 24 h of own output in one day |
| 6 | The Lords' Muster | Lords: lord XP | lord pairing, Trial Grounds chapter 1 | first lord in a complete four-piece set |
| 7 | The First Tourney | the Lists opens (§4.3) | counters, in the Lists | first Lists champion |

On the rail the Founding is ONE icon, shared with onboarding.md §6's founding chapters and counting the same actions: never two lists asking for different chores. For the limits (§6.2) it is ONE event whose open races are its stages. Founding-week event value ≤ 1.5× a standard week (§5 R6): generous on purpose, and checked with econ_sim like any other week.

## 3. Campaign seasons — cross-realm competition

**3.1 Length: 35 days = 1 Truce week + 4 Contest weeks, on ONE global clock** (owner decision). Every realm's Truce falls in the same week, so migration and merges happen once, together, and one calendar file serves every realm. [monetization.md](monetization.md)'s war-season rules apply to the 4 contest weeks; the Truce week is a peace week.

| Length | Shape | War days | Seasons / year | Verdict |
|---|---|---|---|---|
| 4 weeks | Truce + 3 contest | 9 (6 campaign + 3 home) | 13.0 | four landmark tiers do not fit; 13 story frames a year |
| **5 weeks** | **Truce + 4 contest** | **12 (8 + 4)** | **10.4** | recommended: one landmark tier per contest week; one rest week in five |
| 6 weeks | Truce + 5 contest | 15 (10 + 5) | 8.7 | acceptable; contest weeks 4–5 carry the burnout risk |
| 8 weeks | Truce + 7 contest | 21 (14 + 7) | 6.5 | rejected: the genre's long-war fatigue (~50-day wars [unverified]) |

Season track top = 0.70 × 35 × 100 = 2,450, rounded up → **2,500** points (25 full days of 35; core-loop §7 formula; monetization.md §7's 25 levels × 100 give the same top). The Writ of Passage sits at 1,500 (§7). monetization.md §7 dresses the track as the plain chronicle; its paid illuminated lane is that file's question.

**3.2 War days.** Tue and Thu of contest weeks are **campaign** war days (the campaign map); Sat is the **home** war day (the realm's own landmarks and crown seat, world.md); none in the Truce week. War windows exist only on war days (core-loop §8.3's two windows 12 h apart, ≤ 60 min each); both start and end inside the war day in UTC (§3.3), so the 00:00 reset, a Labours stage change or the field camp striking at 23:59 ([world.md](world.md) §14) never cuts a window. Cross-realm fighting is lawful only inside them; "the Truce holds" on the other days (fiction: the medieval Truce of God limited fighting by weekday). One window per war day is enough for full renown, so scheduled war is **≤ 3 h per week, ≤ 12 h per season** per player.
Home cities are never attackable by another realm: players fight on the campaign map (working name "the Debatable Land", world.md) from a field camp, and a lost camp sends survivors home under [combat.md](combat.md)'s field context. No realm can burn or zero another realm's city (owner decision). Median war-day losses heal in ≤ 8 h without speed-ups (core-loop §8.3).

**3.3 Time-zone fair windows.** The window pair (t, t+12 h) is fixed per campaign group at the draw, from the group's active-player time-zone histogram (last 14 days), maximising mean quality: start 17:00–22:00 local = 1.0; 08:00–17:00 or 22:00–23:00 = 0.6; 23:00–08:00 = 0. `t` runs 00:00–11:00 UTC in 30-min steps, so the second window ends by 24:00 UTC. For ANY t, every UTC offset has exactly one window starting between 08:00 and 20:00 local. Offsets are read from the players' current clocks (summer time included); the pair stays fixed in UTC for the campaign, so a summer-time change inside it moves local times by 1 h, and the Board always shows local time. A realm not yet in a campaign uses the same war days, all three as home war days, with its own window pair (picked on realm day 5 from its players so far).
```python
def q(h):                                   # quality of a window starting at local hour h
    h %= 24
    return 1.0 if 17 <= h < 22 else 0.6 if (8 <= h < 17 or 22 <= h < 23) else 0.0
def pick(hist):                             # hist = {utc_offset_h: share of active players}
    return max((sum(w * max(q(t + z), q(t + z + 12)) for z, w in hist.items()), t)
               for t in [x / 2 for x in range(23)])   # t = 00:00..11:00 UTC -> (mean quality, t)
```
Worked: EU-heavy (55% UTC 0/+1, 30% Americas, 15% Asia) → 05:30 and 17:30 UTC, mean 0.85, 63% get an evening window. Americas-heavy (70% UTC −5 to −8) → 11:00 and 23:00 UTC, 0.90, 75%. Asia-heavy (75% UTC +7 to +9) → 00:30 and 12:30 UTC, 0.96, 90%.

**3.4 Scoring — we score ground, not corpses.** Points = landmarks held at window end (hold value by landmark tier 1 / 2 / 4 / 8) + captures (1× the hold value, once per landmark per window). Kills of player troops score 0 toward standings and rewards: the genre's kill points reward zeroing weak players. [combat.md](combat.md) §6's **honour** (the casualty tally, with its weak-target factor) stays a report, feed and chronicle statistic only; the campaign's personal score is a different word, **renown**, earned by ground.
Realm and alliance war-day score = **max(window A, window B)**, so a one-time-zone alliance is not behind a global one. Personal renown per war day is capped at `renown_cap`, reachable in ≈ 40 min of one window. Contest-week weights **1 / 1.5 / 2 / 3** (sum 7.5): the last week is 40% of the season, and 67% of the weight is still open after two weeks, so a trailing realm still plays for the win.
Group standing 1–4 gives realm colours in the chronicle and a pennant to members with ≥ 3 campaign war days or ≥ 1,500 season-track points; alliance standing gives banner trims; personal renown gives milestones (§5). No standing gives power.

**3.5 The draw (Truce day 5, Friday).** Groups of 4 realms (3 allowed; a lone realm runs a home campaign on its own crown seat). Strength `S_realm` = Σ power of its 200 strongest players active in the last 72 h. Sort eligible realms (realm day ≥ 28) by `S_realm` and cut consecutive groups of 4, inside one age band (< 90 d, 90–365 d, > 365 d) when the pool allows. Target max/min `S_realm` ≤ 1.25 per group; a group above it is flagged to ops before publication. The draw runs after migration (Truce days 1–4) and merges (Truce day 1) so it measures the realms as they will fight. War-day dates are on the Board from T−21 and never move; groups and window times are published at the draw, 4 days before the first war day, and hold for the campaign.

**3.6 What the Truce resets.** Resets: campaign-map holdings, season scores and renown, the season track, the season rule (§9), the home crown seat and home landmark tiers 3–4 (→ neutral guardians; tiers 1–2 keep holders: [world.md](world.md) §15 A6). Never touched: city, troops, lords, gear, items, resources, research, alliance, cosmetics, titles, chronicle.
**No season-only power**: no season tech and no stat that exists only in a season, so a realm in its first campaign fights on the same stat sheet as a veteran realm. Balance changes ([lords.md](lords.md) §12) land only on Truce day 1, posted on the Herald's Board ≥ 14 days before.

| Fails when | Caught by |
|---|---|
| Any UTC offset lacks a window starting 08:00–20:00 local | [ ] TZ sweep inside the calendar audit (§11) |
| Full renown needs both windows of a war day | [ ] war-session replay: `renown_cap` reached in one window |
| A group with `S_realm` max/min > 1.25 ships unflagged | [ ] draw report, one line per group |
| Kills change a standing | [ ] scoring unit test: a kill-only log scores 0 |

## 4. Event taxonomy

| Type | Our event (in-world) | Scored window | Cadence | Scores | Losses | Rewards |
|---|---|---|---|---|---|---|
| Point race | **the Crown's Labours** | 6 stages × 24 h, Mon–Sat | contest weeks | work done (§4.1) | none | milestones per stage + weekly |
| Alliance PvE boss | **the Warlord's Hold** | Wed 00:00 – Fri 23:59 | contest weeks | rally damage | PvE context (combat.md), never dead | alliance milestones + share with floor |
| Loss-free solo PvP | **the Lists** | Mon 00:00 – Sun 20:00 | weekly, all year | bouts, wins | none | milestones; bands cosmetic |
| Loss-free team PvP | **the Grand Melee** | 30-min match in a Sunday slot (§4.4) | league Sundays | banners held | none | league points |
| Alliance league | **the Banner League** | 4 match Sundays | per campaign | Melee results | none | trims + Treasury milestones ([alliance.md](alliance.md) §4) |
| Loss-free PvE lessons | **the Trial Grounds** | always open | +2 stages per contest week | stars | none | one-time per stage |
| Story (standing) | chronicle quests | 7 days | 3 per campaign (weeks 1, 3, 5) | quest steps | none | lord XP, chronicle line |
| Realm firsts (standing) | Firsts of the Realm | realm days 1–90 | once each | first to a goal | none | chronicle line + pennant |

"Standing" content lives in the chronicle, not on the event rail, and does not count toward C1, C2 or C10 (§6.2).
**Never**: paid-only events; an event that needs a purchase to finish; gacha events on the rail ([monetization.md](monetization.md)); kill-point events; points for gems or hourglasses spent or held; power in rank rewards; a scored window < 24 h (except the synchronous modes: war windows in pairs 12 h apart, Melee slots every 3 h); progress lost for missing a day.

**4.1 Labours scoring.** Milestones per spine bracket S1–2 / S3–4 / S5–6 (§5).

| Stage | Day | 1 point = |
|---|---|---|
| Masons | Mon | 1 minute of construction work done |
| Muster | Tue | 1 power added by training ([numbers.md](numbers.md) §3 `p_t`) |
| Scriptorium | Wed | 1 minute of research work done |
| Harvest | Thu | 1 minute of the player's own production gathered (gathered ÷ own output per minute) |
| Hunt | Fri | 10 × level of each camp cleared (Resolve-bound, so bot-resistant) |
| Lords | Sat | 1 lord XP gained |
| — | Sun | no stage; the weekly chest auto-claims at 23:59 |

**Work done** = minutes a timer ran during the stage + minutes removed by helps, hourglasses and gem finishes. **Item points** score at most **1/3 of the top milestone** in every stage: minutes removed by hourglasses or gem finishes, the share of a muster batch finished by them (batch power × accelerated minutes ÷ batch minutes), and lord XP from XP tomes.
Worked (S3–4, 2 crews): crews busy 24 h = 2,880 min; a median free player keeps them busy ≈ 62% → `P_ref` ≈ 1,800; top = 1.5 × 1,800 = 2,700 = crews busy ≥ 90% plus helps: 3 check-ins a day, no hourglasses. A payer reaches 2,700 earlier with ≤ 900 item points, never higher.

**4.2 The Warlord's Hold.** One hold per alliance, placed near its territory (world.md), rally-only, 72 h. HP = κ × Σ power of the alliance's 30 strongest members active in 72 h; κ is set so a median alliance clears 100% in ≈ 12 rallies (4 per day). Alliance milestones at 25 / 50 / 75 / 100% HP pay every member who joined ≥ 1 rally. Personal damage share: floor 40% of the median participant's reward, cap 3×. HP scales with the alliance's own members, so a 12-member alliance can clear its hold.

**4.3 The Lists (tourney).** Identical troops: 5 companies of equal size at the Tourney standard tier (t5 proposed), lines chosen freely. Lords at lords.md §11's one loss-free template (L40, Fine rank, Fine gear, talents chosen freely), every lord available, so skill beats investment and a player can try a lord before investing in it.
What wins: lord pair, line mix, rows, target priority, so counters decide ([combat.md](combat.md)). 4 bouts (in-world: jousts) a day, banked up to 12, never sold. Bouts are asynchronous: the attacker fights the defender's saved set-up; the server runs the resolver once per bout. The ladder is one pool across all realms. Rating: Elo K = 32; the player picks 1 of 3 opponents within ±100 rating. Weekly milestones: bouts 4 / 12 / 24 and wins 3 / 7 / 12 (28 bouts granted a week; the bout milestones carry ≥ 50% of the value). Bands top 1% / 5% / 20% → pennants. battle-forge plays the resolver's beats: 20–45 s at 1×, skippable after 3 s.

**4.4 The Grand Melee and the Banner League.** 12 v 12, 30 min, loss-free: each player gets 3 identical companies and one lord at the loss-free template; a beaten company returns to the muster point after 30 s; each held banner (5 on the field) scores 1 point per 10 s; first to 600 or the most at 30:00 (holding all 5 wins at 20:00; a 3–2 hold goes to time). The match is event-driven like realm marches (SKILL.md rule 5): an order is one append, an arrival runs the resolver, banner points = held seconds ÷ 10 from the hold intervals; no server tick loop.
League: divisions of 8 alliances by league rating, across all realms; 4 match Sundays per campaign (contest weeks), Swiss pairing, 3 / 1 / 0 points, top 2 up, bottom 2 down. **Slots**: 8 per Sunday, every 3 h from 00:00 UTC, so every UTC offset has 4 slots starting 08:00–20:00 local. At sign-up (closes Thu 23:59 UTC, 48 h before the first slot) the alliance marks ≥ 3 slots; Swiss pairing pairs only alliances that share one, taking the shared slot with the best §3.3 quality for both rosters (an alliance left unpaired takes a 1-point bye); pairings posted Fri. Roster lock 1 h before the slot; eligibility ≥ 12 members active in the last 7 days; one match per alliance per Sunday. Every member who played ≥ 2 matches gets the member chest (Merit, alliance.md §4).

**4.5 The Trial Grounds.** Fixed armies in fixed scenarios, one rule per stage (a counter, a pairing, a ram against a gate, rally timing, a garrison swap); 3 stars; one-time rewards; no energy. 20 stages at launch; when a late system's first-time moment fires or is skipped ([onboarding.md](onboarding.md) §7), its stage opens as the replayable practice beside the real lesson — the genre's tutorial never teaches these systems.

## 5. Reward rules — milestones, never winner-take-most

| # | Rule | Number |
|---|---|---|
| R1 | Milestones carry 100% of power value (resources, hourglasses, lord XP, Seals, Resolve, gems); ranks, bands and Firsts carry cosmetics, titles and chronicle lines only | genre weekly race: rank 1 = 180 units, ranks 46–50 = 1 unit ([benchmark.md](benchmark.md) §5) |
| R2 | Six milestones at 0.10 / 0.25 / 0.50 / 0.80 / 1.10 / 1.50 × `P_ref`; `P_ref` = median points of free players who scored ≥ 1 in the last run, per spine bracket; first run: loop sim (core-loop §11) | log-normal σ ≈ 0.6 → 1.5 × median ≈ 75th percentile |
| R3 | Value split across M1–M6 | 8 / 10 / 14 / 18 / 22 / 28% |
| R4 | Tuning band, checked after each run (never mid-run) | ≥ 90% of participants reach M1; 20–35% of free participants reach M6 |
| R5 | Money finishes a ladder sooner, never higher | item points (§4.1) ≤ 1/3 of M6; nothing above M6 |
| R6 | Rewards use the 7 hourglass sizes and own-production hours (core-loop §5, §7); all events of a standard week together ≤ 1.0× that week's daily chests + writ, for the 75th-percentile free player | ≈ 4,185 hourglass-minutes (7 × 255 + 2,400); resources ≤ 15% of the realm's weekly production ([economy.md](economy.md) §10); gems ≈ 25 a day (economy.md §11); Seals 20 featured + 10 Plain a month ([lords.md](lords.md) §11); econ_sim band 0.90–1.10 |
| R7 | Reached rewards arrive by mail ≤ 1 h after the end (mail-forge); unclaimed mail keeps ≥ 30 days | 0 lost |
| R8 | Share-based rewards (hold damage, league) have a floor and a cap | floor 40%, cap 3× the median participant |

| Fails when | Caught by |
|---|---|
| M6 reached by < 20% or > 35% of free participants | [ ] per-run telemetry → `P_ref` re-tuned for the next run |
| Any account passes M6, or item points exceed 1/3 of M6 | [ ] scoring unit test with a gem-finish-only log and a tome-only log |
| A 12-member alliance cannot clear its hold in 72 h | [ ] hold HP sim for alliances of 12 / 30 / 60 active members |
| A Lists bout reads a player's owned levels or gear | [ ] resolver-input test: two accounts, different lords, identical inputs |
| Weekly event value > 1.0× chests + writ | [ ] econ_sim line in the campaign's reward budget |
| Win-trading in the Lists (an alt loses on purpose) | [ ] rating test: a pair counts for rating ≤ 3 times a week; defences of accounts < 7 days old or at S1 are never offered |
| Alt accounts farm Fealty or Hold points | [ ] scoring test: accounts < 72 h old or at S1 score 0 for others (core-loop §6) |

## 6. The calendar and the limits

**6.1 The Herald's Board** (ui-forge; a board at the castle gate, ≤ 2 taps from the event rail). Shows 21 days ahead. Each row: name, type icon (Blender-made art, never a line glyph), tags (PvE / PvP / alliance / loss-free / story), start and end in local time with the UTC offset shown, "what counts" in ≤ 12 words, the full milestone list, and "Top reward: about 3 visits a day". Nothing is added inside 14 days (the freeze) except fixes and compensation, each posted as a board notice. **Compensation**: a server fault > 15 min inside a scored window extends that window by the fault's length rounded up to 1 h; any mailed compensation is the same for every player active in the previous 7 days, never scaled by spend.

**6.2 Limits** (the calendar audit checks C1–C12, §11):

| # | Limit | Number |
|---|---|---|
| C1 | Concurrent scoring events per player. Not counted: the campaign itself (the season, rail slot 1) and standing content (season track, daily orders, Trial Grounds, chronicle quests, Firsts of the Realm); the Founding counts as one | ≤ 3 |
| C2 | Event rail icons: season first, then events by end time; never an offer | ≤ 4 (season + 3) |
| C3 | Days an event is on the Herald's Board before it starts | ≥ 14 (shown 21) |
| C4 | Scored window length, unless synchronous (war windows 12 h apart; Melee slots every 3 h) | ≥ 24 h |
| C5 | Days per week without a race stage | ≥ 1 (Sunday) |
| C6 | Power value in rank rewards | 0 (R1) |
| C7 | Item points toward any top milestone | ≤ 1/3 (R5) |
| C8 | Event badges at one time: only for something claimable, never "new", "started" or "rank changed" | ≤ 1 ([ux.md](ux.md) owns the global budget; core-loop A7: ≤ 3 at open) |
| C9 | Event pushes, opt-in by type (war call −10 min before the window the player marked, Hold opens, league match −10 min), quiet hours kept | ≤ 1 per day (inside core-loop A8's ≤ 4) |
| C10 | Event starts per week / new event TYPES per campaign | ≤ 4 / ≤ 1 |
| C11 | Scheduled play per player per week: war (§3.2) + one Melee if rostered | ≤ 3 h + 30 min |
| C12 | Unclaimed rewards delivered after the end (R7) | ≤ 1 h |

**6.3 The standard contest week.** The Truce week runs only the Lists, the Trial Grounds and one chronicle quest. Every realm follows the global week type; a realm's own Founding week (realm days 1–7) replaces whichever week it falls in.

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| Labours | Masons | Muster | Scriptorium | Harvest | Hunt | Lords | rest; weekly chest |
| Warlord's Hold | — | — | opens | open | closes 23:59 | — | — |
| The Lists | open | open | open | open | open | open | closes 20:00 |
| War | next landmark tier opens | campaign war day | — | campaign war day | — | home war day | — |
| League | — | — | — | sign-up closes 23:59 | pairings posted | — | Melee in the paired slot; roster lock −1 h |
| Scoring events | 2 | 2 | **3** | **3** | **3** | 2 | 2 |

| Fails when | Caught by |
|---|---|
| More than 3 scoring events overlap on any day (chronicle-quest weeks and the Founding included) | [ ] calendar audit C1 |
| An event appears or changes inside the freeze without a board notice | [ ] diff between published calendar versions |
| > 1 event badge, or any badge on an offer | [ ] ux_flow_probe screenshot at session open |

## 7. Migration — the Writ of Passage

Genre weak spot: migration power caps that rise season by season trap strong players, and moving is pay-gated ([benchmark.md](benchmark.md) §8, §9). Our rules:

1. **Newcomer's passage** (routed by [onboarding.md](onboarding.md) §8): once, free, in the first 7 days at S ≤ 2 while the peace ward holds (refused once it breaks), to a realm with registration open (≤ 35 days old) or to a friend's realm by invite; resources carried only up to the warehouse allowance `Wp` (economy.md F11).
2. **The Writ**: earned once per campaign at 1,500 season-track points; hold ≤ 1; used only on Truce days 1–4; account ≥ 14 days old; no attack sent or received in the last 72 h (nobody escapes a war); cooldown one campaign. Never sold (owner decision: a move changes who a player fights, so it is power, not a journey).
3. **Destination fit** (all must hold): (a) arrivals this Truce ≤ 5% of the destination's DAU₇ (10% when it is Thinning, §8); (b) the player's keep level ≤ the destination's realm charter (§1.2); (c) the player's power ≤ 1.5 × the destination's 90th-percentile active power, so nobody drops into a weaker realm to prey; (d) destination DAU₇ + arrivals ≤ `A_design`; (e) destination realm day ≥ 90 (younger realms take newcomers only).
4. **No trap**: every eligible player sees ≥ 3 destinations; when fewer pass, rule (c) relaxes to the 3 realms with the highest 90th-percentile power. The strongest realms are always open to the strongest players.
5. **What travels**: everything personal; resources up to 72 H (hours of own production) per resource ([economy.md](economy.md) F11, the feeder guard; a merge carries everything); alliance membership ends under [alliance.md](alliance.md) §11's hopping rules.
6. **Alliance move**: the Liege or the Warden ([alliance.md](alliance.md) §2) may move Writ-holding members together, rules 3a–3e counted for the group; they land in one block.
7. **Arrival**: a 24 h arrival ward that breaks if the player attacks; one free local relocation within 7 days.

| Fails when | Caught by |
|---|---|
| An eligible player sees < 3 destinations | [ ] migration check over all players on Truce day 1 |
| A player migrates within 72 h of an attack | [ ] server lock unit test (cloud-forge) |

## 8. Dying realms and merges

| State | Rule (`D_live` = 300; 14-day window) | Effect |
|---|---|---|
| Healthy | DAU₇ ≥ 600 and ≥ 4 alliances with ≥ 15 daily actives | — |
| Thinning | DAU₇ 300–599, or < 4 alliances with ≥ 15 daily actives (for < 14 days) | priority migration destination: listed first, arrival cap 10% |
| Dying | DAU₇ < 300 for 14 consecutive days, OR < 4 alliances with ≥ 15 daily actives for 14 days | merge candidate at the next Truce |

Why 300: the draw measures a realm's 200 strongest active players (§3.5), and 4 alliances with ≥ 15 daily actives can each field a 12-player Melee roster and fill rallies against each other. world.md may raise it.

1. **Timeline**: health checked on campaign day 15 → announced on the Herald's Board and by mail the same day (21 days' notice) → dry run on a copy by day 29 → executed on Truce day 1 at the realms' lowest-activity hour; all merging realms read-only ≤ 30 min.
2. **Pairing**: 2 realms, or 3 when two Dying realms (each < 300) cannot reach 600 together; same age band; `S_realm` ratio ≤ 1.5; post-merge DAU₇ between 600 and `A_design`; prefer Dying and Thinning realms; the realm with more DAU₇ hosts (its map and name stay); the merged realm takes the older realm's charter ([progression.md](progression.md) §9).
3. **Placement**: cities land by alliance in blocks on the host's reserve land (world.md §2: the Fens, ≈ 1,450 castles). Castles archived under world.md §15 A8 (e.g. 30 days offline at any age) are not placed; they return to an open slot with nothing lost when the owner comes back (no ghost cities, no farm targets).
4. **People**: names stay; a clash adds the old realm's short tag. A 72 h merge ward for every arrival (breaks on attack); one free local relocation within 7 days. Nothing claimable is lost.
5. **Story**: the absorbed realm's chronicle is bound into the host's as a named chapter; its last crown holder keeps the title "Last Crown of <realm>" (cosmetic).

| Fails when | Caught by |
|---|---|
| A merge with < 21 days' notice | [ ] calendar audit: merge row ≥ 21 days before execution |
| Post-merge DAU₇ > `A_design`, overlapping cities, or a lost reward or mail | [ ] merge dry run (§11) |

## 9. The chronicle and the season frame (story-forge)

Fable, the King's Chronicler, keeps each realm's chronicle at his lectern in the castle. Entries: Firsts of the Realm, crown seat changes, campaign results, merges, anniversaries, and the **most helpful alliance** of each campaign (help minutes given, core-loop §6): cooperation is written down like conquest. Each campaign chapter names ≥ 10 players who won nothing by rank (most helpful, most trials cleared, longest-held landmark).
Limits: ≤ 1 feed entry per realm per day; one chapter per campaign, on Truce day 1; an entry = template id + parameters (l10n keys), ≈ 200 bytes; ≤ 60 per realm per campaign ≈ 12 KB. Players share entries to chat as share cards (chat-forge). Each campaign opens with a letter from the Chronicler (mail-forge template, painted header by game-art-director). Fable's portrait is a stand-in today (portraits.md): the letter uses the header, never his portrait, and no event features him until his painted batch is installed ([lords.md](lords.md) §11).

**Season frames**: a pool of 5 in fixed rotation with new chapters each time; at 10.4 campaigns a year each frame returns every 175 days, so 5 splash paintings in total (game-art-director environments.md). A splash is war imagery: never behind the illuminated chronicle's buy button (money-law, [monetization.md](monetization.md) §10). Each frame = a name, a threat, 3 chronicle quests, and ONE season rule that changes maps, timers or scoring on the campaign map, **never combat stats** (the resolver's shape is frozen, gameplay-forge).

| Frame (PROPOSAL names) | Season rule (campaign map only) | Art |
|---|---|---|
| The Season of Sieges | siege engines build 25% faster; tier-3+ landmarks walled (siege-forge) | prompt fragment ready (environments.md "season splash (siege dusk)"); painting to confirm |
| The Season of Beacons | tier-1 landmarks reveal marches within 10 tiles to their holders | new splash |
| The Season of Floods | two river fords close in alternate contest weeks | new splash |
| The Season of the Lists | Lists wins add up to 10% of `renown_cap` | new splash |
| The Season of the Long Winter | marches 15% slower, field-camp supplies 20 h (world.md §14); landmark hold values +50% (holding beats raiding) | new splash |

## 10. Ops calendar template

Copy to `design/liveops/campaign_<n>.md` (path to confirm). The data lives in one calendar file per campaign (`data/liveops/campaign_<n>.json`, path to confirm), shipped as data and read by client and server.

```markdown
# Campaign <n> — "<frame name>"   day 1 = Mon <date> 00:00 UTC   status: DRAFT | FROZEN | LIVE | CLOSED
Frame: threat · season rule (maps/timers/scoring only) · splash id · chronicle quests (weeks 1, 3, 5)
Groups: <realm ids ×4 · S_realm max/min> · windows <t> and <t+12h> UTC · mean quality <q>
| Day | Date | Week (weight) | Labours stage | Hold | Lists | League | War (landmark tier) | Story | Ops |
|---|---|---|---|---|---|---|---|---|---|
| 1–7 | … | Truce | — | — | open | — | — | quest 1 | chapter, reward mail, migration d1–4, draw d5 |
| 8–14 | … | Contest 1 (×1) | Mon–Sat | Wed–Fri | open | Sun | tier 1; Tue/Thu/Sat | — | — |
| 15–21 | … | Contest 2 (×1.5) | Mon–Sat | Wed–Fri | open | Sun | tier 2 | quest 2 | merge check + notice d15 |
(then one row per day once dated)
Reward budget: | event | M1–M6 per bracket | value (hourglass-min) | econ_sim ratio | P_ref source |
Gates: T−35 draft · T−28 frame + art order · T−21 published, merges announced · T−14 FREEZE ·
       T−7 econ_sim + calendar audit green · T−3 staging clock run · T0 live · T+1 telemetry ·
       T+7 milestone reach vs R4 · T+35 predictions vs results → lessons.md
```

Calendar row fields (one per event): `id, type, frame, scope (realm | group | league | global), start_unix, end_unix, stages[], scoring_key, p_ref{S1-2, S3-4, S5-6}, milestones[6], bands[], rail_icon, push_type, tags[]`. There is no spend-score field and no SKU-prerequisite field ([monetization.md](monetization.md) red line 13). Every event is a function of time: start and end are data, and the server never ticks an event (the Melee too is event-driven, §4.4).

## 11. Harness, server cost, metrics

| Proof | Measures | Verdict line (PROPOSED wording; qa-forge fixes it) |
|---|---|---|
| calendar audit (new, headless; qa-forge; path to confirm) | C1–C12, the 21-day merge notice, the TZ sweep (war pairs and the 8 Melee slots), war windows ≤ 60 min and two per war day, 3 open races on realm days 3–7 | `LIVEOPS CALENDAR OK - 35 days, max 3 concurrent, 0 faults` |
| staging clock run (cloud-forge) | the campaign at 1 day = 60 s: every start, end, auto-claim and mail fires once | `LIVEOPS CLOCK OK - 35 days, <n> transitions, 0 missed, 0 double` |
| merge dry run (cloud-forge) | placement, archive count, rewards and mail before/after | `MERGE DRYRUN OK - <n> cities placed, 0 overlaps, 0 lost rewards` |
| migration check | destinations per eligible player | `MIGRATION OK - 100% of eligible players have >= 3 destinations` |
| `tools/econ_sim.py` | events as `per: "day"` sources at M6 for the free player | day-30 ratio 0.90–1.10 ([numbers.md](numbers.md) §6) |
| `core/sd_cost_probe.gd` | writes per player per day, with a Lists and a Melee line | inside €200 per month at 50,000 players |

**Server cost** (estimate; all 50,000 players counted as daily active, an upper bound; 500 league alliances is a planning figure): event points ride on the action's own write (0 extra); milestone and chest claims ≤ 3 writes per player per day = 150,000; war orders 30% of players × 25 per war day = 375,000 per war day ≈ 160,000 per day over a contest week; Lists bouts 1 append each (ratings come from the log) × ≤ 4 = 200,000; Hold rallies 500 alliances × 12 × ≤ 30 joins per week ≈ 26,000 per day; Grand Melee ≈ 2,900 order appends per match (24 players × 1 order per 15 s × 30 min) × 250 matches = 0.72 M on a Sunday ≈ 100,000 per day; leaderboards cached every 15 min per board; the calendar file fetched only when its version changes; the chronicle ≤ 1 write per realm per day. Total ≈ 0.64 M writes per day, ≈ 22% on top of core-loop §11's 2.9 M. The Lists and the Melee are the first two lines for sd_cost_probe; measure before tuning.

**After ship**: ≥ 60% of DAU₇ score in each campaign; R4 bands per event; median scheduled war ≤ 3 h per week; each realm's health state known daily; D30 6–10% and D90 tracked per realm cohort.

## 12. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| ~50-day cross-server wars with daily fighting | 35-day campaign: Truce week + 12 war days | ≤ 3 h scheduled war per week |
| Wars bound to one time zone | two windows 12 h apart; the best window counts; Melee slots every 3 h | every offset: 1 war window and 4 Melee slots starting 08:00–20:00 local |
| Winner-take-most weekly event | milestones hold all power value | rank power = 0 |
| Events reward spending speed-ups | score work done; item points capped | ≤ 1/3 of the top |
| Kill points push zeroing weak players | ground, not corpses; home cities safe from other realms | kills = 0 standing points |
| Season-only tech leaves young realms behind | no season-only power; the realm charter slows only rushers (§1.2) | 0 season stats |
| Too many events, red-dot fatigue | concurrency, rail, badge and push caps | ≤ 3 / ≤ 4 / ≤ 1 / ≤ 1 per day |
| Migration caps trap players; moving is pay-gated | destination fit; the no-trap rule; the Writ never sold | ≥ 3 destinations |
| Dying servers; late starters in old servers | health states, merges with notice; registration closes by day 35 | 21 days' notice; ≤ 35 days |
| Standard-troop duel ladder where lord investment still decides | the Lists: identical troops AND lords at one template | 0 paid bouts |

## 13. Owner decisions required

1. Campaign length 35 days (vs 4, 6 or 8 weeks) on one global clock for all realms.
2. Home cities never attackable by another realm; campaign fighting from field camps; kills score 0 in campaigns.
3. The realm charter dates (progression.md owner decision 4) also gate migration (§7 rule 3b) and merges (§8): one decision, not two.
4. The Writ of Passage never sold (the money-law allows journeys; this file argues a move is power).
5. War days Tue / Thu (campaign) and Sat (home), and the 00:00 UTC reset (also core-loop owner decision 6).
6. In the Lists and the Grand Melee, every lord at lords.md's loss-free template, owned or not (affects what owning a lord is worth).
7. `N_fill` (8,500 or 12,000), with world.md's map capacity `A_design`.
8. In-world names (story-forge canon): the Founding, the Settling, the Truce (not combat.md's 8 h breach truce: story-forge may rename one), renown, the Debatable Land, the Crown's Labours, the Warlord's Hold, the Lists, the Grand Melee, the Banner League, the Trial Grounds, the Writ of Passage (beside core-loop's weekly writ and world.md's seat-move writ: three writs), the Herald's Board, Firsts of the Realm, the five season frames.
