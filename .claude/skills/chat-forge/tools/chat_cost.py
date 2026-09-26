"""Chat cost model for chat-forge - the arithmetic behind references/backend-cost.md.

    python chat_cost.py                      # base / high / stress, every architecture, price ranges
    python chat_cost.py --scenario stress    # one scenario, full working shown step by step
    python chat_cost.py --model my.json      # override inputs, e.g. measured values:
                                             #   {"base": {"msgs_per_dau": 11}, "prices": {"vps_small": [5, 9]}}
    python chat_cost.py --json               # machine-readable totals (compare with sd_cost_probe)
    python chat_cost.py --selftest           # prints 'CHAT COST SELFTEST OK - n checks'

Every input is an ASSUMPTION until core/sd_cost_probe.gd or the chat gateway's own
counters measure it. Prices are (low, high) EUR ranges from remembered 2025 list
prices (1 USD ~ 0.85-0.95 EUR) - verify each one (backend-cost.md section 7) before
any decision. Plain Python 3, no dependencies.
"""
import argparse
import copy
import json
import sys

DAYS = 30  # billing month

COMMON = {
    "players": 50000,
    # share of SENT messages per channel (system = server-written herald lines)
    "mix": {"alliance": 0.55, "realm": 0.20, "private": 0.12, "group": 0.05, "officer": 0.03, "system": 0.05},
    # PROPOSAL retention in days (channels.md section 3)
    "retention": {"alliance": 30, "realm": 3, "private": 30, "group": 30, "officer": 30, "system": 7},
    "realm_cap_per_min": 20,      # adaptive slow mode target per realm (safety.md section 4)
    "heartbeat_per_min": 2,       # app-level ping every 30 s while the socket is open
    "heartbeat_bytes": 80,        # ping + pong incl. TCP/TLS overhead
    "connect_bytes": 6000,        # TLS handshake with certificate chain + upgrade + hello/welcome
    "cursor_writes_per_session": 2,
    "backup_copies": 7,           # 7 daily compressed dumps kept (+ WAL archive, same bucket)
    "backup_ratio": 0.4,          # dump size / table size (no indexes, compressed text)
    "ticker_ratio": 0.3,          # ticker-only viewers get <= 6 of the <= 20 realm msgs/min
    "foreign_share": 0.30,        # share of delivered messages not in the reader's language
    "langs_per_msg": 2,           # distinct foreign target languages per translated message
    "chars_per_msg": 45,
    "translate_taps_per_dau": 3,
    "poll_bytes": 600,            # one empty HTTP poll, request + response headers
    "peak_box_threshold": 5000,   # peak deliveries/s above which the larger box is priced
}

SCENARIOS = {
    "base": {"dau_share": 0.40, "msgs_per_dau": 15, "online_min": 45, "peak": 3.0, "affinity": 2.5,
             "alliance_size": 60, "realm_size": 3000, "realm_live": 0.25, "group_size": 8, "officers": 5,
             "sessions": 6, "catchup": 30, "bytes_wire": 200, "bytes_row": 400, "ticker_only_share": 0.0},
    "high": {"dau_share": 0.60, "msgs_per_dau": 30, "online_min": 60, "peak": 3.0, "affinity": 2.5,
             "alliance_size": 80, "realm_size": 4000, "realm_live": 0.50, "group_size": 8, "officers": 5,
             "sessions": 7, "catchup": 50, "bytes_wire": 250, "bytes_row": 420, "ticker_only_share": 0.0},
    "stress": {"dau_share": 1.00, "msgs_per_dau": 60, "online_min": 90, "peak": 3.0, "affinity": 1.6,
               "alliance_size": 100, "realm_size": 5000, "realm_live": 1.00, "group_size": 8, "officers": 5,
               "sessions": 8, "catchup": 70, "bytes_wire": 300, "bytes_row": 450, "ticker_only_share": 0.0},
}

