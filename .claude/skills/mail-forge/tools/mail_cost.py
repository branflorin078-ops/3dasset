"""Mail cost model for mail-forge - the arithmetic behind references/backend-cost.md.

    python mail_cost.py                     # base / high / stress, every line shown
    python mail_cost.py --scenario stress   # one scenario
    python mail_cost.py --trap all          # the known traps, each priced against stress
    python mail_cost.py --model my.json     # override inputs with measured values, e.g.
                                            #   {"stress": {"ov_kb": 0.42}, "prices": {"rtdb_dl_gb": 1.0}}
    python mail_cost.py --json              # machine-readable totals (compare with sd_cost_probe)
    python mail_cost.py --selftest          # prints 'MAIL COST SELFTEST OK - n checks'

Stack: Firebase Realtime Database (billed on DOWNLOADED bytes and STORED bytes, not on
operations; uploads are free) + a callable Cloud Function for letters, alliance mail and premium
claims + FCM push (no per-message fee). Source: the studio's cloud-forge brief (confirm against
firebase/COST_AUDIT.md, path to confirm). Every input is an ASSUMPTION until core/sd_cost_probe.gd
measures it. Prices: USD list prices seen in search snippets on 2026-09-26 - verify each one
(backend-cost.md section 2). EUR = USD x 0.85-0.95 (the range chat-forge uses). Python 3, no deps.
"""
import argparse
import json
import sys

DAYS = 30
PLAYERS = 50000
FX = (0.85, 0.95)            # USD -> EUR
MAIL_ENVELOPE_EUR = 30       # PROPOSAL: mail's line in the EUR 200 split at STRESS (owner decision)
MAIL_BASE_EUR = 10           # PROPOSAL: mail at BASE must stay under this

PRICES = {                   # USD - VERIFY ALL (backend-cost.md section 2)
    "rtdb_dl_gb": 1.00,      # RTDB download per GB (two snippets agree)
    "rtdb_store_gb": 5.00,   # RTDB storage per GB-month (two snippets agree)
    "fn_per_million": 0.40,  # Cloud Run functions per million requests (snippet)
    "fn_vcpu_s": 0.000024,   # per vCPU-second, tier 1 (not in a snippet - verify)
    "fn_gib_s": 0.0000025,   # per GiB-second, tier 1 (not in a snippet - verify)
    "egress_gb": 0.12,       # function internet egress per GB (not in a snippet - verify)
    "tls_kb": 3.5,           # billed download per NEW TLS connection (Firebase billing doc)
}
# Free tiers (RTDB 1 GB stored + 10 GB/month; functions 2 M requests, 180k vCPU-s, 360k GiB-s)
# are shared by the whole game, so mail is priced at the MARGINAL rate: no free tier credited.

