# Backend shape and cost — 50,000 players inside €200 per month

chat-forge specifies; **cloud-forge** builds and runs it. The owner's binding ruling: server +
database ≤ **€200/month at 50,000 players**, measured with `core/sd_cost_probe.gd` (game-director
lesson 7: the game itself measured ≈ €20 worst case; one read-path bug once cost ≈ €145/month at
100k). Every input below is an **assumption until measured**; every price is a range to
**verify** (§7.7). The arithmetic is reproducible: `python tools/chat_cost.py` prints every table
in §7 (`--selftest` prints `CHAT COST SELFTEST OK - 14 checks`).

## 0. Isolation rules (non-negotiable)

1. **Chat never shares a process or a database with saves, economy or the map.** A chat flood must
   not slow a save; a chat outage must not stop a march. No game action waits for chat.
2. **No per-delivery billing for fan-out.** Realm and alliance fan-out never runs on a service that
   bills each delivered message or each listener read (§7.4: those fail at the BASE scenario).
3. **The game backend is the authority for membership** (realm, alliance, rank, age band, trust
   tier). Chat receives them as claims in a short-lived token and as membership events.

## 1. Shape

```
 phone (Godot 4)                     chat box (one VPS)                     game backend (cloud-forge)
 ChatClient ── wss ──►  gateway: sockets, subscriptions, token buckets,  ◄── token issue (JWT ≤ 15 min)
   WebSocketPeer           filter pipeline, ring buffer (200/channel)     ◄── membership events (queue/webhook)
   local cache             │                                              ──► anti-cheat flags (sellers)
                           ▼
                        Postgres: messages (3 tables by retention, daily partitions), cursors,
                        blocks, mutes, sanctions, reports, evidence
                           │  WAL every 60 s + nightly dump ──► object storage (EU)
                        push worker ──► FCM / APNs (only when the recipient has no socket)
                        translate fallback ──► cloud MT (capped, §7.5)
```

One process can serve the stress scenario (9.4k peak sockets, 11.3k deliveries/s peak) on
4 vCPU / 8 GB **if the load test agrees** (§8). Horizontal split later: channels hashed to
gateway nodes, Postgres `LISTEN/NOTIFY` (payload ≤ 8,000 bytes) or a small pub/sub between nodes.

## 2. Transport: WebSocket in the foreground, push in the background

| Option | Base-scenario load (tool output) | Latency | Verdict |
|---|---|---|---|
| Poll every 3 s | 18.0 M requests/day, 10.8 GB/day of headers; serverless €97–€297/month | 1.5 s average | no |
| Poll every 5 s | 10.8 M/day, 6.5 GB/day; €58–€178 | 2.5 s | no |
| Poll every 15 s | 3.6 M/day, 2.2 GB/day; €19–€59 | 7.5 s — too slow for a rally call | no |
| Poll every 30 s | 1.8 M/day; €10–€30 | 15 s | no |
| **WebSocket** | 120k connects + 1.8 M ping frames/day, 0.14 GB/day | < 300 ms p50, ≤ 1 s p95 target | **yes** |
| Long-poll 25 s (fallback only) | ≈ 2.2 M requests/day if every client needed it | ≤ 1 s | only when the socket fails on a network |

Rules: socket open only while the app is in the foreground (closed on
`NOTIFICATION_APPLICATION_PAUSED`); app-level ping every 30 s, server closes sockets silent for
75 s; background delivery is push (§6), never a held socket (battery, and the OS kills it).

## 3. Wire protocol (JSON, short keys; protocol version in the hello)

