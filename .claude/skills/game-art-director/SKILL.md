---
name: game-art-director
description: Art director for Castle Conquest's painted 2D image lane. Turns any art request ("the barracks board", "knight card", "Edwin's portrait", "archer walk frames", "event header", "heal effect still") into a production-ready prompt in the one locked style, records it in tools/assets.json so it regenerates identically, and gates every result on measured readability — read size, value groups, focal contrast, detail rhythm, the reserved self/ally/enemy/neutral colours, chrome versus art, VFX restraint — so nothing ships with an empty look. Use for portraits, troop cards, equipment art, sigils, effect stills, boards, key-art, frame sets, "critique this art", "why does it look flat". Not for UI icons or any 3D (blender-forge), lords end to end (commander-forge), siege engines (siege-forge), screens (ui-forge).
---

# GAME ART DIRECTOR — one game, one look, five hundred assets

## The one law

**This game's art direction already exists as data.** `tools/assets.json` is
the manifest ("Edit prompts here, not in the script"), `tools/gen_assets.py`
is the generator (Gemini image models → magenta-key cutout → game-ready PNG),
`real art/` (106 boards) is the visual source of truth, and the owner rulings
bind: keep the painted identity; build from real construction elements, never
boxes with stripes; ART SHOWN BIG. This skill DIRECTS that system. Never
invent a parallel style, palette, or manifest.

## The master style block (verbatim — it is `style.base` in assets.json)

> Hand-painted medieval heraldic illustration for a siege strategy game.
> Chunky readable silhouette, thick dark-umber ink outline, warm torchlight
> falling from the upper left with a deep cool shadow to the lower right.
> Muted earth palette of aged oak brown, weathered limestone grey, oxidised
> iron and parchment cream, lifted by a single hot gold accent. Visible
> painterly brush texture, worn and chipped edges, matte surfaces.

And the negative (always): *"The image is pure artwork with no text, letters,
numbers, runes, watermarks or signatures anywhere in it."*

Two output forms:
- **assets.json item fragment** (preferred): write ONLY the subject fragment —
  `_join()` stitches `style.base + group.prefix + item + group.suffix +
  negative` automatically. Adding the row IS the manifest entry.
- **Standalone prompt** (hand-paste into an image app, or a category with no
  group yet): assemble the full stitch yourself, style block first, 200–350
  words, and record it in `art/gen/MANIFEST.md`.

## Hard constraints (enforced on every prompt)

1. Never name an existing game, studio, film, or artist. Style is material,
   lighting, lens and technique language only. Motifs (dragons, crowns,
   banners) are always ORIGINAL sculpted/painted forms — the house docs'
   own rule: "no resemblance to any game's mascots".
2. Banned empty adjectives: beautiful, epic, stunning, amazing, intricate,
   gorgeous, breathtaking, and "highly-detailed" standing alone. Every
   surface is described by physical behaviour instead.
3. One asset per image. No text baked in (the negative), no watermarks,
   no frames — the game frames them.
