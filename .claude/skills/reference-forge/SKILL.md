---
name: reference-forge
description: Reference-driven quality loop for Castle Conquest art — searches real, licensed references (The Met and Cleveland Museum Open Access CC0 arms, armour, furniture, architecture fragments with museum measurements, plus the owner's `real art/` boards), extracts proportion, construction, material and wear facts into a scored REFERENCE.md, compares our render side by side, and drives ranked fixes through blender-forge (or corrective deltas through game-art-director) until the gap closes. Use BEFORE building any asset (to brief it on measured facts) and AFTER any preview (to find what separates it from the real thing), for buildings and castle kit as well as props, or when asked to research references, analyse an asset, "make it look real" or "make it better". Also owns the benchmark lane — measuring genre games for readability numbers, never for style.
---

# reference-forge — study the real thing, then close the gap

blender-forge knows HOW to build (lofts, bevels, layered PBR, glow). This skill
knows WHAT the object really is: its true proportions, how it was put
together, how its surfaces age, where decoration sits and at what scale. The
difference between a generic 3D asset and a convincing one is almost always
one of those four facts — and each one is checkable against a reference.

## Hard rules

1. **Study, never copy.** References teach proportion, construction, material
   and wear. They are never traced, reproduced 1:1, or used as textures. Every
   asset combines ≥ 2 references plus its own original twist, and all heraldry
   and ornament is original (blender-forge rule 1).
2. **Licensed sources only.** The Met Open Access objects flagged
   `isPublicDomain` (CC0) — the tool enforces it. The owner's `real art/`
   boards (the game's own visual source of truth). Never another game's art,
   screenshots, or any copyrighted image.
3. **Numbers over adjectives.** Every proportion claim cites a measurement
   (museum cm) and a ratio; every gap is scored, not described.
4. **Look at everything.** Open every reference sheet and every comparison
   image with Read before writing a single finding.
5. **Three kinds of truth, kept separate.** Museum references are the truth for
   CONSTRUCTION and PROPORTION. The owner's boards are the truth for the
   game's LOOK (palette, finish, how stylised). When they disagree, the boards
   win on look and the museum wins on how a thing is built. Genre games
   (the benchmark lane, sources.md) are truth only for READABILITY numbers
   — px sizes, zones, timings — and never appear beside our art.
6. **A reference you did not keep is a claim you cannot defend.** Every
   id cited in `REFERENCE.md` exists in that folder's `refs.json`.

## The loop (follow in order)

1. **Frame the questions** — asset id, class, and the 4 facts to learn:
   proportions, construction elements, material + finish, decoration scale +
   placement (+ wear logic). See [references/analysis.md](references/analysis.md).
2. **Gather** — 6–10 references into `D:/CastleConquest/art/references/<ID>/`:
   ```powershell
   $t = "D:/CastleConquest/.claude/skills/reference-forge/tools"
   py $t/ref_search.py met "<period term>" --out <dir> --n 4 --must "<class words>" [--from 1250 --to 1600]
   py $t/ref_search.py cma "<period term>" --out <dir> --n 3 --must "<class words>" [--type "Arms and Armor"]
   py $t/ref_search.py local "<keywords>" --out <dir> --n 3
   ```
   Period vocabulary per game item: [references/sources.md](references/sources.md).
   Open `<dir>/refs_sheet.png`. Drop off-class hits and search again.
3. **Extract** — write `REFERENCE.md` in the asset folder: the reference
   sheet template from analysis.md, filled with numbers and cited ids.
4. **Compare** — render our preview at the reference's angle (blender-forge
   preview mode), then:
   ```powershell
   py $t/compare.py <our_preview.png> <refs_dir> --out <dir>/compare_loopN.png --pick 1,3,4
   ```
   Open it. Score the 8 gap axes (0–3) in [references/improve-loop.md](references/improve-loop.md).
5. **Fix** — turn the three lowest axes into concrete deltas mapped to
   blender-forge operators and parameters (the delta table in improve-loop.md),
   apply them to the asset's `build.py`, re-render through
   `blender-forge/tools/forge_run.py`, compare again.
6. **Stop** — when every axis scores ≥ 2 and no proportion is off by more
   than 10%, or after 5 loops (then report the residual gap honestly).
7. **Record** — append each loop's scores and deltas to `REFERENCE.md`; add
   any new trap to [references/lessons.md](references/lessons.md).

## Where it plugs in

- **Before a build**: steps 1–3 replace blender-forge's "3 reference facts
  from real history" with measured facts.
- **After a preview**: steps 4–6 are the critique, with a real object beside
  ours instead of a checklist alone.
- **Buildings and castle kit**: the same loop, with the architecture
  checklist (analysis.md) and the render taken FROM THE GAME CAMERA; the
  8 axes are joined by a 9th — *game read* (job prop, roof identity, tier
  silhouette at 25%) from blender-forge `references/architecture.md`.
- **2D painted art**: the same facts brief game-art-director's prompt
  fragments (construction, material behaviour, one honest wear mark);
  the compare step scores a generated image instead of a render and the
  fixes become a corrective DELTA prompt.
- **UI chrome, props**: same loop — the Medieval Art and
  Cloisters departments cover carved panels, caskets, gilt metalwork, seals,
  reliquaries, architecture fragments (sources.md).

## Tools

| Tool | Does |
|---|---|
| `tools/ref_search.py met` | Met API search (q last — see lessons #1), CC0 filter, class filter `--must`, date window, downloads photos, keeps museum measurements, writes `refs.json` + `refs_sheet.png` |
| `tools/ref_search.py cma` | Cleveland Museum Open Access search, CC0 only (`cc0=1`), `--type` class, measurements parsed from the string |
| `tools/ref_search.py local` | ranks the owner's `real art/` boards by keyword |
| `tools/ref_search.py sheet` | rebuilds the contact sheet |
| `tools/compare.py` | our render beside up to 4 references, captioned with measurements |

`tools/_archive/` holds the workflow scripts from the 2026-09-26 runs
(commander kits, every-aspect, shop/gameplay, UI/story). They are records
with that day's paths baked in, not tools; copy a pattern from them, do not
re-run them.
