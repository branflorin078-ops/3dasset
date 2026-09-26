"""Reference search for reference-forge.

    py ref_search.py met   "<query>" --out <dir> [--dept 4] [--n 8] [--from 1100] [--to 1650]
    py ref_search.py cma   "<query>" --out <dir> [--type "Arms and Armor"] [--n 8] [--from 1100] [--to 1650]
    py ref_search.py local "<keywords>" --out <dir> [--n 8]
    py ref_search.py sheet <dir>

met    The Metropolitan Museum Open Access API. ONLY objects flagged
       isPublicDomain (CC0) are kept. Downloads the web-large photo, keeps
       the museum's numeric measurements (cm / kg) for proportion checks,
       writes <dir>/refs.json and a labelled contact sheet <dir>/refs_sheet.png.
       Departments: 4 = Arms and Armor, 17 = Medieval Art, 7 = The Cloisters.
cma    The Cleveland Museum of Art Open Access API — every record it returns
       with cc0=1 is CC0. Second source when the Met is thin (architecture
       fragments, furniture, caskets, textiles, arms). Measurements come as a
       string ("Overall: 30.5 x 25 cm ..."); the first cm triple is kept as
       Height x Width x Depth and the raw string is stored beside it.
local  The owner's reference boards in D:/CastleConquest/real art/ (the game's
       visual source of truth), ranked by filename keyword match. Nothing is
       copied; refs.json points at the originals.
sheet  Rebuild the contact sheet for <dir> from its refs.json.

References are for STUDY: proportions, construction, materials, wear. They
are never traced or reproduced 1:1 — designs stay original (blender-forge rule 1).
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://collectionapi.metmuseum.org/public/collection/v1"
CMA_API = "https://openaccess-api.clevelandart.org/api/artworks/"
REAL_ART = os.environ.get("REAL_ART") or r"D:\CastleConquest\real art"
UA = {"User-Agent": "reference-forge/1.0 (Castle Conquest art research)"}


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _json(url):
    return json.loads(_get(url).decode("utf-8"))


def _clean(s):
    """Museum titles carry HTML (<i>Tsuba</i>) and typographic dashes the
    default sheet font cannot draw."""
    s = re.sub(r"<[^>]+>", "", str(s or ""))
    return s.replace("–", "-").replace("—", "-").replace("’", "'")


def _measure(obj):
    """The museum's structured measurements -> {'Height': cm, ...}."""
    out = {}
    for m in obj.get("measurements") or []:
        for k, v in (m.get("elementMeasurements") or {}).items():
            if k not in out and isinstance(v, (int, float)):
                out[k] = round(float(v), 2)
    return out


