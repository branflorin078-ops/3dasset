# Kit sets — six four-piece sets, two hall lords, eight visual briefs

Source of this file's set table: the 2026-09-26 commander-kits run
(`reference-forge/tools/_archive/_forge_resume.js`, a record with that day's
text). The TRUTH is `godot/data/equipment.gd` (`desc` = the modelling and
painting brief, "what it names must be visible"; `line` = flavour). Read it
before building; where it differs from this file, equipment.gd wins. Built
pieces live in `art/forge/assets/<ID>/` (REPORT.md, cards, GLB) and the
art-critic's verdicts in `art/forge/CRITIC_REPORT.md` — read both first: a
SHIP piece is reused, an ITERATE piece gets its ranked fixes, nothing is
rebuilt from scratch.

## 1. The six sets (one per field lord)

| Set | Lord | Recorded house + finish | Weapon | Armour | Helm | Token |
|---|---|---|---|---|---|---|
| household | Edwin | household blue (#2B4A99 family); plain, well-kept, old-fashioned | EQ-armingsword — a knight's sword, gold wheel pommel, crimson grip | EQ-gambeson — quilted oak-brown, brass points | EQ-nasal — an older shape, with a mail aventail | EQ-banner War Standard — furled on a dark oak pole, gold finial |
| hammer | Alric | house crimson (#8E1B1B family); heavy, blackened-and-bright plate, no shield | EQ-greatsword — two-handed, leather-bound, the fuller engraved | EQ-fullplate — cuirass and pauldrons, hammered finish | EQ-bascinet — visored, the visor raised | EQ-relic Reliquary — small gold pendant with an amber window |
| longshot | Elena | house green (#3E6B3A family); light, quiet, leather-and-cloth | EQ-warbow — tall yew, gold tip nocks, a cream string | EQ-brigandine — crimson cloth over plates, gilt rivet rows | EQ-hood Archer's Hood — soft leather, a gold clasp at the throat | EQ-wolfcloak — grey wolf fur, a gold chain clasp |
| charge | Rowan | crimson-and-cream tourney colours; polished, showy | EQ-lance — crimson-and-cream spiral, steel point, leather vamplate | EQ-cuirass — polished steel with a gold rope border | EQ-greathelm — gold cross reinforcement over the face | EQ-warhorn — aurochs horn, silver bands, a leather strap |
| measuredwall | Godric | bronze instruments, soot, practical iron; nothing decorative that is not also a tool | EQ-warhammer Engineer's Warhammer — faceted steel head, oak haft, iron langets | EQ-hauberk — riveted, oiled steel rings | EQ-kettle — iron, wide-brimmed, honestly dented | EQ-rule Engineer's Rule — brass, folding, on a leather thong |
| standingline | Maud | household blue with gold; dented, maintained, formidable plate | EQ-pike Tower Pike — leaf blade, a tassel of crimson cord | EQ-oathplate — Masterwork plate, gold inlay, a wax-sealed oath ribbon | EQ-crownhelm — a commander's bascinet under a gold circlet | EQ-signet — gold, with a carnelian seal |

The owner's Oathplate ruling applies to every lane: it must read as ARMOUR
first — a breastplate with an oath engraved into the metal; the ribbon is
secondary (every take that led with the oath came back a document). The
engraving is ornament that reads as an oath WITHOUT legible letters (the
image negative bans letters and runes).

## 2. The hall lords' signature objects and the plinth

| Id | Object | Brief (recorded) |
|---|---|---|
| CMD-faber-hammer | Faber's Forge Hammer | faceted iron head, oak haft, rune-struck cheeks, iron langets, a peen cap |
| CMD-fable-staff | Fable's Lantern Staff | iron-shod walking staff; a small bronze reading lantern with glass panes hangs under the head, its flame the one warm light |
| CMD-fable-chronicle | The Chronicle | tooled leather boards, brass corners, a clasp, an iron chain from its spine |
| CST-hall-plinth | The Hall Plinth | octagonal two-course stone dais ≈ 1.15 m across, gilt fillet between courses, a recessed rune ring flush in the top face — dark for an unsworn lord, warm gold for a sworn one; "status is light, never particles" |

## 3. Per-lord visual briefs

The silhouette column is what the 128 px black shape must show; the head
column is what survives at 44 px (portrait-lane.md §3). Four lords carry a
tall pole — they are told apart by the TOP of the pole and the angle.

| Lord | Silhouette idea (128 px) | Head at 44 px | Palette accent | Signature object + pose | Hardest parts |
|---|---|---|---|---|---|
| Edwin | a narrow triangle beside a tall line: the FURLED standard, pole ≈ 1.45× his height, planted at his right, bulk at the top | conical nasal helm: point + nasal bar, mail aventail widening at the neck | crimson mantle (shipped portrait) over oak-brown quilting; gilt only at the wheel pommel and the finial | right hand on the pole at shoulder height, left on the pommel | aventail (ring texture on a cage), grey temples |
| Alric | an inverted triangle: pauldrons 1.35–1.45× hip width, the greatsword on the right shoulder breaking the outline at 45°, no shield, wolf pelt on one shoulder | rounded bascinet, visor RAISED (a bar above the brow) | blackened plate with bright hammered edges (roughness 0.25–0.60 across the plate), crimson lining; the reliquary's amber the one warm point | weight forward, heels 0.35 m, left fist on the belt by the reliquary chain | pelt edge cards, hammered finish in the normal |
| Elena | a long thin ARC: the strung war bow ≈ her height, vertical in the left hand; cloak mass on the left only | hood with a point + the braid line over the shoulder | green hood and cloth, crimson brigandine with gilt rivet rows, grey fur | bow at rest, right hand checking the string (not drawing: the Legendary Marksman card already draws) | wolf fur, the braid, soft leather creases |
| Rowan | a lance grounded at rest, tip 0.8–1.0 m above his head, tilted 10–15° back; the flat-topped great helm under the left arm (a rectangle at the hip), plume | bare head, collar-length hair (the only bare young head) | crimson-and-cream; the most polished steel of the cast (roughness 0.18–0.25); gold rope border | lance in the right hand, helm under the left arm, horn at the hip | plume cards; a mounted Rowan needs a licensed horse base (animals are never code-built) |
| Godric | a stocky block under the only BRIM of the cast (kettle brim ⌀ ≈ 0.40 m, forms.md) | wide flat brim | bronze, soot-dark iron, oiled mail; the WAX-red stylus | the rule half-open in the right hand, thumb on a graduation; left hand on the hammer haft at the belt | mail (a ring texture on a cage; rings are never modelled one by one in the GLB) |
| Maud | the straightest line: the Tower Pike planted vertical at her right, leaf blade + crimson tassel above the head; broad plate | bascinet point + the circlet's four points (a crown) | black cloth (portraits.md) with household blue and gold (kit record), the WAX seal on the ribbon | braced, heels 0.45 m; right hand on the pike at shoulder height, left on the sealed ribbon | ribbon cloth sim; dents that read as maintained |
| Faber | a broad trapezoid: the apron chest-to-knee, bare forearms, the hammer head-down at his side, tongs through the belt | round bald crown with a grey fringe, no helm | scorched leather, oiled mail, bronze; coal-orange light from below on the KEY side only (never on the rim side, or it reads as sworn) | right hand on the hammer haft, left thumb hooked in the apron string | forearm skin (burn scars), apron creases |
| Fable | a hooded column with a staff ≈ 1.1× his height; the lantern hangs under the staff head at face height; the chained book a rectangle at the hip | hood peak + the only WHITE head (beard to the chest) | road-grey wool, one gilt line (the book clasp), lantern warmth | stooped 4 cm; left hand on the staff, right on the chained book | the beard (largest groom); the lantern must light his face (a real light: emissive flame + a small light, Godot OmniLight3D ≈ 1.5 m range) |

## 4. Set coherence — four pieces, one owner

- **Canon piece first.** The first finished piece of a set is its canon:
  siblings match its metal, finish, glow hue and strength, and motif scale
  (the kit-run rule).
- **One metal family + one accent per set**: household munition steel +
  gold; hammer blackened iron with bright edges + gold; longshot leather +
  gilt rivets; charge polished steel + gold rope; measuredwall bronze +
  iron; standingline plate + gold inlay.
- **One motif per set** (PROPOSAL, drawn from the descs): household — the
  wheel (pommel, finial ring); hammer — hammered facets; longshot — gilt
  rivet rows; charge — the rope border and the spiral; measuredwall —
  graduation ticks; standingline — the engraved oath band. Motif width in
  mm equal across the four pieces ±20%.
- **Material spread inside a set**: roughness spread ≥ 0.30 between the
  smoothest and roughest material (polished steel 0.25 vs leather 0.60);
  ≥ 2 value groups among the base colours — the cure for "all grey".
- **Wear**: one honest history mark per piece, where use would put it
  (equipment.md); never distressed everywhere.
- **Tier**: all four pieces `retier` the same way (forge `TIERS`); on the
  figure the glow lives in engraved lines only.
- **Set sheet**: the four Masterwork cards tiled
  (`blender-forge/tools/rarity_sheet.py`) and the set judged as one kit
  before any piece goes onto a figure.

## 5. House colours — an open question for the owner

The records disagree: Edwin's shipped portrait wears a crimson mantle, the
kit record gives him household blue; Maud is "in black" (portraits.md) and
"household blue with gold" (kit record); Alric (crimson #8E1B1B) and Rowan
(crimson-and-cream) share a hue, as do Edwin and Maud. Until the owner rules:
shipped art wins (Edwin keeps the crimson mantle); cloth follows the kit
record elsewhere; the map tells lords apart by banner division and charge,
not by hue alone (token-lane.md §4). Question to ask: "One field colour per
house, or a two-colour livery (field + division) for each lord?"

## 6. Kit on the figure vs on the item card

- Weapons, tokens and signature objects: ONE GLB serves the card and the
  figure's hand (pivot at the grip centre, export.md).
- Armour and helms: the card piece is a display object; the figure wears a
  FITTED variant built from the same profiles and materials with
  `plate_on_body` / `helm_shell(radius = head half-width + offset)` —
  two meshes, one texture set, one tier wiring. Both are listed in the
  piece's REPORT.md.
- Tier on the figure: Godot animates `emission_energy` per instance on the
  rune dial 0 / 0.7 / 1.5 / 2.6 (equipment.md); kit emissive pixels ≤ 3% of
  the figure at the hall framing; the face stays the lightest large mass.
- Cross-equip (ASK lords.md): if any lord may wear any piece, fitted
  variants multiply (6 armours × 8 bodies = 48). PROPOSAL: 3 body shapes
  via Surface Deform shape keys (figure-lane.md §7) → 18 armour variants;
  helms by head radius ±5 mm, one variant each.

## 7. Budgets on the figure (PROPOSAL; export.md budgets rule the cards)

| Piece class | Card (export.md) | On the figure |
|---|---|---|
| Armour (fitted) | 2048², ≤ 40k | 8–10k |
| Helm | 2048², ≤ 40k | 3–4k |
| Weapon / pole | 2048², ≤ 40k | 4–5k (pole weapons: 3k + banner cloth 1k) |
| Token (relic, horn, rule, signet) | 1024², ≤ 12k | 1–2k |
| The set on the figure | — | ≤ 20k, one 2048² texture set shared by the four |

## 8. Failure modes

| Failure | Looks like | Cause | Fix |
|---|---|---|---|
| Four strangers | pieces of one set look like four shops made them | no canon piece; different metals | §4 canon + one metal family; set sheet |
| Document plate | the Oathplate reads as a scroll | oath led the build | armour first, ornament band, ribbon secondary |
| Pole soup | Edwin, Rowan, Maud, Fable blur at 128 px | four vertical poles | §3: distinct tops (furled cloth, tilted lance + helm at hip, leaf blade + tassel, hanging lantern) |
| Missing noun | the desc names a vamplate the model lacks | brief not checked | every noun of `desc` visible (equipment.md) |
| Glow over face | Masterwork inlay brighter than the face | card-strength emission on the figure | rune dial values in game; ≤ 3% emissive pixels |
| Sworn confusion | Faber's coal light reads as the gilt rim | warm light on the rim side | coal light on the key side only |

## 9. Checklist

- [ ] Set table checked against `data/equipment.gd`; differences listed
- [ ] REPORT.md / CRITIC_REPORT.md read; SHIP pieces reused
- [ ] Canon piece chosen; motif, metal family and spread rules met
- [ ] Set sheet at 128 px opened; the four read as one kit
- [ ] Fitted variants for armour and helm; `QA_FIT` pasted
- [ ] §3 brief met on the figure: silhouette, head at 44 px, pose, accent
- [ ] House colour question asked or answered
