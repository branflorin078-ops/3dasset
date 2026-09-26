# Buildings — the reality note first

**In-game buildings are 3D, not generated images.** All 34 archetypes ×
6 tiers are procedural models from the Blender kit
(`tools/blender/generators/buildings.py`); the building card and ladder
thumbnails are ENGINE RENDERS of those models (`assets/ui3d/builds/`, made
by `core/build_thumbs.gd`). A request for "the barracks at level 3" as it
appears in the game is a **3D-kit task** — route it there (or to the
`hero3d` skill's authoring conventions, which are the same kit).

Image-generation serves buildings only as **painted boards / key-art**: a
screen head-piece, an event banner, a bundle painting, a loading vignette
where a building is the subject. Those follow this pipeline.

## The real archetype vocabulary (use these names)

house, farm, lumber, mine, barracks, archery, smithy, church, market,
tavern, townhall, warehouse, stable, tower, well, hospital, library,
embassy, quarry, huntlodge, encampment, sawmill, stonemason, mill,
victualler, fortress, laboratory, wonder, monument, palace, academy,
milacademy, arsenal, university.

## Board/key-art rules

- Three-quarter view from ~35° elevation (matches the game camera's read);
  the building grounded on a small earth base with a contact shadow —
  never floating, never a lawn hero.
- Sunlight/torchlight upper-left with the deep cool shadow lower-right
  (the master block's light — verbatim block leads the prompt).
- **Visible construction logic** (the owner's ruling made concrete): beams
  carry roofs, stone courses stagger, buttresses meet walls where loads
  land — real construction elements, never boxes with stripes.
- Composition leaves the game's own framing alone: no painted borders.

## Tier language (matches the 3D kit's own ladder so 2D and 3D agree)

| tier | reads as |
|---|---|
| 1 | rough timber, thatch, earth-fast posts, a motte-and-stockade fortress |
| 2–3 | timber framing over a rubble plinth, shingle/clay roofs, first banners |
| 4–5 | dressed stone, arched openings, slate/lead, carved door surrounds |
| 6 | fine ashlar, gilt trim on the civic pieces, hoardings and eight caps on the fortress |

The fortress is special everywhere: its aspect is an engine contract
(KEEP_ASPECT 1.50) — a fortress painting should honour the same tall
proportion or it will read as a different castle than the one in play.

## Ready fragments (board class, standalone stitch, 200–350 words total)

- **barracks board**: THE BARRACKS YARD AT DRILL: a timber-framed drill
  hall over a rubble plinth, spear racks under the eaves, a sergeant's
  brazier smoking upper-left, churned practice ground with one dropped
  training shield.
- **smithy board**: THE SMITHY AT WORK: open forge glow from the hearth
  mouth, an anvil worn bright on its crown, quench barrel steaming, horseshoe
  blanks nailed in a row on the lintel.
- **keep/fortress board**: THE KEEP RISEN: a tall Norman keep at its 1.5
  proportion, banner streaming from the highest cap, gulls of smoke from
  the bailey below, evening gold on the west face.
