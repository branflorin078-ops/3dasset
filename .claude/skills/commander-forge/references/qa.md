# QA — gates, measurements, the lineup, the diagnosis

"Looks fine" is not a verdict. Every lord asset passes its lane's gates
with the numbers pasted, and every image is OPENED before it is judged
(blender-forge rule 8). Stop after 5 critique loops and report the residual
gap honestly.

## 1. Gates per lane

| Lane | Automated gates (all must pass) | Visual gates |
|---|---|---|
| Kit piece | blender-forge qa.md: topology zeros, bake channels inspected, emission at its analytic strength, GLB round trip; budgets (export.md) | the 12-point list; set sheet read as one kit (kit-sets.md §4) |
| Fitted piece | `QA_FIT` 2 mm ≤ min clearance ≤ 1.5 × intended offset; poke-through in 3 poses | no gap at collar and armpit, no skin through plate |
| Hall figure | `QA_BASE` pasted; `quality_report` zeros on the game mesh; `FIGURE_CHECK … fail=0` for bust AND full; `--pair` PASS; GLB re-imported with joints; ≤ 45k tris, ≤ 6 materials | §5 figure list F1–F12; lineup §3 |
| Portrait | `FIGURE_CHECK --kind bust` with the face box, fail=0 | rubric ≥ 22 / 27 (portrait-lane.md §7); 128 / 64 / 44 px looked at |
| Token | `FIGURE_CHECK --kind token` on crops; LOD ranges set with margins | read test 18 / 20; colour-blind check (token-lane.md §7) |
| Screens | the harnesses of screens.md §10 green | art zone ≥ 45% on every tab, every state shown |
| In engine | the core gate (game-director) after any GLB lands | look-dev match: face L* ±8, value bands ±5 points |

## 2. figure_check — what each number means

Thresholds are PROPOSALS until §6 records the first approved lord; then
they are tightened to that lord's numbers minus 10%.

| Check | Measures | Target (bust / figure / token) | A fail means | Go to |
|---|---|---|---|---|
| `fill_h` | subject height / frame height | ≥ 0.85 / 0.78–0.92 / — | lord too small, or cropped | camera, `frame_fill` |
| `solidity_128` | subject area / convex hull at 128 px | — / 0.45–0.82 / 0.40–0.85 | > 0.82 a blob (arms glued, no object out); < 0.45 spiky noise | pose, signature object |
| `windows_128` | enclosed background holes at 128 px | — / ≥ 1 / — | no negative space between arm and body | pose (figure-lane.md §6) |
| `sep_dL`, `sep_dL_128` | L* difference across the silhouette edge (full, 128 px) | ≥ 15 and ≥ 12 / same / ≥ 18 at 128 | the lord melts into the ground | rim, kicker, backdrop centre |
| `band_dark / mid / light` | share of subject pixels at L* < 30 / 30–65 / > 65 | ≥ 0.08 / 0.15 / 0.05 | a value group missing (no shadows, no lights) | key : fill ratio, materials' value spread |
| `band_max` | the largest band | ≤ 0.75 | grey soup: one value everywhere | value plan |
| `rim_ratio` | rim-side edge band L* / band 2k–4k px inside | ≥ 1.10 | no light on the silhouette edge | rim energy, position (`rim_side`) |
| `face_minus_body_L` | face mean L* − body mean L* | ≥ 5 / ≥ 3 | the kit outshines the face | key aim, kit emission ≤ 3% |
| `face_clip` | face pixels above L* 92 | ≤ 0.02 | plastic sheen, blown skin | key energy, skin roughness |
| `face_chroma` | mean C* in the face | 10–40 | < 10 dead grey skin; > 40 orange cartoon | albedo, mottle, white balance |
| `face_px_128` / `face_px_256` | face box height with the image 128 / 256 px tall | ≥ 32 / ≥ 24 | face too small for the card | crop (portrait-lane.md §3) |
| `face_detail_ratio` | high-pass energy in the face / in the body | ≥ 0.90 (bust) | the face is the emptiest area | pores, wrinkles, eyes (figure-lane.md §3–4) |
| `sworn_dL`, `sworn_db` | sworn − unsworn on the rim-side edge band | ≥ 4 L*, ≥ 5 b* | the sworn state does not read | `RIM_GAIN`, rim position |

