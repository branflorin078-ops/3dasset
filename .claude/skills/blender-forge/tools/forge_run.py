"""The ONLY way to launch Blender for blender-forge work.

    python tools/forge_run.py run   <script.py> <mode> <outdir> [extra...]
    python tools/forge_run.py chain <script.py> <outdir>     # export -> verify -> final
    python tools/forge_run.py test  [outdir] [-k substring]  # the regression suite
    python tools/forge_run.py status                         # lock holder + queue
    python tools/forge_run.py which                          # print the Blender it will use

- Finds Blender on Windows / macOS / Linux (env BLENDER wins, then PATH, then
  the newest install under the standard folders).
- Runs with --factory-startup so user add-ons (MCP bridges, human generators)
  never load into a production job — determinism, and a faster start — and
  with --python-exit-code 1 so a script that raises exits NON-ZERO (it used
  to exit 0 with a traceback in the log, and chains ran on).
- Serialises heavy jobs through ONE machine-wide lock, served FIFO: every
  waiter takes a ticket in ~/.blender_forge.queue and only the oldest live
  ticket may take the lock (plain polling let busy agents starve a waiter).
  The lock file itself is unchanged, so older runners still interoperate.
- Logs the full output to <outdir>/<mode>.log and prints only result lines.
"""
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
HOME = os.path.expanduser("~")
LOCK = os.environ.get("FORGE_LOCK") or os.path.join(HOME, ".blender_forge.lock")
QUEUE = LOCK + ".queue" if os.environ.get("FORGE_LOCK") else os.path.join(HOME, ".blender_forge.queue")
RESULT_PREFIXES = ("QA_", "IMPORT", "BAKE", "GLB", "RENDER", "CARD", "SHEET",
                   "TEST", "PASS", "FAIL", "Traceback", "Error", "AttributeError",
                   "KeyError", "TypeError", "ValueError", "RuntimeError", "NameError",
                   "IndexError", "AssertionError", "ModuleNotFoundError")


