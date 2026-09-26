# Templates — every letter the game writes, in every language, with its painting

Game-written letters are **data, not text**: a template id, typed arguments and (for Rewards) an
attachment list. Each reader's phone renders the words in that reader's language when the letter
opens. Strings belong to **l10n-forge** (keys, plurals, fonts), words and voice to **story-forge**,
paintings to **game-art-director**. This file is the contract between them and mail. Every number
is a **PROPOSAL**; `godot/ui/strings.gd` with `S.t` / `S.f` is named in the studio's l10n brief
(path and API to confirm).

## 1. The template card

One card per template. The send validator (§7) refuses a letter whose card is missing or broken.

| Field | Meaning | Example (`ev_result`) |
|---|---|---|
| `id` | lowercase, `a-z0-9_`, ≤ 24 characters; part of the deterministic letter id | `ev_result` |
| `tab` | `n` Notices · `w` Rewards · `a` Alliance · (`l` and `r` are never templates) | `w` |
| `keys` | `mail.<id>.subject`, `mail.<id>.body`; optional `mail.<id>.line.<n>` | `mail.ev_result.subject` |
| `args` | name → type (§3); every arg is required | `event: key`, `marks: int`, `of: int`, `days: int` |
| `attach` | none, or class I/P + the item lines' source (liveops tables) | class I, from the event's milestone table |
| `header` | painted header id (§6) or the tab default | the event's header, else `MLH-reward` |
| `x` | hard expiry rule | `t + 90 d`, claim window 30 d |
| `audience` | who receives it, from SERVER data only | participants with ≥ 1 milestone |
| `badge` / `push` | per [categories.md](categories.md) §4–§5 | badge until claimed / no push |
| `owner` | the system that triggers it | liveops (gameplay-forge) |

## 2. The catalogue (PROPOSAL; story-forge writes the final words)

### 2.1 Notices and account notices (tab `n`)

| id | When | Args | Badge | Source |
|---|---|---|---|---|
| `sys_maintenance` | ≥ 24 h before planned downtime | `from: time`, `length: duration` | no | cloud-forge |
| `sys_patch` | after a client update ships | `version: text`, `notes: key` (≤ 5 line keys) | no | ship-forge |
| `sys_news` | owner news, event season opening | `topic: key` | no | liveops |
| `ev_open` | an event opens (optional; the Herald's Board is the main surface) | `event: key`, `ends: time` | no | liveops.md §6 |
| `realm_merge` | 21 days before a merge, then at 7 d and 1 d | `partner: text`, `when: time` | no | liveops.md §8 |
| `realm_writ` | migration window opens (Writ of Passage) | `closes: time` | no | liveops.md §7 |
| `acct_restriction` | any restriction in chat or mail (DSA statement of reasons) | `what: key`, `rule: key`, `auto: bool`, `until: time`, `appeal: key` | **yes** | chat-forge safety.md §12 |
| `acct_security` | sign-in on a new device, account link done | `device: text`, `when: time` | **yes** | cloud-forge |
| `acct_data_ready` | a GDPR data export is ready | `until: time` | yes | cloud-forge |
| `shop_restored` / `shop_refund` | a purchase restored, or a refund changed the balance (ui-forge states.md §5) | `goods: key`, `balance: int` | yes | shop-forge |

### 2.2 Rewards (tab `w`) and alliance system mail to one member (tab `a`)

| id | When | Args | Attachments | Source |
|---|---|---|---|---|
| `ev_result` | ≤ 1 h after an event ends (liveops R7) | `event: key`, `marks: int`, `of: int` | milestone goods, class I | liveops.md §5 |
| `ev_rank` | same time; ranks and firsts carry cosmetics and titles only (liveops R1) | `event: key`, `rank: int`, `title: key` | cosmetics, class I | liveops.md §5 |
| `chronicle_end` | season end: chronicle rewards earned but unclaimed | `season: key`, `count: int` | the pages' goods, class I | monetization.md §7 |
| `compensation` | after an outage or a bug fix | `cause: key`, `when: time` | ≤ value cap; class I or P | ops, owner second key above cap |
| `welcome` | first session | — | starter goods, class I | onboarding-forge |
| `lord_refit` | a lord is rebalanced: what changed, in numbers | `lord: lord`, `lines: key` (≤ 4 "old → new" lines) | refit goods and seal transfer | lords.md (nerf rule) |
| `ally_released` | a member is released | `alliance: tag`, `reason: key`, `rejoin: time` | — | alliance.md §13 |
| `ally_rank` | promotion or office change | `alliance: tag`, `rank: key` | — | alliance.md §13 |
| `ally_liege_absent` | Liege absent day 5 (officers), 7 and 10 (all) | `days: int`, `heir: player` | — | alliance.md §9, §13 |
| `ally_pact` | pact proposed (officers), signed and notice (all) | `other: tag`, `kind: key`, `ends: time` | — | alliance.md §12, §13 |
| `ally_autorelease` | N − 3 days before auto-release | `days: int` | — | alliance.md §9 |
| `ally_banner_fading` | Treasury at 0 (Steward and Liege) | `banner: coords` | — | alliance.md §13 |

### 2.3 Officer templates for alliance-wide mail (Liege and Herald office)

Templates solve two genre problems at once. **Times are unix values** shown in each reader's local
time, and **the words arrive in each reader's language**. Free text stays possible (≤ 1,000
characters) for everything else.

