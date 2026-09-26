# Lessons — predicted vs measured, and what the genre already taught

This file holds two kinds of entry:

- **L-entries: our own.** A spec predicted a number, a harness measured a different one, and we
  changed something. Written at design-loop step 8 ([SKILL.md](../SKILL.md)) from the §13 table of
  the spec ([spec-template.md](spec-template.md)). Like blender-forge's lessons, every L-entry
  happened: no verdict line, no entry.
- **G-entries: genre lessons.** Mistakes the benchmark genre made in public, taken from
  [benchmark.md](benchmark.md) so we do not pay for them a second time. A G-entry is a hypothesis
  about OUR game until one of our harnesses confirms it. When our data contradicts it, it becomes
  SUPERSEDED and names the L-entry that did it.

No benchmark content names here ([benchmark.md](benchmark.md) §0 quarantine check): the genre's
facts are stated as patterns, with their tags and the benchmark section that holds the evidence.

## 1. Index

| Id | System | Lesson in one line | Rule lives in | Status |
|---|---|---|---|---|
| G-01 | combat | A counter smaller than the stacked bonuses is invisible | [combat.md](combat.md), [lords.md](lords.md) | OPEN |
| G-02 | progression | Month-long timers turn the top of the spine into a wallet check; help cannot fix them | [progression.md](progression.md), [core-loop.md](core-loop.md) §4 | OPEN |
| G-03 | core loop | Energy that stops at its cap punishes sleep | [core-loop.md](core-loop.md) §3 | OPEN |
| G-04 | monetization | A sold queue reads as a paywall, even beside a free trial of it | [core-loop.md](core-loop.md) §2, [monetization.md](monetization.md) | OPEN |
| G-05 | seasons, events | Rank-weighted rewards and long wars turn play into spending and attendance | [liveops.md](liveops.md) | OPEN |
| G-06 | combat, economy | When healing costs more than a fight can win, players stop fighting | [combat.md](combat.md), [economy.md](economy.md) | OPEN |
| G-07 | economy | Any store outside raid protection breaks protection and feeds farm accounts | [economy.md](economy.md) | OPEN |
| G-08 | lords | Power creep plus a long grind turns a lord into a sunk cost | [lords.md](lords.md) | OPEN |
| G-09 | onboarding | A tutorial that teaches only the first hour hands late systems to video guides | [onboarding.md](onboarding.md) | OPEN |
| G-10 | UX, art | Information survives the zoom range only when each channel has one job | [ux.md](ux.md), [readability.md](../../game-art-director/references/readability.md) | OPEN |
| L-001 … | — | none yet: the first entry comes from the first shipped spec's §13 table | — | — |

## 2. Writing an L-entry

When to write one:
1. A spec §13 metric misses: |measured − predicted| > 10% of predicted.
2. A red-team item ([SKILL.md](../SKILL.md)) failed after ship, even when the metric looked fine.
3. The owner reversed a design decision: record the reason, it is a lesson about our guesses.

Rules:
1. **Evidence first.** Quote the harness verdict line exactly, or the telemetry query with dates, cohort and n. Estimates are not measurements.
2. **One mechanism per entry.** The cause is the mechanism ("the reserve filled at half speed, so two-visit players lost Resolve overnight"), never the symptom ("retention low").
3. **The fix is re-measured.** Without a re-measurement the entry stays OPEN; with it, FIXED.
4. **Promote the rule.** The "Rule" line is copied into the domain reference in the same change; the entry keeps the history. A lesson that changes no reference changed nothing.
5. **Ids never move.** L-001, L-002, … in order; never renumber or delete. A wrong entry is SUPERSEDED by a newer one that says why.
6. Plain words; every number with its unit; no benchmark content names.

```
### L-### · yyyy-mm-dd · <system> · OPEN | FIXED | SUPERSEDED by L-###
Lesson:     <one line: a rule with a number>
Spec:       design/<system>/SYSTEM.md §13, row "<metric>"
Predicted:  <metric> = <value>   (from <curve.py | econ_sim.py | spec formula §5>)
Measured:   <metric> = <value>   (<harness>: "<exact verdict line>"; <cohort>, n = <N>, <dates>)
Gap:        <absolute> (<%>). Cause: <the mechanism, one sentence>
Fix:        <what changed> in <file> by <skill>; re-measured <value> on <date>
Rule:       <the rule for next time>  → copied to <reference>.md §<n>
```

Phrasing examples only: the values in this table are illustrations, not measurements.

