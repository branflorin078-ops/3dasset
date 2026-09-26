# Token lane — the lord on the realm map

**The pattern (our words):** at map distance an army is shown as a small
squad of a few figures, the commander's banner and a troop-line icon —
never a count-true crowd — so it reads and renders the same at 500 troops
or 50,000. **Our version:** the LORD is recognised by the lord's own banner (house
field + division + sigil), the squad shows the lead line and its tier, and
the relationship (self / ally / enemy / neutral) lives in a reserved ring
and the march line — never in the banner.

Owners around this lane: world-forge (placement, marches, LOD, map
performance), hero3d (the people rig that walks the squad), ui-forge (line
icons — Blender-made art — and name plates), battle-forge (squads in
battle), design-forge world.md (zoom levels), game-art-director
readability.md (the relationship channel). This lane delivers: the banner
GLB per lord, its sigil texture, the lord's map figure, the token
composition spec and the read tests.

## 1. Token anatomy

| Part | What it is | Real size | Built by |
|---|---|---|---|
| Banner | pole, crossbar, finial, cloth with the house field, division and sigil | pole 2.6–3.0 m (Edwin's standard ≈ 2.6 m), cloth 0.9 × 1.2 m, then ×1.6 for the map read (forms.md: ornament scaled up ~1.6×) | blender-forge (this file §3) |
| Lord map figure | the hall figure's map LOD walking at the front: same helm silhouette, mantle colour, signature object | 1.7–1.85 m | figure lane → LOD (§6) |
| Squad | 1 / 3 / 5 figures of the lead line at the march's top tier | 1.7 m | hero3d people rig + soldier kit |
| Line icon | the lead line's icon, the line accent as its rim | 36–44 px on screen | ui-forge + blender-forge |
| Relationship ring | a ground ring under the token, reserved colours + shape | ⌀ 2.5–3.5 m | world-forge (decal or mesh) |
| Name plate | lord name + level, l10n string | UI | ui-forge |

Squad size by the march's strength (PROPOSAL; combat.md or lords.md may
band it differently): 1 figure below 20% of the lord's march capacity,
3 figures 20–60%, 5 above 60%. Never more, never count-true.

## 2. Zoom levels and sizes (px on a 1080 × 1920 screen)

The zoom model belongs to transition-forge / world.md; these are the
token's targets at the map's three distances (PROPOSAL):

| Map distance | Shown | Token height | Banner cloth | Figures | Line icon | Relationship |
|---|---|---|---|---|---|---|
| Near | lord figure + banner + squad | 110–150 px | ≥ 40 px tall | 34–44 px | 44 px | ring + march line |
| Mid | banner + squad of ≤ 3 | 60–80 px | ≥ 26 px | 20–26 px | 36 px | ring + march line |
| Far | a banner-shaped marker only (impostor) | 28–36 px | the marker IS the banner | none | hidden | ring + march line |

- Switch with Godot 4 `visibility_range_begin` / `visibility_range_end` on
  the squad and figure nodes, `visibility_range_begin_margin` /
  `_end_margin` at 10–15% of the range for hysteresis (no popping when the
  camera rests on a threshold), fade mode per world-forge.
- The far marker is the banner's silhouette (field + division), not a
  generic pin: the lord stays recognisable at the realm view.

## 3. The banner — build recipe (blender-forge pipeline)

- **Finial**: blender-forge `examples/_template_asset.py` already builds a banner-pole
  finial (lathed socket, wire wrap, bulb, spike); each lord's finial is a
  variant of it with the set motif (kit-sets.md §4).
- **Pole and crossbar**: `lathe` profiles with a 2–3 mm bevel, iron
  ferrule at the foot. forge.py has no wood material; use the dark-oak
  material of the EQ-banner build (`art/forge/assets/EQ-banner/`) or ask
  the skill-engineer for a tested `mat_wood` (library change protocol).
- **Cloth**: a subdivided cage (never a flat quad), 2–3 folds modelled,
  hem and pole sleeve as `sweep`s; the SGL sigil painting as its texture.
- **Motion**: Godot vertex shader, not a baked clip (animation.md: a shader
  is cheaper for 100 flags): wave amplitude 2–4% of the cloth length,
  0.6–0.9 Hz, phase running along the cloth, pinned at the pole edge by a
  UV mask; phase randomised per token.