Command forms:
```
py tools/figure_check.py <render.png>                                  # mask + meta found beside it
py tools/figure_check.py <render.png> --pair <unsworn.png> --sheet <check.png>
py tools/figure_check.py <painting.png> --kind bust --face 0.30,0.14,0.62,0.52
py tools/figure_check.py --lineup <l1_mask.png> <l2_mask.png> ...      # §3 pre-check
```
Exit code 1 on any FAIL, so a chain stops on a red lord.

## 3. The silhouette lineup

1. Render every lord full length with the SAME camera distance and lens
   (85 mm, framed on the tallest lord, so heights compare), through
   `render_with_mask`.
2. Pre-check: `figure_check --lineup` on the eight masks — every pair's
   overlap (IoU, 128 px tall, feet aligned) ≤ 0.80. A pair above is
   re-posed or re-kitted before the human test.
3. Human test: the masks as black shapes at 128 px, shuffled, unlabelled
   (tile with `blender-forge/tools/rarity_sheet.py lineup.png m1.png …
   --labels 1,2,…,8`). A reviewer who did not build them names each lord:
   pass ≥ 7 / 8. Record every confusion pair and its fix (kit-sets.md §3).
4. Repeat for the head crops at 44 px (portrait-lane.md §3): the eight
   heads told apart ≥ 7 / 8.

## 4. The "empty figurine" diagnosis

The owner's complaint, turned into signals. Measure first, then fix the
cause the signal points to.

| The owner sees | Signal | Cause | Fix (function / parameter) |
|---|---|---|---|
| "empty figurine" | `face_detail_ratio` < 0.9; `band_max` > 0.75 | no tertiary detail; flat light | pores + roughness zones (`mat_skin pores=, rough=`); `hero_rig` key : fill 5.5 : 1 |
| "no contrast" | `sep_dL` < 15; `band_dark` < 0.08 | dark kit on a dark ground; fill too strong | rim / kicker; `fill_ratio` 0.15–0.20; backdrop centre `#241A10` |
| "plastic" | `face_clip` > 0.02 | uniform low roughness | `rough=(0.38, 0.52)`; `spec=0.5` |
| "wax doll" | ears glow; soft shadow edge | subsurface scale too large | `scale=0.004` |
| "dead eyes" | no catchlight in the eye crop | no eye light; rough cornea | `eye_light=True`; `mat_cornea` roughness 0.02 |
| "toy armour" | uniform shine across the set | one roughness for all metals | set spread ≥ 0.30 (kit-sets.md §4); `mat_metal rough=` per metal |
| "floating kit" | `QA_FIT` > 1.5 × offset | profile not from the body | `plate_on_body(samples=3)` |
| "stiff" | `windows_128` = 0; `solidity_128` > 0.82 | base A-pose, empty hands | contrapposto, hands on objects (figure-lane.md §6) |
| "all the same" | lineup IoU > 0.80 | same pose, same outline | kit-sets.md §3 silhouettes; distinct pole tops |
| "cheap glow" | kit emissive > 3% of pixels; `face_minus_body_L` < 3 | card-strength emission on the figure | rune dial values; substrate `#7E7466` |

Detail placement (the 60 / 30 / 10 rule of forms.md applied to a person):
clusters at the face, hands, collar, belt and joints (rivets, buckles,
seams, the signature object); rest areas on the big plates, the mantle,
the apron. A figure with detail spread evenly reads as noise; with none,
as a toy.

## 5. Visual critique — the figure list (after blender-forge's 12)

| # | Check |
|---|---|
| F1 | The face reads at 256 px (card) and the lord is named from it |
| F2 | Catchlights in both eyes; upper lids cover 1–2 mm of the iris |
| F3 | Skin: roughness changes across the face at 1:1; no wax at the ears |
| F4 | The hair edge breaks the silhouette (flyaways), no helmet hair |
| F5 | Kit fits: no gaps, no clipping at collar, armpit, waist |
| F6 | Every piece carries one honest wear mark, where use puts it |
| F7 | The set reads as one kit (one metal family, one motif scale) |
| F8 | Both hands hold or rest on something |
| F9 | Contrapposto: weight on one leg, counter-tilt in the shoulders |
| F10 | The face is the lightest large mass; one gilt accent, not five |
| F11 | Sworn and unsworn differ at a glance (the pair) |
| F12 | At 44 px the head silhouette is still this lord |

Fix the first failing item, re-render the preview, repeat.

## 6. Calibration record

**Probe** (`examples/figure_probe.py`, stand-in primitives — they calibrate
the RIG and the TOOL, never the art), Blender 4.0.2, 4 CPU cores, no
denoiser, 384 × 480, 24 samples, 2026-09-26:

