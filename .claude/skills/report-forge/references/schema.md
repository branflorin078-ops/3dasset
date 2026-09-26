# Schema — the report record, field by field, byte by byte

One compact JSON record per event, built **on the server** at resolution time, stored gzip'd,
shared by every viewer. This file defines the record (v1), the byte budget per report, the
per-viewer projections and the inbox list line that mail-forge stores. The fixtures in
`tests/fixtures/` are valid v1 records; `tools/report_tool.py check` is the executable form
of every rule below. All numbers are **PROPOSALS** except the measured byte counts, which are
measured on the fixtures (2026-09-26, Python gzip level 6).

## 1. Principles (each one saves bytes or prevents a bug)

1. **One record per event, many viewers.** A 1v1 battle is one record read by two inboxes; a
   30-player rally is one record read by 31. Never a copy per inbox (mail-forge stores only a
   list line, §6).
2. **Built by the server, never by a client.** The report builder runs in the same job as the
   resolver (cloud-forge), from the resolver's outcome, its beat log, the start block and the
   march snapshots. A client cannot submit or edit a report (anti-cheat).
3. **Integers only.** Shares and percents are per mille (‰, 0–1000 or signed); coordinates,
   counts and power are ints. No floats: identical results in Python, GDScript and SQL.
4. **Short keys, positional rows.** Keys are 1–3 letters; repeated rows are arrays in a fixed
   order (a troop row is 7 ints). A key costs ~5 bytes per use; a positional field costs ~1.
5. **Ids, not names.** Players are stored as ids; names are resolved at view time. A renamed
   lord shows the new name; a deleted account (GDPR erasure) shows "A lord who left the realm".
   The alliance tag is stored (3–4 characters, not personal data) because it describes the
   battle as it was.
6. **Add-only versioning.** `v` = 1. New keys may be added; readers ignore unknown keys; a key
   is never repurposed. A breaking change is `v` = 2 with a reader for both.
7. **Presentation is not stored.** The timeline, act marks and highlight ticks are recomputed
   from the beat log (battle-forge `beats.md` §6). The report stores only the ≤ 8 moments that
   the Timeline section lists.

## 2. Record kinds

