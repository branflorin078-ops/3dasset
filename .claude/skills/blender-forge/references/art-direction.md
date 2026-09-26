# Art direction — shape, value, contrast and detail, measured

The owner's standard: "no empty looks — high quality details and contrast".
An empty look is not a matter of taste. It is measurable: large areas with no
planned value step, edges that merge into the backdrop, a focal area that does
not win, ornament that is too thin to read at card size. This file gives the
rules a senior hard-surface and environment artist applies, each with a number,
a failure mode and the `lib/forge.py` knob that fixes it. §9 is the probe that
measures a render; §10 diagnoses the canon card with real numbers.

Order of work: shape (§1) → value plan (§2) → materials and colour (§3–4) →
detail, wear and scale (§5–7). Detail never rescues a bad value plan.

## 1. Shape language — big, medium, small

- **Budget of the read**: primary forms 60% (silhouette, big planes),
  secondary 30% (guard, grip, pommel, bands, straps, openings), tertiary 10%
  (rivets, wire, engraving, scratches). Same rule as forms.md; here it is a
  budget of attention, not of polygons.
- **Size ladder**: neighbouring size classes differ by **2.5–4×**. Closer than
  1.8× and two elements compete; farther than 6× leaves a missing middle and
  the eye jumps from a big calm shape straight to noise. Sunforged: blade
  1020 mm → quillon span 310 mm (3.3×) → sunburst ~150 mm (2.1×, too close to
  the quillon) → gem 28 mm → wire 2.7 mm.
- **Mass versus needle**: a feature longer than 10× its width reads as a line
  at card size. Ornament meant to read as a mass keeps length/width ≤ 5.
  The Sunforged rays are 50–88 mm long on a 12.4 mm root that tapers with
  exponent 0.85: mean width ≈ 6 mm, length/width ≈ 13 → "spikes".
- **Rest areas are planned**: 10–25% of the subject may be calm (the flat
  gate, §9). Put rest far from the focal (the upper third of a blade, a shield
  field, a roof field). Rest is not empty: it keeps micro-surface (§5).

**Detail size at card resolution** — `px/mm = card_px × fill / length_mm`.
Measured on the Sunforged card (tip to pommel 1846 px at 1600 px for 1.37 m):

| Card width | px per mm | 1 px equals | A 0.6 mm bevel | A 6 mm edge bevel |
|---|---|---|---|---|
| 1600 (final) | 1.35 | 0.74 mm | 0.8 px | 8 px |
| 1024 (probe) | 0.86 | 1.2 mm | 0.5 px | 5 px |
| 512 (card spec) | 0.43 | 2.3 mm | 0.26 px | 2.6 px |
| 128 (read test) | 0.11 | 9 mm | — | 0.7 px |

Role of a detail by its size at 512 px: **≥ 3 px = shape** (read one by one),
**1–3 px = texture** (read as a value change of the area), **< 1 px = sheen
only** (changes average roughness, nothing else). Design each detail for the
role it can actually play.

Failure modes: ornaments of equal size everywhere (no hierarchy); needles
instead of masses; detail spread evenly with no rest; tertiary detail below
1 px at 512 counted as "detail" when it is only sheen.

## 2. Value — plan three values before any material

Hard rule 9 in SKILL.md. After the silhouette blockout, give every part one of
three flat greys and render the preview:

```python
VAL = {'dark': '#3C3C3C', 'mid': '#777777', 'light': '#C6C6C6'}   # L* 25 / 50 / 80
def value_mat(key):                        # blockout-only material: flat grey, dielectric
    mb = F.MB("VAL_" + key)
    F.set_in(mb.p, F.IN["base"], F.hex_lin(VAL[key])); F.set_in(mb.p, F.IN["rough"], 0.5)
    return mb.mat
```

Run the probe (§9) and open `<card>_3val.png`: the object must read as itself
in three values. Sunforged plan: blade flat = mid; edge bevels = light on the
lit side, dark on the shade side (each with a light edge line where it meets
the backdrop); fuller = light (glow); sunburst = light on a dark écusson;
grip = dark with light wire; pommel = light ring on a dark face.

