# Architecture — city buildings, castle kit, map set-pieces

Hero props are judged on a card at arm's length. Buildings are judged from a
fixed strategy camera at three distances, hundreds at a time, on a phone. That
changes almost every rule. Read this before any building, wall, gate, tower,
camp or map set-piece. (Integration, placement and the shipped low-poly kit are
`castle-forge`'s; the 34 archetypes × 6 tiers live in
`tools/blender/generators/buildings.py`. This file is how to author them well.)

## 1. Design for the camera you actually have

The city view is a high three-quarter camera (pitch ≈ 45–55°, long lens, near
orthographic). From there:

- **Roofs are 50–60% of a building's pixels.** The roof is the building's face:
  its shape, material and colour carry identity and tier. Design the roof first.
- **Walls are foreshortened to ~half height.** Vertical detail on walls must be
  bold (door, one big window band, a sign prop) or it disappears.
- **The south-east face is the lit hero face** (key light upper-left, the house
  light). Put the door, the sign prop and the richest detail on the faces the
  camera sees; the back faces get the same forms at half the detail.
- **Always render approval shots from the game camera**, not a hero 3/4 low
  angle. A building that only works from eye level is a failed building.

## 2. The three read distances (every building passes all three)

| Distance | On screen | What must read | Test |
|---|---|---|---|
| **City close** | 180–320 px tall | construction logic, material, job prop, tier trims | render 1080×1920 portrait crop at game zoom-in |
| **City overview** | 60–120 px | silhouette + roof colour + job prop → which building, which tier | downscale to 25%; name the building and tier in 1 s |
| **Realm map** | the whole city is 48–96 px | city size/level, owner colour, burning/shielded state | the city as a cluster sprite; is its tier obvious? |

A building that fails the overview test is redesigned in blockout, not fixed
with texture.

## 3. Function reads from one "job prop"

Every archetype carries one oversized, unmistakable prop that says what the
building DOES, placed on the lit face or the yard:

barracks → weapon racks + a training post · archery → butts with straw targets ·
stable → hay rack + a horse-head sign · smithy → anvil + glowing hearth mouth ·
farm → fenced crop rows · lumber → log pile + saw-horse · quarry → cut-block
stack + crane · mine → ore cart on rails · market → awnings + crates · tavern →
hanging tankard sign · hospital → herb racks + linen lines · academy/library →
a telescope or orrery on the roof · warehouse → sacks and a hoist beam ·
church → bell-cote · watchtower → brazier at the top.

The job prop is scaled **1.3–1.6× real size** so it survives the overview read.
Doors and windows are scaled **1.2–1.4× real** for the same reason. Everything
structural (beam sections, stone courses) stays at real size so the building
still reads as built, not as a toy.

## 4. Tier evolution — each step must change the SILHOUETTE

A player upgrades a building to see it change. A tier that only changes texture
is a tier nobody notices. Every visual step adds at least:

1. **one silhouette element** (a storey, a tower, an annex, a chimney stack, a
   higher roof pitch, a gatehouse), and
2. **one material step** up the ladder below, and
3. optionally **one prestige detail** (banners, gilt finials, carved barge-boards).

| Visual tier | Materials | Silhouette language |
|---|---|---|
| 1 | earth-fast posts, wattle, thatch | low, one storey, lean-to roofs |
| 2 | timber frame on rubble plinth, shingles | 1½ storeys, first gable, first banner pole |
| 3 | timber frame on dressed plinth, clay tile | 2 storeys, jettied upper floor, dormers |
| 4 | dressed stone ground floor, slate | stone base + timber upper, arched openings, a tower stub |
| 5 | ashlar, lead roofs, carved surrounds | full stone, towers with caps, buttresses |
| 6 | fine ashlar, gilt finials, heraldic banners | the crown silhouette: tallest caps, flags, one unique flourish |

Keep the **footprint constant** across tiers (the grid cell never changes) and
grow UP and into the yard. Keep the **job prop** at every tier, upgraded in
material, so identity never jumps.

