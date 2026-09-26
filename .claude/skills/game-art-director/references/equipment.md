# Equipment — the armoury's 24 (EQ-*)

Home: `godot/assets/equipment/EQ-*.png` (via `Equipment.art_path()`); the
2D card art pairs with the 3D gear models in `assets/blender/heroes/`
(`gear_*`, authored from the SAME descriptions — see the `hero3d` skill).
The `data/equipment.gd` `desc` line is the modelling/painting brief for
both: what it names must be visible.

## The real inventory (id = display name)

- Weapons: EQ-armingsword Arming Sword · EQ-greatsword Greatsword ·
  EQ-warbow War Bow · EQ-lance Lance · EQ-warhammer Engineer's Warhammer ·
  EQ-pike Tower Pike
- Armour: EQ-gambeson Gambeson · EQ-fullplate Full Plate · EQ-brigandine
  Brigandine · EQ-cuirass Cuirass · EQ-hauberk Mail Hauberk · EQ-oathplate
  Oathplate
- Helms: EQ-nasal Nasal Helm · EQ-bascinet Bascinet · EQ-hood Archer's
  Hood · EQ-greathelm Great Helm · EQ-kettle Kettle Helm · EQ-crownhelm
  Crown Helm
- Tokens: EQ-banner War Standard · EQ-relic Reliquary · EQ-wolfcloak
  Wolf-fur Cloak · EQ-warhorn War Horn · EQ-rule Engineer's Rule ·
  EQ-signet Signet Ring

## Rules

- One object, studio-lit as a cut-out (magenta-key language when the row
  lives in assets.json), the master block's upper-left key.
- **Material dictionary by physical behaviour**: oiled riveted mail rings
  each catching one glint; hammered plate with planishing marks; leather
  with stretch-creases at the straps and burnish at the edges; yew with
  visible growth rings under wax; wool with felted nap; wax seals with
  pooled edges; brass with lathe lines.
- **Wear-story rule**: every piece carries ONE honest history mark — a
  dent hammered flat, a re-stitched strap, a nick polished out — placed
  where use would put it. (The Kettle Helm's brief is literally "honestly
  dented".) Never distressed everywhere; that reads as neglect, and these
  are maintained arms.
- **The owner's EQ-oathplate lesson**: the prompt must say ARMOUR — "a
  breastplate with an oath engraved on the metal"; every take that led
  with the oath came back a document.

## Rarity language (the game's FOUR tiers — never five)

| tier (register) | finish language |
|---|---|
| Issued | plain field metal, the inlay line reads as brass, no gem |
| Sound | clean steel, one bronze fitting, the inlay warm |
| Fine | etched detail lines, gilt border elements, inlay bright |
| Masterwork | gold inlay chased through, one set gem (deep-red, light pooling inside), the rune inlay BURNING with pale-gold light — "it has a name" |

This mirrors the 3D rune dial exactly (RUNE_ENERGY 0 / 0.7 / 1.5 / 2.6):
the geometry is the same; the LIGHT is the rank. Emission grows; particle
language never appears.

## Ready fragments (subject only; the card suffix does the background)

- **EQ-armingsword**: A KNIGHT'S ARMING SWORD point-up: honest straight
  blade with one forge-line, crimson leather grip, gold wheel pommel
  catching the key light.
- **EQ-hauberk**: A MAIL HAUBERK on display: twenty thousand riveted
  rings reading as woven steel cloth, oiled sheen, dagged hem, one
  repaired patch of brighter rings at the shoulder.
- **EQ-crownhelm**: A COMMANDER'S BASCINET UNDER A GOLD CIRCLET: polished
  steel skull, the circlet's four points worked as original crowned-tower
  devices, arming-cap edge showing at the brow.
- **EQ-warhorn**: AN AUROCHS WAR HORN: smoke-dark horn sweeping a quarter
  turn, silver mouth and mid bands, plaited leather strap, the bell rim
  worn bright.