- **Budget** (map unit class, export.md ≤ 4k / 512²): banner ≤ 800 tris,
  256² albedo+normal; pivot at the base centre.
- Round trip through `examples/verify_glb.py`; tier glow never appears on a
  banner.

## 4. Colour and shape on the map

| Channel | Rule |
|---|---|
| Relationship (reserved) | saturation ≥ 70% on ring and march line; shape-coded so colour-blind players read it: PROPOSAL if readability.md has none — self solid ring, ally double ring, enemy notched ring (8 notches), neutral dashed ring |
| House colour on the banner | muted: HSV saturation ≤ 45%, value ≤ 60%, so it never competes with the ring |
| Identity | field colour + DIVISION + sigil. PROPOSAL divisions: Edwin per pale, Alric per bend, Elena per chevron, Rowan paly (tourney stripes), Godric per fess, Maud quarterly; existing SGL rows win |
| Line | the line accent only on the icon's rim (infantry #B4432E, spearmen #8B8F95, archers #4F7A4A, crossbows #6D8AA8, cavalry #C9A76A) |

- Measured contrast: a single-token crop over its local ground passes
  `figure_check --kind token` (sep_dL_128 ≥ 18) under the DARKEST map light
  the game uses (fog, dusk).
- The division carries identity when two houses share a hue (kit-sets.md §5).

## 5. Motion rules

- Gait from the people rig; stride × cadence = march speed; foot sliding
  ≤ 5% of the stride (measure on a 60-frame capture).
- The lord figure walks 0.5–1 body length ahead of the squad, facing the
  march direction; the banner bearer is the squad's first figure.
- Turns rotate over 200–300 ms (ease-in-out), never snap; arrival: squad
  settles, banner planted, idle.
- Rallies and garrisons: the leading lord's banner on the front token; a
  joined lord adds a small pennant in that house's colours, never a second full
  banner (one lord per token reads fastest).

## 6. The lord's map figure (LOD of the hall figure)

| Property | Value (PROPOSAL; world-forge measures the frame budget) |
|---|---|
| Triangles | ≤ 1.5k (hall figure decimated, kit merged, no hair cards: a hair mass mesh) |
| Texture | 256² atlas baked from the hall figure's sets (bake selected-to-active, figure-lane.md §9) |
| Must keep | helm or head silhouette (kit-sets.md §3 "head at 44 px"), mantle colour, signature object |
| Drops | face detail, rivets, straps, glow |
| Whole near token | ≤ 6k tris (figure 1.5k + 4 squad × 0.9k + banner 0.8k), ≤ 4 materials |

## 7. Read tests

1. Game-camera screenshots at the three distances with 20 tokens in mixed
   relationships (world-forge's camera, not a staged one).
2. Timed read at the mid distance: relationship ≤ 0.5 s, which lord
   ≤ 1 s, which line ≤ 1 s (a reviewer names them; 18 / 20 correct).
3. `figure_check --kind token` on single-token crops over their ground.
4. The same screenshot through a deuteranopia and a protanopia simulation:
   relationships still separable by ring shape.
5. Harnesses around it: `map_trap_probe`, `pm_render_probe`, `a11y_audit`
   (qa.md §7).

## 8. Failure modes

| Failure | Looks like | Cause | Fix |
|---|---|---|---|
| Crowd soup | 40 soldiers per march, frame drops | count-true display | squad bands §1 |
| Friend or foe? | a green-house lord reads as "self" | house colour saturated like the relationship | §4 muting + ring shape |
| Anonymous army | every token looks alike at mid | banner too small, no division | cloth ≥ 26 px, divisions §4 |
| Popping | squads flicker at a zoom rest point | no hysteresis | visibility margins 10–15% |
| Flat flag | a stiff textured quad | no cage, no shader | §3 cage + wave shader |
| Skating | squad slides over the ground | gait not tied to speed | stride × cadence = speed |

## 9. Checklist

- [ ] Banner GLB per lord: ≤ 800 tris, 256², round-trip render opened
- [ ] Field + division + sigil unique per lord; saturation ≤ 45%
- [ ] Squad bands and LOD ranges agreed with world-forge
- [ ] Lord map figure ≤ 1.5k tris keeps the head silhouette
- [ ] Read test 18 / 20 at mid distance; colour-blind check passed
- [ ] `figure_check --kind token` PASS on crops; numbers in REPORT.md
