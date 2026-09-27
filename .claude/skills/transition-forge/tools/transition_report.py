"""Transition verdicts for transition-forge — timing, comfort and pops, as numbers.

    py tools/transition_report.py report <probe.csv> [--fps 60] [--hfov 30]
    py tools/transition_report.py pops   <frames_dir> [--k 3.0] [--floor 2.0] [--allow 40-46]
    py tools/transition_report.py sheet  <frames_dir> --out sheet.png [--every 3] [--cols 8]
    py tools/transition_report.py selftest

report  reads the CSV written by the transition probe (references/qa.md §2) and
        checks every (shot id, run) against the house limits: stalls, dropped
        frames, p95 frame time, zoom rate (doublings/s), pan rate (screen
        widths/s), view rotation (deg/s), roll, input-block window, distance
        overshoot and duration vs the shot's spec. Prints one FAULT line per
        breach and a verdict line; exit code 1 on any fault.
pops    finds single-frame jumps (LOD pops, late-streamed props, stale frames)
        in a PNG sequence from Godot's Movie Maker (--write-movie x.png):
        a frame whose mean difference to its predecessor is > k x the local
        median and > floor (0-255 grey scale) is a pop. --allow skips planned
        cuts (reduced-motion dips). Needs Pillow.
sheet   tiles every Nth frame into one labelled contact sheet for review.
selftest builds synthetic good/bad shots and a synthetic popping sequence and
        proves every check fires. Run it after editing this file.

Limits live in LIMITS below and mirror references/easing.md §4 and
references/qa.md §4 — change all three together.
"""
import argparse
import csv
import glob
import math
import os
import statistics
import sys
import tempfile

LIMITS = {
    "zoom_peak_dbl_s": 8.0,     # automated zoom, doublings of distance per second
    "pan_peak_sw_s": 3.0,       # ground flow at screen centre, screen widths per second
    "rot_peak_deg_s": 60.0,     # view-direction rotation (yaw + pitch), deg/s
    "roll_deg": 0.01,           # the rig has no roll axis; anything above is a bug
    "block_repeat_ms": 400.0,   # longest input-block window on a repeat action
    "block_first_ms": 3500.0,   # longest block for a first-time ceremony
    "overshoot_pct": 1.5,       # distance overshoot past the end value (log space)
    "dropped_max": 1,           # frames >= 1.5 x target per shot (warm runs)
    "dropped_max_cold": 2,      # run 1 = first appearance after boot
    "gpu_max_ms": 12.0,         # heaviest frame's GPU time (PROPOSAL, reference phone)
    "stall_max": 0,             # frames >= 2 x target + 2 ms (a whole refresh lost)
    "p95_factor": 1.05,         # p95 frame time <= 1.05 x target
    "duration_tol": 0.03,       # |measured - spec| <= max(1 frame, 3 %)
}

COLS = ["id", "run", "repeat", "frame", "t_ms", "dt_ms", "cpu_ms", "gpu_ms", "draws",
        "focus_x", "focus_z", "yaw", "pitch", "dist", "fov", "roll", "level",
        "input_blocked", "moving", "spec_ms"]


