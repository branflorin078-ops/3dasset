---
name: commander-forge
description: Lords (commanders) of Castle Conquest end to end, never empty figurines. Applies design-forge lords.md (roles, skills, talents, pairing, gear sets, fair acquisition) and produces every lord asset with measured quality - the painted portrait lane (game-art-director pipeline, Edwin anchor), the 3D hall figure lane (licensed human base, sculpted or scanned head, blender-forge kit fitted to the body, skin, eye and hair shading, hero lighting, figure_check gates), the map token lane (banner, line icon, small squad), the six four-piece kit sets, lord screens and skill moments. Use for "make the lords look real", "Edwin's portrait", "hall figure", "lord kit", "commander screen", "sworn state", "lord on the map", "new lord". Not for lord numbers (design-forge), a lone weapon or prop (blender-forge), rigs and animation (hero3d).
---

# commander-forge — a lord is a person, a kit and a promise

The owner's standard for lords, in his words: **"not empty figurines — high
quality details and contrast"**, done "like a senior 3D designer with 40 years
of experience". A lord appears in seven places: the hall stage, the lord
screens, cards and lists (portraits), the realm map (token), battle (skill
moments), reports and chat (portrait chips). This skill owns how every one of
them looks and reads, and applies the design numbers that
[design-forge lords.md](../design-forge/references/lords.md) sets.

## Honest scope — what code can build and what it cannot

