"""forge_run lock queue — plain Python (no Blender), run with:
    py tests/test_runner_queue.py [path/to/forge_run.py]
N workers contend for a TEMP lock (FORGE_LOCK); the test asserts that no two
ever hold it at once (mutual exclusion) and that they are served in arrival
order (FIFO — plain polling let busy agents starve a waiter)."""
import os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "tools", "forge_run.py")
WORKER = r'''
import sys, time, importlib.util
spec = importlib.util.spec_from_file_location("fr", sys.argv[1]); fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)
time.sleep(float(sys.argv[2]))
fr.acquire("w%s" % sys.argv[3], poll=0.1)
t0 = time.time(); time.sleep(0.4); t1 = time.time()
fr.release()
print("%s %.4f %.4f" % (sys.argv[3], t0, t1))
'''


def main():
    if "FORGE_LOCK" not in open(RUNNER, encoding="utf-8").read():
        sys.exit("SKIP: %s has no FORGE_LOCK override - refusing to contend on the REAL lock" % RUNNER)
    tmp = tempfile.mkdtemp(prefix="forge_q_")
    env = dict(os.environ, FORGE_LOCK=os.path.join(tmp, "test.lock"))
    wpath = os.path.join(tmp, "worker.py")
    open(wpath, "w").write(WORKER)
    n = 5
    procs = [subprocess.Popen([sys.executable, wpath, RUNNER, "%.2f" % (0.15 * i), str(i)],
                              stdout=subprocess.PIPE, text=True, env=env) for i in range(n)]
    rows = []
    for p in procs:
        try:
            out, _ = p.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            for q in procs:
                q.kill()
            sys.exit("FAIL runner queue: a worker never got the lock (deadlock/starvation)")
        last = [ln for ln in out.splitlines() if ln.strip()][-1]    # queue notices come first
        rows.append(tuple(float(x) if j else int(x) for j, x in enumerate(last.split())))
    rows.sort(key=lambda r: r[1])
    order = [r[0] for r in rows]
    overlap = any(a[2] > b[1] + 1e-3 for a, b in zip(rows, rows[1:]))
    ok = (not overlap) and order == list(range(n))
    print("%s runner queue: order=%s overlap=%s (%s)" % ("PASS" if ok else "FAIL", order, overlap, RUNNER))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
