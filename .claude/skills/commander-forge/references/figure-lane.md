# Figure lane — a real human in the hall, never a figurine

The hall figures today come from the `hero3d` stand-in tier: "subdivided
smooth figurine renders with subsurface skin, beveled kit" (game-art-director,
realism lanes) — what the owner calls empty figurines. This lane replaces
them with a real human base, a sculpted or scanned head, the lord's set
FITTED by blender-forge, real skin, eyes and hair, and a hero light — and
measures the result. **The one honest limit: a face is only as good as its
source.** Code imports, fits, shades, lights, bakes, exports and measures;
it never sculpts a face (blender-forge scope).

## 1. Sources and licences — record before use

Every file that enters a figure is written in the asset's `base/LICENCE.md`
(PROPOSAL path): source URL, licence name, a copy of the licence text, the
date checked, who checked. Licences change; a row older than 90 days is
re-checked before a new lord uses it.

| Source | What it gives | Licence (verify at time of use) | Use |
|---|---|---|---|
| MPFB2 (Blender add-on) / MakeHuman | parametric human base, topology built for animation, eyes, eyebrow and hair proxies, a game-engine rig option | code GPL/AGPL; the system assets and exported models are published as CC0 | **default body base**. Generate in a SEPARATE session (the runner's `--factory-startup` does not load add-ons, lessons #22), save `.blend`/`.fbx` into `base/`, then import with `figure_kit.import_base` |
| Blender Studio "Human Base Meshes" bundle | sculpt-ready heads and bodies, clean quads | stated as CC0 at release (2023) | head or body starting point for a sculptor |
| A commissioned sculptor | the lord's head from the face sheet (portrait-lane.md §4) | work-for-hire with full IP assignment in the contract | **default head route** for all 8 lords |
| A licensed head scan (commercial store) | real skin detail and anatomy | EULA must allow: commercial game, distribution inside the app binary, modification; a model release included | skin detail and anatomy only; the identity is re-sculpted to the face sheet (rule: original faces) |
| Image-to-3D from OUR painting | a rough head matching the portrait | the tool's licence (some exclude territories or commercial use; read it) | blockout for the sculptor only; triangle soup, soft features — never final |
| MetaHuman, Daz, Character Creator | photoreal humans | engine, interactive-use and royalty terms apply; licences changed recently | **not a default**: read the current EULA and ask the owner; the photoreal look also fights the painted identity |
| Ripped game models, fan models, scans of a person without a release | — | not ours | **never** |

## 2. The base — proportions, topology, scale

- Metres, +Z up, feet at z = 0, facing −Y (the helm and plate operators'
  convention), origin at the ground between the feet.
- Heroic realism: 7.5–8 heads tall, head (crown → chin) 0.23–0.25 m. Heights
  (PROPOSAL, the lineup needs ±5–8% spread): Alric 1.85 heavy, Rowan 1.83
  lean, Edwin 1.80, Faber 1.78 broad, Fable 1.75 (−4 cm stoop), Godric 1.72
  stocky, Maud 1.72, Elena 1.70 lean. Record the MPFB2 macro values (age,
  muscle, weight, height, proportions) in the lord card.
- Topology (check in the viewport and by `quality_report`): all quads on the
  head and joints; ≥ 3 concentric loops around each eye and the mouth; a
  nasolabial loop; 5-poles away from the mouth corners and eyelids; 3 loops
  across every elbow, knee, shoulder and knuckle; zero non-manifold, loose or
  degenerate elements.
- Hidden skin is deleted only where kit covers it with ≥ 10 mm clearance in
  EVERY hero3d pose (poke-through check below); keep hands, head, neck.
- Skeleton: hero3d's. Confirm its bone names before skinning; if hero3d uses
  the MPFB2 game-engine rig, skin directly; otherwise transfer weights
  (Data Transfer, nearest face interpolated) and let hero3d retarget.
  `forge.export_glb` keeps a skin: on Blender 4.0.2 a subdivided mesh on a
  2-bone armature re-imported with its armature modifier and both vertex
  groups (the subdivision was applied) — tested 2026-09-26.

## 3. The head — detail tiers, eyes, mouth

| Tier | Share of the read | What | Where it lives |
|---|---|---|---|
| Primary | 60% | skull, brow ridge, cheekbones, jaw, nose mass, ear placement | the low mesh (5–8k tris) |
| Secondary | 30% | eyelids and their thickness, nasolabial folds, lip edges, age folds, ear forms | low mesh + baked normal |
| Tertiary | 10% | pores (0.1–0.5 mm), fine wrinkles, scars, stubble | normal map + roughness map |

- Bake high → low with blender-forge: `make_bake_target([low], name)` is not
  used for heads (it joins copies); call `bake_pbr(low, sources=[sculpt])`
  on the retopologised head so the sculpt transfers through the normal
  channel. Raise `extrusion` / `ray_dist` above the largest sculpt-to-low
  distance (typically 3–6 mm on a head) or patches bake empty.
- Eyes: separate sclera/iris mesh + a cornea shell 0.3–0.5 mm proud
  (`figure_kit.mat_cornea`, IOR 1.376, roughness 0.02) + a thin wet strip
  along the lower lid. Sclera is never white: L* ≈ 80–85, warm, faint
  vessels at the corners. The upper lid covers the top 1–2 mm of the iris
  (calm); a full iris ring reads as fear or a doll.
- Mouth closed for all hall poses (no interior needed); lips 0.30–0.38
  roughness (§4).

## 4. Skin — Cycles key-art

`figure_kit.mat_skin` builds the layered skin; the numbers below are its
parameters.

| Parameter | Value | Too low | Too high |
|---|---|---|---|
| Subsurface method | Random Walk (Skin) (4.0+) | — | — |
| Subsurface weight | 1.0 | plastic | — |
| Subsurface radius (R, G, B) | (1.0, 0.37, 0.19) — red scatters furthest | grey, lifeless shadow edge | — |
| Subsurface scale | 0.004 m (range 0.003–0.006 for a real-size head) | plastic | ≥ 0.008 candle wax, ears glow like jelly |
| IOR / Specular IOR level | 1.4 / 0.5 | — | oily sheen everywhere |
| Roughness | map 0.35–0.55: T-zone (forehead, nose) 0.35–0.40, cheeks 0.45–0.52, lips 0.30–0.38, stubble 0.50–0.55, scars 0.30 (and less scatter) | wet, plastic | chalk, dead |
| Mottle | 0.04–0.08 (redness at nose, ears, cheeks; cooler at the jaw) | vinyl toy | blotchy |
| Pores | voronoi 1800 per metre (≈ 0.55 mm cells), depth 0.10–0.14, or the scan's normal | airbrushed | orange peel |
| Albedo | de-lit (no shadows or highlights painted in), L* 35–75 by complexion | — | — |

Older lords (Edwin, Godric, Maud, Faber, Fable): deeper wrinkles in the
normal, rough[1] up to 0.55, mottle 0.07. Younger (Rowan, Elena): finer
pores (2200 per metre), mottle 0.05.

**Godot (real time)** — none of the Cycles subsurface survives glTF. The
GLB carries albedo, ORM and normal. In Godot 4 `StandardMaterial3D` has
`subsurf_scatter_enabled` / `subsurf_scatter_strength` (0.2–0.4 for skin) /
`subsurf_scatter_skin_mode`; it is a screen-space effect that the Godot docs
list for the Forward+ renderer only — check the project's
`rendering/renderer/rendering_method` before relying on it. Fallback on
Mobile/Compatibility: `rim_enabled` (rim 0.1–0.2, rim_tint 0.6) and
`backlight_enabled` with a deep red backlight (`#3A0E08`) masked to ears
and nose (`backlight_texture`); verify both on the target renderer with a
screenshot, then run the look-dev match (§9).

## 5. Hair, beard, fur — the hardest part

| Kind | Game (GLB) | Cycles key-art | Counts / sizes |
|---|---|---|---|
| Head hair | alpha cards: 3 layers — cap (solid mass), clumps, flyaway tips | curve hair with `mat_hair_strands`, or the cards | 60–150 cards, 3–8k tris; strand atlas 1024² with 12–20 clumps |
| Beard, brows | cards (beard 30–80), brows as 6–12 small cards or painted | curves | Fable's beard to the chest is the largest groom in the cast |
| Braid (Elena) | a swept tube (blender-forge `sweep`) carrying a braid texture + 10–20 loose cards | same | tube ≤ 1.2k tris |
| Fur (Alric's pelt, Elena's wolf cloak) | a sculpted clump mesh baked to normal + 40–80 edge cards on the silhouette only | curve fur | the silhouette edge is where fur reads; the interior is a normal map |
| Plume (Rowan) | 8–14 feather cards on a lathed quill socket | same | — |

Melanin for `mat_hair_strands` (PROPOSAL per lord, matched to the
portraits): Alric 0.95, Elena 0.90, Godric 0.60 with random colour 0.2,
Rowan 0.55 with redness 0.5, Edwin 0.70 with grey cards at the temples
(melanin 0.15), Maud 0.30 (iron grey), Faber 0.25 (grizzled), Fable 0.05
(white, redness 0.1).

Godot cards: `transparency = TRANSPARENCY_ALPHA_SCISSOR`,
`alpha_scissor_threshold` 0.5, `alpha_antialiasing_mode` alpha-to-coverage
with MSAA 2×/4×, `cull_mode = CULL_DISABLED`, anisotropy 0.5–0.8 with a
flowmap along the strands (verify each on the target renderer).
A CC0 MakeHuman hair proxy may start the groom; it is restyled to the face
sheet (length, parting, grey) — never shipped as-is.

## 6. Pose — a person standing, not a mannequin

- Contrapposto: weight leg straight, the other knee bent 8–15°, pelvis
  dropped 4–7° on the free side, shoulders counter-tilted 2–4°, head turned
  10–20° toward the key and tilted ≤ 5°.
- Both hands occupied: one on the signature object, the other on the belt,
  a pommel, gloves or the book — never both hanging straight.
- Stance width (heel to heel): 0.20–0.35 m; Maud braced 0.45; Fable narrow,
  leaning on the staff.
- Arms away from the torso enough to open a window of background between
  arm and body in the 128 px silhouette (`windows_128 ≥ 1`).
- The hall idle (breathing, weight shift) is hero3d's; this pose is its
  frame 0. Weapons attach at the grip centre, helms at the bottom of the
  neck ring (blender-forge export.md pivots).

## 7. Kit fitting — the set built onto THIS body

Layers from the skin out (real practice; offsets are the distance from the
skin to the inner face of the layer):

| Layer | Thickness | Offset from skin | Built with |
|---|---|---|---|
| Linen shirt / arming cap | 1–2 mm | 0–2 mm (skin-tight; body shrink-wrap) | Shrinkwrap + Solidify |
| Gambeson / arming doublet | 10–25 mm (quilted) | 2 mm | subdivided cage from the body + quilting sweeps |
| Mail | 4–6 mm (rings ⌀ 8–12 mm, sources.md) | over padding | cage + ring normal/alpha texture; one repair patch |
| Plate over mail and padding | 1.5–2 mm | 10–15 mm over mail; 20–30 mm over a gambeson | `figure_kit.plate_on_body` → `forge.plate` |
| Helm over an arming cap | 1.5–2 mm | head half-width + 10–18 mm | `forge.helm_shell(radius = head half-width + offset)` |
| Surcoat, mantle, cloak | 2–4 mm | draped | cloth simulation, then applied (below) |

- `plate_on_body(body, name, z_bottom, height, offset, arc)` samples the
  body at 3 heights and takes the LARGEST radius per angle, so the plate
  clears the chest and the waist. Arcs: front 185–355°, back 5–175°.
- `forge.plate` `taper` pulls the top edge in by taper × half-width: the
  probe's 0.08 taper on a 0.195 m half-width cut the 25 mm offset to
  `QA_FIT min_clearance_mm 8.76`. Always print `QA_FIT`.
- Gate: `0 < min_clearance ≤ 1.5 × intended offset`, and ≥ 2 mm — below is
  clipping, above is a floating shell. Re-check in the hero3d poses
  (shoulder raised 90°, elbow bent 120°, crouch 30°): poke-through fixes
  go in the kit's weights, never by pushing plates further out.
- Straps: `forge.strap` / `strap_buckle` along a path sampled 1–2 mm above
  the surface; rivets: `rivet_row(surface=plate)`.
- Cloth (mantle, cloak, surcoat): Blender cloth sim on a pinned cage
  (pin group on the shoulders or clasp), collision with body + kit
  (distance 5 mm), quality 8–12, mass 0.3–0.5 kg (wool), tension 15–40,
  bending 5–10 for heavy wool; settle 60–120 frames, apply at the rest
  frame, Solidify 3–5 mm, a sweep for the hem seam. Folds come from this
  geometry, never from a bump (materials.md).
- Several body shapes, one kit: bind kit to the body with Surface Deform,
  drive the body's shape keys (broad / standard / slim), store the result
  as kit shape keys — only if lords.md lets pieces move between lords
  (kit-sets.md §6).

## 8. Light, camera and render (Cycles key-art)

| Shot | Camera | Rig | Size (preview / final) |
|---|---|---|---|
| Bust (card stand-in, look-dev) | `bust_camera(eye, head_h=0.24, fill=0.45, lens=85, fstop=4, yaw=18)` → 1.26 m away, 0.53 m frame height | `hero_rig(eye, yaw=18)` | 384×480 / 1024×1280 |
| Full length (CMF stand-in, hall look-dev) | 85 mm, `forge.frame_fill(cam, parts, 0.86)` (≈ 4.9 m for 1.80 m), f/8 | `hero_rig(chest, dist=4.0, yaw=18)` | 512×768 / 1024×1536 |
| Sworn pair | same camera; `set_sworn(rig, False)` then `True` | — | both sizes |

- Depth of field at 85 mm, 1.26 m: f/2.8 gives ≈ 37 mm in focus (the far
  eye goes soft); f/4 ≈ 53 mm (both eyes and nose sharp) — the bust default.
- The rig (figure_kit defaults, calibrated on the probe): torch key
  `#FFD9A8` 150 W at 2 m upper-left; cool fill at 0.18 of key (5.5 : 1);
  rim behind-right, neutral at 0.6× key, SWORN gilt at 2.2× key; kicker
  0.25×; top 0.12×; eye light 0.03× beside the lens (catchlights). The
  probe measured the sworn pair at ΔL* +6.0, Δb* +8.1 on the rim-side edge.
  `rim_side="left"` puts the rim high behind-left (portraits.md's warm
  upper-left rim) — which side the shipped hall uses is an owner question.
- `forge.backdrop_radial` behind (warm centre `#241A10` → `#030304`), AgX
  Medium High Contrast (render_setup), bloom halo only.
- Every render goes out through `render_with_mask` + `write_meta` so
  `figure_check` can measure it.

## 9. Real time — the GLB for the hall

| Part | LOD0 tris (PROPOSAL; ship-forge owns budgets) | Texture set | Material / draw call |
|---|---|---|---|
| Head + eyes | 5–8k | 2048² albedo, ORM, normal | 1 (+1 cornea if separate) |
| Body (visible skin, hands, neck) + underclothes | 8–12k | 2048² shared | 1 |
| Kit (the set, fitted) | 12–20k | 2048² shared by the four pieces | 1 |
| Hair, beard | 3–8k | 1024² albedo+alpha, normal | 1 |
| Signature object | ≤ 6k | its blender-forge set (1024²) | 1 |
| **Total** | **≤ 45k** | ≈ 25 MiB VRAM (ASTC 6×6: 2.5 MiB per 2048² map with mips) | **≤ 6** |

- LOD1 at 50% tris and 1024² maps for the roster and background lords;
  only ONE lord at LOD0 resident at a time (the hall stage).
- Rarity glow on kit inlay is animated in Godot (`emission_energy`), as
  blender-forge export.md prescribes; the sworn rim is a stage light
  (SpotLight3D) driven by the lord's state — never baked.
- Look-dev match: the Godot hall screenshot beside the Cycles still at the
  same framing: `figure_check` face L* within ±8 and each value band within
  ±5 points. Outside → fix the Godot lights first, then the material.

## 10. The build — commands and folder

```
art/forge/assets/HERO-<lord>/          (id PROPOSAL; hero3d's naming wins)
  base/    body.blend|fbx, head (sculpt + low), hair, LICENCE.md
  build.py modes: fit | preview | pair | final | export | verify
  out/     renders, *_mask.png, *_meta.json, logs, GLB, textures
  REPORT.md
```
```
$fr = "<skills>/blender-forge/tools/forge_run.py"
py $fr run <ABS>/build.py fit     <ABS>/out      # QA_BASE, QA_FIT per piece, QA_PART
py $fr run <ABS>/build.py preview <ABS>/out      # bust + full, 512 px
py <skills>/commander-forge/tools/figure_check.py <ABS>/out/<lord>_bust_sworn.png --pair <ABS>/out/<lord>_bust_unsworn.png --sheet <ABS>/out/check.png
py $fr run <ABS>/build.py final   <ABS>/out
py $fr run <ABS>/build.py export  <ABS>/out      # bake kit, QA_GAME, GLB with skin
py $fr run <ABS>/build.py verify  <ABS>/out      # re-import: meshes, materials, joints; render
```
Start `build.py` from `examples/figure_probe.py` (imports, rig, camera,
mask and meta already wired); swap the stand-in primitives for
`import_base` on the licensed files. The outdir is ABSOLUTE (SKILL rule 11).

## 11. Failure modes — the empty figurine, diagnosed

| Symptom | Measured signal | Cause | Fix |
|---|---|---|---|
| Vinyl toy | face_detail_ratio < 0.9; no pores at 1:1 | no tertiary detail, uniform roughness | pores + roughness zones (§4), scan/sculpt normal |
| Candle wax | ears and nose glow orange; soft shadow edge | subsurface scale ≥ 8 mm | scale 0.004 |
| Plastic | face_clip > 2%; one hot sheen | roughness < 0.3 everywhere, spec 1.0 | §4 map, spec 0.5 |
| Dead eyes | no catchlight; iris ring fully visible | no eye light; cornea rough; lids too open | eye light 0.03×, cornea 0.02, lid overlap 1–2 mm |
| Helmet hair | hair edge solid in the silhouette | cap layer only | clump + flyaway layers, 5–10 flyaways at the edge |
| Floating kit | QA_FIT > 1.5× offset; gap visible at the collar | profile not sampled on the body | `plate_on_body`, 3 samples |
| Clipping | QA_FIT < 0 or skin through plate in a pose | offset ignores taper / pose | taper check; weights; pose test |
| Mannequin pose | windows_128 = 0; arms glued | A-pose from the base | §6 contrapposto, hands occupied |
| Grey soup | band_max > 0.75 | no value plan; flat key | §8 rig, key:fill 5.5 : 1 |
| Lost in the dark | sep_dL < 15 | dark kit on a dark ground, no rim | rim/kicker, lighter backdrop centre |
| Kit outshines the face | face_minus_body_L < 3 | Masterwork glow, polished plate at the key | kit emissive ≤ 3% of pixels; steel `#7E7466` substrate |

## 12. Checklist

- [ ] Every source in `base/LICENCE.md` (URL, licence text, date, checker)
- [ ] Base: metres, facing −Y, 7.5–8 heads, topology rules, `QA_BASE` pasted
- [ ] Head from a sculpt or licensed scan, re-sculpted to the face sheet
- [ ] Skin §4 values; Godot fallback chosen for the project's renderer
- [ ] Hair in 3 card layers; flyaways on the silhouette edge
- [ ] Pose §6; `windows_128 ≥ 1`
- [ ] Every fitted piece `QA_FIT` in range; pose poke-through checked
- [ ] Bust + full renders with mask and meta; `FIGURE_CHECK … fail=0`; sworn `--pair` PASS
- [ ] GLB: ≤ 45k tris, ≤ 6 materials, skin re-imported with joints; round-trip render opened
- [ ] Godot look-dev match within ±8 L*; REPORT.md with every number verbatim