| `k` | Kind | Viewers | Built from | Detail |
|---|---|---|---|---|
| 1 | Field battle (open ground, resource node, interception, a single camp or outpost fight) | attacker, defender | resolver outcome + beats | this file §3 |
| 2 | Castle battle (the defender's copy is the "defence report") | attacker, castle owner, stationed allies | same | §3 + `st` |
| 3 | Rally battle (castle, stronghold, large camp) | every participant on both sides | same | §3, ≤ 30 participants per side |
| 4 | Hunt (one march, up to 5 camps in a row — core-loop A6) | the hunter | 1–5 camp resolutions | [kinds.md](kinds.md) §3 |
| 5 | Scout report | the scout | the target snapshot at arrival | [scout.md](scout.md) |
| 6 | Gather trip | the gatherer | the march at return | [kinds.md](kinds.md) §4 |
| 7 | Scouted alert | the scouted player | the scout event | [scout.md](scout.md) §5 |

## 3. The battle record (k = 1, 2, 3)

| Key | Type | Range / meaning | Private | JSON bytes (win example) |
|---|---|---|---|---|
| `v` | int | schema version, 1 | — | 6 |
| `id` | str | 16 hex chars = 64-bit random id (never sequential: no enumeration) | — | 24 |
| `k` | int | kind 1–3 (§2) | — | 6 |
| `ts` | int | unix seconds of resolution (server clock) | — | 16 |
| `rv` | int | rules version: the tuning-table version the resolver ran (gameplay-forge) | — | 8 |
| `cx` | int | battle context, battle-forge `beats.md` §1: 0 camp, 1 outpost, 2 field, 3 intercept, 4 castle, 5 rally, 6 stronghold | — | 7 |
| `at` | [x, y] | realm tile | — | 15 |
| `pl` | [type, level] | place (world.md names; PROPOSAL ids): 0 open ground, 1 castle, 2 barbarian camp, 3 farmland, 4 lumber camp, 5 quarry, 6 iron mine, 7 gold seam, 8 outpost, 9 stronghold, 10 alliance hall | — | 11 |
| `end` | int | 0 annihilated, 1 routed, 2 withdrew (round limit), 3 wall held, 4 gate broken, 5 recalled | — | 8 |
| `win` | int | 0 side A (the attacker) won, 1 side B won, 2 both withdrew | — | 8 |
| `bn` | int | number of beats in the log (moment indices point into it) | — | 8 |
| `s` | [A, B] | the two sides (below) | partly | 415 |
| `why` | object | ledger + evidence ([explain.md](explain.md) §2) | — | 144 |
| `mo` | [[i, kind, side, a, b] ≤ 8] | moments: beat index, kind (below), acting side, two params | — | 109 |
| `rs` | [5 ints] | gold, food, wood, stone, iron carried off by side A | — | 21 |
| `ld` | int ‰ | share of side A's load used | — | 9 |
| `rp` | [5 ints] | resources the castle protected (warehouse) | castle owner only | 41 (loss example) |
| `bx` | [day, bytes] | beat log kept until this day number (unix day); its gzip size | — | 18 |

**Side** `{"lc": int, "lp": int, "u": [participant…], "st": [6 ints] (castle side only)}`

| Key | Meaning |
|---|---|
| `lc` | loss context of this side, combat.md's context table: 0 defend own castle, 1 field, 2 attack castle, 3 camp, 4 alliance structure / stronghold, 5 defend an ally |
| `lp` | power this side lost (all buckets, after heals) = cp the other side dealt |
| `u` | participants, the owner/leader first (≤ 30) |
| `st` | `[wall start ‰, wall end ‰, towers, tower cp, traps, trap cp]` |

**Participant** `{"id": int, "tg": str, "l": [lord rows], "t": [troop rows], "e": [engine rows], "ho": int}` —
`id` 0 = a garrison with no player (camp, stronghold); `ho` = severely wounded who died because
the infirmary was full (private).

| Row | Fields (positional) | Bytes each (measured) |
|---|---|---|
| troop | `[line 0–4, tier 1–10 (cavalry 1–11), sent, light, infirmary, dead, cp dealt]` — line order infantry, spearmen, archers, crossbows, cavalry | 25–26 |
| lord | `[lord 0–7, role 0 primary / 1 secondary, level, cp dealt by skills, cp healed, [[skill, casts]…], xp gained]` — lord order Edwin, Alric, Elena, Rowan, Godric, Maud, Faber, Fable | 27–28 |
| engine | `[type (siege-forge catalogue), sent, lost, wall damage ‰, cp dealt to troops]` | 14–18 |
| moment | `[beat index, kind, side, a, b]` — kinds: 1 counter landed (a hitter line, b target line), 2 skill (a lord, b skill), 3 gate broken, 4 wall at a ‰, 5 rout (a line), 6 ally arrived (a participant), 7 infirmary full, 8 withdrew | 12–14 |

Invariants (all in `check`): casualties ≤ sent per row; `Σ dealt(s) − heals by the other side
= lp(other)` ±1; `neutral ≥ 0` per side; the evidence names lines and tiers present in the
rows; counter evidence is a pair of combat.md's graph; tower and trap cp ≤ the castle side's
defences credit; siege credit only with engines; moments in beat order, ≤ 8, below `bn`.

## 4. Bytes per report (measured)

| Record | Minified JSON | gzip | Opponent's view gzip | Budget (gzip) |
|---|---|---|---|---|
| Field battle, 3 lines each, 2 lords each, 8 moments (`win_field.json`) | 834 | 427 | 426 | ≤ 600 |
| Castle battle with engines and walls (`loss_castle.json`) | 869 | 458 | 432 | ≤ 600 |
| Draw, 1 line each (`even_draw.json`) | 522 | 290 | 290 | ≤ 600 |
| Rally, 3 attackers (`rally_stronghold.json`) | 746 | 382 | 379 | ≤ 600 |
| Rally, 12 attackers (synthetic, `size --rally 12`) | 1,306 | 549 | — | ≤ 1,200 |
| Rally, 30 attackers (synthetic, `size --rally 30`) | 2,440 | 854 | — | ≤ 1,200 |
| Scout, tier 2 (`scout_t2.json`) | 287 | 200 | — | ≤ 300 |
| Hunt of 5 camps (`hunt.json`) | 258 | 177 | — | ≤ 300 |
| Gather trip (`gather.json`) | 142 | 129 | — | ≤ 200 |
| Inbox list line per viewer (§6) | 129–139 | — | — | ≤ 160 minified |
| Beat log (battle-forge's, opaque) | — | ~1,800 (estimate until measured on real logs) | — | ≤ 4,000 |

Where the bytes go in the 834-byte field battle: sides 415 (50%: 6 troop rows × 26, 4 lord
rows × 28, ids and keys), why 144 (17%), moments 109 (13%), header 155 (19%), resources 30 (4%).
Estimate for any battle before building it (reproduces the fixtures within 2%):

```
minified ≈ 160 (header) + 145 (why) + 14 × moments
         + Σ sides (30 + Σ participants (45 + 26 × troop rows + 28 × lord rows + 16 × engine rows))
gzip     ≈ 0.52 × minified (1v1) · 0.42 × (12-player rally) · 0.35 × (30-player rally)
```

The beat log is 3–4× the report. That is why it has its own, shorter retention
([storage.md](storage.md) §1) and why nothing presentation-only is stored.

A "summary form" (moments dropped, tiers collapsed per line) was measured and **rejected**:
it saves only 12% of gzip bytes (427 → 376) and would cost one rewrite per record.

## 5. Projections — what each viewer is sent

The server stores the whole record and sends a **projection** (never "send all, hide on the
client": a packet sniffer would read the hidden fields).

| Field | Own side | Opponent | Share view (chat, alliance) |
|---|---|---|---|
| troop rows | full `[line, tier, sent, light, infirmary, dead, dealt]` | `[line, tier, sent, out of action, dealt]` (bucket split removed) | both sides as "opponent" rows |
| `ho` (infirmary overflow) | yes | removed | removed |
| `rp` (protected resources) | castle owner only | removed | removed |
| lord rows | full | without xp | without xp |
| `why`, `mo`, `rs`, `st`, header | yes | yes | yes |
| names | resolved at view | resolved at view | resolved at share time into the card (chat-forge) |

Why the bucket split is private: light / infirmary / dead reveals the enemy's infirmary state,
which is tier-4 scouting information ([scout.md](scout.md) §2). Both players see how many of
the other side were put out of action — that is what happened on the field.

## 6. The inbox list line (the mail-forge contract)

mail-forge stores one list line per viewer so the inbox and the report headline render with
**0 extra reads** ([layouts.md](layouts.md) §1, 0 ms headline):

```json
{"r":"7f3c9a01d2e45b68","k":1,"ts":1790431500,"o":0,"m":62,"p":51208,"tg":"RVN","pl":4,"at":[412,388],"n":[[0,2780],[1,84000,2]],"c":[0,1]}
```

| Key | Meaning |
|---|---|
| `r`, `k`, `ts` | report id, kind, time |
| `o`, `m` | outcome for this viewer (0 win, 1 loss, 2 draw) and margin ‰ |
| `p`, `tg`, `pl`, `at` | opponent id and tag, place type, tile |
| `n` | the two headline numbers as `[code, value, resource?]`; codes 0 enemy out of action, 1 taken, 2 wounded coming back, 3 lost, 4 your wounded, 5 none lost, 6 plundered (resource 0–4 = gold, food, wood, stone, iron). Win → [0, 1 or 4]; loss → [2, 3 else 6 else 5] |
| `c` | top cause `[factor, 1 for / 0 against]` → the Why line key without opening the record |

Priority, red dots, grouping, expiry and push are mail-forge's rules; report-forge only
supplies `k`, `o` and whether the viewer was the defender (alert-level reports: own castle
attacked, own castle scouted).

## 7. JSON Schema (draft 2020-12) for the battle record

```json
{"$id": "report-forge/battle-v1", "type": "object",
 "required": ["v", "id", "k", "ts", "rv", "cx", "at", "pl", "end", "win", "bn", "s", "why"],
 "properties": {
  "v": {"const": 1}, "id": {"type": "string", "pattern": "^[0-9a-f]{16}$"},
  "k": {"enum": [1, 2, 3]}, "ts": {"type": "integer"}, "rv": {"type": "integer", "minimum": 0},
  "cx": {"enum": [0, 1, 2, 3, 4, 5, 6]}, "end": {"enum": [0, 1, 2, 3, 4, 5]}, "win": {"enum": [0, 1, 2]},
  "at": {"$ref": "#/$defs/pair"}, "pl": {"$ref": "#/$defs/pair"}, "bn": {"type": "integer", "minimum": 0},
  "s": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"$ref": "#/$defs/side"}},
  "why": {"type": "object", "required": ["g", "f"], "properties": {
    "g": {"enum": [0, 1]},
    "f": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"$ref": "#/$defs/eight"}},
    "c": {"type": "array", "items": {"$ref": "#/$defs/evidence"}},
    "t": {"type": "array", "items": {"$ref": "#/$defs/evidence"}},
    "s": {"$ref": "#/$defs/pair"}}},
  "mo": {"type": "array", "maxItems": 8, "items": {"$ref": "#/$defs/int5"}},
  "rs": {"$ref": "#/$defs/res"}, "rp": {"$ref": "#/$defs/res"},
  "ld": {"type": "integer", "minimum": 0, "maximum": 1000}, "bx": {"$ref": "#/$defs/pair"}},
 "$defs": {
  "int": {"type": "integer"},
  "pair": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
  "int5": {"type": "array", "items": {"type": "integer"}, "minItems": 5, "maxItems": 5},
  "res": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 5, "maxItems": 5},
  "eight": {"type": "array", "items": {"type": "integer", "minimum": -1000, "maximum": 1000}, "minItems": 8, "maxItems": 8},
  "evidence": {"type": "array", "items": {"type": "integer"}, "maxItems": 5},
  "side": {"type": "object", "required": ["lc", "lp", "u"], "properties": {
    "lc": {"enum": [0, 1, 2, 3, 4, 5]}, "lp": {"type": "integer", "minimum": 0},
    "st": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 6, "maxItems": 6},
    "u": {"type": "array", "minItems": 1, "maxItems": 30, "items": {"type": "object", "required": ["id"],
      "properties": {"id": {"type": "integer", "minimum": 0}, "tg": {"type": "string", "maxLength": 4},
        "ho": {"type": "integer", "minimum": 0},
        "t": {"type": "array", "items": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 7, "maxItems": 7}},
        "l": {"type": "array", "maxItems": 2, "items": {"type": "array", "minItems": 6, "maxItems": 7}},
        "e": {"type": "array", "items": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 5, "maxItems": 5}}}}}}}}}
```

The schema checks shape; `check` checks meaning (sums, evidence, symmetry). Both run in the
report probe.

## 8. Failure modes and checklist

| Fails when | Caught by |
|---|---|
| A client builds or edits a report (fake victory shared to chat) | [ ] cloud-forge rule: report writes only from the resolver job; share cards carry the server id |
| The victory screen and the report show different numbers | [ ] battle-forge's outcome card reads this record's list line + projection (one source); `report_probe` compares |
| A new field silently grows every record | [ ] `size` budget test: every fixture under its row in §4 |
| The opponent's infirmary state leaks through the bucket split | [ ] projection test: opponent rows have 5 fields, no `ho`, no `rp` |
| Sequential ids let a player read others' reports | [ ] ids are 64-bit random; the API checks the viewer is a participant or holds a share token |

- [ ] New key: added to §3 with type, range, privacy and measured bytes; `check` and the JSON Schema updated; readers ignore it when absent.
- [ ] Enum value added at the end only; renderers show a neutral fallback for unknown values.
- [ ] Fixtures re-measured (`report_tool.py size tests/fixtures/*.json --rally 30`) and §4 updated.