| Frame | Direction | Example | Bytes |
|---|---|---|---|
| hello | C→S | `{"t":"hi","v":1,"tok":"<jwt>","lang":"pl","cur":{"a:812":90412,"w:55:77":310}}` | 300–700 |
| welcome | S→C | `{"t":"ok","me":55123,"srv":1790000000,"ch":[{"c":"a:812","h":90431,"u":19}]}` | 100–2,000 |
| page | S→C | `{"t":"pg","c":"a:812","m":[…≤ 50 messages],"gap":0,"d":[90400]}` | ≤ 15 KB |
| message | S→C | `{"t":"m","c":"a:812","q":90432,"u":55123,"n":"Aldric","g":"OAK","k":"x","x":"Rally at the ford","ts":1790000123}` | 120 + text |
| send | C→S | `{"t":"s","c":"a:812","k":"x","x":"Rally at the ford","cid":"7f3a91"}` | 50 + text |
| ack / error | S→C | `{"t":"a","cid":"7f3a91","q":90432}` · `{"t":"e","cid":"7f3a91","why":"slow","wait":18}` | 40–60 |
| read cursor | C→S | `{"t":"r","c":"a:812","q":90432}` (≤ 1 per 10 s per channel) | 35 |
| realm live on/off | C→S | `{"t":"sub","c":"r:7"}` · `{"t":"uns","c":"r:7"}` | 25 |
| tombstone | S→C | `{"t":"d","c":"a:812","q":90400}` | 35 |
| membership | S→C | `{"t":"mb","c":"a:812","op":"leave"}` | 40 |
| ping / pong | both | `{"t":"p"}` / `{"t":"P"}` | 9 + framing |

- The token travels in the first frame, never in the URL (URLs end up in logs).
- `cid` (client id) makes sends idempotent: the server remembers each sender's `cid`s for 10 min,
  so a resend after a reconnect never doubles a message.
- `q` is the per-channel sequence assigned by the server; clients order by `q`, never by clock.
- Average live frame on the wire ≈ **200 B** = ~120 B frame + ~50 B text (45 characters, mixed
  scripts) + WebSocket header 2–4 B + TLS record overhead ~29 B. The cost tool uses 200 / 250 /
  300 B for base / high / stress.

## 4. Storage (Postgres; cloud-forge may choose the engine if the costs hold)

```sql
-- one table per retention class, each partitioned by day: retention = DROP PARTITION (no vacuum debt)
CREATE TABLE chat_msg_30d (            -- Hall, Council, Whisper, Circle
  ch     text        NOT NULL,         -- 'a:812', 'w:55:77'
  seq    bigint      NOT NULL,
  ts     timestamptz NOT NULL,
  sender bigint,                       -- NULL = system
  kind   char(1)     NOT NULL,         -- x s q k n y
  body   text,                         -- <= 800 bytes
  card   jsonb,                        -- <= 256 bytes
  reply  bigint,
  flags  smallint    NOT NULL DEFAULT 0, -- 1 held, 2 removed, 4 author-deleted
  PRIMARY KEY (ch, seq, ts)
) PARTITION BY RANGE (ts);
-- chat_msg_3d (Market Cross) and chat_msg_7d (Herald): same columns
CREATE TABLE chat_channel (ch text PRIMARY KEY, head bigint NOT NULL, settings jsonb);
CREATE TABLE chat_cursor  (player bigint, ch text, seq bigint, PRIMARY KEY (player, ch));
CREATE TABLE chat_block   (player bigint, target bigint, ts timestamptz, PRIMARY KEY (player, target));
-- plus chat_mute, chat_sanction, chat_report, chat_evidence (expires), chat_circle_member
```

Row size ≈ **400–450 B** with index entries and page overhead (tuple header 23 B + columns
~150–250 B + two index entries ~80 B + ~20% free space). Jobs (nightly, UTC): create tomorrow's
partitions; drop partitions past retention (3 / 7 / 30 d); trim channels over their count guard
([channels.md](channels.md) §1); expire evidence and held items; run GDPR erasure batches
([safety.md](safety.md) §11).

## 5. Sync, offline catch-up and unread counts

1. **Hello** carries the client's cursor per cached channel.
2. **Welcome** returns, for every channel the player belongs to: head `h` and unread `u = h −
   cursor` (tombstones not subtracted — within a few messages is good enough), plus server time.
   Whisper threads appear only when `u > 0` (≤ 50 threads).
