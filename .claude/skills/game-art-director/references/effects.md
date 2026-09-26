# Effects — VFX stills and effect icons

Scope: effect ICONS (boost tray, buffs, battle omens — the `odds` group
precedent) and painted VFX STILLS for cards/boards. Live in-game effects
are engine particles/shaders (CPUParticles3D dust, smoke, brazier flare) —
not image-gen; and the commander design law says status effects on lords
are LIGHT, never particle explosions. Keep generated effects in the same
temper: sophisticated, source-lit, restrained.

This file also publishes the **restraint budget** (below): the art-direction limits every
effect honours, painted or live. battle-forge applies them per beat (its presentation.md §6:
"if effects.md publishes a stricter number, the stricter number wins"); feel-forge applies
them to castle and UI juice; world-forge to map states.

## Rules

- **Effects are LIGHT SOURCES**: every effect must cast its own
  illumination onto an implied ground plane or the object it touches —
  a heal that lights the grass under it, a rally beacon warming the
  banner beside it. An effect that casts nothing reads as a sticker.
- Hot core → soft falloff: a small saturated core, a broad warm mid, a
  cool dissolving edge. 3–4 value steps like any icon.
- Motion is directional streaks plus a particle SIZE RAMP (big slow near
  the core, small fast at the edge) — never uniform confetti.
- One effect per image, no scenery beyond the implied plane, the
  negative applies (no runes-as-text — glyph shapes must be original and
  unreadable as letters).
- **Every effect icon has one hard-edged carrier shape** (a ground ring, an object, a
  chevron) that holds the INK contour; the glow sits on it. A pure glow blob fails the 44 px
  edge-band test on PARCHMENT ([readability.md](readability.md) §9 `--icon`: ≥ 70% of edge
  pixels ≥ 25 L* from the ground).

## Palette hooks (on the game's palette, gold-first)

| effect | core language |
|---|---|
| heal | warm green-gold core, soft rising motes, light pooling below |
| damage/explosion | orange-white core, umber smoke rolling off the top, sparks on a size ramp |
| fire | the hearth's language: deep ember base, one hot tongue, smoke that thins |
| shield/ward | a dome of pale-gold light, hexless and smooth, brightest where it meets the ground ring |
| buff/rally | a rising chevron of gilt light with a slow streak trail |
| march trail | churned-earth dashes with dust catching the key light |
| poison/bane | sickly green with a dark edge (the one cool-core effect) |
| magic/arcane | violet core held INSIDE an object (gem, lantern) — the world's magic lives in things, not in air |
| victory burst | gold laurel-light with parchment-cream rays, short-lived, no confetti |

### Hues that collide with the reserved relationship colours

Measured (CIEDE2000) against [readability.md](readability.md) §4. On the map and battle layers
an effect keeps **ΔE ≥ 15** from SELF, ALLY and ENEMY, so a heal never reads as "mine" and a
fire never reads as "hostile".

| effect | colliding tone | ΔE | use instead | ΔE |
|---|---|---|---|---|
| heal | green-gold #B9C35A vs SELF | 11 | gold-leaning green-gold, hue ≤ 100° (#D6C868) | 17 |
| poison | bright green #9CC84A vs SELF | 6 | dark sickly green, L* ≤ 50 (#5E7A2A), dark edge kept | 29 |
| fire | flat vermilion mid-tone #E2572A vs ENEMY | 4 | orange mid-tones, hue ≥ 55° (#F08A2C), yellow-white core, ember base L* ≤ 35 | 21 |
| ward | pale gold #E8D48A vs SELF | 19 | as is | — |
| arcane | any saturated blue vs ALLY | — | violet held inside an object; blue never on the map layer | — |

Boards and cards away from the map layer may keep the heal and fire language as written above.

## Restraint budget — the numbers

Screen sizes use the 1080 × 1920 reference (2,073,600 px). "Cover" = pixels the effect changes
by more than 10% opacity, as battle-forge measures it.

| surface (who builds it) | burst length | cover per effect | cover, all effects | hot core | notes |
|---|---|---|---|---|---|
| Battle beat — normal / counter (battle-forge) | ≤ 600 ms | ≤ 15% / ≤ 20% | ≤ 20% | ≤ 1.5% of the screen (≈ 31,000 px) | emitters ≤ 4, particles ≤ 300 (battle-forge §6) |
| Battle — lord skill peak (battle-forge) | ≤ 1,200 ms (short moment ≤ 700 ms) | ≤ 35% (short ≤ 20%) | ≤ 35% | ≤ 1.5% | the world dims to 75%, never black |
| Battle — breach (battle-forge) | ≤ 1,500 ms + haze 3 s at ≤ 15% | ≤ 40% | ≤ 40% | ≤ 2% | the one allowed large moment |
| Realm map states: ward dome, burning castle, march dust, camp smoke (world-forge) | loops only; any burst ≤ 600 ms | ≤ 5% at region zoom | ≤ 12% | ≤ 0.5% | pulse ≤ 1 Hz; never covers a march line or marker |
| Castle juice: collect, build dust, upgrade done (feel-forge) | ≤ 800 ms | ≤ 10% | ≤ 15% | ≤ 1% | stays on its building's footprint |
| UI ceremonies: chest open, tier up, sworn, victory panel (feel-forge, ui-forge) | ≤ 1,500 ms | ≤ 25% | ≤ 25% | ≤ 2% | the next-action button and a 16 px margin stay clear |
| Lord status: sworn, buffs (commander-forge) | — | rim / glow change only | — | — | LIGHT, no particles (commander design law) |
| **Never, anywhere** | endless loops during a battle beat | > 50% | > 50% | > 3% | full-screen flashes; confetti; neon |