**Metal is placed by what it reflects, not by its albedo.** The Sunforged
blade base `#7E7466` has L* 49, yet the render shows L* 66–93 and sRGB
(200, 196, 191): the reflection of the 1.2 m key softbox. You set a metal's
value with roughness (higher = wider, dimmer highlight), with the size and
position of the lights it mirrors (`area_light`, strips, §3), and with the dark
world (`world_dark`) the flats reflect between highlights.

**The focal area wins on local contrast.** Choose it before modelling detail:

| Asset class | Focal (highest local contrast) | Rest area |
|---|---|---|
| Sword, axe, mace | guard + ricasso junction (the glow's hottest point, glow.md) | upper third of the blade / haft |
| Helm | brow band + sights | crown of the bowl |
| Shield | boss + device | field between boss and rim |
| Chest, door | lock plate + hinge straps | plank fields |
| Building (game camera) | door + job prop on the lit face (architecture.md §3) | roof field, back faces |
| Siege engine | the working joint (arm pivot, windlass) | frame beams |

Targets (the gate numbers live in qa.md §2; reasoning in §9.3):

| Measure (probe, 1024 px) | Target |
|---|---|
| Flat interior (detail RMS < 2 L*) | 10–25% of the subject |
| Value bands dark < 30 / mid / light ≥ 70 | each ≥ 15% of the subject |
| Clipped L* ≥ 98 | ≤ 2% (≤ 5% legendary/mythic); widest clipped shape ≤ 5 px |
| Silhouette (alpha mask) | ≥ 70% of edge pixels ≥ 15 L* from the backdrop, ≤ 10% below 8 |
| Focal | local contrast ≥ 1.20× the rest; ≥ 4.5:1 against the backdrop |

Bands are necessary, not sufficient: the Sunforged card has balanced bands
(30.6 / 34.7 / 34.7) and is still 34.6% flat — the smooth blade gradient
supplies all three values without one designed step.

## 3. Material contrast — neighbours differ on two axes

Two materials that touch must differ on **at least two** of: rendered value
(**ΔL* ≥ 15**), roughness (**Δ ≥ 0.20**), hue or metalness (metal against
dielectric, or ≥ 30° of hue). One axis alone merges them at 128 px.

| Pair | Roughness (materials.md) | What carries the split | Watch |
|---|---|---|---|
| steel / leather | 0.30 / 0.55–0.70 | roughness + value | leather ≥ 15 L* darker than the steel flat |
| gold / steel | 0.18 / 0.30 (Δ 0.12) | hue + value | put a dark ground (blackened iron) between them |
| gold wire / leather | 0.18 / 0.60 | value | wire ≥ 30 L* above the leather (Sunforged: 47.6 vs 36.4 = 11 → busy, flat) |
| blackened iron / oak | 0.55 / ~0.65 | value | iron ≥ 15 L* darker than the oak |
| stone / timber / plaster | 0.78 / ~0.65 / ~0.85 | value + hue | alternate dark and light storeys (architecture.md §4) |
| cloth / metal | 0.85 / 0.2–0.45 | all three | sheen 0.5–0.7 keeps cloth soft |

**Value range inside one material** (rendered p5–p95, probe `--region`):
polished metal ≥ 50 L*; satin metal 35–55; leather 15–35; cloth 10–25;
stone and wood 20–35. A metal below 30 reads as paint or plastic; a leather
above 45 reads wet or plastic. Sunforged grip leather: albedo `#4A1418` is
L* 15.6, the render gives mean 36.4 and p5–p95 9.8–63.2 (53 L*) — the key's
sheen on `spec` 0.35 and roughness 0.55 turned oxblood into dusty rose,
sRGB (125, 72, 70).

**Roughness spread inside one metal**: `rough_var` ≥ 0.20 on hero metal
(the default 0.12 gives ±0.06 — uniform sheen); worn zones ±0.20.

No `mat_wood` exists in the library yet (library request, TEAM.md). Until
then build wood with `F.MB` + a `ShaderNodeTexWave` (BANDS) stretched along
the grain by a Mapping node, roughness 0.60–0.75, value range 20–35 L*.

## 4. Colour temperature and reserved colours

- **Item cards**: key neutral white (1.2 m softbox upper-left), fill `#C9D4E6`
  at 20% camera-right, rim = tier colour behind-right, hair 15%, warm backdrop
  `#2A1B0C` → `#030304` (lighting-render.md). The key stays neutral because
  `TIERS` were calibrated under it (glow.md, lessons #29): a coloured key
  re-opens the calibration strip.
- **Buildings and map pieces**: the house light of the painted identity —
  warm sun or torch upper-left, cool shadow lower-right (architecture.md §1,
  game-art-director). Approve from the game camera.
- **Chroma budget**: ≤ 3 material hue families per asset plus the tier colour
  (Sunforged: steel grey, gold, oxblood + legendary amber). Props and icon
  objects anchor on the palette tokens GILT `#C9A04C`, WAX `#8A1F24`,
  PARCHMENT `#E8D9B5`, OAK `#4A2E1B`, IRON `#3B4048`, INK `#1E1712`.
- **Reserved channels, never decorative**: tier colour only on rim and glow;
  relationship colours (self / ally / enemy / neutral) only in the owner-colour
  mask (architecture.md §7); troop line accents (infantry `#B4432E`, spearmen
  `#8B8F95`, archers `#4F7A4A`, crossbows `#6D8AA8`, cavalry `#C9A76A`) only on
  troop kit and tokens.
- Failure: dark saturated reds under a white key plus cool fill drift to rose
  (the grip above). Darken the base and lower `spec` before touching hue.

## 5. Detail density — where it clusters, where it rests

Detail clusters where the object's story happens: **joints** (guard to blade,
ferrule to grip, hinge to board), **edges** (arrises catch light and wear),
**touch points** (grip centre, handles, door ring, lock plate) and **load
points** (rivets at stress, straps at folds). It rests on the fields between.

- A focal cluster holds **5 ± 2 distinct features** inside a circle ~10% of
  the object's length (Sunforged guard: quillon finials, écusson, rays, gem,
  ferrule, wire ends).
