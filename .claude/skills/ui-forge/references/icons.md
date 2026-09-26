# Icons and chrome ornaments — the Blender lane

The owner's order (2026-09-26): *"the icons need to be art ... not white and black ... hight
quality art made with blender"*. game-art-director routes every icon, button and glyph request
here, and its `references/ui-icons.md` stays as background for subjects and colour language.
The objects are built and rendered with blender-forge (its library, `tools/forge_run.py`, its
QA). This file sets what a UI icon must be, how to render it, and the survival check that
decides pass or fail.

**In scope**: resource and currency icons, hourglasses, tracker plate icons, bottom-bar and HUD
entries, bubble icons, troop-line emblems, state icons (lock, seals, busy), social and settings
icons, event-type icons, rank badges (alliance.md §2.5), chrome ornaments (corner fittings,
studs, rivet rows, trims, seals), the empty-state still lifes (states.md §6), the guide pointer.
**Not here**: portraits and painted boards (game-art-director, commander-forge), building
thumbnails (`core/build_thumbs.gd`, castle-forge), item-card art (blender-forge's card
pipeline: it uses a dark backdrop, not alpha).

## 1. Size ladder

| Use | Display px | Ship px | Master render |
|---|---|---|---|
| Inline: cost lines, resource strip | 44–48 | 64 | 512 |
| Chip, button, bubble icon | 56–72 | 128 | 512 |
| HUD entries, bottom bar, rail | 96–120 | 128 | 512 |
| Empty-state still life | 256–320 | 512 | 1024 |
| Guide pointer | 120 | 256 | 1024 |

- Ship size ≥ display size and ≤ 2.5 × it. Anything shown below half its ship size needs
  mipmaps (§7), or it shimmers when it moves.
- **The 44 px survival test applies to every icon**, whatever its display size: it will appear
  at 44 px somewhere (a cost line, a chat share card, a report row).

## 2. Construction rules (numbers the check measures)

1. **One real object**, the conventional metaphor built as a crafted thing: settings = a
   forged iron gear with a brass hub; mail = a folded letter under a wax seal; search = a
   brass-rimmed reading lens. Recognition beats novelty. A pile counts as one object.
2. **Fill 76–84% of the frame** (measured on the alpha bounding box; the post step centres it
   at 80%).
3. **Camera**: 10–20° above the object, turned 15–25° so its depth reads; 100 mm lens (no
   distortion). One camera for the whole family.
4. **Value plan before materials** (blender-forge rule): 3–4 value groups on the object
   (measured), an internal value range p95 / p5 ≥ 4.5:1, and a lit rim at the upper left
   whose p90 luminance is ≥ 3:1 against OAK, so the icon survives dark chrome.
5. **The house light**: `studio_rig` key upper-left (the torchlight), cool fill at 20%,
   neutral rim. An icon carries rarity glow ONLY when it depicts a rarity item; then it is
   rendered with `retier()` for each tier, exactly like a card strip.
6. **INK contour 3 px at 128** (12 px at 512), added in post from the alpha: the painted
   house outline. It gives 12.66:1 against PARCHMENT on every icon.
7. **Contact shadow ≤ 20% opacity**, inside the frame (ui-icons.md). No cast shadow into
   scenery, no background.