| Field | Returned by the reviewer | Accepted |
|---|---|---|
| Lesson | "Resolve felt bad for casual players" | "An energy reserve that fills at half speed loses Resolve for two-visit players; fill it at full speed" |
| Measured | "players seemed to lose a lot" | the loop-sim verdict line, quoted, with the profile it covers |
| Cause | "balance was off" | "the bar filled in 10 h but the median night gap is 12 h" |
| Rule | "tune it better" | "any regen pool covers ≥ 15 h of absence" (and the reference § it now lives in) |

| Fails when | Caught by |
|---|---|
| An L-entry has no verdict line or query | [ ] reviewer returns it |
| An entry's Rule is not in any reference | [ ] grep the named reference for the rule's number |
| A G-entry stays OPEN after our own data contradicted it | [ ] G statuses re-checked at each season review (game-director cycle) |

## 3. Genre lessons (seeded 2026-09-26 from benchmark.md)

"Mechanism" lines are our analysis, not facts from the sources. Tags as in [benchmark.md](benchmark.md) §0.

### G-01 · combat · OPEN — A counter smaller than the stacked bonuses is invisible
- **Evidence** (benchmark.md §4): counters +5% damage [snippet]; reviewers: battles are "raw power", not tactics [snippet]; lord talent, gear and paid-status bonuses bury the 5% [snippet].
- **Mechanism**: the counter is one ×1.05 among several bonuses; a single talent or gear line of the same size cancels it, so picking the right line changes little and players stop picking.
- **Rule** (PROPOSAL, verify against the shipped counter table and sacred constants): counter +20–50% so t(n) + counter ≈ t(n+1) ([numbers.md](numbers.md) §4); the lords' total contribution capped so it cannot cancel a counter.
- **Detect in our game**: the resolver harness flips an even mirror fight when only the counter changes; report-forge names the counter among the top-2 causes of a counter-lost fight.

### G-02 · progression · OPEN — Month-long timers turn the top of the spine into a wallet check
- **Evidence** (§2, §1): the top spine level takes 126 d 3 h base, with most of the cost in the last 3–4 levels [snippet]; the maximum help (29 helps at max(1%, 3 min)) still leaves ≈ 94 d [derived: `python tools/curve.py --levels 2 --first 5h --last 126d --shape geometric --helps 29 --help-floor 180s` prints `94d03h`]; a "rush" meta [snippet].
- **Mechanism**: percentage help and fixed-size speed-ups shrink relative to a huge timer; only bought minutes move it.
- **Rule**: no single timer above 14 d base ([core-loop.md](core-loop.md) §4); depth grows by breadth, not length ([progression.md](progression.md)).
- **Detect**: `curve.py` table per ladder, top rung ≤ 14 d; telemetry: share of top-rung finishes that used paid minutes, per spend band.

### G-03 · core loop · OPEN — Energy that stops at its cap punishes sleep
- **Evidence** (§1): cap 1,000, ~1 per 45 s, full in ~12.5 h, regen stops at the cap [community estimate]; one visit per 24 h keeps 1,000 of 1,920 daily regen, −48% [derived]; players find regen wasted at the cap punitive [snippet].
- **Mechanism**: the cap is shorter than a normal night-plus-work gap, so the player loses regen for living their day.
- **Rule**: bar + reserve that covers 15 h of absence ("nothing is lost for 15 hours", [core-loop.md](core-loop.md) §3).
- **Detect**: loop sim, 2-visit profile, Resolve loss 0%.

### G-04 · monetization · OPEN — A sold queue reads as a paywall, even beside a free trial of it
- **Evidence** (§1, §9): the second build queue comes as a 2-day item (one given at start) or permanently at paid-status tier 6 [snippet]; players read it as a paywall on a core queue [snippet].
- **Mechanism**: the free trial teaches "two queues is normal"; when it expires, the player feels a loss, and the only permanent fix is a purchase.
- **Rule**: plate count is never sold; 2 crews from minute one, the 3rd by play ([core-loop.md](core-loop.md) §2; [monetization.md](monetization.md) red lines).
- **Detect**: offer-data grep for plate, bed and banner counts returns 0.

### G-05 · seasons, events · OPEN — Rank-weighted rewards and long wars turn play into spending and attendance
- **Evidence** (§5, §8): a weekly event pays rank 1 = 180 upgrade items, rank 2 = 90, ranks 46–50 = 1 [snippet], so rank 1 earns 2× rank 2 and 180× rank 46–50 [derived]; the event is spend-driven [snippet]; cross-realm wars last ~50 days with time-zone coordination, a "second job" [snippet].
- **Mechanism**: when the top rank pays far more, the last purchase near the top is worth the most, and the event becomes an auction; long wars demand attendance at fixed hours for weeks.
- **Rule**: MILESTONE rewards (everyone who reaches a score gets the same); war windows ≤ 60 min, two a day 12 h apart ([core-loop.md](core-loop.md) §8.3); season length capped in [liveops.md](liveops.md) (PROPOSAL ≤ 4–6 weeks).
- **Detect**: reward-shape lint on event data; participation and completion by spend band and by time zone.