- **Rest ≠ empty.** A rest field has no tertiary FORMS but keeps micro-surface
  (roughness breakup, long scratches ≥ 1 px wide at 1024), so most of it stays
  above the 2 L* detail line. The only flat pixels allowed: glow cores,
  mirror highlights and the calmest third of the largest plane.
- No single rest area over 30% of the subject (`--region` flat share).
- Buildings: clusters at door, job prop, eaves and corners (quoins); rest on
  the roof field and wall fields, which still carry course or tile texture of
  3–6 px at the overview distance (architecture.md §2).

## 6. Wear — one history, placed by use

- **One history mark** per asset, ≥ 3 px at 512 (≥ 7 mm on a greatsword), put
  where the object's life would put it: a nick in the edge at the forte (where
  blades meet), a replaced rivet of a different metal, a re-wrapped grip end,
  a dent on the helm's left brow (the side toward the enemy for a right-handed
  fighter), scorch on a gate's lowest planks. One, not scattered noise.
- Wear follows the working direction (`brush_axis`: blades along the length).

| Material | Where | Real width / form | Knob |
|---|---|---|---|
| Steel arris | edges, rivet crowns | 0.5–2 mm polish line, rough ×0.45 | `mat_metal(wear=)` |
| Blade edge | cutting bevel | honed band 3–8 mm, rough −0.10 to −0.15 | overlay on u = \|x\|/W (§10) |
| Gold, brass, bronze | relief high points, rims | 1–3 mm rub-through, cavities dark | `wear_color`, `cavity`, `cavity_amt` |
| Leather | edges; grip centre; strap folds | 1–3 mm burnish; touch zones 20–40 mm darker | `mat_leather(edge=, wear=)` |
| Wood | corners, handles, thresholds | 2–6 mm rounded and lighter; hand zones darker | MB (no `mat_wood` yet) |
| Stone | arrises, steps | chips 5–30 mm, irregular — never a clean line | geometry + `mat_stone` |

