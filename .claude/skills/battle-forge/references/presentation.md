# Presentation — camera, token squads, counters, lord moments, VFX, sound

How a battle looks and sounds once [beats.md](beats.md) has timed it. The battle is played
where it happened — on the realm map or at the castle — never in a separate battle scene and
never behind a loading screen (live realm ruling). All numbers are **PROPOSALS** measured at a
**1080 px short side** so they hold in either orientation (see the open question in
[../SKILL.md](../SKILL.md)); touch targets ≥ 48 dp (design-forge `ux.md` owns the number).

## 1. Camera — the battle view

transition-forge owns the shot that enters and leaves the battle view (its `shot-library.md`,
zoom model and motion comfort limits). battle-forge owns what the frame must hold once there.

| Rule | Number |
|---|---|
| Pitch | the realm rig's pitch (a fixed 55° per the studio mapping notes of `camera_rig.gd` — verify); no roll, ever |
| Framing | both armies inside the central 70% of the width, 15% margins; squads fill 40–60% of the width |
| Own side | nearest the camera when the rig allows yaw; if yaw is fixed, own banners carry the "self" relationship colour and own strength bars sit on the bottom edge |
| Moves | only at act boundaries or on A beats; ≤ 1 move per 3 s; pan ≤ 20°/s; push-ins ≤ 8% |
| Shake | `Camera3D.h_offset`/`v_offset` only; charge 4 px / 180 ms, ram 3 px per hit, breach 10 px / 250 ms; 18–24 Hz decaying; 0 in reduced motion |
| Hit-stop | 2–3 frames (33–50 ms) on counter impacts and breach only; the first 4 in a battle get it, later ones do not (a stutter every second reads as lag) |
| Slow motion | none. A slowed replay lies about time; hit-stop is enough |
| HUD-free zone | no HUD element inside the central 60% × 60% of the screen |

| Fails when | Caught by |
|---|---|
| A squad leaves the frame during a beat (the player loses the cause) | [ ] `battle_frame_probe` bounds check: every shown actor inside the safe area at its impact frame |
| Camera moves every beat (motion sickness, no reading time) | [ ] timeline probe: camera cues ≤ 1 per 3 s outside A beats |

## 2. Token squads — never a crowd

A march of 80,000 is five squads, not 80,000 soldiers. Strength is a bar and a number; the
figures show line, tier, action and attrition. This keeps readability and frame time
independent of army size (genre pattern: small squad + banner + troop-type icon + health bar
[observational]). Figures are the `hero3d` rig with the soldier kit (game-art-director
`units.md`); never code-built people.

| Line | Figures per squad | Formation | Silhouette cue that must read at 36 px figure height |
|---|---|---|---|
| Infantry | 6 | 2 ranks × 3 | shield + one-handed weapon, squared stance |
| Spearmen | 6 | 2 ranks × 3, spears forward | spear ≥ 1.4× figure height, braced low |
| Archers | 5 | loose staggered line | bow drawn, arm raised |
| Crossbows | 4 + 1 pavise | line behind the pavise | crossbow level at the shoulder, pavise board |
| Cavalry | 3 riders | wedge | horse length > 2× figure height, lance or blade forward |
| Siege engines | 1 model per engine type, ≤ 3 per side | behind the lines | siege-forge models and clips |

1. **One squad per line per side** — a rally's 20 joiners still make ≤ 5 squads a side; joiners
   show as pennons on the squad banners (≤ 6, then a "+N" chip).
2. **Tier reads from the kit** (units.md: "equipment matches the tier economy") and from a tier
   plate on the banner (I–X, XI for cavalry) — UI text, not painted into the art.
3. **Attrition steps**: with `n` figures, figure `k` falls when strength drops below `k/n`
   (infantry: every 16.7%). A fallen figure kneels or lies (`fall`, 400 ms), then sinks and fades
   over 600 ms. No blood, no bodies left on the field (age rating PEGI 7 per the studio notes —
   confirm with ship-forge).
4. **Screen sizes**: figure height ≥ 36 px; squad footprint 120–220 px wide; banner 28–40 px;
   line medallion 44 px (Blender-made icon art — the 44 px survival size); strength bar 88 × 8 px
   under the banner, exact counts on tap-and-hold.
