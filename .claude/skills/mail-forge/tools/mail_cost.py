"""Mail cost model for mail-forge - the arithmetic behind references/backend-cost.md.

    python mail_cost.py                     # base / high / stress, every line shown
    python mail_cost.py --scenario stress   # one scenario
    python mail_cost.py --trap all          # the four known traps priced against stress
    python mail_cost.py --model my.json     # override inputs, e.g. measured values:
                                            #   {"stress": {"ov_kb": 0.42}, "prices": {"rtdb_dl_gb": 1.0}}
    python mail_cost.py --json              # machine-readable totals (compare with sd_cost_probe)
    python mail_cost.py --selftest          # prints 'MAIL COST SELFTEST OK - n checks'

Stack assumed: Firebase Realtime Database (billed on downloaded bytes and stored bytes, NOT on
operations) + callable Cloud Functions for claims and sends + FCM for push (no per-message fee).
Source: the studio's cloud-forge brief (confirm against firebase/COST_AUDIT.md, path to confirm).
Every input is an ASSUMPTION until core/sd_cost_probe.gd measures it. Prices are USD list prices
seen in search snippets on 2026-09-26 - verify each one (backend-cost.md section 2) before any
decision. EUR = USD x 0.85-0.95 (same range as chat-forge). Plain Python 3, no dependencies.
"""
import argparse
import copy
import json
import sys

DAYS = 30
PLAYERS = 50000
FX = (0.85, 0.95)            # USD -> EUR range
MAIL_ENVELOPE_EUR = 20       # PROPOSAL: mail's share of the EUR 200 budget (owner decision)

PRICES = {                   # USD. VERIFY ALL (backend-cost.md section 2)
    "rtdb_dl_gb": 1.00,      # RTDB download per GB (verified in 2 snippets)
    "rtdb_store_gb": 5.00,   # RTDB storage per GB-month (verified in 2 snippets)
    "fn_per_million": 0.40,  # Cloud Run functions, per million requests (snippet)
    "fn_vcpu_s": 0.000024,   # per vCPU-second, tier 1 (NOT seen in a snippet - verify)
    "fn_gib_s": 0.0000025,   # per GiB-second, tier 1 (NOT seen in a snippet - verify)
    "egress_gb": 0.12,       # Cloud Run internet egress per GB (NOT seen in a snippet - verify)
    "tls_kb": 3.5,           # billed download per NEW TLS connection (Firebase billing doc)
}
# Free tiers (RTDB 1 GB + 10 GB/month; functions 2 M requests, 180k vCPU-s, 360k GiB-s) are shared
# by the whole game, so mail is priced at the MARGINAL rate: no free tier is credited here.