# (low, high) EUR per month unless named otherwise. VERIFY ALL (backend-cost.md section 7).
PRICES = {
    "vps_small": [4, 15],             # 2 vCPU / 4 GB, EU budget host, per box
    "vps_large": [8, 30],             # 4 vCPU / 8 GB, EU budget host, per box
    "vps_included_tb": 20,            # egress TB included per box (EU budget host)
    "vps_overage_per_tb": [1.0, 1.2],
    "volume_per_gb": [0.04, 0.12],    # block storage per GB-month
    "object_per_gb": [0.005, 0.025],  # backup object storage per GB-month
    "object_min_fee": [0, 5],         # some object stores bill a monthly minimum instead
    "hyper_vm_small": [15, 35],       # 2 vCPU / 4 GB on a hyperscaler, per box
    "hyper_vm_large": [30, 70],       # 4 vCPU / 8 GB on a hyperscaler, per box
    "hyper_egress_per_gb": [0.05, 0.11],
    "hyper_free_egress_gb": 100,
    "managed_db": [15, 50],           # small managed Postgres (history store for option B)
    "per_msg_per_million": [0.9, 2.4],  # managed realtime billed per delivered message
    "per_msg_base_fee": [0, 25],
    "doc_write_per_100k": [0.08, 0.25],  # document DB, listeners billed as reads
    "doc_read_per_100k": [0.027, 0.055],
    "doc_storage_per_gb": [0.10, 0.17],
    "mt_per_million_chars": [9, 23],     # cloud machine translation
    "translation_fallback_cap": [0, 10], # hard monthly cap on the cloud fallback
    "serverless_per_million_req": [0.18, 0.55],
}

CHAT_ENVELOPE_EUR = 50  # PROPOSAL: chat's share of the EUR 200 budget (owner decision)


def merged(overrides=None):
    common = copy.deepcopy(COMMON)
    scen = copy.deepcopy(SCENARIOS)
    prices = copy.deepcopy(PRICES)
    if overrides:
        for k, v in overrides.get("common", {}).items():
            common[k] = v
        for name, vals in overrides.items():
            if name in scen:
                scen[name].update(vals)
        prices.update(overrides.get("prices", {}))
    return common, scen, prices


def traffic(c, s):
    """Messages, fan-out, bytes and rows per day for one scenario."""
    t = {}
    t["dau"] = c["players"] * s["dau_share"]
    t["sent_wanted"] = t["dau"] * s["msgs_per_dau"]
    # online share of a channel's members at the moment a message is sent
    # f_realm: share of a realm online at peak (every message is priced as if sent at peak)
    # f: share of an alliance/group online when one of them writes (co-play affinity on top)
    t["f_realm"] = min(1.0, s["dau_share"] * s["online_min"] / 1440 * s["peak"])
    t["f"] = min(1.0, t["f_realm"] * s["affinity"])
    sent = {ch: t["sent_wanted"] * share for ch, share in c["mix"].items()}
    t["realms"] = c["players"] / s["realm_size"]
    t["realm_cap_day"] = c["realm_cap_per_min"] * 1440 * t["realms"]
    t["realm_rejected"] = max(0.0, sent["realm"] - t["realm_cap_day"])
    sent["realm"] = min(sent["realm"], t["realm_cap_day"])
    t["sent"] = sent
    t["sent_total"] = sum(sent.values())
    f = t["f"]
    t["recipients"] = {
        "alliance": s["alliance_size"] * f,
        # ticker sampling (lever L1): ticker-only viewers receive ticker_ratio of the realm stream
        "realm": s["realm_size"] * t["f_realm"] * s["realm_live"]
                 * (1 - s["ticker_only_share"] + s["ticker_only_share"] * c["ticker_ratio"]),
        "private": 1.0,
        "group": s["group_size"] * f,
        "officer": s["officers"] * f,
        "system": s["alliance_size"] * f,
    }
    t["deliveries"] = {ch: sent[ch] * t["recipients"][ch] for ch in sent}
    t["deliveries_total"] = sum(t["deliveries"].values())
    t["opm"] = t["dau"] * s["online_min"]                       # online player-minutes per day
    t["ccu_avg"] = t["opm"] / 1440
    t["ccu_peak"] = t["ccu_avg"] * s["peak"]
    t["peak_deliv_s"] = t["deliveries_total"] / 86400 * s["peak"]
    t["catchup_rows"] = t["dau"] * s["sessions"] * s["catchup"]
    t["egress_live_gb"] = t["deliveries_total"] * s["bytes_wire"] / 1e9
    t["egress_catchup_gb"] = t["catchup_rows"] * s["bytes_wire"] / 1e9
    t["egress_hb_gb"] = t["opm"] * c["heartbeat_per_min"] * c["heartbeat_bytes"] / 1e9
    t["egress_connect_gb"] = t["dau"] * s["sessions"] * c["connect_bytes"] / 1e9
    t["egress_day_gb"] = t["egress_live_gb"] + t["egress_catchup_gb"] + t["egress_hb_gb"] + t["egress_connect_gb"]
    t["egress_month_gb"] = t["egress_day_gb"] * DAYS
    t["writes_day"] = t["sent_total"] + t["dau"] * s["sessions"] * c["cursor_writes_per_session"]
    t["rows_stored"] = sum(sent[ch] * c["retention"][ch] for ch in sent)
    t["storage_gb"] = t["rows_stored"] * s["bytes_row"] / 1e9
    t["backup_gb"] = t["storage_gb"] * c["backup_ratio"] * c["backup_copies"]
    return t


