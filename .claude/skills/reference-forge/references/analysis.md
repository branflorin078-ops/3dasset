# Analysis — turning references into a reference sheet

Write this as `REFERENCE.md` in the asset folder BEFORE touching the build.
Every line cites a reference id (`met_22407`, `local_Blacksmith…`).

```
ASSET: <game id> — <name>   CLASS: <sword|hafted|bow|helm|plate|mail|textile|jewellery|horn|instrument|chrome|architecture>
GAME BRIEF: "<desc from data/equipment.gd>"  — every noun must be visible

REFERENCES (6–10): id · title · date · measure_cm · why it was chosen

PROPORTIONS (from measure_cm; ratios, not absolutes — our scale anchors are in blender-forge forms.md)
  - overall H:W:D = …           (e.g. cabasset 20.95 : 21.91 : 26.67 → 0.96 : 1.00 : 1.22)
  - key part ratios = …          (brim width / skull width; blade length / grip; ricasso / blade)
  - thickness cues = …           (rolled edge ≈ 2× plate; rivet head ⌀ ≈ 6–8% of brim depth)

CONSTRUCTION (what physically holds it together — each becomes geometry)
  - parts list, joins, fasteners, lining/strap points, how many rivets and where

MATERIAL + FINISH
  - base metal/wood/leather, surface treatment (bright, russet, blued, etched, gilt),
    where finish changes (bands, borders), roughness breakup direction

DECORATION
  - WHERE it sits (borders, bands, medial ridge, cartouches), its SCALE relative
    to the object (band width ÷ object height), its density; which our design keeps

WEAR LOGIC
  - where use touches (grip, rim, keel), where grime collects (rivets, cavities)

LOOK TRUTH (owner boards)
  - palette + stylisation level the game wants for this class

ORIGINAL TWIST
  - what we change so it is ours (motif, proportion push, a signature element)
```

## Per-class checklists (what to look for first)

- **Blades**: blade length : grip length : guard span; fuller length (% of
  blade); distal and profile taper; pommel form; ricasso on two-handers.
- **Hafted**: head length : haft length; langets (length); socket; balance
  point near the head; butt cap.
- **Helms**: skull height : width; brim projection (% of skull); comb height;
  sight/breath placement; rivet ring spacing; lining-rivet band; neck flare.
- **Plate**: lame count and overlap; keel/medial ridge; rolled edges (thickness
  ×2 at the roll); strap-and-buckle points; fauld/tassets articulation.
- **Mail**: ring size relative to the garment (never a noise texture at
  garment scale); edges bound with leather or brass rings.
- **Textiles/soft goods**: quilting channel width; fold scale; seam logic.
- **Jewellery**: bezel shape; stone cut and size relative to the ring; engraving depth.
- **Horns/instruments**: band spacing; mount hardware; strap attachment.
- **UI chrome**: joinery (mitres, pegs), carving depth, gilt only on raised
  edges, wear at corners — a frame is furniture, not a gradient.
- **Architecture**: batter, string courses, block size vs storey height;
  roof pitch and overhang; opening reveal depth; quoin pattern; how loads
  come down (corbels, buttresses, jetty joists). Then the game read:
  job prop, roof identity, silhouette change per tier (blender-forge
  `references/architecture.md` §2–5).
