# Safety — filter, limits, trust, reports, moderation, minors, privacy

Chat is the only place in Castle Conquest where one player's words reach another player's
screen. Everything in this file is enforced **on the server**; the client repeats some checks
only to give instant feedback. Every number is a **PROPOSAL** (verify against the shipped chat
code, path to confirm). Legal lines are marked **legal to confirm** — this skill writes the
engineering side of compliance, not legal advice. Implementation: **cloud-forge** (pipeline,
queue, jobs), **l10n-forge** (wordlists per language, native review), **mail-forge** (sanction
and appeal notices), **qa-forge** (probes in [qa.md](qa.md)).

## 1. The pipeline (every player message, in this order)

| # | Step | Result on fail | Budget |
|---|---|---|---|
| 1 | Auth token valid; account not chat-banned; channel membership | reject `403` | in memory |
| 2 | Sanction state (muted in this channel?) | reject with remaining time | in memory |
| 3 | Rate limits: per player, per channel, channel-wide cap (§4) | reject with wait seconds | token buckets in memory |
| 4 | Hygiene: size, control and bidi characters, combining marks, line breaks (§2) | reject or strip | ≤ 0.2 ms |
| 5 | Normalize a COPY for matching (§3); the displayed text is not rewritten | — | ≤ 0.5 ms |
| 6 | Link / contact / seller scoring (§7) | hold for review or reject | ≤ 0.5 ms |
| 7 | Abuse wordlists by severity (§6) | mask, reject, strike, escalate | ≤ 1 ms |
| 8 | Duplicate check: same normalized text ≥ 3 times in 10 min, any channel | reject | hash set per player |
| 9 | Store, ack the sender, fan out | — | ≤ 5 ms total p95 CPU per message |

Rules: (1) the client never decides; a modified client that skips its checks changes nothing;
(2) every rejection returns a reason code the UI can show ([ui.md](ui.md) §9); (3) every automated
action is logged with the rule id and the list version, so a decision can be explained later (§12).

## 2. Text hygiene (hard limits)

