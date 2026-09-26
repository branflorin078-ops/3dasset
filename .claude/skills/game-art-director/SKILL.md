---
name: game-art-director
description: Art director for Castle Conquest's 2D image-generation pipeline. Turns any asset request ("wood icon", "the barracks board", "knight card", "archer walk frames", "commander portrait") into a production-ready prompt in the game's single locked style, records it so it can be regenerated identically, and routes 3D-native assets (in-game buildings, troops on the map, hero models) to the 3D kit instead. Use for icons, portraits, unit cards, equipment art, effects, boards/key-art, environments, and animation frame sets.
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

Rarity register (4 tiers, NOT five): **Issued → Sound → Fine → Masterwork**.

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

Established id prefixes (INTAKE_MAP.md): CMD portraits · CMF full-length ·
SGL sigils · SKL skill emblems · EQ equipment · RNK rank medals · SHP shop
goods · BND bundle key-art · EVR event rewards · TOK event tokens · ALS
alliance sigils · DEF defence tools · JRN journeys · T title paintings ·
APP/STORE listing art. From the batch docs (not INTAKE_MAP): TRP troop
recruiting cards (GEMINI_TROOPS.md) · HLP market helpers (GEMINI_HELPERS.md).

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

## Workflow

1. **Route** the request to its category; if genuinely ambiguous, ask ONE
   question. If the asset is 3D-native (an in-game building/troop/hero
   model), say so and hand over to the 3D kit / `hero3d` skill.
2. **Assemble**: master style block (or rely on `_join` for item rows) +
   category rules + asset fragment + tier/rarity language + the negative.
3. **Output** the finished prompt in a code block (or the numbered frame
   set). Sets share identical style language, generated in one response.
4. **Record**: preferred — add the item row to `tools/assets.json` (correct
   group, unique id per group, house register) so `py tools/gen_assets.py
   <group> --dry-run` shows it and `<id> --variants 4` / `--pick` / 
   `--install` regenerate it forever. Otherwise append id, category, tier,
   full prompt to `art/gen/MANIFEST.md`.
5. **Generate** (owner runs; needs `GEMINI_API_KEY` or tools/gemini.key):
   `py tools/gen_assets.py <group> --dry-run` → `<id> --variants 4` →
   `--pick <id> N` → `<group> --install`. No key: `--prompts` writes the
   paste-ready sheet; `--assist` guides a manual run.
6. **Critique pass** (offer it after generation): inspect against the
   category's rules and output a corrective DELTA prompt — fixes only,
   never a rewrite (the intake's reject vocabulary: text, props, stand,
   cold, frame, wrong-subject, two-subjects, off-ladder-colour, weaker).
