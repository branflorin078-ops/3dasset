# Readability — read at real size, value first, no empty looks

The owner's standard: "no empty looks — high quality details and contrast, like a senior
designer with 40 years of experience". This file turns that sentence into tests. Every 2D
asset is judged at the size the player really sees, in the squint, and with numbers from
§9. The 3D twin of these rules (render-side measurement, value plan before materials) is
blender-forge [art-direction.md](../../blender-forge/references/art-direction.md); keep
thresholds in step with it.

**Calibration first (once, then on every new anchor).** Thresholds below are STARTING
values. Run §9 on the three anchors — `commanders/edwin.png` (portrait proof standard),
`icons/gold.png` (icon anchor), one shipped board from `real art/` — and write their numbers
into §9's anchor table. A new asset must land within the anchor band or better. If an anchor
fails a starting threshold, the threshold moves to the anchor, not the other way round, and
the change is noted in this file.

## 1. Read distances — the size the player really sees

Sizes are px in the 1080 × 1920 reference layout (1080 px short side). On a 6.1–6.7 inch
phone 1080 px spans ≈ 65–70 mm, so **≈ 16 px per mm**; the phone is held at 30–40 cm
(pillar 10 "readable at arm's length").

| Asset class | Master size | Smallest display | Other displays | Must read at the smallest size | Test |
|---|---|---|---|---|---|
| UI icon (Blender art now; the rule applies to its render) | 128 (`icons` group) | **44 px ≈ 2.8 mm** | 64, 96 (PROPOSAL, ui-forge) | which resource / action; locked or open | §9 `--icon` on PARCHMENT and OAK |
| Line medallion (battle, map, reports) | Blender icon | 44 px (battle-forge presentation §2) | 72 px counter badge | which of the five lines | greyscale 44 px, name the line |
| Effect icon (boost tray, omens) | 128 | 44 px | 64 | which effect | same as UI icon |
| Equipment card EQ-* | group size (path to confirm) | 128 px grid thumb | 256 detail | object class; rarity in 0.5 s from rim + glow | 128 px row, all 4 tiers side by side |
| Troop card TRP-* (4:5) | batch size (upgrade/GEMINI_TROOPS.md) | 128 × 160 | 256 × 320 recruit panel | the line (weapon silhouette) and the tier band (gear richness) | 128 px greyscale, name line + tier band |
| Lord portrait CMD-* | group size | 56 dp battle chip / 96 px HUD chip | 280 px skill card; lord screen ART SHOWN BIG | WHICH lord: hair or hood mass, head covering, palette accent | 56 px, 8 lords side by side, blind-named |
| Sigil SGL / alliance ALS | group size | 24 px (chat marker) | 28–40 px banner (battle-forge) | the device in 2 values | 24 px black-fill silhouette |
| Map overlay marker (camp, landmark, march medallion) | Blender icon | 32 px (PROPOSAL) | 44 px | class + relationship by SHAPE | §4 greyscale + CVD test |
| City on the realm map (3D cluster) | — | 48–96 px | — | level, owner colour, burning / warded | blender-forge architecture.md §2 |
| Board, head-piece, splash (T-*, BND-*) | full width | 270 px (25% thumbnail in a list) | 1080 wide | the subject in 1 s | 25% thumbnail + §9 on the full image |

Rules:
1. **Test at the smallest display size**, downscaled with Lanczos (what mipmaps do), on every
   ground the asset sits on (PARCHMENT panel, OAK/INK panel, the painted world).
2. **The smallest information-carrying shape is ≥ 12% of the display width** — 5 px at 44 px,
   15 px at 128 px — and stands ≥ 20 L* from its neighbour. Anything smaller is texture: fine
   as surface, never as the thing that tells the player what the object is.
3. **Blind name test**: a critic (a person or a sub-agent) who has NOT seen the prompt gets only
   the downscaled image and names class + state. Icons, medallions, markers and sigils must be
   named 5 of 5 times; cards and portraits 4 of 5.