def met(query, out, dept=4, n=8, yr_from=None, yr_to=None, scan=120, must=None):
    """`must`: comma-separated class words; an object survives only if one of
    them appears in its title/objectName/classification. Met's keyword search
    is loose ("chapel de fer" returns shield bosses) — the filter is what
    makes the sheet relevant."""
    must = [w.strip().lower() for w in (must or "").split(",") if w.strip()]
    os.makedirs(out, exist_ok=True)
    # `q` MUST BE THE LAST PARAMETER — the Met API silently returns
    # {"total":0} (or a truncated set) when anything follows it. Measured:
    # the same cabasset query gave 28 hits with q last and 0 with q first.
    q = urllib.parse.urlencode({**({"departmentId": dept} if dept else {}),
                                "hasImages": "true", "q": query})
    # The Met search endpoint is intermittent: the same query once returned 4
    # hits and 800 a minute later. Ask up to three times, keep the largest.
    hits = []
    for attempt in range(3):
        try:
            got = _json(API + "/search?" + q).get("objectIDs") or []
        except Exception:
            got = []
        if len(got) > len(hits):
            hits = got
        if len(hits) > 20:
            break
        time.sleep(1.0 + attempt)
    print("MET search '%s' dept=%s -> %d hits" % (query, dept, len(hits)))
    refs = _load(out)
    have = {r.get("id") for r in refs}
    kept = 0
    for oid in hits[:scan]:
        if kept >= n:
            break
        if ("met_%d" % oid) in have:
            continue
        try:
            o = _json("%s/objects/%d" % (API, oid))
        except Exception as e:
            print("  skip %d (%s)" % (oid, e))
            continue
        if not o.get("isPublicDomain") or not o.get("primaryImageSmall"):
            continue
        if must:
            hay = " ".join(str(o.get(k) or "") for k in
                           ("title", "objectName", "classification")).lower()
            if not any(w in hay for w in must):
                continue
        b, e = o.get("objectBeginDate"), o.get("objectEndDate")
        if yr_from and isinstance(e, int) and e < yr_from:
            continue
        if yr_to and isinstance(b, int) and b > yr_to:
            continue
        path = os.path.join(out, "met_%d.jpg" % oid)
        try:
            with open(path, "wb") as fh:
                fh.write(_get(o["primaryImageSmall"], timeout=60))
        except Exception as ex:
            print("  image fail %d (%s)" % (oid, ex))
            continue
        rec = {"id": "met_%d" % oid, "source": "The Met Open Access (CC0)",
               "title": _clean(o.get("title")), "object": _clean(o.get("objectName")),
               "date": _clean(o.get("objectDate")), "culture": _clean(o.get("culture")),
               "medium": _clean(o.get("medium")), "dimensions": _clean(o.get("dimensions")),
               "measure_cm": _measure(o), "url": o.get("objectURL"),
               "path": path}
        refs.append(rec)
        kept += 1
        print("  + %s | %s | %s | %s" % (rec["id"], rec["title"], rec["date"],
                                        rec["measure_cm"] or rec["dimensions"]))
        time.sleep(0.05)
    _save(out, refs)
    sheet(out)
    print("REFS %d kept -> %s" % (kept, out))


_L = r"(?:[a-z]+\.?\s*)?"   # optional "h." / "w." / "d." labels
_CM = re.compile(_L + r"(\d+(?:\.\d+)?)\s*(?:x\s*" + _L + r"(\d+(?:\.\d+)?))?"
                 r"\s*(?:x\s*" + _L + r"(\d+(?:\.\d+)?))?\s*cm", re.I)


def _measure_str(s):
    """'Overall: 30.5 x 25 x 12 cm (12 x 9 13/16 in.)' -> {'Height': 30.5, ...}.
    Museum convention is h x w x d; a single value is kept as Length."""
    m = _CM.search(s or "")
    if not m:
        return {}
    vals = [float(v) for v in m.groups() if v]
    keys = ("Height", "Width", "Depth") if len(vals) > 1 else ("Length",)
    return {k: round(v, 2) for k, v in zip(keys, vals)}


def cma(query, out, n=8, yr_from=None, yr_to=None, must=None, typ=None):
    """Cleveland Museum of Art Open Access (CC0 only via cc0=1)."""
    must = [w.strip().lower() for w in (must or "").split(",") if w.strip()]
    os.makedirs(out, exist_ok=True)
    params = {"q": query, "cc0": 1, "has_image": 1, "limit": 100}
    if typ:
        params["type"] = typ
    try:
        data = _json(CMA_API + "?" + urllib.parse.urlencode(params)).get("data") or []
    except Exception as e:
        print("CMA search failed (%s)" % e)
        data = []
    print("CMA search '%s' type=%s -> %d hits" % (query, typ, len(data)))
    refs = _load(out)
    have = {r.get("id") for r in refs}
    kept = 0
    for o in data:
        if kept >= n:
            break
        rid = "cma_%s" % o.get("id")
        img = ((o.get("images") or {}).get("web") or {}).get("url")
        if rid in have or not img or str(o.get("share_license_status", "CC0")).upper() != "CC0":
            continue
        if must:
            hay = " ".join(str(o.get(k) or "") for k in ("title", "type", "technique")).lower()
            if not any(w in hay for w in must):
                continue
        b, e = o.get("creation_date_earliest"), o.get("creation_date_latest")
        if yr_from and isinstance(e, int) and e < yr_from:
            continue
        if yr_to and isinstance(b, int) and b > yr_to:
            continue
        path = os.path.join(out, rid + ".jpg")
        try:
            with open(path, "wb") as fh:
                fh.write(_get(img, timeout=60))
        except Exception as ex:
            print("  image fail %s (%s)" % (rid, ex))
            continue
        culture = o.get("culture")
        rec = {"id": rid, "source": "Cleveland Museum of Art Open Access (CC0)",
               "title": _clean(o.get("title")), "object": _clean(o.get("type")),
               "date": _clean(o.get("creation_date")),
               "culture": _clean(", ".join(culture) if isinstance(culture, list) else culture),
               "medium": _clean(o.get("technique")), "dimensions": _clean(o.get("measurements")),
               "measure_cm": _measure_str(o.get("measurements")), "url": o.get("url"),
               "path": path}
        refs.append(rec)
        kept += 1
        print("  + %s | %s | %s | %s" % (rec["id"], rec["title"], rec["date"],
                                        rec["measure_cm"] or rec["dimensions"]))
    _save(out, refs)
    sheet(out)
    print("REFS %d kept -> %s" % (kept, out))