SCEN = {
    # per DAU per day unless named; sizes in KB (1 KB = 1,000 bytes)
    "base":   dict(dau_share=0.40, sessions=6, inbox_opens=1.5, report_tab_opens=1.5,
                   p_alliance_new=0.5, p_bcast_new=0.3, ov_kb=0.35, head_kb=0.10, bhead_kb=0.40,
                   m_personal=2.0, item_p=0.25, m_bcast=0.6, item_b=0.40, m_alliance=0.7, item_a=0.25,
                   a_text_share=0.5, body_a=0.60, letters=0.5, item_l=0.18, body_l=0.40,
                   report_rows=8, row_kb=0.12, claim_calls=1.5, keys_claimed=2.1, fn_key_kb=0.40,
                   fn_call_kb=0.15, sends=0.3, fn_send_kb=0.50, premium_claims=0.05, fn_wallet_kb=1.0,
                   resync_share=0.01, resync_items=150, res_p=6, res_l=10, res_r=10, report_cap=200,
                   inactive=60000, inactive_kb=1.5, alliance_members=20, realms=15, res_bcast=14,
                   fn_s=0.3, vcpu=0.167, gib=0.25, resp_kb=0.8),
    "high":   dict(dau_share=0.60, sessions=7, inbox_opens=2.0, report_tab_opens=2.0,
                   p_alliance_new=0.6, p_bcast_new=0.4, ov_kb=0.40, head_kb=0.10, bhead_kb=0.45,
                   m_personal=2.5, item_p=0.28, m_bcast=0.8, item_b=0.45, m_alliance=1.0, item_a=0.28,
                   a_text_share=0.5, body_a=0.90, letters=0.8, item_l=0.20, body_l=0.60,
                   report_rows=12, row_kb=0.13, claim_calls=2.0, keys_claimed=2.6, fn_key_kb=0.45,
                   fn_call_kb=0.15, sends=0.5, fn_send_kb=0.60, premium_claims=0.08, fn_wallet_kb=1.0,
                   resync_share=0.015, resync_items=200, res_p=7, res_l=11, res_r=12, report_cap=200,
                   inactive=80000, inactive_kb=1.8, alliance_members=20, realms=20, res_bcast=14,
                   fn_s=0.3, vcpu=0.167, gib=0.25, resp_kb=1.0),
    "stress": dict(dau_share=1.00, sessions=8, inbox_opens=2.5, report_tab_opens=3.0,
                   p_alliance_new=0.7, p_bcast_new=0.5, ov_kb=0.50, head_kb=0.12, bhead_kb=0.50,
                   m_personal=3.0, item_p=0.30, m_bcast=1.0, item_b=0.50, m_alliance=1.5, item_a=0.30,
                   a_text_share=0.6, body_a=1.50, letters=1.2, item_l=0.22, body_l=0.90,
                   report_rows=15, row_kb=0.15, claim_calls=2.5, keys_claimed=3.2, fn_key_kb=0.50,
                   fn_call_kb=0.20, sends=0.8, fn_send_kb=0.80, premium_claims=0.10, fn_wallet_kb=1.2,
                   resync_share=0.02, resync_items=250, res_p=8, res_l=12, res_r=14, report_cap=200,
                   inactive=100000, inactive_kb=2.0, alliance_members=20, realms=25, res_bcast=14,
                   fn_s=0.4, vcpu=0.167, gib=0.25, resp_kb=1.2),
}

TRAPS = {
    "cold":   "every mail REST call opens a new TLS connection (a fresh HTTPRequest per call)",
    "poll":   "a 60 s poll of the mail head while the app is open (60 min online per DAU per day)",
    "fanout": "broadcast notices copied into every player's inbox instead of stored once per scope",
    "cpu1":   "claim/send function deployed with 1 vCPU instead of the 0.167 vCPU class",
}


def month_downloads(s, trap=None):
    """KB per DAU per day, split into named lines. Returns (lines dict, requests per day)."""
    dau_req = (s["sessions"]                                       # 1 head GET per session
               + 1                                                 # 1 broadcast-head GET per day
               + s["inbox_opens"] * (1 + s["p_alliance_new"] + s["p_bcast_new"])  # delta GETs
               + s["report_tab_opens"]                             # report rows delta GET
               + s["inbox_opens"])                                 # 1 batched PATCH per inbox close
    ov = s["ov_kb"] + (PRICES["tls_kb"] if trap == "cold" else 0.0)
    L = {}
    L["request overhead (headers, TLS records)"] = dau_req * ov
    L["heads (personal + broadcast)"] = s["sessions"] * s["head_kb"] + s["bhead_kb"]
    L["personal items (rewards, notices to you)"] = s["m_personal"] * s["item_p"]
    L["letters (header + body)"] = s["letters"] * (s["item_l"] + s["body_l"])
    L["alliance mail"] = s["m_alliance"] * (s["item_a"] + s["a_text_share"] * s["body_a"])
    L["broadcast notices"] = s["m_bcast"] * s["item_b"]
    L["report rows (pointers only)"] = s["report_rows"] * s["row_kb"]
    L["function-side reads: claims"] = s["claim_calls"] * s["fn_call_kb"] + s["keys_claimed"] * s["fn_key_kb"]
    L["function-side reads: sends"] = s["sends"] * s["fn_send_kb"]
    L["function-side reads: premium wallet"] = s["premium_claims"] * s["fn_wallet_kb"]
    L["device resync (new install / new phone)"] = s["resync_share"] * s["resync_items"] * s["item_p"]
    if trap == "poll":
        L["TRAP 60 s head poll (60 min online)"] = 60 * (s["ov_kb"] + s["head_kb"])
    if trap == "fanout":
        L["TRAP broadcast copied per player"] = 0.0   # downloads unchanged; storage explodes
    return L, dau_req


