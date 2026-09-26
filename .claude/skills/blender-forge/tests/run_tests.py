"""blender-forge regression suite — ONE command, well under 5 minutes:

    py tools/forge_run.py run tests/run_tests.py test <outdir> [-k <substring>]

Each test runs in a fresh factory scene and prints one line:
    PASS <module>.<test> (<seconds>s)      or      FAIL <module>.<test>: <reason>
The last line is 'PASS all N tests in S s' or 'FAIL k/N tests ...'; the Blender
exit code is 1 on any failure, so forge_run reports it.

FORGE_LIB is honoured (the runner presets it; the skill-engineer points it at a
STAGED copy of lib/ and swaps lib/forge.py only when this suite is green).
"""
import sys, os, time, traceback, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib")
sys.path.insert(0, LIB)
sys.path.insert(0, HERE)
import bpy
import forge as F
import _util as U

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(HERE, "out")
KEY = argv[argv.index("-k") + 1] if "-k" in argv else ""
os.makedirs(OUT, exist_ok=True)
U.OUT = OUT

MODULES = ["test_forms", "test_materials", "test_tiers", "test_bake", "test_render", "test_operators"]

print("TEST blender %s  lib %s  out %s" % (bpy.app.version_string, os.path.abspath(F.__file__), OUT))
results, t_all = [], time.time()
for modname in MODULES:
    if not os.path.isfile(os.path.join(HERE, modname + ".py")):
        continue
    try:
        mod = importlib.import_module(modname)
    except Exception as e:                      # a module that cannot import is a failure
        results.append((modname, False))
        print("FAIL %s: import: %s: %s" % (modname, type(e).__name__, e), flush=True)
        continue
    for name in sorted(n for n in dir(mod) if n.startswith("test_")):
        full = "%s.%s" % (modname, name)
        if KEY and KEY not in full:
            continue
        F.reset_scene()
        t0 = time.time()
        try:
            note = getattr(mod, name)()
            dt = time.time() - t0
            results.append((full, True))
            print("PASS %s (%.1fs)%s" % (full, dt, ("  " + str(note)) if note else ""), flush=True)
        except Exception as e:  # AssertionError or a library crash — both are failures
            results.append((full, False))
            frames = traceback.extract_tb(e.__traceback__)
            tb = next((f for f in reversed(frames) if not f.filename.endswith("_util.py")), frames[-1])
            print("FAIL %s: %s: %s  [%s:%d]" % (full, type(e).__name__, e,
                                               os.path.basename(tb.filename), tb.lineno), flush=True)
failed = [n for n, ok in results if not ok]
dt = time.time() - t_all
if failed:
    print("FAIL %d/%d tests in %.0fs: %s" % (len(failed), len(results), dt, ", ".join(failed)), flush=True)
    sys.exit(1)
print("PASS all %d tests in %.0fs" % (len(results), dt), flush=True)
sys.exit(0)