| id | Args the officer fills | Rendered for a reader in Lisbon (example) |
|---|---|---|
| `off_rally` | `target: coords`, `at: time`, `lead: player` | "Rally on the Ford at 21:00 your time (in 5 h 10 m). Lead: Aldric." |
| `off_muster` | `from: time`, `to: time` (muster hours, alliance.md §8) | "Muster hours: 20:00–22:00 your time, daily." |
| `off_rules` | `lines: key[]` from a list of 12 standard rules | numbered rule lines |
| `off_welcome` | `player: player` | "Welcome to the Hall, Beatriz. Read the rules, then ask for help on your timers." |
| `off_war` | `window: time`, `objective: coords` | "War window opens at 20:00 your time. Objective: the Old Abbey." |
| `off_pact` | `other: tag`, `kind: key` | "We are at Truce with [RVN] until the season ends." |

## 3. Argument types and how they render

| Type | Stored as | Rendered by the reader's phone |
|---|---|---|
| `int` | integer | locale digits and grouping; plural category chosen by l10n-forge's rules |
| `key` | a string key | `S.t(key)` — never shown raw; a missing key falls back to English and logs once |
| `time` | server ms | local date and time; relative ("in 5 h 10 m") when < 24 h away; the UTC offset on long-press |
| `duration` | minutes | the §5d human units (`Items.pretty_time`, path to confirm): "1 h 12 m", rounded UP |
| `player` | player id + name snapshot ≤ 16 chars | the current name if known, else the snapshot |
| `tag` | alliance id + 3–4 letter tag | "[RVN]" with the sigil (ALS art) in rich layouts |
| `lord` | lord id (Edwin … Fable) | the lord's l10n name |
| `coords` | realm tile x, y | a tappable map point (opens the realm there; not a URL) |
| `text` | ≤ 32 characters, server-validated | shown as is (versions, device names) — never player free text |

Rules:

1. **No sentence is ever built by joining strings.** One key per sentence with named placeholders,
   so languages can reorder words.
2. **Args are validated at send time** against the card (§7). A letter that could fail to render is
   never sent. The client's fallback for a broken letter (old client, new template) is the tab's
   generic subject key plus "Update the game to read this letter", and never a raw key.
3. **Player text never passes through BBCode.** Letters and officer free text render in a label with
   `bbcode_enabled = false`. Template strings may use a whitelist of `[b]`, `[i]` and `[color]` with
   Theme colour names only.

## 4. Localization gates (l10n-forge owns the plan)

- English is v1 (L10N-001 in the brief); the plan names 7 languages. Every template ships with its
  English strings and is extracted with the rest (the data-table extraction step, path to confirm).
- **Lengths in English**: subject ≤ 32 characters (one row line at 42 px bold, [ui.md](ui.md) §3);
  system body ≤ 400 characters; each `line.<n>` ≤ 60 characters.