def local(keywords, out, n=8):
    os.makedirs(out, exist_ok=True)
    toks = [t for t in re.split(r"[\s_,]+", keywords.lower()) if len(t) > 2]
    scored = []
    for root, _, files in os.walk(REAL_ART):
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            name = f.lower()
            s = sum(1 for t in toks if t in name)
            if s:
                scored.append((s, os.path.join(root, f)))
    scored.sort(key=lambda x: -x[0])
    refs = [r for r in _load(out) if r.get("source") != "owner real art"]
    for s, p in scored[:n]:
        refs.append({"id": "local_" + os.path.splitext(os.path.basename(p))[0][:40],
                     "source": "owner real art", "title": os.path.basename(p),
                     "score": s, "path": p})
        print("  + [%d] %s" % (s, os.path.basename(p)))
    _save(out, refs)
    sheet(out)
    print("REFS local %d -> %s" % (min(n, len(scored)), out))


def _load(out):
    p = os.path.join(out, "refs.json")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    return []


def _save(out, refs):
    with open(os.path.join(out, "refs.json"), "w", encoding="utf-8") as fh:
        json.dump(refs, fh, indent=1, ensure_ascii=False)


def sheet(out, cols=4, cell=300, cap=46):
    from PIL import Image, ImageDraw
    refs = [r for r in _load(out) if os.path.isfile(r.get("path", ""))]
    if not refs:
        return None
    rows = (len(refs) + cols - 1) // cols
    img = Image.new("RGB", (cols * cell, rows * (cell + cap)), (24, 20, 16))
    d = ImageDraw.Draw(img)
    for i, r in enumerate(refs):
        try:
            im = Image.open(r["path"]).convert("RGB")
        except Exception:
            continue
        im.thumbnail((cell - 8, cell - 8))
        x, y = (i % cols) * cell, (i // cols) * (cell + cap)
        img.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        m = r.get("measure_cm") or {}
        dims = " x ".join("%s%g" % (k[0], v) for k, v in m.items() if k in ("Height", "Width", "Depth", "Length", "Diameter"))
        lines = ["%d  %s" % (i + 1, (r.get("title") or "")[:34]),
                 "%s  %s" % ((r.get("date") or "")[:20], (dims + " cm") if dims else "")]
        for j, t in enumerate(lines):
            d.text((x + 6, y + cell + 4 + j * 18), t, fill=(222, 196, 134))
    path = os.path.join(out, "refs_sheet.png")
    img.save(path)
    print("SHEET " + path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["met", "cma", "local", "sheet"])
    ap.add_argument("query", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--dept", type=int, default=4)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--from", dest="yr_from", type=int)
    ap.add_argument("--to", dest="yr_to", type=int)
    ap.add_argument("--type", dest="typ", help="cma only: e.g. 'Arms and Armor', 'Furniture and woodwork'")
    ap.add_argument("--must", default="",
                    help="comma list; keep only objects whose title/name has one")
    a = ap.parse_args()
    if a.mode == "sheet":
        sheet(a.query or a.out)
    elif a.mode == "met":
        met(a.query, a.out, a.dept or None, a.n, a.yr_from, a.yr_to, must=a.must)
    elif a.mode == "cma":
        cma(a.query, a.out, a.n, a.yr_from, a.yr_to, must=a.must, typ=a.typ)
    else:
        local(a.query, a.out, a.n)


if __name__ == "__main__":
    sys.exit(main())
