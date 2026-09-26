"""mail-forge tool tests:  python tests/test_tools.py   ->  'MAIL-FORGE TOOLS OK - n checks'

1. mail_cost.py --selftest passes (envelope, round-trip budgets, every trap visibly expensive).
2. claim_sim.py passes on the shipped design (both save policies).
3. Each of the four broken designs is CAUGHT by claim_sim (the simulator has teeth).
4. The cost tool's JSON output reproduces the stress download line by hand.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "tools")


def run(*args):
    p = subprocess.run([sys.executable] + list(args), cwd=TOOLS, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main():
    n = 0
    rc, out = run("mail_cost.py", "--selftest")
    assert rc == 0 and "MAIL COST SELFTEST OK" in out, out; n += 1
    rc, out = run("claim_sim.py", "--seeds", "400")
    assert rc == 0 and "CLAIM SIM OK" in out and " 0 violations" in out, out; n += 1
    rc, out = run("claim_sim.py", "--controls", "--seeds", "400")
    assert rc == 0 and "CONTROLS OK - 4/4" in out, out; n += 1
    assert out.count("CAUGHT") == 4, out; n += 1
    rc, out = run("mail_cost.py", "--json", "--scenario", "stress")
    r = json.loads(out)["stress"]
    assert abs(r["dl_gb_month"] - r["dau"] * r["kb_per_dau_day"] * 30 / 1e6) < 1e-9; n += 1
    assert abs(r["usd"]["RTDB storage"] - r["store_gb"] * 5.0) < 1e-9; n += 1
    print("MAIL-FORGE TOOLS OK - %d checks" % n)


if __name__ == "__main__":
    main()