- **Pseudo-locale +40%** (the brief's layout gate) must fit: the subject may ellipsize in the row,
  never in the letter view (2 lines at 60 px); the body wraps; buttons never clip (UI-004,
  Button-min-width law).
- Plurals use the locale's categories (one/few/many/other), never `if n == 1`.
- Fonts: the Noto fallback chain (CJK, Cyrillic) is l10n-forge's; the probe renders every template
  in every shipped locale ([qa.md](qa.md) §5).

## 5. Voice (story-forge holds the canon)

The Chancery writes like a careful clerk to a lord: short sentences, concrete facts, the number
first, no pressure.

| Do | Don't |
|---|---|
| "You reached 5 of 6 marks." | "AMAZING! You did it!" |
| "Yours to claim for 30 days; after that the Chancery claims it for you." | "Claim now before it's gone!" |
| "The gates close for about 40 minutes from 03:00 your time." | "Short maintenance soon." |
| "Rowan's charge: +12% → +9% damage (example numbers). Your refit is below." | "Rowan was adjusted." |
| "Your message was held for review under rule 4, contact details (example). Automated. Appeal: Settings → Help." | "You broke the rules." |

No exclamation marks in system letters. No countdown pressure (onboarding-forge: no pressure
tactics; money-law). No offers, prices or shop words, ever ([categories.md](categories.md) §1 rule 3).

## 6. Painted headers (game-art-director paints; this is the brief)

| Spec | Value |
|---|---|
| Size | **1080 × 432 px** (2.5 : 1), full width of the letter view, ≤ 22.5% of a 1920 px screen |
| Safe band | subject in the middle 60% of the width; lower 25% quiet (low contrast): the letter's parchment panel overlaps it by 48 px |
| Light | the master style block (warm key from upper left); time-of-day presets from environments.md |
| Text | none in the art; the subject sits BELOW the painting on parchment (INK on PARCHMENT 12.66 : 1), never over it |
| Money-law | no bundle key-art (BND-*) in mail; war scenes are fine because mail has no buy button |
| File | shipped in the build (PNG source → Godot VRAM compression); loaded with `ResourceLoader.load_threaded_request()` when a letter opens; freed on close |
| Delivery | **never through the database** (image bytes would be billed per download, [backend-cost.md](backend-cost.md) §1); a header id missing from the build falls back to the tab default |

Defaults (id prefix `MLH-` proposed to game-art-director, which owns the register; or its screen
head-piece class if it prefers):

| id | Tab | Subject (house register) |
|---|---|---|
| `MLH-notice` | Notices | THE CHANCERY DESK: a sealing table under a high window, wax stick and seal matrix, ledgers stacked, working-noon light |
| `MLH-reward` | Rewards | THE TALLY ROOM: an iron-bound chest open on a trestle, sacks and hourglasses counted out, campaign-dawn light |
| `MLH-alliance` | Alliance | THE HALL BOARD: an oak board of pinned orders and a banner, benches below, lantern light |
| `MLH-chronicle` | chronicle and season letters | THE CHRONICLE LECTERN: an open book with a gilt initial, chronicle-night lantern pool |
| `MLH-account` | account notices | a plain parchment field with one unbroken wax seal — sober on purpose: restrictions are never dramatized |

Event letters use a 1080 × 432 crop of the event's own board painting (liveops' Herald's Board art),
never a new painting per letter.

## 7. The send validator and the send checklist

`validate(card, letter)` runs in the send job and the send function before any write. It refuses when:

1. a key is missing in any shipped locale, or a placeholder in a string has no matching arg;
2. an arg is missing, has the wrong type, or a `text` arg exceeds 32 characters;
3. attachments: > 8 lines, an unknown item id, a mixed class, an item marked random, a currency whose
   validity ends before `x`, or a value above the cap (1,440 hourglass-minutes-equivalent or 500 gems)
   without the owner's second key;
4. `x` is missing, or the Rewards claim window is < 30 d (liveops R7);
5. the header id is neither in the build manifest nor empty;
6. the audience uses a field the server does not own (anything read from a client save);
7. any string contains a price, a currency symbol or a shop word list entry (money-law grep).

Every send with attachments prints a **dry run** first: recipients, total value in gem-equivalent,
the rendered English letter, and the first 3 locales. The owner's second key is required above the
cap, for re-running a done job, and for any clawback ([attachments.md](attachments.md) §9).

## 8. Failure modes and checklist

| Fails when | Caught by |
|---|---|
| A raw key, a `{placeholder}` or an empty body shows in any locale | [ ] mail_l10n_probe: every card × every locale renders, 0 raw keys |
| A subject overflows the letter view at +40% | [ ] mail_l10n_probe pseudo-locale pass |
| Officer templates show the officer's time zone instead of the reader's | [ ] mail_l10n_probe with two device time zones |
| Player text renders BBCode (a `[color]` or `[url]` from a player takes effect) | [ ] mail_ui injection case: 20 BBCode strings stay literal |
| A header is downloaded from the database, or is missing and shows empty | [ ] sd_cost_probe bytes per path; header fallback test |
| A template contains pressure words, prices or shop words | [ ] validator grep in the send tool's unit tests |

New template:

- [ ] Card filled (§1); args typed (§3); English strings within §4 lengths; keys sent to l10n-forge.
- [ ] Words reviewed by story-forge against §5; header chosen or requested from game-art-director (§6).
- [ ] Validator passes on a dry run; the mail_l10n_probe line is green.
- [ ] If it carries goods: [attachments.md](attachments.md) §12 checklist.