def rng(a, b):
    return [a, b]


def add(*ranges):
    return [sum(r[0] for r in ranges), sum(r[1] for r in ranges)]


def mul(r, k):
    return [r[0] * k, r[1] * k]


def costs(c, t, p):
    """Monthly EUR (low, high) per architecture."""
    out = {}
    storage = mul(p["volume_per_gb"], t["storage_gb"])
    per_gb = mul(p["object_per_gb"], t["backup_gb"])
    backups = [max(per_gb[0], p["object_min_fee"][0]), max(per_gb[1], p["object_min_fee"][1])]
    mt = p["translation_fallback_cap"]
    large = t["peak_deliv_s"] >= c["peak_box_threshold"]
    box = p["vps_large"] if large else p["vps_small"]
    over_tb = max(0.0, t["egress_month_gb"] / 1000 - p["vps_included_tb"])
    a1 = add(box, mul(p["vps_overage_per_tb"], over_tb), storage, backups, mt)
    out["A1 flat-traffic VPS, one box + WAL backups"] = a1
    out["A1-HA same + hot standby box"] = add(a1, box)
    hyper = p["hyper_vm_large"] if large else p["hyper_vm_small"]
    hyper_egress = max(0.0, t["egress_month_gb"] - p["hyper_free_egress_gb"])
    out["A2 hyperscaler VM, one box, metered egress"] = add(hyper, mul(p["hyper_egress_per_gb"], hyper_egress),
                                                            storage, backups, mt)
    deliv_m = t["deliveries_total"] * DAYS / 1e6
    out["B per-delivery realtime + managed DB"] = add(mul(p["per_msg_per_million"], deliv_m), p["per_msg_base_fee"],
                                                      p["managed_db"], mt)
    writes_100k = t["writes_day"] * DAYS / 1e5
    reads_100k = (t["deliveries_total"] + t["catchup_rows"]) * DAYS / 1e5
    out["C document DB with listeners"] = add(mul(p["doc_write_per_100k"], writes_100k),
                                              mul(p["doc_read_per_100k"], reads_100k),
                                              mul(p["doc_storage_per_gb"], t["storage_gb"]), mt)
    return out


def translation(c, t, p):
    chars = c["chars_per_msg"]
    rows = {
        "auto-translate every foreign delivery (cloud)": t["deliveries_total"] * c["foreign_share"] * chars * DAYS,
        "auto-translate, cached per message+language (cloud)":
            t["sent_total"] * c["foreign_share"] * c["langs_per_msg"] * chars * DAYS,
        "tap-to-translate, no cache hits (cloud)": t["dau"] * c["translate_taps_per_dau"] * chars * DAYS,
        "on-device translation": 0.0,
    }
    return {k: (v, mul(p["mt_per_million_chars"], v / 1e6)) for k, v in rows.items()}


def polling(c, s, t, p):
    rows = {}
    for n in (3, 5, 15, 30):
        req_day = t["opm"] * 60 / n
        rows["poll every %ds" % n] = (req_day, req_day * c["poll_bytes"] / 1e9,
                                      mul(p["serverless_per_million_req"], req_day * DAYS / 1e6))
    hb = t["opm"] * c["heartbeat_per_min"]
    rows["websocket (connects + ping frames)"] = (t["dau"] * s["sessions"] + hb,
                                                  t["egress_hb_gb"] + t["egress_connect_gb"], [0.0, 0.0])
    return rows


def eur(r):
    return "EUR %6.0f - %6.0f" % (r[0], r[1])


