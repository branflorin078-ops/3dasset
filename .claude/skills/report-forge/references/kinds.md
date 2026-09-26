# Kinds — what each report adds to the common record

Every battle kind shares one record ([schema.md](schema.md) §3), one engine
([explain.md](explain.md)) and one layout ([layouts.md](layouts.md)). This file lists what each
kind adds, who sees what, and its own failure modes. Scout reports are [scout.md](scout.md).
All numbers are **PROPOSALS**; rules (loss buckets, loot, rally size, camp rewards) are
design-forge `combat.md`, `world.md` and `alliance.md`.

| Kind | `k` | Typical volume per active player per day (PROPOSAL, for [storage.md](storage.md)) | Alert level for mail-forge |
|---|---|---|---|
| Field battle (incl. interception, node fights) | 1 | 0.5–5 involvements | normal; alert if the player was attacked |
| Castle battle — attack report / defence report | 2 | 0.2–3 | defence report = alert |
| Rally battle | 3 | 0–1 | normal |
| Hunt (1–5 camps) | 4 | 2–5 | silent (grouped per day) |
| Scout report / scouted alert | 5 / 7 | 0–6 / 0–6 | scout = normal; scouted = alert |
| Gather trip | 6 | 2–6 | silent (grouped per day) |

## 1. Field battle (k = 1)

The base case: both sides are marches (an interception, a fight over a resource node, a single
camp or outpost fight that went badly and needs a detail record). Resources: an attacker who
beats a gathering march carries off its load up to his own load capacity (`rs`, `ld`); the
gatherer's report shows "Plundered {n} {res}" as its second headline number.

| Fails when | Caught by |
|---|---|
| The loser's load disappears without a line in his report | [ ] fixture `win_field` pov 1: headline shows "Plundered 84,000 wood" |
| A camp fight with no player on side B shows "A lord who left the realm" | [ ] id 0 → "The garrison" (`rpt.name.garrison`) |

## 2. Castle battle (k = 2): the attack report and the defence report

One record, two points of view. The castle side (`st` present) is side B.

| Part | Attacker sees | Castle owner sees |
|---|---|---|
| Outcome word | Victory / Defeat | Castle held / Castle breached |
| Place | "Castle 398:405" | "Your castle 398:405" |
| Wall | end durability and state word (intact / cracked / holed / breached — the same bands as battle-forge `defence.md` §6) | same, plus "Repair wall" as Next when damaged |
| Resources | taken (`rs`), load used | plundered (`rs`) and **protected** (`rp`, owner only) |
| Before contact (`da`) | never | what the defender did and when: recall, allies arrived, healed, garrison lord set |
| Stationed allies | as one side with several participants | each ally listed with their own out-of-action total |

