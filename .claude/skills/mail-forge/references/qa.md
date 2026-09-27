# QA — the harness battery for mail

Nothing about mail is "done" without pasted verdict lines (game-director hard rule 3). qa-forge
writes the probes. cloud-forge writes the backend tests beside its functions (paths to confirm).
This file names each harness, its cases, and the exact line it must print. Verdict lines, not exit
codes, are the evidence. Every probe has a **check floor**: it prints FAIL if it ran fewer checks
than its floor (lesson QA-06 in the qa-forge brief: 16 suites once "passed" after running zero
checks).

## 1. The battery

| # | Harness | Kind | Owner | Proves | Verdict line (PROPOSED wording; qa-forge fixes it) |
|---|---|---|---|---|---|
| 1 | `tools/claim_sim.py` | design model (Python) | mail-forge | exactly-once, no late grant, exact wallet; 4 broken designs caught | `CLAIM SIM OK - 2000 seeds x 2 policies, <n> claims, 0 violations` · `CONTROLS OK - 4/4 broken designs caught` |
| 2 | `tools/mail_cost.py --selftest` | design model | mail-forge | envelope, round-trip budgets, every trap visibly expensive | `MAIL COST SELFTEST OK - 19 checks` |
| 3 | `tests/test_tools.py` | both of the above | mail-forge | tools run and agree with hand arithmetic | `MAIL-FORGE TOOLS OK - 6 checks` |
| 4 | `mail_rules_test` | Firebase emulator | cloud-forge (extends `check_rules.ps1`) | the rules in [attachments.md](attachments.md) §4, 28 cases (§2) | `MAIL RULES OK - 28 cases, 0 unexpected` |
| 5 | `mail_claim_test` | emulator + functions | cloud-forge | races, faults, boundary, claim-all, the null-first trap (§3) | `MAIL CLAIM OK - 1000 races, 0 duplicate grants, 0 late grants, 0 lost grants, 0 false NOT_FOUND` |
| 6 | `mail_job_test` | emulator | cloud-forge | send-once under crashes and double starts (§4) | `MAIL JOB OK - 5000 recipients, 3 crashes, 1 double start, 0 duplicates, 0 missing, 0 claims erased` |
| 7 | `mail_spam_test` | emulator + functions | cloud-forge | letter limits, trust tiers, age bands, blocks, alliance caps (§4) | `MAIL SPAM OK - 24 cases` |
| 8 | `mail_push_probe` | fake clock | cloud-forge | push rules, quiet hours, coalescing, budget | `MAIL PUSH OK - 7 days, <n> pushes, 0 in quiet hours, max 1/day` |
| 9 | `mail_apply_test` | Godot headless | qa-forge | the client applier (§5) | `MAIL APPLY OK - 9 cases` |
| 10 | `mail_badge_probe` | Godot headless | qa-forge | the badge formula ([categories.md](categories.md) §4) | `MAIL BADGE OK - 14 fixtures` |
| 11 | `mail_l10n_probe` | Godot headless | qa-forge + l10n-forge | every template × every locale × pseudo +40% × 2 time zones | `MAIL L10N OK - <t> templates x <l> locales, 0 raw keys, 0 overflow` |
| 12 | `mail_ui` cases in `ux_flow_probe` / `ux_touch_probe` / `a11y_audit` / `layout_audit` / `w1f_aspect_sweep` / `contrast_test` / `menu_test` | windowed and headless (existing) | qa-forge | [ui.md](ui.md) §12 | existing lines, e.g. `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| 13 | mail line in `core/sd_cost_probe.gd` | measured | qa-forge + cloud-forge | round trips, bytes per path, calls, stored KB per account | `MAIL COST OK - <x> KB/DAU/day, <r> trips, EUR <e> at 50k (line EUR 30)` |
| 14 | liveops lines: `LIVEOPS CLOCK OK`, `MERGE DRYRUN OK` | staging | cloud-forge | reward mail fires once per event end; a realm merge loses 0 letters | the liveops.md §11 lines |

The emulator runs through the Firebase CLI: `firebase emulators:exec --only database,functions
"<test command>"` in cloud-forge's functions folder (path to confirm). The rules file is the one
deployed, never a copy.

## 2. `mail_rules_test` — 28 cases (the rules must refuse or allow exactly these)

| # | Case | Expect |
|---|---|---|
| 1–2 | owner reads own node; another player reads it | allow; deny |
| 3–6 | client creates a letter; edits `at`; edits `x`; removes `rv` | deny ×4 |
| 7 | claim Class I, `now < x`, not revoked | allow |
| 8 | claim with `x` 1 s in the past | deny |
| 9 | the same claim a second time | deny |
| 10 | claim writing a number for `t` instead of the server timestamp | deny |
| 11 | claim with an extra field in `c` | deny |
| 12 | client claims a Class P letter | deny |
| 13 | claim a revoked letter | deny |
| 14 | claim a letter in another player's node | deny |
| 15 | multi-path claim of 5 letters, one already claimed | deny; **none of the 5 written** |
| 16–18 | delete an unclaimed reward; delete a claimed reward; delete a notice | deny; allow; allow |
| 19–20 | set `kp` on a letter; set `kp` on a reward | allow; deny |
| 21–22 | write the head; write the wallet | deny; deny |
| 23 | member queries alliance mail ordered by `t` from their join time | allow |
| 24 | member queries from before the join time | deny |
| 25 | member reads the alliance node without a query | deny |
| 26 | non-member queries alliance mail | deny |
| 27 | delta query `orderBy="t"` on the player's node | allow (index present) |
| 28 | query ordered by an unindexed child | refused with "Index not defined" (REST 400) |

## 3. `mail_claim_test` — the backend proof of the protocol

1. **Races**: 1,000 rounds; each round creates 3 Class I and 1 Class P letter, then fires 2 "devices"
   × double tap (PATCH for I, callable for P) with random delays of 0–200 ms. Assert: exactly one `c`
   per letter; the wallet grows by exactly the P letters' gems.
2. **Fault injection**: a test-only flag makes the function throw right after the gate commits.
   The client call is retried. Assert the wallet is exact (the resume path).
3. **Boundary**: letters with `x = now + 1,500 ms`; claims fired from 1,000 to 2,000 ms. Assert every
   accepted claim has `c.t < x` and every later one is refused.
4. **Claim-all partial**: 10 ids, 2 already claimed. Assert the PATCH is refused as a whole, the
   client re-reads, sends the 8 once, and the summary says "Claimed from 8 letters · 2 already
   claimed".
5. **Null-first trap**: a cold function instance claims an existing Class P letter 100 times. Assert
   0 answers of NOT_FOUND.
6. **Revoke race**: revoke jobs run while claims fire. Assert no letter ends with `rv` and a `c`
   dated after `rv`.

## 4. `mail_job_test` and `mail_spam_test`

**Send job** (5,000 fake recipients): kill the runner at 3 random chunks and restart it; start a
second runner during the run; pre-claim 100 letters mid-job; then assert exactly one letter per
recipient, 0 erased `c`, the cursor at the end, status `done`, head counters ≥ the letter count
(counters are hints and may over-count after a lease takeover). Value-cap case: a letter above the
cap without the owner's second key is refused before any write.

**Spam and safety** (24 cases): T0 sender to a stranger → refused; T1 4th new recipient in a day →
refused; 31st letter in a day → refused; 6th letter in 10 min → refused; duplicate text to a 4th
stranger → held with "Waiting for review" and an `acct_restriction` letter; a link or handle →
filtered by chat-forge's pipeline; a sender under the age of digital consent → free text refused;
a minor to a stranger → refused; a blocked sender → dropped silently; the recipient setting
"alliance only" → refused with the reason; a Knight sends alliance-wide mail → refused; a 4th
alliance-wide mail in a day → refused; an officer template with a bad coordinate → refused; a
diplomacy letter from a Liege → delivered outside Requests; the 11th diplomacy letter → refused;
and the remaining cases cover a text of 501 characters, 1,501 bytes, 7 line breaks, 2 share cards,
an unknown share-card type, an empty text, a letter to self, a letter to a deleted account and a
letter while muted.

## 5. Client probes (Godot 4, headless)

**`mail_apply_test`** — fixtures of letters with `c`, a fake save:

| # | Case | Expect |
|---|---|---|
| 1 | apply 3 claimed letters | goods once each; keys in the same revision |
| 2 | apply again | no change |
| 3 | "crash" after the local write, restart | no change |
| 4 | "crash" before the local write, restart | applied once |
| 5 | a newer cloud save arrives (from device B, with the goods) | adopt it, re-derive, no change |
| 6 | a newer cloud save WITHOUT the goods arrives (stale device won) | re-derive adds them once |
| 7 | a backup restore rolls the save back 3 days | every claim inside the horizon re-derived once |
| 8 | a claim record older than `H` = 100 d | ignored; its key pruned |
| 9 | the conflict handler is asked to merge | it keeps one revision and re-derives; it never adds deltas |

**`mail_badge_probe`** — 14 fixtures: rewards only; letters from known senders at 71 h and 73 h;
a stranger's request; notices; an account notice; reports; alliance mail; kept letters; 150
claimables ("99+"); a claim-all clears the reward part; an auto-claim at day 30; a device-local
read; and an empty inbox.

**`mail_l10n_probe`** — renders every template card with fixture args in every shipped locale and
the pseudo-locale (+40%). It checks: 0 raw keys, 0 leftover placeholders, subject within 2 lines at
60 px in the letter view, tab labels fit or fall back to icons, and officer templates render the
reader's local time for two device time zones (UTC−5 and UTC+9).

**`mail_ui`** (windowed, added to the existing probes): paths `mail_claim_all` (2 taps) and
`mail_read` (2 taps); the 132/144 px targets; seal shape + weight for `a11y_audit`; 20 BBCode
injection strings in letters stay literal; first rows ≤ 300 ms from cache; a double tap during Busy
sends one request.

## 6. Cost measurement

1. The mail line in `sd_cost_probe.gd` runs the base and stress session scripts. It counts: round
   trips (≤ 6 base, ≤ 10 stress per DAU per day), new TLS connections opened by mail (0),
   bytes per path, function calls per Class I claim (0), and stored KB per active account.
2. It writes `measured.json` in the shape `tools/mail_cost.py --model` reads. Then
   `python tools/mail_cost.py --model measured.json` gives the measured € line. Assumed and
   measured values must agree within ±20% per line, or [backend-cost.md](backend-cost.md) §5 is
   updated with the measured value and a lesson is written.
3. Monthly: the cold-sweep report (accounts swept, GB freed, dormant nodes left = 0).

## 7. The mail gate (run for any change to mail)

| Change touches | Must be green |
|---|---|
| anything | #3 `MAIL-FORGE TOOLS OK`; the core gate (game-director) |
| claims, attachments, send jobs | #1, #4, #5, #6, #9 |
| letters, alliance mail, safety | #7, #8 |
| templates, strings, headers | #11 and the validator's unit tests |
| screens, badges, toasts | #10, #12 |
| any network path | #13 and `mail_cost.py` re-run |

Paste the verdict lines into the ledger row (game-director cycle step 8). A red line is fixed, or
the change is restored from its checkpoint. It is never shipped red.
