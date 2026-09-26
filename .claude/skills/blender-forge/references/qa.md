# QA — automated gates, the value gate and the visual critique

Three layers, in this order: the mesh and bake gates (§1), the value and
contrast gate measured on the render (§2), then the eye (§3). A delivery
pastes the numbers of all three (§5). "Looks fine" is not a result.

## 1. Automated gates (forge.quality_report) — must all pass
- non_manifold_edges = 0 · open_boundary_edges = 0 · loose_verts = 0 · degenerate_faces = 0
- uv_zero_area_faces = 0 on anything that will be baked (the silent-black-map trap)
- every baked channel inspected: `bake_pbr(...)["channels"]` gives min/max/mean
  per map (a black map is a FAIL, not a style). Emission: the strength must
  match the source's ANALYTIC peak (tier strength × breathe × hot factor, e.g.
  Sunforged 13.38) — "peak > 1" passed the 5.x colourspace regression (3.054
  for 13.383, lessons #18/#25)
- the runner's exit code is 0 (`--python-exit-code 1`: a script that raised
  exits 1 even when result lines were printed)
- library changes: `py tools/forge_run.py test <outdir>` prints
  `PASS all N tests` — anything else blocks the swap
- triangles within the asset-class budget (export.md)
- uv_layers ≥ 1 and materials = 1 on the exported game mesh
- dimensions within ±10% of the real-world proportion anchors (forms.md)
- ROUND TRIP: re-import the exported GLB, confirm the baked images and emission
  strength are present, and render it (examples/verify_glb.py). What that
  render shows is what Godot receives.
- Topology gates apply to the mesh BEFORE export. glTF splits vertices at
  every UV seam and hard edge, so a re-imported mesh always shows thousands of
  "open" edges — that is the format, not a defect. Post-import, gate only on:
  one mesh, one material, textures present (metallic+roughness arrive packed
  as one ORM texture), emission strength preserved, triangle count unchanged.
Report the numbers verbatim with every delivery.

## 2. Value and contrast gate — `value_probe.py` (the "empty look" gate)

The probe, the alpha pass and the reasoning behind every threshold are in
[art-direction.md §9](art-direction.md). Run it on every preview and every
final, after the render and before the critique:

```
py value_probe.py <card>.png --mask <card>_mask.png --tier <tier> --focal x0,y0,x1,y1 [--region name=box ...]
```

| Gate (1024 px, CIE L*) | Threshold | Catches | Sunforged canon (2026-09-26) |
|---|---|---|---|
| `flat` — interior with detail RMS < 2 L* | 10–25% of the subject | > 25%: the empty look; < 10%: busy, no rest | 34.6% FAIL (blade tip half 54.0%) |
| `clipped` — L* ≥ 98 | ≤ 2% (≤ 5% legendary/mythic) and widest clipped shape ≤ 5 px | blown highlights, glow collapsed to a white shape | 4.0%, 3 px PASS |
| `bands` — dark < 30 / mid / light ≥ 70 | each ≥ 15% | a washed-out or a murky card | 30.6 / 34.7 / 34.7 PASS |
| `silhouette` — edge vs backdrop (needs `--mask`) | ≥ 70% of edge pixels ≥ 15 L*, ≤ 10% below 8 L* | edges that merge at 128 px | 67.4% / 17.8% FAIL (grip and pommel shadow side) |
| `focal` — local contrast, 15 px window | ≥ 1.20× the rest; ≥ 4.5:1 vs the backdrop | a focal that does not win | ×1.30, 5.8:1 PASS |

Rules of the gate:
- `QA_VALUE verdict PASS` is required before preview → final. A FAIL is fixed
  from the diagnosis table (art-direction.md §8), one change per re-render
  while diagnosing, numbers before and after in the log.
- Without `--mask` the silhouette line is INFO only (bloom halos inflate the
  threshold mask: 57.2% threshold vs 67.4% alpha on the same 1000 px render).