3. **Pages** follow for the open tab and the ticker channel only: ≤ 50 newest after the cursor
   (Market Cross ≤ 20), tombstones since the cursor, and `gap` = messages skipped. The client shows
   "312 older — load" for a gap; older pages are 30 messages on scroll.
4. **Ring buffer**: the gateway keeps the last 200 messages of every active channel in memory, so
   almost every catch-up is served without a database read.
5. **Cursors** are written at most once per 10 s per channel and on panel close (2 writes per
   session in the model).
6. **Reconnect**: delay = min(30 s, 1 s × 2^attempt) × random(0.8–1.2). After a server restart
   (close code 1012) the first attempt waits random(0–10 s): 9,400 stress-peak clients return at
   ≈ 940 per second, not all at once.

## 6. Push transport

FCM (Android) and APNs (iOS) through a push worker in the chat box; **no per-message fee**
(verify quotas). Rules of what may push: [channels.md](channels.md) §8. Payload: string key +
sender name; no message text unless the adult player opted in. Device tokens are refreshed at
each login; tokens rejected by FCM/APNs are deleted at once. Push counts per player per day are
kept in memory and flushed hourly (the A8 budget check).

## 7. The cost model

### 7.1 Assumptions (every one to be replaced by a measured value)

| Input | Base | High | Stress | Why this value |
|---|---|---|---|---|
| Players `P` | 50,000 | 50,000 | 50,000 | the budget definition |
| DAU share `d` | 0.40 | 0.60 | 1.00 | healthy genre games run DAU/MAU 0.3–0.5; stress = everyone daily |
| Messages sent per DAU per day `m` | 15 | 30 | 60 | most players send 0–5, alliance leaders 100+ [assumption] |
| Online minutes per DAU per day `T` | 45 | 60 | 90 | core-loop.md: 4–8 sessions × 6–12 min |
| Peak / average concurrency | 3.0 | 3.0 | 3.0 | evening and war-window peaks; every message priced as if sent at peak |
| Co-play affinity (alliance, Circle) | 2.5 | 2.5 | 1.6 | mates are online together (war windows); stress value chosen so `f` = 0.30 (30 of 100 members online at once) |
| Alliance size (average) `a` | 60 | 80 | 100 | alliance.md owns the cap; verify |
| Realm size `R` | 3,000 | 4,000 | 5,000 | world.md owns N; verify |
| Share of online realm players receiving the realm stream `s` | 0.25 | 0.50 | 1.00 | Hall is the ticker default ([channels.md](channels.md) §1 rule 2) |
| Channel mix of sent messages | Hall 55% · Market Cross 20% · Whisper 12% · Circle 5% · Council 3% · Herald 5% | same | same | [assumption; measure per channel] |
| Sessions per DAU | 6 | 7 | 8 | core-loop.md |
| Catch-up messages per session | 30 | 50 | 70 | page cap 50 (+20 realm) |
| Bytes per delivery on the wire `b` | 200 | 250 | 300 | §3 |
| Bytes per stored row | 400 | 420 | 450 | §4 |
| Retention (days) | Market Cross 3 · Herald 7 · others 30 | same | same | [channels.md](channels.md) §1 |

### 7.2 Formulas

```
DAU            = P × d
sent_c         = DAU × m × mix_c                (Market Cross capped at 20/min × 1,440 × P/R)
f_realm        = d × T / 1440 × peak            (share of a realm online at peak)
f              = f_realm × affinity             (share of an alliance/Circle online when a mate writes)
fan-out r_c    = Hall a·f · Market Cross R·f_realm·s · Whisper 1 · Circle 8·f · Council 5·f · Herald a·f
deliveries/day = Σ sent_c × r_c
egress/day     = deliveries × b  +  DAU × sessions × catch-up × b  +  DAU × T × 2 pings × 80 B
writes/day     = Σ sent_c  +  DAU × sessions × 2 cursor writes
rows stored    = Σ sent_c × retention_c ;  storage = rows × bytes_per_row
backups        = storage × 0.4 (compressed, no indexes) × 7 dumps
€/month        = box + max(0, egress − included) × overage + storage × €/GB
                 + max(backups × €/GB, store minimum) + translation cap
```

