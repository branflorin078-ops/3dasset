# Attachments — the claim protocol (exactly once, never lost, never late)

A reward letter is a promise: "these goods are yours, once." The protocol keeps that promise
through double taps, two phones, lost responses, crashed functions, crashed apps, restored
backups and send jobs that run twice. Every number is a **PROPOSAL**; code blocks are sketches
for **cloud-forge** (storage, rules, functions) and **gameplay-forge** (save, inventory). Paths
are "(path to confirm)". The stack (Firebase Realtime Database + callable Cloud Functions) is the
studio's cloud-forge brief. Confirm it before any code is written.

## 0. Two layers, both required

| Layer | What it guarantees | Where it runs |
|---|---|---|
| **Gate** | a claim record `c` is written **at most once** per (player, letter), only by the owner, only before `x` by the SERVER clock, never on a revoked letter | Class I: database rules · Class P: function transaction |
| **Idempotent applier** | the goods enter the store **at most once** per letter: the letter's key is recorded in the SAME atomic write as the goods | Class I: the player's save · Class P: the server wallet |

Neither layer alone is enough. The gate cannot stop a crashed app from applying twice, and the
applier cannot stop a claim after expiry. The claim record is **never stripped** after it is
applied, so any device can re-derive a missed grant until the horizon `H` (§6). That is why a
restored backup or a stale phone cannot lose a reward. The simulator proves each part is
load-bearing (§11).

## 1. What may be attached

| Rule | PROPOSAL |
|---|---|
| Senders | the game only (send jobs, [templates.md](templates.md) §7). Players, officers and alliances attach nothing — no transfer route (economy.md) |
| Content | a fixed list of item lines `{i: item id, n: count}`, 1–8 lines, shown in full before claiming. No random contents, no "mystery" chest opened by the claim itself (monetization.md §9: no gambling look, PEGI-7) |
| Resources | as item packs ("3 h of own output" is an item the player opens later), never raw numbers computed at send time. Opening follows economy.md protection rules |
| Time-limited currencies | only if the currency outlives the letter's hard expiry `x` (validator refuses otherwise) |
| **Class I** (items) | hourglasses, resource packs, Resolve, lord XP, cosmetics. Gate = database rules; applier = the save |
| **Class P** (premium) | gems and anything counted in a server ledger. Gate = function; applier = the server wallet. One class per letter; a mixed reward is two letters |
| Value cap per letter | ≤ 1,440 hourglass-minutes-equivalent (core-loop §5 price table) or ≤ 500 gems; above it the send job needs the owner's second key ([templates.md](templates.md) §7) |

**Open owner decision**: if gems live in the client save today, mail must not carry gems until a
server wallet exists. Class P needs a server-owned balance, or it is only Class I in disguise.

## 2. The letter and its claim record

Short keys on purpose: RTDB bills the stored bytes of key names too ([backend-cost.md](backend-cost.md) §3).

```
/mail/p/{uid}/{id}        id = "{template}~{source}" for game-sent letters (deterministic, §8)
  k   "w" (Rewards)            t   sent, server ms (written as {".sv":"timestamp"})
  x   hard expiry, server ms   tp  template id        ar  args (typed)       hd  header art id
  cl  "I" | "P"                at  [{i, n}, …]        rv  revoked at (ops only, server ms)
  c   {t: server ms}   <- the claim record: written ONCE (rules for "I", function for "P")
/srv/{uid}/wallet         g  gem balance    ap {id: t} applied ids inside the horizon (server only)
save.mail_applied         {id: t}  lives in the player's save, next to the inventory (client)
```

## 3. The state machine

```
                 send job (§8)                       gate: c absent AND owner AND server now < x
   (no letter) ───────────────► AVAILABLE ───────────AND cl matches AND not rv ───────────► CLAIMED
                                 │  │  │                 (Class I: rules · Class P: function)     │
             server now ≥ x      │  │  │ day 30 reached: next open                                │
            ┌────────────────────┘  │  └── auto-claim ── same gate ──────────────────────────────►│
            ▼                       │ ops revoke (transaction: only if c absent)                    │
         EXPIRED                    ▼                                                               │
     (claim refused;             REVOKED                  applier: goods + key in ONE atomic write  │
      lazy purge)            (claim refused)              (Class I: save revision · P: wallet tx)   ▼
                                                                   APPLIED ◄─────────────────────────┘
                                                                      │ 3 d after claim: client deletes
                                                                      ▼ the letter (c goes with it)
                                                                   PURGED ── claim → NOT_FOUND
```