8. **No text, numbers, letters or rune shapes** in the art (game-art-director's negative).
   Counts and sizes are drawn by the UI in digits.
9. **One hot gold accent** per icon (the master style block's "single hot gold accent"),
   GILT #C9A04C as its base colour.
10. **Detail ≥ 3 px at 128 px** (≥ 12 px at 512). Smaller detail becomes noise at 44 px, and
    noise lowers the measured value range.
11. **Distinct silhouettes in a family**: the 44 px black silhouettes of any two icons in one
    family overlap by IoU ≤ 0.80 (centred masks). Round coin-like sameness is the usual failure.
12. **No legally protected emblem**: no red cross on white for the infirmary (it is protected
    by the Geneva Conventions; stores flag it). Use herbs and linen.

## 3. Families

| Family | Members | Object (house register) | Notes |
|---|---|---|---|
| Resources | food, wood, stone, iron, gold | ui-icons.md fragments: bound wheat sheaf · split oak logs · dressed limestone blocks · blue-grey ingots · stamped coins | the shipped `icons/*.png` rows win until a swap (§8) |
| Premium, points | gems, rp | cut deep-red gem cluster · open study scroll with a brass compass (shipped: sapphire trio · tome and quill) | gems get a richer finish than the stock five |
| Hourglasses | Works · Muster · Universal | oak frame + square caps · iron frame + round caps · gilt frame + crown caps | 3 icons for 7 sizes: the size is a UI digit tag. No weapon on Muster (core-loop §5.5) |
| Tracker plates | build · research · muster · infirmary · banners | mason's trowel on a dressed block · lectern with an open book · practice pell with a battered shield · herb bundle on folded linen · pennon on a pole | the muster chip is not a buy button, so the pell is allowed |
| Bottom bar | Lords · Alliance · seal (castle / realm) · Chronicle · More | crested helm on a stand · three crossed pennons · round seal showing the keep / a folded war-map · bound chronicle with a ribbon · brass-bound cabinet with drawers | the seal shows its destination (architecture.md §1) |
| HUD entries | mail · Herald's Board · Help all · search · bookmarks · home | letter + wax seal · notice board with pinned sheets · two clasped gauntlets · reading lens · map pin flag · the keep | |
| Bubbles | finish free · claim · suggested upgrade | hourglass with a gilt ribbon · the chest (ui-icons.md) · gilt chevron on an iron plate | idle and wounded bubbles reuse the plate icons |
| Troop lines | infantry · spearmen · archers · crossbows · cavalry | heater shield + arming sword · spearhead on a shaft · drawn longbow · spanned crossbow · horse head in a chanfron | the silhouette carries the line (components.md §4); the accent colour is only on cloth or shield |
| States | lock · success · failure · busy · offline | padlock · wax seal · broken wax seal · small hourglass (turned in-engine) · a road sign with a broken arm | |
| Social, settings | chat · mention · block · report · settings · language · audio · alerts · accessibility · hand | rolled note and quill · pointing gauntlet · barred gate · raised pennant · forged gear · armillary sphere · hunting horn · hand bell · horn-rimmed spectacles · left or right gauntlet | |
| Chrome ornaments | corner fittings ×4, rarity studs, Masterwork crest, rivet rows, bead and rope mouldings, sheet grabber, seal base | §6 | ship at 1×, see components.md §3 |

## 4. The render recipe (blender-forge library; run through the lock)

```python
"""icons_<family>.py - one family, one camera, one rig, transparent 512 px masters.
py .claude/skills/blender-forge/tools/forge_run.py run icons_<family>.py icons <outdir>"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
# this script lives in art/ui_forge/icons/<family>/ ; FORGE_LIB overrides (staged library)
sys.path.insert(0, os.environ.get("FORGE_LIB")
                or os.path.abspath(os.path.join(HERE, "../../../../.claude/skills/blender-forge/lib")))
import bpy, forge as F
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(HERE, "out", "icons")
os.makedirs(OUT, exist_ok=True)

def build_gold():
    """Real forms only (forms.md): lathed coins, a stack of 5 and one on edge."""
    parts = []
    # ... F.lathe(...) coins, F.hard_surface(...), F.mat_metal(...) with a crowned relief ...
    return parts

FAMILY = {"gold": build_gold}                  # every member of the family, same staging below
for name, build in FAMILY.items():
    F.reset_scene()
    parts = build()
    center, size = F.bounds(parts)
    F.world_dark('#07080B', 0.4)               # lights the scene; hidden by film_transparent
    F.studio_rig(center, radius=1.2, rim=F.TIERS['common']['rim'],
                 key_energy=260, rim_energy=300, hair_energy=40)
    cam = F.camera(center, center + Vector((0.35, -1.0, 0.32)), lens=100)  # ~17 deg up, ~19 deg turned
    s = F.render_setup(res=(512, 512), samples=64, bloom=False)  # bloom would halo into the alpha
    s.render.film_transparent = True           # render_setup sets False: override AFTER it
    s.render.image_settings.file_format = 'PNG'
    s.render.image_settings.color_mode = 'RGBA'
    F.frame_fill(cam, parts, fill=0.80)        # after render_setup (needs the aspect)
    print("ICON", name, F.render(os.path.join(OUT, f"{name}_512.png")))
```

Every function above exists in `blender-forge/lib/forge.py` (checked 2026-09-26: `reset_scene`,
`bounds`, `world_dark`, `studio_rig`, `TIERS`, `camera`, `render_setup`, `frame_fill`, `render`).
Build the objects with the library's forms, operators and `mat_*` materials. Primitives are
blockout only (blender-forge hard rule 2). Then run `quality_report` on each part, as in the
template.

## 5. The survival check (post step + gate)

PROPOSED tool `ui-forge/tools/icon_check.py`: tested on a synthetic icon on 2026-09-26 with
Pillow 12 and numpy 2. Until the lead installs it, keep a copy beside the family's build
script. It squares and centres the master at 80% fill, measures it, adds the 3 px INK
contour, writes the 128 px ship file, a survival sheet (128 / 64 / 44 px on PARCHMENT, OAK and
INK) and a 44 px black silhouette, then prints one verdict line.

```python
"""icon_check.py <master_512.png> <out_dir> - ship 128 px + INK contour, 44 px survival sheet, metrics."""
import sys, os, numpy as np
from PIL import Image, ImageFilter
INK, PARCH, OAK = (0x1E, 0x17, 0x12), (0xE8, 0xD9, 0xB5), (0x4A, 0x2E, 0x1B)

def lum(rgb):                                   # WCAG relative luminance, rgb uint8 (..., 3)
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c @ np.array([0.2126, 0.7152, 0.0722])

def ratio(a, b):
    hi, lo = max(a, b), min(a, b); return (hi + 0.05) / (lo + 0.05)

src = Image.open(sys.argv[1]).convert("RGBA"); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
name = os.path.splitext(os.path.basename(sys.argv[1]))[0].replace("_512", "")
box = src.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
obj = src.crop(box); side = int(max(obj.size) / 0.80)          # object fills 80% of the frame
sq = Image.new("RGBA", (side, side)); sq.paste(obj, ((side - obj.width) // 2, (side - obj.height) // 2))
ship = sq.resize((128, 128), Image.LANCZOS)            # metrics on the object, before the contour
px = np.asarray(ship); A = px[..., 3] > 127; L = lum(px[..., :3])[A]
fill = max(np.ptp(np.where(A.any(0))[0]), np.ptp(np.where(A.any(1))[0])) / 128
hist = np.histogram(L ** (1 / 2.2), bins=16, range=(0, 1))[0] / L.size
groups = int(np.sum(np.diff(np.r_[0, (hist >= 0.04).astype(int)]) == 1))   # runs of bins holding >= 4%
spread = ratio(float(np.percentile(L, 95)), float(np.percentile(L, 5)))   # the icon's own value range
a = ship.getchannel("A")
inner = np.asarray(a.filter(ImageFilter.MinFilter(13))) < 128   # 6 px band inside the silhouette edge
lit = float(np.percentile(lum(px[..., :3])[A & inner], 90))
ring = a.filter(ImageFilter.MaxFilter(7))                       # 3 px INK contour at 128 px
contour = Image.new("RGBA", ship.size, INK + (0,)); contour.putalpha(ring)
ship = Image.alpha_composite(contour, ship); ship.save(f"{out}/{name}_128.png")

rep = dict(fill=round(float(fill), 2), value_groups=groups, value_range=round(spread, 1),
           lit_rim_vs_OAK=round(ratio(lit, float(lum(np.array(OAK)))), 2))
sheet = Image.new("RGBA", (3 * 3 * 140, 140), (0, 0, 0, 255))   # 128/64/44 on parchment, oak, ink
for i, bg in enumerate((PARCH, OAK, INK)):
    for j, s in enumerate((128, 64, 44)):
        tile = Image.new("RGBA", (140, 140), bg + (255,)); ic = ship.resize((s, s), Image.LANCZOS)
        tile.alpha_composite(ic, ((140 - s) // 2, (140 - s) // 2)); sheet.paste(tile, ((i * 3 + j) * 140, 0))
sheet.save(f"{out}/{name}_survival.png")
sil = Image.new("RGB", (44, 44), (255, 255, 255))
sil.paste((0, 0, 0), mask=ship.resize((44, 44), Image.LANCZOS).getchannel("A").point(lambda v: 255 if v > 127 else 0))
sil.save(f"{out}/{name}_silhouette44.png")
ok = 0.76 <= rep["fill"] <= 0.84 and 3 <= groups <= 4 and spread >= 4.5 and rep["lit_rim_vs_OAK"] >= 3.0
print("ICON", name, rep, "PASS" if ok else "FAIL")
```

Synthetic reference result (a 4-value coin): `ICON synth_coin {'fill': 0.79, 'value_groups': 4,
'value_range': 9.0, 'lit_rim_vs_OAK': 9.39} PASS`.

**The gate** = the PASS line + the eye test: open `<name>_survival.png` and name the icon at
44 px on all three grounds within 1 second (a critic agent or the owner). Then the family's
silhouette IoU check (rule 11). Report all three with the icon.

## 6. Chrome ornaments and trims

1. **Orthographic, straight on**: `cam.data.type = 'ORTHO'`, `cam.data.ortho_scale` set so
   1 render px = 0.5 design px (render at 2×, then LANCZOS down to 1× for clean 3 px lines).
2. **Tiling trims** (rivet rows, bead and rope mouldings): build one repeat unit, array it
   3 times, render the middle unit, so both ends meet the next copy without a seam.
   `rivet_row` spacing = the repeat length. Check the join by tiling the 1× strip 4 times
   in Pillow and looking for a seam at 100%.
3. **Corner fittings** (4 designs: primary button, panel, card, modal) come from `plate`,
   `rivet`, `gem_cabochon` and `mat_metal` with the GILT base. The fitting sets the
   nine-slice patch margin (components.md §3): measure its size at 1×. It must stay ≤ 1/3 of
   the smallest display size of the piece.
4. **Rarity studs**: 0 / 1 / 2 / 4 gilt studs + a Masterwork crest (components.md §4). Each
   stud is ≥ 12 px at 1×, so it counts at 44 px card thumbnails.
5. **Grounds** (parchment and oak fills) come from the painted `panels` group
   (game-art-director) or from a flat Blender material bake. Their luminance varies ≤ 6%
   (components.md §3.5).
6. Nine-slice assembly (corners + tiled edges + centre) happens in a Pillow script beside the
   renders. The result is checked in Godot at 3 display sizes: the minimum size, 1080 wide,
   and 1440 wide.

## 7. Naming, atlases and import

- **Names**: `ui_<family>_<name>_<px>.png` (`ui_res_gold_128.png`). Masters (`_512`) and the
  build scripts live in `art/ui_forge/icons/<family>/` (game-director teams.md). Install to the
  shipped icon folder (`godot/assets/uiicons`, game-art-director's `icons` group).
- **Atlases**: one per family plus one HUD atlas, built with Godot's Texture Atlas importer
  (Import As → TextureAtlas, one `atlas_file` of ≤ 2048²). The HUD atlas stays resident;
  family atlases load with their screens.
- **Import**: `process/fix_alpha_border = true` (no dark fringe from straight alpha);
  VRAM Compressed (ETC2/ASTC) for family atlases, after a 1:1 check of the INK contour
  for block artefacts. Use Lossless for the HUD atlas if the contour breaks up. Mipmaps ON
  for atlases shown at ≤ 64 px, with the CanvasItem's texture filter set to
  linear-with-mipmaps.
- **Budget**: HUD atlas ≤ 2048² (≈ 4 MB with ASTC 4×4, 16 MB lossless). All UI textures
  resident at once ≤ 64 MB (PROPOSAL; ship-forge owns the device total).

## 8. Replacing shipped icons

The shipped painted icons (`icons/gold.png` is the anchor) stay until a family is swapped as a
whole. A swap needs a dated checkpoint of the old files (game-director rule 2), a side-by-side
of old and new at 44 / 64 / 128 px on the three grounds, and the owner's look. Never mix
painted and rendered icons inside one family: the eye reads the mix as two games.

## 9. Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| A white, monochrome or line glyph | owner order broken | [ ] review: every icon has a `_512` master from Blender |
| Bloom left on | a grey halo inside the alpha, a dirty edge on parchment | [ ] `render_setup(bloom=False)` in the script; survival sheet |
| `film_transparent` set before `render_setup` | opaque black background (render_setup resets it) | [ ] survival sheet shows squares |
| Details under 3 px at 128 | mush at 44 px; value range falls | [ ] `icon_check` value_range ≥ 4.5 |
| A dark icon on dark chrome | disappears on OAK | [ ] lit_rim_vs_OAK ≥ 3.0 |
| Two icons in a family with the same silhouette | mis-taps in the tracker | [ ] IoU ≤ 0.80 |
| A dark fringe around icons in-game | the straight-alpha border | [ ] `fix_alpha_border` on import |
| Shimmer on moving inline icons | no mipmaps below half size | [ ] import settings review |
| A red cross on the infirmary | store rejection risk | [ ] review rule 12 |

- [ ] One object, fill 76–84%, camera 10–20° up and 15–25° turned, one camera per family.
- [ ] 3–4 value groups, value range ≥ 4.5:1, lit rim ≥ 3:1 on OAK; INK contour 3 px at 128.
- [ ] No text or glyph shapes; one gold accent; details ≥ 3 px at 128.
- [ ] `icon_check` PASS + the 1-second eye test + the family IoU check, all reported.
- [ ] Atlas, alpha border, compression and mipmaps set; the swap of shipped art has a checkpoint.
