# Units — troop art

TWO homes, do not conflate them:

- **assets.json `units` group — the manifest of record for in-game troop
  art**: 51 item rows matching the roster's 51 rungs one for one,
  full-body magenta-cutout prefix, installing to `godot/assets/troops/`
  (exactly the roster's ART_DIR). Change per-unit art THERE.
- **TRP-\* recruiting-card batch** (`upgrade/GEMINI_TROOPS.md`): the
  owner-approved ~10-painting card set. Its style lock, verbatim:
  *"painted, warm parchment-friendly palette, dark vignetted background,
  NO text, NO watermarks, NO frames (the game frames them). Portrait
  format (4:5), waist-up, one figure, facing slightly left,
  museum-quality oil-painting finish. These are the recruiting cards —
  they must read at thumbnail size: strong silhouette, one clear
  weapon."* (Note: "museum-quality" is permitted only inside this quoted
  lock; NEW prompts substitute physical language — "layered oil-painting
  finish, visible glazing and brushwork".)

Map-walking troops are NOT image-gen: they are the 3D people rig +
soldier kit. How they read on the map and in battle — token squads, banner,
line medallion — is the section "On the map and in battle" below.

## Rules

- Waist-up, 4:5, facing slightly left, one figure, ONE clear weapon.
- Slight low angle, weight settled — ready, not posed.
- **Equipment matches the tier economy**: a Levy in patched gambeson and a
  kettle helm; a Royal Guard in maintained plate with gilt fittings. Rank
  pairs share a face family — "SAME face family, richer gear".
- **Counter-triangle readability** (players read the counter system from
  the art): spear-line = the weapon visibly LONG and braced; cavalry =
  visibly FAST (mane, cloak motion, lean); archers/crossbows = visibly
  RANGED (bow drawn or bolt being seated). Line accent colours: infantry
  #B4432E, spearmen #8B8F95, archers #4F7A4A, crossbows #6D8AA8, cavalry
  #C9A76A — one accent per card, never a uniform repaint. (The full
  five-line counter graph is design-forge [combat.md](../../design-forge/references/combat.md);
  its "The art must show" column is the brief for each line's weapon.)
- **Card read test** ([readability.md](readability.md) §1): at 128 × 160 px in greyscale a
  critic names the line from the weapon silhouette alone, and the tier band (table below) from
  the gear. The weapon crosses a ≥ 25 L* edge against the vignette; the face's lit side sits at
  60–80 L*, the vignette edge ≤ 30 L*.
- **One accent, one gold**: the line accent covers ≤ 10% of the card (a sash, a hood, a
  pauldron, a cloak); GILT appears only from the t9 band up, as one fitting or one small
  group of fittings (≤ 5% of the card) — the Royal Guard's "gilt fittings".

## The tier kit ladder — cards and 3D kit tell the same story

PROPOSAL built from the rule above ("Levy in patched gambeson … Royal Guard in maintained
plate with gilt fittings") and the ready fragments below; the shipped `units` rows and TRP
cards win where they differ. The ranged lines rise in FINISH (cloth, livery, fittings), not in
plate weight; cavalry is one band ahead in armour (a Knight at t6 already rides in plate).
Accent-coloured items in the table (surcoat trim, livery, sash) are CARD-ONLY: the 3D token kit
paints them in OAK, IRON or undyed wool, because on the map and in battle the line accent marks
only the medallion and the banner trim (battle-forge presentation.md §2).

| band | melee foot (infantry, spearmen) | ranged foot (archers, crossbows) | cavalry | reads at 128 px as |
|---|---|---|---|---|
| t1–2 | undyed wool, padded gambeson, kettle helm or bare head, rope belt | hunter's leathers, hood, a short bow or sling | a rider on an unshod pony, no armour | poor, one colour of cloth |
| t3–4 | mail shirt under the gambeson, nasal helm, a round or kite shield | quilted jack, arm guard, a full bow or a light crossbow | mail shirt, nasal helm, a spear | first metal on the body |
| t5–6 | mail plus first plate pieces (couters, greaves), surcoat trim in the line accent | brigandine, a pavise appears (crossbows), a longer bow | maintained plate, great helm (the Knight at t6) | metal and a surcoat |
| t7–8 | plate harness near complete, heraldic surcoat, pike or great weapon | brigandine with fine fittings, livery in the line accent | plate with barding on the horse's head and chest | a uniform, visibly drilled |
| t9–10 (11) | full maintained plate, gilt fittings (one group), royal livery | royal livery, ONE gilt clasp (the Royal Arbalestier), weathered master (the Legendary Marksman) | full barding, gilt fittings (one group); t11 the Legendary Knight | a named veteran: finish, not size |

No glow on troops at any band: glow is the rarity channel (items, gear), never a troop tier.

## The real roster (five lines; use these display names)

- **Infantry** (t1–10): Peasant, Levy, Axeman, Swordsman, Man-at-Arms,
  Heavy Infantry, Veteran Infantry, Elite Infantry, Royal Guard, King's
  Champion.
- **Spearmen** (t1–10): Peasant Levy, Levy Spearman, Spearman, Drilled
  Spearman, Heavy Spearman, Veteran Spearman, Pikeman, Elite Pikeman,
  Royal Pikeman, Dragoon Pikeman.
- **Archers** (t1–10): Hunter, Archer, Scout Archer, Trained Archer,
  Bowman, Ranger, Longbowman, Veteran Archer, Royal Longbowman, Legendary
  Marksman.
- **Crossbows** (t1–10): Slinger, Hand Crossbowman, Basic Crossbowman,
  Pavise Crossbowman, Crossbowman, Heavy Crossbowman, Veteran Crossbowman,
  Elite Crossbowman, Royal Crossbowman, Royal Arbalestier.
- **Cavalry** (t1–11): Peasant Outrider, Mounted Scout, Hobelar, Light
  Cavalry, Mounted Warrior, Knight, Heavy Cavalry, Veteran Knight, Elite
  Knight, Royal Knight, Legendary Knight.
- Siege engines are models + icons, not portraits (ladder/mantlet/engineer
  icons exist; engines come from the 3D kit). siege-forge owns the engines
  end to end: catalogue, construction, build recipes, animation and their
  map token form.

## On the map and in battle — token squads (not image-gen)

The genre pattern, in our words: an army on the map is shown by **a few figures, a banner and
a line medallion; its size is a number**, never a crowd. Readability and frame time then stay
the same for 500 troops or 80,000. Our version (battle-forge flows.md §5 and presentation.md §2
own the numbers; this file owns what the figures look like):

| view | what is drawn | sizes |
|---|---|---|
| Realm, mid zoom (a march) | 3 figures of the march's largest line + the lord's banner + the line medallion + ETA text | figures ≥ 36 px; medallion 44 px; ETA 24 px |
| Realm, far zoom | the banner icon only, on the relationship-coloured march line | 32 px |
| Battle view | one squad per line per side (≤ 5 a side): infantry 6 figures, spearmen 6, archers 5, crossbows 4 + 1 pavise, cavalry 3 riders | figure ≥ 36 px; squad 120–220 px wide; banner 28–40 px; strength bar 88 × 8 px |

Each element carries ONE channel ([readability.md](readability.md) §3):

| element | carries | made by |
|---|---|---|
| figures | the line (silhouette cue) and the tier band (kit ladder above) | `hero3d` rig + soldier kit, built through blender-forge; never code-built people |
| banner field | relationship: self / ally / enemy / neutral (readability.md §4) | engine tint (blender-forge architecture.md §7 mask) |
| banner device | which lord | the lord's SGL sigil (this skill, [portraits.md](portraits.md)); commander-forge's map-token lane |
| banner trim | the line accent | tint mask, line colour |
| line medallion | the line | Blender icon art (ui-forge icons.md + blender-forge) — never a white or line glyph |
| tier plate I–X (XI cavalry) | tier number | UI text, never painted |
| pennons (≤ 6, then "+N") | rally joiners | battle-forge rally.md |
| gilt corner on a banner | "your troops are in this squad" | battle-forge rally.md |

**Silhouette cues** — each must read at a 36 px figure height in greyscale (battle-forge
presentation §2), and the TRP card shows the SAME cue as its one clear weapon:

| line | cue on the token | the card's "one clear weapon" |
|---|---|---|
| Infantry | shield + one-handed weapon, squared stance | axe or sword held, shield rim in frame |
| Spearmen | spear ≥ 1.4 × figure height, braced low | the shaft running out of frame, butt set |
| Archers | bow drawn, arm raised | bow as tall as the frame, arrow at the string |
| Crossbows | crossbow level at the shoulder, pavise board | arbalest cranked and seated, pavise slung |
| Cavalry | horse length > 2 × figure height, lance or blade forward | mane mid-toss, reins, forward lean |

Figures carry no accent colour of their own: the line is read from the silhouette, the accent
lives on the medallion ring and the banner trim, the side lives on the banner field.

**Against the empty figurine** (owner standard): a token figure at 36 px keeps 3 value groups
(head and helm, torso, legs), a light edge on its upper-left contour, a contact shadow, and the
weapon crossing its outline. A figure that is one flat value with its weapon inside the body
outline is an empty figurine and fails the greyscale test.

## Ready fragments (house register — subject line only; the batch doc's
numbered format carries them)

- **Levy (inf t2)**: AN ORDINARY MEDIEVAL INFANTRY LEVY: padded gambeson,
  simple kettle helm, one-handed axe over the shoulder, honest tired face.
- **Knight (cav t6)**: A KNIGHT AHORSE AT THE WALK: maintained plate with
  a cavalry-gold pauldron accent, great helm crooked under one arm, reins
  easy in the other hand, the horse's mane mid-toss.
- **Pikeman (spear t7)**: A PIKEMAN AT THE BRACE: pike butt set, both
  hands staggered on the shaft running out of frame, jaw set under a
  kettle brim, spear-grey sash.
- **Royal Arbalestier (xbow t10)**: A ROYAL ARBALESTIER: heavy arbalest
  cranked and seated, pavise slung at the back, blue-grey livery with one
  gilt clasp, eyes over the sights.
- **Legendary Marksman (arch t10)**: the shipped exemplar, verbatim from
  the batch doc: weathered face, warbow as tall as the frame, arrow held
  between fingers, green cloak clasped with a silver leaf.
- **Hobelar (cav t3)**: A HOBELAR ON A SHAGGY HORSE: mail shirt and nasal helm, a short spear
  held level, a stirrup-worn boot, the horse's breath fogging, one cavalry-gold rag at the
  shoulder.

## Failure modes

| fails when | caught by |
|---|---|
| Two lines told apart only by colour | [ ] 128 px greyscale card test and 64 px greyscale squad crop: the line is named |
| t2 and t9 look alike (tier invisible) | [ ] tier strip t1 / t5 / t10 per line, blind-named in 1 s (battle-forge presentation §2) |
| Card weapon and token cue disagree (the player learns two shapes) | [ ] card beside the token render at 36 px: same weapon silhouette |
| The army grows into a crowd with troop count | [ ] battle-forge `battle_frame_probe` rally fixture: skinned figures ≤ 70 |
| Line accent painted as a uniform repaint | [ ] accent ≤ 10% of the card; figures carry no accent on the map |
| A troop glows like a rarity item | [ ] review: no emission on troops at any band |
| Relationship shown only by colour | [ ] banner field + marker shape (readability.md §4 test) |

## Checklist — a new or changed troop asset

- [ ] Right home: `units` row (in-game art) or TRP card (recruiting); a map or battle figure is
      the 3D kit, not this lane.
- [ ] Display name from the roster; tier band from the ladder; one accent, GILT only from t9.
- [ ] Card read test at 128 × 160 greyscale: line and tier band named.
- [ ] The card's weapon matches the token's silhouette cue.
- [ ] readability.md §9 run on the card; rubric ≥ 24 / 30, axis 1 = 3.
