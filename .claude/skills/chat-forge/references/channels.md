# Channels — who talks to whom, for how long, how fast

Every number in this file is a **PROPOSAL** unless it quotes a canonical fact. The game's
shipped chat code and data are not visible here (repo on the owner's machine; paths to
confirm). Alliance ranks, size cap and permissions belong to design-forge
[alliance.md](../../design-forge/references/alliance.md); realm size belongs to design-forge
world.md; this file only says what chat does with them. Implementation: **cloud-forge**
(gateway, storage), **ui-forge** (screens, via [ui.md](ui.md)), **story-forge** (names),
**l10n-forge** (quick-call strings, wordlists), **qa-forge** (probes in [qa.md](qa.md)).

## 1. The channel catalogue

Diegetic names are proposals to story-forge (canon owner). The code id is what the wire
format and the data use ([backend-cost.md](backend-cost.md) §3).

| Code id | Diegetic name (PROPOSAL) | Members | Who can post | Retention (days / count guard) | Live fan-out |
|---|---|---|---|---|---|
| `r:<realm>` | Market Cross | every player of the realm | trust T1+ ([safety.md](safety.md) §5) | 3 d / last 1,000 kept for scroll-back | only to players with the realm tab open, or the realm ticker opted in (sampled, §7) |
| `a:<alliance>` | Hall | alliance members | every member | 30 d / last 5,000 | every online member (default ticker channel) |
| `o:<alliance>` | War Council | the top two ranks + ranks granted "council" (alliance.md) | members of the channel | 30 d / last 2,000 | every online member of the channel |
| `w:<lo>:<hi>` | Whisper (1:1) | two players (`lo` < `hi` player ids, so one thread per pair) | both, unless one blocked the other | 30 d / last 500 per thread | the other player; push if offline (§8) |
| `g:<id>` | Circle (group) | 3–20 invited players | members | 30 d / last 1,000 | online members |
| `h:<alliance>` | Herald (system feed) | alliance members | server only | 7 d / last 500 | online members; merged into the Hall view as system lines |
| `hr:<realm>` | Realm Herald | realm | server only (realm events, owner news) | 7 d / last 200 | shown as system lines in Market Cross |

Rules:

1. **One realm channel per realm.** Language rooms (§9) are an opt-in split, not a default.
2. **The Hall is the default ticker channel** for every player in an alliance; a player with no
   alliance sees Market Cross in the ticker (sampled, §7). This single default is the biggest
   cost lever in [backend-cost.md](backend-cost.md) §7 — realm fan-out is 61–83% of all
   deliveries in every scenario.
3. **Retention is whichever limit comes first**: days or the count guard. Nothing is kept
   longer "in case" (GDPR storage limitation, [safety.md](safety.md) §11). Reported messages
   are copied to the evidence store (90 d) — the chat row itself still expires on time.
4. **No chat channel is a record.** Anything a player must be able to find again later
   (rewards, sanctions, officer orders, reports) goes to the inbox (**mail-forge**) or the report
   archive (**report-forge**); chat only links to it with a share card ([share-cards.md](share-cards.md)).
5. **Private data never crosses channels by itself**: an officer message can be shared to the
   Hall only by re-typing or a share card that the sharer creates; there is no "forward".

| Fails when | Caught by |
|---|---|
| Realm fan-out goes to every online player (ticker default = realm) | [ ] `chat_cost_probe` deliveries/day per channel vs the tool's base line |
| A channel keeps rows past its retention | [ ] `chat_retention_probe`: 0 rows older than retention + 1 d |
| A player who left an alliance still receives Hall or Council lines | [ ] `chat_membership_probe` leave/kick/disband cases |

## 2. Message types

| Type | Wire kind | Payload | Size cap | Allowed in | Rendering |
|---|---|---|---|---|---|
| Text | `x` | UTF-8 text | ≤ 200 graphemes AND ≤ 800 bytes; ≤ 3 line breaks | all player channels | row with name line ([ui.md](ui.md) §3) |
| Reply | `x` + `re` | text + id of the quoted message | as text; quote shows ≤ 60 graphemes of the original | all player channels | quote strip above the text |
| Sticker | `s` | sticker id (u16) | 2 bytes of data | all player channels, all ages | 240 px painted sticker ([ui.md](ui.md) §7) |
| Quick call | `q` | phrase key + validated args | ≤ 64 bytes | all player channels, all ages | text in the READER's language (§7) |
| Share card | `k` | card envelope | ≤ 256 bytes | per card type ([share-cards.md](share-cards.md) §2) | 800 × 248 px card |
| Announcement | `n` | text | ≤ 400 graphemes / 1,600 bytes | Hall; one pinned at a time | pinned strip at the top of the Hall |
| System line | `y` | l10n key + args | ≤ 128 bytes | Herald channels | centred grey line, no avatar |
| Tombstone | `d` | id of the removed message | 12 bytes | all | "Message removed" in 28 px italic, no content |