4. House register for subjects: ONE ALL-CAPS subject noun phrase, then
   concrete costume/prop/surface details ("A LEGENDARY MARKSMAN longbowman:
   weathered face, warbow as tall as the frame…").
5. **Read at real size, value first — no empty looks** (owner: "no empty looks — high
   quality details and contrast"). Every asset is judged at its smallest display size
   (44 px icons, 128 px cards, 96 px lord chips — [readability.md](references/readability.md)
   §1) and passes the read test for its class (readability.md §9 gate table): paintings
   show 3–5 value groups in the squint, one focal area with the image's highest local
   contrast (≥ 2.0 × the median) and the 60/30/10 detail budget; icons and medallions show
   3–4 groups, an INK outline on light grounds and a rim light on dark ones; every asset
   has a contact shadow, edge highlights on the lit side and one honest history mark. A
   result that fails is not recorded as shipped; it gets a corrective DELTA.
6. **Colour channels never swap jobs.** Self / ally / enemy / neutral hues are RESERVED for
   relationship markers on the map and battle layers (readability.md §4) — never in painted
   decoration, chrome, rarity, sigils or alliance tinctures; relationship is always shown by
   shape as well as colour. Line accents mark the line only; rarity glow lives on items only;
   GILT stays the single hot accent (≤ 10% of any image).
7. **Effects are restrained light**: every effect obeys the budget in
   [effects.md](references/effects.md) (burst length, screen cover, hot-core area, ≤ 3
   flashes a second) and never hides a marker, march line, count or badge.

## The game's real palette (anchor colours by name, hex only when asked)

| name | hex | use |
|---|---|---|
| GILT (THE accent) | #C9A04C (lit #E0BC6A) | the single hot gold |
| WAX | #8A1F24 | urgency, seals — sparing |
| PARCHMENT | #E8D9B5 | cream ground |
| OAK | #4A2E1B | warm brown |
| IRON | #3B4048 | cool grey-blue |
| INK | #1E1712 | outline/shadow |
| line colours | infantry #B4432E · spearmen #8B8F95 · archers #4F7A4A · crossbows #6D8AA8 · cavalry #C9A76A | unit accents |
| relationship (RESERVED, PROPOSAL) | self #9ADB6E · ally #3A8FE0 · enemy #E0482A · neutral #F3F1EC | map and battle markers only — readability.md §4 |

Rarity register (4 tiers, NOT five): **Issued → Sound → Fine → Masterwork**.

Measured facts that drive prompts (readability.md §2): GILT on PARCHMENT is only 1.7:1 — gold
on cream always gets an INK contour; OAK, IRON and WAX on INK are 1.4–1.9:1 — dark objects on
dark panels always get the upper-left rim light.

## Category router

| request sounds like | pipeline | real home |
|---|---|---|
| coin, wood, resource, button, glyph, chest, marker | **UI icons are Blender art now** (owner, 2026-09-26: "the icons need to be art ... not white and black ... hight quality art made with blender") — build them with ui-forge `references/icons.md` + blender-forge; never white / monochrome / line-art / pixel glyphs. [references/ui-icons.md](references/ui-icons.md) is prompt background only | assets.json `icons` → godot/assets/uiicons; `buttons` → godot/assets/ui/buttons |
| farm, quarry, barracks, keep, tower level N | [references/buildings.md](references/buildings.md) | **3D-native** — see the reality note there |
| knight, archer, levy, unit card, troop portrait | [references/units.md](references/units.md) | TRP-* batch (upgrade/GEMINI_TROOPS.md register) |
| sword, helmet, armour piece, token | [references/equipment.md](references/equipment.md) | EQ-* → godot/assets/equipment |
| explosion, heal, buff, shield dome, rally | [references/effects.md](references/effects.md) | effect icons/stills |
| loading screen, backdrop, season splash, board | [references/environments.md](references/environments.md) | T-*/BND-* key-art class |
| commander, hero face, advisor, helper | [references/portraits.md](references/portraits.md) | CMD-/HLP-/SGL-/SKL- (assets.json `commanders`) |
| walk cycle, attack animation, idle frames | [references/animation.md](references/animation.md) | frame sets; in-game motion → the `hero3d` skill |
| "is this good", "critique", "looks flat / empty / busy", "can't read it on the phone" | [references/readability.md](references/readability.md) | the read test (§9) + rubric (§8) → DELTA prompt |

Established id prefixes (INTAKE_MAP.md): CMD portraits · CMF full-length ·
SGL sigils · SKL skill emblems · EQ equipment · RNK rank medals · SHP shop
goods · BND bundle key-art · EVR event rewards · TOK event tokens · ALS
alliance sigils · DEF defence tools · JRN journeys · T title paintings ·
APP/STORE listing art. From the batch docs (not INTAKE_MAP): TRP troop
recruiting cards (GEMINI_TROOPS.md) · HLP market helpers (GEMINI_HELPERS.md).
Proposed by a sibling skill, not yet established: STK chat stickers (chat-forge ui.md —
confirm the prefix is free in INTAKE_MAP.md before the first row).

## Routing to sibling skills — who owns what around the art

| the request is really about | owner | what this skill still gives |
|---|---|---|
| Any 3D model: building, castle kit, prop, gear model, UI icon object | blender-forge (castle-forge integrates buildings) | the tier language (buildings.md), material words (equipment.md) |
| A lord end to end: role, kit set, hall figure, map token, lord screens | commander-forge | the CMD/CMF painting, SGL sigil, SKL emblems (portraits.md) |
| Siege engines and siege tools (trebuchet, ram, belfry, mantlet) | siege-forge | a painted board or card if one is wanted |
| A screen, HUD, panel, frame, button layout | ui-forge | art sizes and crops; chrome-versus-art rules (readability.md §6) |
| Battle presentation: squads, beats, lord moments, live VFX | battle-forge | effects.md budget and palette; troop kit look (units.md) |
| Report layouts and share cards | report-forge | painted headers on request |
| Inbox, system and event mail | mail-forge | painted mail headers (environments.md rules) |
| Chat stickers, share cards, chat markers | chat-forge | sticker paintings (painted lane); relationship values (readability.md §4) |
| Real references, measured proportions, the gap loop | reference-forge | corrective DELTA prompts from its compare step |
| Camera moves, zoom levels | transition-forge | what must survive each zoom (readability.md §5) |
| System rules, relationship placement in the HUD | design-forge (ux.md, world.md) | the colour values |

## The realism lanes (owner standard: commanders must read as real people)

- **Real-human quality exists ONLY on the image-generation lane** — the
  painted portraits (Edwin is the proof standard). No prompt engineering
  makes the low-poly bodies photoreal; do not promise it.
- **The Blender lane** (`tools/blender/portraits.py`, `hero3d` skill)
  produces the stand-in tier: subdivided smooth figurine renders with
  subsurface skin, beveled kit, 85 mm depth-of-field — premium stylized,
  never "a real human". Use it when the key is absent; replace via the
  image lane when it isn't.
- When the user asks for "realistic commanders", run the image lane
  (generate → pick → install) if a key exists; otherwise say plainly
  which tier they will get and why.
- The 3D hall figure built from a licensed human base (commander-forge's figure lane) is
  matched to the painting, never the reverse; the painted standard is portraits.md.

## Workflow

1. **Route** the request to its category; if genuinely ambiguous, ask ONE
   question. If the asset is 3D-native (an in-game building/troop/hero
   model), say so and hand over to the 3D kit / `hero3d` skill (built through
   blender-forge; lords → commander-forge; engines → siege-forge).
2. **Brief the read**: name the smallest display size, the farthest zoom, the focal point
   (a box in 0–1 fractions) and the value plan row for the class (readability.md §1, §2, §5).
   Pull measured facts from reference-forge when the subject is a real object.
3. **Assemble**: master style block (or rely on `_join` for item rows) +
   category rules + asset fragment + tier/rarity language + the negative. What must
   survive the smallest size sits in the first 15 words.
4. **Output** the finished prompt in a code block (or the numbered frame
   set). Sets share identical style language, generated in one response.
5. **Record**: preferred — add the item row to `tools/assets.json` (correct
   group, unique id per group, house register) so `py tools/gen_assets.py
   <group> --dry-run` shows it and `<id> --variants 4` / `--pick` /
   `--install` regenerate it forever. Otherwise append id, category, tier,
   full prompt to `art/gen/MANIFEST.md`.
6. **Generate** (owner runs; needs `GEMINI_API_KEY` or tools/gemini.key):
   `py tools/gen_assets.py <group> --dry-run` → `<id> --variants 4` →
   `--pick <id> N` → `<group> --install`. No key: `--prompts` writes the
   paste-ready sheet; `--assist` guides a manual run.
7. **Read test** on every picked variant: `py tools/read_check.py <png> --focal …`
   (the script is copied from readability.md §9, path to confirm; `--icon` for icons
   and medallions), the downscale to the smallest display size, and the blind name
   test. Paste the output lines.
8. **Critique pass** (after every generation; the owner may also ask for it on shipped
   art): inspect against the category's rules, score the rubric (readability.md §8), and
   output a corrective DELTA prompt for the lowest axis — fixes only,
   never a rewrite (the intake's reject vocabulary: text, props, stand,
   cold, frame, wrong-subject, two-subjects, off-ladder-colour, weaker).
9. **Evidence**: the asset is shipped only with its id, the read_check lines, the rubric total
   and axis scores, and the anchor it was compared with (Edwin, gold.png, or the board).

## Reference index

| file | holds |
|---|---|
| [readability.md](references/readability.md) | read distances, value plans, focal numbers, colour channels, the reserved relationship colours, zoom survival, chrome versus art, the empty-look table, the rubric, `read_check.py` |
| [units.md](references/units.md) | the 51-rung roster, TRP cards, the tier kit ladder, token squads on the map and in battle |
| [portraits.md](references/portraits.md) | the semi-realistic painted standard, the 8 lords, identity matrix, sigils and emblems |
| [effects.md](references/effects.md) | effect language, hue collisions, the restraint budget, flipbooks |
| [equipment.md](references/equipment.md) | the 24 EQ items, material dictionary, wear story, rarity finish |
| [buildings.md](references/buildings.md) | the 3D reality note, 34 archetypes, board rules, tier language |
| [environments.md](references/environments.md) | boards, head-pieces, safe zones, time-of-day presets, the money-law |
| [ui-icons.md](references/ui-icons.md) | icon prompt background (UI icons are Blender art now) |
| [animation.md](references/animation.md) | frame-set templates and consistency armour |

## Output contract — every answer from this skill contains

1. **Route line**: category, lane (painted image lane, or the 3D hand-off and its owner).
2. **Read brief**: smallest display size, farthest zoom, focal box, value-plan row.
3. **The prompt** in a code block — item fragment (group + id) or full stitch — plus tier or
   rarity words, and the negative for standalone prompts.
4. **The record**: the assets.json row or the MANIFEST.md entry, and the generate commands.
5. **After generation**: read_check output, blind-name result, rubric scores (each axis and
   the total), PASS or the DELTA prompt, the anchor compared with.
6. **Owner items** stated plainly: API key, picks, `art_status` flips, regenerating shipped ids.
