# Art direction — shape, value, contrast and detail, measured

The owner's standard: "no empty looks — high quality details and contrast". An
empty look is measurable: planes with no designed value step, edges that merge
into the backdrop, a focal area that does not win, ornament too thin to read at
card size. Every rule here has a number, a failure mode and the `lib/forge.py`
knob that fixes it; §9 is the probe, §10 diagnoses the canon card. Order of
work: shape (§1) → value plan (§2) → materials, colour (§3–4) → detail, wear,
scale (§5–7). Detail never rescues a bad value plan.

## 1. Shape language — big, medium, small

- **Budget of the read** (forms.md): primary forms 60% (silhouette, big
  planes), secondary 30% (guard, grip, bands, openings), tertiary 10%.
- **Size ladder**: neighbouring size classes differ by **2.5–4×**. Below 1.8×
  two elements compete; above 6× the middle is missing and the eye jumps from a
  calm shape straight to noise. Sunforged: blade 1020 mm → quillon span 310 mm
  (3.3×) → sunburst ~150 mm (2.1×: too close to the quillon) → gem 28 mm.
- **Mass, not needles**: a feature longer than 10× its width reads as a line.
  Ornament meant as a mass keeps length/width ≤ 5. The canon rays: 50–88 mm on
  a 12.4 mm root tapering with exponent 0.85 → mean width ≈ 6 mm, L/W ≈ 13.
- **Rest is planned**: 10–25% of the subject may be calm (the `flat` gate),
  far from the focal (upper third of a blade, a shield field, a roof field).

Detail size at card size, `px/mm = card_px × fill / length_mm` (canon: 1846 px for 1.37 m at 1600):

| Card width | px/mm | 1 px = | 0.6 mm bevel | 6 mm edge bevel |
|---|---|---|---|---|
| 1600 (final) | 1.35 | 0.74 mm | 0.8 px | 8 px |
| 1024 (probe) | 0.86 | 1.2 mm | 0.5 px | 5 px |
| 512 (card spec) | 0.43 | 2.3 mm | 0.26 px | 2.6 px |
| 128 (read test) | 0.11 | 9 mm | — | 0.7 px |

At 512 px a detail of **≥ 3 px is shape**, **1–3 px is texture** (a value
change of its area), **< 1 px is sheen** only. Failure modes: equal-size
ornament, needles, detail spread evenly, sub-pixel detail counted as detail.

## 2. Value — plan three values before any material

Hard rule 9 in SKILL.md. After the silhouette blockout give each part one of
three flat greys, render the preview and run the probe (§9):

```python
VAL = {'dark': '#3C3C3C', 'mid': '#777777', 'light': '#C6C6C6'}   # L* 25 / 50 / 80
def value_mat(key):                        # blockout-only material: flat grey dielectric
    mb = F.MB("VAL_" + key)
    F.set_in(mb.p, F.IN["base"], F.hex_lin(VAL[key])); F.set_in(mb.p, F.IN["rough"], 0.5)
    return mb.mat
```

`<card>_3val.png` must read the object in three values. Sunforged plan: blade
flat mid, edge bevels light/dark by side, fuller light, sunburst light on a dark
écusson, grip dark with light wire, pommel a light ring on a dark face.

**Metal takes its value from what it reflects, not from its albedo.** The canon
blade base `#7E7466` is L* 49; the render shows L* 66–93, sRGB (200, 196, 191):
the 1.2 m key softbox, mirrored. Set a metal's value with roughness, with the
size, position and radiance of the lights it mirrors (`area_light`, §8) and with
the dark world (`world_dark`) it mirrors between highlights.

**The focal area wins on local contrast.** Choose it before any detail:

| Asset class | Focal (highest local contrast) | Rest area |
|---|---|---|
| Sword, axe, mace | guard + ricasso (the glow's hottest point, glow.md) | upper third of blade / haft |
| Helm | brow band + sights | crown of the bowl |
| Shield | boss + device | field between boss and rim |
| Chest, door | lock plate + hinge straps | plank fields |
| Building (game camera) | door + job prop on the lit face (architecture.md §3) | roof field, back faces |
| Siege engine | the working joint (arm pivot, windlass) | frame beams |

Gates: qa.md §2, reasoning §9.3. Bands are necessary, not sufficient: the canon
card has balanced bands (30.6 / 34.7 / 34.7) and is still 34.6% flat — one
smooth gradient supplies all three values without one designed step.

## 3. Material contrast — neighbours differ on two axes

Touching materials differ on **at least two** of: rendered value (**ΔL* ≥ 15**),
roughness (**Δ ≥ 0.20**), hue or metalness (metal against dielectric, or ≥ 30°
of hue). One axis alone merges them at 128 px.

| Pair | Roughness (materials.md) | Carries the split | Watch |
|---|---|---|---|
| steel / leather | 0.30 / 0.55–0.70 | roughness + value | leather ≥ 15 L* below the steel flat |
| gold / steel | 0.18 / 0.30 (Δ 0.12) | hue + value | a dark ground (blackened iron) between them |
| gold wire / leather | 0.18 / 0.60 | value | wire ≥ 30 L* above leather (canon: 47.6 vs 36.4) |
| blackened iron / oak | 0.55 / ~0.65 | value | iron ≥ 15 L* below the oak |
| stone / timber / plaster | 0.78 / ~0.65 / ~0.85 | value + hue | alternate dark and light storeys |
| cloth / metal | 0.85 / 0.2–0.45 | all three | cloth sheen 0.5–0.7 |

**Rendered range inside one material** (p5–p95, `--region`): polished metal
≥ 50 L*, satin metal 35–55, leather 15–35, cloth 10–25, stone and wood 20–35.
Canon grip: albedo `#4A1418` (L* 15.6) renders at mean 36.4, p5–p95 9.8–63.2,
sRGB (125, 72, 70) — `spec` 0.35 at roughness 0.55 turned oxblood to dusty rose.
Hero metal needs `rough_var` ≥ 0.20 (0.12 = ±0.06, a uniform sheen). No
`mat_wood` yet (library request): `F.MB` + a `ShaderNodeTexWave` (BANDS)
stretched along the grain, roughness 0.60–0.75.

## 4. Colour temperature and reserved colours

- **Item cards**: neutral white key, fill `#C9D4E6` at 20%, rim = tier colour,
  warm backdrop (lighting-render.md); the key stays neutral because `TIERS`
  were calibrated under it (lessons #29). **Buildings**: warm sun or torch
  upper-left, cool shadow lower-right (architecture.md §1).
- **Chroma budget**: ≤ 3 material hue families + the tier colour (canon: steel,
  gold, oxblood + legendary amber). Props and icon objects anchor on GILT
  `#C9A04C`, WAX `#8A1F24`, PARCHMENT `#E8D9B5`, OAK `#4A2E1B`, IRON `#3B4048`,
  INK `#1E1712`. House families of architecture: architecture.md §10.
- **Reserved channels, never decorative**: tier colour only on rim and glow;
  relationship colours only through the tint mask (architecture.md §7); line
  accents (infantry `#B4432E`, spearmen `#8B8F95`, archers `#4F7A4A`, crossbows
  `#6D8AA8`, cavalry `#C9A76A`) only on troop kit and tokens.

## 5. Detail density — where it clusters, where it rests

Detail clusters where the object's story happens: **joints** (guard to blade,
ferrule to grip, hinge to board), **edges** (arrises catch light and wear),
**touch points** (grip centre, handles, door ring, lock plate), **load points**
(rivets at stress, straps at folds). It rests on the fields between.

- A focal cluster holds **5 ± 2 distinct features** within ~10% of the
  object's length (canon guard: finials, écusson, rays, gem, ferrule).
- **Rest ≠ empty**: a rest field has no tertiary FORMS but keeps micro-surface
  (roughness breakup, long scratches ≥ 1 px at 1024), so most of it stays above
  the 2 L* detail line. Flat pixels belong to glow cores, mirror highlights and
  the calmest third of the largest plane. No rest area above 30% of the subject.
- Buildings: clusters at door, job prop, eaves, quoins; roof and wall fields
  keep course or tile texture of 3–6 px at the overview.

## 6. Wear — one history, placed by use

**One history mark**, ≥ 3 px at 512 (≥ 7 mm on a greatsword), where the
object's life puts it: a nick at the forte (where blades meet), a replaced rivet
of another metal, a re-wrapped grip end, a dent on the helm's left brow (toward
the enemy of a right-handed fighter), scorch on a gate's lowest planks. One
mark, not scattered noise. Wear follows `brush_axis`.