Rules:

1. **Every system text is a string key + arguments**, never baked text: each reader sees their
   own language (l10n-forge). Arguments are ids (player, alliance, lord, tile), resolved to names
   on the client at render time — a renamed player shows the new name.
2. **No editing.** A sender may delete their own message at any time inside its retention (a
   tombstone replaces it for everyone at once). The server keeps the deleted text hidden for 24 h
   so a report filed in that window still captures it, then erases it ([safety.md](safety.md) §11).
   Editing invites bait-and-switch after replies.
3. **No clickable links in any message type, for any account** ([safety.md](safety.md) §7).
   Share cards are the only tappable content, and the server builds them.
4. **Unknown kinds render as nothing** and are logged once per session (old clients meet new
   kinds safely; the protocol version is in the hello frame, [backend-cost.md](backend-cost.md) §3).

## 3. History and membership rules

| Event | Rule (PROPOSAL) |
|---|---|
| Player joins an alliance | sees the last 50 Hall messages (alliance setting: 0 / 50 / 200; default 50); never Council history |
| Promoted into the Council | sees Council messages from the promotion time only |
| Leaves, is kicked, alliance disbands | Hall, Council and Herald access ends at once; the client deletes those channels from its cache on the membership event |
| Moves to another realm (migration, liveops.md) | Market Cross switches; whispers and Circles move with the player; realm history is not carried |
| Blocks a player | that player's messages are hidden in every channel for the blocker; whispers stop both ways |
| Account deleted (GDPR) | [safety.md](safety.md) §11: whispers/Circle messages by the account hard-deleted; public-channel rows replaced by tombstones within 30 d |
| Alliance hopping | chat adds no rule of its own; alliance.md's cooldowns apply. The Herald shows "joined / left" lines so hopping is visible |

## 4. Mentions

| Mention | Who may use it | Limit | Effect |
|---|---|---|---|
| `@name` | anyone in a channel where the target is a member | ≤ 5 per message | mention badge + optional push ([ui.md](ui.md) §5, §8 here) |
| `@council` | top two ranks | ≤ 10 per day per alliance | mention for every Council member |
| `@all` (Hall) | top two ranks | ≤ 3 per day per alliance; ≥ 30 min apart | mention for every member; push only for members who opted in |
| `@` in Market Cross | anyone T2+ | ≤ 5 per message | mention badge only, never a push (strangers must not push strangers) |

The mention is stored as a player id inside the text (`<@55123>`) and rendered as the current
name; typing `@` opens a picker of channel members sorted by last active (≤ 3 taps to insert).
Blocked players cannot mention the blocker (silently dropped for that recipient).

## 5. Announcements and the Herald

- **Pinned announcement**: one per alliance, set by the top two ranks, ≤ 400 graphemes, shows
  the author and the date; replacing it moves the old one to the Hall as a normal line. The
  scheduled announcement tool (leader burnout relief) belongs to alliance.md; chat renders it.
- **Herald events** (PROPOSAL list; each owning system emits the key, chat renders it):

| Event | Owner | Merge rule |
|---|---|---|
| member joined / left / kicked / rank changed | alliance (gameplay-forge) | one line each |
| rally opened (with rally card) | battle-forge | one line per rally |
| member under attack (with coordinates card) | battle-forge | per member ≤ 1 per 10 min; members opt in |
| alliance research finished, territory gained or lost, landmark taken | gameplay-forge / world-forge | one line each |
| gifts received | alliance (gameplay-forge) | aggregated: ≤ 1 line per 10 min ("12 gifts from camp kills") |
| event started / ending in 1 h | liveops (design-forge liveops.md) | ≤ 2 lines per event |

- **Herald cap**: ≤ 30 lines per hour per alliance; above it, lines merge into a digest line
  ("8 more alliance events — open the Herald"). Herald lines never push.
- A Herald line is not a claim: gifts are claimed in the alliance screen or the inbox (mail-forge).

## 6. Whispers and Circles

| Rule | PROPOSAL | Why |
|---|---|---|
| Who may start a whisper | same realm or same alliance; the recipient's setting decides: everyone (adults only) / alliance and Circle mates (default) / nobody | strangers are the main harassment and seller channel |
| First whisper from a non-alliance stranger | arrives as a **request**: the text is held and shown after the recipient taps Accept; Ignore and Block are one tap each | a seller's first line never lands unread |
| New threads per day | T1: 3 · T2+: 10 · requests count | caps cold-contact spam |
| Minors | under the local age of digital consent: whispers off; above it (to 17): only with alliance and Circle mates, never requestable by strangers | [safety.md](safety.md) §10 |
| Circle size | 3–20; creator invites; members accept; creator can remove; empty Circle deleted after 7 d | small and consent-based |
| Circles created per day | ≤ 3 per player; ≤ 10 Circles per player total | caps group spam |

