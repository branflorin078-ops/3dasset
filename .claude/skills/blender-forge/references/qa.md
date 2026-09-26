# QA — automated gates and the visual critique

## Automated gates (forge.quality_report) — must all pass
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

## Visual critique — inspect every render against all 12
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
Fix the first failing item, re-render the preview, repeat. Only then go final.
