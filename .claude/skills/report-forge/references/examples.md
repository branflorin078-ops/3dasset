# Examples — two reports worked from hits to screen

Two complete reports: a close **win** decided by a counter, and a castle attack **lost** at the
wall. Each goes the whole way: the hits the resolver produced → the ledger → the ranking → the
text on screen, for both players. Everything is reproducible:

```
python tools/report_tool.py ledger tests/hits/win_field.hits.json      # hits -> why block
python tools/report_tool.py explain tests/fixtures/win_field.json      # ranking + full text
python tools/report_tool.py render tests/fixtures/win_field.json --pov 1
```

`tests/test_report_tool.py` fails if the fixture's why block differs from the ledger of its hits.

**Example assumptions — NOT shipped values** (design-forge `combat.md` and `numbers.md` own the
real ones): power per unit t4 5 · t5 8 · t6 11 · t7 15 (numbers.md §3, p1 = 2, k = 1.4, rounded);
counter bonus +50% (the top of combat.md's proposed +20–50%); tier step ×1.18 per tier of
difference; mass exponent α = 0.6 on army totals (the builder uses the running stack counts);
counter graph (combat.md PROPOSAL): spearmen > cavalry, cavalry > archers and crossbows,
archers > infantry, infantry > spearmen. Lord names are canon; **skill names are placeholders**
(lords.md and commander-forge own them).

## 1. Worked example 1 — a close win by a counter

**Situation.** Brannoc [GRY] intercepts Garrick [RVN], who is gathering at a level-4 lumber camp
(412:388). Brannoc: Elena (primary) + Rowan, 6,000 tier-6 archers, 3,000 tier-5 infantry,
1,000 tier-5 cavalry = 10,000. Garrick: Edwin + Maud, 7,000 tier-6 infantry, 3,000 tier-5
spearmen, 1,500 tier-4 archers = 11,500. Garrick's line breaks at beat 38 (routed). Field
context: 30% of the fallen are lightly wounded, 70% go to the infirmary, nobody dies unless an
infirmary is full (example split; combat.md decides).

**Losses and power.** Brannoc: 600 archers, 1,700 infantry, 400 cavalry → 6,600 + 13,600 + 3,200
= **23,400** power. Garrick: 1,900 infantry, 400 spearmen, 480 archers → 20,900 + 3,200 + 2,400 =
**26,500**. `T = 49,900`. Margin for Brannoc `m = 1000 · (26,500 − 23,400) / 49,900 = 62‰`
→ "close".

**Hits → ledger** (grade 0, [explain.md](explain.md) §2.1). Side multipliers: numbers
(10,000/11,500)^0.6 = 0.9196 for Brannoc's hits and 1.0875 for Garrick's; lord (1.06/1.03) =
1.0291 and its inverse 0.9717; research and boosts (1.12/1.07) = 1.0467 and 0.9554.

| Hit group (hitter → target) | cp | Multipliers besides numbers, lord, stats | R | Neutral | Counter | Tier | Numbers | Lord | Stats |
|---|---|---|---|---|---|---|---|---|---|
| Brannoc archers t6 → infantry t6 | 14,500 | counter 1.5 | 1.4859 | 9,759 | 4,855 | — | −1,004 | 344 | 547 |
| archers t6 → spearmen t5 | 1,500 | tier 1.18 | 1.1689 | 1,283 | — | 230 | −116 | 40 | 63 |
| infantry t5 → infantry t6 | 3,700 | tier 0.8475 | 0.8395 | 4,408 | — | −669 | −339 | 116 | 185 |
| infantry t5 → spearmen t5 | 1,500 | counter 1.5 | 1.4859 | 1,010 | 502 | — | −104 | 36 | 57 |
| cavalry t5 → archers t4 | 1,700 | counter 1.5, tier 1.18 | 1.7533 | 970 | 527 | 215 | −109 | 37 | 59 |
| cavalry t5 → spearmen t5 | 600 | — | 0.9906 | 606 | — | — | −51 | 17 | 28 |
| Elena's and Rowan's skill hits | 3,000 | booked whole | — | — | — | — | — | 3,000 | — |
| Garrick infantry t6 → infantry t5 | 9,000 | tier 1.18 | 1.1912 | 7,555 | — | 1,367 | 692 | −237 | −377 |
| infantry t6 → archers t6 | 6,500 | — | 1.0095 | 6,439 | — | — | 542 | −186 | −295 |
| spearmen t5 → cavalry t5 | 2,400 | counter 1.5 | 1.5143 | 1,585 | 796 | — | 165 | −56 | −90 |
| spearmen t5 → archers t6 | 2,300 | tier 0.8475 | 0.8555 | 2,688 | — | −412 | 209 | −71 | −114 |
| archers t4 → infantry t5 | 2,500 | counter 1.5, tier 0.8475 | 1.2833 | 1,948 | 897 | −366 | 186 | −64 | −101 |
| Edwin's skill hits | 700 | booked whole | — | — | — | — | — | 700 | — |

Check one row by hand (the first): `R = 1.5 × 0.9196 × 1.0291 × 1.0467 = 1.4859`;
extra = 14,500 × (1 − 1/1.4859) = 4,742; counter share = ln 1.5 / ln 1.4859 = 0.4055 / 0.3960
= 1.024 → **4,855 cp**; numbers −0.0839/0.3960 → −1,004; lord → 344; stats → 547; the four sum
to 4,742 and neutral 9,759 + 4,742 = 14,500.

| Side | counter | tier | numbers | lord | stats | defences | siege | other | neutral | share of T |
|---|---|---|---|---|---|---|---|---|---|---|
| Brannoc (A) ‰ | 118 | −4 | −35 | 72 | 19 | 0 | 0 | 0 | 361 | 531 |
| Garrick (B) ‰ | 34 | 12 | 36 | 2 | −20 | 0 | 0 | 0 | 405 | 469 |
| **Net for Brannoc** | **+84** | −16 | **−71** | **+70** | +39 | 0 | 0 | 0 | | |

(118‰ = (4,855 + 502 + 527) / 49,900. Garrick's lord ends at +2‰: Edwin's 700-cp skill minus the
−614 cp his weaker lord bonus cost on every hit — why the engine has no "lord ≥ skill" rule.)
Evidence: Brannoc's top counter matchup archers t6 → infantry t6 = 97‰; Garrick's archers t4 →
infantry t5 = 18‰.

**Ranking** (explain.md §3). Win → main pool ≥ +50‰: counter +84 (8%), lord +70 (7%). Stats +39
and tier −16 stay under 5%. Label: casualty end (routed), `m = +62`, `84 ≥ 1.25 × 62 = 77.5` →
**FLIP**. Counterpoint pool ≤ −50‰: numbers −71 → "Despite this". Advice from the counterpoint
(numbers) → "Send a bigger march, or call a rally."

**Brannoc's report** (`render`, verbatim; the layout is [layouts.md](layouts.md)):

```
Victory · close
vs Garrick [RVN] · Lumber camp 412:388
Enemy out of action 2,780 · Taken 84,000 wood
Why: Your archers countered their infantry. Without this edge, you would have lost.

WHY (tap a row for its numbers)
  ▲   +8%  Your archers countered their infantry.
           Without this edge, you would have lost.
  ▲   +7%  Elena's Volley struck 4 times.
  Despite this:
  ▼   -7%  They had more troops: 11,500 against your 10,000.
  Next: Send a bigger march, or call a rally.  [Call a rally]

YOUR TROOPS              sent   light  infirm.   dead   dealt
  archers    t6       6,000     180      420      0  16,000
  infantry   t5       3,000     510    1,190      0   5,200
  cavalry    t5       1,000     120      280      0   2,300
  810 lightly wounded recover by themselves.
  1,890 severely wounded are in your infirmary.
  Field battle: severely wounded go to your infirmary.
THEIR TROOPS             sent  out of action
  infantry   t6       7,000     1,900
  spearmen   t5       3,000       400
  archers    t4       1,500       480
LORDS          lvl   dealt  healed  skill casts
  Elena  (you )  38   2,500       0  Volley ×4
  Rowan  (you )  31     500       0  Charge ×2
  Edwin  (they)  35     700       0  Rally Cry ×3
  Maud   (they)  29       0       0  Shield Wall ×1
RESOURCES  Taken: 84,000 wood (load 61% used)
TIMELINE (tap = replay from 1 s before)
  beat   4  Your archers countered their infantry.
  beat   9  Elena: Volley.
  beat  15  Their spearmen countered your cavalry.
  beat  18  Their lord Edwin: Rally Cry.
  beat  22  Elena: Volley.
  beat  27  Your cavalry countered their archers.
  beat  31  Elena: Volley.
  beat  38  Their infantry broke and fled.
REPLAY  available
```

**Garrick's report** — the same record, signs reversed (`--pov 1`):

```
Defeat · close
vs Brannoc [GRY] · Lumber camp 412:388
Wounded coming back 2,780 · Plundered 84,000 wood
Why: Their archers countered your infantry. Without this edge, you would have won.

WHY (tap a row for its numbers)
  ▼   -8%  Their archers countered your infantry.
           Without this edge, you would have won.
  ▼   -7%  Their lord Elena's Volley struck 4 times.
  What went well:
  ▲   +7%  You had more troops: 11,500 against 10,000.
  Next: Send cavalry against archers.  [Train cavalry]
```

Garrick learns the counter graph from his own defeat: archers beat his infantry, cavalry beats
archers, and the button opens the cavalry muster yard. He sees Brannoc's losses only as
"out of action" per line — never Brannoc's infirmary split ([schema.md](schema.md) §5).

**Bytes.** 834 minified, **427 gzip**; Brannoc's list line 139 B:
`{"r":"7f3c9a01d2e45b68","k":1,…,"o":0,"m":62,…,"n":[[0,2780],[1,84000,2]],"c":[0,1]}`.

## 2. Worked example 2 — a castle attack lost at the wall

**Situation.** Brannoc attacks Isolde's castle [HRT] (tier 5, 398:405) with Rowan (primary) +
Alric, 7,000 tier-7 cavalry, 2,500 tier-6 spearmen and 2 rams = 9,500 troops. Isolde defends with
Maud (primary) + Godric, 6,000 tier-7 spearmen, 3,000 tier-6 crossbows, 2,000 tier-5 archers =
11,000, a wall and 4 towers. The rams take the wall from 100% to 45% early (beat 9); the
cavalry breaks on the spearmen; Brannoc withdraws at beat 26. End: **wall held**.

Extra example assumptions: wall mitigation 30% at full durability, average durability 55%
during Brannoc's hits (siege credit (1 − 0.3 × 0.55)/0.7 = 1.1929); lord bonus Brannoc +5%,
Isolde +8%; research and boosts +12% vs +15%. Loss split (example; combat.md decides):
attacking a castle — 20% light, 80% severe of which half die; defending your own castle — 20%
light, 80% infirmary, none die; the infirmary admits the highest tier first.

**Losses.** Brannoc: 3,900 cavalry (780 light, 3,120 severe → 1,560 die by the war rule, 1,560
need beds) and 700 spearmen (140 light, 560 severe → 280 die, 280 need beds). 1,840 need beds,
1,500 are free → 1,500 cavalry admitted; **340 die for lack of beds** (60 cavalry + 280
spearmen). Power: 3,900 × 15 + 700 × 11 = **66,200**. Isolde: 1,100 spearmen, 900 crossbows,
300 archers → 16,500 + 9,900 + 2,400 = **28,800**. `T = 95,000`; `m = −394‰` → "clear".

| Hit group | cp | Multipliers (numbers 0.9158 / 1.0919, lord 0.9722 / 1.0286, stats 0.9739 / 1.0268 on every row) | R | Counter | Tier | Numbers | Lord | Stats | Defences | Siege |
|---|---|---|---|---|---|---|---|---|---|---|
| Brannoc cavalry t7 → crossbows t6 | 8,000 | counter 1.5, tier 1.18, wall 0.7, siege 1.1929 | 1.2816 | 2,873 | 1,173 | −623 | −200 | −187 | −2,527 | 1,249 |
| cavalry t7 → spearmen t7 | 11,900 | wall 0.7, siege 1.1929 | 0.7241 | — | — | −1,235 | −396 | −371 | −5,010 | 2,477 |
| cavalry t7 → archers t5 | 2,000 | counter 1.5, tier 1.3924, wall, siege | 1.5123 | 664 | 542 | −144 | −46 | −43 | −584 | 289 |
| spearmen t6 → spearmen t7 | 4,500 | tier 0.8475, wall, siege | 0.6136 | — | −960 | −510 | −163 | −153 | −2,069 | 1,023 |
| Rowan's skill hits; Maud's heal | 3,000; −600 | booked whole on Brannoc's lord | — | — | — | — | 2,400 | — | — | — |
| Isolde spearmen t7 → cavalry t7 | 36,000 | counter 1.5 | 1.7298 | 11,238 | — | 2,438 | 781 | 733 | — | — |
| spearmen t7 → spearmen t6 | 6,000 | tier 1.18 | 1.3608 | — | 855 | 454 | 145 | 136 | — | — |
| crossbows t6 → cavalry t7 | 12,000 | tier 0.8475 | 0.9773 | — | −2,009 | 1,068 | 342 | 321 | — | — |
| archers t5 → cavalry t7 | 5,600 | tier 0.7182 | 0.8282 | — | −2,040 | 542 | 174 | 163 | — | — |
| Maud's and Godric's skills; 4 towers | 2,400; 4,200 | booked whole | — | — | — | — | 2,400 | — | 4,200 | — |

| Side | counter | tier | numbers | lord | stats | defences | siege | other | neutral | share of T |
|---|---|---|---|---|---|---|---|---|---|---|
| Brannoc (A) ‰ | 37 | 8 | −26 | 17 | −8 | −107 | 53 | 0 | 330 | 303 |
| Isolde (B) ‰ | 118 | −34 | 47 | 40 | 14 | 44 | 0 | 0 | 466 | 697 |
| **Net for Brannoc** | **−81** | +42 | **−73** | −23 | −22 | **−151** | **+53** | 0 | | |

Spot checks: towers 4,200 / 95,000 = 44‰ (100% defences); Maud's 600-cp heal lowers
*Brannoc's* lord entry (it undid his damage); the wall costs Brannoc −10,190 cp (−107‰) and his
rams win back 5,038 cp (+53‰).

**Ranking.** Loss → main pool ≤ −50‰, sorted by displayed percent: defences −15%, counter −8%,
numbers −7%. Label: the end is structure-decided (wall held) → no FLIP; 151 < 250 → no MAIN.
Counterpoint ≥ +50‰: siege +53 → "What went well". Advice from row 1, defences, and Brannoc
**did** bring engines → `rpt.next.defences_more`.

**Brannoc's report** (verbatim, first 23 lines):

```
Defeat · clear
vs Isolde [HRT] · Castle 398:405
Wounded coming back 2,420 · Lost 2,180
Why: Their wall held at 45% and 4 towers fired.

WHY (tap a row for its numbers)
  ▼  -15%  Their wall held at 45% and 4 towers fired.
  ▼   -8%  Their spearmen countered your cavalry.
  ▼   -7%  They had more troops: 11,000 against your 9,500.
  What went well:
  ▲   +5%  Your siege engines wore their wall down to 45%.
  Next: Bring more siege engines to open the wall sooner.  [Siege workshop]

YOUR TROOPS              sent   light  infirm.   dead   dealt
  cavalry    t7       7,000     780    1,500  1,620  21,900
  spearmen   t6       2,500     140        0    560   4,500
  rams       ×2   lost 1, wall damage 55%
  920 lightly wounded recover by themselves.
  1,500 severely wounded are in your infirmary.
  Your infirmary was full: 340 severely wounded died.
  Attacking a castle costs more lives (war rules).
THEIR TROOPS             sent  out of action
  spearmen   t7       6,000     1,100
```

The loser reads, in order: what comes back (2,420), what is gone (2,180), the honest main
reason (the wall), the counter he walked into, the one thing that worked, and one next step.
The 340 deaths from a full infirmary get their own line — the cost of attacking with no free
beds, stated once, without blame.

**Isolde's defence report** (same record, `--pov 1`, first 12 lines):

```
Castle held · clear
vs Brannoc [GRY] · Your castle 398:405
Enemy out of action 4,600 · Your wounded 2,300
Why: Your wall held at 45% and 4 towers fired.

WHY (tap a row for its numbers)
  ▲  +15%  Your wall held at 45% and 4 towers fired.
  ▲   +8%  Your spearmen countered their cavalry.
  ▲   +7%  You had more troops: 11,000 against 9,500.
  Despite this:
  ▼   -5%  Their siege engines wore your wall down to 45%.
  Next: Repair your wall and ask allies to reinforce.  [Repair wall]
```

**Bytes.** 869 minified, **458 gzip**; Brannoc's view after the projection 432 gzip; list line
138 B. Isolde's `rp` (protected resources) is sent to Isolde only.

## 3. What the reviewer checked (and what it found)

| Check | Result |
|---|---|
| Every ledger cell = Σ of its column in the hit table ÷ T, rounded half away from zero | holds for all 32 cells (the test recomputes them) |
| A counter can add at most `1 − 1/1.5 = 33%` of a countered hit's cp | largest: 11,238 of 36,000 = 31% ✓ (a first draft had 300‰ on 17,000 counter-cp — impossible; caught and replaced by computed ledgers) |
| `Σ dealt − enemy heals = power lost by the other side` | 26,500 / 23,400 and 29,400 − 600 = 28,800 / 66,200 ✓ |
| The wall % in the sentence = the state battle-forge shows | 45% = "cracked" (34–66%) in castle, battle view and report ✓ |
| The loser's headline never says "None lost" while resources were carried off | fixed: Garrick's second number is "Plundered 84,000 wood" |
| "Bring siege engines" said to a player who brought two rams | fixed: `rpt.next.defences_more` when the attacker sent engines |
