# Categories — what goes in the inbox, for how long, and who is told

Every number in this file is a **PROPOSAL** unless it quotes a canonical fact. The shipped mail
code and data are not visible here (the repo is on the owner's machine). Paths come from the
studio's cloud-forge brief and are marked "(path to confirm)". Alliance ranks and caps belong to
design-forge [alliance.md](../../design-forge/references/alliance.md); reward timing belongs to
[liveops.md](../../design-forge/references/liveops.md) R7; chat channels and safety belong to
**chat-forge**. This file says what mail does with them.

## 0. Who owns what

| Piece | Owner | mail-forge's part |
|---|---|---|
| Inbox content rules: categories, retention, badges, push, letters, alliance mail | **mail-forge** | this file |
| Claim protocol, attachments, send jobs | **mail-forge** | [attachments.md](attachments.md) |
| Report CONTENT: schema, "why you won/lost", layouts, report bodies and their retention | **report-forge** | delivers the row, the tab, the badge rule (§9) |
| Chat channels, share cards, filter, trust tiers, age bands, moderation queue | **chat-forge** | calls the same filter, uses the same block list and share-card format |
| Screens, components, Theme, list recycling | **ui-forge** | content spec in [ui.md](ui.md) |
| Storage, rules, functions code, save sync, budget alerts | **cloud-forge** | data layout and cost in [backend-cost.md](backend-cost.md) |
| Painted headers | **game-art-director** | spec in [templates.md](templates.md) §6 |
| Seal, tab and claim icons (Blender-made art, never line glyphs) | **blender-forge** via ui-forge | names the icons needed ([ui.md](ui.md) §3) |
| Names and voice (the Chancery, tab names) | **story-forge** | proposals only |
| Strings, plurals, fonts | **l10n-forge** | keys and args in [templates.md](templates.md) |
| Claim ceremony, sounds | **feel-forge**, **audio-forge** | timings in [ui.md](ui.md) §9 |
| Reward amounts, event results, gifts | design-forge liveops / alliance / economy | carries them, never sets them |

## 1. The five tabs

Diegetic names are proposals to story-forge. The screen is **Letters**. System mail is signed by
**the Chancery** (the castle office that writes letters and writs). The words "Herald" and
"Steward" are not used for mail: chat-forge's Herald is the system feed, and the alliance has
Herald and Steward offices ([alliance.md](../../design-forge/references/alliance.md) §2).

| Tab | Code `k` | What arrives | Written by | Stored | Attachments | Body | Badge on the HUD icon | Push |
|---|---|---|---|---|---|---|---|---|
| **Notices** | `n` | maintenance, patch notes, news, event opening notices, policy and security | send job (ops, liveops) | copied into each player's node ([backend-cost.md](backend-cost.md) §3) | never | template key + args + painted header id | never | never |
| **Rewards** | `w` | event milestones (liveops R7), rankings (cosmetic), season chronicle, compensation, welcome, lord refit notes (lords.md) | send job | each player's node | yes — [attachments.md](attachments.md) | template key + args | yes, until claimed | never |
| **Alliance** | `a` | officer mail to all members; alliance system mail to one member (alliance.md §13) | Liege or Herald office (function); alliance system (server) | alliance-wide: once per alliance · to one member: that member's node | never | officer text ≤ 1,000 characters, or a template | yes, unread and < 7 d old | alliance-wide: opt-in, ≤ 1 per day |
| **Personal** | `l` | letters between players, diplomacy between alliance leaders | players (through the send function) | recipient's node | never — players cannot send goods (economy.md owns transfers) | plain text ≤ 500 characters + ≤ 1 share card | yes, from known senders, < 7 d old | known senders only, ≤ 1 per 30 min |
| **Reports** | `r` | a row per battle, defence, scout, rally, hunt order, daily gathering ledger | the report writer (resolver side) | each participant's node (row only) | never | report-forge content | never | never (battle-forge owns attack alerts) |

**Requests** is a list inside Personal: letters from strangers wait there, text hidden until the
player taps Accept (the same rule as chat-forge whispers). **Kept** is a filter across tabs.

Rules:

1. **Attachments exist only on Rewards letters in the player's own node.** Notices, alliance mail,
   letters and report rows never carry goods. Compensation for "everyone" is a Rewards letter per
   eligible player, never a shared notice with a claim button.
2. **Text is keys, not baked sentences**, for every letter the game writes (Notices, Rewards,
   alliance system mail, officer templates). Only players type free text ([templates.md](templates.md)).
3. **The inbox is not a shop.** No offer, price, buy button or shop link appears in any letter, header
   or toast (money-law). A purchase is delivered by shop-forge at purchase time, never by mail.
4. **Every row names its sender** in words and a sigil: the Chancery seal, an alliance sigil (ALS),
   a player's name, or the report kind — never an anonymous "System".

## 2. Lifetime of a letter

`t` = sent, `x` = hard expiry (both server milliseconds). "Held" = stored in the player's node.

| Tab | Unread held | After read / claim | Hard expiry `x` | Tab cap (newest kept) |
|---|---|---|---|---|
| Notices | 14 d | 3 d after read | `t` + 14 d | 50 |
| Rewards | claim window 30 d, then **auto-claimed at the next open** | 3 d after claim | `t` + 90 d | 200 — overflow auto-claims the oldest, never drops it |
| Alliance (to you) | 30 d | 7 d after read | `t` + 30 d | 100 |
| Alliance-wide (shared) | 30 d in the alliance node | hidden locally when read and deleted | `t` + 30 d | last 100 per alliance |
| Personal letters | 30 d | 7 d after read | `t` + 30 d | 200 |
| Requests | 7 d, then removed | — | `t` + 7 d | 50 (oldest removed first) |
| Report rows | as report-forge sets for the body (PROPOSAL 7 d PvE, 14 d PvP) | — | the body's expiry | 100 rows |
| Kept (any tab but Rewards) | no expiry while kept | — | ignored while kept | **40**; Guild Patronage rank IV: 100 (= "mail archive × 2.5", [monetization.md](../../design-forge/references/monetization.md) §6) |

Rules:

1. **No reward is lost to a missed deadline.** Day 30 is when the Chancery claims for you, not when
   the reward disappears. The next open after day 30 claims the reward through the same gate
   ([attachments.md](attachments.md) §7), and a digest line says so. Only after `x` = 90 days with no
   session at all is the reward gone. The welcome-back card (onboarding-forge) covers a player who
   was away longer. This keeps liveops R7 ("unclaimed mail keeps ≥ 30 days, 0 lost").
2. **Nothing a player might need disappears unseen.** A letter never expires before its tab shows it
   once, except Requests (spam protection) and Notices older than 14 d.
3. **Purging is lazy and costs no server ticks**. At the first session of the day, the client
   deletes its own expired, read, unkept and claimed items in one batched write. The database rules
   refuse any delete of an unclaimed reward ([attachments.md](attachments.md) §4).
4. **Dormant accounts are swept.** A monthly cold-account job deletes the mail node of accounts with
   no session for > 90 days. Notice send jobs skip accounts with no session for > 14 days, and
   compensation jobs skip accounts with none for > 30 days. Without this, the storage bill grows
   forever (trap `leak`: +USD 146/month at stress, [backend-cost.md](backend-cost.md) §9).
5. **Mail attachments never include a currency that expires before `x`** (event tokens after the
   event, season points after the season). The template validator refuses it
   ([templates.md](templates.md) §7).

## 3. Deletion

| Action | Taps | Rule |
|---|---|---|
| Delete one letter | 2 (⋯ → Delete) | a letter with unclaimed rewards shows **Claim & delete** instead; one tap does both |
| Delete read (per tab) | 3 (⋯ → Delete read → confirm) | skips unclaimed rewards and Kept; the result line counts what was skipped |
| Multi-select delete | long-press 500 ms, tap rows, Delete | same skips; "3 letters still hold rewards — Claim & delete them?" |
| Leave or lose an alliance | 0 | shared alliance mail disappears from the cache on the membership event (chat-forge parity); alliance mail sent to you personally stays |
| Account deletion (GDPR) | — | own node deleted at once; letters the player wrote in other inboxes are hard-deleted within 30 d; evidence copies name the sender "Former lord" (chat-forge safety.md §11) |
| Log out | — | the local mail cache (encrypted, [ui.md](ui.md) §11) is wiped |

"Never delete unclaimed rewards without warning" (brief) is stronger here: the database refuses
the delete, so no client bug and no batch action can do it.

## 4. Badges (red dots)

The HUD letter icon shows ONE number badge (ui-forge rule 10: dots only for something claimable,
idle or addressed to the player; core-loop A7: ≤ 3 dots at open for the median player).

```
badge = unclaimed Rewards letters
      + unread Personal letters from known senders, sent < 7 d ago
      + unread Alliance mail (to you or alliance-wide), sent < 7 d ago
      + unread account notices (statement of reasons, security) — the only Notices that count
shown: 1–9, then "9+"; 32 px digits; hidden at 0
```

1. **Never counted**: Notices (except account notices), Reports, Requests, anything older than 7
   days, and Kept.
2. Inside the screen every tab shows its own unread count, including Notices and Reports.
3. **Batching**: arrivals within 10 s make ONE toast ("3 letters · 2 with rewards"). There is at most
   1 mail toast per 5 min, never over battle presentation (battle-forge), and never during a ceremony
   (feel-forge's one-popup law).
4. "Claim all" clears the Rewards part of the badge in one tap. Opening a letter clears its unread.
   "Mark all read" per tab = 1 tap.
5. The badge updates from the head counters before any letter is fetched
   ([backend-cost.md](backend-cost.md) §3), so it appears at resume without an extra round trip.

## 5. Push

Push shares the day's budget in core-loop A8 (≤ 4 per day, grouped, quiet hours 22:00–08:00 local).
chat-forge takes ≤ 2 of the 4 slots. **Mail takes ≤ 1 by default.**

| Event | Default | Coalescing | Lock-screen text |
|---|---|---|---|
| Letter from a known sender (alliance mate, contact, diplomat) | on | 1 per 30 min; later letters update the count | "A letter from Aldric" — no text preview by default; preview opt-in, adults only |
| Alliance-wide mail from the Liege or Herald | opt-in | ≤ 1 per member per day (alliance.md §13, shared with chat) | the template subject in the reader's language |
| Rewards, Notices, Reports, Requests | never | — | — |
| Anything paid or promotional | never (money-law) | — | — |

Auto-claim (§2 rule 1) removes the only reason the genre pushes about mail: an expiring reward.

## 6. Offline delivery and sync

Mail is **store-and-forward**. The sender never needs the recipient online, and the recipient never
needs the sender online. Sequence at resume:

1. The head counters (`w l n r a`, about 50 bytes) arrive with the read cloud.gd already makes at
   resume (cloud-forge chooses the node; path to confirm). The badge updates. No mail round trip yet.
2. At the first session of the day, and whenever the head changed since the last fetch: one delta
   GET of the player's node (`orderBy="t"&startAt=<last t>`), and one of the alliance node if its
   counter moved. The client runs the auto-claim and the lazy purge (§2).
3. Opening the screen shows the local cache at once (≤ 300 ms, [ui.md](ui.md) §11). A delta fetch
   runs only if the head moved after step 2.
4. Offline: the cache is readable. Claim, send and delete are disabled with the words "Needs a
   connection". Nothing is queued to be sent later, so an offline tap can never grant or lose
   anything.
5. A new phone or reinstall downloads the node once (the resync line in the cost model).

## 7. Letters — who may write, and the limits

One contact setting covers whispers and letters (chat-forge channels.md §6): **everyone (adults
only) / alliance and Circle mates and contacts (default) / nobody**. A contact is a player whose
letter or whisper you accepted, or to whom you wrote first.

| Rule | PROPOSAL | Why |
|---|---|---|
| Length | ≤ 500 characters, ≤ 1,500 bytes UTF-8, ≤ 6 line breaks; ≤ 1 share card (chat-forge format, ≤ 256 B) | cost ([backend-cost.md](backend-cost.md) §7) and a letter is not an essay |
| Links | none, in any letter, for any account; URL and handle patterns are filtered | chat-forge rule; sellers |
| Stranger letter | goes to Requests, text hidden until Accept; Ignore and Block are 1 tap each | a seller's first line never lands unread |
| New recipients per day | trust T0: alliance mates only · T1: 3 (as requests) · T2+: 10 (chat-forge safety.md §5: T0 = < 48 h or S < 2) | caps cold contact; alt farms |
| Letters per day | ≤ 30; ≤ 5 per 10 min | caps flooding |
| Duplicate text | the same normalized text to ≥ 3 non-alliance recipients in 24 h → further copies held; the sender sees "Waiting for review" and gets a statement of reasons (§7 rule 2) | gold-seller pattern |
| Under the age of digital consent (13–16 by country) | no free-text letters, sent or received; share cards and alliance templates only | chat-forge safety.md §10 (COPPA, GDPR Art. 8) |
| Minor above it (to 17) | letters only with alliance and Circle mates, strict filter locked; never requestable by strangers; no push preview | chat-forge safety.md §10 |
| Diplomacy | a Liege or Marshal may write to another alliance's Liege and officers without Requests; ≤ 10 such letters per day | pacts (alliance.md §12) need a formal channel |
| Blocks | one block list with chat; a blocked sender's letters are dropped by the server without telling the sender | chat parity; no escalation |
| Report a letter | 1 tap from the letter; a copy goes to chat-forge's evidence store (90 d) and moderation queue | one moderation pipeline |

All of this is checked **server-side in the send function**, never in the client alone. The client
only hides the Write button where the server would refuse ([backend-cost.md](backend-cost.md) §3).

1. The filter, trust tier, age band, block list and moderation queue are chat-forge's (safety.md
   §1–§10). The send function calls the same pipeline. Mail never keeps a second wordlist.
2. **Statements of reasons** (EU Digital Services Act; legal to confirm applicability): every
   restriction in chat or mail (message removed or held, mute, ban) sends the player an account
   notice by mail: what was restricted, which rule, whether it was automated, how long, and how to
   appeal (template `acct.restriction`, [templates.md](templates.md) §2.1).

## 8. Alliance mail

| Rule | Number | Source |
|---|---|---|
| Who sends alliance-wide mail | Liege, and the officer holding the Herald office | alliance.md §2 action 13 |
| How many | ≤ 3 alliance-wide mails per alliance per day | alliance.md §13 |
| Body | ≤ 1,000 characters of text, or an officer template with typed args ([templates.md](templates.md) §2.3) | cost; templates read in each member's language |
| Who reads | members; the database serves only mail sent after the reader joined (query rule, [attachments.md](attachments.md) §4) | a new member cannot read old war plans |
| Young members | under the age of digital consent: officer text shown with the strict filter and contact masking; templates in full | chat-forge safety.md §10 (Hall parity) |
| Scheduled | a scheduled announcement may also send as mail (alliance.md §9); it counts in the 3 | leader burnout tools |

Alliance **system** mail to one member, per alliance.md §13: released member (reason and rejoin
rule), promotion or office change, Liege absent day 5 (officers), day 7 and day 10 (all), pact
proposed (officers), signed and notice (all), auto-release warning at N − 3 days, banner fading
(Steward and Liege). Each is a template ([templates.md](templates.md) §2.2), written by the server,
never typed.

## 9. Reports — mail delivers, report-forge writes

1. **One write, both halves.** The report writer stores the report body (report-forge storage) and a
   row in every participant's node in ONE multi-path update. There is never a row without a body,
   and never a body that nobody can reach.
2. **Row format** (about 90 bytes): `k:"r"`, `t`, `rid` (report id), `rk` kind (battle, defence,
   scout, rally, hunt, gathering), `o` outcome (−1/0/+1), `pe` peer name snapshot ≤ 16 characters.
   Everything else is fetched from report-forge when the row opens.
3. **Batching for PvE**: ≤ 1 row per hunt order (up to 5 camps), and 1 "gathering ledger" row per day
   updated in place. One row per camp or per gathering return is the genre's inbox flood.
4. **Cap**: the newest 100 rows plus Kept ones. Older reports stay reachable in report-forge's
   archive while their bodies live.
5. **No HUD badge and no push** for reports. Urgency ("under attack") belongs to battle-forge's
   watchtower alerts. The tab shows its own unread count.
6. Share a report → chat-forge share card (≤ 256 B) in chat or in a letter.

## 10. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](../../design-forge/references/benchmark.md)) | Our fix | Number |
|---|---|---|
| Rewards vanish at an expiry the player never saw | auto-claim at the next open after 30 d; hard purge only after 90 d with no session | 0 lost for any player who returns within 90 d |
| Inbox used to push offers; red-dot fatigue ([observational] in the research) | no offers in mail; badge only for rewards and people; notices never badge | ≤ 1 HUD badge from mail |
| One report per barbarian camp floods the inbox | 1 row per hunt order; 1 gathering ledger per day | ≤ 15 rows per day at stress |
| Officers write times in their own time zone; members misread them | officer templates carry unix time; every reader sees local time | 0 typed times in templates |
| Alliance-wide text only in the officer's language | templates render in each member's language | all shipped locales |
| Delete-all wipes unclaimed rewards | the database refuses the delete | 0 by construction |
| Strangers and sellers spam letters | Requests with hidden text; trust tiers; duplicate-text hold | T1: 3 new recipients per day |

## 11. Failure modes

| Fails when | Caught by |
|---|---|
| A reward disappears unclaimed for a player who returned within 90 d | [ ] mail_apply_test auto-claim case; liveops `LIVEOPS CLOCK OK` run |
| A notice, report or request raises the HUD badge | [ ] mail_badge_probe: 0 badge from `n`, `r`, requests |
| More than 1 mail push per day by default, or any push in quiet hours | [ ] mail_push_probe with a fake clock |
| Any delete of an unclaimed reward succeeds | [ ] mail_rules_test delete cases |
| A new alliance member reads mail sent before joining | [ ] mail_rules_test query-rule case |
| A dormant account's node keeps growing | [ ] cold-sweep dry run: 0 nodes for accounts > 90 d without a session |
| An offer, price or shop link appears in any template or header | [ ] template validator + shop-forge offer grep over mail templates |
| A report row exists without its body, or the reverse | [ ] report writer test: one multi-path update, both halves |

## 12. Checklist — adding a mail type or a category

- [ ] Tab and `k` code chosen from §1; a new tab needs owner approval (5 tabs is the cap).
- [ ] Lifetime row filled (§2): unread, after read, `x`, cap, and the auto-claim rule if it carries goods.
- [ ] Badge and push decided (§4, §5): default is no badge and no push.
- [ ] Template card written ([templates.md](templates.md) §1), keys sent to l10n-forge.
- [ ] Sender path decided: send job, send function or report writer; cost line added to
      `tools/mail_cost.py` and re-run ([backend-cost.md](backend-cost.md) §12).
- [ ] If it carries goods: value class I or P, the attachments validator passes, and
      `claim_sim.py` still prints `CLAIM SIM OK` ([attachments.md](attachments.md) §11).
- [ ] Diegetic name sent to story-forge.