def storage_kb(s, trap=None):
    """Stored KB: per active account, per inactive account, shared."""
    per_active = {
        "reward/notice items held": s["m_personal"] * s["res_p"] * (s["item_p"] + 0.08),  # + claim record
        "letters held": s["letters"] * s["res_l"] * (s["item_l"] + s["body_l"]),
        "report rows held": min(s["report_rows"] * s["res_r"], s["report_cap"]) * s["row_kb"],
        "head + rate state": 0.25,
    }
    if trap == "fanout":
        per_active["TRAP broadcast copies"] = s["m_bcast"] * s["res_bcast"] * s["item_b"]
    dau = PLAYERS * s["dau_share"]
    alliances = dau / s["alliance_members"]
    shared = {
        "alliance mail (once per alliance, 30 d)": alliances * s["m_alliance"] * 30
                                                   * (s["item_a"] + s["a_text_share"] * s["body_a"]),
        "broadcast notices (once per scope)": (1 + s["realms"]) * s["m_bcast"] * s["res_bcast"] * s["item_b"],
    }
    return per_active, shared


def cost(s, trap=None):
    s = dict(s)
    if trap == "cpu1":
        s["vcpu"] = 1.0
    dau = PLAYERS * s["dau_share"]
    dl, req = month_downloads(s, trap)
    kb_day = sum(dl.values())
    dl_gb = dau * kb_day * DAYS / 1e6
    per_active, shared = storage_kb(s, trap)
    st_gb = (dau * sum(per_active.values()) + s["inactive"] * s["inactive_kb"] + sum(shared.values())) / 1e6
    inv = dau * (s["claim_calls"] + s["sends"]) * DAYS
    fn_usd = (inv / 1e6 * PRICES["fn_per_million"]
              + inv * s["fn_s"] * s["vcpu"] * PRICES["fn_vcpu_s"]
              + inv * s["fn_s"] * s["gib"] * PRICES["fn_gib_s"])
    eg_gb = inv * s["resp_kb"] / 1e6
    usd = {
        "RTDB downloads": dl_gb * PRICES["rtdb_dl_gb"],
        "RTDB storage": st_gb * PRICES["rtdb_store_gb"],
        "functions (requests + compute)": fn_usd,
        "function egress": eg_gb * PRICES["egress_gb"],
        "push (FCM)": 0.0,
    }
    total = sum(usd.values())
    return {
        "dau": dau, "requests_per_dau_day": req, "kb_per_dau_day": kb_day, "dl_lines": dl,
        "dl_gb_month": dl_gb, "store_gb": st_gb, "store_active_kb": per_active, "store_shared_kb": shared,
        "invocations_month": inv, "egress_gb": eg_gb, "usd": usd, "usd_total": total,
        "eur_total": (total * FX[0], total * FX[1]),
    }


