# Portrait lane — painted lords, Edwin is the bar

Today the painted portrait is the only lane where a lord reads as a real
person (game-art-director, "the realism lanes"). This file does not restate
the style: the master style block, the `commanders` group prefix, suffix and
negative live in game-art-director (SKILL.md, references/portraits.md) and
win. This file adds what is lord-specific: the image set per lord, sizes and
crops, the face-structure sheets that keep ONE face across every image, the
value plan, and the rubric. Pipeline: `tools/assets.json` row →
`py tools/gen_assets.py <group> --dry-run` → `<id> --variants 4` →
`--pick <id> N` → `<group> --install` (owner runs; needs the Gemini key).

## 1. The standard

- **Semi-realistic painted.** Real anatomy, real age, the planes of the face
  modelled (brow ridge, cheekbone, jaw, the turn of the skull); stylisation
  lives in brushwork and palette only (the master block), never in
  proportions: no enlarged eyes, no shrunken chins, no smoothed skin.
- **Edwin is the anchor** (`godot/assets/commanders/edwin.png`): every new
  portrait is conditioned on it (the group already is) and judged beside it
  at the same size.
- **House temper, verbatim**: "calm and worn rather than posed". Group
  prefix, verbatim: *"A head-and-shoulders portrait of a named medieval
  commander, three-quarter view, facing slightly left, calm and worn rather
  than posed, one figure only:"* — 85 mm portrait-lens language, eyes on the
  upper-third line.

## 2. The image set per lord

