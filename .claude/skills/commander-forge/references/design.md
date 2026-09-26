# Design — applying lords.md to eight people

design-forge [lords.md](../../design-forge/references/lords.md) owns the
numbers: roles, rarity, levels, skills, talents, pairing, set bonuses,
duplicates and pity, acquisition channels, power-creep rules. This file turns
those numbers into assets, states, screens and hand-offs. Where lords.md is
silent, write **ASK lords.md** in the brief — never a number of our own.
Shipped data to read first (paths named in the 2026-09-26 mapping scripts,
reference-forge `tools/_archive/`; confirm on disk): `godot/data/commanders.gd`
(levels, SIGNATURES, OATHS, BONDS, chairs, the clamp ledger, `CMD_FX_CAP`),
`godot/data/attack_data.gd` (COMMANDERS `note`), `godot/data/equipment.gd`
(`desc` = the modelling and painting brief, `line` = flavour).

## 1. Who owns what

| Design element | lords.md sets | commander-forge produces | Built by |
|---|---|---|---|
| Role and lead line | the role of each lord, which line it leads | the role readable in silhouette, kit and token icon | this skill |
| Rarity (4 tiers: Issued, Sound, Fine, Masterwork) | which tier each lord is, if lords carry one | the card frame register per tier (§4) | ui-forge |
| Levels and XP | curve, cap, XP sources (incl. the daily chest "lord XP", core-loop.md) | level numeral + ring on the chip; level-up moment | ui-forge, feel-forge |
| Skills (active on a meter + passives) | count, numbers, meter rate | one SKL emblem per skill; one battle moment per active | game-art-director, battle-forge |
| Talents (≤ 3 branches, ≤ 30–40 points) | trees and costs | talent tab, branch icons (Blender-made art) | ui-forge, blender-forge |
| Pairing (primary + secondary; only the primary's talents and gear apply) | the rule | pairing screen, preset slots, the token shows the primary | ui-forge, world-forge |
| Six four-piece sets + set bonuses | the bonuses | fitted kit on the figure, item cards, set-complete moment | blender-forge + this skill |
| Duplicates → upgrade currency, pity counter | the published math | the counter always visible, the conversion moment | ui-forge |
| Acquisition channels + free path per rarity | channel per lord, path length | "where to earn" card on every unowned lord | ui-forge |
| Power creep: sidegrades, reworks, refunds | the rules | rework notice, refund screen; old art stays valid | ui-forge, story-forge |
| Sworn state | what swearing means (OATHS in the shipped data) | the gilt rim + the plinth ring (§4) | this skill, hero3d |

## 2. The lord card (fill one per lord before any work)

```yaml
id: edwin                      # lower-case key used in every file name
display: Lord Edwin            # from data; l10n key, never baked into art
temper: "the inherited veteran; steady, has never lost a rearguard"
role: ASK lords.md             # §3 lists the proposals
lead_line: infantry            # PROPOSAL (§3); accent #B4432E; token line icon
rarity: ASK lords.md
set: household                 # kit-sets.md §1
signature_object: EQ-banner    # the one object the figure always carries
house_colour: ASK owner        # open question, kit-sets.md §5
face: portrait-lane.md §4 edwin   # the structure paragraph, verbatim everywhere
lanes:
  portrait: {ids: [CMD-edwin, CMF-edwin], art_status: shipped (CMD) / missing (CMF)}
  figure:   {id: HERO-edwin, base: <licensed file + licence>, head: <sculpt|scan>, art_status: missing}
  token:    {banner: TOK-edwin-banner, squad_line: infantry, art_status: missing}
skills: [{name: ASK lords.md, emblem: SKL-<id>, moment: §6 row}]
lines_needed: [hall_greeting, oath_sworn, level_up, skill_bark, defeat, hall_idle x3]
open_questions: []
```
Ids `HERO-*` and `TOK-*` are PROPOSALS (hero3d and world-forge may already
name these — their names win). `CMD`, `CMF`, `SGL`, `SKL`, `EQ` are the
established prefixes (game-art-director).

## 3. The eight lords — role proposals

**PROPOSAL — lords.md is the authority.** Derived from portraits.md, the
2026-09-26 kit run and the five troop lines. Two lines have no obvious lord;
the proposal gives spearmen to Maud (her Tower Pike) and crossbows to Godric
(mechanical weapons), so every line has a lord to lead it.

| Lord | Temper (canon) | Role (proposal) | Lead line (proposal) | Set | Signature object |
|---|---|---|---|---|---|
| Edwin | older veteran, grey temples, crimson mantle; never lost a rearguard | steady infantry, rearguard | infantry | household | War Standard |
| Alric | wins quickly or not at all; dark, heavy-set, wolf-pelt shoulder | shock / assault | infantry (heavy) | hammer | Greatsword |
| Elena | archer-commander, dark braid, green hood; decides a siege on the approach | ranged pressure | archers | longshot | War Bow |
| Rowan | young cavalier, plume, kite shield; rides the flank | charge / flank | cavalry | charge | Lance |
| Godric | siege master, wax stylus behind the ear, bronze instruments | siege + engines | crossbows (+ siege) | measuredwall | Engineer's Rule |
| Maud | stern matron in black; held a breach two days | defence / garrison | spearmen | standingline | Oathplate |
| Faber | the King's Armourer, broad, sixty, coal-light | gear / armoury (hall lord) | none on the map | — (signature objects) | Forge Hammer |
| Fable | the King's Chronicler, hooded elder, white beard | chronicle / knowledge (hall lord) | none on the map | — (signature objects) | The Chronicle + Lantern Staff |

If lords.md gives Faber or Fable a field role, they get a token (token-lane.md)
and a lead line; until then they appear in the hall, screens and reports only.

## 4. The channel table — one channel, one meaning

| Channel | Means | Values | Never |
|---|---|---|---|
| Rim light on the figure; the inner gilt edge of a portrait card or chip | SWORN | figure: gilt `#E0BC6A` at 2.2× key (figure_kit `RIM_GAIN`), unsworn neutral `#D9DDE3` at 0.6× key; card: 2–3 px `#E0BC6A` edge (screens.md §5) | never a rarity colour, never a coloured aura |
| Plinth rune ring (hall) | SWORN | dark unsworn, warm gold sworn (CST-hall-plinth brief) | never animated as particles |
| Emission in kit inlay | that PIECE's tier | cards: forge `TIERS` strength 0 / 2.6 / 4.0 / 7.5; in game: the rune dial 0 / 0.7 / 1.5 / 2.6 (equipment.md) | never on the silhouette edge; never brighter than the face (kit emissive pixels ≤ 3% of the figure) |
| Card frame material | lord rarity (if lords.md uses it) | ui-forge chrome register | never on the painting itself |
| House colour | who the lord is | cloth, banner field, sigil ground | never saturated like a relationship colour on the map (token-lane.md §4) |
| Line accent | the lead troop line | one element: sash, pennon or token icon (infantry `#B4432E`, spearmen `#8B8F95`, archers `#4F7A4A`, crossbows `#6D8AA8`, cavalry `#C9A76A`) | never a uniform repaint |
| Relationship colour (self / ally / enemy / neutral) | whose march it is | reserved channel, game-art-director readability.md | never on a lord's body, kit or portrait |

A painting's warm upper-left edge light is the house KEY light (the master
style block's torchlight), present on every lord in every state; it is not
the sworn signal, which is why a painting has no sworn variant
(portrait-lane.md §2).

Collision to watch: the Masterwork glow body (`#E8A33C`) and the sworn gilt
rim are one hue family. They stay apart by GEOMETRY: the glow lives inside
engraved lines on the kit, the rim traces the outer silhouette. A Masterwork
kit on an unsworn lord must still read as unsworn: rim neutral, plinth dark.

## 5. Every investment is visible

A lord the player invests in must look different afterwards, or the
investment is invisible (design-forge red-team check 5, "others see it").

| Event | Visible change | Where | Timing (PROPOSAL; feel-forge owns motion) |
|---|---|---|---|
| Level up | numeral rolls then lands; chip ring fills | chip, detail header | ≤ 800 ms, no model change |
| Skill level up | emblem gains a pip; the moment's light grows one step (§6) | skills tab, battle | ≤ 600 ms |
| Talent point | node fills with gilt; branch line lights to it | talents tab | ≤ 300 ms per node |
| Equip a piece | the figure wears it at once (GLBs of the lord's set preloaded when the screen opens) | hall figure, kit tab | swap ≤ 150 ms, no spinner |
| Piece tier up | `retier` step: glow and rim of the ITEM card; inlay emission on the figure | kit tab, figure | 600 ms ramp |
| Set complete (4/4) | the set motif lights across the four pieces in order, once | figure | 4 × 120 ms, then steady; no aura |
| Sworn | gilt rim ramps 0 → full; plinth ring warms; card edge and chip ring turn gilt | hall, cards, chips | 600 ms, one sound (audio-forge) |
| Duplicate converted | currency count rolls; pity counter "N of M" updates | lord detail | ≤ 800 ms |
| Max level / max rank | a laurel mark on the chip (PROPOSAL) | chip | once, ≤ 1.2 s |

Every ceremony: skippable after 300 ms, honours `UI.reduced_motion`
(feel-forge), ≤ 2 s on repeats, ≤ 4 s the first time only.

## 6. Skill moments — hand-off to battle-forge

battle-forge plays the resolver's beats; this table says what a lord's
active skill LOOKS like when its beat arrives. Skill names and numbers come
from lords.md / `SIGNATURES`; the moment is one object doing one thing —
the same idea as the SKL emblem ("a cut fuse, a raised standard").

Restraint (PROPOSAL; game-art-director effects.md wins where it sets
numbers): anticipation 120–250 ms → burst 250–600 ms → decay 200–400 ms;
whole moment ≤ 1,200 ms; ≤ 15% of the battle view at peak, ≤ 5% after
600 ms; the effect is a LIGHT SOURCE that lights the ground and the troops
it touches; particles on a size ramp; status on lords is light, never a
particle storm; counters and damage numbers stay readable through it.

| Lord | Moment (proposal) | Light | Sound cue (audio-forge) |
|---|---|---|---|
| Edwin | the standard is raised; a gilt line runs up the pole and the line of troops straightens | gilt column 2–3 m, warms the nearest 2 squads | cloth snap + one drum |
| Alric | the reliquary's amber window flares; one wide cutting arc | amber flash ≤ 250 ms, orange-white arc | a single heavy strike |
| Elena | a volley: arrows as streaks, dust puffs where they land | cool streaks, warm dust catching the key | bowstrings, then impacts |
| Rowan | the horn note; a pressure ring of dust runs along the ground ahead of the charge | ground ring, no colour glow | one horn note |
| Godric | the rule unfolds; a chalk measure line on the wall, then masonry cracks along it | chalk-white line, dust | click of brass, crack |
| Maud | the oath seal warms; a pale-gold ward dome at ground ring (effects.md shield language) | dome brightest at the ground ring | a low bell |
| Faber | hammer strikes; sparks on a size ramp (only if lords.md gives him a battle skill) | spark cone ≤ 0.6 m | anvil ring |
| Fable | the lantern brightens; pages turn (only if lords.md gives him one) | lantern warmth on nearby faces | page turn |

## 7. Voice and story — hand-off to story-forge

story-forge writes; this skill lists what each lord needs so every screen
and moment has a line: `hall_greeting`, `oath_sworn`, `level_up`,
`skill_bark` (≤ 4 words, readable during the moment), `defeat` (respects the
loser: what came back), `hall_idle` × 3. The shipped homes (per the mapping
scripts): SIGNATURES `line`, OATHS `txt`/`nm`, COMMANDERS `note`,
equipment `line`. All text via l10n keys (l10n-forge), +35% length budget,
never baked into any image.

## 8. A new lord (the visual side of the anti-power-creep rules)

1. design-forge writes the SYSTEM.md first (role as a sidegrade, the free
   path, acquisition channel). No art before that spec exists.
2. The silhouette lineup grows to 9: the new lord must be named ≥ 90% of the
   time and must not drop any existing lord below that.
3. House colour ΔE2000 ≥ 20 from every existing house colour, or a
   different banner division (token-lane.md §4).
4. All three lanes are planned at once; a lord never ships with a figure and
   no portrait, or a portrait and no token.
5. A reworked lord keeps his art; the rework notice and any refund are UI
   (screens.md §6), not a repaint.

## 9. Failure modes

| Failure | Looks like | Cause | Fix |
|---|---|---|---|
| Invisible investment | a maxed lord looks like a new one | no state mapped to a channel | §5 table; every row wired |
| Channel clash | players read the gilt rim as "legendary" | rarity pushed onto the rim | §4: rarity on the frame only |
| Role unreadable | an archer-lord who reads as a knight | kit chosen for looks | signature object tied to the role, visible at 128 px |
| Orphan line | no lord leads crossbows | roles set without the line list | §3 check: every line has a lead |
| Moment wallpaper | skill VFX covers the counters | no coverage budget | §6: ≤ 15% at peak, ≤ 1.2 s |
| Silent lord | a ceremony with no line | lines not requested | §7 list sent with the brief |

## 10. Checklist

- [ ] Lord card filled; every ASK resolved or listed as an owner question
- [ ] Role and lead line match lords.md (or marked PROPOSAL)
- [ ] Every row of §5 mapped to a screen state and a harness check
- [ ] Channel table respected on every render (rim = sworn only)
- [ ] Skill moment row sent to battle-forge with the restraint numbers
- [ ] Line list sent to story-forge; no text in any image
- [ ] New lord: SYSTEM.md exists, lineup 9/9 ≥ 90%, colour distance measured