| Rule | Value |
|---|---|
| Length | ≤ 200 grapheme clusters (UAX #29) AND ≤ 800 bytes UTF-8; announcements 400 / 1,600 |
| Line breaks | ≤ 3; runs of blank lines collapse to one |
| Control characters | C0 and C1 removed except `\n` |
| Bidi overrides and isolates | U+202A–U+202E and U+2066–U+2069 removed (spoofed names and reversed text); U+200E/U+200F marks kept |
| Invisible characters | U+200B, U+2060, U+FEFF, U+180E, U+3164, U+115F/U+1160 removed; ZWJ U+200D and ZWNJ U+200C kept (emoji sequences, Persian and Indic scripts) but ignored for matching |
| Combining marks | ≤ 4 consecutive marks per base character (stacked-diacritic "zalgo" text rejected) |
| Emoji | count as graphemes; ≤ 30 per message |
| Names and alliance tags | the same rules plus: 3–16 graphemes, no whitespace-only, unique after confusable skeleton (§3) — names are owned by the account system; chat requires that they pass this filter |

## 3. Normalization for matching (on a copy only)

1. Unicode NFKC, then full case folding.
2. Confusable skeleton (Unicode UTS #39): Cyrillic "а" and Latin "a" match; fullwidth letters match.
3. Remove the invisible characters of §2 and separators between single letters
   ("f.r.e.e", "f r e e", "f_r_e_e" → "free").
4. Leet map: 0→o, 1→i/l, 3→e, 4→a, 5→s, 7→t, 8→b, @→a, $→s, €→e (both branches tried for 1).
5. Repeated letters collapse to at most 2 ("gooold" → "goold"; lists store both forms).
6. Scripts without spaces (Chinese, Japanese, Thai) are matched by substring with a per-language
   minimum length (l10n-forge sets it); Latin words ≤ 4 letters match whole words only (avoids
   the town-name false-positive class).

## 4. Rate limits and slow mode

Token buckets (sustained rate, burst) per player per channel, plus a channel-wide cap.

| Channel | Player T2+ | Player T1 | Channel-wide cap | Slow mode |
|---|---|---|---|---|
| Market Cross | 1 per 10 s, burst 3 | 1 per 30 s, burst 1 | 20 accepted per min per realm, burst 30 (the cost tool's `realm_cap_per_min`) | when the cap fills: per-player cooldown 30 s, at 2× fill 60 s; the send button shows the countdown |
| Hall | 1 per 2 s, burst 6 | same | 120 per min | at the cap: 5 s cooldown |
| War Council | 1 per 2 s, burst 6 | — | 60 per min | — |
| Whisper | 1 per 2 s per thread, burst 5 | same | — | — |
| Circle | 1 per 2 s, burst 5 | same | 60 per min | — |
| All channels | ≤ 600 messages per player per day (10× the stress average) | ≤ 150 per day | — | above it: chat pauses until 00:00 UTC, logged as a bot signal |

Share cards and quick calls use the same buckets; extra per-type limits live in
[share-cards.md](share-cards.md) §7.

## 5. The trust ladder (never bought)

Trust grows with **time and clean play only** — never with payment (money-law; a paid bypass
would sell reach to gold sellers).

| Tier | Reached when (PROPOSAL; S = spine-building tier, design-forge core-loop.md notation) | Adds |
|---|---|---|
| T0 | new account (< 48 h since creation) OR S < 2 | Hall, Council if promoted, whispers with alliance mates, quick calls, stickers, share cards in the Hall; Market Cross read-only |
| T1 | ≥ 48 h AND S ≥ 2 | Market Cross at 1 per 30 s; 3 new whisper threads per day (as requests) |
| T2 | ≥ 7 d AND 0 active strikes | standard rates; 10 new threads per day; `@name` in Market Cross |
| T3 | ≥ 30 d AND no strike in 30 d | may be appointed a realm warden (§9); plain, non-clickable URL text in Hall and Council if the owner allows it (owner decision) |

A strike drops the player one tier for 7 days. Age bands (§10) cap the ladder further.

## 6. Abuse wordlists and severities

| Severity | Examples of classes | Action | Strike |
|---|---|---|---|
| S1 mild | common swearing | masked with ✱ for readers who keep the "strict" setting (default strict; adults may choose "standard") | no |
| S2 abuse | slurs, hate against protected groups, sexual harassment, severe insults | message rejected; sender told which rule class | yes |
| S3 danger | threats of violence, self-harm statements, sexual content involving minors, sharing someone's real address or phone number | rejected; the S3 queue gets the item with 10 lines of context; chat mute 24 h pending review | yes (confirmed by a human) |

- **One list per shipped language**, three severity files each, curated by native speakers through
  l10n-forge (≥ 1 native review per language per release). Open-licence lists may seed them —
  verify each licence before use.
- **Allowlist** per language for false positives found in the corpus (place names, troop names,
  lord names: Edwin, Alric, Elena, Rowan, Godric, Maud, Faber, Fable must never be masked).
- **List versions** are data files hot-reloaded by the server (no client release needed); the
  client copy (for instant feedback) updates with the game's content version.
- The `chat_filter_probe` corpus thresholds are in [qa.md](qa.md) §2: S2+S3 recall ≥ 95%, false
  positives on clean text ≤ 1%.

## 7. Links, contacts and gold sellers

**Rule: no clickable link anywhere, for anyone.** Text that looks like a link is either rejected
or shown as plain text (T3 adults in Hall/Council only, if the owner allows).

Seller score (sum of weights on the normalized copy; PROPOSAL values):

| Signal | Weight |
|---|---|
| URL pattern: scheme, `www`, a TLD after a dot or after "dot"/"d0t" | 4 |
| Contact pattern: ≥ 7 digits within 12 characters; e-mail shape; messenger handle words (per-language list) | 3 |
| Sell words near game currency ("cheap", "sell", "buy", price shapes like "5$", "€10", "usd") + "gems"/"gold" | 3 |
| Account T0/T1 | 2 |
| First message ever in Market Cross, or first whisper to a stranger | 1 |
| Same text to ≥ 3 channels or threads in 10 min | 3 |

- Score ≥ 6: **held for review** — the sender sees "Waiting for review" (never silently hidden;
  the sender is told, §12); readers see nothing until a warden or the owner approves.
- Score ≥ 9: rejected, 1 h mute, account flagged to cloud-forge's anti-cheat (real-money trading
  is economy abuse, design-forge economy.md).
- Held items expire unreviewed after 24 h (deleted, sender told).

## 8. Player tools (every channel, every message, ≤ 3 taps)

| Tool | Effect | Limits |
|---|---|---|
| **Report** | reason (spam or selling · harassment · hate · sexual · threat or self-harm · cheating · other) + optional note ≤ 200 chars; the server snapshots the message + 10 before and 5 after into the evidence store (90 d) | ≤ 20 reports per player per day |
| **Block** | hides all the target's messages in every channel for the blocker; stops whispers both ways; the target is not told | ≤ 500 blocks per player; unblock any time in settings |
| **Mute sender** | hides the sender in one channel for 1 h / 8 h / 24 h / always | client-side plus server filter on catch-up |
| **Officer tools (Hall)** | remove a message (tombstone); mute a member in the Hall 1 h or 24 h; every action logged in the alliance log | top two ranks (alliance.md); ≤ 50 actions per day |

After a report the reporter sees "Thank you — we will look at it" and, when a decision is made,
a short mail (mail-forge) saying action was taken or not (no details about the other player).

## 9. Moderation

**Queue shape**: the queue shows **offenders, not reports** — one case per reported player per
24 h with all reports, reasons, context snapshots, the seller score and history. Order: S3 first
(target: human review ≤ 24 h), then cases with ≥ 3 independent reporters, then the rest.

**Report weighting (anti-brigading)**: each reporter has an accuracy score (share of their past
reports upheld). Reporters under 20% accuracy count 0.2. Reports against one player from ≥ 3
members of one alliance within 1 h count as one report.

**Automatic actions** (limited, reversible):

| Trigger | Action |
|---|---|
| ≥ 3 independent weighted reports in 24 h against a T0/T1 account | chat mute 24 h pending review |
| Seller score ≥ 9 or a known seller text signature | 1 h mute + anti-cheat flag |
| S3 match | 24 h mute pending human review |
| Anything longer than 24 h | **human decision only** |

**Workload model** (base scenario, [backend-cost.md](backend-cost.md) §7): 300,000 messages per
day × 1–3 reports per 1,000 messages [assumption; measure] = 300–900 reports per day → grouped at
≈ 6 reports per offender ≈ 50–150 cases → 70–85% closed by the automatic rules → **10–45 human
cases per day × 45–90 s = 8–68 minutes of moderation per day**. Who does that work is an owner
decision (the owner, trusted volunteers, or a paid service — a paid service is outside the
server budget and needs its own line).

**Roles**:

| Role | Powers | Oversight |
|---|---|---|
| Owner / staff | everything, incl. permanent bans and appeals | — |
| Realm warden (T3 volunteer, PROPOSAL 2–4 per realm) | approve/deny held messages; mute ≤ 1 h in Market Cross; escalate | every action logged; staff audit 10% weekly; removed after 2 overturned actions in 30 d |
| Alliance officers | Hall only (§8) | alliance log |

**Sanctions ladder** (chat only; the game account is not touched unless cheating is involved):

| Strike | Sanction |
|---|---|
| 1 | warning + message removed |
| 2 | 1 h chat mute |
| 3 | 24 h chat mute |
| 4 | 7 d chat ban (human-confirmed) |
| 5 | permanent chat ban (human-confirmed); quick calls and stickers stay on |

Strikes decay: one strike removed per 30 clean days. Every sanction sends a statement of
reasons (§12). Appeals: a button in that mail → a form (≤ 500 chars) → staff answer ≤ 7 d.

## 10. Minors and age rating

**Age gate**: at account creation a neutral birth-year picker (no default year, no hint of the
threshold); only the **age band** is stored, never the date (data minimization). The band decides:

| Feature | Under the local age of digital consent (13–16 by country; the table is maintained by legal/l10n-forge) | Minor above it (to 17) | Adult (18+) |
|---|---|---|---|
| Free text | **off** (unless verified parental consent is added later — owner decision) | on, strict filter locked | on, strict by default, may choose standard |
| Quick calls, stickers, share cards | on | on | on |
| Hall (alliance) | reads mates' text with the strict filter plus contact masking (≥ 5 digits, e-mail shapes, handles shown as ✱); posts quick calls, stickers, cards | read and write | read and write |
| Market Cross | sees only quick calls, stickers and cards (free text from others hidden); posts quick calls only | read and write | read and write |
| Whispers | off | alliance and Circle mates only; never requestable by strangers | per setting |
| Link-like text, lock-screen previews | off | off | per settings |

**Store and rating obligations** (engineering checklist; **legal to confirm**):

- Apple App Store guideline 1.2 (user-generated content): a filter, a report mechanism with
  timely responses, blocking of abusive users, published contact information → §6, §8, §9, and the
  contact line in settings.
- Google Play user-generated-content policy: terms accepted before a player can post, in-app
  reporting and blocking, ongoing moderation → first-post terms sheet + §8 + §9. If the target
  audience includes children, the Google Play Families policy also applies (owner decides the
  target audience).
- IARC questionnaire: declare "Users Interact" (chat) — the rating shown in stores changes with it.
- US COPPA (under 13) and GDPR Art. 8 (13–16 by member state): no free text for those players
  without verified parental consent → the table above.
- UK Age Appropriate Design Code: high-privacy defaults for minors → the table above.

## 11. Privacy and data (GDPR)

| Item | Rule |
|---|---|
| Lawful basis | contract (providing chat) for messages; legitimate interest for safety logs and evidence — **legal to confirm** and write into the privacy notice |
| Retention | [channels.md](channels.md) §1 (realm 3 d, alliance/whisper/Circle 30 d, Herald 7 d); evidence store 90 d or case closed + 30 d; IP addresses in gateway logs ≤ 7 d; moderation decisions pseudonymised 1 year |
| Erasure (Art. 17) | account deletion runs a chat job **≤ 30 days** (Art. 12(3) one month): whispers and Circle messages by the account hard-deleted; public-channel rows replaced by tombstones; read cursors, blocks and mutes deleted; sender id replaced by "Former lord" in evidence copies |
| Backups | 7 daily compressed dumps + WAL; deleted rows leave the backups ≤ 7 days after deletion (stated in the privacy notice) |
| Access / portability (Art. 15, 20) | export of the player's own messages still inside retention as JSON, from the account's data request flow |
| Processors | hosting provider; the cloud translation fallback (text leaves the device) — both need a DPA; on-device translation keeps text on the phone |
| Data location | EU hosting preferred (verify the host's region and sub-processors) |
| Client cache | encrypted, wiped on logout and on leaving an alliance ([ui.md](ui.md) §11) |

## 12. Transparency and notices (EU Digital Services Act — **legal to confirm** applicability)

- Anyone can report any message (notice and action) → §8.
- Every restriction (message removed, held, mute, ban) sends the affected player a **statement of
  reasons** by mail-forge: what was restricted, which rule, whether it was automated, duration,
  how to appeal. That is why held messages show "Waiting for review" instead of being silently
  hidden.
- Keep the counts for a yearly summary (reports received, actions, automated share, median time
  to decision) — a daily counter row, no extra storage cost.

## 13. Failure modes

| Fails when | Caught by |
|---|---|
| Obfuscated seller text ("w w w . g e m s 4 u . c 0 m") passes | [ ] `chat_filter_probe` obfuscation corpus, link recall ≥ 99% |
| A lord or place name is masked | [ ] clean corpus includes every lord, troop line and building name; false positives ≤ 1% |
| Reversed or spoofed names via bidi characters | [ ] `chat_injection_probe` bidi cases |
| A T0 account posts in Market Cross | [ ] `chat_trust_probe` ladder matrix |
| An under-consent-age account can send free text or whisper a stranger | [ ] `chat_age_probe` band matrix |
| Report brigade mutes an innocent player automatically | [ ] brigading unit test: 5 alliance-mates' reports count as 1 |
| An erased account's whispers still in the DB after the job | [ ] `gdpr_erasure_probe`: 0 rows with the author id |
| Moderation queue grows faster than it is worked | [ ] daily counter: open cases > 3× daily closed for 3 days → alert the owner |

## 14. Safety checklist (every chat change)

- [ ] Server-side for every rule; client only mirrors.
- [ ] Hygiene limits (§2) apply to the new field, including names and card labels.
- [ ] Rate-limit row and trust tier row exist for any new channel or type.
- [ ] Report, block, mute reachable in ≤ 3 taps from the new content.
- [ ] Age-band row filled; nothing new reaches under-consent-age players as free text.
- [ ] Retention and erasure rules cover the new data; evidence copies expire.
- [ ] Every automated action logs rule id + list version and sends a statement of reasons.
- [ ] Filter corpus extended with the new content's words (names, places) and re-run.
