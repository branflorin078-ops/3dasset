"""figure_check.py - measure a lord render or painting against the commander-forge
quality bar (references/qa.md). Plain Python + Pillow + numpy; no Blender.

    py tools/figure_check.py <image.png> [--mask m.png] [--face x0,y0,x1,y1]
                             [--kind bust|figure|token] [--rim right|left|none]
                             [--sheet out.png] [--json out.json]

- Mask: --mask, else <stem>_mask.png (figure_kit.render_with_mask), else the
  image's own alpha, else a border key (approximate - printed as such).
- Face box (image fractions, y down): --face, else <stem>_meta.json
  (figure_kit.write_meta). Paintings: pass --face by hand.
- Prints one line per check:  CHECK <name> <value> <op> <target> PASS|FAIL|INFO
  then:                        FIGURE_CHECK <file> kind=<k> pass=<n> fail=<m>
- Exit code 1 when any check FAILS (so a chain stops on a red figure).
Thresholds are PROPOSALS until calibrated on the first approved lord
(qa.md section 6 records the calibrated values).
"""
import argparse
import json
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

# kind -> {check: (op, target)}   (PROPOSAL thresholds, qa.md section 6)
TARGETS = {
    "bust": {
        "fill_h": (">=", 0.85), "sep_dL": (">=", 15.0), "sep_dL_128": (">=", 12.0),
        "band_dark": (">=", 0.08), "band_mid": (">=", 0.15), "band_light": (">=", 0.05),
        "band_max": ("<=", 0.75), "rim_ratio": (">=", 1.10),
        "face_minus_body_L": (">=", 5.0), "face_clip": ("<=", 0.02),
        "face_chroma": ("range", (10.0, 40.0)), "face_px_128": (">=", 32.0),
        "face_detail_ratio": (">=", 0.90),
    },
    "figure": {
        "fill_h": ("range", (0.78, 0.92)), "solidity_128": ("range", (0.45, 0.82)),
        "windows_128": (">=", 1), "sep_dL": (">=", 15.0), "sep_dL_128": (">=", 12.0),
        "band_dark": (">=", 0.08), "band_mid": (">=", 0.15), "band_light": (">=", 0.05),
        "band_max": ("<=", 0.75), "rim_ratio": (">=", 1.10),
        "face_minus_body_L": (">=", 3.0), "face_clip": ("<=", 0.02),
        "face_chroma": ("range", (10.0, 40.0)), "face_px_256": (">=", 24.0),
    },
    "token": {
        "sep_dL_128": (">=", 18.0), "solidity_128": ("range", (0.40, 0.85)),
    },
}


