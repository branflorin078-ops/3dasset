# Explain — the "why you won / why you lost" engine

Pillar 5 of the game-director scorecard: **the player can say why they won or lost**. The genre
fails here: its counter bonus is about 5% and disappears under stat stacks, so players decide
that "only raw power matters" (design-forge `benchmark.md`). Our counters are bigger
(design-forge `combat.md` proposes +20–50%) and battle-forge shows every counter as it lands.
This engine closes the loop: after the battle it names the edges that decided it, with a number,
in one plain sentence each, and gives one next step.

**Three laws.** (1) No sentence without a number behind it: every cause row comes from the
ledger, and every noun in it (a line, a tier, a lord) comes from the record. (2) The engine
ranks what happened; it never guesses what the player "should have felt". (3) Both players read
the same numbers with opposite signs: `net(A) = −net(B)` for every factor.

Every threshold here is a **PROPOSAL** (tuned by the fidelity probe, [qa.md](qa.md) §4). Rule
constants (counter bonus, tier quality, mass exponent, wall mitigation, loss buckets) are
design-forge `combat.md`'s; the resolver is gameplay-forge's frozen shape; the record is
[schema.md](schema.md). The reference implementation is `tools/report_tool.py` (`explain`).

## 1. The unit: casualty power

- **cp** (casualty power) of a hit = troops it put out of action (all three buckets: lightly
  wounded, infirmary, dead) × power per unit of the target's tier (design-forge `numbers.md` §3).
  Power is the one number players already compare, and it weighs a tier-7 knight above a
  tier-1 levy, so "casualties" never means "bodies".
- `CP_s` = cp dealt by side `s` = power lost by the other side **after** enemy heals
  (record field `s[o].lp`).
- `T = CP_A + CP_B` — the size of the battle. Every ledger value is stored in **per mille of
  T** (‰, signed int). 50‰ = 5% of all the power that fell in this battle.
- **Margin** for the viewer `v` (other side `o`): `m = round(1000 · (CP_v − CP_o) / T)`.

## 2. The ledger — eight factors per side

| # | Factor | Measures | Neutral (multiplier = 1) | Credited to |
|---|---|---|---|---|
| 0 | counter | the counter bonus on a hit (combat.md's counter graph) | the pair is not a counter | the hitting side |
| 1 | tier | quality of the hitting unit vs the hit unit | same tier | the hitting side (can be < 0) |
| 2 | numbers | stack size of the hitter vs the target (mass term `N^α`, numbers.md §4) | equal stacks | the hitting side (can be < 0) |
| 3 | lord | lord skills (100%), lord stat bonuses after combat.md's lord cap | no lord | the lord's side; an enemy heal is booked here as a **negative** entry on the side whose damage it undid |
| 4 | stats | research, alliance research, boosts (from the march snapshot) | equal bonuses | the hitting side |
| 5 | defences | wall mitigation at full durability (< 0 on the attacker), towers and traps (100%, the castle side) | no structure | wall: the attacker (negative); towers/traps: the castle side |
| 6 | siege | wall mitigation removed by wall damage; engine hits on troops (100%) | undamaged wall | the attacker |
| 7 | other | multipliers nobody tagged (grade 1 only, §2.2) | — | never shown; QA flag at ≥ 100‰ |

Stored as `why.f = [[8 ints for side A], [8 ints for side B]]`. The **neutral** part of a side
is not stored: `neutral_s = round(1000 · CP_s / T) − Σ f[s]` and must be ≥ 0 (checked).

### 2.1 Splitting one hit — log-mean (LMDI) attribution

A hit carries multipliers `m_f` relative to the neutral battle (table above). With
`R = Π m_f`, the neutral part of its cp is `cp / R`, and the extra part `cp · (1 − 1/R)` is
split across factors in proportion to `ln m_f`:

```
extra_f = cp · (1 − 1/R) · ln(m_f) / ln(R)     when |ln R| ≥ 1e-6
extra_f = cp · ln(m_f)                          when |ln R| <  1e-6   (the limit)
Σ_f extra_f + cp / R = cp                       (exact: no residual)
```

This is the Log-Mean Divisia Index (Ang, 2004): the standard exact, order-free additive split of
a product of factors. Order-free matters: a counter applied "before" or "after" a stat bonus
gets the same credit.

Beats that have no neutral version are booked whole: a skill hit → 100% lord; tower fire and
traps → 100% defences; an engine shot that kills troops → 100% siege. An engine hit on a
structure has no cp: its effect appears later as siege credit on the hits that pass the
weakened wall. A heal of `h` cp by side B's lord → `f[A][lord] −= h` (it undid A's damage).

