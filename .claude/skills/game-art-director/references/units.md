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
soldier kit.

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
  #C9A76A — one accent per card, never a uniform repaint.

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
  icons exist; engines come from the 3D kit).

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