**Test**: render all 6 tiers side by side from the game camera, downscale to
25%. Each neighbour pair must differ in silhouette at a glance. Use
`tools/rarity_sheet.py` to tile the strip (it takes any labelled PNGs).

### 4.1 Visual ages ride on unlock bands

Genre pattern (design-forge `references/benchmark.md`, in our words): one
spine building gates everything, and every 5–6 spine levels an "age" bundles
a mechanical unlock with a visible change of the whole city; the models swap
per age and the change is the player's graduation reward (age boundaries
[unverified]). Our rules:

1. **Six ages = the six visual tiers above.** Which keep levels form each
   band and what each band opens belong to design-forge
   (`design-forge/references/progression.md` §1 — PROPOSAL: keep levels 1–30
   in six ages of five, `tier(ℓ) = ⌈ℓ/5⌉`; verify against `data/buildings.gd`).
   This file owns what each age LOOKS like.
2. **The look and the unlock land on the same level-up.** A silhouette step
   with no unlock is noise; an unlock with no silhouette step is invisible.
3. **The keep carries the age.** Each age adds one keep silhouette element
   inside the `KEEP_ASPECT 1.50` frame (caps, hoardings, towers, banners —
   never a taller or wider box), and the castle's own kit (walls, gate, ground
   skirt) steps one material on the ladder above.
4. **Levels between ages still show.** Levels 2–5 of a band each add one
   outline-breaking prop from ONE shared kit — banner pole, pennon, weather
   vane, chimney stack, hoist beam, crenel shields, awning, lantern bracket —
   placed on empties `lvl_2` … `lvl_5` authored like the `fx_*` / `npc_*`
   empties (§8) (progression.md's PROPOSAL; anchor names to confirm with
   castle-forge). Each prop is ≥ 6% of the building's height (≥ 4–7 px at the
   60–120 px overview) and breaks the OUTLINE at 25% — a prop inside the
   silhouette does not count.
5. **Measure the step.** From the alpha pass (art-direction.md §9.2) of two
   neighbouring ages at 25%, the changed silhouette must be ≥ 10% of the union
   (PROPOSAL — a pair of caps on a keep measures ~5–8%, a new storey ~15–20%):
   ```python
   from PIL import Image; import numpy as np
   a, b = (np.asarray(Image.open(p).getchannel('A').reduce(4)) > 127 for p in (age_n_mask, age_n1_mask))
   print("SILHOUETTE_DELTA %.1f%%" % (100 * (a ^ b).sum() / (a | b).sum()))
   ```
6. **Everything ages together.** Troop kit climbs the same material ladder
   (t1 cloth → t10 plate; progression.md §6, battle-forge presentation §2),
   so the city, its walls and its soldiers read as one age.

## 5. Construction logic (the owner's ruling, made geometric)

"Real construction elements, never boxes with stripes":

- **Loads go down visibly.** Roofs sit on wall plates and rafters that show at
  the eaves; jetties sit on projecting joists; towers step out on corbels;
  buttresses land where vaults or wall weight would push.
- **Stone is coursed.** Course height 0.25–0.35 m, staggered joints, quoins at
  corners (larger blocks, alternating long/short), a plinth course and a
  string course per storey. Model quoins and string courses as geometry; the
  courses between them can be a trim-sheet texture.
- **Timber is framed.** Posts at ≤ 2.5 m spacing, a sill beam, a wall plate,
  braces at the corners. Infill panels between, never a flat box with stripes
  painted on.
- **Openings have frames.** Every door and window has a lintel (timber or stone
  arch with a keystone), a sill, and a reveal depth ≥ 0.15 m so it casts a shadow.
- **Roofs have thickness and overhang.** Eave overhang 0.3–0.6 m, visible
  thickness at the verge, ridge tiles/cap, and a slight sag on old tiers.
- **Walls batter.** Castle walls and towers widen 4–8% toward the base;
  crenels are 0.6–0.8 m wide with merlons 1.2–1.8 m; walk-ways have a parapet.