def show(name, s, trap=None):
    r = cost(s, trap)
    t = "" if not trap else "  + TRAP '%s': %s" % (trap, TRAPS[trap])
    print("\n== %s: %d DAU (%.0f%% of %d players)%s" % (name, r["dau"], s["dau_share"] * 100, PLAYERS, t))
    print("  REST round trips per DAU per day: %.1f" % r["requests_per_dau_day"])
    print("  downloads per DAU per day (KB):")
    for k, v in r["dl_lines"].items():
        print("    %-44s %7.2f" % (k, v))
    print("    %-44s %7.2f   -> %.1f GB/month" % ("TOTAL", r["kb_per_dau_day"], r["dl_gb_month"]))
    print("  stored per active account (KB):")
    for k, v in r["store_active_kb"].items():
        print("    %-44s %7.2f" % (k, v))
    print("    %-44s %7.2f   (+ %d inactive x %.1f KB, + shared %.0f KB) -> %.2f GB"
          % ("TOTAL", sum(r["store_active_kb"].values()), s["inactive"], s["inactive_kb"],
             sum(r["store_shared_kb"].values()), r["store_gb"]))
    print("  function invocations: %.2f M/month, egress %.1f GB" % (r["invocations_month"] / 1e6, r["egress_gb"]))
    print("  monthly cost (USD):")
    for k, v in r["usd"].items():
        print("    %-44s %7.2f" % (k, v))
    lo, hi = r["eur_total"]
    flag = "fits" if hi <= MAIL_ENVELOPE_EUR else ("OVER at high FX" if lo <= MAIL_ENVELOPE_EUR else "OVER")
    print("    %-44s %7.2f  = EUR %.1f - %.1f  (%.1f%% of EUR 200; mail envelope EUR %d: %s)"
          % ("TOTAL", r["usd_total"], lo, hi, hi / 2.0, MAIL_ENVELOPE_EUR, flag))
    return r


def selftest():
    n = 0
    b, h, x = (cost(SCEN[k]) for k in ("base", "high", "stress"))
    assert b["usd_total"] < h["usd_total"] < x["usd_total"]; n += 1
    assert x["eur_total"][1] <= MAIL_ENVELOPE_EUR, "stress must fit the mail envelope"; n += 1
    assert b["eur_total"][1] <= MAIL_ENVELOPE_EUR / 2, "base must use <= half the envelope"; n += 1
    assert x["requests_per_dau_day"] <= 25, "stress round-trip budget"; n += 1
    assert b["requests_per_dau_day"] <= 16, "base round-trip budget"; n += 1
    for t in TRAPS:                      # every trap must be visibly expensive
        assert cost(SCEN["stress"], t)["usd_total"] > x["usd_total"] * 1.25, t; n += 1
    assert cost(SCEN["stress"], "cold")["eur_total"][0] > MAIL_ENVELOPE_EUR; n += 1
    assert cost(SCEN["stress"], "poll")["eur_total"][0] > MAIL_ENVELOPE_EUR; n += 1
    # arithmetic spot check: 50,000 DAU x 1 KB x 30 d = 1.5 GB = USD 1.50 of downloads
    one = dict(SCEN["stress"]); r = cost(one)
    assert abs(r["dl_gb_month"] - 50000 * r["kb_per_dau_day"] * 30 / 1e6) < 1e-9; n += 1
    print("MAIL COST SELFTEST OK - %d checks" % n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=list(SCEN))
    ap.add_argument("--trap", choices=list(TRAPS) + ["all"])
    ap.add_argument("--model")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.model:
        with open(a.model) as f:
            o = json.load(f)
        PRICES.update(o.get("prices", {}))
        for k in SCEN:
            SCEN[k].update(o.get(k, {}))
    if a.selftest:
        return selftest()
    names = [a.scenario] if a.scenario else list(SCEN)
    if a.json:
        out = {k: cost(SCEN[k]) for k in names}
        print(json.dumps(out, indent=1, default=float))
        return
    if a.trap:
        base = cost(SCEN["stress"])["usd_total"]
        for t in (TRAPS if a.trap == "all" else [a.trap]):
            r = show("stress", SCEN["stress"], t)
            print("  TRAP DELTA vs stress: +USD %.2f/month (x%.1f)" % (r["usd_total"] - base, r["usd_total"] / base))
        return
    for k in names:
        show(k, SCEN[k])


if __name__ == "__main__":
    sys.exit(main())