| Part of a lord | Built by | Can code build it? |
|---|---|---|
| Face, head, body | a licensed human base + a human sculpt or a licensed scan (figure lane); the image model (portrait lane) | **No. Never code-built** (blender-forge scope, game-director rule 8) |
| Hair, beard, fur | cards from a strand atlas; groom by an artist or a CC0 hair asset restyled | partly: card shading, placement helpers, QA |
| Kit: armour, weapons, tokens, signature object | blender-forge operators, fitted with `tools/figure_kit.py` | **Yes** — real forms, layered PBR, tiers |
| Skin, eye, hair materials | `figure_kit.mat_skin / mat_cornea / mat_hair_*` | yes (the texture source must be licensed) |
| Pose | bone rotations on the `hero3d` rig | yes (the rig is hero3d's) |
| Light, camera, render, bake, export, QA | forge.py + figure_kit + `tools/figure_check.py` | **Yes** |
| Painted portrait | game-art-director (`tools/assets.json`, `gen_assets.py`) | the prompt yes; the painting is the image model's |

The quality ceiling of a face is the quality of its source. Say which source
a lord will get, and what tier that means, before any work starts.

## Hard rules

1. **Never code-build a face or a body.** A figure starts from a licensed
   human base; its head from a sculpt or a licensed scan
   ([figure-lane.md](references/figure-lane.md) §1). Every source is recorded
   with its licence, URL and check date before it enters a build.
2. **Design numbers come from design-forge `lords.md`.** This skill applies
   them (states, screens, visuals) and never invents stats, costs or drop
   rates. Sacred balance constants (`CMD_FX_CAP`, the clamp ledger in
   `data/commanders.gd` — path to confirm) are never touched.
3. **One channel, one meaning** ([design.md](references/design.md) §4): the
   rim light on a lord = SWORN only (gilt `#E0BC6A`); kit emission = that
   piece's tier; card frame = lord rarity; house colour = identity; line
   accent = lead troop line; relationship colours = the map only, never on a
   lord.
4. **ART SHOWN BIG.** The lord detail screen gives the figure or painting
   ≥ 45% of screen height (≥ 864 px of 1920); source art ≥ 1.25× its display
   size. Cards never shrink a lord below the face rules of
   [portrait-lane.md](references/portrait-lane.md) §3.
5. **Silhouette before surface.** The 8 lords as black shapes at 128 px: a
   reviewer names ≥ 7 of 8 ([qa.md](references/qa.md) §3). A lord that fails
   is re-posed or re-kitted before any material work.
6. **Value plan before materials.** Three values planned per image: the face
   is the lightest large mass, kit in the mids, ground dark; measured by
   `figure_check` (value bands, edge separation ΔL* ≥ 15).
7. **No plastic, no wax.** Skin roughness map 0.35–0.55, subsurface radius
   (1.0, 0.37, 0.19) × 4 mm (range 3–6 mm), skin highlights clipped on ≤ 2%
   of the face, catchlights in both eyes.
8. **Kit is fitted, never floating, never clipping.** `figure_kit.clearance`
   prints `QA_FIT`; minimum clearance ≥ 2 mm and ≤ 1.5× the intended layer
   offset ([figure-lane.md](references/figure-lane.md) §7).
9. **A set reads as one kit.** Same metal family, finish and motif scale on
   all four pieces; one honest wear mark per piece (equipment.md); the
   Masterwork glow never out-shines the face.
10. **Painted and 3D never mix in one slot class.** A render standing in for
    a painting is tagged `art_status: stand_in` until replaced.
11. **Blender only through `blender-forge/tools/forge_run.py`, with an
    ABSOLUTE outdir.** The runner starts Blender in the script's folder, so a
    relative outdir lands next to the script (measured 2026-09-26).
12. **Numbers or it did not happen.** Every delivery carries the `QA_*`
    lines, the `FIGURE_CHECK` verdict and the opened images; stop honestly
    after 5 critique loops and state the residual gap.
13. **Original only.** Faces described by structure, never by resemblance
    to a real person or an existing character; heraldry and ornament ours;
    genre games teach patterns, never content.
14. **The money-law holds on every lord surface**: no war imagery over a buy
    button; the free path to the lord is shown beside any paid path
    (design-forge monetization rules decide what may be sold).

## The three lanes

| Lane | Output | Where it shows | Reference |
|---|---|---|---|
| Painted portrait | CMD bust 4:5, CMF full length, SGL sigil, SKL skill emblems | cards, lists, chips, reports, chat, lord detail fallback | [portrait-lane.md](references/portrait-lane.md) |
| 3D hall figure | skinned GLB on the hero3d skeleton + Cycles key-art stills | hall stage, lord detail, ceremonies | [figure-lane.md](references/figure-lane.md) |
| Map token | banner GLB + sigil + line icon + squad spec | realm map, marches, rallies, garrisons | [token-lane.md](references/token-lane.md) |

Kit sets feed the figure and the item cards ([kit-sets.md](references/kit-sets.md));
screens are specified for ui-forge ([screens.md](references/screens.md)).

## Workflow (every lord task)

1. **Read state** — `lords.md` (numbers), the lord's rows in
   `data/commanders.gd`, `data/equipment.gd`, `data/attack_data.gd`
   (paths named in the 2026-09-26 mapping scripts; confirm), game-art-director
   `portraits.md` and `equipment.md`, the lord's brief in
   [kit-sets.md](references/kit-sets.md) §3, and the art status of each lane.
2. **Brief** — fill the lord card ([design.md](references/design.md) §2):
   role, lead line, set, signature object, silhouette idea, palette accent,
   face structure, lines needed, skill moment, source per lane.
3. **References** — reference-forge for every kit piece (Met / Cleveland
   CC0 measurements); the owner's `real art/` boards for the look.
4. **Silhouette** — 128 px lineup with the other seven (qa.md §3). Fix
   before surface.
5. **Build the lane** — portrait ([portrait-lane.md](references/portrait-lane.md)),
   figure ([figure-lane.md](references/figure-lane.md)), token
   ([token-lane.md](references/token-lane.md)); kit pieces through the
   blender-forge pipeline with the set rules of [kit-sets.md](references/kit-sets.md).
6. **Measure** — `figure_check` on every figure/portrait render (with
   `--pair` for sworn), blender-forge `quality_report` + 12-point list on
   every kit piece, `QA_FIT` on every fitted piece, the lineup again.
7. **Hand off** — screens to ui-forge ([screens.md](references/screens.md)),
   skill moments to battle-forge, lines to story-forge, ceremonies to
   feel-forge, rig and idle to hero3d, map placement to world-forge.
8. **Prove in engine** — the Godot hall screenshot beside the Cycles
   look-dev still: face L* within ±8, value bands within ±5 points; the core
   gate plus the screen harnesses (qa.md §7).
9. **Record** — `REPORT.md` in the asset folder with the numbers verbatim;
   new traps into [qa.md](references/qa.md) §9; the recipe that worked
   written back into this skill (game-director rule 7).

## Routing

| The request sounds like | Here | Then |
|---|---|---|
| "make the lords look real", "empty figurines", "hall figure" | figure lane | hero3d (rig, idle), feel-forge (hall light) |
| "Edwin's portrait", "a painting of Maud", "commander card art" | portrait lane | game-art-director (prompt row, generate, install) |
| "lord kit", "Alric's greatsword", "the six sets" | kit-sets.md | blender-forge (build, cards, GLB) |
| "lord on the map", "march banner", "token" | token lane | world-forge (placement, LOD), ui-forge (icons) |
| "lord screen", "talent tab", "pairing", "sworn ceremony" | screens.md | ui-forge (build), transition-forge, feel-forge |
| "skill effect", "Maud's ward in battle" | design.md §6 | battle-forge (beats), audio-forge |
| "lord voice lines", "oath text" | design.md §7 | story-forge, l10n-forge |
| "lord stats", "skill numbers", "drop rate", "talent points" | — | design-forge `lords.md`, gameplay-forge |
| "new lord" | design.md §8 + all lanes | design-forge first (SYSTEM.md), then this skill |

## References

- [references/design.md](references/design.md) — applying lords.md: the lord card, roles (proposals), every investment made visible, the channel table, pairing, skill moments, voice, new-lord rules
- [references/portrait-lane.md](references/portrait-lane.md) — painted portraits: ids, sizes and crops, face-structure sheets for all 8, prompt assembly, value plan, critique rubric
- [references/figure-lane.md](references/figure-lane.md) — the 3D human pipeline: licensed sources, topology, head, skin, eyes, hair, kit fitting, pose, light, real-time budgets, forge_run commands
- [references/kit-sets.md](references/kit-sets.md) — the six four-piece sets, the hall lords' signature objects, per-lord visual briefs for all 8, set coherence, kit on the figure
- [references/token-lane.md](references/token-lane.md) — the lord on the realm map: banner, squad, line icon, sizes per zoom, colour rules
- [references/screens.md](references/screens.md) — lord screens for ui-forge: layout, tap counts, states, ceremonies, harnesses
- [references/qa.md](references/qa.md) — gates per lane, figure_check thresholds, silhouette lineup, "empty figurine" diagnosis, calibration record, lessons

## Tools

| Tool | Runs in | Does |
|---|---|---|
| `tools/figure_kit.py` | Blender (via forge_run) | `import_base`, `vgroup_points`, `mat_skin`, `mat_cornea`, `mat_hair_strands`, `mat_hair_cards`, `body_section`, `body_profile`, `plate_on_body`, `clearance`, `hero_rig`, `set_sworn`, `bust_camera`, `render_with_mask`, `write_meta`, `box_corners` |
| `tools/figure_check.py` | Python + Pillow + numpy | fill, silhouette solidity and windows at 128 px, value bands, edge separation, rim ratio, face L*/clip/chroma/detail, sworn pair delta; `--sheet` contact sheet; exit 1 on FAIL |
| `examples/figure_probe.py` | Blender (via forge_run) | smoke test of every figure_kit function on stand-in primitives (never an asset) |
| `tests/test_figure_check.py` | Python | 5 synthetic-image tests → `PASS all 5 tests` |

```
py <skills>/blender-forge/tools/forge_run.py run <skills>/commander-forge/examples/figure_probe.py preview <ABS outdir>
py <skills>/commander-forge/tools/figure_check.py <outdir>/probe_sworn.png --pair <outdir>/probe_unsworn.png --sheet <outdir>/check.png
py <skills>/commander-forge/tests/test_figure_check.py
```
Measured 2026-09-26 in the authoring sandbox (Blender 4.0.2, 4 CPU cores, no
GPU): probe preview 32–59 s, `FIGURE_CHECK … pass=15 fail=0`, tests
`PASS all 5 tests`. Not yet run on the owner's Blender 5.2.1 — run the probe
once there before the first real figure.

## Output contract

Every lord task ends with: the lord card (filled); per lane the files and
their `art_status`; `QA_BASE` / `QA_FIT` / `QA_GAME` / `IMPORT` lines verbatim;
`FIGURE_CHECK` verdicts (and `--pair` for sworn); the 128 px lineup sheet
opened; the source licences recorded; the hand-offs sent (skill, file,
what is asked); and the owner decisions still open, listed separately.