Proportion anchors (metres): storey 2.8–3.2 · door 1.1×2.1 (scaled 1.3 for read)
· castle wall module 4.0 long, 6–10 high, 2.0–3.0 thick · tower Ø 5–8 ·
keep aspect 1.50 (engine contract `KEEP_ASPECT`) · gate passage 3.0×4.0.

## 6. Kit, texel density, budgets (mobile)

- **Author as a kit**: walls, corners, roof pieces, towers, openings and props
  as snapped modules on a **1 m grid** (0.5 m for trims). Buildings are
  assembled, so 34 archetypes × 6 tiers share ~40 kit pieces, not 204 unique
  meshes.
- **Trim sheets + tiling atlases**, not unique bakes: one 2048² kit atlas
  (stone courses, timber, thatch, shingle, tile, slate, plaster, trims) shared
  by every building = one material, batched draw calls. Unique bakes only for
  the landmark pieces (keep/fortress, wonder, monument, palace).
- **Texel density**: 128–160 px/m for city buildings (they never fill the
  screen); 256 px/m for the fortress/keep and landmarks. Keep it uniform
  across the kit — a mismatched module is instantly visible side by side.

| Class | LOD0 tris | LOD1 | Map form |
|---|---|---|---|
| Ordinary building (per tier) | 2–6k | 30% | part of the city cluster sprite |
| Landmark (keep, palace, wonder) | 8–15k | 35% | its own impostor |
| Wall module / tower | 0.8–2.5k | 40% | — |
| Map set-piece (camp, fort, shrine, ruin) | 3–8k | 30% | 300–800 tri LOD2 or impostor |

LODs: `make_bake_target(decimate=…)` for LOD1 from the same sources; LOD
switch distances are set in Godot (`visibility_range_*`), not in Blender.

## 7. Ownership colour and states — mask channels, not texture copies

Strategy players must read **mine / ally / enemy / neutral** instantly (banners,
roof trims, flag pennons, map city ring). Author it once:

- Paint a **tint mask** into vertex colour R (1 = takes the owner colour):
  banners, pennons, shield devices, a roof-trim band. Everything else 0.
- Godot's building shader multiplies albedo by the owner colour where the mask
  is 1. One mesh serves every player and alliance colour.
- The owner palette must stay readable against the terrain and never collide
  with the rarity ladder colours (glow.md) or the unit line accents.
- Which colour feeds the mask — relationship colour or alliance tincture — is
  the realm rules' call (design-forge `references/world.md` §12,
  game-art-director `references/readability.md`); the mesh never changes.
- **States** are engine overlays on the same mesh: under construction
  (a reusable scaffold kit sized to the footprint: poles, ladders, a hoist),
  burning (particle emitters at authored empties named `fx_fire_*`), shielded
  (a dome shader), damaged (a decal set). Author the `fx_*` empties in Blender
  at chimneys, roof peaks and doors so effects spawn in believable places.

## 8. Ground contact and life

- Every building sits on a **foundation/plinth** that sinks 0.1–0.2 m into the
  ground plane, plus a skirt (packed earth, cobbles, grass tufts) modelled as a
  ring that blends into the terrain texture. Floating buildings are the second
  most common kit failure after unbevelled boxes.
- Author empties for life: `fx_smoke_*` (chimneys), `fx_flag_*` (poles),
  `npc_work_*` (where a villager works), `npc_door_*` (where people enter).
  Villager life and smoke are `feel-forge`'s; the anchor points are ours.

## 9. Building QA (in addition to qa.md)

1. Approved from the GAME camera at all three distances (section 2).
2. The 6-tier strip: every neighbour pair differs in silhouette at 25%.
3. The job prop reads at the overview distance.
4. Every structural claim is geometry: lintels, eaves, quoins, braces, corbels.
5. Footprint identical across tiers; pivot at base centre on the grid origin.
6. Owner-colour mask present and limited to heraldic surfaces.
7. `fx_*` / `npc_*` empties present and named.
8. Triangles and texel density within the table in section 6.
9. Sits in the ground (plinth sunk, skirt present), no floating.
10. Age strip: each neighbouring pair's `SILHOUETTE_DELTA` ≥ 10% (§4.1), the
    step on the level that opens the band; `lvl_2` … `lvl_5` empties present
    and each prop breaks the outline at 25%.