4. What must survive the smallest size goes in the prompt's first 15 words: the ALL-CAPS
   subject noun plus the one object that defines the silhouette ("A PIKEMAN AT THE BRACE: pike
   butt set…").

## 2. Value structure — plan the values before the colours

The palette tokens, measured (CIE L*, and WCAG 2.x contrast ratio against three grounds):

| token | hex | L* | vs INK | vs OAK | vs PARCHMENT |
|---|---|---|---|---|---|
| INK | #1E1712 | 8 | 1.0 | 1.4 | 12.7 |
| OAK | #4A2E1B | 22 | 1.4 | 1.0 | 8.8 |
| IRON | #3B4048 | 27 | 1.7 | 1.2 | 7.5 |
| WAX | #8A1F24 | 31 | 1.9 | 1.4 | 6.5 |
| GILT | #C9A04C | 68 | 7.3 | 5.1 | **1.7** |
| GILT lit | #E0BC6A | 78 | 9.8 | 6.8 | 1.3 |
| PARCHMENT | #E8D9B5 | 87 | 12.7 | 8.8 | 1.0 |

What the table forces:
- **GILT on PARCHMENT is 1.7:1** — gold detail on a cream ground disappears. Gold on cream
  always carries an INK contour.
- **OAK, IRON and WAX on INK are 1.4–1.9:1** — a dark object on a dark panel vanishes. Its
  upper-left edge carries a rim light (the house torchlight gives it for free).
- So an icon is read by its **INK outline on light grounds** and by its **rim light on dark
  grounds**; it needs both.

Value plan per class (L* ranges; the squint must show these masses):

| class | darkest mass | middle | lightest | notes |
|---|---|---|---|---|
| Icon / medallion | INK outline ≤ 20, continuous ≥ 90% of the contour | shadow side 25–40, lit face 55–75 | rim and speculars 80–95 on ≤ 10% of the area | 3–4 steps (ui-icons.md) |
| Portrait | hair / hood / background 10–30 | face shadow side 35–50 | face lit planes 65–80 | the catchlight is the single brightest point |
| Troop card | vignette edges ≤ 30 | armour and cloth 35–60 | lit side of face + weapon 60–80 | the weapon crosses a ≥ 25 L* edge |
| Board | foreground anchor 12–30 | subject band: full range | haze band 55–75 with a range ≤ 20 | UI safe zones: range ≤ 15 L* |
| Effect still | the implied ground 20–40 | body 60–80 | core ≥ 90 on ≤ 5% of the frame | light pools on the ground |

**The squint test** (§9 does it): shrink to 64 px on the long side and blur 1 px.
- **3–5 value groups** (fewest groups with in-group spread ≤ 6 L*). 1–2 = flat or graphic
  (icons may sit at 3); 6 = no plan.
- **Value range** (2nd to 98th percentile) ≥ **45 L*** for dawn and noon presets, ≥ **35 L***
  for siege dusk and chronicle night (environments.md).

**Focal contrast** (8 × 8 grid, RMS contrast of L* per cell):
- the highest-contrast cell ≥ **2.0 ×** (median cell + 2 L*);
- when the brief names a focal box: **≥ 4 of the 6** highest-contrast cells lie inside it,
  and the box alone spans **≥ 0.8** of the whole image's value range — the darkest dark and
  the lightest light meet at the focal point;
- the 6 top cells form one cluster. Two separated clusters = two focal points = fail.

## 3. Colour channels — each colour has one job

| channel | carries | lives on | never on |
|---|---|---|---|
| GILT (the single hot accent) | value, sworn state (gilt rim), "yours" (rally gilt corner) | one fitting per image, ≤ 10% of the area; the sworn rim light | large fields; text on PARCHMENT |
| WAX | urgency, seals | seals, the HUD alert, ≤ 5% of the area | relationship; decoration |
| Line accents | which troop line | medallion ring, banner trim, one accent per card | banner fields, chrome |
| Rarity (forge.TIERS glow + rim) | Issued / Sound / Fine / Masterwork | item cards, gear models | the map layer, markers, chrome |
| Relationship (§4) | self / ally / enemy / neutral | map and battle overlays only | everything else |

Channels never swap roles (battle-forge presentation §2 uses the same words). The one
allowed combination on one element: a banner with a relationship FIELD, a line-accent TRIM
and the lord's SGL device.

## 4. Relationship colours — the reserved channel

| class | hex (PROPOSAL) | L* | marker shape | march line | where it appears |
|---|---|---|---|---|---|
| SELF | #9ADB6E spring green | 81 | circle | solid dashes | own castle ring, own marches, own banner fields, own territory edge |
| ALLY | #3A8FE0 clear blue | 58 | heater shield | dash-dot | alliance members' castles, marches, banner fields, territory |
| ENEMY | #E0482A vermilion | 53 | crossed blades | chevron dashes pointing at the target | hostile castles, marches, AI lords at war with you |
| NEUTRAL | #F3F1EC bone white | 95 | square | dotted | barbarian camps, unaligned lords, unowned landmarks |

Marker shapes match chat-forge ui.md (circle / shield / crossed blades / square). The march
line width and pulse are battle-forge flows.md §5 (6 px; 8 px + ≤ 1 Hz pulse when aimed at
you).

**Measured** (Machado 2009 colour-vision simulation at full severity, CIEDE2000):
- full colour vision: every pair ≥ 26 apart;
- protanopia, deuteranopia, tritanopia: every pair ≥ **18** apart (worst: self/enemy for
  deuteranopes 18, self/ally for tritanopes 20);
- against an INK outline: 10.7 / 5.2 / 4.3 / 15.7 : 1 — all above the 3:1 non-text minimum;
- on PARCHMENT the fills alone fail (1.2–2.9:1) → **every relationship marker carries a 2 px
  INK outline**, on panels and on the map alike.

Known near-collisions with other channels (why placement is a rule, not a hope): ally vs the
Sound rarity glow #4F7FD6 ΔE 7; ally vs crossbows #6D8AA8 ΔE 9; enemy vs infantry #B4432E ΔE 10;
neutral vs PARCHMENT ΔE 12; SELF vs a green-gold heal glow ΔE 11; ENEMY vs orange-red fire
mid-tones ΔE 4 (effects.md §"Restraint budget" moves those effect hues).

Rules:
1. **Reserved.** On any asset that sits on the map, battle or HUD layer (icons, medallions,
   markers, sigils, token kit, effect textures) pixels within ΔE ~15 of SELF, ALLY or ENEMY at
   chroma ≥ 35 are **≤ 0.5%** (§9 RESERVED lines). Boards and portraits never paint a reserved
   hue as a flat field; Edwin's crimson mantle is WAX-family (ΔE 22 from ENEMY) and is fine.
2. **Never** in chrome, buttons, rarity, event art fields, alliance tinctures or house sigils
   (ΔE ≥ 15 from every relationship colour — design-forge alliance.md says tinctures never match
   a relationship colour).
3. **Shape first, colour confirms.** Test: a realm screenshot in greyscale and in the three
   simulations; a critic names 20 random markers; ≥ 19 correct in each version.
4. An attack aimed at the player stays ENEMY on the map; the HUD alert about it is WAX.
5. Values of record: this table (art direction owns colour values). design-forge ux.md and
   world.md own where the channel appears; battle-forge, ui-forge and chat-forge apply it. If the
   shipped owner-colour table (path to confirm) differs, the shipped values win and this table is
   corrected; the building tint mask (blender-forge architecture.md §7) uses the same values.

## 5. Zoom survival — shape and colour carry far, paint detail pays near

The four zoom levels are transition-forge's (ui-forge architecture.md §1 maps the HUD onto them).

| zoom | typical size on screen | information carried by | paint detail that still counts |
|---|---|---|---|
| Castle close | building 180–320 px, villager 40–80 px | material, construction, job prop, faces of working people | all of it: wear, brushwork, one history mark |
| Castle overview | building 60–120 px | silhouette + roof colour + job prop → which building, which tier | shapes ≥ 5 px only |
| Region | march token: 3 figures of the largest line + lord banner + 44 px medallion (battle-forge flows.md §5) | squad silhouette (line), banner field (relationship), medallion (line), tier plate (text) | kit silhouette steps (t1 cloth → t10 plate) |
| Realm | city 48–96 px, markers 32–44 px, march = relationship line + 32 px banner icon | shape class, relationship colour + marker shape, size class | none — flat shape and colour only |

Rules:
1. Every brief names its **farthest zoom** and what must survive there. Information put in a
   channel that is gone at that zoom is a bug (a tier shown only by engraving, a relationship
   shown only by a banner device).
2. **One layer per zoom band** (design-forge lessons G-10): the realm shows relationship and
   size, not tier trims; castle close shows craft, not relationship rings.
3. Test: downscale the asset to each listed size and blind-name class, state and relationship.

## 6. Chrome versus painted art — chrome never wins

1. **ART SHOWN BIG.** The floor is ui-forge hard rule 1: a screen about one thing gives its art
   ≥ 30% of the screen area, the building card's next-tier render ≥ 40% of the screen height,
   list rows ≥ 96 px of art. Art direction's target for the lord screen and key-art screens:
   the painted subject ≥ **50% of the screen height** (≥ 960 px) — PROPOSAL to ui-forge. A
   chrome frame is ≤ **6% of the panel's short side** (the UI-002 lesson: a 58 px border
   swallowed a 60 px button).