Mask scale rule (materials.md): AO mask distance ≈ 15% of the part's
thickness. `mat_leather(edge=)` exposes it; `mat_metal` uses a fixed 4 mm
(`_edge_mask` default) — right for parts ~25–30 mm thick, suspect on 2–10 mm
blades (open library request: `mat_metal(edge=)`).

## 7. Scale cues — real sizes the eye uses as a ruler

Build cues at real size; exaggerate only readable props (job props 1.3–1.6×,
doors and windows 1.2–1.4×, architecture.md §3) and ornament (~1.6×,
forms.md). Never scale structural cues. A cue repeats **≥ 3 times** in view
to work as a ruler; one rivet is a dot, a row is a scale.
Sizes are approximate (general historical knowledge); measure the real
object through reference-forge when it matters.

| Cue | Real size | Cue | Real size |
|---|---|---|---|
| armour snap rivet head | Ø 6–10 mm | door/chest clench nail | Ø 12–20 mm |
| iron strap-hinge | 40–60 mm wide, 4–6 mm thick | plank | 150–300 mm wide, 25–50 mm thick |
| frame post / beam | 200–300 mm square | stone course | 250–350 mm high |
| plain clay roof tile | ~265 × 165 mm | shingle | 100–150 mm exposed |
| thatch at the eave | 300–400 mm thick | belt / strap | 25–40 mm wide, ~3 mm thick |
| mail ring | 6–10 mm inside Ø | siege rope | Ø 20–40 mm |

## 8. "Empty look" diagnosis — symptom → cause → fix → knob

| Symptom (probe / eye) | Cause | Fix (numbers) | forge.py |
|---|---|---|---|
| Metal is one smooth gradient, a "rod" | continuous convex section mirrors a continuous slice of the lights | flat + edge bevel over 22–28% of the half-width; samples ON the shoulders | `loft` sections; `hard_surface(width=0.0003–0.0005, angle=15)` |
| Shoulders smoothed away | shoulder angle below `hard_surface` angle (30° shoulder, angle 35) | angle below the shoulder angle | `hard_surface(angle=)` |
| No edge highlight line | bevel < 1 px at 1024 | ≥ 1 px at 1024 on hero parts | `hard_surface(width=)`, `mat_metal(bevel_r=)` |
| Uniform plastic sheen | roughness ±0.06 | `rough_var` 0.20–0.24, `scratch` 0.4–0.6 | `mat_metal(rough_var=, scratch=)` |
| Scratches invisible | 1.1 mm specks (noise scale 900) = 0.5 px at 512 | long scratches: noise 25–30, Mapping (60, 60, 1) along the length, ramp 0.64–0.70 | `MB.n`, `MB.ramp`, overlay (§10) |
| Big field with no story | no etched band, mark or inscription | etched panel 12–16 cm: base `#2E2A24`, rough 0.62, a motif | `MB.map_range`, `MB.obj_axis`, `ShaderNodeTexWave` |
| Ornament reads as spikes | length/width > 10, no root mass, no ground | fewer, wider rays touching at the root; dark ground | `loft(tip=)`, `lathe`, `mat_metal('#1B1A1A', rough=0.55)` |
| Focal is a white dot | emissive disc clipped, no inner structure | gem or cabochon with facets; widest clip ≤ 5 px | `gem_cabochon`, `gem_brilliant`, `mat_gem(emit_strength≤1.5)` |
| Leather pink or rose | sheen lifts dark red +20 L* | base darker, rough 0.68–0.72, spec 0.22 | `mat_leather(rough=)`, `set_in(mb.p, IN["spec"], …)` |
| Wire wrap busy but flat | wire/leather ΔL* 11 | ≥ 30 | leather darker; wire gold rough 0.18 |
| Shadow-side edge merges | the rim reaches one side only | low kicker aimed at the dark part | `area_light(name, loc, target, energy, size, size_y=)` |
| Dark bevel on the silhouette | faceted plane mirrors the dark world | strip at the plane's mirror direction, 0.3–0.7× key radiance | `area_light(…, size=0.10, size_y=1.8)` |
| Blown streak after "fixing" | strip radiance above the key's | radiance = energy ÷ area; key 480 W ÷ 1.44 m² = 333 W/m² | `area_light` energy |
| Focal lost after the detail pass | the rest gained local contrast | raise the focal (darker ground, more value steps) or calm the rest | probe `--focal` |
| Materials merge | neighbours differ on < 2 axes | §3 table | `mat_*` parameters |
| Whole part reads as "edge" | AO mask distance > 15% of thickness | scale the mask | `mat_leather(edge=)` |
| Wall or roof reads as a box | courses, quoins, verge only as sub-pixel texture | geometry for quoins, string courses, verge thickness, ridge | architecture.md §5 |
| Ornament floats or looks glued | not sunk | sink 0.2 mm | forms.md |

