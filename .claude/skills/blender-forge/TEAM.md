# blender-forge — the agent team

Five roles. One writer per file. One Blender at a time. Numbers, never "looks fine".

## Roles and ownership

| Role | Owns (the only writer) | Does | Never |
|---|---|---|---|
| **skill-engineer** (one) | `lib/forge.py`, `tests/`, `tools/`, `examples/`, `SKILL.md`, `references/*.md`, `TEAM.md` | fixes and extends the library test-first; keeps 4.0–5.x compatibility; calibrates tiers/bloom by render strip; answers builders' library requests | edits a builder's asset script; swaps an untested library |
| **forge-builder** (one per asset, many in parallel) | its own asset script + outputs (e.g. `art/forge/<asset>/`) | follows the SKILL.md pipeline (brief → blockout → real forms → materials → preview → critique → final → bake/export → round trip); starts from `examples/_template_asset.py`; reports `QA_*` lines verbatim | edits `lib/forge.py` (send the skill-engineer a minimal repro script instead) |
| **art-critic** | critique notes only | inspects every render against the 12-point list in `references/qa.md` and the canon card `art/forge/baseline/sunforged_final.png`; ranks fixes; approves preview → final | edits scripts; approves an image it has not opened |
| **qa-engineer** | QA verdicts | runs `forge_run.py test`; checks `quality_report` gates, bake channel stats (`bake_pbr(...)["channels"]`, emission strength), the GLB round trip (`examples/verify_glb.py`), budgets (`references/export.md`), the 128 px tier read (`tools/rarity_sheet.py --thumb 128`) | passes a delivery without pasted numbers |
| **godot-integrator** | Godot-side files for the asset (`godot/assets/models/...`, import settings) | imports approved GLBs; sets emission energy + WorldEnvironment glow (export.md); verifies in-engine; reports mismatches back | changes Blender outputs or the library |

## The lock — one Blender at a time

- **`py tools/forge_run.py` is the ONLY way to launch Blender.** Never call
  `blender.exe` directly, never kill a Blender process, never run renders or
  bakes in parallel.
- The runner serialises every job through `~/.blender_forge.lock`, served
  **first-come first-served**: each waiter holds a heartbeat ticket in
  `~/.blender_forge.queue/` and only the oldest live ticket may take the lock.
  `py tools/forge_run.py status` shows the holder and the queue.
- It runs Blender with `--factory-startup` (no user add-ons in a production
  job) and `--python-exit-code 1` (a script that raises exits 1 — check it).
- Full log in `<outdir>/<mode>.log`; the console gets result lines only
  (`QA_ RENDER BAKE GLB CARD SHEET TEST PASS FAIL` and tracebacks).
- Long jobs: launch in the background and poll the log; the queue may be
  several jobs deep while eight builders work.

## Library change protocol (skill-engineer)

1. Reproduce on the real data at tiny resolution (lessons #16); write the
   failing test in `tests/` first.
2. Edit a STAGED copy: `art/forge/_staging_lib/forge.py`; run the suite
   against it: `$env:FORGE_LIB='D:/CastleConquest/art/forge/_staging_lib'`
   then `py tools/forge_run.py test <outdir>` (the runner honours a preset
   FORGE_LIB).
3. Only when the WHOLE suite is green: copy to `lib/forge.py.new`, then
   `Move-Item -Force` over `lib/forge.py` (atomic — builders import it live).
   Re-run the suite against the live file. Snapshot every live version.
4. Record the change below; add a numbered lesson when a mistake taught one.

## Library changelog

- **2026-09-26 v1 (07:29)** — `bake_pbr` emission fixed for Blender 5.x
  (measured in a raw float buffer, written as explicit 8-bit sRGB; 5.x had
  read the sRGB OETF of the peak: 3.054 for a true 13.383 — lessons #18).
  **Any GLB baked on 5.2 before 07:29 has emission_strength = OETF(peak):
  re-export it.** `gpu_setup` survives `reset_scene`; bakes pinned to CPU
  (2x faster than OptiX for selected-to-active); `bake_pbr` returns
  `channels` min/max/mean and `emission_peak`.
- **2026-09-26 v2 (07:49)** — tiers calibrated on 5.2 (`common` added; rare
  2.6, epic 4.0, mythic 6.0, saturated cores); `retier()` re-tiers a built
  asset in place; 5.x bloom calibrated (Size 0.0625, Strength 0.40: halo,
  not haze) with `render_setup(bloom_strength=, bloom_size=)`;
  `denoise_available()` no longer caches "no denoiser" when no camera
  exists yet; `render_setup(bloom=False)` detaches an earlier bloom.
- **2026-09-26 v3** — operators: `helm_shell`, `slot_cutter` +
  `boolean_cut` (per-shell, local weld), `plate` (lames, rolled edges),
  `rivet` / `rivet_row` (instanced, surface-snapped), `strap` / `buckle` /
  `strap_buckle`, `gem_brilliant` (73 planar facets), `gem_cabochon`;
  helpers `resample`, `path_frames`. `frame_fill(cam, objs, fill)` dollies
  IN or OUT (lessons #28); `mat_leather(edge=)` scales the burnish mask to
  the part (lessons #9). `uv_zero_area_faces` no longer crashes
  on a join without an active UV layer. Runner: FIFO queue,
  `--python-exit-code 1`, `test` / `status` commands.
- **2026-09-26 (no library change)** — `examples/armour_kit.py` promoted:
  Met-measured sallet proportions, 3:2 frame + `aim_at_silhouette`
  (lessons #31). Live `lib/forge.py` = staged = `_bisect/forge_v3` (hashes
  equal); suite `PASS all 28 tests`.