SCEN = {  # per DAU per day unless named; sizes in KB (1 KB = 1,000 bytes)
    "base":   dict(dau_share=0.40, sessions=6, head_piggyback=1.0, head_kb=0.05, ov_kb=0.35,
                   inbox_opens=1.5, p_personal_new=0.9, p_alliance_new=0.5, claim_calls=1.2,
                   delete_batches=1.0,
                   m_rewards=1.5, item_p=0.25, m_notice=0.5, item_n=0.30, m_alliance=0.5, item_a=0.25,
                   a_text_share=0.5, body_a=0.60, letters=0.5, item_l=0.18, body_l=0.35,
                   report_rows=8, row_kb=0.08, sends=0.3, fn_send_kb=0.50,
                   premium_claims=0.03, fn_wallet_kb=1.0, resync_share=0.005,
                   res_p=5, res_n=4, res_l=10, res_r=10, report_cap=100, kept_avg=3,
                   inactive=60000, inactive_kb=1.5, alliance_members=20,
                   fn_s=0.3, vcpu=0.167, gib=0.25, resp_kb=0.8),
    "high":   dict(dau_share=0.60, sessions=7, head_piggyback=1.0, head_kb=0.05, ov_kb=0.40,
                   inbox_opens=2.0, p_personal_new=0.9, p_alliance_new=0.6, claim_calls=1.5,
                   delete_batches=1.0,
                   m_rewards=2.0, item_p=0.28, m_notice=0.7, item_n=0.35, m_alliance=0.8, item_a=0.28,
                   a_text_share=0.5, body_a=0.90, letters=0.8, item_l=0.20, body_l=0.50,
                   report_rows=12, row_kb=0.09, sends=0.5, fn_send_kb=0.60,
                   premium_claims=0.05, fn_wallet_kb=1.0, resync_share=0.0075,
                   res_p=6, res_n=5, res_l=11, res_r=12, report_cap=100, kept_avg=6,
                   inactive=80000, inactive_kb=1.8, alliance_members=20,
                   fn_s=0.3, vcpu=0.167, gib=0.25, resp_kb=1.0),
    "stress": dict(dau_share=1.00, sessions=8, head_piggyback=1.0, head_kb=0.06, ov_kb=0.50,
                   inbox_opens=2.5, p_personal_new=0.95, p_alliance_new=0.7, claim_calls=2.0,
                   delete_batches=1.0,
                   m_rewards=2.5, item_p=0.30, m_notice=1.0, item_n=0.40, m_alliance=1.2, item_a=0.30,
                   a_text_share=0.6, body_a=1.50, letters=1.2, item_l=0.22, body_l=0.75,
                   report_rows=15, row_kb=0.10, sends=0.8, fn_send_kb=0.80,
                   premium_claims=0.10, fn_wallet_kb=1.2, resync_share=0.01,
                   res_p=6, res_n=6, res_l=12, res_r=14, report_cap=100, kept_avg=10,
                   inactive=100000, inactive_kb=2.0, alliance_members=20,
                   fn_s=0.4, vcpu=0.167, gib=0.25, resp_kb=1.2),
}

TRAPS = {
    "cold":    "every mail REST call opens a NEW TLS connection (a fresh HTTPRequest per call)",
    "poll":    "a 60 s poll of the mail head while the app is open (60 min online per DAU per day)",
    "ownhead": "the mail head is its own GET each session instead of riding cloud.gd's resume read",
    "fanout":  "alliance mail copied into every member's inbox instead of stored once per alliance",
    "fnclaim": "every claim goes through the function instead of the database-rules gate",
    "leak":    "notices fanned out to 200k dormant accounts for a year with no cold-account sweep",
}


def requests_per_day(s, trap=None):
    head = s["sessions"] * (1.0 if trap == "ownhead" else 1.0 - s["head_piggyback"])
    claims = 0.0 if trap == "fnclaim" else s["claim_calls"]
    return (head
            + s["inbox_opens"] * (s["p_personal_new"] + s["p_alliance_new"])  # delta GETs
            + claims                                                         # rules-gated PATCH
            + s["delete_batches"])                                           # daily delete PATCH


def downloads(s, trap=None):
    """KB per DAU per day by line; returns (lines, REST round trips per day)."""
    req = requests_per_day(s, trap)
    ov = s["ov_kb"] + (PRICES["tls_kb"] if trap == "cold" else 0.0)
    held = (s["m_rewards"] * s["res_p"] + s["m_notice"] * s["res_n"] + s["letters"] * s["res_l"]
            + min(s["report_rows"] * s["res_r"], s["report_cap"]))
    L = {
        "REST overhead (headers + TLS records)": req * ov,
        "head payload (rides the resume read)": s["sessions"] * s["head_kb"],
        "reward items": s["m_rewards"] * s["item_p"],
        "notices (fanned out, painted-header id only)": s["m_notice"] * s["item_n"],
        "letters (header + body)": s["letters"] * (s["item_l"] + s["body_l"]),
        "alliance mail (shared node)": s["m_alliance"] * (s["item_a"] + s["a_text_share"] * s["body_a"]),
        "report rows (pointers; bodies = report-forge)": s["report_rows"] * s["row_kb"],
        "function reads: sends": s["sends"] * s["fn_send_kb"],
        "function reads: premium wallet": s["premium_claims"] * s["fn_wallet_kb"],
        "device resync (new phone / reinstall)": s["resync_share"] * held * 0.3,
    }
    if trap == "fnclaim":
        L["TRAP function reads per claim"] = s["claim_calls"] * 0.15 + s["m_rewards"] * 0.4
    if trap == "poll":
        L["TRAP 60 s head poll"] = 60 * (s["ov_kb"] + s["head_kb"])
    return L, req