## 9. Measure it — `value_probe.py`

### 9.1 The probe (Pillow + numpy; copy it next to the renders)

Run outside Blender: `py value_probe.py card.png --mask card_mask.png --tier
legendary --focal 0.24,0.55,0.40,0.74 --region blade=0.56,0.14,0.93,0.44`.
If numpy is missing: `py -m pip install numpy pillow`.

```python
"""value_probe.py - value, contrast and empty-look numbers for one render (Pillow + numpy).
    py value_probe.py card.png [--mask card_mask.png] [--focal x0,y0,x1,y1]
                      [--region name=x0,y0,x1,y1 ...] [--tier legendary]
Boxes are FRACTIONS of the image (0..1). --mask = the alpha pass (art-direction.md 9.2);
without it the subject is "L* > 6" and bloom halos count as subject. Writes
<card>_flat.png (flat interior painted red) and <card>_3val.png (3-value squint)."""
import sys, numpy as np
from PIL import Image
S, SUBJ, FLAT, LO, HI = 1024, 6.0, 2.0, 30.0, 70.0   # width, subject L*, flat RMS, band edges
GATE = dict(flat=(10.0, 25.0), clip=2.0, clip_hot=5.0, clip_w=5, band=15.0,
            sep=70.0, lost=10.0, focal=1.20, cr=4.5)

def lstar(im):                                # sRGB -> linear Y -> CIE L* (0..100)
    a = np.asarray(im.convert('RGB'), np.float64) / 255
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    Y = lin @ np.array([0.2126, 0.7152, 0.0722])
    return np.where(Y > 216 / 24389, 116 * np.cbrt(Y) - 16, Y * 24389 / 27), Y

def box(img, r):                              # mean over a (2r+1)^2 window (integral image)
    k = 2 * r + 1; c = np.pad(img, ((r + 1, r), (r + 1, r)), 'edge').cumsum(0).cumsum(1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / k ** 2

def sel(shape, spec):                         # "x0,y0,x1,y1" fractions -> boolean box
    x0, y0, x1, y1 = map(float, spec.split(',')); h, w = shape; b = np.zeros(shape, bool)
    b[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = True; return b

def row(tag, s):
    v, f = L[s], det[s & inner]
    print(f"{tag:<10} px {s.sum():>6} meanL {v.mean():5.1f} p5-p95 {np.percentile(v, 5):3.0f}-"
          f"{np.percentile(v, 95):3.0f} flat {100 * (f < FLAT).mean() if f.size else 0:5.1f}% "
          f"clip {100 * (v >= 98).mean():4.1f}%")

def gate(name, ok, text):
    print(f"QA_VALUE {name:<10} {text:<52} {'PASS' if ok else 'FAIL'}"); return ok

args = sys.argv[1:]; path, pairs = args[0], list(zip(args[1::2], args[2::2])); opt = dict(pairs)
im = Image.open(path); im = im.resize((S, round(im.height * S / im.width)), Image.LANCZOS)
L, Y = lstar(im)
if '--mask' in opt:
    mk = Image.open(opt['--mask']); mk = mk.getchannel('A') if 'A' in mk.getbands() else mk.convert('L')
    m = np.asarray(mk.resize(L.shape[::-1])) > 127
else:
    m = L > SUBJ
mf = m.astype(float); inner = box(mf, 3) > 0.999            # interior: skip the silhouette edge
bp = box(L, 1) - box(L, 3)                                   # band-pass: features ~3-7 px
det = np.sqrt(np.maximum(box(bp ** 2, 3), 0))                # local detail RMS, L* units
far = ~(box(mf, 24) > 0.001); ff = box(far.astype(float), 40)  # backdrop >= 24 px away
bgl = np.where(ff > 0, box(L * far, 40) / np.maximum(ff, 1e-6), L[far].mean())
v = L[m]; bands = [100 * (v < LO).mean(), 100 * ((v >= LO) & (v < HI)).mean(), 100 * (v >= HI).mean()]
flat, clip = 100 * (det[inner] < FLAT).mean(), 100 * (v >= 98).mean()
c, w = (m & (L >= 98)).astype(float), 0                      # widest clipped shape (erosions)
while c.any(): c, w = (box(c, 1) > 0.999).astype(float), w + 1
edge = (box(mf, 1) > 0.999) & ~(box(mf, 3) > 0.999)          # 1-3 px inside the silhouette
dl = (L - bgl)[edge]
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
    f = m & sel(L.shape, opt['--focal']); rest = m & ~f
    lc = np.sqrt(np.maximum(box((L - box(L, 7)) ** 2, 7), 0))  # local contrast, 15 px window
    ratio, cr = lc[f].mean() / lc[rest].mean(), (Y[f].mean() + 0.05) / (Y[far].mean() + 0.05)
    ok.append(gate('focal', ratio >= GATE['focal'] and cr >= GATE['cr'],
                   f"local contrast x{ratio:.2f} (>=1.20), {cr:.1f}:1 (>=4.5)"))
print(f"QA_VALUE verdict {'PASS' if all(ok) else 'FAIL'} ({sum(ok)}/{len(ok)} gates)")
stem = path.rsplit('.', 1)[0]; rgb = np.asarray(im.convert('RGB')).copy(); fl = inner & (det < FLAT)
rgb[fl] = (rgb[fl] * 0.3 + [178, 0, 0]).astype(np.uint8); Image.fromarray(rgb).save(stem + '_flat.png')
Image.fromarray(np.select([~m, L < LO, L < HI], [0, 60, 140], 230).astype(np.uint8)).save(stem + '_3val.png')
```

