# Export — from procedural render asset to Godot-ready GLB

## Why baking is mandatory
glTF (and Godot) read image textures + a Principled-style material. Procedural
nodes (noise, AO masks, bevel node, object-space glow masks) do NOT export.
Without a bake, the exported asset is flat grey. Always bake.

## The professional bake: selected-to-active
1. `game = F.make_bake_target(parts, "AssetName")` — duplicates every part,
   applies modifiers, joins the copies into ONE mesh (one draw call).
   Originals stay untouched as bake SOURCES.
2. `F.bake_pbr(game, sources=parts, size=2048)` — for each channel, rays cast
   from the joined mesh onto the original parts (cage extrusion 1.5 mm,
   max distance 6 mm) so each part's own shading transfers exactly.
3. Channels: albedo, metallic, roughness (via emission proxies — a DIFFUSE bake
   returns black for metals), tangent-space normal (captures bump + bevel-node
   highlights), emission (normalised to 0–1 + one strength factor → glTF
   KHR_materials_emissive_strength).
   Emission is measured in a RAW (Non-Color) float buffer and written as an
   8-bit PNG with explicit sRGB encoding, so `strength × decode(png)` returns
   the baked radiance on every Blender version (5.x otherwise encodes into a
   float buffer's declared colourspace — lessons #18).
4. Delete the sources, `quality_report`, `export_glb`.
5. Inspect `info["channels"]` (min, max, mean per map) and
   `info["emission_peak"]`: a black map is a FAIL, and a glowing source must
   come back at its analytic strength (tier strength × hot factor), not merely
   "> 1".

Bakes run on CPU (`bake_pbr(device='CPU')`, the default): selected-to-active is
CPU-bound — Sunforged 1024 five maps: 51 s on 20 cores vs 105 s on OptiX,
identical maps. Renders use the GPU.

## High-to-low: the in-world LOD
`make_bake_target(parts, name, decimate=0.30)` collapses the joined copy to
~30% of its triangles; `bake_pbr(sources=parts)` then casts from the LOW mesh
onto the untouched HIGH parts, so bevels, wire wraps and engraving survive in
the normal map. Sunforged greatsword: ~40k triangle sources → ~12k in-world.
Keep extrusion (1.5 mm) and max ray distance (6 mm) larger than the largest
surface deviation the decimation introduces; raise both if patches bake empty.

## Texture budgets
| Asset class | Texture | Triangles |
|---|---|---|
| Hero weapon / helm (card + inspect) | 2048² | ≤ 40k |
| Equipment in-world | 1024² | ≤ 12k |
| Map unit / prop | 512² | ≤ 4k |
| Castle kit piece | 1024² tiling + trim sheet | ≤ 8k |
UVs: smart project, island margin 0.004; for heroes, hand-seam before baking.

## Orientation and pivots
Build in metres, +Z up, the object's "length" along +Z; the glTF exporter
converts to Godot's +Y up. Pivot at the grip centre (weapons), sole centre
(boots, greaves), base centre (buildings, stands), bottom of neck ring (helms).

## Godot import notes
- Drag the .glb into res://assets/models/…; it imports as a scene.
- Emission strength arrives via KHR_materials_emissive_strength; enable Glow in
  the WorldEnvironment for bloom (strength 0.6–0.9, HDR threshold 1.0).
- For rarity glow in-engine, animate the material's emission_energy for
  "breathing" (legendary ±15% over 3.8 s, mythic flicker ±25% noise).
- Metallic/roughness are merged into one texture by the exporter (glTF ORM convention).

## Naming (matches the art handoff)
`EQ-<tier>-<slot>_<set>.glb` (e.g. EQ-leg-blade_sunforged.glb), textures
`<Asset>_<channel>.png`, one folder per asset. Record every export in the manifest.