GDScript shape for the report builder (cloud-forge runs it right after the resolver; names to
confirm):

```gdscript
func book_hit(side: int, cp: float, mult: Dictionary) -> void:   # mult: {factor_id: m}
	var ln_r := 0.0
	for f in mult: ln_r += log(mult[f])
	var r := exp(ln_r)
	for f in mult:
		var share := (1.0 - 1.0 / r) * log(mult[f]) / ln_r if absf(ln_r) >= 1e-6 else log(mult[f])
		ledger[side][f] += cp * share
	neutral[side] += cp / r
```

### 2.2 Two grades — no change to the frozen resolver

| Grade (`why.g`) | Source of the multipliers | When |
|---|---|---|
| **0 — derived** (default) | rebuilt per beat from the start block (lines × tiers × counts, lord pair, structures), the march snapshots (stat and lord bonuses) and combat.md's published constants; running stack counts are tracked by subtracting each beat's losses | always available; needs no resolver change (the shape is frozen; battle-forge `beats.md` §1 also derives its counter flag client-side) |
| 1 — exact | per-hit factor accumulators emitted by the resolver itself | only if gameplay-forge adds them in a sanctioned resolver version; then `other` collects any multiplier without a tag |

Grade-0 reconstruction table (PROPOSAL — map every row to the shipped resolver term, file:line):

| Factor | Grade-0 multiplier per hit | Constant owner |
|---|---|---|
| counter | `1 + c(hitter line, target line)` if the pair is in the counter graph | combat.md counter table |
| tier | `Q(hitter tier) / Q(target tier)` | combat.md tier quality (if only power is published: `(p_a/p_d)^β`, β stated in combat.md) |
| numbers | `(N_hitter / N_target)^α` with the stack counts at that beat | numbers.md §4 α, fixed in the resolver |
| lord | `(1 + L_hitter) / (1 + L_target)`, L after the lord cap | combat.md lord cap; lords.md |
| stats | `(1 + S_hitter) / (1 + S_target)` | march snapshot (cloud-forge) |
| defences | `1 − w0` on attacker hits into a walled castle (w0 = mitigation at full durability) | combat.md wall rules |
| siege | `(1 − w_now) / (1 − w0)` on the same hits (≥ 1 once the wall is damaged) | combat.md; siege-forge engine stats |

### 2.3 Evidence stored beside the ledger

| Field | Content | Used by |
|---|---|---|
| `why.c[s]` | the top counter matchup of side s: `[hitter line, tier, target line, tier, ‰]` | the counter sentence, the "Next" line |
| `why.t[s]` | the top **positive** tier matchup of side s, same shape | the tier sentence |
| `why.s` | mean stat bonus per side in ‰ (+12% = 120) | the stats sentence |
| rows, lords, `st`, `mo` | counts, lord casts, wall state, gate moment | numbers, lord, defences, siege sentences |

A counter bonus only adds damage, so `f[s][counter] ≥ 0` and `why.c[s][4] ≤ f[s][counter]`;
skill hits are 100% lord, so `f[s][lord] ≥ (skill cp − enemy heals)/T`; towers and traps are
100% defences. `report_tool.py check` enforces all three.

### 2.4 First-order honesty

The ledger books each hit where it happened. It does not follow the knock-on effect (a counter
that kills early also removes enemy hits later). That compounding lands in the neutral gap, so
the ledger **under-counts** the big causes. Result: "Without this edge, you would have lost" is
claimed only when it is true even without the compounding — conservative by construction —
and the fidelity probe checks it against knockout re-runs ([qa.md](qa.md) §4).

| Fails when | Caught by |
|---|---|
| A resolver multiplier has no factor mapping (its effect hides in "neutral") | [ ] grade-1 `other` ≥ 100‰ flag; grade 0: fidelity probe sign agreement < 95% |
| The ledger shows a counter where no counter pair fought | [ ] `check`: `why.c` names a pair from the counter graph, with lines/tiers present in both sides' rows |
| Heals make a side's ledger exceed what it dealt | [ ] `check`: neutral ≥ 0 per side; heals booked negative on the healed-against side |

## 3. The ranking algorithm (identical on server, client and tool)

