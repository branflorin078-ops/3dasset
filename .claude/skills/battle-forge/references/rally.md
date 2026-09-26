# Rally — one leader, many banners, one army

A rally gathers several players' troops under one leader's lords against a target too strong
for one march: a player castle, an AI lord's fortress, a rally-only stronghold or a large camp.
Rules are design-forge `combat.md` §9 (windows, capacity, one command, requested mix, late
marches, loss share, the 5% floor) and `alliance.md` (ranks, scheduling); this file is the
experience. Numbers quoted from combat.md carry its section; the rest are **PROPOSALS**.

## 1. Genre pattern → our move

| Genre does (design-forge benchmark.md) | Where it hurts players | Our move |
|---|---|---|
| A castle building sets rally capacity; the leader picks a wait of 5 or 10 min, up to 8 h | long waits tie players to a clock; time zones decide who can join | combat.md caps windows at 5 / 10 / 30 min against players and 60 min on PvE strongholds; alliance.md §8 adds **scheduled rallies** (15 min – 24 h ahead, 15-min grid, each member's local time) with a **Pledge**; battle-forge shows each window's reach before launch |
| Joiners send troops; the leader's commanders lead | joiners cannot see their part; the battle feels like someone else's | joiners' pennons on the squad banners; a gilt corner on the squads that carry YOUR troops; a personal share line in the outcome |
| Forts are rally-only; rewards by each participant's damage share | shares are opaque | the share is shown before (expected) and after (actual) |
| Joining a rally you cannot reach in time fails late | wasted march, wasted attention | Join is blocked before Send with the arrival math |

## 2. Launch — the leader

| # | Step | Taps | Seconds |
|---|---|---|---|
| 1 | Tap the target (map or Find panel) | 1 | 2 |
| 2 | **Rally** | 1 | 1 |
| 3 | Window chips: 5 / 10 / 30 min against players, 5 / 10 / 30 / 60 min on PvE strongholds (combat.md §9); last choice remembered, default 5 min inside a war window (PROPOSAL); each chip shows "in reach: 9 of 24" — members active in the last 24 h whose march to the leader fits the window (computed on the client from the alliance roster, 0 extra reads) | 0–1 | 2 |
| 4 | Lead lord pair + own troops (rally preset pre-filled; matchup strip and "+0.4 tier" vs the scouted target); optional **Post mix** (1 tap): the requested composition from the latest scout (combat.md §9 rule 3) | 0–1 | 5 |
| 5 | **Launch** — the "Call the alliance" switch is ON by default: the rally card goes to the alliance Hall channel with a Herald line, never where enemies read (chat-forge `share-cards.md`); 0 extra taps | 1 | 1 |
| | **Total** | **3–5** | **≤ 15** |

**Scheduled rally** (alliance.md §8 owns the rule): Rally → **Schedule** → a slot 15 min – 24 h
ahead on the 15-min grid (the Marshal's muster hours are marked; each member sees local time) →
Launch = 5 taps. Members answer with **Pledge** (2 taps): their march leaves at launch if they
are online, or offline if they allowed it — castle rallies never auto-join offline (alliance.md
§8). The alliance calendar and the Rallies panel list it with its pledged count.

Leader actions while the window runs (dead air ≤ 90 s, core-loop §8.3):

| Action | Taps | Rule |
|---|---|---|
| Remind | 1 | one push to members who pledged but have not sent; once per rally (chat-forge allows one rally card per rally, so no re-post) |
| Scout the target | 2 | refreshes the matchup strip and the posted mix |
| Cancel | 2 (with confirm) | before departure every march goes home at 0 cost (combat.md §9 rule 4); joiners are told why |
| Launch now | 2 (with confirm) | PROPOSAL for combat.md, which today sends the rally at window end: leave early with whoever has arrived |

## 3. Join — the member

Entry points, each 1 tap: the alliance **Rallies** panel row, the rally card in the Hall channel
(chat-forge), the rally banner over the leader's castle on the map, the push (if opted in).
**Standing pledges** (alliance.md §8, PvE targets only) fill places still open at 50% of the
wait — people first; their pennons carry a small seal mark so the leader sees who came by pledge.

| # | Step | Taps | Seconds |
|---|---|---|---|
| 1 | Open the rally from any entry point | 1 | 2 |
| 2 | **Join** → form pre-filled from the member's rally preset — or from the leader's posted mix, capped by what the member owns — and capped to the remaining capacity; lords greyed ("the leader's lords lead this rally" — combat.md §9 rule 2); the rally's live "+0.3 tier" and the floor line "Send at least 1,200 (5% of capacity) to earn a share" (combat.md §9 rule 6) | 1 | 4 |
| 3 | **Send** | 1 | 1 |
| | **Total** | **3** | **≤ 10** |

The join form's summary line decides everything:

- "Arrives in 1:12 — rally leaves in 2:40 ✓"
- "Too far — arrives 0:38 after the rally leaves ✗" → Send disabled; offered: **Reinforce the
  leader's castle** (defence.md §5) or **Remind me of the next rally**.
- A march delayed after sending (the leader's window shortened, the joiner intercepted) that
  arrives late turns home by itself: 0 taps, 0 cost (combat.md §9 rule 4); the tracker says so.

**Rallies panel** (alliance): one row per open rally — target, leader, window countdown,
capacity bar, joiner count, the member's own ETA to the leader. Sorted: rallies the member can
reach, window closing soonest first; unreachable rallies last, greyed with the reason.

| Fails when | Caught by |
|---|---|
| A joiner's march arrives after the rally has left | [ ] `rally_flow_probe`: 0 late arrivals over 50 random join positions |
| Join takes > 3 taps from the chat card | [ ] `rally_flow_probe` join pass |
| Launch takes > 4 taps from the target (> 5 with a posted mix) | [ ] `rally_flow_probe` launch pass: `RALLY FLOW OK - launch 4 taps, join 3 taps, 0 late` |

## 4. The waiting window

| Window (combat.md §9) | Suits | Joiners who can make it |
|---|---|---|
| 5 min (default in war windows) | war windows | march to the leader ≤ 5 min — covers the 60–180 s war-march band (core-loop §2 and §8.3) |
| 10 min | spread-out alliances | ≤ 10 min |
| 30 min | a planned push outside the busiest hour | ≤ 30 min |
| 60 min (PvE strongholds only) | far strongholds, large camps | ≤ 60 min |

The leader is never idle for long: Remind, Scout and chat stay ≤ 2 taps away (dead air
≤ 90 s, core-loop §8.3), and the window countdown sits in the tracker.

The leader's castle shows a rally banner on the map for the whole window: its pennon count
grows as marches arrive (≤ 6 pennons, then "+N"). The capacity bar splits into one segment per
joiner (name on tap), so every member sees their own part of the whole before the march.

## 5. The rally march

- One column, one token: the leader's lord banner + the pennon cluster; speed = the slowest line
  across all joined troops (combat.md), named on the march card ("Speed set by: siege train").
- The column's line uses the viewer's relationship colour for the leader, plus a rally marker
  shape (never colour alone).
- Every participant's tracker shows the rally row with ETA; **Follow** (1 tap) works for all.
- A rally can be intercepted like any march ([flows.md](flows.md) §6); the whole rally army
  fights the interceptor.

## 6. The rally battle

Context "rally" in [beats.md](beats.md) §4: 30–45 s at 1×, `T_fight` 40 s (PROPOSAL).

| Element | Rule |
|---|---|
| Squads | still ≤ 5 per side (presentation.md §2) with up to 15 joiners (combat.md §9); joined troops merge into the leader's squads by line |
| Pennons | each squad banner carries the pennons of the players whose troops are in it (≤ 6, "+N") |
| Your troops | the squads that carry the viewer's troops get a gilt corner mark on their banner; tap-and-hold: "Your 3,200 archers are in this squad" |
| Lords | only the leader's lord pair casts; their full moments follow presentation.md §5 |
| Watch offer | every participant gets the watch toast at contact; each participant's client fetches the log once (N reads per rally of N players — report-forge `storage.md` costs it); the replay is shared from the rally report |

| Fails when | Caught by |
|---|---|
| A joiner cannot find their own troops on the field | [ ] frame review: the gilt corner visible on each joiner's squads |
| 15 joiners make 15 squads (frame time and clutter grow with the rally) | [ ] `battle_frame_probe` rally fixture: squads ≤ 5 per side |

## 7. Outcome and shares

Each participant gets their own card ([outcome.md](outcome.md)), built from the rally report
(report-forge):

| Line | Leader | Joiner |
|---|---|---|
| Headline | the rally result | the rally result |
| What came back | their own troops | their own troops |
| Share | "Rally total: 38,000 troops, 14 players" | "Your share: 3,200 troops (8%) · damage share 11% · 2,400 stone" — or, under 5% of capacity, "Below the 5% floor — no share this time" (combat.md §9 rule 6). On strongholds the card shows alliance.md §8's two parts: "equal part + damage part" |
| Losses | pro rata by troops given, per line and tier (combat.md §9 rule 5) | the same, into the joiner's own beds under the joiner's own overflow rule |
| Why | top causes (report-forge explanation engine) | same causes |
| Next | Heal all · Rally again · Share | Heal all · Share |

The expected share shown at Join ("≈ 8% of the rally") and the actual share on the card use
the same formula (combat.md / alliance.md); a gap > 2 points between them is a bug to report.

## 8. Failure states

| Case | What everyone sees | Losses |
|---|---|---|
| Leader cancels before departure | "Rally cancelled by <leader> — your troops are returning (1:12)" | none, 0 cost (combat.md §9 rule 4); camp Resolve refunded |
| Joiner arrives after departure | the march turns home by itself: "Arrived after the rally left — returning (0:54)" | none, 0 taps |
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
- Camp rallies: the leader pays Resolve, joiners pay 0 (core-loop §3). PvE never kills (combat.md
  §6 rule 2): the join form's infirmary line says "overflow would walk home".
- Stronghold rewards by damage share: the share line in §7 is mandatory there.

## 10. Teaching the first rally

The genre's tutorial never teaches rallies; onboarding.md's chapter 5 "The Rally" (about 80 h)
asks the player to join one rally and lead one, with AI companions filling it if allies are
offline (onboarding-forge owns the sequence; core-loop §10 adds a guided rally order in week 1).
battle-forge supplies three one-line highlights, each dismissed on tap, each ≤ 40 characters in
English:
1. on Join — "Your troops march to <leader>'s castle";
2. on the arrival line — "The tick means you will make it in time" (a shape icon, never colour alone);
3. on the battle view — "The gold corner marks your troops".

## 11. Checklist — any rally change

- [ ] Launch ≤ 5 taps (≤ 4 without a posted mix), join ≤ 3 taps, both measured with `rally_flow_probe`.
- [ ] The arrival check blocks unreachable joins before Send; 0 late arrivals in the probe.
- [ ] Window chips match combat.md §9 (5 / 10 / 30 vs players, ≤ 60 on PvE strongholds), each with its "in reach" count.
- [ ] Squads ≤ 5 per side at any rally size; pennons and the gilt corner visible.
- [ ] Expected share at Join and actual share on the card use one formula.
- [ ] Every failure in §8 has its message key and states the losses (usually none).
