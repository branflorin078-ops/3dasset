"""Claim protocol simulator for mail-forge - the evidence behind references/attachments.md.

    python claim_sim.py                        # the shipped design, both save policies, 2,000 seeds each
    python claim_sim.py --seeds 20000          # longer run
    python claim_sim.py --break splitwrite     # negative control: items and applied key saved apart
    python claim_sim.py --break merge          # negative control: save conflicts replay local deltas
    python claim_sim.py --break clientclock    # negative control: expiry checked on the device clock
    python claim_sim.py --break stripack       # negative control: grant stripped after ack + blind saves
    python claim_sim.py --controls             # run all four controls; each MUST report violations

What it models (a design-level model, not the real backend - qa-forge's emulator test is the proof
on real code): mails with attachments in each player's node; Class I items claimed through a
database-rules gate (one atomic multi-path write, all-or-nothing, server clock); Class P (premium)
claimed through a function (gate transaction, then an idempotent wallet transaction, with a crash
possible between the two); two devices per player, double taps, lost requests and lost responses,
retries with the same body, device crashes and restarts, whole-document cloud saves pushed either
with a base-revision check ('rev') or last-writer-wins ('lww'). After the run every device syncs,
then the invariants are checked:
  I1 every claimed Class I mail is in the final cloud save exactly once; unclaimed ones 0 times
  I2 no claim record is dated at or after its mail's expiry, and no revoked mail is claimed
  I3 the server wallet holds exactly the gems of the claimed Class P mails
Prints 'CLAIM SIM OK - <seeds> seeds x 2 policies, <n> claims, 0 violations' or the first
violations with their seed. Python 3, no dependencies.
"""
import argparse
import random
import sys
from collections import Counter

N_PLAYERS, N_MAILS, N_DEVICES, STEPS = 2, 6, 2, 260
P_REQ_LOST, P_RESP_LOST, P_FN_CRASH, P_DEV_CRASH = 0.10, 0.10, 0.15, 0.04


class World:
    def __init__(self, rng, brk, policy):
        self.rng, self.brk, self.policy, self.now = rng, brk, policy, 0
        self.items, self.wallet, self.cloud, self.jobs, self.claims = {}, {}, {}, [], 0
        for u in range(N_PLAYERS):
            self.wallet[u] = {"gems": 0, "applied": set()}
            self.cloud[u] = {"rev": 0, "inv": Counter(), "applied": set()}
            for m in range(N_MAILS):
                self.items[(u, m)] = {"item": "it%d" % m, "n": 1 + m % 4, "cls": "P" if m % 3 == 2 else "I",
                                      "x": rng.randint(30, 200), "rv": rng.random() < 0.1, "c": None,
                                      "at": True}

    # ---- server: database-rules gate (Class I) -------------------------------------------
    def rules_claim(self, u, ids, client_now):
        clock = client_now if self.brk == "clientclock" else self.now
        for m in ids:                                   # all-or-nothing, like a multi-path update
            it = self.items[(u, m)]
            if it["cls"] != "I" or it["c"] is not None or not clock < it["x"] or it["rv"] or not it["at"]:
                return False
        for m in ids:
            self.items[(u, m)]["c"] = {"t": self.now}
            self.claims += 1
        return True

    # ---- server: callable function (Class P) as a generator, one yield per network hop -----
    def fn_claim(self, u, m, client_now, out):
        clock = client_now if self.brk == "clientclock" else self.now
        it = self.items[(u, m)]
        yield
        if it["c"] is None:
            if not clock < it["x"] or it["rv"]:
                out.append(("REFUSED", None)); return
            yield                                       # the transaction commits atomically here
            if it["c"] is None:
                it["c"] = {"t": self.now}; self.claims += 1
        yield                                           # crash window between gate and wallet
        if self.rng.random() < P_FN_CRASH:
            return                                      # instance died: no response
        w, key = self.wallet[u], (u, m)
        if self.brk == "splitwrite":                    # gems and applied key in two writes
            if key not in w["applied"]:
                w["gems"] += it["n"]
                yield
                if self.rng.random() < P_FN_CRASH:
                    return
                w["applied"].add(key)
        elif key not in w["applied"]:                   # ONE transaction: gems + applied key
            w["gems"] += it["n"]; w["applied"].add(key)
        out.append(("GRANTED", it["c"]["t"]))

    def push(self, u, dev):
        cl = self.cloud[u]
        if self.policy == "rev" and dev.base_rev != cl["rev"]:
            return False
        cl["rev"] += 1
        cl["inv"], cl["applied"] = Counter(dev.inv), set(dev.applied)
        dev.base_rev, dev.base_inv = cl["rev"], Counter(dev.inv)
        if self.brk == "stripack":                      # ack: the server strips claimed grants
            for m in dev.applied_now:
                self.items[(u, m)]["at"] = False
        dev.applied_now = set()
        return True


