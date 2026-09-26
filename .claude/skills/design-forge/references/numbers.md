# Numbers — curves, formulas and simulations

Designers of successful live strategy games tune in **player time**, then derive
costs. This file is the toolkit. Tools: `tools/curve.py` (timers),
`tools/econ_sim.py` (sources vs sinks). Tests: `python tests/test_tools.py`.

## 1. Design timers from intended player time

Decide the felt length first, per phase of the game:

| Phase | Upgrade length | Why |
|---|---|---|
| First session (levels 1–5) | 5 s – 3 min, many **instant/free** under a threshold | every tap must produce a result; the tutorial is the game |
| First week | 5 min – 4 h | fits between sessions; "come back after lunch" |
| First month | 4 h – 2 d | overnight and weekend goals; alliance help matters |
| Endgame | 2 – 14 d on single upgrades | status items; speed-ups and help become the lever |

Then run:
```
python tools/curve.py --levels 25 --first 1m --last 14d --shape phased --helps 20
```
`phased` front-loads growth (fast, frequent level-ups) and flattens the tail so
the last levels are long without exploding. Paste the table into SYSTEM.md §5.

**Free-under-threshold** (a pattern worth keeping): any timer shorter than a
threshold (e.g. 3–5 min) completes instantly with one tap. The threshold
itself can be a progression reward (research, a title), which turns "skip the
wait" from a purchase into an earned perk.

## 2. Costs follow time, income follows level

- Cost of level L: `C(L) = C1 · r^(L−1)`, with `r` chosen so
  `C(L) / income(L)` ≈ the intended wait in hours of passive production
  plus active play. Early r ≈ 1.4–1.8, late r ≈ 1.15–1.3.
- Income grows slower than costs (`income(L) ∝ g^L` with g < r), so time,
  not money, is the main gate early, and resources become a gate late —
  that is where gathering, trading and alliance help earn their place.
- Mix of resources rotates by tier: early levels cost the common resources
  (food, wood); stone and iron arrive as the second and third gates. A new
  resource appearing is itself a progression beat.

## 3. Power — one number that summarises strength

A single "power" score is how players compare themselves and pick targets;
it must be **monotonic and legible**, not a hidden truth.

```
power = Σ_troops count_t · p_t
      + Σ_buildings b(level) + Σ_research r(level)
      + Σ_lords (level + skills + gear)
```
- Troop power per unit by tier: `p_t = p1 · k^(t−1)`; with 10 tiers keep
  k ≈ 1.35–1.5 so t10 ≈ 15–38× t1 (a t10 must be worth many t1s, never
  infinitely many — mass must still matter).
- Power is displayed, but battle outcome comes from stats, counters and
  lords. Publish the difference (a tooltip: "power is a guide; counters and
  lords decide battles") — players who lose to lower power must learn why.

## 4. Combat scaling — mass versus quality

Lanchester's laws are the honest starting point:
- **Linear law** (melee, one-on-one contact): fighting strength ∝ N · q.
- **Square law** (ranged, everyone can shoot everyone): strength ∝ N² · q.
Pure square law makes the biggest army win absurdly; pure linear makes mass
pointless. Mobile strategy damage models usually sit between them, e.g.
damage ∝ q · N^α with α ≈ 0.5–0.8 per round, so doubling an army is strong
but not decisive. Fix α in the resolver's frozen shape (gameplay-forge), not
per feature.

Counter bonuses: a counter should swing an even fight clearly but not
erase tiers — typically +20–50% damage dealt by the counter line. Validate
with the resolver harness: t(n) with counter ≈ t(n+1) without counter is a
readable rule of thumb.

## 5. Loss model — make defeat cost time, not the account

Three buckets per casualty:
- **lightly wounded** → return by themselves after the battle (field fights),
- **severely wounded** → hospital (capacity-limited, healed for resources +
  time, cheaper than training),
- **dead** → gone, when the hospital is full or in designated war zones.
Hospital capacity is the dial that makes defeat recoverable. Design it so a
median player's worst normal day (losing one full field march) fits in the
hospital; overflow is the deliberate cost of over-committing.

## 6. Sources and sinks — run the simulation

```
python tools/econ_sim.py --example > design/<system>/econ.json   # edit
python tools/econ_sim.py design/<system>/econ.json --days 1,7,30,90 --csv design/<system>/econ.csv
```
Rule: free player, day 30, every resource with a sink, ratio sinks/sources
in 0.90–1.10. HOARD (< 0.9) → rewards inflate and stop mattering; add a sink
or cut a source. WALL (> 1.1) → the player hits a resource wall; decide
whether that wall is meant to push gathering/trading (name it in the spec) or
is a bug.

Standing sinks that keep an economy honest: upgrades, training, healing,
research, upkeep (food per troop per hour), alliance donations, crafting,
and cosmetic/prestige spends. Standing sources: production buildings,
gathering, camp raids, daily/weekly tasks, events, alliance gifts.

## 7. Speed-ups are a currency — price them in minutes

Every speed-up item and gem cost is a price in minutes. Keep one table:
`1 m, 5 m, 15 m, 1 h, 3 h, 8 h, 24 h` and the gem price per minute
(degressive: longer items are cheaper per minute). Events and rewards grant
speed-ups by this table so their value is comparable across the game.

## 8. Retention numbers to design against

Design targets used across the genre (validate on our own cohorts):
D1 40%+, D7 15–20%, D30 6–10% for a healthy launch in this genre; session
count 4–8/day for engaged players; session length median 6–12 min. A
system that adds a reason to come back at a specific time (a march lands,
a building finishes, an event opens) supports D1/D7; a system that adds
standing among other players supports D30+.

## 9. Sanity checks before any table ships

- Monotonic: no level is cheaper or faster than the one before.
- No dead levels: every level grants something the player can see.
- Round numbers at display (1.2 h not 1.19 h), exact numbers in data.
- Every multiplier stacks additively inside a category, multiplicatively
  across categories — and the spec says which is which.
