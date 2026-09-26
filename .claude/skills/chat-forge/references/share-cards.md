# Share cards — one envelope, six card types, built by the server

**Ownership.** chat-forge owns the share-card **format** (envelope, types, sizes, layout, access
and abuse rules). The **content** of report cards belongs to **report-forge** (what a battle,
defence, scout, rally or camp report says, its headline and its share policy); rally rules belong
to **battle-forge**; lord data to **commander-forge** / design-forge lords.md; alliance join rules
to design-forge [alliance.md](../../design-forge/references/alliance.md). Other surfaces that show
a card (mail-forge's inbox, a profile) reuse this envelope unchanged; a new type is added here
first (§8 checklist). Numbers are PROPOSALS at the 1080 × 1920 reference.

## 1. The envelope

The client sends only a **reference**; the server checks the sender may share it, builds a
**snapshot** from authoritative data, and stores both. A modified client cannot forge a
Masterwork lord, a victory or a rally.

```json
client → server   {"t":"s","c":"a:812","k":"k","card":{"type":"lord","ref":{"lord":3}},"x":"my new set","cid":"91ac2e"}
stored and sent   {"type":"lord","v":1,"ref":{"p":55123,"lord":3},
                   "snap":{"lvl":34,"tier":2,"sworn":1,"set":4},"at":1790000123}
```

| Field | Rule |
|---|---|
| `type` | one of §2; unknown types render as nothing ([channels.md](channels.md) §2 rule 4) |
| `v` | card version per type; old clients render the fields they know |
| `ref` | ids only (player, lord, report, alliance, rally, realm/x/y) |
| `snap` | server-built values at share time, ids and numbers only — names resolve on the client |
| `at` | snapshot time (unix seconds); shown as "as of 14:02" where values can change |
| Comment `x` | optional, ≤ 80 graphemes, same filter as text ([safety.md](safety.md) §1) |
| Size | envelope ≤ 256 bytes JSON; comment separate (≤ 320 bytes) |

## 2. The six types

| Type | Who may share | Channels | Snapshot fields (bytes) | Tap opens | Expires |
|---|---|---|---|---|---|
| `coord` Coordinates | anyone | all; Market Cross T1+ | tile kind, camp level or landmark key, owner id + tag (≈ 60 B) | camera focus on the tile (transition-forge realm focus), then the tile's own menu | never; live data on tap |
| `report` Battle / defence / rally / camp report | a participant | all; Market Cross T2+ | report-forge contract §4 (≤ 160 B) | report-forge's report view (read-only for others), replay if battle-forge has it | when report-forge's retention drops the report |
| `scout` Scout report | the scout's owner | all except Market Cross for T0–T1 | report-forge contract §4 | report-forge scout view, sections by its share policy | report retention; values "as of" |
| `lord` Lord | the lord's owner | all; Market Cross T2+ | lord id (1 of 8), level, rarity tier (Issued / Sound / Fine / Masterwork), sworn flag, set pieces 0–4 (≈ 40 B) | read-only lord sheet (commander-forge screens via ui-forge) | never; "as of" date |
| `invite` Alliance invitation | ranks with the recruit permission (alliance.md) | Whisper, Circle, Market Cross | alliance id, tag, members/cap, language, minimum spine tier, sigil id, token (16 B), expiry (≈ 90 B) | alliance profile with Join / Ask to join (alliance.md rules) | 7 d, or alliance full or disbanded |
| `rally` Rally call | the rally leader (battle-forge) | **Hall and Council only** (never where enemies read) | rally id, target coord + kind, leader id, launch time, slots filled/total (≈ 70 B) | battle-forge rally join screen | at launch → "Marched" state |

## 3. Card rules

1. **One tap = one meaning**: the whole card opens its target; secondary actions (report, hide,
   copy coordinates) are on long-press.
2. **No card carries a price, an offer or a shop link** (money-law). No card type for shop goods.
3. **Countdowns are computed on the client** from the launch time; the server never ticks cards.
4. **Stale is a state, not an error**: a cleared camp, a faded report, a full alliance render the
   card greyed with one line of why (§5); no dialog, no crash.
5. **Access is checked at tap time** (server): a non-participant opening a report gets the
   sections report-forge's share policy allows; a player outside the alliance never opens a rally.
6. Cards obey the same rate buckets as text plus the per-type limits of §7.

## 4. The report-card contract (report-forge fills it)

chat-forge needs these fields in `snap`; report-forge decides their values and wording.

| Field | Type | Bytes | Meaning (report-forge defines) |
|---|---|---|---|
| `rid` | u64 as string | ≤ 20 | report id |
| `rt` | enum | 1 | battle · defence · scout · rally · camp/gather |
| `hk` | l10n key | ≤ 48 | the headline sentence (report-forge's "why you won / lost" engine picks it) |
| `ha` | array of ids/numbers | ≤ 48 | arguments for `hk`, resolved on the reader's client |
| `sa`, `sb` | player / camp / AI-lord ids | ≤ 24 | the two sides; names and tags resolved on the client |
| `oc` | enum | 1 | outcome class — chooses the art plate only; the words come from `hk` |
| `ts` | u32 | 4 | when the fight happened |
| `sp` | enum | 1 | share policy: which sections non-participants see |

**Respect the loser** (battle-forge / report-forge framing): the card never says "DEFEAT" in
large type and never uses a mocking plate. The headline key is the same neutral sentence
family both sides see ("Aldric's raid on the ford was held off — 62% of the force came home").

## 5. Layout (800 × 248 px card inside the message list)

| Part | Size / position | Content |
|---|---|---|
| Frame | 800 × 248 px, oak border 8 px, parchment fill (ui-forge kit, `NinePatchRect`) | — |
| Art plate | 200 × 200 px at (24, 24) | `coord`: tile-kind icon (Blender-made art); `report`/`scout`: report-forge plate by `rt` + `oc`; `lord`: painted portrait crop with the rarity rim 6 px and, if sworn, the gilt rim light; `invite`: alliance sigil (ALS); `rally`: rally banner icon (Blender-made) |
| Type ribbon | 132 × 40 px over the art's top-left | type icon 32 px + label 26 px PARCHMENT on the ribbon colour: coord IRON, report OAK, scout IRON, lord OAK with GILT label (5.07:1), invite OAK, rally WAX |
| Title | x 248, 34 px bold INK, 1 line, ellipsis | "Wolf camp · level 12" · report headline · "Elena · level 34" · "[OAK] Oakheart Company" · "Rally on the old abbey" |
| Line 2 | 28 px OAK (8.85:1) | "K7 · 412, 388 · 14 tiles away" · sides · "Fine · Sworn · set 4/4" · "38/60 lords · English · spine tier ≥ 3" · "Marches in 04:12 · 7/10 joined" |
| Line 3 | 28 px IRON (7.46:1) | "as of 14:02" / fight time / invitation expiry |
| Comment | above the card, as a normal text line | the sharer's ≤ 80-grapheme note |

Colour rules: ribbons never use the reserved relationship colours or the troop-line colours
(those channels keep their meaning); text pairs come from the [ui.md](ui.md) §3 contrast table.
The art plate is the largest element — ART SHOWN BIG.

| State | Look |
|---|---|
| Live | as above |
| Loading | parchment placeholder, no text, ≤ 300 ms |
| Stale | art at 40% saturation; line 2 replaced: "This camp has been cleared" / "This report has faded" / "This invitation has expired" / "This alliance is full" |
| Forbidden | title + line 2 only; line 3: "Only participants can open the details" |
| Marched (rally) | ribbon IRON; line 2 "Marched at 20:14" |

## 6. Share flows (≤ 3 taps; a 2-second Undo instead of a confirm dialog)

| From | Taps |
|---|---|
| Report screen (report-forge UI) | Share (1) → channel sheet (2) → sent; optional comment field in the sheet; Undo toast 2,000 ms |
| Map tile | long-press tile (1) → Share (2) → channel (3) → sent + Undo |
| Lord screen | Share (1) → channel (2) → sent + Undo |
| Alliance recruit | Invite (1) → a player (whisper) or Market Cross (2) → sent + Undo |
| Rally (battle-forge flow) | "Call the alliance" switch, ON by default → card posted in the Hall + a Herald line; 0 extra taps |

The channel sheet lists: Hall · Council (if member) · recent Whispers (5) · Circles · Market Cross
(if trust allows); rows 120 px, in the thumb zone.

## 7. Abuse limits per type

| Type | Rate per sender | Extra rule |
|---|---|---|
| `coord` | 1 per 10 s | Market Cross T1+ |
| `report`, `scout` | 1 per 30 s | only reports the sender took part in; Market Cross T2+ |
| `lord` | 1 per 60 s | own lords only |
| `invite` | Market Cross 1 per 30 min per alliance; whispers 10 per day per recruiter | token single-use in whispers, ≤ 20 uses in Market Cross; blocked players never receive invites |
| `rally` | 1 per rally | Hall and Council only |

Every card is reportable like a message; a comment that breaks the filter blocks the whole card.

## 8. Adding a card type (checklist)

- [ ] Owner of the content named; that skill defines the snapshot fields.
- [ ] Row in §2: who may share, channels, snapshot bytes (envelope ≤ 256 B), tap target, expiry.
- [ ] Access check at tap time written; stale and forbidden states designed (§5).
- [ ] Art plate source is existing art (Blender icon, painted portrait, sigil) — no new art per share.
- [ ] Rate limit and trust tier row in §7; minors' band checked ([safety.md](safety.md) §10).
- [ ] `share_card_probe` extended (qa.md): round trip, forged ref rejected, stale, forbidden, size.
- [ ] No price, offer or war imagery over anything paid (money-law).

## 9. Failure modes

| Fails when | Caught by |
|---|---|
| A client forges a snapshot (level, tier, outcome) | [ ] `share_card_probe`: client-sent `snap` is ignored; server snapshot stored |
| A rally card leaks to Market Cross or another alliance | [ ] probe: rally share to `r:` rejected; tap by non-member → forbidden |
| A report card opens details the share policy hides | [ ] probe with report-forge canned reports, non-participant viewer |
| A stale card throws an error dialog | [ ] probe: delete the referent, render → stale state screenshot |
| Card text below contrast or card target < 120 px | [ ] `contrast_test`, `ux_touch_probe` chat pass |
| Invite spam in Market Cross | [ ] server test: 2nd invite inside 30 min rejected |
