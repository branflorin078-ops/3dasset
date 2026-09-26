# Layouts — the outcome in 1 second, the reason in 10, everything in 20

The report is a **war screen** (design-forge `monetization.md` §10): painted, but data first.
ui-forge owns the component kit, the type scale and the Theme; this file owns what the report
shows, in which order, at which size, and what each state looks like. Pixel values are for the
1080 × 1920 portrait reference frame (the session_audit window is 1080 × 1900) and are
**PROPOSALS** until ui-forge's type scale confirms them.

## 0. The reading budget

| Time | The player knows | Carried by |
|---|---|---|
| 1 s | won or lost | the outcome mark + one word, 88 px |
| 3 s | against whom, where, and the cost | the vs line + two numbers |
| 10 s | why, and what to do next | the Why strip: ≤ 3 cause rows, 1 counterpoint, 1 Next |
| 20 s | everything that matters in a war battle | sections on expand (design-forge `core-loop.md` §8: "report read ≤ 20 s") |

Rule: nothing below the Why strip is needed to answer "why". A player who never expands a
section still learns the counter graph, one battle at a time.

## 1. The headline band (0–420 px below the safe area)

| Element | Size | Content | Rule |
|---|---|---|---|
| Context art | 1080 × 420 px, painted (game-art-director vignette per place type: field, castle wall, camp, node, stronghold) | ART SHOWN BIG; never war imagery near a buy button — there is none here | a scrim of INK #1E1712 from 0% (top) to 72% (bottom 60%) under the text |
| Outcome mark | 120 × 120 px, left, Blender-made icon (ui-forge, blender-forge) | raised banner (win), dipped banner (loss), two level banners (draw) — the same banner motion battle-forge plays at the outcome | **never a laurel or seal**: the laurel-and-seal motif is reserved for earned honours (monetization.md §3 #9); never a relationship colour |
| Outcome word | 88 px, PARCHMENT #E8D9B5 on the scrim | Victory / Defeat / Both withdrew / Castle held / Castle breached | ≤ 3 words in English |
| Margin tag | 40 px, GILT_LIT #E0BC6A | close / clear / crushing / heavy / even | GILT_LIT on INK 9.75:1 |
| vs line | 36 px | "vs Garrick [RVN] · Lumber camp 412:388" | name resolved at view time |
| Two numbers | 44 px, tabular figures | the list line's `n` codes ([schema.md](schema.md) §6) | a loss shows what comes back first, then what is gone |
| Why line | 36 px, one line, ellipsis if long (the full sentence is row 1 below) | row 1's sentence | never a sentence without a number behind it |

Measured contrast (WCAG): PARCHMENT on INK 12.66:1, GILT on INK 7.26:1, GILT_LIT on INK 9.75:1
— text over the painted vignette must keep ≥ 4.5:1 **measured at the text box** after the
scrim (contrast_test), because the painting underneath varies.

The headline renders from the inbox list line with **0 network reads** — it is on screen in the
first frame after the tap (≤ 100 ms); the body fills in when the record arrives (target p95
≤ 500 ms on 4G; the record is ~430 B gzip).

| Fails when | Caught by |
|---|---|
| Won/lost is unreadable in 1 s | [ ] the 1-second test ([qa.md](qa.md) §5): ≥ 9 of 10 readers correct |
| The outcome is told by colour alone | [ ] a11y_audit colour-blind pass: mark shape and word differ per outcome |
| Text over bright paint drops below 4.5:1 | [ ] contrast_test on each of the 6 context vignettes |
| The victory card and the report disagree | [ ] both read the list line; `report_probe` compares |

## 2. The Why strip (parchment panel directly under the band)

| Part | Size | Rule |
|---|---|---|
| Cause row | 112 px tall, 3 rows max | icon 64 px · sentence 34 px, ≤ 2 lines · bar · value |
| Icon | 64 px, Blender-made | counter: the battle-forge medallion pair (hitter line → chevron → target line); tier: line icon + tier pips; numbers: banner count; lord: the lord's portrait chip (commander-forge); stats: research seal; defences: wall; siege: engine icon |
| Bar | 8 px tall, diverging from the row's centre line; right = for you, left = against | length ∝ `|n|`, full half-width at 300‰; ▲ / ▼ and the signed value always beside it |
| Bar colour | for: GILT #C9A04C fill **with a 2 px OAK #4A2E1B outline**; against: IRON #3B4048 fill | GILT on PARCHMENT is only 1.74:1 — the OAK outline (8.85:1) carries the shape; IRON on PARCHMENT 7.46:1; never red/green (reserved relationship colours) |
| Value | 34 px, tabular, "+8%" / "−15%" | the displayed percent is the sort key, so the column always reads in order ([explain.md](explain.md) §3) |
| Label line | 30 px italic under row 1 | "Without this edge, you would have lost." / "This was the main reason." |
| More chip | 30 px, "+1 more" | opens Details at the hidden causes |
| Counterpoint | same row anatomy, header 30 px "Despite this:" / "What went well:" | 1 row, only when ≥ 5% |
| Next | a full-width button, 128 px tall (≥ 48 dp at 2.625 px/dp) | the advice sentence + its deep link ("Train cavalry"); never a shop, gem, offer or ward for sale |

Tap a cause row → a small sheet with its numbers: "Your counter edge +118‰ · theirs +34‰ →
net +84‰ = 8% of all power lost in this battle", plus the evidence matchup. This is where a
curious player (or a doubting one) checks the engine.

## 3. Sections (collapsed by default, fixed order)

| # | Section | Content | Private rules |
|---|---|---|---|
| 1 | Losses | yours per line and tier: sent · light · infirmary · dead · dealt, then the loss notes (what comes back first); theirs: sent · out of action | bucket split own side only ([schema.md](schema.md) §5) |
| 2 | Lords | each lord: portrait chip, level, cp dealt, cp healed, skill casts; xp gained (own lords) | — |
| 3 | Resources | taken / plundered per resource, load used; protected (castle owner only) | `rp` owner only |
| 4 | Rally share (k = 3) | each participant's damage share, sorted high → low, you highlighted; no "worst" label, no per-troop efficiency ranking (it shames small contributors) | visible to participants and alliance officers |
| 5 | Before contact (defence) | defender actions: recall, allies arrived, healed, garrison lord ([kinds.md](kinds.md) §2) | castle side only |
| 6 | Timeline | ≤ 8 moments; tap → replay from 1,000 ms before that beat (battle-forge `beats.md` §5) | — |
| 7 | Details | all seven nets with values, the loss-context rule text read live from combat.md data, the rules version `rv`, the report id | — |

Section header rows 96 px; expand 180 ms ease-out cubic; reduced-motion setting → instant.
Tables use tabular figures (a `FontVariation` with the `tnum` OpenType feature) so columns align
without monospace fonts.

## 4. The action bar (bottom thumb zone, 160 px)

| Button | Behaviour | Disabled state (always visible, never hidden) |
|---|---|---|
| Replay | battle-forge replay from the beat log; ≤ 2 taps from the inbox | "Replays are kept 7 days. This one has expired." — tap Keep before day 7 to keep it |
| Share | chat-forge share card to alliance chat or a private chat (§6) | offline: "Share when online" |
| Next | the advice deep link (duplicate of the Next button for thumb reach) | no advice → hidden slot, bar re-centres to 3 buttons |
| Keep | star: keeps the record and its beats 90 days (max 30 kept per player, PROPOSAL) | at 30 kept: "Keep limit reached — remove one" |

Tap targets ≥ 48 dp (≥ 126 px at 1080 px wide); spacing between targets ≥ 8 dp. The bar never
holds a gem price, an offer, or a ward for sale (monetization.md §10; battle-forge `defence.md` §7).

## 5. States (every one designed, none blank)

| State | What shows | Timing |
|---|---|---|
| Opening | headline from the list line; body skeleton (3 grey cause rows, 3 section headers) | headline ≤ 100 ms; body ≤ 500 ms p95 |
| Body failed | headline stays; "Report could not load. Tap to retry."; cached copy if any | retry at once, then backoff 2 s / 8 s |
| Offline | the last 20 opened reports from the local cache (`user://reports/`, ≤ 2 MB) | — |
| Expired (link from chat after retention) | "This report has expired (reports are kept 30 days)." + the share card's own summary | — |
| Opponent left the realm | "A lord who left the realm" in the vs line | — |
| No casualties (`T = 0`) | Why strip shows the empty/even sentence; Losses shows "No losses." | — |
| Replay expired | Replay button disabled with its reason; Timeline moments still listed | — |

## 6. Share cards (content here, rendering in chat-forge)

The card is built on the server from the record id — a client cannot fake a victory card.

| Card field | Source | Privacy |
|---|---|---|
| Outcome word + mark, margin | the sharer's point of view | — |
| Both names + tags (resolved at share time), place, time | record | — |
| Two headline numbers | the sharer's list line | the sharer's own totals only; never the opponent's infirmary split |
| Top cause sentence (+ label) | explain engine, sharer's view | — |
| "Open report" | share token → the share projection ([schema.md](schema.md) §5) | read-only; no `rp`, no `ho` |

Card size, chat placement, moderation and rate limits are chat-forge's (`share-cards.md`).
A shared report counts one read per open; it never copies the record.

## 7. Godot 4 implementation notes (ui-forge builds; names to confirm)

- One `ReportView` scene on a `CanvasLayer` above the realm: `ScrollContainer` →
  `VBoxContainer` [HeadlineBand (`Control` with a `TextureRect` vignette + `ColorRect` scrim),
  WhyStrip (`PanelContainer` with a parchment `StyleBoxTexture`), sections, ActionBar].
- Sentences are `Label`s with `autowrap_mode = TextServer.AUTOWRAP_WORD_SMART` and
  `max_lines_visible = 2`; text is `tr(key).format(params)` — never concatenated fragments.
- Bars are a small custom `Control` using `draw_rect()` (fill + outline) so the OAK outline is
  exact at any scale; the grow animation (300 ms ease-out, first open only) is one
  `create_tween()` on a `ratio` property.
- Headline data arrives with the inbox row; the body via `HTTPRequest`, gzip body decoded with
  `PackedByteArray.decompress_dynamic(-1, FileAccess.COMPRESSION_GZIP)`, then `JSON.parse_string`.
- Deep links go through ui-forge's navigation map; each Next link id is in [explain.md](explain.md) §6.

## 8. Checklist — a layout change

- [ ] The 1 / 3 / 10 / 20-second budget still holds (qa.md §5 test re-run if the band changed).
- [ ] Every colour pair on the report is listed with its measured ratio (text ≥ 4.5:1, bars and icons ≥ 3:1).
- [ ] Pseudo-locale +40%: no sentence exceeds 2 lines, no headline number truncates (layout_audit).
- [ ] w1f_aspect_sweep prints `ASPECT SWEEP OK - 6 shapes, 0 faults` with the report open.
- [ ] ux_flow_probe: inbox → headline 1 tap; → replay ≤ 2 taps; → Next target 1 tap from the report.
- [ ] No buy, gem, offer or ward-for-sale element anywhere on the report or its sheets.