### 7.3 The base scenario by hand

- DAU = 50,000 × 0.40 = **20,000**; sent = 20,000 × 15 = **300,000 messages/day**.
- f_realm = 0.40 × 45 / 1440 × 3 = 0.0375 (1,875 peak sockets); f = 0.0375 × 2.5 = 0.094.
- Hall: 165,000 × (60 × 0.094 = 5.63) = 928,125 · Market Cross: 60,000 × (3,000 × 0.0375 × 0.25 =
  28.1) = 1,687,500 · Whisper 36,000 × 1 = 36,000 · Circle 15,000 × 0.75 = 11,250 · Council 9,000 ×
  0.47 = 4,219 · Herald 15,000 × 5.63 = 84,375 → **2.75 M deliveries/day** (95 per s at peak).
- Egress: 2.75 M × 200 B = 0.55 GB + catch-up 20,000 × 6 × 30 × 200 B = 0.72 GB + pings 900,000 ×
  2 × 80 B = 0.14 GB = **1.41 GB/day → 42 GB/month** (0.2% of a 20 TB allowance).
- Writes: 300,000 + 20,000 × 6 × 2 = **540,000/day** (6 per s).
- Rows: 165k × 30 + 60k × 3 + 36k × 30 + 15k × 30 + 9k × 30 + 15k × 7 = **7.04 M** × 400 B =
  **2.8 GB**; backups 2.8 × 0.4 × 7 = 7.9 GB.
- A1 cost: box €4–€15 + egress overage €0 + storage 2.8 × €0.04–€0.12 = €0.11–€0.34 + backups
  max(7.9 × €0.005–€0.025, minimum €0–€5) = €0.04–€5 + translation cap €0–€10 = **€4–€30/month**.
- Not in the tool: a domain name (≈ €1/month), TLS certificates (free ACME), monitoring and error
  tracking (self-hosted on the box or a free tier). A paid monitoring service needs its own line.

### 7.4 Three scenarios, five architectures (tool output, EUR per month, low–high price)

| | Base | High | Stress |
|---|---|---|---|
| Sent / day | 300 k | 900 k | 3.0 M (312 k rejected by the realm cap) |
| Deliveries / day (peak per s) | 2.75 M (95) | 35.3 M (1,230) | 325 M (11,280) |
| Egress / month | 42 GB | 352 GB | 3,197 GB |
| Writes / day | 540 k | 1.32 M | 3.49 M |
| Stored rows / storage | 7.0 M / 2.8 GB | 21.1 M / 8.9 GB | 69.4 M / 31.2 GB |
| **A1 flat-traffic VPS, one box + WAL backups** | **€4–€30** | **€4–€31** | **€10–€49** |
| A1-HA (+ hot standby box) | €8–€45 | €8–€46 | €18–€79 |
| A2 hyperscaler VM, metered egress | €15–€50 | €28–€79 | €187–€429 |
| B per-delivery realtime + managed DB | €89–€283 | €968–€2,627 | €8,786–€23,475 |
| C document DB, listeners billed as reads | €65–€156 | €404–€866 | €2,945–€6,099 |

