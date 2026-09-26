# Materials — layered, physically plausible, scaled to the object

## The layer stack (every hero material)
1. **Base colour** — never pure: `mat_*` mixes base, a lighter wear colour, a dark cavity colour.
2. **Roughness breakup** — noise, stretched along the working direction
   (`brush_axis`: blades along their length, plates across).
3. **Edge wear** — AO "inside" mask (convex edges): brighter, smoother.
4. **Cavity dirt** — AO mask (concave): darker, rougher. Grime lives where cloths can't reach.
5. **Micro-surface** — scratches (stretched high-frequency noise → bump).
6. **Micro-bevel** — Bevel shader node into the normal: every hard edge gets a
   thin highlight even on low geometry. Cheapest single realism upgrade.

## Mask scale rule
AO distances must match the part: edge-mask distance ≈ 15% of the part's
thickness/radius. Too large → the whole part is "edge" (pink leather lesson).

## Starting values (tune by eye under AgX)
| Material | Base | Rough | Wear | Cavity | Notes |
|---|---|---|---|---|---|
| Polished steel (dark) | #7E7466 | 0.30 | 0.5 | #2A2016 | darker substrate lets glow read |
| Munition steel | #8A8C90 | 0.42 | 0.6 | #1C1D20 | storage-oil speckle via noise |
| Blued steel | #1E2A40 | 0.28 | 0.4 | #0B0F18 | add Coat 0.2 for oily sheen |
| Blackened iron | #1B1A1A | 0.55 | 0.3 | #080808 | polish only rivet crowns |
| 22k gold | #D6A64A | 0.18 | 0.7 (#F2D38A) | #3A2208 | brushed=False |
| Bronze | #9A6B3A | 0.30 | 0.6 | #2A1A0C | verdigris only in cavities |
| Silver | #C8CCD4 | 0.22 | 0.6 | #2A2C30 | tarnish = cavity grey |
| Oxblood leather | #4A1418 | 0.55 | 0.35 | — | grain 1400, sheen 0.06 |
| Veg-tan leather | #8A5A30 | 0.60 | 0.40 | — | darker at touch points |
| Wool (grey) | #6B6862 | 0.85 | — | — | sheen 0.6, weave 1400 |
| Stone plinth | #3A3834 | 0.78 | — | — | voronoi + noise bump |
| Amber gem | #C4661A | 0.02 | — | — | emit ≤1.5, density 70 |

## Gems
Transmission 1.0, IOR 1.55–1.75, Volume Absorption for depth (density 40–80),
an emissive heart driven by Layer Weight facing so facet centres glow, FLAT
shading on lathed facets. Caustics on (`render_setup` does it) and indirect
clamp 8 against fireflies.

## Cloth
Sheen 0.5–0.7, roughness 0.8–0.9, a wave-band weave bump at object scale
1200–1600. Folds come from geometry (subdivided cage), never from the bump.
