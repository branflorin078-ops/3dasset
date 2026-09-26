# The improve loop — score the gap, fix the worst, repeat

## Render ours to match the reference

Match the dominant reference's camera: museum photos are usually a 3/4 view
from slightly above, on a neutral grey. Render a blender-forge PREVIEW
(768 px) at that angle, THEN run `compare.py`. Comparing a diagonal hero card
with a side photo hides proportion errors.

## The 8 gap axes (score each 0–3, one sentence of visual evidence)

| # | axis | 3 = matches | 0 = missing |
|---|---|---|---|
| 1 | Silhouette | reads as the same class at 64 px | reads as something else |
| 2 | Proportions | every key ratio within 10% of refs | any ratio off by >30% |
| 3 | Construction | every structural element present (rivets, rolls, langets…) | parts float or are missing |
| 4 | Material read | metal/wood/leather each read as themselves | plastic / uniform |
| 5 | Finish + roughness | breakup follows the working direction; finish changes where refs change | one roughness everywhere |
| 6 | Decoration | placement + scale match the refs' logic, survives 256 px | wrong place / wrong scale / noise |
| 7 | Wear logic | wear where use touches, grime in cavities | uniform or random wear |
| 8 | Look fit | matches the owner's boards' palette + stylisation | clashes with the game |
| 9 | Game read *(buildings, map pieces, icons)* | names class + tier at the game's read distance (25% / 44 px) | unreadable at play size |

## Ranked deltas → blender-forge

Fix the THREE lowest axes per loop. Each delta names the part, the operator
or parameter, the old value, the new value, and the reference that justifies it.

| gap | typical delta |
|---|---|
| proportion | edit the loft/lathe profile numbers (radius/height pairs) to the ratio from `measure_cm` |
| missing construction | add a `sweep` rolled edge, `rivet_row` (or instanced lathe rivets), langets as lofts, a strap `sweep` |
| material read | switch `mat_*` preset / base hex to the materials.md row; add the missing layer (edge wear, cavity) |
| finish | set `brush_axis` along the working direction; split one material into two zones by an object-space mask |
| decoration scale | scale ornament to the refs' band-width ratio; sink it 0.2 mm; retest at 256 px |
| wear | shrink/enlarge the AO mask distance (≈15% of the part) — materials.md mask rule |
| look fit | pull palette to the game tokens (GILT #C9A04C, OAK #4A2E1B, IRON #3B4048, WAX #8A1F24) |

## Stop rule
All axes ≥ 2 and no proportion off by more than 10% → done (axis 9 must
reach 3 for buildings and icons: they live at play size). After 5 loops
without that → stop, keep the best version, and report the residual gap with
its evidence (and whether the card-only image route would serve better).

## Record (append to REFERENCE.md each loop)
`loop N · scores [1..8] · deltas applied · compare_loopN.png`