Reading: **A1 is the only shape that holds in every scenario** inside the proposed €50 chat
envelope. B and C fail at base — they are banned for fan-out (rule 0.2). A2 fails as soon as egress
is metered at scale. A1-HA doubles the box for availability; it fits base and high, and at stress
only at low-to-mid prices (owner decision #2 in SKILL.md). Realm fan-out is 61% / 76% / 83% of all
deliveries — it is the number to watch.

### 7.5 Translation (the hidden budget killer)

| Mode (base scenario, 45 characters per message, 30% foreign) | Characters / month | € / month at €9–€23 per M chars |
|---|---|---|
| Cloud, auto-translate every foreign delivery | 1.11 B | €10,029–€25,630 |
| Cloud, auto-translate cached per message + language | 243 M | €2,187–€5,589 |
| Cloud, tap-to-translate (3 taps per DAU, no cache hits) | 81 M | €729–€1,863 |
| **On-device** (Android ML Kit / iOS Translation framework) | 0 on the server | **€0** |

Rule: translation is **on-device**; the cloud fallback is tap-only, ≤ 5 per player per day, behind
a global breaker of **€10/month** (0.43–1.1 M characters ≈ 10,000–25,000 taps per month, plus any
provider free tier — verify it allows commercial use). The breaker trips → the menu item rests
until the 1st ([ui.md](ui.md) §6).

### 7.6 Scaling past 50,000 players

Costs grow with **online players × channel rate**, not with total players: doubling to 100k
players at base doubles deliveries (5.5 M/day) and storage (5.6 GB) and still runs on one small
box. A new realm adds a realm channel, not a new server. Re-run the tool with `"players": 100000`
in `--model` before any growth decision.

### 7.7 Prices to verify (provider-specific; remembered 2025 list prices, 1 USD ≈ €0.85–€0.95)

| Line | Range used | Check at (examples, not a choice) | Must verify |
|---|---|---|---|
| VPS 2 vCPU / 4 GB | €4–€15 / month | EU budget hosts (e.g. Hetzner Cloud, OVHcloud, Scaleway, netcup) | current price, region, dedicated vs shared vCPU |
| VPS 4 vCPU / 8 GB | €8–€30 | same | same |
| Included egress | 20 TB per box, then €1–€1.2 per TB | e.g. Hetzner EU locations | the allowance differs by region (much smaller outside the EU at some hosts) |
| Block volume | €0.04–€0.12 per GB-month | host volumes | price and IOPS |
| Object storage (backups) | €0.005–€0.025 per GB-month or a monthly minimum ≈ €5 | host object storage or storage boxes | minimum fee, EU region, egress on restore |
| Hyperscaler VM + egress | €15–€35 / €30–€70; egress $0.05–$0.12 per GB after ~100 GB free | AWS, Google Cloud, Azure | egress tiers and free allowance |
| Per-message realtime | $1–$2.5 per M messages (+ connection-minutes) | e.g. AWS API Gateway WebSocket, Supabase Realtime, hosted pub/sub | only to prove the ban in rule 0.2 still holds |
| Document DB reads/writes | reads $0.03–$0.06 / 100k; writes $0.09–$0.27 / 100k | e.g. Firestore (listener updates bill as reads) | EU-region price |
| Cloud translation | $10–$25 per M characters; free tiers 0.5–2 M chars/month | Google Cloud Translation, DeepL API, Azure Translator, Amazon Translate | price, free-tier terms for commercial use, DPA |
| On-device translation | €0 | Google ML Kit Translation (≈ 30 MB per language), Apple Translation framework (iOS 18+) | terms, attribution, language list, model size |
| Push | €0 per message | FCM, APNs | quotas and rate limits |
| Serverless requests | €0.18–€0.55 per M | e.g. Cloudflare Workers, AWS Lambda | only for the polling comparison |

### 7.8 The €200 split (PROPOSAL — owner decision #1)

| Line | € / month at stress, high prices | Source |
|---|---|---|
| Game server + DB (saves, economy, map) | ≈ €20 | measured by `sd_cost_probe.gd` (game-director lesson 7) |
| **Chat envelope** | **≤ €50** (A1 stress high end €49) | this file |
| Mail | mail-forge backend-cost.md | mail-forge |
| Report storage | report-forge storage.md | report-forge |
| Headroom | €130 minus the mail and report lines | incidents, HA standby, growth |

### 7.9 Levers (ranked by what they save)

| # | Lever | Saves (tool) |
|---|---|---|
| L1 | Realm cap 20 accepted msg/min per realm (slow mode) | stress: realm deliveries 563 M → 270 M per day |
| L2 | Hall, not Market Cross, as the ticker default | base: realm deliveries 6.75 M → 1.69 M per day (s 1.0 → 0.25) |
| L3 | Ticker sampling ≤ 1 realm msg per 10 s (`{"stress":{"ticker_only_share":0.8}}`) | stress: 325 M → 174 M deliveries per day, egress 3.2 → 1.8 TB |
| L4 | On-device translation, capped cloud fallback | €729–€1,863 per month at base vs tap-to-translate cloud |
| L5 | Ring buffer for catch-up | most catch-up reads leave the database |
| L6 | Count guards on retention | bounds storage when a channel is very busy |
| L7 | Language rooms ([channels.md](channels.md) §9) | smaller realm fan-out per room |
| L8 | Frame 200 → 150 B (shorter keys, no name snapshot) | −25% egress; matters only on metered egress |

## 8. Capacity and reliability

| Item | Target |
|---|---|
| Peak sockets | 1.9k base · 3.8k high · 9.4k stress (≈ 20–50 KB each → ≤ 0.5 GB RAM) |
| Deliveries at peak | 95 / 1,230 / 11,280 per s; box size switches at 5,000/s in the tool — the load test decides |
| DB writes | 6 / 15 / 40 per s average; 3× at peak |
| Filter CPU | ≤ 5 ms per message × ≈ 93 accepted messages/s at stress peak ≈ 0.5 core |
| Latency | send → other client p95 ≤ 1 s; ack p95 ≤ 500 ms |
| Load test (cloud-forge; `chat_load_probe`) | stress profile for 30 min: p95 ≤ 1 s, CPU ≤ 60%, 0 lost messages, egress bytes logged |
| RPO / RTO | ≤ 5 min (WAL shipped every 60 s) / ≤ 30 min (box rebuilt from script + restore) |
| During an outage | ticker "Chat resting"; sends queue ≤ 5; the game runs normally |
| Abuse traffic | host's DDoS filtering (verify it is included); per-IP connect limit 20 per min; token required before any work |
| Deploys | drain: close code 1012, clients spread reconnects over 10 s (§5.6) |

## 9. Measuring (feeds `core/sd_cost_probe.gd`)

The gateway writes a daily counter row: sent and deliveries per channel, egress bytes, catch-up
rows, writes, storage GB, peak sockets, cloud-translation characters, pushes, reports, held
items. The probe (or a qa-forge script beside it) scales the measured per-DAU rates to 50,000
players with the same formulas as `tools/chat_cost.py --model` and prints
`CHAT COST OK - measured €<x>/month at 50k, envelope €50` (wording fixed by qa-forge).

## 10. Failure modes

| Fails when | Caught by |
|---|---|
| Someone moves fan-out to a per-read or per-message billed service | [ ] tool: B and C rows > envelope at base; design review rule 0.2 |
| Realm stream sent to every online player | [ ] counter: realm deliveries per sent message ≤ R × f_realm × 0.25 at base |
| Cloud translation spend grows silently | [ ] breaker at €10; daily character counter alarm at 80% |
| Duplicate messages after reconnect | [ ] `chat_catchup_probe`: resend with the same `cid` → 1 row |
| Retention job stops; storage grows | [ ] `chat_retention_probe`; alarm when the oldest row > retention + 1 d |
| Reconnect storm after a deploy | [ ] load test with a forced restart: peak connects ≤ 1,000 per s |
| Chat outage blocks gameplay | [ ] kill the chat box in a staging session: `session_audit` still passes |

## 11. Backend checklist

- [ ] Isolation rules 0.1–0.3 hold (separate process and DB, no per-delivery billing, game backend owns membership).
- [ ] `python tools/chat_cost.py` re-run with any changed input; the three-scenario table pasted.
- [ ] Every price used is on the verify list with a date and a source.
- [ ] Load test at the stress profile passed; box size confirmed.
- [ ] Retention, erasure and backup expiry jobs scheduled and probed.
- [ ] `sd_cost_probe` chat line reads measured counters, not the assumptions.