| Material | Where | Real width / form | Knob |
|---|---|---|---|
| Steel arris | edges, rivet crowns | 0.5–2 mm polish line, rough ×0.45 | `mat_metal(wear=)` |
| Blade edge | cutting bevel | honed band 3–8 mm, rough −0.10 to −0.15 | overlay on u = \|x\|/W (§10) |
| Gold, brass, bronze | relief high points, rims | 1–3 mm rub-through; cavities dark | `wear_color`, `cavity`, `cavity_amt` |
| Leather | edges, grip centre, strap folds | 1–3 mm burnish; touch zones 20–40 mm darker | `mat_leather(edge=, wear=)` |
| Wood | corners, handles, thresholds | 2–6 mm rounded, lighter; hand zones darker | MB (no `mat_wood`) |
| Stone | arrises, steps | chips 5–30 mm, irregular, never a clean line | geometry + `mat_stone` |

AO mask distance ≈ 15% of the part's thickness (materials.md): `mat_leather(edge=)`
exposes it; `mat_metal` is fixed at 4 mm — suspect on 2–10 mm blades (library
request: `mat_metal(edge=)`).

## 7. Scale cues — real sizes the eye uses as a ruler

Build cues at real size. Exaggerate only readable props (job props 1.3–1.6×,
doors, windows 1.2–1.4×, architecture.md §3) and ornament (~1.6×, forms.md),
never structural cues. A cue repeats **≥ 3×** in view to act as a ruler. Sizes
are approximate; measure the real object through reference-forge.

| Cue | Real size | Cue | Real size |
|---|---|---|---|
| armour snap rivet head | Ø 6–10 mm | door or chest clench nail | Ø 12–20 mm |
| iron strap-hinge | 40–60 mm wide, 4–6 mm thick | plank | 150–300 mm wide, 25–50 mm thick |
| frame post, beam | 200–300 mm square | stone course | 250–350 mm high |
| plain clay roof tile | ~265 × 165 mm | shingle | 100–150 mm exposed |
| thatch at the eave | 300–400 mm thick | belt, strap | 25–40 mm wide, ~3 mm thick |
| mail ring | 6–10 mm inside Ø | siege rope | Ø 20–40 mm |

## 8. "Empty look" diagnosis — symptom → cause → fix → knob

| Symptom | Cause | Fix (numbers) | forge.py |
|---|---|---|---|
| Metal is one smooth gradient, a "rod" | a continuous convex section mirrors a continuous slice of the lights | flat + edge bevel over 22–28% of the half-width, samples ON the shoulders | `loft` sections; `hard_surface(width=0.0003–0.0005)` |
| Shoulders smoothed away | shoulder angle below the `hard_surface` angle | angle below the shoulder (canon: 25–30° shoulder → 15) | `hard_surface(angle=)` |
| No edge highlight line | bevel < 1 px at 1024 | ≥ 1 px at 1024 on hero parts | `hard_surface(width=)`, `mat_metal(bevel_r=)` |
| Uniform plastic sheen | roughness ±0.06 | `rough_var` 0.20–0.24, `scratch` 0.4–0.6 | `mat_metal(rough_var=, scratch=)` |
| Scratches invisible | 1.1 mm specks (noise scale 900) = 0.5 px at 512 | long scratches: noise 25–30 behind Mapping (60, 60, 1), ramp 0.64–0.70 | `MB.n`, `MB.ramp`, overlay (§10) |
| A big field with no story | no etched band, mark or inscription | etched panel 12–16 cm: base `#2E2A24`, rough 0.62, motif | `MB.map_range`, `MB.obj_axis`, `ShaderNodeTexWave` |
| Ornament reads as spikes | L/W > 10, no mass at the root, no ground | fewer, wider rays; blunt tips ≥ 1.5 mm; dark ground | `loft(tip=)`, `lathe`, `mat_metal('#1B1A1A', rough=0.55)` |
| Focal is a white dot | emissive disc blown, no inner structure | a faceted gem or cabochon; widest clip ≤ 5 px | `gem_cabochon`, `gem_brilliant`, `mat_gem(emit_strength≤1.5)` |
| Leather pink or rose | sheen lifts dark red by +20 L* | darker base, rough 0.68–0.72, spec 0.22 | `mat_leather(rough=)`, `set_in(mb.p, IN["spec"], …)` |
| Wire wrap busy but flat | wire/leather ΔL* 11 | ≥ 30 | darker leather; gold rough 0.18 |
| Shadow-side edges merge | the rim reaches one side only | low kickers aimed at the dark part | `area_light(name, loc, target, energy, size, size_y=)` |
| A dark bevel on the silhouette; or a blown streak after "fixing" it | the plane mirrors the dark world; or the strip's radiance is too high | a strip at the plane's mirror direction at 0.1–0.3× key radiance (energy ÷ area; key 480 W ÷ 1.44 m² = 333 W/m²) | `area_light(…, size=0.10, size_y=1.8)` |
| Focal lost after a detail pass | the rest gained local contrast | raise the focal (dark ground, more steps) or calm the rest | probe `--focal` |
| Materials merge | neighbours differ on < 2 axes | §3 table | `mat_*` parameters |
| Whole part reads as "edge" | AO mask distance > 15% of thickness | scale the mask | `mat_leather(edge=)` |
| Wall or roof reads as a box | quoins, courses, verge only as sub-pixel texture | geometry quoins, string courses, verge thickness, ridge | architecture.md §5 |
| Ornament floats or looks glued | not sunk | sink 0.2 mm | forms.md |

