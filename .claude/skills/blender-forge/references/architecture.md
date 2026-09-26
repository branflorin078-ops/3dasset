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
