# Outcome — the ceremony, the card, the infirmary and the report hand-off

The seconds after a battle decide whether the player tries again or closes the game. The
genre's documented failures are here: zeroed players quit, a full hospital turns one bad fight
into a death spiral, and offers appear when the player is most upset. Our outcome answers four
questions in this order, for winners and losers alike: **what is safe, what is gone, why, what
next.** Every number is a **PROPOSAL**; loss buckets per context are design-forge `combat.md`.

## 1. Rules

1. **Losers are respected.** Defeat uses the same plate, size, frame and gilt rim as victory;
   no shake, no red wash, desaturation ≤ 15%, the loss stinger at the same loudness as the win
   stinger (presentation.md §8). No enemy emote, no mocking line.
2. **Safe before lost.** The first line under the headline is always what came back or what was
   protected — on both results.
3. **One cause, in plain words.** The top cause from report-forge's explanation engine, with the
   counter medallions the player saw in battle (presentation.md §5).
4. **Three next actions at most**, each ≤ 2 taps to its result.
5. **No purchase on any battle surface** (battle view, outcome card, report, warning banners,
   march form): 0 buy buttons, 0 offers, 0 gem prices. Items the player already holds may be
   used. This is the money-law applied to war: no war imagery over a buy button.

## 2. The ceremony — ≤ 1,800 ms, skippable after 300 ms

feel-forge owns motion rules (its "battle won 1,800 ms, skippable" rule per the studio notes;
banned easing list). The timeline:

| t (ms) | Victory | Defeat |
|---|---|---|
| 0 | `outcome` beat: winner `cheer`, camera eases out 6% over 800 ms | loser `fall_back`, same camera |
| 300 | a tap anywhere jumps to the interactive card | same |
| 300–700 | outcome plate slides in (PARCHMENT ground, GILT rim), ease-out cubic 400 ms | same plate, same motion |
| 700–1,500 | three numbers count up (`TRANS_QUART`, `EASE_OUT`, 800 ms): returning, loot, lord XP | returning and in the infirmary count up; **lost is shown still** — a loss never animates |
| 1,500–1,800 | one gold light pulse on the winner's banner (effects.md victory burst: short, no confetti) | the banner lowers over 300 ms, no effect |
| 1,800 | card buttons active | same |

Reduced motion: the plate fades in over 200 ms and numbers appear without counting.

| Fails when | Caught by |
|---|---|
| The ceremony blocks input > 300 ms or runs > 1,800 ms | [ ] `outcome_probe` timing in frames: `OUTCOME OK - 108 frames, skip at 18` |
| Defeat looks smaller, darker or louder than victory | [ ] `outcome_probe` plate size diff = 0 px; frame review side by side |

## 3. Headlines

Placeholder wording (story-forge owns the voice, l10n-forge the keys
`battle.outcome.<ctx>.<side>.<win|loss>`):

| Context | Side | Win | Loss |
|---|---|---|---|
| Camp | attacker | Camp cleared | The camp held — your march fell back |
| Field, interception | either | The field is yours | Your march fell back |
| Castle | attacker | Castle raided | Repelled at the walls |
| Castle | defender | The walls held | Your castle was raided |
| Castle | stationed ally | You helped hold <name>'s walls | <name>'s castle was raided |
| Rally | every participant | The rally won | The rally fell back |
| Stronghold | every participant | <stronghold> taken | <stronghold> held |

## 4. The card

A card covering ≤ 60% of the screen; the headline reads in 1 s (report-forge layout rule),
the whole card in ≤ 10 s.

| # | Line | Attacker example | Defender example |
|---|---|---|---|
| 1 | Headline | Your march fell back | Your castle was raided |
| 2 | Safe | 1,180 returning · 412 in the infirmary (heals in 1 h 40 m) | 82% of your stores were safe · 412 wounded in the infirmary |
| 3 | Lost | 96 lost | 60 lost · 12,400 food and 3,100 stone taken |
| 3b | Overflow (only if it happened) | Infirmary full: 60 could not be saved | same |
| 4 | Why | [cavalry medallion] » [archers medallion] "Their cavalry ran down your archers — 3 times" | "Your towers and drop-stones cost them 2,100 before the walls" |
| 5 | Changed | lord XP +1,240 | wall 40% — full in 1 h 10 m |
| 6 | Next | ≤ 3 buttons (§6) | ≤ 3 buttons |

Expanding "Why" shows up to 2 more causes; "Report" opens the full report (report-forge).

## 5. The infirmary hand-off

