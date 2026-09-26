# Sources — where references come from, and the search vocabulary

## The Met Open Access (primary, CC0)

- API: `https://collectionapi.metmuseum.org/public/collection/v1` —
  `/search?departmentId=<d>&hasImages=true&q=<term>` (**q LAST**), then
  `/objects/<id>`. Keep only `isPublicDomain: true` (the tool enforces it).
- Departments: **4 Arms and Armor** (swords, staff weapons, helmets, armour,
  shields, horse armour — the core), **17 Medieval Art** (reliquaries,
  caskets, carved ivory and wood, seals, jewellery, textiles, metalwork),
  **7 The Cloisters** (architecture fragments, stained glass, furniture).
- `measurements[].elementMeasurements` gives numeric cm / kg (Height, Width,
  Depth, Length, Diameter, Weight) — use these for proportions, never eyeball.
- Search is keyword-loose: always pass `--must` class words, and a date
  window when the class spans centuries.

## Cleveland Museum of Art Open Access (secondary, CC0)

- API: `https://openaccess-api.clevelandart.org/api/artworks/?q=<term>&cc0=1&has_image=1`
  (`ref_search.py cma`). Every record returned with `cc0=1` is CC0.
- Strong where the Met is thin: furniture and woodwork (castle interiors,
  chests, thrones), architectural fragments, textiles, caskets, medieval
  metalwork. `--type "Arms and Armor"` / `"Furniture and woodwork"` /
  `"Textile"` / `"Sculpture"` narrows the class.
- Measurements arrive as a string; the tool keeps the first cm triple as
  H × W × D and stores the raw string — check the raw string when the object
  has several parts (it may have measured the lid, not the chest).
- (Added 2026-09-26; the parser is unit-tested, the live endpoint was not
  reachable from the authoring sandbox — run one search and open the sheet
  before trusting it in a loop.)

## Architecture (castle kit, city buildings, map set-pieces)

Museums hold fragments (capitals, doorways, windows), not whole buildings.
For WHOLE-building proportion use measured drawings and surveys, studied
for numbers only: storey heights, wall thickness, batter, crenel/merlon
widths, roof pitch. Record the numbers in `REFERENCE.md` with the source
URL; download nothing that is not CC0/public domain. The anchors in
blender-forge `references/architecture.md` §5 are the defaults when no
source is at hand.

## The benchmark lane — genre games, measured, never looked at for style

Other strategy games are studied for DESIGN and READABILITY, never for art:
- **Allowed**: measuring from our own play sessions — HUD zones as % of
  screen, tap-target px, text sizes, how many px a city/march/unit occupies at
  each zoom, timer lengths, reward cadence, number of taps to a task.
  Numbers go into `art/benchmarks/<game>/<topic>.md` (tables, no images
  required).
- **Never**: their screenshots on a compare sheet beside our art, their
  images in any image-model prompt or conditioning, tracing, palette
  picking, or naming the game in any art prompt (game-art-director rule 1).
- The design conclusions live in `design-forge` (`references/benchmark.md`).

## The owner's boards (the game's look)

`D:/CastleConquest/real art/` — 198 boards, descriptive filenames
(`Blacksmith_and_farm_prop_sheet…`, `Army_management_interface…`,
`Building_evolution_sheet…`, `Biomes_for_Castle_Conquest…`, barbarian
camps, animals). `ref_search.py local "<keywords>"` ranks them. They set the
palette, finish level and stylisation; they are NOT construction references.

## Never
Other games' art or screenshots as visual references (the benchmark lane
above measures, it does not look), fan art, stock photos of unknown licence,
Pinterest/ArtStation images, or anything without a clear CC0 / owner source.

## Search vocabulary — the game's 24 items (starting points; refine per run)

| game id | Met query | --must | window | notes |
|---|---|---|---|---|
| EQ-armingsword | sword | sword | 1250–1450 | single-hand, cruciform; wheel pommels |
| EQ-greatsword | two-handed sword | sword | 1400–1600 | ricasso, long grip, side rings |
| EQ-warbow | bow | bow | — | few long bows survive; lean on proportions (≈ archer height) |
| EQ-lance | lance | lance,vamplate | 1450–1650 | tournament lances + vamplates (hand guards) |
| EQ-warhammer | war hammer | hammer | 1400–1650 | "horseman's hammer": faceted head, langets |
| EQ-pike | spear | spear,pike,partisan | 1400–1650 | leaf blades, langets, tassels |
| EQ-gambeson | doublet | doublet,arming | — | textiles are rare; use quilting patterns + boards |
| EQ-fullplate | armor | armor | 1450–1600 | full harnesses: lame counts, articulation |
| EQ-brigandine | brigandine | brigandine | 1400–1550 | cloth-covered, rivet rows showing plate layout |
| EQ-cuirass | breastplate | breastplate,cuirass | 1450–1650 | keel (medial ridge), rolled edges, fauld |
| EQ-hauberk | mail | mail,shirt | — | ring diameter ≈ 8–12 mm; riveted vs solid rows |
| EQ-oathplate | breastplate | breastplate | 1500–1650 | etched and gilt bands: where decoration sits |
| EQ-nasal | helmet | spangenhelm,conical,nasal | 900–1250 | conical skull, nasal bar, aventail |
| EQ-bascinet | bascinet | bascinet | 1350–1450 | pointed skull, visor pivots, aventail rivets |
| EQ-hood | hood | hood,coif | — | soft goods — boards + textile references |
| EQ-greathelm | great helm | helm | 1250–1400 | flat-topped drum, sights, breaths |
| EQ-kettle | morion / cabasset / kettle | morion,cabasset,kettle,hat | 1300–1650 | brim width vs skull, rivet band, comb |
| EQ-crownhelm | armet / bascinet | armet,bascinet | 1400–1550 | + Medieval Art "crown" for the circlet |
| EQ-banner | standard | banner,standard,pennon | — | pole fittings, finials (Medieval Art) |
| EQ-relic | reliquary pendant | reliquary,pendant | 1200–1500 | dept 17: crystal windows, gilt frames |
| EQ-wolfcloak | — | — | — | fur: owner boards; no museum proxy |
| EQ-warhorn | horn / oliphant | horn,oliphant | 1000–1500 | dept 17: carved bands, mounts, straps |
| EQ-rule | rule | rule,measure,compass | — | instruments are sparse; hinge + graduations |
| EQ-signet | signet ring | ring | 1200–1600 | dept 17: bezel shapes, engraved seals |

## UI chrome, castle, props

| need | dept | query / --must |
|---|---|---|
| carved oak frames, panels | 17 / 7 | panel, chest, cupboard / panel,chest |
| gilt metal, caskets, mounts | 17 | casket, box / casket |
| wax seals, matrices | 17 | seal matrix / seal |
| heraldic shields | 4 | shield / shield,pavise,targe |
| banners, textiles | 17 | textile, embroidery / textile |
| architecture (castle kit) | 7 | capital, window, doorway / capital,window,door |