2. **Contrast order.** Run §9 on a screenshot of the screen: the top contrast cell lies in the
   art, not on a frame corner, and the frame's own highest cell is ≤ **0.8 ×** the art's focal
   cell.
3. **Chrome values** stay in OAK / IRON / INK and PARCHMENT. GILT on chrome ≤ **3% of the
   screen**; ornament only at corners (≤ 12% of each edge length), plain rails between — rest
   areas apply to chrome too.
4. **Chrome is matte and cooler in chroma than the art's focal area**: no painted glow, no
   rarity colour, never a relationship hue.
5. Text over art sits on an INK scrim ≥ 70% or carries an INK outline (ui-forge rule 7);
   environments.md's UI safe zones are where that scrim goes.

## 7. Against empty looks

**The 60/30/10 detail budget.** On boards, portraits and cards, measured on a 16 × 16 grid of
edge energy (§9 DETAIL line; brush grain removed first):
- **quiet 45–75% of cells** (below half the mean): broad planes, sky, big cloth folds, the
  vignette — rest for the eye;
- **supporting 20–40%**: secondary forms, props, the second material;
- **rich 5–15%**: the cluster at the focal point, holding **30–70%** of all edge energy.

Where detail clusters: joints, edges, touch points (grip, buckle, hinge, stirrup), the face and
hands, the job prop. Where it rests: large planes turned away from the key, the shadow side, the
background beyond the subject band.