**Envelope of every burst** (60 fps):
- rise to peak ≤ 15% of the burst, at least 1 frame; the peak holds ≤ 2 frames (33 ms);
- the hot core is gone by 30% of the burst; the warm body by 70%; the cool edge, smoke or motes
  dissolve last (to 100%) — the order of real light, then smoke;
- decay is a curve (ease-out), never a linear fade (animation.md: roll-then-land).

**Flash and brightness:**
- ≤ 3 luminance flashes in any 1 s anywhere on screen (WCAG 2.3.1; a flash is a pair of opposite
  changes of ≥ 10% relative luminance); full-screen tints ≤ 15% opacity for ≤ 300 ms; never a
  white frame;
- only ONE hot core at peak brightness at a time — stagger overlapping peaks by ≥ 100 ms;
- additive overdraw ≤ 3 layers at any pixel (a mobile fill-rate cost as well as a whiteout);
- `reduced_motion` halves particle counts (battle-forge §8); cover and timing caps stay.

**Particles** (live effects):
- size ramp: particles at the core 2–3× the size of edge particles; edge particles 1.5–2× faster;
- ≤ 24 particles per normal burst (PROPOSAL, inside battle-forge's ≤ 300 alive); lifetime ≤ the
  burst length; no particle outlives its emitter's beat;
- ground light is an emissive `Decal` or an additive quad, not a real light (battle-forge §6) —
  it satisfies "every effect lights what it touches".

**Layer order:** relationship markers, march lines, count plates, ETA labels and counter badges
draw ABOVE effects. An effect never hides the information channel, even for one frame.

**Money-law:** no fire, blast or battle effect on or behind a control that spends money or
gems; paid surfaces get goods-light only (gold glints, lamp warmth) — environments.md.

## Painted stills and flipbooks (this skill's output)

- **Effect icon**: carrier shape + glow fills 75–85% of the frame (ui-icons.md "~80%"); core ≤ 5%
  of the frame; reads at 44 px (readability.md §1).
- **Effect still for a card or board**: the effect is the focal point — it holds the image's top
  contrast cells (readability.md §2 FOCAL); the implied ground shows the light pool; the core
  ≤ 5% of the frame, the whole effect ≤ 60% so the ground reads.
- **Flipbook**: 4–8 frames at 12 fps (83 ms a frame). One-shots ≤ 8 frames (≤ 667 ms); loops
  exactly 8. The peak is ONE frame; anticipation 1–2 frames before it; the rest is decay
  (animation.md frame-set rules; the shipped chest-open 4-frame sequence is the precedent).
- Every frame of a flipbook passes the same cover and core limits as its live surface above.

## Ready fragments

- **heal glow icon**: A HEALING BLESSING: a warm green-gold light blooming
  above an implied ground, three rising motes on a size ramp, the glow
  pooling in a soft ring below.
- **rally beacon still**: A RALLY BEACON LIT: an iron fire-basket on an
  oak post, one hot flame tongue leaning with the wind, gilt light thrown
  onto a torn pennon beside it, smoke thinning to cool shadow upper-right.
- **shield dome icon**: A WARDING DOME: smooth pale-gold light over an
  implied circle, edge brightest at the ground ring, one soft internal
  glint, nothing inside it drawn.
- **victory light still**: A WAR BANNER IN VICTORY LIGHT: an oak-poled banner lifted, one pulse
  of gold laurel-light behind the cloth throwing parchment-cream rays, the light pooling on the
  trodden ground below, no confetti, no sparks.
- **burning-state still (map layer)**: A KEEP ROOF AFIRE: one hot yellow-white tongue from a
  roof ridge, orange mid-flame, deep ember base in the rafters, grey-umber smoke leaning
  lower-right and thinning — no vermilion fields.

## Failure modes

| fails when | caught by |
|---|---|
| An effect hides a march line, marker, count plate or counter badge | [ ] frame capture of the peak: every information element visible, drawn above |
| Whiteout: one peak frame covers > the surface cap or flashes the whole screen | [ ] battle-forge `vfx_budget_probe` / capture: cover % per frame, flashes per second ≤ 3 |
| Sticker effect: nothing lit around it | [ ] still: light pool on the ground; live: emissive decal present |
| Uniform confetti | [ ] size ramp visible: core particles ≥ 2× edge particles |
| A heal reads as "mine", a fire as "hostile" | [ ] read_check RESERVED on the peak frame ≤ 0.5% outside markers |
| Two effects peak on the same frame | [ ] capture: one hot core at peak at a time |
| A lord's status shown as particles | [ ] review: rim or glow change only |
| Effect icon is a glow blob at 44 px | [ ] readability.md §9 `--icon` edge band ≥ 70% on PARCHMENT |

## Checklist — a new effect

- [ ] Surface named (battle beat, map state, castle juice, UI ceremony, still, icon) and its row
      of the restraint budget copied into the brief.
- [ ] Burst length, envelope (rise ≤ 15%, peak ≤ 2 frames, core gone by 30%), cover and core
      area measured on a capture or the still; numbers pasted.
- [ ] Light cast onto ground or carrier; size ramp; one hot core.
- [ ] Hues ≥ 15 ΔE from the relationship colours on map and battle layers.
- [ ] Information elements drawn above it; no war effect on a paid surface.
- [ ] Rubric (readability.md §8) ≥ 24 / 30 for stills and icons.
