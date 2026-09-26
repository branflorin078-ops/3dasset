---
name: blender-forge
description: Professional 3D asset production in headless Blender for Castle Conquest — weapons, armour, equipment, props, UI icon objects, city buildings and their 6-tier evolution, castle kit pieces, map set-pieces and animated props — built from real forms (lofted cross-sections, lathed profiles, swept curves), finished with layered PBR materials and rarity glow tiers, rendered as item-card art, and baked to game-ready GLB for Godot. Use for any request to model, render, bake, animate or export a 3D asset, or to improve an existing Blender asset. Not for character faces or organic figures (see scope).
---

# blender-forge

A tested toolkit (`lib/forge.py`) plus the craft rules that separate professional
assets from "primitives stacked on each other." Proven end-to-end on the
Sunforged Daybreak Greatsword (`examples/sunforged_greatsword.py`).

## Scope — be honest about it

**This skill excels at:** hard-surface and crafted objects — swords, axes, bows,
shields, helms, armour plates, jewellery, gems, chests, banners on poles, siege
engines, castle walls/towers/gates, furniture, props — and their item-card renders.

**This skill does not build:** faces, bodies, animals, or any organic hero
character. Code cannot sculpt a face. Route characters through the image pipeline
(commander-forge) or image-to-3D + retopo; this skill may then finish, light,
bake, and export them. Never code-build a person as a final asset.

## Hard rules

1. **Original designs only.** Never replicate another game's item, logo, or
   character. Real history is the reference library; the design is ours.
2. **No primitive is ever final.** Cubes, cylinders and spheres are blockout
   only. Every final part is a loft, lathe, sweep, or subdivided/bevelled form
   with a designed cross-section (see references/forms.md).
3. **Every hard edge is bevelled** (geometry bevel + weighted normals, plus the
   micro-bevel shader node). Perfectly sharp edges are the #1 CG tell.
4. **Every material is layered**: base + roughness breakup + edge wear + cavity
   dirt + micro-surface. A single flat Principled BSDF is a blockout material.
5. **Glow is a light source with contrast** — dark substrate, three-layer
   emission, calibrated per tier under AgX (references/glow.md).
6. **Nothing ships without a bake.** Procedural materials do not survive glTF.
   Bake selected-to-active to one texture set, then export (references/export.md).
7. **Every asset passes the QA gates** before it is shown or exported
   (references/qa.md). Report the numbers, never "looks fine."
8. **Look at every render** and critique it against the checklist before
   iterating. A render you did not inspect is not a result.

## The pipeline (follow in order)

1. **Brief** — asset id (EQ-*/CMD-*/CST-*), tier, silhouette idea, 3 reference
   facts from real history, one original twist, target triangle budget.
2. **Silhouette blockout** — primitives only, judged as a black shape at 64 px.
   If the silhouette doesn't read, nothing later will save it.
3. **Real forms** — replace every blockout part with loft/lathe/sweep builds.
   Primary forms 60% of visual weight, secondary 30%, tertiary detail 10%.
4. **Hard-surface finish** — `hard_surface()` / `subsurf()` per part.
5. **Materials** — `mat_metal`, `mat_leather`, `mat_cloth`, `mat_stone`,
   `mat_gem`, then `add_glow()` with object-space masks. Rarity is per
   INSTANCE in Castle Conquest (common/rare/epic/legendary = Issued/Sound/
   Fine/Masterwork): build the geometry ONCE, wire `add_glow` once, and
   `retier(tier, rig=rig)` re-colours glow, embers and rim in place.
6. **Stage and render** — `studio_rig`, `camera`, `backdrop_radial`,
   `render_setup` (AgX, bloom, denoiser probe), then `frame_fill` (in or out,
   fill 0.78) or `frame_camera` (push-back only). Preview first (768–1000 px);
   final only after the critique passes. Tier sheet: a `tiers` mode that
   loops `retier` with an identical camera + rig, tiled by
   `tools/rarity_sheet.py --thumb 128` (the half-second read test).
7. **Critique** — inspect the image against references/qa.md; fix; re-render.
8. **Bake and export** — `make_bake_target` → `bake_pbr(sources=...)` →
   delete sources → set pivot → `quality_report` → `export_glb`. Canonical
   orientation, pivot at the grip centre (weapons) or base centre (everything
   else), metres, length along +Z (becomes +Y in Godot).
9. **Buildings and map pieces** swap steps 6–7 for the strategy camera:
   approve from the game camera at the three read distances, render the
   6-tier strip, and run the building QA in `references/architecture.md`.
   Animated props (lids, gates, engines) add `references/animation.md`.
10. **Round-trip proof** — re-import the GLB and render it
   (`examples/verify_glb.py` pattern). Deliver that render alongside the card:
   it is exactly what Godot receives.

## Library quick reference (lib/forge.py)

| Area | Functions |
|---|---|
| Scene | `reset_scene`, `render_setup(bloom_strength=, bloom_size=)`, `denoise_available`, `gpu_setup`, `world_dark`, `backdrop_radial`, `floor`, `render` |
| Light/camera | `studio_rig`, `area_light`, `camera`, `frame_fill` (in or out), `frame_camera` (push back), `look_at`, `bounds` |
| Forms | `loft(tip=)`, `lathe(cap=)`, `sweep(closed=)`, `helix`, `resample`, `path_frames`, `to_mesh`, `hard_surface`, `subsurf`, `flat`, `assign`, `apply_mods`, `join` |
| Armour / jewellery operators | `helm_shell` (bowl + tail/brim, rolled rim), `slot_cutter` + `boolean_cut` (sights, slits, holes), `plate` (profile, lames, rolled edges), `rivet` / `rivet_row` (instanced, surface-snapped), `strap` / `buckle` / `strap_buckle`, `gem_brilliant` (73 real facets), `gem_cabochon` — see references/forms.md |
| Materials | `MB` builder (`map_range`, `obj_axis`, `ramp`, `mix_col`, `mix_f`, `math`), `mat_metal`, `mat_leather(edge=)`, `mat_cloth`, `mat_stone`, `mat_gem`, `hex_lin`, `srgb_encode` / `srgb_decode`, `set_in` |
| Glow | `TIERS` (common, rare, epic, legendary, mythic), `add_glow`, `ember`, `retier` |
| Game | `make_bake_target(decimate=…)`, `bake_pbr` (returns `channels` stats), `uv_unwrap`, `uv_zero_area_faces`, `export_glb`, `quality_report` |