**Edge highlights.** Every plane that turns toward the upper-left key carries a highlight line —
1–2 px at 44–64 px, 2–4 px at 256 px — brighter than its plane by ≥ 15 L*. Edges turned away
keep the INK outline. A form without either reads as cut paper.

**Shadows.** Every object touching something carries a contact shadow, darkest (≤ 20 L*)
within 2% of the object's height from the contact; the cast shadow falls lower-right (the
house light). Icons keep the contact shadow soft and ≤ 20% (ui-icons.md). The shadow side of a
form sits ≥ 25 L* below its lit side — one value group apart.

**Material contrast.** Two touching materials differ by ≥ 1 value group or by finish (matte
wool next to polished steel); same-value, same-finish neighbours merge into one shape.

**Diagnosis → DELTA** (the fix is a corrective delta prompt, never a rewrite):

| symptom | §9 signal | cause | delta fragment (house register) |
|---|---|---|---|
| grey, nothing pops | range < 45, groups ≤ 2 | flat light, no value plan | "warm torchlight from the upper left, deep umber shadow pooling lower right, the lit face near parchment cream" |
| busy everywhere | quiet < 45%, rich share < 30% | detail spread evenly | "the background falls into broad unbroken planes; fine detail only on <focal object>" |
| the eye lands in the wrong place | < 4 of top-6 cells in the box | contrast on a secondary object | "the brightest light and darkest dark meet at <focal>; <secondary> sinks into shadow" |
| two focal points | two top-cell clusters | two lit subjects | "<second subject> in half-shadow, lower contrast" |
| sticker, floating | no dark within 2% of contact | no contact shadow | "a soft contact shadow directly beneath, darkest where it touches" |
| plastic, airbrushed | quiet > 75%, no grain | missing surface behaviour | "visible painterly brush texture following the form, matte surfaces, worn and chipped edges" |
| new, toy-like | — (rubric axis 8) | no history | "one honest history mark: <dent hammered flat / re-stitched strap>" |
| mush at size | fails the blind name test | key shape < 12% of width | "one bold silhouette; <key element> oversized and clear of the body" |
| cold (intake code) | no pixels near GILT | no warm key | "warm torchlight … a single hot gold accent on <one fitting>" |
| gold everywhere | GILT-like pixels > 10% | accent overused | "gold only on <one fitting>; the rest aged oak, iron and parchment" |
| dark icon lost on panels | < 20% edge px vs OAK | no rim light | "thick rim highlight along the upper-left edge" |
| reserved hue in decoration | RESERVED > 0.5% | colour from the wrong channel | "<cloth> in aged oak brown and iron grey" |

