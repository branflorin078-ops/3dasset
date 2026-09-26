# UI icons — resources, currency, buttons, glyphs, markers, frames

Home: assets.json group `icons` (out art/gen/icons, install godot/assets/uiicons,
size 128, magenta-key cutout, ref anchor `icons/gold.png`). Group prefix
(verbatim): *"A single game interface icon, one object only, seen straight on,
filling most of the frame, no scenery around it:"*

## Rules

- Single bold silhouette filling ~80% of the frame; 3–4 value steps maximum
  so it survives 44 px; thick consistent rim highlight upper-left (the house
  torchlight); soft contact shadow only (≤20%), nothing cast into scenery.
- The magenta suffix does the cutout — never describe a background beyond
  the group's own suffix; never bake glow halos that fight the key.
- One object. A "pile" is one pile. No hands, no stands, no props
  (intake reject codes: props, stand, two-subjects).
- Existing anchor to match: `icons/gold.png` — condition new icons on it.

## Per-resource colour language (the game's real five + two)

**The shipped rows in assets.json WIN.** Five of the seven below differ
from what shipped (gems ships as a blue sapphire trio, rp as a tome and
quill, iron with forge-heat in the seam, wood as a log pyramid, food with
red cord and apples) — this table is the register for NEW icon work and
proposed redescriptions; regenerating a shipped id changes shipped art
and needs the owner's nod.

| id | fragment core |
|---|---|
| gold | stamped warm-gold coins, one on edge showing a crowned face in relief (the shipped row — match it) |
| food | bound wheat sheaf, husks catching the gold accent, twine visibly knotted |
| wood | split oak logs, end-grain rings and one fresh axe-cut face |
| stone | dressed limestone blocks, chisel marks on the faces, one corner chipped |
| iron | rough blue-grey ingots, casting seams and hammer-flat tops, one dull glint |
| gems | a cut deep-red gem cluster, light pooling inside the stone (premium currency — richer finish than the stock five) |
| rp | an open study-scroll with a brass compass laid across it (research points) |

## Ready fragments (house register)

- **chest (closed)**: A WOODEN CAMPAIGN CHEST: iron-banded oak, riveted
  straps, a heavy hasp closed over a worn lock plate. (Tiers exist in-game:
  Wooden/Iron/Silver/Royal — escalate banding metal and one gilt fitting per
  tier, never size.)
- **chest (open/glowing)**: THE SAME CHEST OPEN: lid back, warm gold light
  rising from inside and catching the underside of the lid, contents
  unreadable.
- **speed-up**: AN HOURGLASS: turned oak frame, sand mid-fall, the falling
  thread catching the gold accent.
- **shield-peace**: A ROUND PARADE SHIELD: parchment-cream field, a single
  gilt laurel ring, rim iron worn to bare metal at the boss.
- **sword-attack**: A BARE ARMING SWORD point-up: honest steel with one
  forge-line down the fuller, crimson grip, gold wheel pommel.
- **level-up**: A CHEVRON OF HAMMERED GOLD rising off an iron base plate,
  edges peened.
- **lock**: AN IRON PADLOCK: heavy shackle, keyhole plate polished by use.
- **seal/checkmark**: A WAX SEAL pressed with an original crowned-tower
  device, deep crimson wax with one gilt fleck.
- **alliance banner**: A HANGING PENNON: oak cross-pole, wool banner in a
  line colour, embroidered original device, frayed fly edge.

## Frames and buttons

Nine-slice frames live in the `panels` group (its suffix already explains
nine-slice; `trim: false`). A frame must be shipped NEAR its display size —
a 58 px border swallowed a 60 px button once (UI-002 lesson). Buttons ride
the `buttons` group. Never put words on either — the game sets its own type.
