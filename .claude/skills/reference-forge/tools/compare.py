"""Side-by-side for gap analysis: our render (left, large) vs references.

    py compare.py <our_render.png> <refs_dir> --out <compare.png> [--pick 1,3,5]

The critic LOOKS at this image and scores the gaps (analysis.md). Pick the
references closest in class and angle; four is plenty.
"""
import argparse
import json
import os

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ours")
    ap.add_argument("refs_dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pick", default="")
    a = ap.parse_args()
    with open(os.path.join(a.refs_dir, "refs.json"), encoding="utf-8") as fh:
        refs = [r for r in json.load(fh) if os.path.isfile(r.get("path", ""))]
    if a.pick:
        idx = [int(x) - 1 for x in a.pick.split(",") if x.strip()]
        refs = [refs[i] for i in idx if 0 <= i < len(refs)]
    refs = refs[:4]
    H, R = 900, 440
    ours = Image.open(a.ours).convert("RGB")
    ours.thumbnail((H, H))
    cols = 2
    rows = max(1, (len(refs) + 1) // 2)
    W = H + cols * R
    img = Image.new("RGB", (W, max(H, rows * (R + 30)) + 40), (24, 20, 16))
    d = ImageDraw.Draw(img)
    img.paste(ours, ((H - ours.width) // 2, 40 + (H - ours.height) // 2))
    d.text((10, 10), "OURS: " + os.path.basename(a.ours), fill=(240, 210, 140))
    for i, r in enumerate(refs):
        im = Image.open(r["path"]).convert("RGB")
        im.thumbnail((R - 10, R - 10))
        x = H + (i % cols) * R
        y = 40 + (i // cols) * (R + 30)
        img.paste(im, (x + (R - im.width) // 2, y))
        m = r.get("measure_cm") or {}
        dims = " ".join("%s%g" % (k[0], v) for k, v in m.items())
        d.text((x + 6, y + R - 6), "REF %d: %s  %s" % (i + 1, (r.get("title") or "")[:26], dims),
               fill=(222, 196, 134))
    img.save(a.out)
    print("COMPARE " + a.out)


if __name__ == "__main__":
    main()