**Before contact** closes the promise in battle-forge `defence.md` §8 ("Doing something must
visibly matter — the report names it"):

| `da` kind | Key | English | Shown when |
|---|---|---|---|
| 1 recall | `rpt.act.1` (P) | Your recall brought {n} troops home {t} before contact. | a recalled march arrived before contact |
| 2 ally arrived | `rpt.act.2` (P) | {name} arrived with {n} troops {t} before contact. | a reinforcement arrived in time |
| 3 healed | `rpt.act.3` (P) | You healed {n} troops {t} before contact. | a heal finished inside the Near band |
| 4 garrison lord | `rpt.act.4` | {lord} took the garrison {t} before contact. | the garrison lord was swapped |

If the wall reaches 0 (gate broken), the defence report adds combat.md's consequence line
(burning state or relocation — whichever combat.md chooses), read live from its rule text,
with the repair time as a duration ("Full in 1 h 10 m"), never as a rate.

**Stationed allies** (defending an ally's castle): each ally opens the same record; their own
participant rows are their "own side" view (bucket split, infirmary note, loss context 5
"Defending an ally"), and the castle owner's split stays private to the owner.

| Fails when | Caught by |
|---|---|
| A defender who recalled a march in time is not told it mattered | [ ] fixture with `da`: the recall line renders for the castle side only |
| The attacker learns the defender's protected resources | [ ] projection test: `rp` absent from the attacker's and the share view |
| An ally's report shows the owner's infirmary split | [ ] projection per participant: only the viewer's own rows keep 7 fields |

## 3. Hunt (k = 4) — up to 5 camps, one record

A hunt order sends one march through up to 5 barbarian camps in a row (design-forge
`core-loop.md` A6). One report per hunt, not five:

```json
{"v":1,"id":"91c3e5a7b2d04f68","k":4,"ts":1790410800,"rv":12,"at":[405,380],
 "hu":[[7,1,40,60,0,420],[7,1,35,55,0,420],[8,1,60,90,0,480],[8,1,55,80,0,480],[9,0,210,330,0,120]],
 "rw":[[1101,3],[1204,1]],"rs":[12000,18000,18000,6000,2400],"d":"3d8e1f5a9c2b7046"}
```

| Field | Meaning |
|---|---|
| `hu` | per camp: `[camp level, won 1/0, light, infirmary, dead, lord xp]` |
| `rw`, `rs` | item rewards `[item id, qty]` and resources for the whole hunt |
| `d` | id of a k = 1 detail record for the first **lost** fight (so the engine can explain it); absent when all were won |

Headline `rpt.hunt.head` "Hunt: {won} of {n} camps cleared" (win count first), then rewards; a
lost camp shows its Why line from the detail record, `rpt.hunt.why` "Why (camp {level}): {why}" —
e.g. "Why (camp 9): Their tier-9 spearmen outclassed your tier-6 infantry." (camp garrisons use
the five lines; world.md decides their mix). Won camps get no Why (nothing to learn; it would be noise ×24 a day). mail-forge
groups a day of hunts into one thread. Size: 258 B minified, 177 B gzip.

| Fails when | Caught by |
|---|---|
| 24 camp fights create 24 inbox rows a day (red-dot fatigue, storage) | [ ] one record per hunt; mail-forge daily grouping |
| A lost camp gives no reason | [ ] every `hu` row with won = 0 has a `d` detail record |

## 4. Gather trip (k = 6)

```json
{"v":1,"id":"4f7a2c9e1b3d5068","k":6,"ts":1790410800,"rv":12,"at":[412,388],"pl":[4,4],
 "dur":14400,"g":[0,0,96000,0,0],"b":250,"lx":[[2,600]]}
```

`dur` seconds gathered, `g` resources brought home, `b` bonus ‰ (alliance territory and research,
economy.md), `lx` lord xp. A march attacked while gathering produces a **field battle** report
instead (§1), with the load lost as plunder; the gather report is then not written. Size: 142 B
minified, 129 B gzip; kept 7 days.

## 5. Rally battle (k = 3)

| Part | Rule |
|---|---|
| Participants | leader first; ≤ 30 per side (alliance.md decides the cap); each participant's own rows |
| Lords | only the leader's lord pair fights (PROPOSAL, combat.md decides); joiners' rows have no `l` |
| Rally share | each participant's damage dealt ÷ the side's total, sorted; "You: 22% (2nd of 3)" |
| Rewards | stronghold and large-camp rewards by damage share (world.md) — shown per participant from this table, so the reward and the report never disagree |
| Late joiners | a moment of kind 6 "An ally arrived" at the beat they joined; their share is still counted from that beat |
| Why | the same engine on the whole side: a rally is one army to the resolver |

The Rally share section never labels anyone "worst" and never ranks troops-per-damage: small
accounts filling a rally is the free player's real role in the genre (design-forge
`benchmark.md` §9), and shaming it drives them out. Size: 746 B for 3 attackers; 1,306 B / 549 B
gzip at 12; 2,440 B / 854 B gzip at 30 (synthetic, `size --rally N`).

| Fails when | Caught by |
|---|---|
| Rally rewards and the report's share table differ | [ ] rewards computed from the same `dealt` sums (world.md reward probe reads the record) |
| A 30-player rally record exceeds its budget | [ ] test: synthetic 30 ≤ 1,200 B gzip |

## 6. Checklist — adding a report kind

- [ ] A `k` value appended to [schema.md](schema.md) §2, fields in a table with bytes and privacy.
- [ ] Volume per player per day added to [storage.md](storage.md) §2 and `cost` re-run.
- [ ] Alert level agreed with mail-forge; grouping rule for anything above 3 a day.
- [ ] A fixture in `tests/fixtures/`, `check` extended, `REPORT TOOL OK` re-run.
- [ ] If it has a winner and a loser, it uses the engine; if not, it says so in its headline.
