---
name: chat-forge
description: In-game chat for Castle Conquest — channels (realm, alliance, officer, whisper, group, herald system feed), message types (text, painted stickers, quick calls, share cards for coordinates, battle and scout reports, lords, alliance invites, rally calls), the bottom ticker and one-hand chat panel, unread counts, mentions, on-device translation, safety (filter, report/block/mute, rate limits, trust ladder, gold-seller filtering, moderation queue, minors and store rules, GDPR deletion), the WebSocket backend and its cost model for 50,000 players inside €200/month, offline catch-up, push rules and the chat harness. Use for "add chat", "alliance chat", "world chat", "chat filter", "mute/block/report a player", "share this report to chat", "chat cost", "chat translation". Not for the inbox (mail-forge), report content (report-forge) or general screens (ui-forge).
---

# chat-forge — words between lords: safe, readable, and inside the budget

Chat is where alliances plan, recruit and hold together — and the only place where one player's
words reach another player's screen. It must carry a rally call in under a second, stay readable
in one hand, keep sellers, abusers and strangers away from children, and cost a small, measured
share of the **€200/month at 50,000 players** ruling. This skill specifies all of it with numbers;
the domain forges build it.

Every number here is a **PROPOSAL** unless it quotes a canonical fact. The game's shipped chat code
and data are not visible to this skill (owner's repo, paths to confirm): read them first, and write
changes as "PROPOSAL (verify against <file>)".

## Hard rules

1. **The server decides; the client only mirrors.** Filter, limits, trust, age band, membership and
   sanctions are enforced server-side. A modified client changes nothing ([safety.md](references/safety.md) §1).
2. **Player text is never markup and never a link.** `RichTextLabel.add_text()` / `Label` only;
   `[url]`, `[img]` render as characters; no clickable URL anywhere ([ui.md](references/ui.md) §11).
3. **Report, block and mute are ≤ 3 taps** from every message, card and name, in every channel —
   the store UGC rules require them and so do players ([safety.md](references/safety.md) §8, §10).
4. **The age band decides the features.** Under the local age of digital consent (13–16 by
   country): no free text, no whispers; quick calls, stickers and cards stay on. Minors above it:
   strict filter locked, whispers only with alliance and Circle mates ([safety.md](references/safety.md) §10).
5. **Trust is earned, never bought.** Rates and reach grow with account age and clean play only.
   Nothing in chat is sold — no paid length, speed, colour, reach or realm-wide horn (money-law).
6. **Retention per channel, erasure within 30 days.** Market Cross 3 d, Herald 7 d, Hall / Council /
   Whisper / Circle 30 d, each with a count guard; evidence 90 d. Nothing is kept "just in case"
   ([channels.md](references/channels.md) §1, [safety.md](references/safety.md) §11).
7. **Cost shape A1 only**: persistent WebSocket gateway + Postgres on a flat-traffic box; never a
   per-delivered-message or per-listener-read service for fan-out (those fail at the BASE scenario,
   €65–€283/month); the Hall is the ticker default; the realm channel is capped at 20 accepted
   messages per minute; translation is on-device with a €10 cloud breaker
   ([backend-cost.md](references/backend-cost.md) §7). Measured by `core/sd_cost_probe.gd`, never guessed.
8. **Isolation**: chat never shares a process or database with saves, economy or the map; with the
   chat box down the game runs normally.
9. **Share cards carry references; the server builds the snapshot.** chat-forge owns the card
   format; report-forge owns report content; battle-forge owns rallies ([share-cards.md](references/share-cards.md)).
10. **Push only for whispers, mentions and rally calls**, inside design-forge core-loop.md A8
    (≤ 4 per day, quiet hours 22:00–08:00 local); never for Market Cross, the Herald or anything paid.
11. **The painted identity holds in chat.** Stickers come from the painted lane (game-art-director);
    tab and card icons are Blender-made art, never white or line glyphs; faces are never code-built;
    card art is the largest element of a card (ART SHOWN BIG).
12. **Numbers or it is not a chat rule**: every rule states its limit (graphemes, bytes, seconds,
    px, days, €) and has a "Fails when → Caught by" row.

## Key numbers (PROPOSALS; details in the references)

| Item | Value |
|---|---|
| Text message | ≤ 200 graphemes and ≤ 800 bytes; ≤ 3 line breaks; no edit, delete any time |
| Rates (T2+) | Market Cross 1 per 10 s (channel cap 20/min) · Hall 1 per 2 s · whisper 1 per 2 s · ≤ 600 per day |
| Trust ladder | T0 < 48 h or spine tier < 2 · T1 · T2 ≥ 7 d clean · T3 ≥ 30 d clean |
| Ticker / panel | strip 84 px, hit area 120 px · half sheet 960 px · full 1690 px · targets ≥ 120 px (48 dp) · body text 36 px |
| Latency | send → other client p95 ≤ 1 s; optimistic own row ≤ 1 frame |
| Cost (A1, one box) | base €4–€30 · high €4–€31 · stress €10–€49 per month; chat envelope PROPOSAL €50 |
| Moderation load (base) | 8–45 human cases per day ≈ 6–68 minutes |

## Workflow

1. **Frame** — which part (channel, message type, UI, safety, backend, card) and which owner order,
   backlog line or ledger row asked for it. Read the shipped chat code and data first (paths to confirm).
2. **Read** the matching reference (index below) and the owners' files it points to
   (alliance.md, ux.md, core-loop.md; mail-forge, report-forge, ui-forge by name).
3. **Design with numbers** — fill the rows the change needs: channel row, message-type row, rate
   row, trust row, age-band row, retention and erasure, push row, card row.
4. **Cost it** — `python tools/chat_cost.py` (and `--model changes.json` for new inputs); paste the
   three scenario lines and the A1 range. A change that pushes A1 stress above the envelope needs a
   lever from backend-cost.md §7.9 or an owner decision.
5. **Safety pass** — [safety.md](references/safety.md) §14; **UI pass** — [ui.md](references/ui.md) §14;
   cards — [share-cards.md](references/share-cards.md) §8.
6. **Hand off** by the routing table; one writer per file; strings to l10n-forge, names to story-forge.
7. **Prove** — the probes and harnesses of [qa.md](references/qa.md) §1 with pasted verdict lines;
   the launch gate §3 before chat first reaches players.
8. **Record** — predictions vs measured in qa.md §5; lessons to the game-director lead; the recipe
   that worked written back into the owning reference here (game-director hard rule 7).

## Routing — who builds what

| Need | Skill |
|---|---|
| Ticker, panel, rows, components, Theme, screens | `ui-forge` |
| Gateway, database, push worker, jobs, load test, the cost probe line | `cloud-forge` |
| Inbox, sanction and appeal notices, persistent officer orders | `mail-forge` |
| Report content, headline keys, report share policy | `report-forge` |
| Rally flow, rally card data, battle hand-offs | `battle-forge` |
| Alliance ranks, permissions, size, recruit rights | `design-forge` (references/alliance.md) |
| HUD zones, red-dot budget, text and tap minimums | `design-forge` (references/ux.md) |
| Push budget A8, session shapes | `design-forge` (references/core-loop.md) |
| Lord data and lord screens behind lord cards | `commander-forge` |
| Painted stickers (new `stickers` group, `STK-` prefix to confirm) | `game-art-director` |
| Blender-made icons (tabs, card types, object stickers) | `blender-forge` + ui-forge icon rules |
| Strings, quick-call texts, wordlists, fonts, right-to-left | `l10n-forge` |
| Channel names and voice | `story-forge` |
| Panel and ticker motion tokens | `transition-forge` |
| Probes and corpora | `qa-forge` |
| Store age rating, IARC answers, APK size | `ship-forge` |
| Seller and real-money-trading sanctions on the account | `cloud-forge` + `gameplay-forge` |

## Reference index

| File | Holds |
|---|---|
| [references/channels.md](references/channels.md) | channel catalogue, message types, history rules, mentions, Herald, whispers and Circles, quick calls, push policy |
| [references/ui.md](references/ui.md) | ticker, panel, row anatomy, contrast table, unread, translation UX, stickers, states, motion, Godot 4 patterns, budgets |
| [references/safety.md](references/safety.md) | filter pipeline, hygiene, normalization, rate limits, trust ladder, wordlists, sellers, player tools, moderation, minors, GDPR, DSA |
| [references/backend-cost.md](references/backend-cost.md) | isolation, shape, transport, wire protocol, schema, catch-up, push, the full cost model for 50,000 players, price verify list, levers |
| [references/share-cards.md](references/share-cards.md) | card envelope, six types, report-card contract, layout, flows, abuse limits |
| [references/qa.md](references/qa.md) | probe battery with verdict lines, corpora, launch gate, review checklist, predictions vs measured |
| [tools/chat_cost.py](tools/chat_cost.py) | the cost arithmetic (`--scenario`, `--model`, `--json`, `--selftest`) |

## Output contract

Every chat task ends with: the files changed and their owners; the rule rows added (channel,
type, rate, trust, age band, retention/erasure, push, card); the cost line (tool output for base,
high and stress, plus the measured line when it exists); the safety and UI checklist results; the
verdict lines of the probes run; and the owner decisions below that the change touches, listed
separately.

## Owner decisions (open)

1. **Chat's share of the €200**: PROPOSAL envelope €50 (game ≈ €20 measured; mail and report lines from their skills).
2. **Hot standby for chat** (A1-HA): fits base and high; at stress €18–€79, over the envelope at high prices.
3. **Who moderates**: 6–68 minutes per day at base, S3 cases reviewed ≤ 24 h — the owner, volunteers or a paid service (outside the server budget).
4. **Push**: may a player's "every whisper" setting exceed the A8 budget of 4 per day?
5. **Audience and rating**: target age, Families-policy scope, and whether a parental-consent path for free text is ever built.
6. **Plain URL text** for T3 adults in Hall and Council (never clickable): allow or not.
7. **Sticker packs**: always free, or sold as stat-free cosmetics under the money-law.
8. **Names**: Market Cross, Hall, War Council, Whisper, Circle, Herald, horn calls (story-forge canon).
9. **Cloud translation fallback**: ship it at all (needs a DPA) and keep the €10 monthly breaker.
