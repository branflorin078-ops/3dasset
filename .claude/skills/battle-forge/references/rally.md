# Rally — one leader, many banners, one army

A rally gathers several players' troops under one leader's lords against a target too strong
for one march: a player castle, an AI lord's fortress, a rally-only stronghold or a large camp.
Rules (capacity, who contributes what, reward shares, loss buckets) are design-forge
`combat.md` and `alliance.md`; this file is the experience. Every number is a **PROPOSAL**.

## 1. Genre pattern → our move

| Genre does (design-forge benchmark.md) | Where it hurts players | Our move |
|---|---|---|
| A castle building sets rally capacity; the leader picks a wait of 5 or 10 min, up to 8 h | long waits tie players to a clock; time zones decide who can join | windows of 1 / 3 / 5 / 10 min (default 3); long waits replaced by **scheduled rallies** inside the two daily war windows (core-loop §8.3) |
| Joiners send troops; the leader's commanders lead | joiners cannot see their part; the battle feels like someone else's | joiners' pennons on the squad banners; a gilt corner on the squads that carry YOUR troops; a personal share line in the outcome |
| Forts are rally-only; rewards by each participant's damage share | shares are opaque | the share is shown before (expected) and after (actual) |
| Joining a rally you cannot reach in time fails late | wasted march, wasted attention | Join is blocked before Send with the arrival math |

## 2. Launch — the leader

| # | Step | Taps | Seconds |
|---|---|---|---|
| 1 | Tap the target (map or Find panel) | 1 | 2 |
| 2 | **Rally** | 1 | 1 |
| 3 | Window: 1 / 3 / 5 / 10 min chips (last choice remembered; default 3) | 0–1 | 2 |
| 4 | Lead lord pair + own troops (rally preset pre-filled; matchup strip vs the scouted target) | 0 | 5 |
| 5 | **Launch** | 1 | 1 |
| | **Total** | **3–4** | **≤ 15** |

**Scheduled rally** (war windows): Rally → **Schedule** → a start slot in the next war window
(15-minute steps) → Launch = 5 taps. It posts to the alliance feed and calendar; members tap
**Remind me** (1) and get one push 5 min before the window opens (core-loop A8 push budget).

Leader actions while the window runs (dead air ≤ 90 s, core-loop §8.3):

| Action | Taps | Rule |
|---|---|---|
| Launch now | 2 (with confirm) | leaves with whoever has arrived |
| Call again | 1 | re-posts the chat card; at most once per 60 s |
| Scout the target | 2 | refreshes the matchup strip |
| Cancel | 2 (with confirm) | every march returns; joiners are told why |
| Auto-launch at full | toggle, default on | departs the moment capacity is full |

## 3. Join — the member

Entry points, each 1 tap: the alliance **Rallies** panel row, the chat share card (chat-forge),
the rally banner over the leader's castle on the map, the push (if opted in).

| # | Step | Taps | Seconds |
|---|---|---|---|
| 1 | Open the rally from any entry point | 1 | 2 |
| 2 | **Join** → form pre-filled from the member's rally preset, capped to the remaining capacity; lords greyed ("the leader's lords lead this rally") | 1 | 4 |
| 3 | **Send** | 1 | 1 |
| | **Total** | **3** | **≤ 10** |

The join form's summary line decides everything:

- "Arrives in 1:12 — rally leaves in 2:40 ✓"
- "Too far — arrives 0:38 after the rally leaves ✗" → Send disabled; offered: **Reinforce the
  leader's castle** (defence.md §5) or **Remind me of the next rally**.

**Rallies panel** (alliance): one row per open rally — target, leader, window countdown,
capacity bar, joiner count, the member's own ETA to the leader. Sorted: rallies the member can
reach, window closing soonest first; unreachable rallies last, greyed with the reason.

| Fails when | Caught by |
|---|---|
| A joiner's march arrives after the rally has left | [ ] `rally_flow_probe`: 0 late arrivals over 50 random join positions |
| Join takes > 3 taps from the chat card | [ ] `rally_flow_probe` join pass |
| Launch takes > 4 taps from the target | [ ] `rally_flow_probe` launch pass: `RALLY FLOW OK - launch 4 taps, join 3 taps, 0 late` |

## 4. The waiting window

| Window | Suits | Joiner reach at war-march speed |
|---|---|---|
| 1 min | allies next door | ≤ 1 min march |
| 3 min (default) | war windows | ≤ 3 min — covers the 60–180 s war-march band (core-loop §2 and §8.3) |
| 5 min | spread-out alliances | ≤ 5 min |
| 10 min | far strongholds, large camps, scheduled starts | ≤ 10 min |