## 9. Measure it — `value_probe.py`

### 9.1 The probe (Pillow + numpy, outside Blender; copy it next to the renders)

Run: `py value_probe.py card.png --mask card_mask.png --tier legendary --focal
0.24,0.55,0.40,0.74` (missing numpy: `py -m pip install numpy pillow`).

```python
"""value_probe.py - value, contrast and empty-look numbers for one render (Pillow + numpy).
  py value_probe.py card.png [--mask card_mask.png] [--tier legendary] [--focal x0,y0,x1,y1]
                    [--region name=x0,y0,x1,y1 ...]     boxes = FRACTIONS of the image (0..1)
Without --mask the subject is "L* > 6" (bloom halos count). Writes <card>_flat.png, <card>_3val.png."""
import sys, numpy as np
from PIL import Image
S, SUBJ, FLAT, LO, HI = 1024, 6.0, 2.0, 30.0, 70.0   # width, subject L*, flat RMS, band edges
GATE = dict(flat=(10.0, 25.0), clip=2.0, clip_hot=5.0, clip_w=5, band=15.0,
            sep=70.0, lost=10.0, focal=1.20, cr=4.5)
def lstar(im):                                # sRGB -> linear Y -> CIE L* (0..100)
    a = np.asarray(im.convert('RGB'), np.float64) / 255
    Y = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4) @ np.array([0.2126, 0.7152, 0.0722])
    return np.where(Y > 216 / 24389, 116 * np.cbrt(Y) - 16, Y * 24389 / 27), Y
def box(img, r):                              # mean over a (2r+1)^2 window (integral image)
    k = 2 * r + 1; c = np.pad(img, ((r + 1, r), (r + 1, r)), 'edge').cumsum(0).cumsum(1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / k ** 2
def sel(shape, spec):                         # "x0,y0,x1,y1" fractions -> boolean box
    x0, y0, x1, y1 = map(float, spec.split(',')); h, w = shape; b = np.zeros(shape, bool)
    b[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = True; return b
def row(tag, s):
    v, f = L[s], det[s & inner]; p5, p95 = np.percentile(v, [5, 95])
    print(f"{tag:<10} px {s.sum():>6} meanL {v.mean():5.1f} p5-p95 {p5:3.0f}-{p95:3.0f} "
          f"flat {100 * (f < FLAT).mean() if f.size else 0:5.1f}% clip {100 * (v >= 98).mean():4.1f}%")
def gate(name, ok, text):
    print(f"QA_VALUE {name:<10} {text:<52} {'PASS' if ok else 'FAIL'}"); return ok
args = sys.argv[1:]; path, pairs = args[0], list(zip(args[1::2], args[2::2])); opt = dict(pairs)
im = Image.open(path); im = im.resize((S, round(im.height * S / im.width)), Image.LANCZOS); L, Y = lstar(im)
if '--mask' in opt:                           # the alpha pass (9.2), or any white-on-black mask
    mk = Image.open(opt['--mask']); mk = mk.getchannel('A') if 'A' in mk.getbands() else mk.convert('L')
    m = np.asarray(mk.resize(L.shape[::-1])) > 127
else: m = L > SUBJ
mf = m.astype(float); inner = box(mf, 3) > 0.999            # interior: skip the silhouette edge
bp = box(L, 1) - box(L, 3)                                   # band-pass: features ~3-7 px
det = np.sqrt(np.maximum(box(bp ** 2, 3), 0))                # local detail RMS, L* units
far = ~(box(mf, 24) > 0.001); ff = box(far.astype(float), 40)  # backdrop >= 24 px away
bgl = np.where(ff > 0, box(L * far, 40) / np.maximum(ff, 1e-6), L[far].mean())
v = L[m]; bands = [100 * (v < LO).mean(), 100 * ((v >= LO) & (v < HI)).mean(), 100 * (v >= HI).mean()]
flat, clip = 100 * (det[inner] < FLAT).mean(), 100 * (v >= 98).mean()
c, w = (m & (L >= 98)).astype(float), 0                      # widest clipped shape (erosions)
while c.any(): c, w = (box(c, 1) > 0.999).astype(float), w + 1
dl = (L - bgl)[(box(mf, 1) > 0.999) & ~(box(mf, 3) > 0.999)]  # edge band 1-3 px inside vs backdrop
print(f"frame {L.shape[1]}x{L.shape[0]}  subject {100 * m.mean():.2f}%  backdrop meanL {L[far].mean():.1f}")
print("subject L* histogram, 10 bins:", (np.histogram(v, 10, (0, 100))[0] / v.size * 100).round(1).tolist())
row('SUBJECT', m)
for k, spec in pairs:
    if k == '--region': name, b = spec.split('=', 1); row(name, m & sel(L.shape, b))
cmax = GATE['clip_hot'] if opt.get('--tier') in ('legendary', 'mythic') else GATE['clip']
ok = [gate('flat', GATE['flat'][0] <= flat <= GATE['flat'][1], f"{flat:.1f}% of interior (10-25)"),
      gate('clipped', clip <= cmax and 2 * w - 1 <= GATE['clip_w'],
           f"{clip:.1f}% (<={cmax:.0f}), widest {max(2 * w - 1, 0)} px (<=5)"),
      gate('bands', min(bands) >= GATE['band'], "dark/mid/light %.1f/%.1f/%.1f (each>=15)" % tuple(bands))]
sil = gate('silhouette', 100 * (dl >= 15).mean() >= GATE['sep'] and 100 * (dl < 8).mean() <= GATE['lost'],
           f">=15 L*: {100 * (dl >= 15).mean():.1f}% (>=70), <8: {100 * (dl < 8).mean():.1f}% (<=10)")
if '--mask' in opt: ok.append(sil)
else: print("QA_VALUE silhouette is INFO only: rerun with --mask (bloom halos fake the edge)")
if '--focal' in opt:
    f = m & sel(L.shape, opt['--focal']); lc = np.sqrt(np.maximum(box((L - box(L, 7)) ** 2, 7), 0))
    ratio, cr = lc[f].mean() / lc[m & ~f].mean(), (Y[f].mean() + 0.05) / (Y[far].mean() + 0.05)
    ok.append(gate('focal', ratio >= GATE['focal'] and cr >= GATE['cr'],
                   f"local contrast x{ratio:.2f} (>=1.20), {cr:.1f}:1 (>=4.5)"))
print(f"QA_VALUE verdict {'PASS' if all(ok) else 'FAIL'} ({sum(ok)}/{len(ok)} gates)")
stem = path.rsplit('.', 1)[0]; rgb = np.asarray(im.convert('RGB')).copy(); fl = inner & (det < FLAT)
rgb[fl] = (rgb[fl] * 0.3 + [178, 0, 0]).astype(np.uint8); Image.fromarray(rgb).save(stem + '_flat.png')
Image.fromarray(np.select([~m, L < LO, L < HI], [0, 60, 140], 230).astype(np.uint8)).save(stem + '_3val.png')
```