Usage from any Blender script:
```python
import sys; sys.path.insert(0, "<skill>/lib"); import forge as F
```

## Environment notes (measured 2026-09-26)

- **Launch Blender only through the runner**:
  `py tools/forge_run.py run <script.py> <mode> <outdir> [extra]` — it finds
  Blender (5.2.1 LTS here, not on PATH), serialises jobs through ONE lock
  served first-come first-served (`… status` shows the queue), runs with
  `--factory-startup` (user add-ons such as MCP bridges never load) and
  `--python-exit-code 1` (a script that raises exits 1), and logs to
  `<outdir>/<mode>.log`. `… chain <script> <outdir>` = export → verify → final.
- **Windows / PowerShell 5.1**: no `&&` — chain with `;`. Paths with spaces in
  quotes. Long jobs: run the runner in the background and poll the log.
- **GPU**: `render_setup` → `gpu_setup()` picks OptiX > CUDA > HIP > Metal >
  oneAPI (RTX 3500 Ada via OptiX here; the "HIPEW" warning is harmless) and
  re-applies it after every `reset_scene()`. Bakes stay on CPU (`bake_pbr`
  default): the Sunforged 1024 bake is 51 s on 20 cores vs 105 s on OptiX.
- **Timings on this machine** (5.2.1, OptiX, 20 cores): regression suite
  7 s in Blender, 10 s wall · 768² / 48-sample preview ≈ 2 s per render ·
  5-tier strip at 768² 13 s · armour-kit 1200×800 preview 7 s · Sunforged
  chain 58 s (export with 1024 bake 39 s, verify 7 s, 1600² final 11 s) ·
  template export 5 s. Queue waits come on top while
  builders are busy. Single-core fallback: preview 1000² ≈ 2 min, 1024²
  bake ≈ 8 min, final 1600² ≈ 10 min — chain, never parallel.
- **Blender 4.0 – 5.x**: handled in the library — compositor node group vs
  `scene.node_tree` (5.0), Glare sockets vs properties (4.5), Principled
  names via `set_in`/`IN`, auto-smooth (4.1). Bake colourspaces are explicit
  (lessons #18). Only 5.2 is installed here: 4.x branches are kept but not
  exercised on this machine.
- **Staged library**: to test a candidate `forge.py`, set
  `$env:FORGE_LIB='<dir with forge.py>'` before the runner; every example and
  the suite import from `FORGE_LIB` when it is set.

## Regression suite — one command, < 1 min

```
py tools/forge_run.py test <outdir> [-k <substring>]
```
28 tests: forms watertight (loft tip, lathe caps, sweep weld), every `mat_*`
builds and renders, tiers + `retier`, a known-strength glowing bake returns
that strength and decodes back, GLB round trip (1 mesh, 1 material, emission
strength, triangles), `render_setup` on this Blender (bloom, GPU after reset,
denoise probe, `frame_fill`), and every operator watertight. Plain-Python
runner check: `py tests/test_runner_queue.py tools/forge_run.py`
(FIFO + mutual exclusion on a temp lock). Run the suite after ANY library
change; `PASS all N tests` or it did not happen.

## Tools and team

- `tools/forge_run.py` — the ONLY way to launch Blender (above).
- `tools/rarity_sheet.py` — Pillow: tile N labelled PNGs (tier accents read
  from `TIERS`) + a `--thumb 128` read-test row. `py tools/rarity_sheet.py
  out.png a.png b.png … [--labels …] [--title …] [--thumb 128]`.
- `examples/_template_asset.py` — start every new asset here. As shipped it
  builds a probe finial: `py tools/forge_run.py run examples/_template_asset.py
  preview <outdir> [tier]` is the one-command smoke test (`tiers`, `export`,
  `final` too).
- `examples/sunforged_greatsword.py` — the canon build (`tiers` mode renders
  the ladder); `examples/armour_kit.py` — every armour/jewellery operator in
  one still life; `examples/verify_glb.py` — round-trip proof for any GLB.
- `TEAM.md` — the five roles (skill-engineer, forge-builder, art-critic,
  qa-engineer, godot-integrator), who owns which files, the lock, and the
  library changelog.

## Reference files — read the relevant ones before building

- `references/forms.md` — cross-section design, loft/lathe/sweep recipes, proportions
- `references/materials.md` — per-material values, layering, scale of noise
- `references/glow.md` — rarity tiers, masks, contrast, bloom, embers
- `references/lighting-render.md` — rigs, hero composition, backdrop, sampling
- `references/export.md` — bake selected-to-active, textures, GLB, Godot, budgets
- `references/architecture.md` — buildings, castle kit, tier evolution, map read distances, owner-colour masks
- `references/animation.md` — prop animation, clips, pivots, rigging scope
- `references/qa.md` — automated gates + visual critique checklist
- `references/lessons.md` — real mistakes from real iterations; read first