The leader's castle shows a rally banner on the map for the whole window: its pennon count
grows as marches arrive (≤ 6 pennons, then "+N"). The capacity bar splits into one segment per
joiner (name on tap), so every member sees their own part of the whole before the march.

## 5. The rally march

- One column, one token: the leader's lord banner + the pennon cluster; speed = the slowest line
  across all joined troops (combat.md), named on the march card ("Speed set by: siege train").
- The column's line is the leader's relationship colour plus a rally marker shape (never colour
  alone).
- Every participant's tracker shows the rally row with ETA; **Follow** (1 tap) works for all.
- A rally can be intercepted like any march ([flows.md](flows.md) §6); the whole rally army
  fights the interceptor.

## 6. The rally battle

Context "rally" in [beats.md](beats.md) §4: 30–45 s at 1×, `T_fight` 40 s (PROPOSAL).

| Element | Rule |
|---|---|
| Squads | still ≤ 5 per side (presentation.md §2); joined troops merge into the leader's squads by line |
| Pennons | each squad banner carries the pennons of the players whose troops are in it (≤ 6, "+N") |
| Your troops | the squads that carry the viewer's troops get a gilt corner mark on their banner; tap-and-hold: "Your 3,200 archers are in this squad" |
| Lords | only the leader's lord pair casts; their full moments follow presentation.md §6 |
| Watch offer | every participant gets the watch toast at contact; the replay is shared from the rally report |

| Fails when | Caught by |
|---|---|
| A joiner cannot find their own troops on the field | [ ] frame review: the gilt corner visible on each joiner's squads |
| 20 joiners make 20 squads (frame time and clutter grow with the rally) | [ ] `battle_frame_probe` rally fixture: squads ≤ 5 per side |

## 7. Outcome and shares

Each participant gets their own card ([outcome.md](outcome.md)), built from the rally report
(report-forge):

| Line | Leader | Joiner |
|---|---|---|
| Headline | the rally result | the rally result |
| What came back | their own troops | their own troops |
| Share | "Rally total: 38,000 troops, 14 players" | "Your share: 3,200 troops (8%) · damage share 11% · 2,400 stone" |
| Why | top causes (report-forge explanation engine) | same causes |
| Next | Heal all · Rally again · Share | Heal all · Share |

The expected share shown at Join ("≈ 8% of the rally") and the actual share on the card use
the same formula (combat.md / alliance.md); a gap > 2 points between them is a bug to report.

## 8. Failure states

| Case | What everyone sees | Losses |
|---|---|---|
| Leader cancels | "Rally cancelled by <leader> — your troops are returning (1:12)" | none; camp Resolve refunded |
| Target warded or moved during the window | "Target out of reach — rally stood down" | none |
| Rally full | Join disabled: "Rally full — 0 places"; offered: Reinforce the leader | — |
| Joiner too far | Send disabled with the arrival math (§3) | — |
| Joiner recalls during the window | the joiner's march returns; the leader sees "<name> left", the bar shrinks | none |
| Leader goes offline | nothing changes: marches and the window are functions of time | — |
| Leader's castle attacked during the window | whether waiting joiners defend it is combat.md's rule; the rally row states it ("Waiting troops will / will not defend") | per combat.md |
| Under-filled at the window end | departs with what arrived; the leader saw the matchup strip before | per the battle |
| Server resolution slow | as any battle (beats.md §6) | — |

## 9. Camp and stronghold rallies

- Large camps and rally-only strongholds (design-forge `world.md`) use the same flows.
- Camp rallies: the leader pays Resolve, joiners pay 0 (core-loop §3).
- Stronghold rewards by damage share: the share line in §7 is mandatory there.

## 10. Teaching the first rally

The genre's tutorial never teaches rallies; core-loop §10 places a guided first rally as a
rotating daily order in week 1 (onboarding-forge owns the sequence). battle-forge supplies three
one-line highlights, each dismissed on tap, each ≤ 40 characters in English:
1. on Join — "Your troops march to <leader>'s castle";
2. on the arrival line — "The tick means you will make it in time" (a shape icon, never colour alone);
3. on the battle view — "The gold corner marks your troops".

## 11. Checklist — any rally change

- [ ] Launch ≤ 4 taps, join ≤ 3 taps, both measured with `rally_flow_probe`.
- [ ] The arrival check blocks unreachable joins before Send; 0 late arrivals in the probe.
- [ ] Windows ≤ 10 min; longer waits only as scheduled rallies inside war windows.
- [ ] Squads ≤ 5 per side at any rally size; pennons and the gilt corner visible.
- [ ] Expected share at Join and actual share on the card use one formula.
- [ ] Every failure in §8 has its message key and states the losses (usually none).
