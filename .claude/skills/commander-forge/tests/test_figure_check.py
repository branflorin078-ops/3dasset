"""Unit tests for tools/figure_check.py on synthetic images (no Blender).

    py tests/test_figure_check.py        ->  PASS all N tests
"""
import os
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import figure_check as FC  # noqa: E402

W, H = 400, 500


def _figure(path, warm_rim=False, flat=False):
    """A standing 'lord': cloak body, lit face, a spear held off the body
    (the gap between arm and spear is a negative-space window), rim on the right."""
    im = Image.new("RGB", (W, H), (14, 12, 12))
    mk = Image.new("L", (W, H), 0)
    d, dm = ImageDraw.Draw(im), ImageDraw.Draw(mk)
    body = [(140, 150), (260, 150), (300, 470), (100, 470)]
    face = (170, 60, 230, 140)
    if flat:                                   # the empty figurine: one value, no break-up
        d.ellipse((110, 50, 290, 470), fill=(92, 88, 84))
        dm.ellipse((110, 50, 290, 470), fill=255)
        im.save(path)
        mk.save(path[:-4] + "_mask.png")
        return None
    d.polygon(body, fill=(128, 98, 80))                               # lit cloak (mid band)
    d.polygon([(200, 150), (260, 150), (300, 470), (200, 470)], fill=(40, 32, 28))   # shadow side (dark band)
    d.ellipse(face, fill=(214, 168, 140))
    d.rectangle((255, 200, 330, 215), fill=(80, 60, 50))          # arm out to the spear
    d.rectangle((330, 45, 338, 468), fill=(120, 100, 70))          # spear shaft
    d.rectangle((280, 430, 330, 445), fill=(80, 60, 50))           # lower hand on the shaft
    rim = (255, 214, 140) if warm_rim else (200, 200, 205)
    d.line([(257, 152), (297, 470)], fill=rim, width=4)             # rim just inside the right edge
    for shape in (body, [(255, 200), (330, 200), (330, 215), (255, 215)],
                  [(280, 430), (330, 430), (330, 445), (280, 445)],
                  [(330, 45), (338, 45), (338, 468), (330, 468)]):
        dm.polygon(shape, fill=255)
    dm.ellipse(face, fill=255)
    im.save(path)
    mk.save(path[:-4] + "_mask.png")
    return [face[0] / W, face[1] / H, face[2] / W, face[3] / H]


def test_good_figure_passes_core_checks(tmp):
    p = os.path.join(tmp, "good.png")
    face = _figure(p)
    r, kind = FC.measure(p, face=face, kind="figure")
    rows, fails = FC.judge(r, kind)
    bad = [row for row in rows if row[4] == "FAIL"]
    assert r["windows_128"] >= 1, r["windows_128"]
    assert 0.45 <= r["solidity_128"] <= 0.82, r["solidity_128"]
    assert r["sep_dL"] >= 15, r["sep_dL"]
    assert r["face_minus_body_L"] > 20, r["face_minus_body_L"]
    assert not [b for b in bad if b[0] in ("sep_dL", "windows_128", "solidity_128", "band_max")], bad


def test_empty_figurine_fails(tmp):
    p = os.path.join(tmp, "flat.png")
    _figure(p, flat=True)
    r, kind = FC.measure(p, kind="figure")
    rows, fails = FC.judge(r, kind)
    failed = {row[0] for row in rows if row[4] == "FAIL"}
    assert {"band_max", "windows_128", "solidity_128"} <= failed, failed
    assert fails >= 3


def test_sworn_pair_reads(tmp):
    a, b = os.path.join(tmp, "sworn.png"), os.path.join(tmp, "unsworn.png")
    _figure(a, warm_rim=True)
    _figure(b, warm_rim=False)
    dl = FC.sworn_delta(a, b)
    assert dl["sworn_db"] > 5.0, dl
    same = FC.sworn_delta(b, b)
    assert abs(same["sworn_dL"]) < 1e-6 and abs(same["sworn_db"]) < 1e-6, same


def test_lab_anchors():
    L, a, b = FC.srgb_to_lab(np.array([[[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.5, 0.5, 0.5]]]))
    assert abs(L[0, 0] - 100) < 0.5 and abs(L[0, 1]) < 0.5 and abs(L[0, 2] - 53.4) < 0.6, L
    assert abs(a[0, 2]) < 0.5 and abs(b[0, 2]) < 0.5


def test_solidity_and_windows_basics():
    disc = np.zeros((64, 64), bool)
    yy, xx = np.mgrid[:64, :64]
    disc[(yy - 32) ** 2 + (xx - 32) ** 2 < 400] = True
    assert FC.solidity(disc) > 0.9
    ring = disc & ~((yy - 32) ** 2 + (xx - 32) ** 2 < 100)
    assert FC.windows(ring) == 1


def test_lineup_flags_twins(tmp):
    a, b, c = (os.path.join(tmp, n + "_mask.png") for n in ("a", "b", "c"))
    for path, box in ((a, (40, 10, 80, 190)), (b, (42, 12, 82, 192))):
        im = Image.new("L", (120, 200), 0)
        ImageDraw.Draw(im).rectangle(box, fill=255)
        im.save(path)
    im = Image.new("L", (120, 200), 0)
    d = ImageDraw.Draw(im)
    d.rectangle((50, 60, 70, 190), fill=255)
    d.line([(20, 10), (100, 190)], fill=255, width=6)          # a diagonal pole: a different shape
    im.save(c)
    rows = {(x, y): v for x, y, v in FC.lineup([a, b, c])}
    assert rows[("a_mask.png", "b_mask.png")] > 0.8, rows
    assert rows[("a_mask.png", "c_mask.png")] < 0.8, rows


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for n, f in tests:
            try:
                f(tmp) if f.__code__.co_argcount else f()
                print("TEST", n, "ok")
            except AssertionError as e:
                failed += 1
                print("FAIL", n, e)
    print("PASS all %d tests" % len(tests) if not failed else "FAIL %d of %d" % (failed, len(tests)))
    sys.exit(1 if failed else 0)
