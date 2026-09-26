# SYSTEM.md — the design spec contract

Every design lands as `design/<system>/SYSTEM.md` (plus `tuning.json` /
`tuning.csv` and the econ/curve outputs beside it). Copy this skeleton.
Sections marked ★ are mandatory; a spec missing one is returned, not reviewed.

```markdown
# <System name> — <diegetic name in the realm>        status: DRAFT | REVIEWED | SHIPPED

## ★ 1. The four questions
- Want:     what the player wants next here (power / progress / standing / collection / mastery / story)
- Obstacle: what stands between them and it
- Wait:     how long, in real minutes, for the three player types
- Witness:  who else sees them get it (alliance feed, map, city visual, title, ranking)

## ★ 2. Why now
Audit area + score, backlog line, owner order or ledger id that asked for it.

## ★ 3. Benchmark → pattern → our move
| Genre does | Pattern (our words) | Where it hurts players | Our move |
|---|---|---|---|
(one row per borrowed pattern; benchmark.md section cited)

## ★ 4. Rules of the system
Plain numbered rules a player could read. Every noun defined once.
The loop it feeds (core-loop.md layer: 30 s / session / day / week / season).

## ★ 5. Numbers
- Formulas (with every constant named and justified).
- Tuning table: first, 25%, 50%, 75% and last level/tier at minimum.
- `curve.py` output for timers; `econ_sim.py` output (day 1/7/30/90,
  free/light/heavy) for anything that creates or spends resources.
- The free-player path length to the top (SKILL.md rule 6).

## ★ 6. Data and code
Owning skill · data files (`data/*.gd`) · new fields · SAVE MIGRATION (old
saves load, defaults chosen) · server fields and their write rate.

## ★ 7. Server cost
Writes/reads per player per day × 50,000 players → € at current pricing,
with the formula. Measured by `core/sd_cost_probe.gd` when it touches the cloud.

## ★ 8. Harness
The probe/audit that proves it and the exact verdict line it must print.
Metrics to watch after ship (retention cohort, session count, sink ratio…).

## 9. UX
Where it lives in the castle/realm, entry points, the red-dot rule it obeys
(ux.md), the one-hand flow in taps.

## 10. Exploits and abuse
Multi-account, feeder farms, alliance hopping, time-zone play, refunds, bots.

## 11. Fiction
Names, the voice (story-forge canon), what the painted art must show.

## ★ 12. Owner decisions required
Anything touching sacred constants, spend, the money-law, or shipped art.
Empty is a valid answer; missing is not.

## 13. Predictions vs results (filled after ship)
| metric | predicted | measured | gap → lesson |
```

## Reviewing a spec (the reviewer's pass)

1. Every ★ section present and specific (no "TBD" in 1, 5, 7, 8, 12).
2. Numbers reproduce: re-run the curve/econ commands in section 5.
3. Red-team checklist in SKILL.md — all ten, each with one line of evidence.
4. One writer per file in section 6; the save migration is real code, named.
5. Verdict: `REVIEWED` with the reviewer's initials and date, or a numbered
   list of returns.