### 9.2 The alpha pass (in the asset script, after the beauty render)

```python
bpy.data.objects["Backdrop"].hide_render = True      # backdrop_radial() names it "Backdrop"
s = bpy.context.scene; s.render.film_transparent = True; s.cycles.samples = 8
F.render(os.path.join(OUT, f"{asset}_{MODE}_mask.png"))   # RGBA: alpha = the subject
```

8 samples are enough for coverage (≈ 1 s on the owner's GPU, 25 s on 4 CPU
cores at 1000²). Render it last: it changes the scene.

### 9.3 What the numbers mean, and why the gates sit where they do

- **L\*** (CIE lightness, 0–100) is used because equal L* steps look equal;
  1 L* is about the smallest visible step on a flat patch. Every image is
  resized to 1024 px wide first, so previews (768–1000) and finals (1600)
  compare: the Sunforged flat share reads 34.6% / 34.5% / 32.3% from the
  1600 / 768 / 512 px versions of the same card.
- **flat 10–25%**: detail RMS < 2 L* at the 3–7 px scale (3.5–8 mm on a
  greatsword at 1024). Above 25% the eye finds large areas without one
  designed step — the empty look. Below 10% there is no rest and the asset
  reads busy. The render noise floor measured on the backdrop is 0.03 L*, so
  the 2 L* line measures design, not noise.
- **bands ≥ 15% each**: three values present. Never enough on its own (§2).
- **clipped**: ≤ 2% keeps highlights as glints. Legendary and mythic cores
  clip by calibration (`#FFF3C4` at 7.5 × the hot factor): the Sunforged
  fuller core alone is 58% of its clipped pixels, 4.0–4.5% of the subject,
  3 px wide — hence 5% for those tiers. Widest clipped shape ≤ 5 px: a white
  LINE is light, a white SHAPE is a hole (the over-lit test in §10 reached
  7 px).