- The focal box is drawn TIGHT around the focal element, ≤ 15% of the frame
  (box placement moves the ratio by about ±0.10).
- Each gate caught a different failure in the 2026-09-26 test log
  (art-direction.md §10): `flat` the canon blade (34–36%); `clipped` a strip
  light at 4.3× key radiance (8.6%, 7 px); `bands` a card lit too bright (dark
  band 13.3%); `silhouette` the dark hilt edges; `focal` a detail pass that
  raised the rest (×1.10).
- The thresholds are a PROPOSAL calibrated on one card family (a 1.4 m weapon,
  fill ~0.78, the item-card rig). Record the `QA_VALUE` lines of every card the
  art-critic approves in lessons.md; after five, re-tune the ranges and
  record the change there.
- **Buildings and map pieces** (game camera, architecture.md §2): run the probe
  on the city-close render with `--mask`; focal box = door + job prop. Until
  five approved buildings exist, gate only `flat` and `silhouette` and report
  the rest as numbers.

## 3. Visual critique — inspect every render against all 15
1. Silhouette reads as a black shape at 64 px?
2. Decorated face toward the camera, three-quarter, not edge-on?
3. Fills ~75% of a square frame; nothing clipped by the frame edge?
4. Every hard edge carries a thin highlight (bevel + micro-bevel)?
5. Roughness varies across each surface (no uniform plastic sheen)?
6. Wear sits where use would put it; cavities hold grime?
7. Glow shows three layers (core/body/haze), not a white line?
8. Glow lights its neighbours (guard, grip, underside shadows)?
9. Tier reads in half a second from rim + glow colour alone? (judge the 128 px
   row of `tools/rarity_sheet.py … --thumb 128`, all tiers side by side)
10. Gems show depth and facets, not a flat disc?
11. Ornament scale survives 256 px?
12. Background clean: no light spill blobs, no banding?
13. **No empty look**: open `<card>_flat.png`. No red field covers more than
    ~30% of any part except the one planned rest area; every large plane
    carries a designed value step (edge-bevel line, grind line, fuller walls,
    an etched or engraved band, scratches ≥ 1 px at 1024). A smooth gradient
    across a whole plane is a FAIL even when the gate numbers pass.
14. **Value plan holds**: `<card>_3val.png` reads the object in three values;
    the focal is where the plan put it; touching materials differ on two
    axes (art-direction.md §3) — no rose leather, no plastic metal.
15. **Edges separate and ornament has mass**: no dark plane touches the
    silhouette without a light edge line; ornament meant as mass has
    length/width ≤ 5 at card size (no "spikes"); one history mark, placed by
    use.
Fix the first failing item, re-render the preview, repeat. Only then go final.

## 4. Critique protocol (art-critic)

1. Open the render at 100%, then at 512, 256 and 128 px (the read distances
   of the card). Never approve an image you did not open.
2. Run `value_probe.py`; open `_flat.png` and `_3val.png`.
3. Rank the failures by the order of work — shape → value → materials →
   detail — not by the order found. A shape or value fault is fixed before any
   material or detail note, because it changes everything after it.
4. Write each fix as a knob and a number (art-direction.md §8), never an
   adjective: "edge bevel 26% of the half-width, `hard_surface(angle=15)`",
   not "make the blade more interesting".
5. After each re-render, re-run the probe and check the focal again: detail
   added to a rest area lowers the focal ratio (×1.26 → ×1.10 in the test log).
6. Stop when the verdict is PASS and items 1–15 hold, or after 5 loops — then
   report the residual gap with its numbers.

## 5. Delivery report (paste with every preview and final)

```
QA      {quality_report of each hero part}
QA_GAME {quality_report of the game mesh}      BAKE channels + emission_peak
QA_VALUE flat / clipped / bands / silhouette / focal / verdict   (+ region table)
CRIT    items 1–15: PASS or the first FAIL and its fix (knob + number)
FILES   card, _mask, _flat, _3val, tier sheet, round-trip render
```