| # | From → to | Guard | Writer | Atomic unit | Repeat of the same request |
|---|---|---|---|---|---|
| T1 | none → AVAILABLE | job lease held; chunk not yet written | send job | 500 letters + job cursor in one multi-path update | same id, leaf writes: no change, `c` untouched |
| T2 | AVAILABLE → CLAIMED (I) | `!c`, owner, `now < x`, `cl = "I"`, `at` exists, `!rv` | client PATCH, checked by rules | all letters of one claim-all PATCH (all or nothing) | refused (c exists) → client re-reads → treats as claimed |
| T3 | AVAILABLE → CLAIMED (P) | same, `cl = "P"` | function | one transaction on the letter node | ALREADY + the same `c.t` |
| T4 | CLAIMED → APPLIED (I) | `id ∉ save.mail_applied` and `c.t > now − H` | client | one save revision: goods + `mail_applied[id]` | skip (key present) |
| T5 | CLAIMED → APPLIED (P) | `id ∉ wallet.ap` | function | one wallet transaction: `g += n` + `ap[id]` | abort (key present) |
| T6 | AVAILABLE → EXPIRED | `now ≥ x` | nobody (time) | — | claims refused |
| T7 | AVAILABLE → REVOKED | `!c` | ops tool | transaction per letter | no-op |
| T8 | APPLIED → PURGED | `c` exists, claimed ≥ 3 d ago, not kept | client lazy purge | one batched delete | no-op |

Invariants: **I1** each claimed Class I letter is in the final save exactly once; **I2** no `c.t ≥ x`,
no claim on a revoked letter; **I3** wallet `g` = the sum of the claimed Class P letters.

## 4. Server-side check A — the database rules (Class I, no function, no cost per claim)

The whole gate for items is the database. A claim is one REST PATCH at `/mail/p/{uid}.json` with
body `{"<id1>/c": {"t": {".sv":"timestamp"}}, "<id2>/c": …}` and `?print=silent`. Multi-path updates
are all-or-nothing: one bad path refuses the whole claim-all (§7 handles that).

```json
{
  "rules": {
    "mail": {
      "p": {
        "$uid": {
          ".read": "auth != null && auth.uid === $uid",
          ".indexOn": ["t"],
          "$id": {
            ".write": "auth != null && auth.uid === $uid && !newData.exists() && (!data.child('at').exists() || data.child('c').exists())",
            "c": {
              ".write": "auth != null && auth.uid === $uid && !data.exists() && newData.exists() && data.parent().child('cl').val() === 'I' && data.parent().child('at').exists() && !data.parent().child('rv').exists() && now < data.parent().child('x').val()",
              ".validate": "newData.hasChildren(['t']) && newData.child('t').val() === now",
              "t": { ".validate": "newData.isNumber()" },
              "$other": { ".validate": false }
            },
            "kp": {
              ".write": "auth != null && auth.uid === $uid && data.parent().child('k').exists() && data.parent().child('k').val() !== 'w'",
              ".validate": "newData.val() === 1"
            }
          }
        }
      },
      "a": {
        "$aid": {
          ".read": "auth != null && root.child('alliances').child($aid).child('m').child(auth.uid).exists() && query.orderByChild === 't' && query.startAt >= root.child('alliances').child($aid).child('m').child(auth.uid).child('j').val()",
          ".indexOn": ["t"]
        }
      },
      "h": { "$uid": { ".read": "auth != null && auth.uid === $uid" } }
    },
    "srv": { "$uid": { "wallet": { ".read": "auth != null && auth.uid === $uid" } } }
  }
}
```