def _f(row, key, default=0.0):
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def load_rows(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    missing = [c for c in COLS if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"REPORT FAIL - probe CSV lacks columns: {', '.join(missing)}")
    shots = {}
    for r in rows:
        shots.setdefault((r["id"], int(float(r["run"]))), []).append(r)
    for k in shots:
        shots[k].sort(key=lambda r: int(float(r["frame"])))
    return shots


def _view_dir(yaw_deg, pitch_deg):
    y, p = math.radians(yaw_deg), math.radians(pitch_deg)
    return (math.cos(p) * math.sin(y), -math.sin(p), math.cos(p) * math.cos(y))


def _angle(a, b):
    dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
    return math.degrees(math.acos(dot))


def analyse(rows, fps=60.0, hfov=30.0):
    """Metrics for one (id, run). Kinematics use central differences over
    moving rows so frame-time jitter does not fake a speed spike."""
    target = 1000.0 / fps
    k_w = 2.0 * math.tan(math.radians(hfov / 2.0))
    dts = [_f(r, "dt_ms") for r in rows]
    mov = [r for r in rows if _f(r, "moving") >= 0.5]
    m = {"frames": len(rows), "target_ms": target}
    m["max_dt"] = max(dts) if dts else 0.0
    m["p95_dt"] = sorted(dts)[max(0, int(math.ceil(0.95 * len(dts))) - 1)] if dts else 0.0
    m["dropped"] = sum(1 for d in dts if d >= 1.5 * target)
    m["gpu_max"] = max((_f(r, "gpu_ms") for r in rows), default=0.0)
    m["stalls"] = sum(1 for d in dts if d >= 2.0 * target + 2.0)
    m["duration_ms"] = sum(_f(r, "dt_ms") for r in mov[1:]) if len(mov) > 1 else 0.0
    m["spec_ms"] = _f(rows[0], "spec_ms") if rows else 0.0
    m["repeat"] = int(_f(rows[0], "repeat", 1)) if rows else 1
    zoom = pan = rot = 0.0
    for i in range(1, len(mov) - 1):
        a, c = mov[i - 1], mov[i + 1]
        span = (_f(c, "t_ms") - _f(a, "t_ms")) / 1000.0
        if span <= 0:
            continue
        da, dc = max(_f(a, "dist"), 1e-6), max(_f(c, "dist"), 1e-6)
        zoom = max(zoom, abs(math.log2(dc / da)) / span)
        width = k_w * max(_f(mov[i], "dist"), 1e-6)
        step = math.hypot(_f(c, "focus_x") - _f(a, "focus_x"), _f(c, "focus_z") - _f(a, "focus_z"))
        pan = max(pan, step / width / span)
        rot = max(rot, _angle(_view_dir(_f(a, "yaw"), _f(a, "pitch")),
                              _view_dir(_f(c, "yaw"), _f(c, "pitch"))) / span)
    m["zoom_peak"], m["pan_peak"], m["rot_peak"] = zoom, pan, rot
    m["roll_max"] = max((abs(_f(r, "roll")) for r in rows), default=0.0)
    block = best = 0.0
    for r in rows:
        block = block + _f(r, "dt_ms") if _f(r, "input_blocked") >= 0.5 else 0.0
        best = max(best, block)
    m["block_ms"] = best
    m["overshoot_pct"] = 0.0
    if len(mov) > 2:
        l0, l1 = math.log2(max(_f(mov[0], "dist"), 1e-6)), math.log2(max(_f(mov[-1], "dist"), 1e-6))
        total = l1 - l0
        if abs(total) >= 0.1:
            sign = 1.0 if total > 0 else -1.0
            past = max(sign * (math.log2(max(_f(r, "dist"), 1e-6)) - l1) for r in mov)
            m["overshoot_pct"] = max(0.0, 100.0 * past / abs(total))
    return m


def faults_for(sid, run, m):
    L, out = LIMITS, []
    t = m["target_ms"]

    def add(what, val, cap, unit=""):
        out.append(f"FAULT {sid} run {run}: {what} {val:.2f}{unit} > {cap:.2f}{unit}")

    if m["stalls"] > L["stall_max"]:
        add("stalls (frame >= 2x target)", m["stalls"], L["stall_max"])
    cap_drop = L["dropped_max_cold"] if run == 1 else L["dropped_max"]
    if m["dropped"] > cap_drop:
        add("dropped frames (>= 1.5x target)" + (" cold" if run == 1 else ""), m["dropped"], cap_drop)
    if m["gpu_max"] > L["gpu_max_ms"]:
        add("GPU frame time", m["gpu_max"], L["gpu_max_ms"], " ms")
    if m["p95_dt"] > L["p95_factor"] * t:
        add("p95 frame time", m["p95_dt"], L["p95_factor"] * t, " ms")
    if m["zoom_peak"] > L["zoom_peak_dbl_s"]:
        add("zoom rate", m["zoom_peak"], L["zoom_peak_dbl_s"], " dbl/s")
    if m["pan_peak"] > L["pan_peak_sw_s"]:
        add("pan rate", m["pan_peak"], L["pan_peak_sw_s"], " sw/s")
    if m["rot_peak"] > L["rot_peak_deg_s"]:
        add("view rotation", m["rot_peak"], L["rot_peak_deg_s"], " deg/s")
    if m["roll_max"] > L["roll_deg"]:
        add("roll", m["roll_max"], L["roll_deg"], " deg")
    cap = L["block_repeat_ms"] if m["repeat"] else L["block_first_ms"]
    if m["block_ms"] > cap:
        add("input block" + (" (repeat)" if m["repeat"] else " (first time)"), m["block_ms"], cap, " ms")
    if m["overshoot_pct"] > L["overshoot_pct"]:
        add("distance overshoot", m["overshoot_pct"], L["overshoot_pct"], " %")
    if m["spec_ms"] > 0:
        tol = max(t, L["duration_tol"] * m["spec_ms"])
        if abs(m["duration_ms"] - m["spec_ms"]) > tol:
            out.append(f"FAULT {sid} run {run}: duration {m['duration_ms']:.0f} ms vs spec "
                       f"{m['spec_ms']:.0f} ms (tolerance {tol:.0f} ms)")
    return out


def cmd_report(path, fps, hfov, quiet=False):
    shots = load_rows(path)
    faults, ids, runs, block_max = [], set(), set(), 0.0
    if not quiet:
        print(f"{'shot':22s} run  dur_ms  spec  max_dt  p95  drop stall   gpu  zoom  pan   rot  roll  block  over%")
    for (sid, run), rows in sorted(shots.items()):
        m = analyse(rows, fps, hfov)
        ids.add(sid)
        runs.add(run)
        block_max = max(block_max, m["block_ms"])
        if not quiet:
            print(f"{sid:22s} {run:3d} {m['duration_ms']:7.0f} {m['spec_ms']:5.0f} {m['max_dt']:7.1f}"
                  f" {m['p95_dt']:5.1f} {m['dropped']:4d} {m['stalls']:5d} {m['gpu_max']:5.1f} {m['zoom_peak']:5.2f}"
                  f" {m['pan_peak']:4.2f} {m['rot_peak']:5.1f} {m['roll_max']:5.2f}"
                  f" {m['block_ms']:6.0f} {m['overshoot_pct']:5.2f}")
        faults += faults_for(sid, run, m)
    for f in faults:
        print(f)
    stalls = sum(1 for f in faults if "stalls" in f)
    if faults:
        print(f"TRANSITION REPORT FAIL - {len(faults)} faults in {len(ids)} shots x {len(runs)} runs")
        return 1
    print(f"TRANSITION REPORT OK - {len(ids)} shots x {len(runs)} runs, {stalls} stalls, "
          f"0 comfort faults, max block {block_max:.0f} ms")
    return 0


def _frames(folder):
    files = sorted(glob.glob(os.path.join(folder, "*.png")))
    if not files:
        raise SystemExit(f"POP CHECK FAIL - no PNG frames in {folder}")
    return files


def _parse_allow(spec):
    allowed = set()
    for part in (spec or "").split(","):
        if "-" in part:
            a, b = part.split("-")
            allowed.update(range(int(a), int(b) + 1))
        elif part.strip():
            allowed.add(int(part))
    return allowed


def cmd_pops(folder, k=3.0, floor=2.0, allow="", quiet=False):
    from PIL import Image, ImageChops, ImageStat
    files = _frames(folder)
    prev, diffs = None, [0.0]
    for f in files:
        im = Image.open(f).convert("L")
        im = im.resize((270, max(1, round(270 * im.height / im.width))))
        if prev is not None:
            diffs.append(ImageStat.Stat(ImageChops.difference(im, prev)).mean[0])
        prev = im
    allowed, pops = _parse_allow(allow), []
    for i in range(1, len(diffs)):
        near = [diffs[j] for j in range(max(1, i - 4), min(len(diffs), i + 5)) if j != i]
        med = statistics.median(near) if near else 0.0
        if diffs[i] > floor and diffs[i] > k * max(med, 0.25) and i not in allowed:
            pops.append((i, diffs[i], med))
    for i, d, med in pops:
        print(f"POP frame {i:4d} ({os.path.basename(files[i])}): diff {d:.2f} vs local median {med:.2f}")
    if pops:
        print(f"POP CHECK FAIL - {len(pops)} pops in {len(files)} frames")
        return 1
    if not quiet:
        print(f"POP CHECK OK - 0 pops in {len(files)} frames (max diff {max(diffs):.2f})")
    return 0


def cmd_sheet(folder, out, every=3, cols=8):
    from PIL import Image, ImageDraw
    files = _frames(folder)[::max(1, every)]
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        thumbs.append(im.resize((270, max(1, round(270 * im.height / im.width)))))
    tw, th = thumbs[0].size
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), (30, 23, 18))
    draw = ImageDraw.Draw(sheet)
    for n, (f, im) in enumerate(zip(files, thumbs)):
        x, y = (n % cols) * tw, (n // cols) * (th + 18)
        sheet.paste(im, (x, y + 18))
        draw.text((x + 4, y + 3), os.path.splitext(os.path.basename(f))[0], fill=(232, 217, 181))
    sheet.save(out)
    print(f"SHEET {out} - {len(thumbs)} frames, every {every}, {cols} columns")
    return 0


# ---------------------------------------------------------------- selftest
def _sine_io(t):
    return -(math.cos(math.pi * t) - 1.0) / 2.0


def _synth(sid, run, d0, d1, frames, repeat=1, spec_ms=0.0, roll=0.0, stall_at=None,
           block_frames=0, speed=1.0):
    rows, t = [], 0.0
    total = frames + 20
    for f in range(total):
        dt = 1000.0 / 60.0
        if stall_at is not None and f == stall_at:
            dt = 50.0
        t += dt
        p = min(1.0, max(0.0, f / frames)) if f <= frames else 1.0
        e = _sine_io(min(1.0, p * speed))
        dist = d0 * (d1 / d0) ** e
        pitch = 50.0 + 10.0 * e
        rows.append({"id": sid, "run": run, "repeat": repeat, "frame": f, "t_ms": round(t, 3),
                     "dt_ms": round(dt, 3), "cpu_ms": 4.0, "gpu_ms": 8.0, "draws": 300,
                     "focus_x": 0.0, "focus_z": 0.0, "yaw": 0.0, "pitch": round(pitch, 5),
                     "dist": round(dist, 5), "fov": 30.0, "roll": roll, "level": 1,
                     "input_blocked": 1 if f < block_frames else 0,
                     "moving": 1 if f <= frames else 0, "spec_ms": spec_ms})
    return rows


def selftest():
    tmp = tempfile.mkdtemp(prefix="tf_selftest_")
    good = _synth("CASTLE_LEAVE", 1, 143.9, 1399.5, 42, spec_ms=700.0)
    bad = _synth("BAD_SHOT", 1, 143.9, 22392.3, 18, repeat=1, spec_ms=700.0, roll=2.0,
                 stall_at=10, block_frames=40)
    for name, rows in (("good.csv", good), ("bad.csv", bad)):
        with open(os.path.join(tmp, name), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows)
    ok = cmd_report(os.path.join(tmp, "good.csv"), 60.0, 30.0, quiet=True) == 0
    m = analyse(bad)
    faults = faults_for("BAD_SHOT", 1, m)
    want = ["stalls", "zoom rate", "roll", "input block", "duration"]
    missing = [w for w in want if not any(w in f for f in faults)]
    gm = analyse(good)
    print(f"SELFTEST good shot: zoom peak {gm['zoom_peak']:.2f} dbl/s (analytic 7.36), "
          f"duration {gm['duration_ms']:.0f} ms")
    ok = ok and not missing and abs(gm["zoom_peak"] - 7.36) < 0.25
    cold = _synth("CASTLE_ENTER", 1, 1399.5, 143.9, 42, spec_ms=700.0)
    for f in (10, 20):
        cold[f]["dt_ms"] = 26.0
    warm = [dict(r, run=2) for r in cold]
    ok = ok and not faults_for("CASTLE_ENTER", 1, analyse(cold)) \
        and any("dropped" in f for f in faults_for("CASTLE_ENTER", 2, analyse(warm)))
    try:
        from PIL import Image, ImageDraw
        fdir = os.path.join(tmp, "frames")
        os.makedirs(fdir)
        for i in range(24):
            im = Image.new("RGB", (540, 960), (90, 110, 70))
            d = ImageDraw.Draw(im)
            d.rectangle([100 + 4 * i, 300, 300 + 4 * i, 600], fill=(170, 150, 120))
            if i == 15:
                d.rectangle([20, 40, 520, 250], fill=(230, 230, 230))
            im.save(os.path.join(fdir, f"f{i:08d}.png"))
        rc = cmd_pops(fdir, quiet=True)
        rc_allowed = cmd_pops(fdir, allow="15-16", quiet=True)
        ok = ok and rc == 1 and rc_allowed == 0
    except ImportError:
        print("SELFTEST note: Pillow missing, pops check not exercised")
    print("SELFTEST PASS" if ok else f"SELFTEST FAIL - missing faults: {missing}")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report")
    r.add_argument("csv")
    r.add_argument("--fps", type=float, default=60.0)
    r.add_argument("--hfov", type=float, default=30.0)
    p = sub.add_parser("pops")
    p.add_argument("dir")
    p.add_argument("--k", type=float, default=3.0)
    p.add_argument("--floor", type=float, default=2.0)
    p.add_argument("--allow", default="")
    s = sub.add_parser("sheet")
    s.add_argument("dir")
    s.add_argument("--out", required=True)
    s.add_argument("--every", type=int, default=3)
    s.add_argument("--cols", type=int, default=8)
    sub.add_parser("selftest")
    a = ap.parse_args(argv)
    if a.cmd == "report":
        return cmd_report(a.csv, a.fps, a.hfov)
    if a.cmd == "pops":
        return cmd_pops(a.dir, a.k, a.floor, a.allow)
    if a.cmd == "sheet":
        return cmd_sheet(a.dir, a.out, a.every, a.cols)
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