# ------------------------------------------------------------------ colour
def srgb_to_lab(rgb):
    """rgb: float array (..., 3) in 0..1 sRGB -> CIE L*, a*, b* (D65)."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return L, a, b


# ------------------------------------------------------------------ masks
def load_mask(path, img_rgba, explicit=None):
    stem = os.path.splitext(path)[0]
    for cand in ([explicit] if explicit else []) + [stem + "_mask.png"]:
        if cand and os.path.isfile(cand):
            m = Image.open(cand).convert("RGBA").resize(img_rgba.size, Image.BILINEAR)
            a = np.asarray(m, np.float32)[..., 3] / 255.0
            if a.min() < 0.5 < a.max():
                return a > 0.5, "mask:" + os.path.basename(cand)
            g = np.asarray(m.convert("L"), np.float32) / 255.0
            return g > 0.5, "mask(lum):" + os.path.basename(cand)
    a = np.asarray(img_rgba, np.float32)[..., 3] / 255.0
    if a.min() < 0.5 < a.max():
        return a > 0.5, "alpha"
    rgb = np.asarray(img_rgba.convert("RGB"), np.float32) / 255.0
    L, A, B = srgb_to_lab(rgb)
    lab = np.stack([L, A, B], -1)
    bw = max(2, int(0.02 * min(L.shape)))
    border = np.concatenate([lab[:bw].reshape(-1, 3), lab[-bw:].reshape(-1, 3),
                             lab[:, :bw].reshape(-1, 3), lab[:, -bw:].reshape(-1, 3)])
    ref = np.median(border, 0)
    return np.linalg.norm(lab - ref, axis=-1) > 12.0, "border-key(approximate)"


def shrink(m, n):
    """n steps of 4-neighbour erosion."""
    m = m.copy()
    for _ in range(n):
        p = np.pad(m, 1, constant_values=False)
        m = m & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m


def grow(m, n):
    return ~shrink(~m, n)


def resize_mask(m, long_side):
    h, w = m.shape
    s = long_side / max(h, w)
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((max(1, round(w * s)), max(1, round(h * s))),
                                                            Image.BILINEAR)
    return np.asarray(im) > 127


def hull_area(pts):
    """Monotone-chain convex hull area of (x, y) points."""
    pts = sorted(set(map(tuple, pts)))
    if len(pts) < 3:
        return 0.0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    h = lo[:-1] + hi[:-1]
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(h, h[1:] + h[:1])))


def solidity(m):
    """Subject area / convex hull area (pixel corners, so full pixels count)."""
    ys, xs = np.nonzero(m & ~shrink(m, 1))
    if len(xs) == 0:
        return 0.0
    corners = np.concatenate([np.stack([xs + dx, ys + dy], 1) for dx in (0, 1) for dy in (0, 1)])
    ha = hull_area(corners.tolist())
    return float(m.sum() / ha) if ha else 0.0


def windows(m, min_px=4):
    """Enclosed background regions (negative-space windows) not touching the border."""
    bg = ~m
    h, w = bg.shape
    seen = np.zeros_like(bg)
    count = 0
    for y0 in range(h):
        for x0 in range(w):
            if not bg[y0, x0] or seen[y0, x0]:
                continue
            q, size, edge = deque([(y0, x0)]), 0, False
            seen[y0, x0] = True
            while q:
                y, x = q.popleft()
                size += 1
                if y in (0, h - 1) or x in (0, w - 1):
                    edge = True
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if not edge and size >= min_px:
                count += 1
    return count


def blur(a, r=2):
    k = 2 * r + 1
    p = np.pad(a, r, mode="edge")
    c = np.cumsum(np.cumsum(p, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


# ------------------------------------------------------------------ measure
def measure(path, mask_path=None, face=None, kind="bust", rim="right"):
    img = Image.open(path).convert("RGBA")
    rgb = np.asarray(img.convert("RGB"), np.float32) / 255.0
    L, A, B = srgb_to_lab(rgb)
    m, msrc = load_mask(path, img, mask_path)
    meta_p = os.path.splitext(path)[0] + "_meta.json"
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}
    face = face or meta.get("face")
    kind = kind or meta.get("kind", "bust")
    H, W = L.shape
    r = {"mask_source": msrc}
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        raise SystemExit("figure_check: empty subject mask for %s" % path)
    r["fill_h"] = (ys.max() - ys.min() + 1) / H
    r["fill_w"] = (xs.max() - xs.min() + 1) / W
    # value plan of the subject (3 bands of L*)
    Ls = L[m]
    r["band_dark"] = float((Ls < 30).mean())
    r["band_mid"] = float(((Ls >= 30) & (Ls <= 65)).mean())
    r["band_light"] = float((Ls > 65).mean())
    r["band_max"] = max(r["band_dark"], r["band_mid"], r["band_light"])
    # separation at the silhouette edge (full size and at 128 px)
    k = max(2, round(0.006 * max(H, W)))
    inner, outer = m & ~shrink(m, k), grow(m, k) & ~m
    r["sep_dL"] = abs(float(L[inner].mean() - L[outer].mean())) if outer.any() else 0.0
    s128 = Image.fromarray((np.clip(L, 0, 100) * 2.55).astype(np.uint8))
    m128 = resize_mask(m, 128)
    L128 = np.asarray(s128.resize((m128.shape[1], m128.shape[0]), Image.BILINEAR), np.float32) / 2.55
    i1, o1 = m128 & ~shrink(m128, 2), grow(m128, 2) & ~m128
    r["sep_dL_128"] = abs(float(L128[i1].mean() - L128[o1].mean())) if o1.any() and i1.any() else 0.0
    r["solidity_128"] = solidity(m128)
    r["windows_128"] = windows(m128)
    # rim: outer 0..k px band vs the band 2k..4k px inside, on the rim side
    if rim != "none":
        cx = (xs.min() + xs.max()) / 2
        side = (np.arange(W)[None, :] >= cx) if rim == "right" else (np.arange(W)[None, :] < cx)
        edge_b = inner & side
        deep_b = shrink(m, 2 * k) & ~shrink(m, 4 * k) & side
        if edge_b.any() and deep_b.any():
            r["rim_ratio"] = float(L[edge_b].mean() / max(1.0, L[deep_b].mean()))
    # face
    if face:
        x0, y0, x1, y1 = face
        fm = np.zeros_like(m)
        fm[int(y0 * H):int(np.ceil(y1 * H)), int(x0 * W):int(np.ceil(x1 * W))] = True
        fm &= m
        body = m & ~fm
        if fm.any():
            r["face_L"] = float(L[fm].mean())
            r["face_minus_body_L"] = float(L[fm].mean() - (L[body].mean() if body.any() else 0.0))
            r["face_clip"] = float((L[fm] > 92).mean())
            r["face_chroma"] = float(np.hypot(A[fm], B[fm]).mean())
            hp = np.abs(L - blur(L, 2))
            r["face_detail_ratio"] = float(hp[fm].mean() / max(1e-3, hp[body].mean())) if body.any() else 0.0
            r["face_px_128"] = (y1 - y0) * 128.0     # face height with the image 128 px tall
            r["face_px_256"] = (y1 - y0) * 256.0
    return r, kind


def judge(r, kind):
    rows, fails = [], 0
    for name, (op, tgt) in TARGETS.get(kind, {}).items():
        if name not in r:
            continue
        v = r[name]
        if op == ">=":
            ok = v >= tgt
        elif op == "<=":
            ok = v <= tgt
        else:
            ok = tgt[0] <= v <= tgt[1]
        fails += 0 if ok else 1
        rows.append((name, v, op, tgt, "PASS" if ok else "FAIL"))
    for name in sorted(r):
        if name not in TARGETS.get(kind, {}) and name != "mask_source":
            rows.append((name, r[name], "", "", "INFO"))
    return rows, fails


def sheet(path, m, out):
    """Original | 128 px silhouette | 3-band value read | 64 px thumbnail."""
    img = Image.open(path).convert("RGB")
    h = 384
    orig = img.resize((round(img.width * h / img.height), h), Image.LANCZOS)
    m128 = resize_mask(m, 128)
    sil = Image.fromarray(np.where(m128, 0, 235).astype(np.uint8)).convert("RGB")
    sil = sil.resize((round(sil.width * h / sil.height), h), Image.NEAREST)
    L, _, _ = srgb_to_lab(np.asarray(img, np.float32) / 255.0)
    bands = np.select([L < 30, L <= 65], [40, 128], 225).astype(np.uint8)
    val = Image.fromarray(bands).convert("RGB").resize(orig.size, Image.NEAREST)
    th = img.resize((round(img.width * 64 / img.height), 64), Image.LANCZOS)
    tiles = [orig, sil, val, th]
    W = sum(t.width for t in tiles) + 10 * (len(tiles) + 1)
    S = Image.new("RGB", (W, h + 34), (11, 12, 16))
    d = ImageDraw.Draw(S)
    x = 10
    for t, lab in zip(tiles, ("render", "silhouette 128", "value bands", "64 px")):
        S.paste(t, (x, 24))
        d.text((x, 6), lab, fill=(232, 228, 220))
        x += t.width + 10
    S.save(out)
    print("SHEET", out, "%dx%d" % S.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--mask")
    ap.add_argument("--face", help="x0,y0,x1,y1 image fractions, y down")
    ap.add_argument("--kind", choices=sorted(TARGETS))
    ap.add_argument("--rim", default="right", choices=("right", "left", "none"))
    ap.add_argument("--sheet")
    ap.add_argument("--json")
    a = ap.parse_args()
    face = [float(v) for v in a.face.split(",")] if a.face else None
    r, kind = measure(a.image, a.mask, face, a.kind, a.rim)
    rows, fails = judge(r, kind)
    print("MASK", r["mask_source"])
    for name, v, op, tgt, verdict in rows:
        vs = "%.3f" % v if isinstance(v, float) else str(v)
        print("CHECK %-18s %8s %-5s %-14s %s" % (name, vs, op, tgt, verdict))
    npass = sum(1 for row in rows if row[4] == "PASS")
    print("FIGURE_CHECK %s kind=%s pass=%d fail=%d" % (os.path.basename(a.image), kind, npass, fails))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(dict(r, kind=kind, fails=fails), fh, indent=1)
    if a.sheet:
        img = Image.open(a.image).convert("RGBA")
        m, _ = load_mask(a.image, img, a.mask)
        sheet(a.image, m, a.sheet)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