11. House family (§10): the job prop, footprint, anchors and tier logic equal
    the default family's; the building is named at the overview in 1 s.
12. Value gate on the city-close render with `--mask` (qa.md §2): `flat` and
    `silhouette` gated, the rest reported as numbers.

## 10. House families — many cultures from one kit

Genre pattern (benchmark.md, in our words): each culture gets its own
architecture, grouped in practice into a few regional families [unverified
detail], and city skins layer on top — in the genre, skins carry stats. We
take the family idea and refuse the stats.

- **A family is a swap, not a rebuild**: a new trim-sheet atlas (2048²), a new
  roof kit and ≤ 12 signature pieces on the SAME structural kit — the 1 m
  grid, footprints, openings, `fx_*` / `npc_*` / `lvl_*` anchors and job props
  (§3, §6). ≥ 75% of the ~40 kit pieces are shared; texel density is
  identical (128–160 px/m) so families can stand side by side.
- **Function and tier never change with the family**: same job prop at 1.3–1.6×,
  same tier ladder logic (§4), same owner-colour mask (§7). A family changes
  wall and roof language only.
- **Where families appear** (PROPOSAL — the owner decides): AI lords' cities
  and camp regions of the realm map first (variety without new archetypes);
  later, cosmetic city styles sold WITHOUT stats (money-law; design-forge
  `references/monetization.md`, shop-forge).

Starting set (working names; story-forge names them; each rooted in a real
regional building tradition, general historical knowledge):

| Family | Real-world root | Walls | Roofs | Signature pieces (≤ 12) |
|---|---|---|---|---|
| Lowland (default) | English / Norman lowland | timber frame on rubble → ashlar | thatch → clay tile → slate, lead | jettied storey, close studding, carved barge-boards |
| March (north border) | border tower houses | thick rubble, lime-washed, few small openings | stone slab, turf on tier 1–2 | corbelled corner turrets, crow-stepped gables, walled yard |
| Riverland (south) | southern brick and terracotta towns | brick, rendered panels | low-pitch curved clay tile | open loggia, brick machicolations, swallowtail merlons, belfry |
| Forest (wild marches) | northern log and stave building | log crib, vertical plank | steep shingle, stacked roofs | carved finials, log-crib corners, raised granary on posts |

Test: render one archetype (e.g. the smithy, tier 3) in every family from the
game camera and downscale to 25%: the building is named in 1 s in every
family, and the family is named in 1 s from roof and wall alone.

## 11. Map troops — token squads (cross-reference)

Genre pattern [observational]: an army on the map is a small squad with a
banner, a troop-type icon and a health bar, never a head-count crowd, so
readability and frame time do not grow with army size. Our token is
battle-forge's (`presentation.md` §2: figures per squad by line, figure
height ≥ 36 px, squad 120–220 px wide; `flows.md`: the realm token = 3
figures of the march's largest line + the lord banner + a 44 px line
medallion). Figures are the `hero3d` rig with the soldier kit — people are
never code-built. blender-forge builds the hard parts:

- **Soldier kit** per line and tier (helms, shields, spears, bows, crossbows,
  blades, barding plates) at the map budget: ≤ 4k triangles and 512² per
  piece (export.md "Map unit / prop"), one shared atlas per line. The line
  reads from the silhouette at 36 px (spear ≥ 1.4× figure height, battle-forge);
  the tier reads from the material ladder (§4.1 rule 6).
- **Lord banner**: pole, crossbar and finial as real forms (forms.md), the
  cloth animated by shape keys or a Godot vertex shader (animation.md), the
  field carrying the tint mask (§7).
- **Line medallion**: a Blender-made icon object, never a flat glyph
  (game-art-director `references/ui-icons.md`).
- **Siege engine tokens**: the siege-forge build recipes, same map budget.