class Device:
    def __init__(self, w, u):
        self.w, self.u, self.skew = w, u, w.rng.randint(-40, 40)
        self.load_cloud()
        self.cache, self.applied_now = {}, set()

    def load_cloud(self):
        cl = self.w.cloud[self.u]
        self.inv, self.applied = Counter(cl["inv"]), set(cl["applied"])
        self.base_rev, self.base_inv = cl["rev"], Counter(cl["inv"])

    def fetch(self):
        if self.w.rng.random() < P_RESP_LOST:
            return
        self.cache = {m: dict(self.w.items[(self.u, m)]) for m in range(N_MAILS)}

    def apply(self):
        """Apply every claimed Class I grant not yet in THIS save; items + key in one revision."""
        for m, it in self.cache.items():
            key = (self.u, m)
            if it["cls"] == "I" and it["c"] is not None and it["at"] and key not in self.applied:
                self.inv[it["item"]] += it["n"]
                if self.w.brk == "splitwrite" and self.w.rng.random() < 0.3:
                    self.crash(); return                # crash after the items, before the key
                self.applied.add(key); self.applied_now.add(m)

    def claim_items(self):
        ids = [m for m, it in self.cache.items() if it["cls"] == "I" and it["c"] is None]
        if not ids:
            return
        ids = self.w.rng.sample(ids, self.w.rng.randint(1, len(ids)))
        for attempt in range(3):                        # same body on every retry
            if self.w.rng.random() < P_REQ_LOST:
                continue
            self.w.rules_claim(self.u, ids, self.w.now + self.skew)
            if self.w.rng.random() < P_RESP_LOST:
                continue
            break
        self.fetch()                                    # success, denial or timeout: re-read, then apply
        self.apply()

    def claim_premium(self):
        ms = [m for m in range(N_MAILS) if self.w.items[(self.u, m)]["cls"] == "P"]
        m = self.w.rng.choice(ms)
        for _ in range(1 + (self.w.rng.random() < 0.3)):  # double tap = two concurrent calls
            self.w.jobs.append(self.w.fn_claim(self.u, m, self.w.now + self.skew, []))

    def push(self):
        if self.w.push(self.u, self):
            return
        if self.w.brk == "merge":                       # replay local deltas on top of the cloud save
            cl = self.w.cloud[self.u]
            delta = self.inv - self.base_inv
            self.inv = cl["inv"] + delta
            self.applied |= cl["applied"]
            self.base_rev, self.base_inv = cl["rev"], Counter(cl["inv"])
            self.w.push(self.u, self)
        else:                                           # adopt the newer save, re-derive, push later
            self.load_cloud(); self.applied_now = set()
            self.apply()

    def crash(self):
        self.load_cloud() if self.w.rng.random() < 0.5 else None  # lost unpushed local state, or not
        self.cache, self.applied_now = {}, set()