| Constant | Value | Why this number |
|---|---|---|
| `T_SHOW` | 50‰ | below 5% of the battle, rounding plus the first-order error (fidelity probe) is as large as the signal |
| `T_MAIN` | 250‰ | a quarter of all power that fell: "the main reason" is literally true |
| `FLIP_SAFETY` | 1.25 | a flip claim needs 25% headroom over the margin, because the ledger is first-order |
| `T_CLOSE` / `T_BIG` | 100‰ / 500‰ | margin words: close < 10%, clear 10–49%, crushing/heavy ≥ 50% |
| `MAX_ROWS` | 3 | three rows fit the Why strip at 1080 px without scrolling ([layouts.md](layouts.md) §2) |
| `T_OTHER_WARN` | 100‰ | untagged share that means the factor mapping is incomplete |
| `ACTION_ORDER` | counter, lord, numbers, tier, defences, siege, stats | tie order: what the player can change soonest first (next march → rally → training → castle → research) |

Steps for viewer `v` (`o = 1 − v`):

1. `T = CP_A + CP_B`. If `T = 0`: the key is `rpt.why.empty` when the losing side sent 0 troops,
   else `rpt.why.even`. Skip to step 9.
2. `n_f = f[v][f] − f[o][f]` for every factor except `other`.
3. Outcome from `win`: win / loss / draw. Margin `m` as in §1.
4. Pools: `pos = {n ≥ +T_SHOW}`, `neg = {n ≤ −T_SHOW}`. Win: main = pos, counterpoint pool = neg.
   Loss: main = neg, pool = pos. Draw: main = pos ∪ neg, no pool.
5. Sort main by the **displayed** percent `|round(n/10)|`, largest first; equal displayed percents
   by `ACTION_ORDER`. (Sorting by the displayed value means the bars always read in order.)
6. Drop a cause whose evidence is missing (QA flag `no_evidence`). Keep the first `MAX_ROWS`;
   the rest go to Details as `hidden_rows`.
7. Label row 1 (§5): FLIP, else MAIN, else nothing.
8. Counterpoint: the first of the pool under the same sort, one row, headed
   `rpt.why.despite` (win) or `rpt.why.still` (loss). A loser always sees what went well when
   anything did.
9. Advice (§6) from the strongest cause **against** the viewer: loss → row 1; win → the
   counterpoint if negative; draw → the first negative row; loss or draw with none → `even`.
10. Headline Why line = row 1's sentence (+ its label sentence), else the even/empty sentence.

| Fails when | Caught by |
|---|---|
| The two players see different numbers for the same factor | [ ] `check`: `nets(pov 0) = −nets(pov 1)` for every fixture |
| Bars read out of order (6%, 7%, 5%) | [ ] test: equal displayed percents only fall back to `ACTION_ORDER` |
| A 4.9% cause is shown, or a 5.0% cause is hidden | [ ] boundary tests at 49‰ / 50‰ |

## 4. Cause sentences

`for` = the edge was the viewer's; `against` = it was the enemy's. Params come from the
evidence named. English ≤ 64 characters after filling (§7).