### 9.2 The alpha pass (last lines of the asset script, after the beauty render)

```python
bpy.data.objects["Backdrop"].hide_render = True      # backdrop_radial() names it "Backdrop"
s = bpy.context.scene; s.render.film_transparent = True; s.cycles.samples = 8   # 25 s on 4 CPU cores
F.render(os.path.join(OUT, f"{asset}_{MODE}_mask.png"))   # RGBA, alpha = subject; render it LAST
```

### 9.3 What the numbers mean — and why the gates sit where they do

- **CIE L\*** (0–100): equal steps look equal. Images are resized to 1024 px
  first: the canon flat share reads 34.6 / 34.5 / 32.3% at 1600 / 768 / 512 px.
- **flat 10–25%**: detail RMS < 2 L* at the 3–7 px scale (3.5–8 mm on a
  greatsword at 1024). Above 25%: large areas without one designed step — the
  empty look. Below 10%: no rest, busy. The backdrop's noise floor is 0.03 L*,
  so the 2 L* line measures design, not render noise.
- **bands ≥ 15% each**: catches washed-out cards (test E: dark 13.3%).
- **clipped ≤ 2%** keeps highlights as glints. Legendary and mythic cores clip
  by calibration (core `#FFF3C4` at 7.5 × the hot factor): the canon fuller core
  is 58% of its clipped pixels, 4.0–4.5% of the subject, 3 px wide — hence 5%
  for those tiers. **Widest clipped shape ≤ 5 px**: a white LINE reads as
  light, a white SHAPE as a hole (test C reached 7 px).