The core-loop promise: one lost full march heals in ≤ 8 h without speed-ups (core-loop §2);
combat.md sizes the beds. The outcome makes the promise visible:

1. Wounded move to the infirmary at resolution; line 2 shows the count AND the heal time.
2. **Heal all** from the card starts healing with resources (2 taps: Heal all → confirm).
   The infirmary plate's own finish options follow core-loop §5 (hourglass art only).
3. **Overflow** is shown on its own line with its reason, never merged into "lost".
4. **Forecast before the fight**: the march form's infirmary line ([flows.md](flows.md) §3)
   warned when the worst case exceeded the free beds; the outcome's overflow line links back to
   that warning ("You were warned: 3,200 beds for 4,100 at risk") only when overflow happened.
5. Lightly wounded who heal by themselves (combat.md bucket) count as "returning".

| Fails when | Caught by |
|---|---|
| A player loses troops to overflow with no forecast shown before | [ ] form unit test (flows.md §3) + `outcome_probe` overflow fixture |
| The card's heal time differs from the infirmary plate's | [ ] `outcome_probe`: equal to the second |

## 6. Next actions

| Case (from the report's top cause) | 1 | 2 | 3 |
|---|---|---|---|
| Attacker won | Heal all (if any wounded) or Attack next camp | Share | Report |
| Attacker lost to a counter | **Try <counter line>** (march form pre-filled by "Auto by counter") | Heal all | Ask for a rally |
| Attacker lost to numbers or tier gap | Heal all | Ask for a rally | Find a closer match (Find panel, "even" band) |
| Defender held | Heal all | Repair wall | Share |
| Defender raided | Heal all | Ask allies to station troops | Defence setup |
| Rally (any result) | Heal all | Rally again (leader only) | Share |

**A hard day**: after 2 lost defences inside 12 h, the defender's card replaces button 3 with
"Ask your alliance for a garrison" (1 tap posts the request). Any protective rule for repeated
losses (a truce, a cooldown) is combat.md's decision; this card only shows it.

| Fails when | Caught by |
|---|---|
| A defeat card offers nothing to do (the player closes the game) | [ ] `outcome_probe`: every fixture shows ≥ 2 buttons |
| "Try <line>" pre-fills a line the player does not own | [ ] probe: pre-fill uses only owned troops; greyed with "Train spearmen" otherwise |

## 7. Victory without gloating

- The winner's card shows their gains and the enemy's banner lowered, never destroyed.
- The winner may Share (chat-forge share card, report-forge content); the loser's name appears
  in the share card only as it does in the report — no "crushed", no ranking of humiliation.
- Victory lines stay factual: "Castle raided — 12,400 food taken".

## 8. Hand-off to report-forge

report-forge owns the schema (`schema.md`), the explanation engine (`explain.md`) and storage.
The contract between the two skills:

| Direction | Content | Rule |
|---|---|---|
| report → battle-forge | the log and header of [beats.md](beats.md) §1 | enough to replay; nothing else needed |
| battle-forge → report | nothing stored | act marks, highlight ticks and durations are recomputed on view (0 bytes, 0 writes) |
| shared code | the counter derivation (actor line vs target line → counter flag) | ONE function used by the badge, the matchup strip and the "why" line, so the three never disagree |
| deep links | "Watch the breach", "Watch the counter" in the report | computed on view as highlight indexes |

Telemetry for the battle experience (sampled 10% of battles to respect the server budget;
cloud-forge counts the cost):

| Event | Fields | Used for |
|---|---|---|
| `battle_watch` | ctx, watched_ms, skipped_at_ms, speed | are budgets right? skip rate per context |
| `outcome_next` | button, ms_to_tap | which next actions help |
| `retry_after_loss` | minutes, countered_line_changed (bool) | the learning signal for pillar 5 |

Targets (PROPOSAL): in playtests ≥ 80% of testers name the main cause within 10 s of the card
(pillar 5, "battles that are understood"); in telemetry, ≥ 30% of retries within 30 min of a
counter-caused loss change the countered line; D1 of players whose first PvP battle was a loss
within 5 points of those who won.

## 9. Checklist — any outcome change

- [ ] Safe line first, on both results; lost never animates.
- [ ] Defeat and victory plates identical in size, frame and loudness.
- [ ] Top cause present, with the same medallions as the battle and the march form.
- [ ] ≤ 3 next actions, each ≤ 2 taps; none sells anything.
- [ ] Overflow on its own line; heal time equal to the infirmary plate.
- [ ] `outcome_probe` verdict line pasted; reduced-motion capture checked.