## 7. Quick calls and the ticker sample

**Quick calls** (the "horn calls") are preset phrases every age band may use. They render in the
reader's language, so they are the only chat that crosses a language gap for free. 24 keys
(PROPOSAL; l10n-forge writes the strings, story-forge the voice):

| Group | Keys |
|---|---|
| War | `rally_at {coords}` · `join_rally` · `reinforce {player}` · `under_attack {coords}` · `shield_up` · `hold_line` · `fall_back` · `target {coords}` · `scout {coords}` |
| Economy | `gather_here {coords}` · `ask_help_timers` · `donate_research` · `thanks_help` |
| Social | `hello` · `good_night` · `welcome` · `thank_you` · `well_fought` · `sorry` · `ready` · `wait_for_me` · `follow {player}` · `good_luck` · `congrats` |

Arguments are validated by the server (a coordinate on the realm's grid; a player who is in
the channel). A quick call counts against the rate limit like text.

**Ticker sampling (realm)**: a player who opts the realm into the ticker receives at most one
realm message per 10 s (the newest, `ticker_ratio` 0.3 in the cost tool), not the full stream.
The full stream starts when the realm tab opens and stops 5 s after it closes.

## 8. Push policy (the only chat events that may leave the game)

Push is sent only when the recipient has no open socket, and it shares the day's push budget of
design-forge core-loop.md A8 (≤ 4 per day, grouped, quiet hours 22:00–08:00 local).

| Event | Default | Coalescing | Lock-screen text |
|---|---|---|---|
| Whisper (accepted thread) | on | 1 push per thread per 10 min; later messages update the count | "A whisper from Aldric" — no message text by default |
| Whisper request from a stranger | off | — | — |
| `@name` in Hall, Council or Circle | on | 1 per channel per 30 min | "Aldric mentioned you in the Hall" |
| `@all` / `@council` | opt-in | 1 per call | "Your alliance calls: rally at the ford" (from the quick-call key, localized) |
| Rally call card | opt-in (battle-forge rally flow) | 1 per rally | localized rally key |
| Market Cross, Herald, stickers, group chatter | never | — | — |

- Chat pushes use at most **2 of the 4** daily A8 slots by default. A player who turns on
  "every whisper" may exceed A8 for whispers only — the player's explicit choice
  (owner decision #4 in SKILL.md).
- Message text on the lock screen: opt-in, adults only.
- Never a push for an offer, a shop item or anything paid (money-law).

## 9. Hooks for later (costed before they exist)

- **Language rooms**: when ≥ 20% of a realm's weekly senders write in one other language
  (server language-id on sent text), the realm offers `r:<realm>:<lang>`; fan-out per room is
  smaller, so cost falls. Players choose their room; the realm room stays.
- **Season / cross-realm coalition channel** (design-forge liveops.md seasons): one channel per
  coalition; fan-out = coalition online members. Add its line to the cost tool (`mix` + a
  recipients term) before it ships; cap 20 msg/min like a realm.
- **Voice**: out of scope (moderation cost and minors risk); any proposal goes to the owner.

## 10. Failure modes

| Fails when | Caught by |
|---|---|
| A stranger's first whisper is shown before the recipient accepts | [ ] `chat_membership_probe` request case |
| Quick call shows the sender's language to a reader of another language | [ ] `chat_l10n_probe`: 24 keys × shipped languages render, 0 missing keys |
| Herald floods the Hall in a war hour (> 30 lines) | [ ] Herald merge unit test at 100 events/hour |
| `@all` used more than 3 times a day | [ ] server cap test |
| Chat push arrives in quiet hours or for Market Cross | [ ] `chat_push_probe` with a fake clock |
| Council history visible to a newly promoted member | [ ] membership probe promotion case |

## 11. Channel checklist (any change to channels)

- [ ] Channel row filled: members, posters, retention days + count guard, fan-out rule.
- [ ] Rate limit row added in [safety.md](safety.md) §4 and age-band row in §10.
- [ ] Cost tool line updated (`mix`, recipients, retention) and re-run; result pasted.
- [ ] Push row decided (default off unless it is a whisper, a mention or a rally).
- [ ] Membership events (join, leave, kick, disband, migrate, block, delete) each have a rule.
- [ ] Diegetic name sent to story-forge; strings to l10n-forge.
