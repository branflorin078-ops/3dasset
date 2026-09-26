# Lighting and render — the item-card look

## Studio rig (forge.studio_rig)
Key: 1.2 m softbox, upper-left at 45°, energy ~480–900 W.
Fill: camera-right, cool #C9D4E6, ~20% of key.
Rim: behind-right, tall strip (0.6 × 1.6 m), RARITY colour, energy ≥ key —
it traces the silhouette and carries the tier colour.
Hair: faint top light, ~15% of key.
Common tier: rim is neutral white at low power.

## Hero composition rules
- Square 1:1 cards. Weapons diagonal 45–55°: pommel lower-left, point upper-right.
- The decorated face points at the camera, turned 20–35° (three-quarter).
  Never edge-on — verify face-normal · view > 0.8.
- Frame AFTER `render_setup` (needs the aspect). `frame_fill(cam, parts, 0.78)`
  moves the camera in OR out until the bounding box fills 78% of the frame
  (the template's probe finial went from 51% to 78% of the height);
  `frame_camera(cam, parts, margin=1.08)` only pushes back (the Sunforged card).
  1.04 put the pommel against the frame edge — lessons.md #17, #28.
- 85–100 mm lens: product compression, no distortion.
- Floating on `backdrop_radial` (warm centre #2A1B0C → #030304 edge) for items;
  floor + contact shadow only for standing objects (boots, greaves, stands).

## Colour management
AgX + Medium High Contrast (set automatically). Filmic fallback on old builds.
Never Standard: it clips glow to flat colour.

## Sampling and time
Measured 2026-09-26 (Blender 5.2.1, OptiX on RTX 3500 Ada): preview 768² at 48
samples ≈ 2 s per render; Sunforged final 1600² at 110 samples ≈ 7 s of render
(11 s job); a 5-tier strip at 768² 13 s. Single-core CPU reference: preview
1000² at 64 samples (×2.5 with no denoiser) ≈ 2 min; final 1600² at 110 samples
≈ 8–12 min. Card spec is 512 px; 1600 is plenty. Adaptive sampling on,
threshold 0.01. Long jobs → background + poll; the runner queue adds waits
while builders are busy.

## Views
Approval: front 3/4, back 3/4, profile. Card: one hero. Rarity comparison
sheets: identical camera + rig, only materials and rim colour change — loop
`F.retier(tier, rig=rig)` in one process (examples: `tiers` mode) and tile
with `tools/rarity_sheet.py`.