What each line does (JSON is valid; merge it into cloud-forge's rules file, path to confirm):

1. `$id/.write` allows only **delete**, and only when the letter has no attachments or is already
   claimed. "Never delete unclaimed rewards" is enforced by the database, not by the UI.
2. `c/.write` is the gate: owner only, `c` absent, Class I, attachments present, not revoked, and
   **`now` (server clock) before `x`**. The device clock is never read.
3. `c/.validate` forces `t` to be exactly the server timestamp and forbids any other field.
4. No rule grants writes to `k t x cl at rv tp ar hd`. Clients cannot create letters, edit
   attachments, extend expiry or un-revoke. Only the admin SDK (send jobs, functions) writes them.
5. `kp` (keep) may be set on any letter except Rewards. Deleting a keep flag is allowed (validate does
   not run on deletes).
6. Alliance mail is readable only by members, and only through a query ordered by `t` that starts
   at or after the reader's join time (`alliances/{aid}/m/{uid}/j`, path to confirm). Rules are not
   filters: an unfiltered read of the node is refused.
7. The head and the wallet are read-only for their owner.

## 5. Server-side check B — the premium function (Class P)

A sketch for cloud-forge: Cloud Functions for Firebase, 2nd gen, Node. Recommended: add it as an
op of the existing single function (cloud-forge decides).

```js
const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { getDatabase } = require("firebase-admin/database");
const H_MS = 100 * 86400 * 1000;                          // horizon > the 90-day hard expiry

exports.mailClaimP = onCall({ cpu: "gcf_gen1", memory: "256MiB", concurrency: 1, maxInstances: 5 },
  async (req) => {
  const uid = req.auth && req.auth.uid;
  if (!uid) throw new HttpsError("unauthenticated", "sign in first");
  const ids = [...new Set((req.data && req.data.ids) || [])];
  if (ids.length < 1 || ids.length > 20 || !ids.every(k => /^[A-Za-z0-9_~-]{1,64}$/.test(k)))
    throw new HttpsError("invalid-argument", "1-20 letter ids");
  const db = getDatabase();
  const now = Date.now();                                 // server clock, captured once per call
  const out = {};
  for (const id of ids) {
    const tx = await db.ref(`mail/p/${uid}/${id}`).transaction(m => {
      if (m === null) return null;        // first call may be a stale local guess: NEVER abort on it
      if (m.c || m.cl !== "P" || !m.at || m.rv || now >= m.x) return;   // abort; judged below
      m.c = { t: now };
      return m;                            // pure function: no side effects, may run many times
    });
    const m = tx.snapshot.val();
    if (!m) { out[id] = { r: "NOT_FOUND" }; continue; }
    if (!m.c) { out[id] = { r: m.cl !== "P" ? "WRONG_CLASS" : m.rv ? "REVOKED" : "EXPIRED" }; continue; }
    const gems = m.at.filter(a => a.i === "gems").reduce((s, a) => s + a.n, 0);
    await db.ref(`srv/${uid}/wallet`).transaction(w => {  // runs on GRANTED and on ALREADY (resume)
      w = w || { g: 0, ap: {} };
      w.ap = w.ap || {};
      if (w.ap[id]) return;                               // applied before: no second grant
      w.g = (w.g || 0) + gems;
      w.ap[id] = now;
      for (const k in w.ap) if (w.ap[k] < now - H_MS) delete w.ap[k];
      return w;
    });
    out[id] = { r: m.c.t === now ? "GRANTED" : "ALREADY", t: m.c.t };
  }
  return { now, out, g: (await db.ref(`srv/${uid}/wallet/g`).get()).val() || 0 };
});
```

Traps this code avoids (each has cost someone money):

- **The null first call.** The admin SDK calls the handler first with its cached value, often
  `null`. Aborting on `null` reports NOT_FOUND for a letter that exists. Returning `null` commits
  nothing if the node is really empty, and it forces a retry with the server's data if it is not.
- **Side effects inside the handler.** The handler may run several times. The wallet is touched
  only after the gate returns, in its own keyed transaction.
- **Crash between gate and wallet.** The retry sees `c` present and answers ALREADY. The wallet
  transaction then runs anyway and adds only if `ap[id]` is missing. That is how the resume works.
- **Cost.** 0.167 vCPU class (`gcf_gen1` at 256 MiB, concurrency 1). A 1 vCPU deploy multiplies
  compute about 6×. `maxInstances: 5` caps a hammering client. Every retry is free of effect, so
  hammering gains nothing.

## 6. The client applier (Class I)

Sketch in GDScript 4. The save, inventory and cloud names are placeholders (gameplay-forge and
cloud-forge own the real ones).

```gdscript
const HORIZON_MS := 100 * 86400 * 1000

func apply_claimed(letters: Dictionary) -> void:          # id -> letter from the cache or a fetch
	var now_ms := Cloud.server_now_ms()                    # device time + server offset (core-loop §4.6)
	var changed := false
	for id in letters:
		var m: Dictionary = letters[id]
		if m.get("cl", "") != "I" or not m.has("c") or not m.has("at"):
			continue
		if save.mail_applied.has(id) or int(m["c"]["t"]) < now_ms - HORIZON_MS:
			continue
		for line in m["at"]:
			save.inventory_add(String(line["i"]), int(line["n"]))
		save.mail_applied[id] = int(m["c"]["t"])        # SAME save revision as the goods above
		changed = true
	if changed:
		save.write_local()      # temp file + DirAccess.rename_absolute(): the write is all or nothing
		Cloud.push_soon()       # the normal cloud.gd push; mail adds no push path of its own
```

1. **Re-derive, never replay.** At every start, after every pull of a newer cloud save, and after
   every fetch, run `apply_claimed` over the cached letters. The goods are derived from `c` + `at`,
   so a restored backup, a stale phone or a crash never loses a claimed reward.
2. **Never merge saves by replaying deltas.** If cloud-forge resolves a save conflict, it keeps ONE
   whole revision (base-revision check preferred, last-writer-wins tolerated) and then re-derives.
   Adding "local changes since base" on top of another save doubles grants (control `merge`).
3. **Horizon `H` = 100 d** (> `x` max 90 d): `mail_applied` entries older than `H` are pruned. A claim
   record older than `H` is ignored, so a pruned key can never re-apply.
4. **Class P on the client** is display only: it shows the `g` the function returns. A premium letter
   whose last call had no answer is called again at the next start. The call is idempotent, and a
   letter with `c` and no confirmed answer is exactly that case.

## 7. Claim, claim-all and auto-claim

| Step | Class I | Class P |
|---|---|---|
| Request | one PATCH with every selected id's `c` (≤ 50 ids) over cloud.gd's open connection, `print=silent` | one function call, ≤ 20 ids |
| Success | HTTP 204 → set `c` locally → `apply_claimed` → one ceremony | `out[id].r` GRANTED or ALREADY → update the balance → same ceremony |
| Refused | HTTP 401 → GET the delta → ids that are still claimable are sent again ONCE; the rest show their reason from the fetched state (claimed elsewhere → counted as success; expired; revoked) | per-id reason codes |
| No answer | retry the same body after 1 s and 3 s; then GET and decide as above | retry the same ids after 1 s and 3 s; then at next start |
| Offline | buttons disabled, "Needs a connection" — nothing is queued | same |

- **Claim-all** sends the Class I PATCH and the Class P call in parallel. It shows one merged
  summary ("Claimed from 7 letters · 1 expired") and one ceremony ([ui.md](ui.md) §5).
- **Auto-claim**: at the first session of the day, every Rewards letter with `now ≥ t + 30 d` and no
  `c` is claimed through the same two paths. A digest line appears: "The Chancery claimed 3 rewards
  for you." There is no ceremony. Overflow above 200 Rewards letters auto-claims the oldest the same
  way.
- A claim never waits on a push notification, a timer or a server tick.

## 8. Send-once — game-sent letters

Liveops R7 wants reached rewards in the inbox ≤ 1 h after an event ends, exactly once, for up to
50,000 recipients. The send job (admin SDK script or scheduled function; cloud-forge) uses four guards:

1. **Lease**: a transaction on `/mail/jobs/{job}/lease` (`{by, until}`, 120 s, renewed with each chunk).
   A second runner stops. A dead runner's lease expires, and the next runner resumes.
2. **Cursor in the chunk**: each chunk of 500 recipients (ordered by uid, from server-side data) is
   ONE multi-path update. It writes the 500 letters, their head counters
   (`ServerValue.increment(1)`) and `/mail/jobs/{job}/cursor`. A crash leaves the chunk fully written
   or not written at all.
3. **Deterministic id** `"{template}~{source}"` (e.g. `ev_result~harvest_2026w39`) plus **leaf writes**
   (`…/{id}/k`, `…/{id}/at`, never the whole node). A re-run writes the same values and can never
   erase an existing `c`.
4. **Status**: `done` is final. Re-running a done job needs the owner's second key (§9), because a
   letter already claimed and purged would be sent again.

`t` is written as the server timestamp in every chunk. Delta fetches order by `t`, so a letter
written late in a long job is still newer than anything the player has seen. The client starts each
delta 60 s before its newest `t` and removes duplicates by id. 50,000 recipients = 100 chunks
(≈ 150 KB each, uploads are free) ≈ 30–60 s.

## 9. Revoke, clawback, mistakes

- **Revoke** (a wrong letter was sent): an ops job sets `rv` with a transaction per letter, only
  where `c` is absent. Letters already claimed stay claimed. The audit query lists them.
- **Clawback** of Class P: only by an audited wallet adjustment (cloud-forge + shop-forge policy),
  never silent, always with an account notice ([templates.md](templates.md) §2.1). Class I is not
  clawed back. The goods live in the client save; the fix is the next send, not a deletion.
- **Two keys**: any send with attachments above the value cap (§1), any re-run of a done job and any
  clawback needs the owner's approval. The dry run prints the recipient count and the total value
  (gem-equivalent) first.

## 10. Exploit table

| Attack | Defence | Enforced by | Test |
|---|---|---|---|
| Double tap, two phones, replayed request | gate writes `c` once; applier keys | rules / function transaction; save revision | mail_claim_test races; claim_sim |
| Claim another player's letter | path `$uid` must equal `auth.uid` | rules | mail_rules_test |
| Set the phone clock back to beat expiry | server `now` in rules, `Date.now()` in the function | server | mail_rules_test boundary ±1 ms; claim_sim control `clientclock` |
| Edit `at` (more goods), extend `x`, remove `rv` | no client write rule on those keys | rules | mail_rules_test |
| Create a fake Rewards letter | no client create rule | rules | mail_rules_test |
| Delete a claimed letter to claim it again | the letter is gone; claim → NOT_FOUND / rules refuse | rules | mail_rules_test |
| Crash the app between goods and key | one atomic save write; re-derive on start | client applier | mail_apply_test; control `splitwrite` |
| Crash the function between gate and wallet | keyed wallet transaction on retry | function | mail_claim_test fault injection |
| Two saves merged by replaying deltas | forbidden: keep one revision, re-derive | cloud-forge save policy | control `merge` |
| Edit the save to add goods | not a mail hole (any save edit can); claim records give cloud-forge's validator a list to reconcile | cloud-forge | cloud-forge save tamper tests |
| Gems through save editing | Class P goods never enter the save | server wallet | mail_claim_test |
| Flood the function to raise the bill | idempotent (no gain), `maxInstances` 5, App Check when integrated (confirm) | function config | mail_cost trap `fnclaim` |
| Farm accounts collect welcome rewards for a main | goods are bound to the account; mail cannot send goods between players | send rules | mail_spam_test |
| A send job runs twice or crashes | lease, cursor in the chunk, deterministic id, leaf writes | send job | mail_job_test |
| An ops typo sends 1,000,000 gems | value cap + two keys + dry run | send tool | mail_job_test value-cap case |

## 11. Proof — the design-level simulator

`python tools/claim_sim.py` models §3–§7: rules gate (all-or-nothing), function gate with a crash
point before the wallet, two devices per player, double taps, 10% lost requests, 10% lost
responses, 15% function crashes, device crashes with and without local data loss, and whole-save
pushes with a base-revision check (`rev`) or last-writer-wins (`lww`). Output on 2026-09-26:

```
CLAIM SIM OK - 20000 seeds x 2 policies, 338126 claims, 0 violations
CONTROL splitwrite  CAUGHT - 3427 violations in 2000 seeds (seed 0 policy rev: I1 u0 m4 in save 2, expected 1)
CONTROL merge       CAUGHT - 6372 violations in 2000 seeds (seed 0 policy rev: I1 u1 m0 in save 2, expected 1)
CONTROL clientclock CAUGHT - 781 violations in 2000 seeds (seed 1 policy rev: I2 late/revoked claim u0 m1 t=53 x=46 rv=False)
CONTROL stripack    CAUGHT - 2419 violations in 2000 seeds (seed 2 policy lww: I1 u0 m1 in save 0, expected 2)
CONTROLS OK - 4/4 broken designs caught
```

Read it: the shipped design holds under both save policies. Each control removes one guard and
the simulator catches it: goods and key saved apart → duplicates; delta-replay merge →
duplicates; device clock → late claims; stripping the grant after an ack with last-writer-wins
saves → lost rewards. **What it does not prove**: real RTDB rule semantics, the SDK transaction
behaviour, Godot file atomicity and network timing. qa-forge's emulator tests prove those
([qa.md](qa.md) §2–§4).

## 12. Failure modes and checklist

| Fails when | Caught by |
|---|---|
| A duplicate grant in any race, retry or crash | [ ] mail_claim_test `0 duplicate grants`; claim_sim |
| A claim accepted at `now ≥ x` or on a revoked letter | [ ] mail_rules_test boundary cases |
| A claimed reward missing from the final save | [ ] mail_apply_test restart and restore cases |
| A premium grant added twice after a crash between gate and wallet | [ ] mail_claim_test fault injection |
| A send job writes a letter twice, or erases a `c` | [ ] mail_job_test double start and crash at chunk k |
| The claim path makes a function call for Class I | [ ] sd_cost_probe mail line: 0 function calls per Class I claim |

Before any change to claims, attachments or send jobs:

- [ ] Value class chosen (I or P), one class per letter, ≤ 8 lines, value cap respected.
- [ ] Gate and applier both named for the change; the goods and the key share one atomic write.
- [ ] `python tools/claim_sim.py` prints `CLAIM SIM OK`, and `--controls` prints `CONTROLS OK - 4/4`.
- [ ] Rules diff reviewed line by line against §4; mail_rules_test green in the emulator.
- [ ] Cost re-run: `python tools/mail_cost.py` stays inside the line ([backend-cost.md](backend-cost.md)).