| Id | Frame | Aspect | Master (PROPOSAL; the group's size in assets.json wins) | Shows |
|---|---|---|---|---|
| `CMD-<lord>` | bust | 4:5 | ≥ 1024 × 1280 | head and shoulders, set armour at the collar, signature object edge in frame if natural |
| `CMF-<lord>` | full length | 2:3 | ≥ 1024 × 1536 | standing, whole set worn, signature object held, feet and a ground shadow |
| `SGL-<house>` | sigil | 1:1 | 512 | original device on a shield blank, 3–4 value steps, no letters |
| `SKL-<skill>` | emblem | 1:1 | 512 | one object-moment per skill (design.md §6) |

**One painting per lord, no state variants.** The SWORN state on a painting
is the card/chip's inner gilt edge (ui-forge, `#E0BC6A`, 2–3 px at 128 px),
matching the 3D rim. Painting a second "sworn" version doubles cost and
invites face drift.

Known status (portraits.md): Edwin CMD shipped (the anchor); Elena has a
shipped row; Faber and Fable rows EXIST, conditioned on Edwin, their
installed images are Blender figurine stand-ins (`art_status: stand_in`) —
the work is running the batch, not writing new rows. Everything else: check
the `commanders` group before writing a row; a shipped image is never
regenerated without the owner's nod (checkpoint first, game-director rule 2).

## 3. Sizes, crops and the face rules

| Use | Display px (1080-wide screen) | Crop from | Head (crown → chin) in the crop | Must read |
|---|---|---|---|---|
| Lord detail, no figure yet | ≥ 864 tall | CMF | 11–13% of height (7.5–8 heads, figure ≈ 90% of the frame) | pose, set, signature object, face at arm's length |
| Roster card (4 across) | 256 × 320 | CMD | 40–50% of height | face, expression, set collar |
| List chip | 128 × 128 | CMD | 70–80%, eyes 40–45% from the top | face; identity |
| Avatar (march tracker, reports, chat) | 64 × 64 and 44 × 44 | CMD | 80–90% | head silhouette (helm, hood, hair), hair value, house-colour ring |
| Share card (chat, report) | 96 × 120 | CMD | 55–65% | identity |

- At 44 px nobody reads eyes (3 px). Identity there is the head silhouette
  + hair value + the ring colour; that is why the silhouettes of the eight
  must already differ at the head (kit-sets.md §3, column "Head at 44 px").
- Crops are computed, never hand-cut per size: store per lord a
  `crop.json` (eye centre x, y; crown y; chin y in image fractions) next to
  the installed PNG (PROPOSAL path) and derive every size from it.
- Downscale with a Lanczos filter, then one pass of unsharp mask
  (radius 0.6 px, amount 40%) for ≤ 128 px — thumbnails of painted faces go
  soft without it.

## 4. Face-structure sheets — one face across every image

One paragraph per lord, used **verbatim** in every prompt where the face
shows (CMD, CMF, story paintings). Structure only: age, skull and jaw, brow,
eyes and lids, nose, mouth, skin and marks, hair. All original, never "like"
anyone. **Status: DRAFT.** Edwin and Elena must first be TRANSCRIBED from
their shipped paintings (open the PNG, describe what is there, replace the
draft); Faber and Fable follow their shipped rows (quoted in portraits.md).

- **edwin** (DRAFT, transcribe from edwin.png): a man near sixty, long oval
  face, high forehead with three shallow lines, heavy brow ridge, deep-set
  grey eyes under hooded lids with crow's feet, a straight nose with one old
  step in the bridge, a thin wide mouth, close-trimmed grey beard, dark hair
  cut short and grey at the temples, weathered skin darker at the neck.
- **alric**: a man about forty, broad square skull, heavy jaw with a cleft,
  short thick neck, low straight brows nearly meeting, small dark eyes set
  close, a flattened nose, full lower lip, black hair cropped close, heavy
  stubble shadow, ruddy cheeks, a notch missing from the right ear.
- **elena** (DRAFT, transcribe from her shipped image): a woman in her early
  thirties, narrow heart-shaped face, high cheekbones, straight dark brows,
  level dark eyes with a marksman's slight squint (lower lids raised), a long
  straight nose, a firm closed mouth, dark hair in one thick braid over the
  left shoulder, wind-reddened cheekbones, fine lines at the outer eyes.
- **rowan**: a man about twenty-three, long face, strong straight nose,
  clean-shaven, high arched brows, light brown eyes, a wide mouth lifting at
  one corner, chestnut hair to the collar, windburn across the nose, a healed
  split in the lower lip.
- **godric**: a man in his fifties, round face with heavy cheeks, broad
  forehead and a receding hairline, bushy greying brows, pale blue
  appraising eyes with one deep crease between them, a broad nose, a short
  grey-brown beard, soot in the creases around the eyes, a wax stylus behind
  the right ear.
- **maud**: a woman about fifty-five, long face of strong vertical planes,
  pronounced cheekbones, thin arched brows, grey eyes under heavy lids, a
  straight narrow nose, a mouth set with two deep lines at its corners,
  iron-grey hair pinned tight under a black coif, pale skin, a faded scar
  along the left jaw.
- **faber** (from the shipped row: "broad and sixty … a patient, appraising
  face"): a wide face and wide jaw, short grizzled beard, eyebrows singed
  thin at the outer ends, heavy-lidded patient eyes, a bald crown with a grey
  fringe, small pale burn scars on the forearms, coal-light warming one side.
- **fable** (from the shipped row: "hooded … white beard … deep-set amused
  eyes"): a lean old face, deep-set amused eyes in dark sockets, a long white
  beard to the chest, a hooked nose, hollow cheeks, age spots at the temples,
  ink-stained fingertips.

## 5. Prompt assembly (item-row form)

The row carries the subject only; `_join()` adds style, prefix, suffix and
negative. Order, always:

1. ONE ALL-CAPS subject: title and name ("LORD EDWIN, THE INHERITED VETERAN").
2. The face-structure paragraph (§4), verbatim.
3. The costume = that lord's set (kit-sets.md §1), described by physical
   behaviour (equipment.md dictionary), one honest wear mark.
4. The signature object and what the hands do with it (a hand ON something:
   hands with nothing to do read as a mannequin).
5. The temper in ≤ 10 words.

Worked fragment, `CMF-godric` (full length; check whether a CMF group
exists — if not, a standalone prompt recorded in `art/gen/MANIFEST.md`):

> MASTER GODRIC, THE SIEGE ENGINEER: a man in his fifties, round face with
> heavy cheeks, broad forehead and a receding hairline, bushy greying brows,
> pale blue appraising eyes with one deep crease between them, a broad nose,
> a short grey-brown beard, soot in the creases around the eyes, a wax stylus
> behind the right ear; an oiled riveted mail hauberk to mid-thigh, rings
> catching single glints, one patch of brighter replacement rings at the
> shoulder; a wide-brimmed iron kettle helm, honestly dented above the left
> eye; a faceted steel warhammer with iron langets and an oak haft hanging
> from the belt; the brass folding rule on its leather thong, half-open in his
> right hand, thumb on a graduation; soot
> on the knuckles; weight on the left leg, measuring, not posing.

Rejected on sight: a face paragraph that changes between images; a costume
that is not the set; "handsome", "beautiful", "epic" (banned adjectives);
any real person or character named; a background described beyond the
group suffix.

## 6. Value plan for a lord portrait

Measured on the installed PNG with `tools/figure_check.py --kind bust
--face x0,y0,x1,y1` (the face box by hand, image fractions). PROPOSAL
targets until the anchor is measured (qa.md §6 records Edwin's numbers —
new portraits then match Edwin ±8 L*). A painting has no render mask: give
`--mask` from the cut-out alpha when the group installs a magenta-keyed
cut-out; otherwise figure_check falls back to a border key, printed as
"approximate" — the value bands still hold, the edge numbers need a look.

| Element | L* target |
|---|---|
| Lit side of the face | 60–78 |
| Face mean | ≥ body mean + 5 (the face is the lightest large mass) |
| Shadow side of the face | 25–40 (the master block's "deep cool shadow") |
| Kit | 25–60; one gilt highlight ≤ 85 |
| Background | 6–20; the head never against the lightest part of the vignette |
| Edge separation at the silhouette | ΔL* ≥ 15 (≥ 12 at 128 px) |
| Blown skin | ≤ 2% of face pixels above L* 92 |

## 7. Critique rubric (after every generation)

Score 0–3 each; ship at ≥ 22 / 27 with no axis at 0 and identity ≥ 2.

| Axis | 3 means |
|---|---|
| Identity | the §4 face, same person as the lord's other images side by side |
| Structure | skull, brow, cheekbone and jaw planes read; hands have 5 fingers and knuckles |
| Small read | recognisable at 128 and 64 px (downscale and look) |
| Value plan | §6 met, measured |
| Material behaviour | mail glints per ring, leather burnish at edges, wool nap |
| Wear honesty | one history mark per visible piece, where use puts it |
| Temper | calm and worn; weight settled; no heroic chin-up |
| Set match | every visible piece is from the lord's set, per `data/equipment.gd` `desc` |
| Clean | no text, frame, second figure, stand or prop outside the brief |

Reject codes: the art-director's (text, props, stand, cold, frame,
wrong-subject, two-subjects, off-ladder-colour, weaker) plus **face-drift,
costume-drift, plastic-skin, doll-eyes** (a full iris ring showing, no lid
overlap), **beauty-filter** (poreless, symmetric, too young for the lord),
**pose-hero** (fists on hips, chin up), **hands**, **anachronism**. The fix
is a DELTA prompt — fixes only, never a rewrite.

## 8. Failure modes

| Failure | Looks like | Cause | Fix |
|---|---|---|---|
| Face drift | CMF Elena is a different woman from CMD Elena | face described differently or loosely | §4 paragraph verbatim; condition on the lord's approved CMD if the tool allows a per-item reference (verify in gen_assets.py) |
| Mannequin | empty hands, straight arms | no action in the prompt | §5 step 4: a hand on the signature object |
| Tiny face on the card | the head is 25% of a 256 card | CMF used where CMD belongs | §3 table: crop from the right source |
| Mud at 44 px | a brown disc | head silhouette like the others | kit-sets.md §3 "Head at 44 px" |
| Paint vs render clash | a Blender stand-in beside paintings | mixed lanes in one list | SKILL rule 10; tag `stand_in`, replace |
| Glamour | youthful, smooth Faber | model default beauty bias | age and marks in §4; reject code beauty-filter |

## 9. Checklist

- [ ] Face paragraph transcribed or approved; identical in every prompt
- [ ] Costume = the set; every noun of the equipment `desc` visible
- [ ] Hands doing something with the signature object
- [ ] `figure_check --kind bust` PASS (face box given); numbers pasted
- [ ] Downscaled to 128 / 64 / 44 and looked at; identity holds
- [ ] Rubric ≥ 22 / 27, no 0; reject codes and DELTA recorded
- [ ] Row in assets.json (or MANIFEST.md); `crop.json` written; `art_status` updated