def storage(s, trap=None):
    """Stored KB per active account (by line) and total GB."""
    per = {
        "reward items held (+ 30 B claim record)": s["m_rewards"] * s["res_p"] * (s["item_p"] + 0.03),
        "notices held": s["m_notice"] * s["res_n"] * s["item_n"],
        "letters held": s["letters"] * s["res_l"] * (s["item_l"] + s["body_l"]),
        "kept letters": s["kept_avg"] * (s["item_l"] + s["body_l"]),
        "report rows held (cap)": min(s["report_rows"] * s["res_r"], s["report_cap"]) * s["row_kb"],
        "head + rate state": 0.25,
    }
    dau = PLAYERS * s["dau_share"]
    alliances = dau / s["alliance_members"]
    a_kb = s["item_a"] + s["a_text_share"] * s["body_a"]
    shared = alliances * s["m_alliance"] * 30 * a_kb            # once per alliance, 30 d
    if trap == "fanout":
        per["TRAP alliance mail copied per member"] = s["m_alliance"] * 30 * a_kb
    extra = 0.0
    if trap == "leak":
        extra = 200000 * s["m_notice"] * 365 * s["item_n"]
    gb = (dau * sum(per.values()) + s["inactive"] * s["inactive_kb"] + shared + extra) / 1e6
    return per, shared, extra, gb


def cost(s, trap=None):
    dau = PLAYERS * s["dau_share"]
    dl, req = downloads(s, trap)
    kb_day = sum(dl.values())
    dl_gb = dau * kb_day * DAYS / 1e6
    per, shared, extra, st_gb = storage(s, trap)
    calls = s["sends"] + s["premium_claims"] + (s["claim_calls"] if trap == "fnclaim" else 0.0)
    inv = dau * calls * DAYS
    fn = (inv / 1e6 * PRICES["fn_per_million"] + inv * s["fn_s"] * s["vcpu"] * PRICES["fn_vcpu_s"]
          + inv * s["fn_s"] * s["gib"] * PRICES["fn_gib_s"])
    eg = inv * s["resp_kb"] / 1e6
    usd = {"RTDB downloads": dl_gb * PRICES["rtdb_dl_gb"], "RTDB storage": st_gb * PRICES["rtdb_store_gb"],
           "function requests + compute": fn, "function egress": eg * PRICES["egress_gb"], "push (FCM)": 0.0}
    tot = sum(usd.values())
    return {"dau": dau, "requests_per_dau_day": req, "kb_per_dau_day": kb_day, "dl_lines": dl,
            "dl_gb_month": dl_gb, "store_per_active_kb": per, "store_shared_kb": shared,
            "store_leak_kb": extra, "store_gb": st_gb, "invocations_month": inv, "egress_gb": eg,
            "usd": usd, "usd_total": tot, "eur_total": (tot * FX[0], tot * FX[1])}


def show(name, s, trap=None):
    r = cost(s, trap)
    t = "" if not trap else "\n   TRAP '%s': %s" % (trap, TRAPS[trap])
    print("\n== %s: %d DAU (%.0f%% of %d players)%s" % (name, r["dau"], s["dau_share"] * 100, PLAYERS, t))
    print("  REST round trips per DAU per day: %.1f   function calls per DAU per day: %.2f"
          % (r["requests_per_dau_day"], r["invocations_month"] / r["dau"] / DAYS))
    print("  downloads per DAU per day (KB):")
    for k, v in r["dl_lines"].items():
        print("    %-48s %7.2f" % (k, v))
    print("    %-48s %7.2f  -> x %d DAU x %d d = %.1f GB/month" % ("TOTAL", r["kb_per_dau_day"], r["dau"], DAYS, r["dl_gb_month"]))
    print("  stored per active account (KB):")
    for k, v in r["store_per_active_kb"].items():
        print("    %-48s %7.2f" % (k, v))
    print("    %-48s %7.2f  -> x %d + %d inactive x %.1f KB + alliance %.0f MB%s = %.2f GB"
          % ("TOTAL", sum(r["store_per_active_kb"].values()), r["dau"], s["inactive"], s["inactive_kb"],
             r["store_shared_kb"] / 1e3, "" if not r["store_leak_kb"] else " + LEAK %.0f MB" % (r["store_leak_kb"] / 1e3),
             r["store_gb"]))
    print("  function: %.2f M invocations/month, egress %.2f GB" % (r["invocations_month"] / 1e6, r["egress_gb"]))
    print("  monthly cost (USD):")
    for k, v in r["usd"].items():
        print("    %-48s %7.2f" % (k, v))
    lo, hi = r["eur_total"]
    flag = "fits" if hi <= MAIL_ENVELOPE_EUR else ("OVER at high FX" if lo <= MAIL_ENVELOPE_EUR else "OVER")
    print("    %-48s %7.2f  = EUR %.1f-%.1f (%.1f%% of EUR 200; envelope EUR %d: %s)"
          % ("TOTAL", r["usd_total"], lo, hi, hi / 2.0, MAIL_ENVELOPE_EUR, flag))
    m2 = m2_eur(r)
    print("  lever M2 (mail rows on chat-forge's Postgres box, marginal): EUR %.2f-%.2f "
          "(storage + backups; egress inside the box's included TB)" % m2)
    return r