5. **Line accent colours** mark medallions and banner trims only: infantry #B4432E, spearmen
   #8B8F95, archers #4F7A4A, crossbows #6D8AA8, cavalry #C9A76A. Side (self / ally / enemy) is
   the reserved relationship channel on the banner field and the bar (hexes: game-art-director
   `readability.md` and design-forge `ux.md`); the two channels never swap roles.

Clip set per line (hero3d authors; 30 fps authoring per blender-forge animation.md):

| Clip | Frames @30 | Used by |
|---|---|---|
| `idle_ready` | 48 loop | holds, late beats |
| `march` | 24 loop | approach, march-out, return |
| `attack` | 20 | clash (infantry, spearmen) |
| `volley` | 18 | archers, tower tops |
| `shoot` | 16 | crossbows |
| `charge` | 42 | cavalry |
| `brace` | 12 + hold | spearmen |
| `hit` | 8 | any target |
| `fall` | 12 | attrition |
| `rout` | 30 | break |
| `cheer` / `fall_back` | 36 | outcome |

| Fails when | Caught by |
|---|---|
| Figures pile up with army size (frame time grows with the march) | [ ] `battle_frame_probe` rally fixture: skinned figures ≤ 70 |
| Two lines are told apart only by colour | [ ] 64 px greyscale crop of each squad: the tester names the line |
| Tier is invisible (t2 and t9 squads look alike) | [ ] tier strip render t1/t5/t10 per line, named in 1 s |

## 3. The battle on the map (no battle view)

What spectators, hunts and players who did not open the battle view see at the contact point.
It uses only the two march records and the result flag (beats.md §6: 0 extra reads).

| Element | Mid zoom | Far zoom |
|---|---|---|
| Clash marker | crossed-blades medallion 44 px (Blender icon art), ring split in the two sides' relationship colours + a shape per side | 32 px medallion, pulse ≤ 1 Hz |
| Motion | low dust loop at the contact point, ≤ 3% of the screen | none |
| Length | exactly `T_fight` (4 s for a camp inside a hunt order) | same |
| Result | the winner's banner icon for 10 s; a won camp's banner falls over 400 ms | banner icon 24 px |
| Tap | opens the battle card: sides, "Watch" for participants only | same |

## 4. Battle HUD

| Element | Place | Size | Behaviour |
|---|---|---|---|
| Side totals | top edge band ≤ 10% of the short side; own left, enemy right | bar 280 × 12 px; total as text 28 px | count down with each beat (`TRANS_QUART`, `EASE_OUT`, 300 ms) |
| Lord chips | beside each total | 56 dp portraits (painted CMD art) | pulse once when that lord casts |
| Act strip | under the top band | 6 marks, current act gilt | — |
| Skip | bottom-right, thumb zone | 48 dp min, 16 dp from the 2× button | fades in over 200 ms at the skip time |
| 2× | bottom-right | 48 dp | toggles; state remembered |
| Pause | bottom-left | 48 dp | — |
| Floating numbers | above the target squad | 30 px text, 3 px INK outline | shown only for counter hits, skills, decisive beats; ≤ 3 on screen; rise 24 px over 700 ms, fade the last 200 ms |

Numbers are losses in troops ("−1,240"), never "damage points" the player cannot relate to.

## 5. Readable counters — the main genre fix

The genre's counter bonus of about 5% (design-forge `benchmark.md`) is buried under stat
stacks; players conclude that only raw power matters. Our counter is a constant worth one tier
(combat.md §2: the ring Spearmen → Cavalry → Crossbows → Archers → Infantry → Spearmen, c ≈ 26%,
never changed by any bonus) and it is **shown every time it lands**.

| Moment | What the player sees | Timing |
|---|---|---|
| Impact frame | target squad flashes white-gold (`flash` 0 → 1 in 1 frame, back to 0 over 120 ms); hit-stop 2 frames | frame 0 |
| Badge | above the target: attacker line medallion → gilt chevron → target line medallion, 72 px tall; pops from 140% to 100% | 180 ms ease-out-back |
| Hold | badge holds; the loss number shows 25% larger with a gilt edge | 700 ms (Min 2×: 450 ms) |
| First time this pair lands in this battle | a one-line label under the badge in combat.md's own words — "The pike stops the horse — worth one tier" — beside the ring icon with the pair lit (Blender-made, five accents; l10n key) | same hold |
| Exit | badge fades | 200 ms |
| Sound | `bt_counter_sting` (2 notes, metallic); other SFX ducked −3 dB for 300 ms | at impact |