### G-06 · combat, economy · OPEN — When healing costs more than a fight can win, players stop fighting
- **Evidence** (§3, §4): healing 100k troops costs ≈ 7.2M gold at tier 4 and ≈ 144M at tier 5, ×20 per step [one guide; unverified]; the top-tier heal cost makes players avoid fighting [snippet]; hospital overflow → death spirals, zeroed players quit [snippet].
- **Mechanism**: the rational player compares the loss with the prize; once the heal bill is larger, the war game loses its main verb.
- **Rule**: healing always cheaper than training ([numbers.md](numbers.md) §5); a median player's worst normal day (one full field march lost) fits the hospital and heals ≤ 8 h without speed-ups ([core-loop.md](core-loop.md) §2); a late throttle resource must not make healing the dearest act ([economy.md](economy.md), [combat.md](combat.md)).
- **Detect**: `econ_sim.py` heal cost vs daily income per tier band; the hospital sizing test.

### G-07 · economy · OPEN — Any store outside raid protection breaks protection and feeds farm accounts
- **Evidence** (§3): the warehouse protects a fixed amount, the rest is raidable [snippet]; resources held as items cannot be raided [observational]; farm accounts are standard practice and guides teach them [snippet].
- **Mechanism**: an unraidable store removes the risk that makes surplus worth spending; a second account is both an unraidable store and a free source.
- **Rule**: items count against protection when opened, or stay unraidable only up to a cap; transfers taxed, capped by keep level, alliance-only; chest rewards bound to the account ([economy.md](economy.md); [core-loop.md](core-loop.md) §7).
- **Detect**: economy test (opening items cannot lift stock above the cap); transfer telemetry by account age and device.

### G-08 · lords · OPEN — Power creep plus a long grind turns a lord into a sunk cost
- **Evidence** (§5): 690 upgrade items to max one top-rarity lord's skills [snippet]; the free top-rarity item drops at ~3.023% from a free chest ~every 2 days [snippet] ≈ 5.5 a year, assuming one item per drop [derived]; "miss a meta commander → stuck" [snippet]; the developer later reworked old trees and weakened outliers [snippet].
- **Mechanism**: each new release that outclasses old lords devalues every point already spent, and a grind this long leaves no way to invest again.
- **Rule**: new lords are sidegrades; published duplicate math and a pity counter; investment refunded or moved on a rebalance; a written free path to max per rarity ([lords.md](lords.md)).
- **Detect**: sidegrade check against the role table; free-path days per rarity in the lords spec.

### G-09 · onboarding · OPEN — A tutorial that teaches only the first hour hands late systems to video guides
- **Evidence** (§10): the scripted first session covers a village, a camp fight, build / train / heal and the zoom-out to the map [observational]; group attacks, garrisons, cross-realm wars and talent planning are never taught, so players learn from videos and wikis [snippet]; early choices are often "wrong" and paid to redo [snippet].
- **Mechanism**: late systems unlock days or weeks after the tutorial ends; players who never learn the group systems never join the social layer that supports D30 ([numbers.md](numbers.md) §8).
- **Rule**: every late system gets a guided "first time" moment when it unlocks — first rally, first garrison, first season, first talent point ([onboarding.md](onboarding.md); [core-loop.md](core-loop.md) §10).
- **Detect**: the unlock table covers every system in [SKILL.md](../SKILL.md)'s system table; completion rate of each first-time moment.

### G-10 · UX, art · OPEN — Information survives the zoom range only when each channel has one job
- **Evidence** (§6, §11, §12): one continuous zoom from city to world with no loading screens, reviewed frame by frame, the genre's defining feature [snippet]; relationship shown as green / blue / red on public march lines [snippet]; armies as small token squads with a banner, a type icon and a health bar [observational]; icon clutter, red-dot fatigue and UI chrome fighting the painted world on small screens [observational].
- **Mechanism**: when relationship colour is also decoration, chrome outshines the art, or every icon carries a dot, the signal channel saturates and the player stops reading it.
- **Rule**: relationship colour is a reserved channel with shape coding; each zoom band shows one layer; token squads; chrome never out-contrasts the art; ≤ 3 red dots at open ([ux.md](ux.md); [readability.md](../../game-art-director/references/readability.md); [art-direction.md](../../blender-forge/references/art-direction.md); [core-loop.md](core-loop.md) §9 A7).
- **Detect**: `a11y_audit` (colour-blind pass), `ux_flow_probe` (dots at session open), `contrast_test`, `layout_audit` (event rail cap).