def find_blender():
    env = os.environ.get("BLENDER")
    if env and os.path.isfile(env):
        return env
    for name in ("blender", "blender.exe"):
        for d in os.environ.get("PATH", "").split(os.pathsep):
            p = os.path.join(d, name)
            if os.path.isfile(p):
                return p
    cands = (glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe")
             + glob.glob("/Applications/Blender*.app/Contents/MacOS/Blender")
             + glob.glob("/opt/blender*/blender") + glob.glob("/usr/bin/blender"))
    if not cands:
        sys.exit("forge_run: no Blender found - set BLENDER=<path to blender>")

    def ver(p):
        import re
        m = re.search(r"(\d+)\.(\d+)", p)
        return (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return sorted(cands, key=ver)[-1]


def _pid_alive(pid):
    if pid <= 0:
        return False
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH"],
                             capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


TICKET_TTL = 30.0   # a waiter refreshes its ticket every poll; silent tickets are dead


def _tickets():
    """Live tickets, oldest first. Liveness is a heartbeat (mtime), not a PID
    check: Windows reuses PIDs, and tasklist per ticket per poll is costly."""
    try:
        names = sorted(os.listdir(QUEUE))
    except OSError:
        return []
    live, now = [], time.time()
    for n in names:
        p = os.path.join(QUEUE, n)
        try:
            fresh = now - os.path.getmtime(p) < TICKET_TTL
        except OSError:
            continue
        if fresh:
            live.append(n)
        else:
            try:
                os.remove(p)
            except OSError:
                pass
    return live


def _lock_owner():
    try:
        pid_s, t_s, owner = open(LOCK).read().split("|", 2)
        return int(pid_s), float(t_s), owner
    except (OSError, ValueError):
        return None


def acquire(tag, poll=2.0, stale_after=3 * 3600):
    """FIFO: take a ticket, wait until it is the oldest live one, then take
    the exclusive-create lock (stale recovery: dead owner or too old)."""
    os.makedirs(QUEUE, exist_ok=True)
    ticket = os.path.join(QUEUE, "%.6f_%d" % (time.time(), os.getpid()))
    open(ticket, "w").close()
    announced = False
    try:
        while True:
            try:
                os.utime(ticket)                    # heartbeat
            except OSError:
                open(ticket, "w").close()           # removed by someone's cleanup: re-queue
            live = _tickets()
            mine = os.path.basename(ticket)
            if mine not in live:
                open(ticket, "w").close()
                continue
            if live[0] == mine:
                try:
                    fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.write(fd, ("%d|%f|%s" % (os.getpid(), time.time(), tag)).encode())
                    os.close(fd)
                    return
                except FileExistsError:
                    own = _lock_owner()
                    if own and (not _pid_alive(own[0]) or time.time() - own[1] > stale_after):
                        try:
                            os.remove(LOCK)
                        except OSError:
                            pass
                        continue
            if not announced:
                own = _lock_owner()
                print("forge_run: queued (position %d of %d); lock held by %s" % (
                    live.index(mine) + 1 if mine in live else 0, len(live),
                    "%s (pid %d)" % (own[2], own[0]) if own else "nobody"), flush=True)
                announced = True
            time.sleep(poll)
    finally:
        try:
            os.remove(ticket)
        except OSError:
            pass


def release():
    try:
        own = _lock_owner()
        if own is None or own[0] == os.getpid():
            os.remove(LOCK)
    except OSError:
        pass


def run(script, args, outdir, logname, timeout=3600):
    os.makedirs(outdir, exist_ok=True)
    blender = find_blender()
    script = os.path.abspath(script)
    log = os.path.join(outdir, logname + ".log")
    acquire("%s %s" % (os.path.basename(script), logname))
    t0 = time.time()
    try:
        # FORGE_LIB may be preset to a STAGED library (skill-engineer tests a
        # candidate lib there, and swaps it into lib/ only when green — so
        # builders importing lib/ mid-run never see a half-edited file).
        env = dict(os.environ)
        env.setdefault("FORGE_LIB", os.path.join(SKILL, "lib"))
        with open(log, "w", encoding="utf-8", errors="replace") as fh:
            proc = subprocess.run([blender, "--background", "--factory-startup",
                                   "--python-exit-code", "1",
                                   "--python", script, "--"] + list(args),
                                  stdout=fh, stderr=subprocess.STDOUT, env=env,
                                  cwd=os.path.dirname(script), timeout=timeout)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        code = "TIMEOUT"
    finally:
        release()
    print("%s: exit %s after %ds  (log %s)" % (logname, code, time.time() - t0, log))
    with open(log, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.lstrip().startswith(RESULT_PREFIXES):
                print("  " + line.rstrip()[:600])
    return code


def status():
    own = _lock_owner()
    print("lock: %s" % ("%s (pid %d, %ds)" % (own[2], own[0], time.time() - own[1]) if own else "free"))
    for i, t in enumerate(_tickets()):
        print("  queue %d: %s" % (i + 1, t))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("run", "chain", "which", "test", "status"):
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "which":
        print(find_blender())
        return
    if cmd == "status":
        status()
        return
    if cmd == "test":
        rest = sys.argv[2:]
        outdir = rest[0] if rest and not rest[0].startswith("-") else os.path.join(SKILL, "tests", "out")
        extra = rest[1:] if rest and not rest[0].startswith("-") else rest
        code = run(os.path.join(SKILL, "tests", "run_tests.py"), ["test", outdir] + extra, outdir, "test")
        sys.exit(0 if code == 0 else 1)
    if cmd == "run":
        if len(sys.argv) < 5:
            sys.exit(__doc__)
        script, mode, outdir = sys.argv[2], sys.argv[3], sys.argv[4]
        code = run(script, [mode, outdir] + sys.argv[5:], outdir, mode)
        sys.exit(0 if code == 0 else 1)
    script, outdir = sys.argv[2], sys.argv[3]
    verify = os.path.join(SKILL, "examples", "verify_glb.py")
    for s, mode in ((script, "export"), (verify, "verify"), (script, "final")):
        code = run(s, [mode, outdir], outdir, mode)
        if code != 0:
            sys.exit("chain stopped at %s" % mode)


if __name__ == "__main__":
    main()