1. **Both directions**: a counter AGAINST the player shows the same badge with an IRON (#3B4048)
   rim instead of GILT — the loser must see what hurt them.
2. **Shape, not colour, carries the state**: favoured = double chevron, even = bar, unfavoured
   = inverted chevron; three distinct silhouettes (alpha-mask IoU < 0.6), made as Blender icon
   art (ui-forge icons, blender-forge). Never white or line glyphs.
3. The same medallions appear in the march form's matchup strip ([flows.md](flows.md) §3) and in
   the report's cause line (report-forge), so the player meets one visual word three times.
4. A salvo of counter hits of the same pair shows ONE badge with "×N" beside the chevron (the
   probe counts N); two different pairs landing together show two badges, never more.

| Fails when | Caught by |
|---|---|
| A counter lands without a badge, or a badge shows where the log has no counter | [ ] `counter_readability_probe`: Σ badge ×N = counter-flagged beats |
| The badge cannot be told apart under colour-blind simulation | [ ] probe: mask IoU < 0.6 between the three states; contrast ≥ 4.5:1 vs the field behind it |
| Badges stack (> 2 on screen) and nothing reads | [ ] probe: max concurrent badges ≤ 2 |

## 6. Lord skill moments

The lord is the player's investment; the cast is the one place the battle is allowed to stop
and look. commander-forge owns each lord's portrait, emblem and signature effect; battle-forge
owns the template.

| t (ms) | Full moment (2,000 ms) | Short moment (900 ms) |
|---|---|---|
| 0 | world dims to 75% brightness over 150 ms (never black) | no dim |
| 150 | portrait card slides in from the caster's side, 280 px tall (painted CMD art — ART SHOWN BIG), ease-out cubic 220 ms | the lord's HUD chip scales 1.0 → 1.7× → 1.0 over 600 ms, emblem beside it |
| 370 | skill emblem (SKL art) + name, 1 line, ≤ 24 characters in English (+40% room for l10n) | — |
| 500 | signature effect on the field, 800–1,200 ms, ≤ 35% cover | effect ≤ 700 ms, ≤ 20% cover |
| 1,700 | undim 200 ms; card slides out 180 ms | — |

Rules: each lord's **first** cast in a battle is a full moment, later casts are short; full
moments are ≥ 6 s apart (a second one inside 6 s plays short); an enemy lord's cast uses the
same template on the other side; two casts inside 1 s → the second plays short with its effect.
Repeated casts of the same skill inside one act may merge into one short moment marked "×N" on
the chip ([beats.md](beats.md) §3 priority rule) — every cast is counted, none is hidden.

Staging per lord — PROPOSAL until commander-forge's per-lord briefs land (roles from
design-forge `lords.md`, looks from game-art-director `portraits.md`):

| Lord | Moment (magic lives in objects; light, not particle storms) |
|---|---|
| Edwin | the infantry banner lifts; a rising gilt chevron above the shield line; crimson mantle on the card |
| Elena | one long volley whose arrow streaks carry warm light; green hood on the card |
| Rowan | the cavalry wedge's dust wake lengthens; plume and kite shield on the card |
| Godric | every engine releases on the same frame; a bronze instrument glints on the card |
| Maud | a pale-gold ward dome over the garrison, brightest at the ground ring |
| Alric | the first contact lands with a doubled impact ring (still ≤ 35% cover); wolf pelt on the card |
| Faber | armour on one squad gains a bright edge sheen (roughness drop) for the rest of the act |
| Fable | a chronicle page turns on the card; one hidden enemy tool is outlined for 1 s |

| Fails when | Caught by |
|---|---|
| Moments chain and the battle becomes a slideshow | [ ] timeline probe: full moments ≥ 6,000 ms apart |
| A lord's moment is indistinguishable from another's (8 lords, one effect) | [ ] frame review: 8 peak frames side by side, each named by a tester |