## 8. The critique rubric — score every result

Score each axis 0–3 with one sentence of visual evidence. **PASS = total ≥ 24 / 30 and no axis
below 2.** Axis 1 must score 3 for icons, medallions, markers, sigils and cards (they live at
play size — reference-forge improve-loop axis 9 has the same rule).

| # | axis | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|
| 1 | Read at size | blind-named at the smallest size, 5/5 | 4/5 | named only at 2× | not named |
| 2 | Silhouette | black-fill reads the class; one clear weapon/object; no tangents | reads, one tangent | needs interior detail to read | reads as something else |
| 3 | Value structure | 3–5 groups, range in band | one number off by ≤ 10% | groups ≤ 2 or range short by > 10 L* | flat |
| 4 | Focal contrast | ≥ 2.0 ×, ≥ 4/6 in the box, one cluster | 1.6–2.0 × | second focal competing | no focal |
| 5 | Detail rhythm | 60/30/10 bands met, detail at joints and touch points | one band off by ≤ 10 points | evenly busy or evenly bare | noise or empty |
| 6 | Edges and light | upper-left key, edge highlights, INK outline, rim on dark grounds | one lapse | light direction mixed | no light logic |
| 7 | Grounding | contact + cast shadow correct | contact only | soft float | floating |
| 8 | Material and wear | each material by physical behaviour; one honest mark | one material generic | plastic surfaces | uniform CG surface |
| 9 | Palette and channels | tokens, one GILT accent ≤ 10%, reserved ≤ 0.5%, one line accent | one accent drifts | off-ladder colour | wrong channel colours |
| 10 | Fit to its frame | fill / crop / safe zones right; no text, no frame | minor crop issue | safe zone busy | text, frame or wrong format |

Rubric fails map to the intake reject vocabulary (text, props, stand, cold, frame,
wrong-subject, two-subjects, off-ladder-colour, weaker). PROPOSAL additions for the intake:
`flat` (axis 3), `busy` (axis 5), `float` (axis 7), `reserved-hue` (axis 9).

## 9. The measurement tool

