"""Tile N labelled PNGs into one comparison sheet (Pillow; runs outside Blender).

    py tools/rarity_sheet.py <out.png> <img> [<img> ...] [--labels a,b,...]
                             [--cols N] [--tile PX] [--title TEXT] [--thumb PX]

- Labels default to the tier/variant parsed from each filename
  (sunforged_legendary.png -> LEGENDARY). A label that names a tier gets that
  tier's body colour as an accent bar — read from lib/forge.py TIERS, so the
  sheet always shows the calibrated colours (single source of truth).
- --thumb PX adds a second row of PX-sized thumbnails: the half-second read
  test (qa.md #9: the tier must read from rim + glow colour alone).
- Prints: SHEET <path> <w>x<h> tiles=<n>
"""
import ast
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FORGE = os.path.join(os.environ.get("FORGE_LIB") or os.path.join(HERE, "..", "lib"), "forge.py")
BG, FG, DIM = (11, 12, 16), (232, 228, 220), (120, 118, 112)


def tier_colours(path=FORGE):
    """TIERS[*]['body'] from forge.py without importing bpy."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "TIERS" for t in node.targets):
                tiers = eval(compile(ast.Expression(node.value), path, "eval"), {"__builtins__": {}, "dict": dict})
                return {k: v.get("body", "#808080") for k, v in tiers.items()}
    except Exception as e:  # never fail a sheet over colours
        print("rarity_sheet: TIERS not read (%s); neutral accents" % e)
    return {}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(px, bold=True):
    names = (["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"] if bold else
             ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"])
    for n in names:
        try:
            return ImageFont.truetype(n, px)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=px)
    except TypeError:
        return ImageFont.load_default()


def label_from(path, tiers):
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    for t in tiers:
        if t in stem.split("_") or stem.endswith(t):
            return t.upper()
    return stem.split("_", 1)[-1].upper()


def build(out, paths, labels=None, cols=None, tile=None, title=None, thumb=0):
    tiers = tier_colours()
    imgs = [Image.open(p).convert("RGB") for p in paths]
    n = len(imgs)
    cols = cols or n
    rows = (n + cols - 1) // cols
    tile = tile or imgs[0].width
    labels = labels or [label_from(p, tiers) for p in paths]
    pad, bar = max(8, tile // 48), max(30, tile // 14)
    head = (bar + pad) if title else 0
    thumb_h = (thumb + pad * 2 + bar // 2) if thumb else 0
    W = cols * tile + (cols + 1) * pad
    H = head + rows * (tile + bar + pad) + pad + thumb_h
    sheet = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(sheet)
    f_lab, f_title, f_small = font(int(bar * 0.52)), font(int(bar * 0.62)), font(max(10, int(bar * 0.36)), False)
    if title:
        dr.text((pad, pad // 2 + 2), title, fill=FG, font=f_title)
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (tile + pad)
        y = head + pad + r * (tile + bar + pad)
        sheet.paste(im.resize((tile, tile), Image.LANCZOS) if im.size != (tile, tile) else im, (x, y))
        acc = hex_rgb(tiers[lab.lower()]) if lab.lower() in tiers else DIM
        dr.rectangle([x, y + tile, x + tile - 1, y + tile + 4], fill=acc)
        dr.text((x + 6, y + tile + 7), lab, fill=FG, font=f_lab)
    if thumb:
        y0 = head + pad + rows * (tile + bar + pad)
        dr.text((pad, y0), "%d px read test" % thumb, fill=DIM, font=f_small)
        y0 += bar // 2
        for i, (im, lab) in enumerate(zip(imgs, labels)):
            x = pad + i * (thumb + pad)
            if x + thumb > W:
                break
            sheet.paste(im.resize((thumb, thumb), Image.LANCZOS), (x, y0))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out, optimize=True)
    print("SHEET %s %dx%d tiles=%d" % (out, W, H, n))
    return out


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    opts, files, i = {}, [], 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            opts[a[2:]] = argv[i + 1]; i += 2
        else:
            files.append(a); i += 1
    out, paths = files[0], files[1:]
    if not paths:
        sys.exit("rarity_sheet: no input images")
    build(out, paths,
          labels=opts["labels"].split(",") if "labels" in opts else None,
          cols=int(opts["cols"]) if "cols" in opts else None,
          tile=int(opts["tile"]) if "tile" in opts else None,
          title=opts.get("title"),
          thumb=int(opts.get("thumb", 0)))


if __name__ == "__main__":
    main(sys.argv[1:])