| Pass | Key | Result |
|---|---|---|
| 1 | 260 W, rim 0.55× / 1.15× key, rig not camera-relative | `face_L` 79.7, `face_clip` 0.041 FAIL, `rim_ratio` 1.045 / 1.063 FAIL |
| 2 | 150 W, rim 0.6× / 2.2×, rig rotated with the camera yaw | `FIGURE_CHECK pass=15 fail=0`: fill_h 0.852, sep_dL 47–50, bands dark / mid / light 0.17 / 0.52 / 0.31, rim_ratio 1.115 / 1.145, face_clip 0.002 / 0.017, face_chroma 26–28, sworn_dL +6.0, sworn_db +8.1 |

`QA_FIT` 8.76 mm for a 25 mm offset with taper 0.08 (figure-lane.md §7).
Job time 32–59 s per preview pair on that CPU.

To record next (the thresholds move to these): Edwin's shipped portrait
measured with `--kind bust --face …` (the portrait-lane anchor); the first
approved hall figure, bust and full.

## 7. Engine-side harnesses

| Change | Run |
|---|---|
| Lord screens | `menu_test`, `layout_audit`, `ux_flow_probe`, `ux_touch_probe`, `a11y_audit`, `contrast_test`, `w1f_aspect_sweep` (`ASPECT SWEEP OK - 6 shapes, 0 faults`) |
| A figure or token GLB in the game | the core gate (game-director: the headless battery + the real boot test) and the windowed suites it lists |
| Map tokens | `map_trap_probe`, `pm_render_probe`, the read test (token-lane.md §7) |
| Server cost of a lord feature | `core/sd_cost_probe.gd` (design-forge rule 5) |

Proposed to qa-forge: `lord_screen_probe` (screens.md §10) and a hall
look-dev capture that screenshots each lord at the Cycles framing for the
±8 L* match.

## 8. REPORT.md — the evidence format

```markdown
# HERO-<lord> — <status: SHIP | ITERATE | STAND_IN | FAILED>
Sources: base <file> (<licence>, checked <date>), head <sculpt|scan> (<licence>)
Loops used: n / 5
QA_BASE {...}
QA_FIT  {...}   (one line per fitted piece)
QA_GAME {...}   IMPORT {... joints: n}
FIGURE_CHECK <bust> kind=bust pass=n fail=0      sworn_dL +x.x sworn_db +x.x
FIGURE_CHECK <full> kind=figure pass=n fail=0
LINEUP_CHECK masks=8 pairs=28 fail=0 worst=<a>/<b> 0.xx   human lineup 8/8
Look-dev match: face L* Cycles xx.x / Godot xx.x; bands within ±n
Files: <renders, sheets, GLB, textures>
Open questions / residual gap:
```

## 9. Lessons (dated; add every trap that cost a loop)

1. **2026-09-26 — a relative outdir lands next to the script.** The runner
   starts Blender with the script's folder as the working directory, so
   `run build.py preview out/x` wrote into the skill folder while the log
   went to the caller's `out/x`. Always pass an ABSOLUTE outdir.
2. **2026-09-26 — `plate` taper eats clearance.** Taper 0.08 on a 0.195 m
   half-width pulled the top edge in 16 mm: 25 mm offset → 8.76 mm. Print
   `QA_FIT` after every fitted piece.
3. **2026-09-26 — skin blows out first.** At 260 W / 2 m the probe's face
   hit L* 80 with 4.1% clipped; 150 W with the same rig passed. Measure
   before judging by eye.
4. **2026-09-26 — the sworn rim is subtle on matte materials.** On skin and
   wool the gilt rim moved the edge by +6 L* / +8 b*; on armour it reads
   stronger. Always render and measure the sworn PAIR.
5. **2026-09-26 — `forge.export_glb` keeps skins** (Blender 4.0.2: armature,
   bones, vertex groups back after re-import; the subdivision applied).
6. **2026-09-26 — MPFB2 does not load under `--factory-startup`** (the
   runner's default, blender-forge lessons #22): generate bases in a
   separate session, save them to `base/`, import the files.
7. **2026-09-26 — the sandbox Blender 4.0.2 build has no OpenImageDenoiser**
   ("Build without OpenImageDenoiser" in the log): render_setup falls back
   to 2.5× samples — slower, not wrong. The owner's 5.2.1 has a denoiser.
