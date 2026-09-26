# Portraits — commanders, helpers, sigils, emblems

Homes: assets.json `commanders` group (CMD class → godot/assets/commanders/
<id>.png, anchor `commanders/edwin.png`); HLP-* market helpers
(upgrade/GEMINI_HELPERS.md register); SGL-* house sigils and SKL-* skill
emblems beside them. The 3D figures on the hall stage are the `hero3d`
skill's; these are the paintings.

Lords end to end — role, kit set, the 3D hall figure, the map token, the lord screens — are
**commander-forge**'s. Its hall-figure lane builds a real human from a licensed base with the
kit made through blender-forge and the `hero3d` rig underneath; its portrait lane points HERE.
This file owns the painted standard every appearance of a lord is matched to.

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
- Sigils and alliance devices keep ΔE ≥ 15 from the reserved relationship colours
  ([readability.md](readability.md) §4) and read as a 2-value black-fill shape at 24 px (the
  chat marker size) — the banner on the map carries them at 28–40 px.

## The semi-realistic painted standard (Edwin is the proof)

The genre's lords are painted semi-realistically with exaggerated features. Ours are
semi-realistic WITHOUT the exaggeration: real people, painted, "calm and worn". Measurable:

| # | rule | number | fails as |
|---|---|---|---|
| 1 | Real head proportions | eye line at 50% ± 3% of the head height (crown to chin); hairline–brow–nose base–chin in near-equal thirds (± 5%); gap between the eyes ≈ one eye width | a doll or a caricature |
| 2 | No exaggeration | no feature scaled more than 10% from those proportions (eyes, jaw, chin, nose) | the genre's cartoon lord |
| 3 | Framing | head (with hair or helm) 50–60% of the frame height; eyes on the upper-third line (± 3% of height); head turned 20–35° (three-quarter), tilt ≤ 8° | a passport photo or a tiny head |
| 4 | Face value plan | lit planes 65–80 L*; shadow side 35–50 L*; ≥ 25 L* between them; the nose's cast shadow falls lower-right | a flat face |
| 5 | Three colour zones of the face | forehead warm ochre; cheeks, nose and ears warmer red; jaw and chin cooler and greyer (strongest on older and bearded men: Edwin, Faber, Fable) | one flat skin hue — plastic |
| 6 | Eyes | one catchlight per eye, upper-left, in the same place in both eyes; the whites ≤ 80 L*, never pure white; a darker ring at the iris edge; the upper lid shadows the eyeball | dead eyes, or two light sources |
| 7 | Edge control | hard edges ≤ 15% of the contour: the near eye, the lit side of the nose bridge, the armour rim; lost edges where the shadow side meets the background | a sticker (all hard) or mush (all soft) |
| 8 | Skin surface | matte; oil highlights only on forehead, nose tip, top of the cheekbone (each ≤ 2% of the face); visible strokes following the form; no single pores drawn at card size | airbrushed plastic |
| 9 | Hair | 3 value masses; ≤ 5 loose strands, only on the lit side against the background | a helmet of hair, or noise |
| 10 | Temper | one asymmetry in the expression (one brow higher, a half-set mouth); weight settled in the shoulders | a symmetric figurine |
| 11 | Character mark | ≥ 1 mark of a life per face, readable at 256 px (a scar, grey temples, crow's feet, a burn, ink stains) | a stock face |
| 12 | Background | ≥ 10 L* darker than the face's shadow side behind the lit profile; one warm rim light may separate the dark side; SWORN = gilt rim | the face sinks into the ground |
| 13 | Detail budget | face = the rich 10%; collar, clasp, pauldron near the face = supporting 30%; the rest of the costume and the ground = quiet 60% ([readability.md](readability.md) §7) | costume louder than the face |

Faber's coal-light is the one documented second light: it warms ONE side of the face from
below the key and never outshines it (≤ 80% of the key side's brightness).

## Read tests for lords

- **Chip size** (battle-forge presentation §3 and §5: the 96 px HUD chip is the smallest; the
  56 dp battle chip is ≈ 140–168 px): all 8 lords side by side at 96 px, a critic who has not
  seen the prompts names each one — 8 of 8. If ui-forge ships a smaller lord chip, the test
  moves to that size.
- **Identity matrix** — each pair of lords differs in at least TWO columns (derived from the
  cast below; commander-forge's per-lord briefs extend it):

| lord | head shape at 96 px | hair / face value | palette accent | signature object |
|---|---|---|---|---|
| Edwin | bare head, older | grey temples (mid-light) | crimson mantle | — (infantry lord, the anchor) |
| Alric | bare, heavy-set, wide shoulders | dark | wolf-pelt grey-brown | wolf-pelt shoulder |
| Elena | hood | dark braid | green | the hood |
| Rowan | tall plume | young, light face | cavalry gold | kite shield |
| Godric | bare, stylus behind the ear | mid | bronze | bronze instruments |
| Maud | veil or close coif (PROPOSAL) | stern, pale face in black | black | tower shield |
| Faber | bare, broad | coal-lit, sixty | scorched-leather brown | tongs through the belt |
| Fable | deep hood | white beard | road-grey | chained ledger, lantern |

  Elena and Fable both wear hoods: they differ in hair value (dark braid vs white beard) and
  accent (green vs road-grey). Alric and Maud are both dark: they differ in head shape and
  build. Keep those contrasts in every new painting of them.
- **At 256 px and above** the expression, the character mark and the three colour zones read.
- **§9 of readability.md** on each portrait with the focal box on the face: FOCAL ≥ 2.0, ≥ 4 of
  6 top cells on the face, SQUINT 3–5 groups.

## One lord, several appearances — who makes which

| appearance | lane | owner |
|---|---|---|
| CMD portrait (bust) | painted image lane | this skill (`commanders` rows) |
| CMF full-length | painted image lane | this skill (INTAKE_MAP prefix) |
| Stand-in figurine render | `tools/blender/portraits.py` | used until `art_status` flips (see Faber and Fable below) |
| Hall figure (3D, the hall stage) | commander-forge figure lane: licensed human base, kit via blender-forge, `hero3d` rig | commander-forge |
| Map token: banner with the lord's SGL device | commander-forge token lane | commander-forge; sigil art here |
| Battle chip 56 dp, skill card 280 px | the CMD painting, cropped | battle-forge |
| SKL skill emblems | painted image lane | this skill |
| Lord screens | layout, ART SHOWN BIG | ui-forge |

The painting is the source of truth for the face: the hall figure is matched to the portrait,
never the other way round. Every appearance keeps the same face structure, palette accent and
signature object.

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
- **Standard delta** (append to any lord row that came back as a figurine): one catchlight
  upper-left in each eye, the face in three warm-to-cool colour zones, the jaw firmer on the lit
  side, one brow slightly raised, visible brushwork following the planes of the face

## Failure modes

| fails when | caught by |
|---|---|
| Plastic skin (one hue, airbrushed) | [ ] rules 5 and 8 checked at 100%; rubric axis 8 |
| Dead eyes, or catchlights in two places | [ ] rule 6 at 256 px |
| Figurine: frontal, symmetric, posed | [ ] rules 3 and 10; the head turn measured |
| Cartoon exaggeration creeping in | [ ] rule 1–2 proportions measured on the image (eye line, thirds) |
| Two lords confused at chip size | [ ] 8-lord sheet at 96 px, blind-named 8/8 |
| Costume louder than the face | [ ] readability.md §9 FOCAL: top cells on the face |
| The hall figure and the painting disagree | [ ] side-by-side: same face structure, accent, object |
| Off the anchor's style | [ ] beside `commanders/edwin.png`: same finish, light, temper |
| A coloured aura instead of the gilt rim for SWORN | [ ] review: warm rim upper-left only |

## Checklist — a new or regenerated portrait

- [ ] Row in `commanders` (or HLP / SGL / SKL register); conditioned on the Edwin anchor.
- [ ] The 13 rules of the standard checked; the numbers for 1, 3, 4 and 6 noted.
- [ ] 8-lord identity sheet at 96 px re-run when a lord's painting changes.
- [ ] readability.md §9 with the face as the focal box; rubric ≥ 24 / 30.
- [ ] For Faber and Fable: `art_status` flipped only after install.
- [ ] commander-forge told when a lord's face changes (its hall figure matches the painting).