| Factor | Key | English | Params from |
|---|---|---|---|
| counter | `rpt.why.counter.for` | Your {a_line} countered their {d_line}. | `why.c[v]` |
| counter | `rpt.why.counter.against` | Their {a_line} countered your {d_line}. | `why.c[o]` |
| tier | `rpt.why.tier.for` | Your tier-{a_tier} {a_line} outclassed their tier-{d_tier} {d_line}. | `why.t[v]` |
| tier | `rpt.why.tier.against` | Their tier-{a_tier} {a_line} outclassed your tier-{d_tier} {d_line}. | `why.t[o]` |
| numbers | `rpt.why.numbers.for` | You had more troops: {n_v} against {n_o}. | Σ sent per side |
| numbers | `rpt.why.numbers.against` | They had more troops: {n_o} against your {n_v}. | Σ sent per side |
| lord | `rpt.why.lord.for` (P) | {lord}'s {skill} struck {casts} times. | lord with most dealt + healed; its most-cast skill |
| lord | `rpt.why.lord.against` (P) | Their lord {lord}'s {skill} struck {casts} times. | same, enemy side |
| lord | `rpt.why.lord.for_heal` (P) | {lord}'s {skill} healed your troops {casts} times. | when that lord healed more than it dealt |
| lord | `rpt.why.lord.against_heal` (P) | Their lord {lord}'s {skill} healed them {casts} times. | same, enemy side |
| stats | `rpt.why.stats.for` | Research and boosts: your +{s_v}% against their +{s_o}%. | `why.s` |
| stats | `rpt.why.stats.against` | Research and boosts: their +{s_o}% against your +{s_v}%. | `why.s` |
| defences | `rpt.why.defences.for` | Your wall held at {wall}% and {towers} towers fired. | `st` end durability, tower count |
| defences | `rpt.why.defences.against` | Their wall held at {wall}% and {towers} towers fired. | `st` |
| defences | `rpt.why.defences.for_fell` | Your wall and towers held them until the gate fell. | a gate moment (kind 3) exists |
| defences | `rpt.why.defences.against_fell` | Their wall and towers held you until the gate fell. | same |
| siege | `rpt.why.siege.for` | Your siege engines wore their wall down to {wall}%. | `st` |
| siege | `rpt.why.siege.against` | Their siege engines wore your wall down to {wall}%. | `st` |
| siege | `rpt.why.siege.for_gate` | Your siege engines broke their gate. | gate moment |
| siege | `rpt.why.siege.against_gate` | Their siege engines broke your gate. | gate moment |
| — | `rpt.why.even` | An even fight: no edge was worth {pct}% of the battle. | `T_SHOW` |
| — | `rpt.why.empty` | They had no troops to fight. | `T = 0`, loser sent 0 |
| — | `rpt.why.despite` / `rpt.why.still` | Despite this: / What went well: | counterpoint header |

Wall percent in a sentence is the same number battle-forge uses for the wall state
(intact 67–100%, cracked 34–66%, holed 1–33%, breached 0% — battle-forge `defence.md` §6), and
the layout shows the state word beside it. The counter row's icon is the battle-forge counter
medallion pair (hitter line → chevron → target line; GILT rim for, IRON rim against —
battle-forge `presentation.md` §4), so the player meets one visual word in the march form,
the battle and the report.

## 5. The label and the margin word

| Label (row 1 only) | Condition | Key |
|---|---|---|
| FLIP | end reason is casualty-decided (annihilated, routed, withdrew, recalled) **and** `sign(m)` agrees with the outcome **and** `|n₁| ≥ 1.25 · |m|` | `rpt.why.flip.win` "Without this edge, you would have lost." / `rpt.why.flip.loss` "Without this edge, you would have won." |
| MAIN | not FLIP and `|n₁| ≥ 250‰` | `rpt.why.main` "This was the main reason." |
| none | otherwise | — |

Castle ends (wall held, gate broken) never get FLIP: the result there is decided by the gate,
not by the casualty balance, so a casualty counterfactual would not be honest.

| `|m|` | Win | Loss | Draw |
|---|---|---|---|
| < 100‰ | `rpt.margin.win.close` close | `rpt.margin.loss.close` close | `rpt.margin.draw.close` even |
| 100–499‰ | `rpt.margin.win.clear` clear | `rpt.margin.loss.clear` clear | `rpt.margin.draw.clear` even |
| ≥ 500‰ | `rpt.margin.win.big` crushing | `rpt.margin.loss.big` heavy | `rpt.margin.draw.big` even |

Outcome words: `rpt.outcome.win` Victory · `rpt.outcome.loss` Defeat · `rpt.outcome.draw` Both
withdrew · for the castle side of a castle battle `rpt.outcome.held` Castle held /
`rpt.outcome.breached` Castle breached.

## 6. "Next" — one step, always play, never the shop

| Cause against the viewer | Key | English | Link (deep link, 1 tap) |
|---|---|---|---|
| counter | `rpt.next.counter` | Send {c_line} against {d_line}. | `train(c_line)`; `c_line` = the line that counters their hitting line in combat.md's graph |
| tier | `rpt.next.tier` | Raise your {line} to tier {tier}. | `train(line)` (muster yard of that line) |
| numbers | `rpt.next.numbers` | Send a bigger march, or call a rally. | `rally` |
| lord | `rpt.next.lord` | Scout first to see their lords, then answer them. | `scout` |
| stats | `rpt.next.stats` | Their research is ahead: continue military research. | `research` |
| defences | `rpt.next.defences` | Break the wall first: bring siege engines. | `siege` |
| defences, engines were sent | `rpt.next.defences_more` | Bring more siege engines to open the wall sooner. | `siege` |
| siege | `rpt.next.siege` | Repair your wall and ask allies to reinforce. | `wall` |
| none (loss or draw) | `rpt.next.even` | Scout before the next attack. | `scout` |

