# Forms — building real shapes, not stacked primitives

## The core idea: design the cross-section, then vary it along a path
Every crafted object is a small number of cross-sections moved through space.
A blade is a lenticular section tapering along its length; a grip is a circle
swelling in the middle; a quillon is an ellipse swept along an arc. Design the
section on paper-logic first, then choose the operator:

| Operator | Use for | forge.py |
|---|---|---|
| **Loft** — rings of points joined into quads | blades, spear heads, axe bits, ray spikes, horns, limb splints, arrow shafts with fletch taper | `loft(name, sections)` |
| **Lathe** — revolve a (radius, height) profile | pommels, gems, finials, ferrules, helm bowls, goblets, towers, domes, bottles, bolts | `lathe(name, profile, segments)` |
| **Sweep** — tube along a polyline, per-point radius | quillons, wire wraps, filigree, chains, lacing, straps, crowns of thorns, roots | `sweep(name, pts, radius, taper=…)` |
| **Subdivide** — low cage + subsurf with support loops | organic props: leaves, cloth folds, pouches, soft leather | `subsurf(ob, levels)` |
| **Boolean** (sparingly) | sights, visor slits, breaths, rivet holes, windows, crenels | `slot_cutter` + `boolean_cut(target, cutters)` — applied first in the stack, per shell, welded, bevelled |

## Armour and jewellery operators (lib/forge.py, all watertight — tests/test_operators.py)
| Operator | Builds | Key parameters |
|---|---|---|
| `helm_shell` | a raised bowl as ONE sheet: lathed superellipse bowl whose lower edge is drawn out per azimuth into a tail (sallet) or brim (kettle hat); real thickness; armourer's rolled rim | `radius, height, thickness, squareness` (2 round, 2.3+ flatter crown), `apex` (bascinet point), `tail, tail_flare, tail_width`, `brim`, `roll`. Face −Y, tail +Y |
| `slot_cutter` → `boolean_cut` | stadium-section cutters (length = width → round hole) cut out and cleaned | place/rotate the cutter first; `boolean_cut(target, [cutters], bevel=0.0005)` |
| `plate` | an armour plate from a horizontal PROFILE curve: belly (`bulge`), `taper`, thickness, rolled `top`/`bottom` edges, overlapping `lames` (lower behind upper) | profile drawn left → right, outer face toward −Y; `lames, overlap, roll, roll_edges` |
| `rivet` / `rivet_row` | domed snap rivets at equal arc-length spacing, heads along a normal or snapped to a surface, sunk 0.4 mm; one mesh instanced | `count` or `spacing`, `surface=obj`, `join=False` → linked duplicates |
| `strap` / `buckle` / `strap_buckle` | leather strap (rounded-rectangle section, parallel-transport frames, round tip) + centre-bar buckle (frame, bar, prong) seated on it | `width, thickness, up, tip`, `at` (arc fraction) |
| `gem_brilliant` | round brilliant, 73 PLANAR facets (table, 8 star, 8 bezel, 16 upper girdle, 16 girdle, 16 lower girdle, 8 mains, culet), Tolkowsky proportions, flat shaded | `diameter, table 0.56, crown 0.162, pavilion 0.431, girdle 0.03` |
| `gem_cabochon` | smooth oval dome on a short girdle with a chamfered back | `rx, ry, height, base, dome` |

Helpers: `resample(points, n, closed, smooth)` (arc-length, Catmull-Rom) and
`path_frames(points, up)` (twist-free frames) for anything with a section.

### Recipes (metres)
- **Sallet**: `helm_shell(radius=0.104, height=0.150, squareness=2.3, tail=0.085,
  tail_flare=0.045, tail_width=150, roll=0.0024)` → `hard_surface(0.0006)` →
  two `slot_cutter(0.062, 0.0085, 0.08)` sights at z 0.058, x ±0.036 →
  `boolean_cut` → brow `rivet_row(..., surface=helm)` (examples/armour_kit.py).
- **Kettle hat**: `helm_shell(radius=0.10, height=0.12, brim=0.06, roll=0.002)`.
- **Bascinet**: `helm_shell(radius=0.10, height=0.17, apex=0.25)` + face opening by `boolean_cut`.
- **Fauld / tassets / pauldron lames**: `plate(arc, height=0.17, lames=4, overlap=0.3,
  bulge=0.012, roll=0.0026, roll_edges=('top','bottom'))` + two rivets per lame.
- **Breastplate**: `plate(arc with depth 0.06, height=0.32, bulge=0.02, taper=0.18, roll=0.003)`.
- **Belt**: `strap_buckle(path, width=0.028, thickness=0.0032, at=0.42)`; leather
  `mat_leather(edge=0.0005)` for a 3 mm strap (lessons #9).
- **Set stones**: `gem_brilliant(diameter)` flat-shaded + `mat_gem`; cabochons for
  pommels and bosses; sink both 0.2 mm into a bezel.

A target that is several closed shells (helm + rolled rim) is cut shell by
shell — never boolean overlapping shells as one object (lessons #27).

## Blades (loft recipe — see examples/sunforged_greatsword.py)
- Section: lenticular `y = T·(1−|x|^2.2)^0.62` across normalised x ∈ [−1, 1],
  edges exactly at y = 0 (sharp), ~23 samples, dense near the centre for the fuller.
- Fuller: subtract `D·cos²(π/2·|x|/F)` inside |x| < F → a rounded groove, faded
  in/out along the length with smoothstep windows.
- Taper: width −22% to 80% of length, then an ogive to the point
  `(1−u^1.7)^0.75`; distal thickness taper −55%.
- 60–80 sections along the length. End with a microscopic ring, not a pole.

## Lathe profiles library (radius, height) — starting points
- Wheel pommel: face rim raised at 0.034/0.036 of a 1.4 m sword; axis turned to face viewer.
- Scent-stopper pommel: pear body r≈0.022, neck r≈0.011, button r≈0.006.
- Round brilliant gem: `[(0,−0.47d),(r,0),(0.65r,0.30d),(0,0.33d)]`, 8–12
  segments, FLAT shading = real facets.
- Helm bowl: quarter-ellipse with a lip; add a sweep for the brow band.
- Tower: slight batter (base radius +6%), string course every storey, crenels by boolean.

## Proportion anchors (real-world metres)
Arming sword 0.95 total · longsword 1.15 · greatsword 1.40 · grip ≈ 1 hand
(0.10) per hand · quillon span ≈ 0.22–0.32 · kettle helm brim ⌀ 0.40 ·
kite shield 0.95 tall · ring ⌀ 0.020 · gorget ⌀ 0.16 · castle wall module 4.0.
Build at real scale; the renderer, bake distances and Godot all expect metres.

## Silhouette and hierarchy
- Primary forms carry 60% of the read, secondary 30%, tertiary 10%.
- Test the silhouette as pure black at 64 px — rarity must read there.
- Asymmetry is character (one wing pauldron, one replaced splint), symmetry is order.
- Tertiary ornament must survive card resolution: test at 256 px; scale up ~1.6x
  from what looks right in isolation.

## Anti-patterns (reject on sight)
Cubes as armour plates · cylinders as limbs · spheres as gems (use lathe facets)
· unbevelled edges · uniform thickness everywhere · perfectly straight "steel"
with no taper · ornaments floating off the surface (sink them 0.2 mm in).