- **silhouette**: a 128 px thumbnail averages a 1 px edge with the backdrop
  about 50/50, so a 15 L* step survives as ~8 L* — four times the 2 L* step, a
  margin for phone glare. 70%, not 100%, leaves room for planned lost edges.
  Only with `--mask`: the threshold mask swallows bloom halos (57.2% vs 67.4%
  with the alpha pass on the same render).
- **focal ×1.20**: mean local contrast (15 px window), focal box over the rest.
  Moving the box ±2% of the frame moves it ±0.10, so 1.20 = "clearly wins";
  box tight, ≤ 15% of the frame. 4.5:1 is ui-forge's body-text contrast.

### 9.4 When the probe lies

Bloom halos inflate the threshold mask (use `--mask`); parts darker than L* 6
drop out of it; a busy backdrop breaks the backdrop estimate; boxes are image
fractions (redraw after reframing). Gates are a PROPOSAL calibrated on one card
family (1.4 m weapon, fill ~0.78): log approved cards in lessons.md, re-tune after five.

## 10. Worked example — the canon Sunforged card

Rendered 2026-09-26 by `examples/sunforged_greatsword.py final` on Blender 4.0.2
(Linux, 4 CPU cores, a build without OpenImageDenoiser: 275 samples, 2 min 32 s);
the owner keeps it as `art/forge/baseline/sunforged_final.png`.

| Region (`--region` box) | Mean L* | p5–p95 | Flat | Clipped |
|---|---|---|---|---|
| Subject (5.53% of frame; blade = 63.5% of it) | 52.7 | 8–97 | **34.6%** | 4.0% |
| Blade tip half `0.56,0.14,0.93,0.44` | 66.2 | 11–93 | **54.0%** | 0.9% |
| Blade lower half `0.39,0.35,0.69,0.62` | 62.8 | 16–100 | 29.3% | 6.8% |
| Guard + sunburst `0.24,0.55,0.40,0.74` | 45.5 | 8–99 | 23.1% | 5.5% |
| Grip `0.06,0.68,0.28,0.87` | 37.3 | 7–81 | 0.1% | 1.4% |

Gates: flat 34.6% **FAIL**; clipped 4.0%, 3 px PASS; bands PASS; silhouette
**FAIL** (alpha pass of the 1000 px control: 67.4% ≥ 15 L*, 17.8% < 8 — the
shadow side of grip and pommel); focal ×1.30, 5.8:1 PASS. **Cross-section
scan** (pixel column x = 1100 of the 1600 px card): a 3 px edge line peaking at
L* 53, a trough of 8–14, a smooth ramp 14 → 92 over ~35 px, a plateau of 90–93
over ~30 px (the softbox), a fade 91 → 6 over ~15 px with no edge line. Not one
designed step.

**Diagnosis → fix**, ranked (all values tested below):
1. **Rod section** — the lenticular `y = T·(1−|x|^2.2)^0.62` mirrors the key as
   one gradient → hexagonal: crowned flat to |x| = 0.74·W, edge bevel over the
   outer 26%, samples ON the shoulders, `hard_surface(blade, width=0.0004,
   segments=2, angle=15)` (the old `angle=35` smoothed the ~25–30° shoulder).
2. **No ricasso** — 95 mm flat, unsharpened, 1.08·T thick, a crisp step.
3. **Uniform sheen** — `mat_metal(rough=0.34, rough_var=0.22, scratch=0.5)` +
   long scratches + a polished bevel band. 4. **No etched band** — panel beside
   the fuller, z 0.11–0.26 m, `#2E2A24`, rough 0.62, wave BANDS scale 70.