- **silhouette**: a 128 px thumbnail averages a 1 px edge with the backdrop
  about 50/50, so a 15 L* step survives as ~8 L* — four times the 2 L*
  step, kept as margin for phone glare. 70% (not 100%) leaves room for
  deliberate lost edges (a cast shadow, the far side of a grip).
  Only valid with `--mask`: the threshold mask swallows bloom halos and read
  the same baseline card 60.8% instead of 67.4%.
- **focal ×1.20**: mean local contrast (15 px window) in the focal box over the
  rest of the subject. Moving the box ±2% of the frame moves the ratio about
  ±0.10, so 1.20 means "clearly the winner". Draw the box tight around the
  focal element, ≤ 15% of the frame. 4.5:1 against the backdrop is the
  contrast ui-forge requires for body text: the focal reads at least as well
  as text on the same phone.

### 9.4 When the probe lies

Bloom halos inflate the threshold mask (use `--mask`); parts darker than
L* 6 fall out of the threshold mask (holes in `_flat.png` are lost parts);
a busy or bright backdrop breaks the backdrop estimate (item cards only, or
a mask on a plain world); boxes are fractions of the IMAGE, so re-draw them
after reframing; the gates are calibrated on one card family (a 1.4 m weapon
at fill ~0.78) — record the numbers of every approved card in lessons.md and
re-tune after five.

## 10. Worked example — the canon Sunforged card

Rendered 2026-09-26 by `examples/sunforged_greatsword.py final` on Blender
4.0.2 (Linux, 4 CPU cores, a build without OpenImageDenoiser: 275 samples,
2 min 32 s). Kept in the owner's repo as
`art/forge/baseline/sunforged_final.png`.

`py value_probe.py sunforged_final.png --tier legendary --focal
0.24,0.55,0.40,0.74 --region blade_tip=0.56,0.14,0.93,0.44 --region
blade_mid=0.39,0.35,0.69,0.62 --region guard=0.24,0.55,0.40,0.74 --region
grip=0.06,0.68,0.28,0.87 --region pommel=0.01,0.85,0.11,0.94`

| Region | Mean L* | p5–p95 | Flat | Clipped |
|---|---|---|---|---|
| Subject (5.53% of the frame) | 52.7 | 8–97 | **34.6%** | 4.0% |
| Blade, tip half | 66.2 | 11–93 | **54.0%** | 0.9% |
| Blade, lower half (fuller glow) | 62.8 | 16–100 | 29.3% | 6.8% |
| Guard + sunburst (focal) | 45.5 | 8–99 | 23.1% | 5.5% |
| Grip | 37.3 | 7–81 | 0.1% | 1.4% |
| Pommel | 36.3 | 7–82 | 7.7% | 1.6% |

Gates: flat 34.6% **FAIL**; clipped 4.0%, 3 px PASS; bands 30.6 / 34.7 /
34.7 PASS; silhouette 67.4% ≥ 15 L*, 17.8% < 8 **FAIL** (alpha pass of the
1000 px control render; failing edges = the shadow side of grip and pommel);
focal ×1.30, 5.8:1 PASS. Blade pixels are 63.5% of the subject.

**Cross-section scan** (pixel column x = 1100 of the 1600 px card, across the
blade): a 3 px edge line peaking at L* 53, a trough of 8–14, a smooth ramp
14 → 92 over ~35 px, a plateau of 90–93 over ~30 px (the softbox mirrored),
then a fade 91 → 6 over ~15 px with no edge line. Not one designed step.

**Diagnosis → fix** (ranked by the probe; the knobs are in the build script):

1. **Rod section** — the lenticular `y = T·(1−|x|^2.2)^0.62` mirrors the key
   as one gradient. Fix: hexagonal section — crowned flat to |x| = 0.74·W,
   edge bevel over the outer 26% down to the edge, sample points ON the
   shoulders, `hard_surface(blade, width=0.0004, segments=2, angle=15)`
   (the shoulder is ~25–30°, below the old `angle=35`).
2. **Ricasso missing** — add 95 mm of flat, unsharpened section above the
   guard (thickness 1.08·T, blunt chamfered edge, a crisp step into the
   blade): a medium plain block between guard and blade.