def m2_eur(r):
    """Marginal EUR/month if mail rows move to chat-forge's A1 box (chat_cost.py price ranges):
    volume EUR 0.04-0.12 per GB-month; 7 compressed backup copies at 0.4 ratio on object storage
    EUR 0.005-0.025 per GB-month; egress inside the included 20 TB; CPU inside the box's headroom."""
    gb = r["store_gb"]
    return (gb * 0.04 + gb * 0.4 * 7 * 0.005, gb * 0.12 + gb * 0.4 * 7 * 0.025)


def selftest():
    n = 0
    b, h, x = (cost(SCEN[k]) for k in ("base", "high", "stress"))
    assert b["usd_total"] < h["usd_total"] < x["usd_total"]; n += 1
    for r in (b, h, x):
        assert r["eur_total"][1] <= MAIL_ENVELOPE_EUR, "every scenario fits the envelope at high FX"; n += 1
    assert b["eur_total"][1] <= MAIL_BASE_EUR, "base stays under the base cap"; n += 1
    assert m2_eur(x)[1] < 2.0, "lever M2 must cost < EUR 2 marginal at stress"; n += 1
    assert x["requests_per_dau_day"] <= 10, "stress round-trip budget"; n += 1
    assert b["requests_per_dau_day"] <= 6, "base round-trip budget"; n += 1
    for t in TRAPS:
        assert cost(SCEN["stress"], t)["usd_total"] > x["usd_total"] * 1.10, t; n += 1
    for t in ("cold", "poll", "leak"):
        assert cost(SCEN["stress"], t)["eur_total"][0] > MAIL_ENVELOPE_EUR, t; n += 1
    # hand check: stress downloads = 50,000 DAU x kb/day x 30 d / 1e6 GB
    assert abs(x["dl_gb_month"] - 50000 * x["kb_per_dau_day"] * 30 / 1e6) < 1e-9; n += 1
    # hand check: base invocations = 20,000 x (0.3 sends + 0.03 premium) x 30 = 198,000
    assert abs(b["invocations_month"] - 198000) < 1e-6; n += 1
    print("MAIL COST SELFTEST OK - %d checks" % n)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", choices=list(SCEN))
    ap.add_argument("--trap", choices=list(TRAPS) + ["all"])
    ap.add_argument("--model")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.model:
        with open(a.model, encoding="utf-8") as f:
            o = json.load(f)
        PRICES.update(o.get("prices", {}))
        for k in SCEN:
            SCEN[k].update(o.get(k, {}))
    if a.selftest:
        return selftest()
    names = [a.scenario] if a.scenario else list(SCEN)
    if a.json:
        print(json.dumps({k: cost(SCEN[k]) for k in names}, indent=1, default=float))
        return 0
    if a.trap:
        base = cost(SCEN["stress"])["usd_total"]
        for t in (TRAPS if a.trap == "all" else [a.trap]):
            r = show("stress", SCEN["stress"], t)
            print("  TRAP DELTA vs stress: +USD %.2f/month (x%.1f)" % (r["usd_total"] - base, r["usd_total"] / base))
        return 0
    for k in names:
        show(k, SCEN[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