## 7. VFX restraint

game-art-director `effects.md` owns the art rules (effects are light sources; hot core → soft
falloff; gold-first palette); battle-forge applies them per beat. If `effects.md` publishes a
stricter number, the stricter number wins.

| Limit | Normal beat | Counter | Skill peak | Breach | Never |
|---|---|---|---|---|---|
| Screen cover (pixels changed > 10% opacity) | ≤ 15% | ≤ 20% | ≤ 35% | ≤ 40% | > 50% |
| Burst length (one emitter) | ≤ 600 ms | ≤ 600 ms | ≤ 1,200 ms | ≤ 1,500 ms + haze 3 s at ≤ 15% | endless loops during beats |
| Emitters alive | ≤ 4 | ≤ 4 | ≤ 6 | ≤ 6 | — |
| Particles alive (all) | ≤ 300 | ≤ 300 | ≤ 500 | ≤ 500 | — |
| Dynamic lights | 0 | 0 | ≤ 1 `OmniLight3D`, no shadow | ≤ 2, no shadow | shadowed dynamic lights |

- Ground light from an effect is an emissive `Decal` or an additive quad, not a real light
  (mobile cost); it satisfies effects.md's "every effect lights what it touches".
- Luminance flashes ≤ 3 per second anywhere on screen (WCAG 2.3.1 general flash threshold).
- No confetti, no neon, no screen-wide colour washes; the victory "burst" is gold light on the
  winner's banner only (effects.md: short-lived, no confetti).
- Particles: `GPUParticles3D` with `one_shot = true` from a pool; `CPUParticles3D` fallback on
  devices ship-forge marks as low tier.

## 8. Sound

audio-forge owns assets, buses and loudness; battle-forge names the cues (`bt_*`, beats.md §3)
and the mix rules.

| Rule | Number |
|---|---|
| Music under battle | ducked −6 dB (attack 150 ms, release 600 ms) |
| Battle bed | wind + distant host loop, fades in over 400 ms in act I, out over 800 ms after the outcome |
| Stingers (counter, skill, breach, outcome) | duck other SFX −3 dB for 300 ms |
| Voices | ≤ 12 simultaneous battle voices |
| Variants | ≥ 3 takes per one-shot, chosen by the seeded RNG; pitch ±3%; the same take never within 150 ms |
| Win and loss stingers | equal loudness (±1 dB); the loss stinger is low and settled, never mocking |
| Sound off | every cue has a visual twin (badge, flash, chip) — the battle must read muted |

## 9. Reduced motion and accessibility

`UI.reduced_motion` (studio mapping notes — verify the name) switches: shake 0, push-ins 0,
hit-stop 0, camera moves become 200 ms crossfades, particle counts × 0.5, dim 90% instead of 75%.
Timings stay the same so the replay is the same length. Text ≥ 28 px at the 1080 px short side;
subtitles for the lord's voice line if one plays (story-forge writes the line).

## 10. Performance budget (battle view)

The frame target is ship-forge's (60 fps assumed here: 16.7 ms).

| Budget | Limit |
|---|---|
| Frame time | p95 ≤ 16.7 ms; no frame > 33.3 ms at beat boundaries |
| Draw calls (`RenderingServer.get_rendering_info(RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)`) | ≤ 150 |
| Visible triangles | ≤ 250k (castle kit LODs per blender-forge `architecture.md`) |
| Skinned figures | ≤ 70 (2 sides × 5 squads × ≤ 6 figures + climbers) |
| Asset load | all battle resources requested at contact − 10 s; 0 synchronous `load()` during a battle |
| Extra memory | ≤ 64 MB above the realm view |

## 11. Checklist — a presentation change

- [ ] Frame captured with Movie Maker at 60 fps (qa.md §4) and the key frames looked at.
- [ ] Cover, emitters, particles and lights measured against §7, verdict line pasted.
- [ ] Counter badge present for every counter beat, in both directions.
- [ ] Reads with sound off and in reduced motion.
- [ ] Line identity readable in greyscale at 64 px.
- [ ] Frame-time capture on the heaviest fixture (siege + rally + 3 engines).