3. **Sheen too uniform, scratches sub-pixel** — `mat_metal(rough=0.34,
   rough_var=0.22, scratch=0.5)` plus a long-scratch layer and a polished
   bevel band, added through an overlay (below).
4. **No etched band** — an etched panel beside the fuller, z 0.11–0.26 m:
   base `#2E2A24`, roughness 0.62, wave motif (BANDS, scale 70, distortion 6).
5. **Sunburst reads as spikes** — 7 rays per side (lengths 62/85/66/95 mm,
   alternating), root half-width 10 mm, taper exponent 0.55, 2.6 mm proud,
   disc r 30 mm with a stepped face, an amber `gem_cabochon` (r 18.6 mm) as
   the sun, a blackened-iron écusson (`#1B1A1A`, rough 0.55) behind it.
6. **Grip rose and flat** — `mat_leather(base='#3A0F12', rough=0.70)`,
   `F.set_in(leather.p, F.IN["spec"], 0.22)`.
7. **Shadow-side edges merge** — two low kickers aimed at the hilt,
   and a bevel strip ≤ 0.7× key radiance (see test log).

The overlay used for 3 and 4 (only existing API: `get_in`, `IN`, `MB`):

```python
def overlay(mb, key, fac, value):          # mix a new layer over what feeds a Principled input
    sock = F.get_in(mb.p, F.IN[key]); src = sock.links[0].from_socket
    mb.link(mb.mix_col(fac, src, value) if key == 'base' else mb.mix_f(fac, src, value), sock)

m = blade_m; ax = m.math('ABSOLUTE', m.obj_axis('X')); z = m.obj_axis('Z')
w = m.math('MULTIPLY', m.math('SUBTRACT', 1.0, m.math('MULTIPLY', z, 0.22 / L)), W0)
u = m.math('DIVIDE', ax, w)                                   # 0 at the spine, 1 at the edge
overlay(m, 'rough', m.map_range(u, 0.725, 0.755), 0.16)       # honed edge bevel
```

**Test log** (1000 px previews, same camera and rig, 4.0.2 CPU; `--tier
legendary`; silhouette with `--mask` where rendered):

| Variant | Flat | Clipped | Silhouette ≥15 / <8 | Focal | Verdict |
|---|---|---|---|---|---|
| base (canon) | 34.3% | 4.5%, 3 px | 67.4 / 17.8 | ×1.26 | 3/5 |
| + fixes 1–6 | 24.0% | 4.1%, 3 px | (no mask) | ×1.12 | 3/4 |
| + strips 260/140 W + brighter backdrop | 46.4% | 8.6%, 7 px | (no mask) | — | FAIL |
| + fixes 1–6, hilt kickers 700 W ×2 | 14.7% | 5.5%, 3 px | 67.3 / 24.1 | ×1.10 | 2/5 |
| V6_ROW |

What the log teaches: (a) the section and material fixes carry the blade
(blade lower-half flat 30% → 2–3%); (b) a strip on mirror metal is the
light's own radiance — 260 W on 0.18 m² is 4.3× the key and blew the
bevels; (c) detail added to the rest steals from the focal (×1.26 → ×1.10):
every detail pass re-checks the focal; (d) a dark bevel that touches the
silhouette needs its own light edge, or the silhouette drops.

## 11. Checklist — before preview, before final

- [ ] Value plan rendered in three greys; `_3val.png` reads the object.
- [ ] Focal chosen and boxed; one rest area planned away from it.
- [ ] Size ladder 2.5–4× between neighbouring classes; no needles (L/W ≤ 5
      for masses); every tertiary detail ≥ 1 px at 512 or accepted as sheen.
- [ ] Touching materials differ on two axes (§3); metals placed by what they
      reflect; no rose leather, no plastic metal.
- [ ] One history mark, placed by use; wear widths from §6.
- [ ] Scale cues at real size, repeated ≥ 3×.
- [ ] Probe run with `--mask`, `--tier`, `--focal`; `QA_VALUE verdict PASS`
      pasted into the delivery with the region table; `_flat.png` opened.