1. **Allowed link targets**: train, rally, scout, research, siege, wall, infirmary, replay.
   Reports are war screens (design-forge `monetization.md` §10): no shop, no gem price, no offer,
   no ward for sale — the infirmary link opens the infirmary, whose gem finish shows hourglass
   art only.
2. One Next line per report. After a defeat the battle-forge outcome card offers "Try
   {counter line}" with the march form pre-filled (battle-forge `flows.md` §9 flow F); it takes
   the same `c_line` from this table, so the two never disagree.
3. The imperative is advice, never blame: no "you should have", no "mistake", no "!".

## 7. Loss notes, the key list and l10n rules

Loss notes (own side only, in this order — what comes back first):

| Key | English | When |
|---|---|---|
| `rpt.loss.light` (P) | {n} lightly wounded recover by themselves. | own light > 0 |
| `rpt.loss.hosp` (P) | {n} severely wounded are in your infirmary. | own infirmary > 0 |
| `rpt.loss.hosp_full` (P) | Your infirmary was full: {n} severely wounded died. | participant `ho` > 0 |
| `rpt.loss.lc.0` | Defending your castle: severely wounded go to your infirmary. | loss context 0 |
| `rpt.loss.lc.1` | Field battle: severely wounded go to your infirmary. | 1 |
| `rpt.loss.lc.2` | Attacking a castle costs more lives (war rules). | 2 |
| `rpt.loss.lc.3` | Camp fight: losses follow the camp rules. | 3 |
| `rpt.loss.lc.4` | Alliance structure: losses follow the war rules. | 4 |
| `rpt.loss.lc.5` | Defending an ally: losses follow the war rules. | 5 |
| `rpt.loss.none` | No losses. | own out of action = 0 |

The context names map to combat.md's context table; its exact percentages are shown on tap
(Details), read live from combat.md's data, never stored in the report.

Headline keys ([layouts.md](layouts.md) §1): `rpt.head.vs` "vs {name} [{tag}] · {place} {x}:{y}",
`rpt.head.vs_notag` "vs {name} · {place} {x}:{y}" (camps, strongholds), `rpt.head.enemy_out`
"Enemy out of action {n}", `rpt.head.taken` "Taken {n} {res}", `rpt.head.home_wounded` "Wounded
coming back {n}", `rpt.head.lost` "Lost {n}", `rpt.head.your_out` "Your wounded {n}".

l10n rules (l10n-forge ships the tables; `tools/strings_en.json` is the key list):

1. Named params only (`{a_line}`), so a language can reorder the sentence; Godot
   `tr(key).format(dict)` and Python `str.format(**dict)` fill the same templates.
2. A number is never followed by a counted noun ("Lost 2,180", not "2,180 troops lost") — except
   keys marked **(P)**, which use plural forms (`tr_n()`, gettext PO; CSV tables cannot carry
   plurals).
3. English ≤ 64 characters after filling with the longest params; every language gets +40% room
   in the layout (ui-forge) — the pseudo-locale pass in [qa.md](qa.md) §3 proves it.
4. Line names sit in subject or object position; languages with cases may add
   `troop.line.<id>.acc` forms — the param names stay the same.
5. Player names are resolved at view time from the player id ([schema.md](schema.md) §5);
   a deleted account shows `rpt.name.gone` "A lord who left the realm".

## 8. Checklist — changing the engine or a sentence

- [ ] Threshold changes are made in this file, `tools/report_tool.py` and the Godot builder together; the tests' boundary cases re-run.
- [ ] Every new sentence key is in `tools/strings_en.json` **and** in §4/§6/§7 of this file (the test fails otherwise).
- [ ] Each sentence names only things present in the record (line, tier, lord, count) — `check` passes on all fixtures.
- [ ] `python tests/test_report_tool.py` prints `REPORT TOOL OK - <n> checks`.
- [ ] Golden outputs regenerated (`report_tool.py golden`) and `report_probe` green ([qa.md](qa.md) §2).
- [ ] Fidelity probe re-run when a combat.md constant changes ([qa.md](qa.md) §4).
- [ ] No link target outside §6 rule 1; no advice that names a price or a purchase.