def big(x):
    for unit, div in (("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= div:
            return "%.2f%s" % (x / div, unit)
    return "%.1f" % x


def show(name, c, s, p, detail):
    t = traffic(c, s)
    print("=" * 78)
    print("SCENARIO %s" % name.upper())
    print("  DAU = %d x %.2f = %s" % (c["players"], s["dau_share"], big(t["dau"])))
    print("  sent/day = DAU x %d = %s (realm cap rejects %s)" % (s["msgs_per_dau"], big(t["sent_wanted"]),
                                                                big(t["realm_rejected"])))
    print("  f_realm (realm online at peak) = %.2f x %d/1440 x %.1f = %.4f ; f (alliance/group, x %.1f affinity) = %.4f"
          % (s["dau_share"], s["online_min"], s["peak"], t["f_realm"], s["affinity"], t["f"]))
    if detail:
        print("  %-9s %10s %10s %14s" % ("channel", "sent/day", "fan-out", "deliveries/day"))
        for ch in c["mix"]:
            print("  %-9s %10s %10.2f %14s" % (ch, big(t["sent"][ch]), t["recipients"][ch], big(t["deliveries"][ch])))
    print("  deliveries/day = %s ; peak %s/s ; CCU avg %s peak %s" % (big(t["deliveries_total"]),
          big(t["peak_deliv_s"]), big(t["ccu_avg"]), big(t["ccu_peak"])))
    print("  egress/day = live %.2f + catch-up %.2f + pings %.2f + connects %.2f = %.2f GB ; month %.0f GB"
          % (t["egress_live_gb"], t["egress_catchup_gb"], t["egress_hb_gb"], t["egress_connect_gb"],
             t["egress_day_gb"], t["egress_month_gb"]))
    print("  writes/day %s ; rows stored %s ; storage %.1f GB ; backups %.0f GB (7 compressed dumps)"
          % (big(t["writes_day"]), big(t["rows_stored"]), t["storage_gb"], t["backup_gb"]))
    print("  monthly cost by architecture (chat envelope PROPOSAL EUR %d):" % CHAT_ENVELOPE_EUR)
    for arch, r in costs(c, t, p).items():
        flag = "fits" if r[1] <= CHAT_ENVELOPE_EUR else ("OVER at high prices" if r[0] <= CHAT_ENVELOPE_EUR else "OVER")
        print("    %-44s %s   %s" % (arch, eur(r), flag))
    if detail:
        print("  translation (month):")
        for k, (chars, r) in translation(c, t, p).items():
            print("    %-52s %9s chars  %s" % (k, big(chars), eur(r)))
        print("  polling vs websocket (per day; serverless request price per month):")
        for k, (req, gb, r) in polling(c, s, t, p).items():
            print("    %-34s %9s req  %6.2f GB/day  %s" % (k, big(req), gb, eur(r)))
    return t


def selftest():
    c, scen, p = merged()
    n = 0
    tb, th, ts = (traffic(c, scen[k]) for k in ("base", "high", "stress"))
    assert abs(sum(c["mix"].values()) - 1.0) < 1e-9; n += 1
    assert tb["deliveries_total"] < th["deliveries_total"] < ts["deliveries_total"]; n += 1
    assert ts["realm_rejected"] > 0 and tb["realm_rejected"] == 0; n += 1
    a1, ha = "A1 flat-traffic VPS, one box + WAL backups", "A1-HA same + hot standby box"
    for t in (tb, th, ts):
        assert costs(c, t, p)[a1][1] <= CHAT_ENVELOPE_EUR; n += 1
    for t in (tb, th):
        assert costs(c, t, p)[ha][1] <= CHAT_ENVELOPE_EUR; n += 1
    assert costs(c, tb, p)["B per-delivery realtime + managed DB"][0] > CHAT_ENVELOPE_EUR; n += 1
    assert costs(c, tb, p)["C document DB with listeners"][0] > CHAT_ENVELOPE_EUR; n += 1
    assert costs(c, ts, p)["A2 hyperscaler VM, one box, metered egress"][0] > CHAT_ENVELOPE_EUR; n += 1
    # lever L1 (ticker sampling) must cut stress deliveries by more than 40 %
    s2 = dict(scen["stress"], ticker_only_share=0.8)
    assert traffic(c, s2)["deliveries_total"] < 0.6 * ts["deliveries_total"]; n += 1
    assert translation(c, tb, p)["on-device translation"][0] == 0; n += 1
    # hand check of the base alliance line: 20,000 DAU x 15 x 0.55 = 165,000 sent
    assert abs(tb["sent"]["alliance"] - 165000) < 1e-6; n += 1
    print("CHAT COST SELFTEST OK - %d checks" % n)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", choices=sorted(SCENARIOS))
    ap.add_argument("--model", help="JSON file with overrides")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    over = None
    if a.model:
        with open(a.model, encoding="utf-8") as fh:
            over = json.load(fh)
    c, scen, p = merged(over)
    names = [a.scenario] if a.scenario else ["base", "high", "stress"]
    if a.json:
        out = {}
        for n in names:
            t = traffic(c, scen[n])
            out[n] = {"deliveries_day": t["deliveries_total"], "egress_month_gb": t["egress_month_gb"],
                      "storage_gb": t["storage_gb"], "writes_day": t["writes_day"],
                      "cost_eur": costs(c, t, p)}
        print(json.dumps(out, indent=1))
        return 0
    for n in names:
        show(n, c, scen[n], p, detail=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
