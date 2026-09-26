# Backend shape and cost — the inbox for 50,000 players inside €200 a month

The owner's ruling: server + database ≤ **€200/month at 50,000 players**, measured with
`core/sd_cost_probe.gd` (game-director hard rule 1, lesson 7). This file is the arithmetic for
mail. Every input is an **assumption stated as a range** until the probe measures it. Every price
is **to verify** on the provider's page on the day of the decision. The numbers reproduce with
`python tools/mail_cost.py` (and `--trap all`, `--json`, `--selftest`).

## 1. The stack and the unit of cost

The studio's cloud-forge brief records the backend: **Firebase Realtime Database on the Blaze plan**
(pay as you go, **no spending cap**) + **one Cloud Function** + `godot/core/cloud.gd` with push beats,
`print=silent` writes, pointer-first boards and "mail/chat throttles" (paths to confirm). The brief
also says **RTDB bills downloads and storage, not operations**. That decides the whole design:

1. **The unit is the round trip, not the record.** Every REST response carries headers (≈ 0.35–0.5 KB
   billed), and every NEW TLS connection costs ≈ 3.5 KB of billed download (Firebase billing
   documentation). A 50-byte head costs 10× its size in overhead on a warm connection and 80× on a
   cold one.
2. **Writes are free, reads are not.** Uploads are not billed, so fan-out WRITES are cheap (counters,
   rewards to 50,000 players). Every byte a client or a function READS is billed.
3. **Stored bytes cost $5/GB-month** — about 200× object storage. Short keys, compact rows and
   retention are money.

## 2. Prices (USD list prices; seen 2026-09-26 in search results — verify before deciding)

| Item | Price | Status | Source |
|---|---|---|---|
| RTDB download | $1 per GB | two search results agree | firebase.google.com/pricing (via airbyte.com and back4app.com pages) |
| RTDB storage | $5 per GB-month | two results agree | same |
| RTDB free usage on Blaze | 1 GB stored + 10 GB/month downloaded | shared by the whole game → **not credited to mail** | same |
| TLS handshake | ≈ 3.5 KB per new connection, + tens of bytes per record | Firebase billing doc text | firebase.google.com/docs/database/usage/billing |
| Cloud Run functions requests | $0.40 per million after 2 M free/month | search snippet | cloud.google.com/functions/pricing-overview |
| Functions compute | $0.000024 per vCPU-s, $0.0000025 per GiB-s after 180,000 vCPU-s and 360,000 GiB-s free | free tier seen; **rates not seen — verify** | cloud.google.com/run/pricing |
| Function internet egress | $0.12 per GB | **not seen — verify** | cloud.google.com/run/pricing |
| Push (FCM) | $0 per message | several results agree | firebase.google.com/pricing |
| Firestore (only for comparisons) | reads $0.03, writes $0.09, deletes $0.01 per 100,000; 50k/20k/20k free per day | **sources disagree ($0.03 vs $0.06 reads) — verify** | cloud.google.com/firestore/pricing |
| FX | €1 = $ × 0.85–0.95 | the range chat-forge uses | — |

Free tiers are shared by every system in the game, so mail is priced at the marginal rate. The
real bill for mail is lower until the free usage is spent elsewhere.

## 3. Data layout (PROPOSAL — cloud-forge owns the final paths)

| Path | What | Bytes (JSON, short keys) | Written by | Read by |
|---|---|---|---|---|
| `/mail/h/{uid}` → rides inside the node cloud.gd already reads at resume | head: arrival counters `w l n r a` | ≈ 50 | send jobs, send function, report writer (`ServerValue.increment`) | the owner, with the resume read |
| `/mail/p/{uid}/{id}` | every letter to one player: rewards, notices, alliance-to-you, letters, report rows | reward 250–300 · notice 300–400 · letter 180–220 + body ≤ 1,500 · report row 80–100 | send jobs, send function, report writer; client writes only `c` (Class I), `kp`, deletes | the owner, delta by `t` |
| `/mail/a/{aid}/{id}` | alliance-wide mail, once per alliance | 250–300 + text ≤ 3,000 (1,000 chars) | send function | members, query from their join time |
| `/srv/{uid}/wallet` | premium balance + applied ids | ≈ 1,000 | claim function | the owner |
| `/mail/rl/{uid}`, `/mail/ct/{uid}` | sender rate state, contacts | ≈ 100 + 30 per contact | send function | send function |
| `/mail/jobs/{job}` | send-job lease, cursor, status | ≈ 200 | send job | send job |

Rules of the layout:

1. **One node per player** holds everything addressed to that player. One delta GET per fetch, one
   rules block, one lazy purge.
2. **Fan out a counter, store content once** when nobody needs per-reader state: alliance-wide mail
   (100 members × 1.2 KB × 30 d per mail would be +USD 10.8/month at stress, trap `fanout`).
3. **Fan out content** only when each reader needs their own state (a reward's claim record) or when
   the copies are small and short-lived (notices: 0.4 KB, 3–14 d, active accounts only).
4. **Report bodies are report-forge's** (storage.md there). Mail stores the ~90-byte row only.

## 4. The round-trip budget

| When | Mail round trips | Why |
|---|---|---|
| Every resume | **0** — the head rides the read cloud.gd already makes | trap `ownhead` = +USD 6/month at stress |
| First session of the day, or head changed | 1 personal delta GET + 1 alliance delta GET if its counter moved | badge, auto-claim, lazy purge |
| Open the Letters screen | 0 if nothing changed since the last fetch | the cache shows at once |
| Claim or claim-all (items) | 1 PATCH, `print=silent` | the rules gate |
| Premium claim, letter, alliance mail | 1 function call each | server checks |
| Purge | 1 batched delete per day | lazy, no server tick |
| **Never** | a polling timer; a new connection per call; a GET without `.indexOn`; a write without `print=silent` | §9 traps |

Budget: **≤ 6 round trips per DAU per day at base, ≤ 10 at stress** (the tool's selftest enforces it).
All mail calls use cloud.gd's open HTTP connection (one `HTTPClient` kept alive). A fresh
`HTTPRequest` per call opens a new TLS connection, and that is the `cold` trap. Confirm in the
shipped Godot version whether `HTTPRequest` reuses connections before relying on it.

## 5. Assumptions (ranges; per DAU per day unless named)

Scenarios match chat-forge's: players `P` = 50,000; DAU = 40% / 60% / 100% of `P`.

| Input | Base | High | Stress | Why this range |
|---|---|---|---|---|
| DAU | 20,000 | 30,000 | 50,000 | stress = every player daily (the budget's worst reading) |
| Sessions | 6 | 7 | 8 | numbers.md §8: 4–8 for engaged players |
| Screen opens | 1.5 | 2.0 | 2.5 | core-loop check-in step 10 (chests, gifts) + letters |
| P(personal delta needed) / P(alliance delta) | 0.9 / 0.5 | 0.9 / 0.6 | 0.95 / 0.7 | head-gated fetches |
| Claim calls (claim-all batches) | 1.2 | 1.5 | 2.0 | rewards arrive in bursts (event ends, chronicle) |
| Response overhead per round trip | 0.35 KB | 0.40 KB | 0.50 KB | HTTP/1.1 headers + TLS records; **measure** |
| Rewards letters received / size | 1.5 / 0.25 KB | 2.0 / 0.28 | 2.5 / 0.30 | liveops milestones, chronicle, compensation |
| Notices / size | 0.5 / 0.30 KB | 0.7 / 0.35 | 1.0 / 0.40 | ≤ 1 notice a day is already a lot |
| Alliance mails seen / free-text share / text size | 0.5 / 50% / 0.6 KB | 0.8 / 50% / 0.9 | 1.2 / 60% / 1.5 | alliance.md cap is 3 a day per alliance |
| Letters received / header / body | 0.5 / 0.18 / 0.35 KB | 0.8 / 0.20 / 0.50 | 1.2 / 0.22 / 0.75 | cap 500 characters; 0.75 KB ≈ 250 CJK characters |
| Report rows / size | 8 / 0.08 KB | 12 / 0.09 | 15 / 0.10 | PvE batched to 1 row per hunt order |
| Sends (letters + alliance) / function read per send | 0.3 / 0.5 KB | 0.5 / 0.6 | 0.8 / 0.8 | rate state, contacts, blocks, roster |
| Premium claims / wallet read | 0.03 / 1.0 KB | 0.05 / 1.0 | 0.10 / 1.2 | compensation with gems is rare |
| Resync share (new phone, reinstall) | 0.5% | 0.75% | 1% | the cache in user:// survives updates |
| Held days: rewards / notices / letters / reports | 5 / 4 / 10 / 10 | 6 / 5 / 11 / 12 | 6 / 6 / 12 / 14 | categories.md §2 retention, averaged |
| Kept letters (cap 40) | 3 | 6 | 10 | — |
| Accounts with mail but not daily / their KB | 60,000 / 1.5 | 80,000 / 1.8 | 100,000 / 2.0 | cold sweep at 90 d bounds it |
| Function billed time / vCPU / memory | 0.3 s / 0.167 / 0.25 GiB | same | 0.4 s | `gcf_gen1` class at 256 MiB |

## 6. The formulas

```
round trips/day  R = S·(1 − piggyback) + O·(p_personal + p_alliance) + C + 1
downloads KB/day D = R·ov + S·head + rewards·size + notices·size + letters·(hdr + body)
                   + alliance·(hdr + share·text) + rows·size + sends·f_send + premium·f_wallet
                   + resync·held_items·0.3
storage KB/active A = rewards·days·(size + 0.03) + notices·days·size + letters·days·(hdr + body)
                   + kept·(hdr + body) + min(rows·days, 100)·size + 0.25
GB/month: downloads = DAU·D·30/10^6 · storage = (DAU·A + inactive·kb + alliances·alliance·30·size)/10^6
functions $ = inv/10^6·0.40 + inv·t·vCPU·0.000024 + inv·t·GiB·0.0000025,  inv = DAU·(sends + premium)·30
```

## 7. Worked arithmetic — stress (50,000 DAU, every input at its high end)

Round trips: 8 × (1 − 1) + 2.5 × (0.95 + 0.7) + 2.0 + 1 = **7.1 per DAU per day**.

| Download line (per DAU per day) | Arithmetic | KB |
|---|---|---|
| Round-trip overhead | 7.125 × 0.50 | 3.56 |
| Head payload (rides the resume read) | 8 × 0.06 | 0.48 |
| Rewards letters | 2.5 × 0.30 | 0.75 |
| Notices | 1.0 × 0.40 | 0.40 |
| Letters | 1.2 × (0.22 + 0.75) | 1.16 |
| Alliance mail | 1.2 × (0.30 + 0.6 × 1.5) | 1.44 |
| Report rows | 15 × 0.10 | 1.50 |
| Function reads: sends / premium | 0.8 × 0.8 / 0.10 × 1.2 | 0.64 / 0.12 |
| Resync | 0.01 × 135 held × 0.3 | 0.41 |
| **Total** | | **10.46** |

- Downloads: 10.46 KB × 50,000 × 30 = **15.69 GB → $15.69**
- Storage per active account: 4.95 (rewards) + 2.40 (notices) + 13.97 (letters) + 9.70 (kept)
  + 10.00 (100 report rows) + 0.25 (head) = **41.27 KB** × 50,000 = 2.06 GB; + 100,000 × 2.0 KB =
  0.20 GB; + alliances 2,500 × 1.2 × 30 × 1.2 KB = 0.11 GB → **2.37 GB × $5 = $11.86**
- Functions: 50,000 × (0.8 + 0.1) × 30 = **1.35 M calls** → $0.54 requests + 1.35 M × 0.4 s × 0.167 ×
  $0.000024 = $2.16 vCPU + $0.34 memory = **$3.04**; egress 1.35 M × 1.2 KB = 1.62 GB → **$0.19**
- Push: **$0**
- **Total $30.79 → €26.2–29.2** (FX 0.85–0.95)

| Scenario | DAU | Trips/day | KB/DAU/day | Download GB | Stored GB | Calls/month | USD | **EUR** |
|---|---|---|---|---|---|---|---|---|
| base | 20,000 | 4.3 | 3.83 | 2.30 | 0.37 | 0.20 M | 4.52 | **3.8–4.3** |
| high | 30,000 | 5.5 | 6.21 | 5.59 | 0.91 | 0.50 M | 11.07 | **9.4–10.5** |
| stress | 50,000 | 7.1 | 10.46 | 15.69 | 2.37 | 1.35 M | 30.79 | **26.2–29.2** |

## 8. Against the budget

| Line (chat-forge backend-cost.md §7.8, PROPOSAL) | € / month at stress, high prices |
|---|---|
| Game server + DB (measured, game-director lesson 7) | ≈ 20 |
| Chat envelope | ≤ 50 |
| **Mail (this file)** | **≤ 30** (computed 29.2); base ≤ 10 (computed 4.3) |
| Report storage | report-forge storage.md |
| Headroom | ≈ 100 minus reports |

Mail's line is a **proposal to the owner**. Stress fits it with €0.8 to spare, and that margin is thin
on purpose: the probe replaces these assumptions, and lever M2 (§10) removes almost the whole bill.

## 9. Traps (priced at stress with the tool; `--trap all`)

| Trap | What someone does | Extra per month | Total |
|---|---|---|---|
| `leak` | notices fanned out to 200,000 dormant accounts for a year, no cold sweep | **+$146.00** | €150–168 |
| `poll` | a 60 s head poll while the app is open (60 min a day) | **+$50.40** | €69–77 |
| `cold` | a new TLS connection per mail call (fresh HTTPRequest each time) | **+$37.41** | €58–65 |
| `fanout` | alliance mail copied into every member's node | +$10.80 | €35–40 |
| `fnclaim` | every item claim goes through the function instead of the rules gate | +$7.64 | €33–37 |
| `ownhead` | the head as its own GET per session | +$6.00 | €31–35 |

The first three alone would each break the whole €200 plan together with chat. Game-director
lesson 7 records the same shape: one read-path bug cost more than everything else combined.

## 10. Levers, ranked by saving at stress

| # | Lever | Saves | Cost to the player |
|---|---|---|---|
| M2 | **Mail rows on chat-forge's Postgres box** (if that box ships): storage €0.04–0.12/GB, egress inside the box's included TB; claim gate = a unique `(uid, id)` row inserted with `ON CONFLICT DO NOTHING`, same applier | the tool prints €0.13–0.45 marginal at stress, vs €26–29 | mail shares the box's uptime (the cache hides short outages); cloud-forge builds a second server path |
| L5 | Function billed time 0.4 → 0.2 s (warm instance, fewer reads) | $1.25 | none |
| L1 | Letter read-retention 7 → 3 d | $1.19 | read letters vanish sooner (Keep exists) |
| L2 | Letter cap 500 → 400 characters | $1.18 | shorter letters |
| L3 | Report rows cap 100 → 60 | $1.18 | older reports only via report-forge's archive |
| L4 | Kept cap 40 → 25 (average kept 10 → 6) | $0.97 | the Guild Patronage perk shrinks with it (monetization.md) |
| L1–L5 together | | $5.44 → €21.5–24.1 at stress | all of the above |

Savings are `mail_cost.py` sweeps against stress on 2026-09-26; apply one with `--model`.
Without M2, the €200 plan can hold mail below about €22 only by making mail worse for players.
M2 is the structural lever.

## 11. Measuring

1. **sd_cost_probe mail line** (qa-forge adds it): per scripted session, count mail round trips, bytes
   down per path, function calls, and stored KB per account. Verdict (wording fixed by qa-forge):
   `MAIL COST OK - <x> KB/DAU/day, <r> trips, EUR <e> at 50k (line EUR 30)`.
2. **Put measured values into the tool**: `python tools/mail_cost.py --model measured.json`, e.g.
   `{"stress": {"ov_kb": 0.43, "report_rows": 11}}`. The measured run replaces §7 in the next review.
3. **RTDB profiler**: `firebase database:profile` for 5 minutes at peak shows bytes per path. The
   `/mail/` paths must match the probe within ±20%.
4. **Budget alerts** (Blaze has no cap): cloud-forge sets Google Cloud budget alerts at €50 / €100 /
   €150 / €200. Mail's function has `maxInstances: 5`. A remote switch can pause letters (not rewards)
   if a spam wave or bug pushes costs.
5. **Monthly**: the cold sweep report (accounts swept, GB freed). Stored GB per active account must
   be ≤ 45 KB at stress.

## 12. Failure modes and checklist

| Fails when | Caught by |
|---|---|
| Mail trips per DAU per day > 10, or any timer-driven mail read | [ ] sd_cost_probe mail line; grep for Timer nodes in the mail UI code |
| A mail call opens its own TLS connection | [ ] sd_cost_probe connection count per session = cloud.gd's count |
| A write returns a body (no `print=silent`) | [ ] probe: bytes down on writes ≈ headers only |
| A query without `.indexOn` (REST refuses with 400; an SDK would download the whole node) | [ ] mail_rules_test query cases |
| Stored KB per active account > 45 at stress, or dormant nodes > 90 d exist | [ ] monthly cold-sweep report |
| Measured € above the line | [ ] `mail_cost.py --model measured.json`; apply §10 levers or M2 |

Before any new mail path ships:

- [ ] Its round trips and bytes are a line in `tools/mail_cost.py`; `--selftest` still passes.
- [ ] It reuses cloud.gd's connection, writes with `print=silent`, queries an indexed child.
- [ ] Content stored once unless per-reader state is needed (§3 rules 2–3).
- [ ] Retention and cap written in [categories.md](categories.md) §2; the cold sweep covers it.
- [ ] sd_cost_probe line updated; the € result pasted into the ledger row (game-director).