Copy to `tools/read_check.py` (path to confirm; Pillow + numpy). Tested on synthetic cases on
2026-09-26: an evenly noisy image scores groups 1 / quiet 0%; a flat image groups 1 / range
5 L*; a lit focal on a quiet ground 3 groups / 6 of 6 cells in the box; an outlined, rim-lit coin
icon 90% / 24% on the two grounds; the same coin without outline or rim 100% / 0%.

```python
# py tools/read_check.py <image.png> [--focal x0,y0,x1,y1] [--icon]   (focal box in 0..1)
import sys, numpy as np
from PIL import Image, ImageFilter
PARCH, OAK = (232, 217, 181), (74, 46, 27)
REL = {"self": "#9ADB6E", "ally": "#3A8FE0", "enemy": "#E0482A"}          # §4, PROPOSAL values

def lab(rgb):                                     # sRGB 0..255 (...,3) -> CIE L*a*b* (D65)
    c = np.asarray(rgb, float) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = c @ np.array([[0.4124564, 0.2126729, 0.0193339], [0.3575761, 0.7151522, 0.1191920],
                        [0.1804375, 0.0721750, 0.9503041]]) / [0.95047, 1.0, 1.08883]
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116*f[..., 1] - 16, 500*(f[..., 0] - f[..., 1]), 200*(f[..., 1] - f[..., 2])], -1)

def flat(im, bg):                                 # RGBA flattened onto a panel colour
    b = Image.new("RGB", im.size, bg); b.paste(im, mask=im.getchannel("A")); return b

def fit(im, n):                                   # long side -> n px (Lanczos, like mipmaps)
    s = n / max(im.size); return im.resize((max(1, round(im.width*s)), max(1, round(im.height*s))), Image.LANCZOS)

def cells(a, n):
    H, W = a.shape[:2]; return [a[i*H//n:(i+1)*H//n, j*W//n:(j+1)*W//n] for i in range(n) for j in range(n)]

def value_groups(L):                              # fewest 1-D k-means groups with in-group RMS <= 6 L*
    x = L.ravel()
    for k in range(1, 7):
        c = np.percentile(x, np.linspace(0, 100, 2*k + 1)[1::2])
        for _ in range(25):
            g = np.abs(x[:, None] - c[None]).argmin(1)
            c = np.array([x[g == i].mean() if (g == i).any() else c[i] for i in range(k)])
        if np.sqrt(((x - c[g]) ** 2).mean()) <= 6.0: return k
    return 6

def report(path, focal=None, icon=False):
    im = Image.open(path).convert("RGBA"); rgb = flat(im, PARCH) if icon else im.convert("RGB")
    Ls = lab(fit(rgb, 64).filter(ImageFilter.GaussianBlur(1)))[..., 0]          # the squint
    p2, p98 = np.percentile(Ls, [2, 98])
    print(f"SQUINT   groups {value_groups(Ls)} | range {p98 - p2:.0f} L* | dark/mid/light % "
          f"{(Ls < 35).mean()*100:.0f}/{((Ls >= 35) & (Ls <= 65)).mean()*100:.0f}/{(Ls > 65).mean()*100:.0f}")
    L = lab(fit(rgb, 256))[..., 0]; rms = np.array([c.std() for c in cells(L, 8)])
    floor = np.median(rms) + 2.0; top = np.argsort(rms)[::-1][:6]
    print(f"FOCAL    top cell / (median+2) {rms.max()/floor:.2f} | top-6 cells (col,row) "
          + " ".join(f"({t % 8},{t // 8})" for t in top))
    if focal:
        x0, y0, x1, y1 = focal; H, W = L.shape; box = L[int(y0*H):int(y1*H), int(x0*W):int(x1*W)]
        inside = sum(x0 <= (t % 8 + .5)/8 <= x1 and y0 <= (t // 8 + .5)/8 <= y1 for t in top)
        g2, g98 = np.percentile(L, [2, 98]); b2, b98 = np.percentile(box, [2, 98])
        print(f"FOCAL    box range / image range {(b98 - b2)/max(1e-6, g98 - g2):.2f} | top-6 inside box {inside}/6")
    s = lab(fit(rgb, 256).filter(ImageFilter.MedianFilter(5)))[..., 0]        # shapes, not brush grain
    gy, gx = np.gradient(s); e = np.array([c.mean() for c in cells(np.hypot(gx, gy), 16)])
    m = e.mean() + 1e-9; q, r = (e < 0.5*m).mean(), (e >= 2*m).mean()
    print(f"DETAIL   quiet/supporting/rich cells % {q*100:.0f}/{(1 - q - r)*100:.0f}/{r*100:.0f} | "
          f"rich cells hold {e[e >= 2*m].sum()/(e.sum() + 1e-9)*100:.0f}% of edge energy")
    px = lab(rgb).reshape(-1, 3); chroma = np.hypot(px[:, 1], px[:, 2])
    for k, hx in REL.items():                     # dE76 < 24 ~ dE2000 < 15 for these saturated hues
        ref = lab(np.array([[int(hx[i:i+2], 16) for i in (1, 3, 5)]]))[0]
        hit = ((np.linalg.norm(px - ref, axis=1) < 24) & (chroma >= 35)).mean() * 100
        print(f"RESERVED {k:6s} {hit:.2f}% of pixels")
    if icon:
        a = np.asarray(im.getchannel("A")) > 127; ys, xs = np.nonzero(a)
        print(f"ICON     fill (bbox long side / frame) {max(np.ptp(xs), np.ptp(ys)) / max(a.shape)*100:.0f}%")
        s44 = fit(im, 44); m44 = np.asarray(s44.getchannel("A")) > 127
        core = np.asarray(Image.fromarray((m44*255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 127
        for name, bg in (("parchment", PARCH), ("oak", OAK)):
            dL = np.abs(lab(flat(s44, bg))[..., 0][m44 & ~core] - lab(np.array([bg]))[0, 0])
            print(f"ICON     44 px edge band vs {name}: {(dL >= 25).mean()*100:.0f}% of edge px >= 25 L* apart")

if __name__ == "__main__":
    a = sys.argv[1:]; f = [float(v) for v in a[a.index("--focal") + 1].split(",")] if "--focal" in a else None
    report(a[0], f, "--icon" in a)
```

