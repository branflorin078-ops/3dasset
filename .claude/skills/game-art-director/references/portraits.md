# Portraits — commanders, helpers, sigils, emblems

Homes: assets.json `commanders` group (CMD class → godot/assets/commanders/
<id>.png, anchor `commanders/edwin.png`); HLP-* market helpers
(upgrade/GEMINI_HELPERS.md register); SGL-* house sigils and SKL-* skill
emblems beside them. The 3D figures on the hall stage are the `hero3d`
skill's; these are the paintings.

## Rules

- Bust framing, 85 mm portrait-lens language (flattering compression, no
  wide-angle distortion), eyes on the upper-third line, facing slightly
  left (the group prefix already says so — verbatim: *"A head-and-shoulders
  portrait of a named medieval commander, three-quarter view, facing
  slightly left, calm and worn rather than posed, one figure only:"*).
- **ORIGINAL faces described by structure** — age, jaw, brow, scars,
  expression — never by resemblance to any real person or existing
  character. "Calm and worn rather than posed" is the house temper.
- Armour and cloth follow the equipment material rules (physical
  behaviour, one honest wear mark); the face fills most of the frame and
  must read at small card size.
- Rarity/status rim: a lord's SWORN state in-game is a gilt rim light —
  portraits may carry the same warm rim upper-left, never a colour-coded
  aura. Helpers get warm lamplight instead (their register: "a PERSON
  WITH A JOB you can read in one glance").
- Sigils (SGL): an original heraldic device on a shield blank, 3–4 value
  steps, no letters. Emblems (SKL): one ability told as one object-moment
  (a cut fuse, a raised standard), same discipline.

## The real cast (grounding for consistency with shipped art)

Edwin (older infantry lord, grey temples, crimson mantle — the shipped
anchor) · Alric (wins quickly or not at all — dark, heavy-set, wolf-pelt
shoulder) · Elena (archer-commander, dark braid, green hood — shipped row) ·
Rowan (young cavalier, plume and kite shield) · Godric (siege master, wax
stylus behind the ear, bronze instruments) · Maud (stern matron in black,
tower shield's mistress) · **Faber** (the King's Armourer: rolled sleeves,
scorched leather apron over mail, smith's forearms, coal-light) · **Fable**
(the Chronicler: hooded elder, road-grey wool, the chained book at his hip,
lantern warmth on the face). Faber and Fable are `art_status: stand_in` —
their assets.json `commanders` rows ALREADY EXIST (conditioned on the
edwin anchor); what is wanted is running the batch (generate → pick →
install) so `art_status` can flip. Until then their installed portraits
are Blender figurine renders from `tools/blender/portraits.py`.

## Ready fragments (item-row form — subject only)

- **faber**: Master Faber, the King's Armourer, broad and sixty, rolled
  sleeves and scorched leather apron over oiled mail, tongs through the
  belt, coal-light warming one side of a patient, appraising face
- **fable**: Old Fable, the King's Chronicler, hooded in road-grey wool,
  white beard, ink-stained fingers resting on a chained ledger, lantern
  warmth in deep-set amused eyes
- **HLP-style helper**: THE DRILL SERGEANT: barrel-chested man with a
  waxed tally-cord of recruits' tokens, kettle helm pushed back, voice
  mid-bark, honest scarred forearms
