# QA — the chat harness battery, corpora, gates, predictions

chat-forge names what must be proven; **qa-forge** writes the probes that do not exist yet
(paths to confirm in the owner's repo); **cloud-forge** runs the server-side ones. Verdict lines
below are PROPOSED wording — qa-forge fixes the final text, and the thresholds stay.
Nothing in chat is "done" without the pasted verdict lines (game-director hard rule 3).

## 1. The battery

### 1.1 New chat probes (qa-forge writes them)

| Probe | Lane | Proves | Pass threshold | Verdict line (PROPOSED) |
|---|---|---|---|---|
| `chat_filter_probe` | headless (server filter module + client mirror) | wordlists, normalization, links, sellers | S2+S3 recall ≥ 95%; clean-text false positives ≤ 1%; link/contact recall ≥ 99% on the obfuscation set; every shipped language | `CHAT FILTER OK - 9 langs, recall 96.8%, fp 0.6%, links 99.5%` |
| `chat_injection_probe` | headless client | BBCode, bidi, zero-width, zalgo, oversize, control characters | 0 parsed tags; 0 bidi overrides stored; all oversize rejected | `CHAT INJECTION OK - 412 cases, 0 parsed, 0 stored overrides` |
| `chat_trust_probe` | server | trust ladder T0–T3 and rate buckets | every matrix cell as [safety.md](safety.md) §4–§5 | `CHAT TRUST OK - 4 tiers x 5 channels, 0 faults` |
| `chat_age_probe` | server + client | age-band feature matrix | every cell as [safety.md](safety.md) §10; 0 free text from under-consent accounts | `CHAT AGE OK - 3 bands x 9 features, 0 faults` |
| `chat_membership_probe` | server | join, leave, kick, disband, promote, migrate, block, whisper requests | no delivery to a non-member within 1 s of the event; history rules of [channels.md](channels.md) §3 | `CHAT MEMBERSHIP OK - 11 events, 0 leaks` |
| `chat_catchup_probe` | server + headless client | offline 1 min / 1 h / 24 h / 8 d; resend with the same `cid`; tombstones | unread counts exact ±0 for ≤ 50 missed; 0 duplicates; gap marker correct | `CHAT CATCHUP OK - 4 gaps, 0 dupes, unread exact` |
| `chat_retention_probe` | server (nightly) | partitions dropped, count guards, evidence expiry | 0 rows older than retention + 1 d | `CHAT RETENTION OK - oldest 3d/7d/30d within limits` |
| `gdpr_erasure_probe` | server | account erasure job | 0 rows with the author's id in whisper/Circle tables; tombstones in public channels; job ≤ 30 d (runs in minutes in staging) | `CHAT ERASURE OK - 0 rows, 37 tombstones` |
| `chat_push_probe` | server, fake clock | push rules, quiet hours, coalescing, A8 budget | 0 pushes for Market Cross/Tidings; 0 in quiet hours; ≤ 2 chat pushes/day by default | `CHAT PUSH OK - 0 forbidden, budget 2/4` |
| `share_card_probe` | server + headless client | six card types round trip; forged snapshots; stale; forbidden; sizes | envelope ≤ 256 B; forged `snap` ignored; stale renders, never errors | `SHARE CARDS OK - 6 types, 0 forged, 0 errors` |
| `chat_l10n_probe` | headless client | quick-call keys, Tidings keys, card strings in every shipped language | 0 missing keys; 0 clipped strings at +40% length | `CHAT L10N OK - 24 calls x 9 langs, 0 missing` |
| `chat_load_probe` | server (staging) | stress profile ([backend-cost.md](backend-cost.md) §8) for 30 min | p95 delivery ≤ 1 s; CPU ≤ 60%; 0 lost; reconnect storm ≤ 1,000 connects/s | `CHAT LOAD OK - 9.4k sockets, p95 0.41s, cpu 48%, lost 0` |
| `chat_cost_probe` (a chat line in `core/sd_cost_probe.gd`) | server counters | measured rates scaled to 50k players | ≤ the chat envelope (PROPOSAL €50) | `CHAT COST OK - measured €18/month at 50k, envelope €50` |
| `tools/chat_cost.py --selftest` | local | the cost arithmetic itself | 14 checks | `CHAT COST SELFTEST OK - 14 checks` |

### 1.2 The owner's existing harnesses that must run on chat changes

| Harness | Lane | What it must show for chat |
|---|---|---|
| `contrast_test` | headless | every chat text pair ≥ 4.5:1 ([ui.md](ui.md) §3 table) |
| `menu_test` | headless | chat panel opens/closes from the ticker, every tab reachable |
| `layout_audit` | windowed | ticker and panel inside their zones; +30–40% strings do not clip |
| `ux_flow_probe` | windowed | chat pass: open, send, report (≤ 3 taps), share a card (≤ 3 taps), every §9 state screenshot |
| `ux_touch_probe` | windowed | every chat control ≥ 120 px hit area (48 dp) |
| `a11y_audit` | windowed | no flashing, text scale 130% reflows, relationship marker has a shape |
| `w1f_aspect_sweep` | windowed | `ASPECT SWEEP OK - 6 shapes, 0 faults` with the panel open and the keyboard height mocked |
| `session_audit.gd` | windowed | the full session still passes with chat open and with the chat box killed (isolation) |
| `core/audit.gd`, `backlog_gen.gd` | headless | area scores do not drop |

## 2. Corpora (versioned data, extended every release)

| Corpus | Size per shipped language (minimum) | Content |
|---|---|---|
| Abuse (S2/S3) | 500 lines | real-style abuse per class, incl. obfuscations (§3 of safety.md) |
| Clean | 1,500 lines | ordinary chat, war talk ("kill the camp", "burn the gate"), every lord, troop line, building and place name, common town names that contain rude substrings |
| Obfuscation | 300 lines | spaced letters, leet, confusables, fullwidth, zero-width inserts, "dot com" spellings, phone numbers split by words |
| Seller | 200 lines | currency-selling lines in each language, with and without contacts |
| Care | 100 lines | self-harm statements (must trigger the help card and never a sanction) |
| Injection | 400 cases (language-free) | BBCode tags, nested tags, 10,000-character strings, bidi overrides, zalgo, control characters, broken UTF-8, 4-byte emoji sequences with ZWJ |

War vocabulary is **clean** in this game: "kill", "burn", "raid", "siege", "slaughter the camp" must
pass. A filter that blocks the game's own verbs fails the clean corpus.

## 3. Launch gate (all true before chat reaches players)

- [ ] Every probe in §1.1 green with pasted verdict lines; §1.2 harnesses green.
- [ ] `chat_cost.py` re-run with measured staging counters; A1 inside the envelope at stress.
- [ ] Store checklist of [safety.md](safety.md) §10 done: report, block, filter, contact info, terms before first post, IARC "Users Interact" declared.
- [ ] Privacy notice lists chat retention, processors, erasure time; DPA with host (and translation, if the cloud fallback ships).
- [ ] A named person for the moderation queue and the S3 review ≤ 24 h (owner decision #3 in SKILL.md).
- [ ] Wordlists natively reviewed for every shipped language (l10n-forge sign-off).
- [ ] Load test passed on the production box size; restore drill done (RTO ≤ 30 min measured).
- [ ] Real-phone smoke (owner-only item): send, receive, push, keyboard, background/foreground, low-end phone frame times.

## 4. Review checklist (the hostile pass for any chat change)

1. **Numbers**: every new rule has its number (rate, size, retention, ms, px) and the number
   has a source or is marked PROPOSAL.
2. **Cost**: the tool re-run; which scenario line moved and by how much; B/C shapes still banned.
3. **Failure modes**: the change adds at least one "Fails when → Caught by" row.
4. **Safety**: server-side, report ≤ 3 taps, trust and age rows, statement of reasons.
5. **Privacy**: new data has a retention, an erasure path and a place in the export.
6. **Readability**: contrast pairs, 120 px targets, 28 px minimum text, +40% strings.
7. **Money-law**: nothing in chat is sold as reach, speed, colour or length; no offer in chat.
8. **Isolation**: chat down → the game still runs (session_audit with the chat box killed).
9. **Ownership**: every file touched belongs to its skill (report content → report-forge; inbox → mail-forge; screens → ui-forge).

## 5. Predictions vs measured (fill after launch; each gap becomes a lesson)

| Metric | Predicted (base) | Measured | Gap → lesson |
|---|---|---|---|
| Messages sent per DAU per day | 15 | | |
| Market Cross share of sent | 20% | | |
| Deliveries per day at 50k-equivalent | 2.75 M | | |
| Realm share of deliveries | 61% | | |
| Egress per month | 64 GB | | |
| Storage | 2.8 GB | | |
| Reports per 1,000 messages | 1–3 | | |
| Human moderation minutes per day | 6–68 | | |
| Held-for-review items per day | < 1% of Market Cross messages | | |
| Filter false positives in live appeals | ≤ 1% of automated actions overturned | | |
| p95 delivery latency | ≤ 1 s | | |
| Chat € per month (A1) | €4–€30 | | |

Lessons are handed to the game-director lead for `game-director/references/lessons.md`
(one writer per file); the chat-specific recipe change is written back into the owning
reference here (game-director hard rule 7).

## 6. Failure modes of the QA itself

| Fails when | Caught by |
|---|---|
| Corpus stops growing while languages are added | [ ] `chat_filter_probe` refuses a language with fewer lines than §2 |
| Probes pass on a mocked server but prod config differs (limits, lists) | [ ] probes read the same config files the server loads; config hash printed in the verdict |
| Cost measured on a quiet staging week | [ ] the cost line always prints the three tool scenarios beside the measured one |