| gate | boards, portraits, cards | icons, medallions, markers |
|---|---|---|
| SQUINT groups / range | 3–5 / ≥ 45 L* (≥ 35 dusk, night) | 3–4 / ≥ 45 L* |
| FOCAL top cell | ≥ 2.0; box ≥ 0.8 of range; ≥ 4/6 inside | — |
| DETAIL quiet / supporting / rich | 45–75 / 20–40 / 5–15 %; rich share 30–70% | — |
| RESERVED | ≤ 0.5% each on map/battle/HUD-layer art | ≤ 0.5% each |
| ICON fill / edge vs PARCHMENT / vs OAK | — | 75–85% / ≥ 70% / ≥ 20% |
| Anchor values (fill in at calibration) | edwin.png: … · board: … | gold.png: … |

## 10. Checklist — before an asset is recorded as shipped

- [ ] Smallest display size known (§1) and the blind name test passed at it.
- [ ] §9 run; the output pasted beside the asset id; every gate in band or the miss explained.
- [ ] Focal box stated in the brief and confirmed by the FOCAL line.
- [ ] Contact shadow, edge highlights, one honest history mark visible at 256 px.
- [ ] No reserved relationship hue outside a relationship marker; one GILT accent.
- [ ] Farthest zoom named; the asset downscaled to it still says what it must (§5).
- [ ] On its screen: art at the ui-forge floor (≥ 30% of the area; ≥ 50% of the height on lord
      and key-art screens) and chrome contrast below the art's (§6).
- [ ] Rubric scored (§8): total, each axis, PASS or the DELTA prompt that fixes the lowest axis.
