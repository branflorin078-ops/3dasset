# Glow — rarity tiers as real light

## The tier ladder (forge.TIERS — calibrated 2026-09-26 on Blender 5.2, AgX)
Castle Conquest's ladder is common / rare / epic / legendary (shown to players
as Issued / Sound / Fine / Masterwork); mythic is kept for the library.

| Tier | Core | Body | Haze | Strength | Breathe | Rim | Behaviour |
|---|---|---|---|---|---|---|---|
| Common | — | — | — | 0 | — | #D9DDE3 at 0.45 gain | no emission, neutral dim rim, no embers |
| Rare | #BCD0FF | #4F7FD6 | #16243F | 2.6 | 0.03 | #6A8FD8 | sapphire, contained in the channel, no embers |
| Epic | #DEC4FF | #8F6ADB | #2E2150 | 4.0 | 0.05 | #8F6ADB | violet, lives only in engraved lines, no embers |
| Legendary | #FFF3C4 | #E8A33C | #4A2F10 | 7.5 | 0.35 | #E8A33C | breathes; one hottest point (`hot_gradient`); embers |
| Mythic | #FFCFC4 | #D6303F | #3D0F16 | 6.0 | 0.55 | #D6303F | crimson; leaks from seams; embers up, ash down |

Strength is applied to `mask^1.6`, so haze stays dim while colour spreads.
Measured on the Sunforged strip (glow-only renders: lights, world and backdrop
off): glowing pixels rare 18.9k → epic 21.4k → legendary 31.8k, hue rare 210°,
epic 273°, legendary 32°, mythic 3°. Sheet: `art/forge/calibration/tier_sheet.png`.

Why the cool tiers carry more strength: per unit strength, blue/violet/red
bodies have ~0.21 luminance against gold's 0.44 — at 1.4 the old rare read as
"slightly blue steel" at 128 px. Contained-tier cores stay SATURATED: a
near-white core reads as light, not as sapphire. Mythic above ~6 paths to
pink-white under AgX (8.0 lost its crimson in the strip). Recalibrate only by
rendering a strip, never by guessing (lessons #29).

## One geometry, every tier — retier()
Rarity is per instance: a piece is raised up the ladder, so every item needs
all four looks on ONE geometry. Build once, wire `add_glow` once, then:
```python
rig = F.studio_rig(center, rim=F.TIERS[tier]['rim'], ...)
for t in ("common", "rare", "epic", "legendary"):
    F.retier(t, rig=rig)                  # glow colours + strength, embers, rim
    F.render(f"{out}/{asset}_{t}.png")
```
`add_glow` tags its tier nodes (`forge:glow_*` labels) and `ember` tags its
objects, so `retier` touches nothing else. `common` keeps the glow wiring at
strength 0 — the same script renders every tier. Tile the strip with
`py tools/rarity_sheet.py sheet.png a.png b.png … --thumb 128` and judge the
128 px row: the tier must read in half a second from rim + glow colour alone.

## Building masks (object space, per part)
Use `MB.obj_axis('X'|'Y'|'Z')` + `MB.map_range` + `math` nodes:
- Channel across a width: `map_range(|x|, 0.1·F, 1.05·F, 1, 0)`.
- Window along a length: product of a rising and a falling `map_range` on z.
- Hottest point: a `map_range` gradient fed to `add_glow(hot_gradient=…)`.
- Ray/spike glow: `map_range(z_local, 0, 0.4·length, 0.8, 0)` — glow at the root.
- Band around a lathed part: `map_range(|z − z_band|, 0.0005, 0.0032, 1, 0)`
  (examples/_template_asset.py).
Masks live in each part's OWN local space — so bake selected-to-active.

## Contrast is the whole trick
Emission reads against darkness. Darken the substrate (steel #7E7466, not
#C9B596) before touching strength. A glowing channel in a recessed groove
(fuller, engraving) reads as light INSIDE the metal — that is the premium look.

## Light behaviour (free in Cycles)
Emissive surfaces genuinely light neighbours: guards pick up gold, grips warm,
underside shadows tint. Keep `sample_clamp_indirect = 8` against fireflies.

## Bloom — a halo, never a haze
`render_setup(bloom=True)` builds a Glare node (Bloom on 4.2+, Fog Glow on 4.0).
- **4.5+ / 5.x (sockets)**: Size is RELATIVE to the frame and Strength is
  ADDITIVE. Calibrated Size 0.0625, Strength 0.40 (`BLOOM_SIZE_AT_7`,
  `BLOOM_STRENGTH`; override with `render_setup(bloom_strength=, bloom_size=)`;
  the legacy int `glare_size` maps to 0.0625·2^(size−7)). The documented
  2^(size−9) mapping (0.25 at size 7) spread a third of the lift 24–96 px from
  the highlights — a warm veil: mid/near lift ratio 0.35 at 0.25, 0.22 at
  0.125, 0.08 at 0.0625, with the near halo unchanged (0.0767 vs 0.0755).
- **4.0–4.4 (properties)**: threshold 0.85–1.0, size 7, mix −0.55 (= 1.124·
  image + 0.326·glare), as calibrated on 4.0.
- `render_setup(bloom=False)` detaches any earlier bloom compositor.

## Embers and particles
`ember(name, loc, tier, size)` — stretched emissive spheres, BODY colour,
3–6 of them, graded sizes, rising from the hottest point. Hidden on tiers with
`embers=False` (common, rare, epic) by `retier`. Mythic adds 2–4 darker ash
flecks drifting down (small grey planes, no emission).