def run(seed, brk=None, policy="rev"):
    rng = random.Random(seed)
    w = World(rng, brk, policy)
    devs = [Device(w, u) for u in range(N_PLAYERS) for _ in range(N_DEVICES)]
    for _ in range(STEPS):
        w.now += 1
        if w.jobs and rng.random() < 0.5:               # advance a running function instance
            j = rng.choice(w.jobs)
            try:
                next(j)
            except StopIteration:
                w.jobs.remove(j)
            continue
        d = rng.choice(devs)
        r = rng.random()
        if r < 0.25: d.fetch(); d.apply()
        elif r < 0.50: d.claim_items()
        elif r < 0.62: d.claim_premium()
        elif r < 0.90: d.push()
        elif r < 0.90 + P_DEV_CRASH * 2.5: d.crash()
    for j in w.jobs:                                    # drain function instances
        for _ in j:
            pass
    for _ in range(2):                                  # every device syncs at the end
        for d in rng.sample(devs, len(devs)):
            d.fetch_ok = True
            d.cache = {m: dict(w.items[(d.u, m)]) for m in range(N_MAILS)}
            d.apply()
            while not w.push(d.u, d):
                d.load_cloud(); d.applied_now = set(); d.apply()
    bad = []
    for (u, m), it in w.items.items():
        c = it["c"]
        if c is not None and (c["t"] >= it["x"] or it["rv"]):
            bad.append("I2 late/revoked claim u%d m%d t=%d x=%d rv=%s" % (u, m, c["t"], it["x"], it["rv"]))
        if it["cls"] == "I":
            want = it["n"] if c is not None else 0
            got = w.cloud[u]["inv"][it["item"]]
            if got != want:
                bad.append("I1 u%d m%d in save %d, expected %d" % (u, m, got, want))
    for u in range(N_PLAYERS):
        want = sum(it["n"] for (uu, m), it in w.items.items() if uu == u and it["cls"] == "P" and it["c"])
        if w.wallet[u]["gems"] != want:
            bad.append("I3 u%d wallet %d, expected %d" % (u, w.wallet[u]["gems"], want))
    return bad, w.claims


def batch(seeds, brk, policies):
    total, viol, first = 0, 0, []
    for policy in policies:
        for s in range(seeds):
            bad, n = run(s, brk, policy)
            total += n
            if bad:
                viol += len(bad)
                if len(first) < 3:
                    first.append("seed %d policy %s: %s" % (s, policy, bad[0]))
    return total, viol, first


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", type=int, default=2000)
    ap.add_argument("--break", dest="brk", choices=["splitwrite", "merge", "clientclock", "stripack"])
    ap.add_argument("--controls", action="store_true")
    a = ap.parse_args()
    if a.controls:
        ok = True
        for brk, pol in (("splitwrite", ["rev"]), ("merge", ["rev"]), ("clientclock", ["rev"]),
                         ("stripack", ["lww"])):
            total, viol, first = batch(a.seeds, brk, pol)
            caught = viol > 0
            ok &= caught
            print("CONTROL %-11s %s - %d violations in %d seeds (%s)"
                  % (brk, "CAUGHT" if caught else "MISSED", viol, a.seeds, first[0] if first else "-"))
        print("CONTROLS OK - 4/4 broken designs caught" if ok else "CONTROLS FAIL - a broken design passed")
        return 0 if ok else 1
    policies = ["lww"] if a.brk == "stripack" else ["rev", "lww"]
    total, viol, first = batch(a.seeds, a.brk, policies)
    if total < a.seeds:                                 # check floor: the run must exercise claims
        print("CLAIM SIM FAIL - only %d claims in %d seeds (check floor)" % (total, a.seeds)); return 1
    if viol:
        print("CLAIM SIM FAIL - %d violations%s" % (viol, "".join("\n  " + f for f in first))); return 1
    print("CLAIM SIM OK - %d seeds x %d policies, %d claims, 0 violations%s"
          % (a.seeds, len(policies), total, "" if not a.brk else " (break=%s)" % a.brk))
    return 0


if __name__ == "__main__":
    sys.exit(main())