5. **Spikes** — 7 rays per side (62/85/66/95 mm alternating), root half-width
   10 mm, taper exponent 0.55, 2.6 mm proud; disc r 30 mm with a stepped face;
   an amber `gem_cabochon` (r 18.6 mm) as the sun; a blackened-iron écusson
   (`#1B1A1A`, rough 0.55, r 36 mm) behind the rays.
6. **Rose grip** — `mat_leather(base='#3A0F12', rough=0.70)` + `spec` 0.22.
7. **Light** — hot gradient peak 1.0 → 0.45 (recompute the bake gate's analytic
   peak, qa.md §1); bevel strips 15 W / 8 W (0.10 × 1.8 m at each bevel's mirror
   direction, 1.6 m out: 0.25× / 0.13× key radiance); two 250 W hilt kickers
   (0.5 × 1.2 m, behind and below the grip, left and right).

Fixes 3–4 use an overlay built only from existing API (`get_in`, `IN`, `MB`):

```python
def overlay(mb, key, fac, value):          # mix a new layer over what feeds a Principled input
    sock = F.get_in(mb.p, F.IN[key]); src = sock.links[0].from_socket
    mb.link(mb.mix_col(fac, src, value) if key == 'base' else mb.mix_f(fac, src, value), sock)
m = blade_m; ax = m.math('ABSOLUTE', m.obj_axis('X')); z = m.obj_axis('Z')   # L, W0: the example's DIMENSIONS
w = m.math('MULTIPLY', m.math('SUBTRACT', 1.0, m.math('MULTIPLY', z, 0.22 / L)), W0)
u = m.math('DIVIDE', ax, w)                                   # 0 at the spine, 1 at the edge
overlay(m, 'rough', m.map_range(u, 0.725, 0.755), 0.16)       # honed edge bevel
```

**Test log** (1000 px previews, same camera and rig, 4.0.2 on CPU, `--tier
legendary`; "thr" = no alpha pass, silhouette not gated):

| Test | Change | Flat | Clipped | Bands d/m/l | Silhouette ≥15 / <8 | Focal | Gates |
|---|---|---|---|---|---|---|---|
| A | canon | 34.3% | 4.5%, 3 px | 29 / 34 / 37 | 67.4 / 17.8 | ×1.26 | 3/5 |
| B | A + fixes 1–6 | 24.0% thr | 4.1%, 3 px | 37 / 23 / 40 | — | ×1.12 | 3/4 |
| C | B + strips 260/140 W, backdrop falloff 0.5 | 46.4% thr | 8.6%, 7 px | 41 / 21 / 39 | — | ×1.66 | 2/4 |
| D | B + hot 0.45, écusson r 36 mm, hilt kickers 700 W ×2 | 14.7% | 5.5%, 3 px | 25 / 30 / 45 | 67.3 / 24.1 | ×1.10 | 2/5 |
| E | D + strips 40/20 W, kickers 450 W | 22.4% | 6.6%, 3 px | 13 / 29 / 58 | 95.5 / 1.5 | ×1.38 | 3/5 |
| F | D + strips 15/8 W, kickers 250 W | 20.3% | 4.9%, 3 px | 17 / 31 / 53 | 91.8 / 3.3 | ×1.29 | **5/5** |

Lessons: (a) section + material carry the blade (lower-half flat 31.6% → 2.7%
in B); (b) a strip on mirror metal shows its own radiance — 260 W on 0.18 m² is
4.3× the key and blew the bevels (C), 40 W washed the card out (E); (c) detail
added to the rest steals from the focal (×1.26 → ×1.10, D); (d) a brighter
backdrop (falloff 0.5) LOWERED separation to 57.9%; (e) the canon failed on the
unlit hilt, not the glowing edges. F's tip half (42% flat) is the planned rest.

## 11. Checklist — before preview, before final

- [ ] Value plan in three greys reads in `_3val.png`; focal boxed; rest planned.
- [ ] Size ladder 2.5–4×; masses L/W ≤ 5; tertiary ≥ 1 px at 512 or sheen only.
- [ ] Materials differ on two axes; metals placed by what they reflect; one
      history mark; wear widths §6; scale cues real, repeated ≥ 3×.
- [ ] Alpha pass rendered; probe run with `--mask --tier --focal`; `QA_VALUE
      verdict PASS` and the region table pasted; `_flat.png`, `_3val.png` opened.
