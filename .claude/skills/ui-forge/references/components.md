# Components — the painted kit, measured

Every screen is built from these parts and nothing else (SKILL.md hard rule 13). Sizes are
design px on the 1080 × 1920 canvas. The contrast numbers are computed from the canonical
palette with the WCAG 2.x formula. The colour-blind distances are CIE76 ΔE after the
Machado 2009 simulation at full severity. `palette_check.py` (qa.md §5) reproduces every
number in §2 and §4.

## 1. Spacing and type

**Spacing scale**: nothing else is allowed. A value off the scale is a review return.

| Token | px | Use |
|---|---|---|
| s1 | 4 | icon to its own tag; the pressed-state offset |
| s2 | 8 | items inside one group; chips in the resource strip |
| s3 | 12 | padding inside rows; between tracker chips |
| s4 | 16 | minimum gap between two tap targets; HUD edge inset |
| s5 | 24 | panel gutter (content to the panel edge); between groups |
| s6 | 32 | between sections of one panel; the last row to the footer |
| s7 | 48 | section break; the isolation of a buy button (16 dp) |
| s8 | 64 | around hero art; above the footer on full screens |

**Type scale** (ratio ≈ 1.2):

| Token | px | Weight | Line height | Use | Never |
|---|---|---|---|---|---|
| digits | 32 | bold, tabular | 1.15 | badges, tags, timers on chips, counts | sentences |
| caption | 36 | regular | 1.3 | secondary lines, meta, the ticker, the next-goal line | the only line of a card |
| body | 42 | regular | 1.3 | default text, list primary lines, toasts | — |
| label | 50 | semi-bold | 1.2 | buttons, tab labels in full screens, list titles | paragraphs |
| title | 60 | bold | 1.15 | sheet and modal titles | more than 1 line |
| screen | 72 | bold | 1.1 | full-screen titles, report headlines | inside rows |
| display | 96 | display face | 1.0 | ceremony numbers, "Victory", the tier numeral | running text |

1. **Two families**: a display face for sizes ≥ 60 px only, and a text face for everything
   else. The text face has an x-height ≥ 0.47 em and covers every shipped language
   (l10n-forge chooses it; OFL licence). The display face never sets a sentence.
2. **Tabular figures** (OpenType `tnum`, set on the FontVariation) for every number that
   changes: timers, counts and resources never jitter sideways.
3. **≤ 3 sizes per surface**, plus the digits token.
4. **All caps** only for ≤ 3 words, with letter spacing +4%.
5. **Line length** 28–60 characters. A full-width panel body (1032 px at 42 px) holds about
   45 characters. Paragraphs ≤ 3 lines, except on the Herald's Board and in help pages.
6. **Text-size setting** 100 / 115 / 130% scales every Theme font size, minimums included.
   Layouts must pass `layout_audit` at 130%.

## 2. Colour tokens and measured contrast

| Token | Hex | Role |
|---|---|---|
| PARCHMENT | #E8D9B5 | content ground; light text on dark chrome |
| INK | #1E1712 | text, contour, scrims |
| OAK | #4A2E1B | frames, bars, secondary buttons |
| IRON | #3B4048 | neutral, info, Premium frame |
| GILT / GILT_LIT | #C9A04C / #E0BC6A | primary buttons, focus ring, selected, idle outline, progress fill |
| WAX | #8A1F24 | danger, badges, shortfall numbers |

Contrast ratio of text or foreground (row) on background (column):

| fg \ bg | PARCHMENT | OAK | INK | IRON | WAX | GILT |
|---|---|---|---|---|---|---|
| INK | **12.66** | 1.43 | — | 1.70 | 1.94 | **7.26** |
| OAK | **8.85** | — | 1.43 | 1.19 | 1.36 | **5.07** |
| WAX | **6.53** | 1.36 | 1.94 | 1.14 | — | 3.74 |
| IRON | **7.46** | 1.19 | 1.70 | — | 1.14 | 4.28 |
| PARCHMENT | — | **8.85** | **12.66** | **7.46** | **6.53** | 1.74 |
| GILT | 1.74 | **5.07** | **7.26** | 4.28 | 3.74 | — |
| GILT_LIT | 1.30 | **6.82** | **9.75** | **5.75** | **5.03** | 1.34 |

Bold = passes 4.5:1 for body text. 3.0–4.5 = large text (≥ 64 px, or ≥ 50 px bold) and
non-text only.

1. **Forbidden as text**: GILT or GILT_LIT on PARCHMENT (1.74 / 1.30); any troop line
   accent on PARCHMENT (1.63–3.97); IRON on OAK (1.19); WAX on OAK, INK or IRON (≤ 1.94).
2. **Semantic colours**: positive = GILT + a seal icon + the word; negative = WAX + a broken
   seal + the word; neutral = IRON. **No green/red pair anywhere**: the archers' green and
   the infantry red are troop accents, not states.
3. **Line accents** are bands, fills and icon tints with an INK contour. They are never text.
4. **Scrims** (sRGB blending, as Godot 2D blends): PARCHMENT text reaches 4.5:1 over PURE
   WHITE with an INK scrim of ≥ 69%, and 3:1 at ≥ 57%. Rule: **70%** behind body text over
   the world or over art, 60% behind large text only.
5. **Muted text** = INK at ≥ 70% opacity on PARCHMENT (5.55:1). 60% gives 4.12:1 and fails.
6. **Text over the world without a scrim** (resource values, timers over the map) carries an
   INK outline of `max(3, round(0.10 × size))` px (LabelSettings `outline_size`) plus a
   2 px shadow.
7. **Disabled fill** = PARCHMENT mixed 35% toward OAK (#B19D7F). The INK label keeps 6.74:1,
   because a disabled control shows its reason and that reason must stay readable.

## 3. The painted chrome

Chrome is built from real crafted materials: an oak board with a moulded edge (bars, frames),
a parchment sheet with a deckled edge (content grounds), gilt metal (primary buttons, corner
fittings), iron straps and rivets (Premium, secondary structure) and wax (danger, badges).
The ornaments and trims are Blender renders ([icons.md](icons.md) §6). Painted grounds come
from the `panels` group (game-art-director). Both follow these numbers.

| Piece | Source (1×) | Patch margins l/t/r/b | Content margins | Axis stretch | Min display |
|---|---|---|---|---|---|
| Full-screen panel (oak frame, parchment centre) | 256 × 256 | 40 | 64 (40 + s5) | TILE_FIT (carved edge) | 400 × 400 |
| Sheet top edge + grabber | 512 × 96 | 48 / 32 / 48 / 0 | 24 | TILE_FIT | full width |
| Button L | 192 × 144 | 36 / 28 / 36 / 28 | 40 / 24 | STRETCH | 320 × 144 |
| Button M | 160 × 120 | 30 / 24 / 30 / 24 | 40 / 20 | STRETCH | 240 × 120 |
| Button S / chip | 132 × 132 | 24 | 16 | STRETCH | 96 × 96 |
| Card frame | 160 × 200 | 24 | 24 + s2 | TILE_FIT for stud rows | 128 × 160 |
| Tag | 88 × 40 | 12 / 8 / 12 / 8 | 12 / 4 | STRETCH | 56 × 40 |
| Tooltip / toast | 256 × 96 | 24 | 24 / 16 | STRETCH | 320 × 96 |

1. **Ship at 1×.** `StyleBoxTexture` draws its margins at texel size and has no scale
   property, so the texture's patch margins ARE the on-screen border at 1080 wide.
2. **Patch margin ≤ 1/3 of the smallest display size.** The UI-002 lesson: a 58 px border
   swallowed a 60 px button (qa.md §7).
3. **No detail thinner than 3 px at 1×.** Tablets draw the chrome 1.33× larger and 720-wide
   phones 0.67× smaller: a 2 px gilt line blurs on the first and shimmers on the second.
4. **Repeating edges** (rope, rivet rows, carved beads) use `AXIS_STRETCH_MODE_TILE_FIT`, so
   a repeat is never stretched. Smooth edges use STRETCH.
5. **The centre fill varies ≤ 6% in luminance.** Text sits there, and busy parchment fibres
   eat its contrast.
6. **Chrome never out-contrasts the art.** The brightest chrome highlight is GILT_LIT, never
   white. Chrome carries no glow: glow is the language of rarity (blender-forge glow.md).
7. **One 2048² chrome atlas** holds the HUD and the common panels, so the HUD batches
   (godot.md §13).
8. `StyleBoxTexture` for Control backgrounds (theme-driven, with states); `NinePatchRect`
   only for frames drawn over content (card frames over art, portrait frames).

## 4. Colour-blind coding — measured collisions and the shape codes

| Pair | Full colour vision ΔE | Protan | Deutan | Tritan | Verdict |
|---|---|---|---|---|---|
| spearmen #8B8F95 / crossbows #6D8AA8 | **15.9** | **14.5** | **17.0** | **16.1** | collide for everyone |
| infantry #B4432E / archers #4F7A4A | 71.4 | **10.6** | 20.5 | 83.3 | collide for protans |
| archers / crossbows | 47.5 | 44.7 | 41.3 | **12.4** | collide for tritans |
| Sound #6A8FD8 / Fine #8F6ADB (rarity rims) | 34.3 | **17.7** | **10.8** | 30.7 | collide for protans and deutans |
| GILT / Masterwork rim #E8A33C | **16.8** | **12.2** | **13.3** | **15.9** | chrome gilt is not a rarity signal |
| GILT / cavalry #C9A76A | **12.7** | **13.8** | **12.2** | **5.8** | the cavalry band vanishes next to gilt chrome |
| WAX / infantry | **17.6** | **18.6** | **17.5** | **14.0** | a dot needs its PARCHMENT ring on infantry fills |

A pair with ΔE < 20 counts as colliding at icon size. The shape codes:

| Meaning | Shape / count / word (primary) | Colour (secondary) |
|---|---|---|
| Troop line | silhouette icon: shield and sword · spearhead · bow · crossbow · horse head | the line accent band |
| Rarity | frame studs: Issued 0 · Sound 1 · Fine 2 · Masterwork 4 + a gilt crest; the tier word on detail views | the forge.TIERS rim colour on an INK card back (4.43–12.98:1); never on PARCHMENT (1.03–2.86) |
| Idle plate | outline + the word "Idle" | GILT_LIT |
| Shortfall | the need number + "−7.6K" + a "Get" link | WAX |
| Success / failure | seal / broken seal + the word | GILT / WAX |
| Relationship (self, ally, enemy, neutral) | marker shapes (world-forge, game-art-director readability.md) | reserved colours, never in chrome |

## 5. Buttons

| Variant | Material | Label | Contrast | Use | Per surface |
|---|---|---|---|---|---|
| Primary | bevelled gilt plate | INK | 7.26:1 | THE main action | ≤ 1 |
| Secondary | oak plank | PARCHMENT | 8.85:1 | alternatives | ≤ 3 |
| Quiet | parchment tag with an oak edge | OAK | 8.85:1 | row actions, batch tabs, "Get" | any |
| Danger | wax-red leather | PARCHMENT | 6.53:1 | dismiss, leave, recall, break the peace ward | ≤ 1; never in the primary slot |
| Premium | iron frame with gilt rivets; gem icon + number | PARCHMENT on IRON | 7.46:1 | any gem spend | ≤ 1; never the default focus |
| Icon | object art on a round parchment medallion | — | icon edge ≥ 3:1 | HUD and toolbars | — |

Sizes: **L 144** high (min width 320), **M 120** (min 240), **S 96** inside a 132 hit rect.
Label padding ≥ 40 px per side. Button icon 72 / 56 / 48 px, then s3 before the label.

| State | Visual | Behaviour |
|---|---|---|
| Rest | normal texture | — |
| Pressed | pressed texture (12% darker, 4 px inner shadow), content 4 px down, scale 0.96 in 50 ms | shown on touch-down, the same frame |
| Focus | 4 px GILT_LIT ring + a 2 px INK outer edge, outside the frame (its own StyleBox); texture unchanged. The INK edge carries 12.66:1 on parchment, where GILT_LIT alone is 1.30:1 | keyboard, gamepad, screen reader |
| Disabled | 35% OAK fill mix, icon desaturated 60%, INK label | still takes taps: a tap shows the reason toast |
| Locked | padlock art 48 px + the requirement ("Keep tier 5") | a tap opens the requirement's route |
| Busy | a turning hourglass (48 px) replaces the icon; the label stays | ignores taps until the server answers; 15 s → error state |
| Selected | raised parchment + bold label + 6 px GILT underline with a 2 px INK edge (GILT alone is 1.74:1 on parchment) | tabs, toggles, segments |

1. **A disabled control without a visible reason is banned.** The reason sits under the
   button, or a tap shows it.
2. **Commit on release** (`ACTION_MODE_BUTTON_RELEASE`), so a finger can slide off to cancel.
3. **Two-step gem spend**: the first tap turns the Premium button into "Confirm [gem] 120" for 3 s;
   the second tap commits. Gem prices also show "≈ €x.xx" (monetization.md §9). A spend at or
   above shop-forge's large-spend threshold opens a modal instead.
4. **Footer slots**: Primary 440 × 144 on the hand side; Secondary on its inner side; the back
   control in the opposite corner. Danger is ≥ 48 px from Primary or on another row.
5. **Real-money Buy**: the same height as Close; Close visible from the first frame and
   labelled "Close"; ≥ 48 px from frequent controls; never where Claim or Help all sit on
   other screens. The store's own sheet is the confirm (monetization.md §9–10).
6. Pressed visual in the same frame; the tap sound ≤ 50 ms after touch-down (audio-forge);
   a 10 ms haptic on commits when haptics are on.

## 6. Tabs

- 2–5 tabs, equal widths ≥ 180 px, 112 px high, 42 px labels. Selected = the Selected state
  in §5 (raised, bold, INK-edged gilt underline). More than 5 means two screens.
- **Placement**: the strip always sits directly above the footer, on sheets and full screens
  alike (full screen: y 1576–1688, the easy zone). A strip at the top of a sheet would land at
  y ≈ 600, in the hard zone.
- No swiping between tabs: it fights the edge back gesture and every slider.
- The last tab is remembered per screen for the session; deep links open at their tab; a tab
  with a claim carries a dot.

## 7. Lists and rows

| Row | Height | Content |
|---|---|---|
| Compact | 120 | text only: 42 px line + 36 px meta |
| Standard | 144 | icon 96 · text · one action |
| Rich | 200 | art 160 · title 50 · two lines · one action |

- Padding s3 vertical, s5 horizontal. Divider 2 px OAK at 30%. Sticky section headers 72 px.
- One action per row, on the hand side: a Quiet S/M button. A tap on the rest of the row opens
  its detail. **No swipe-to-reveal actions**: hidden gestures fail the discoverability pass.
- More than 60 rows → a virtual list (godot.md §10). The server pages 50. In rankings the
  player's own row stays pinned.
- `ScrollContainer.scroll_deadzone = 24` so a scroll never becomes a tap. The last row clears
  the footer by s6.
- Filters: a chip row 96 high (hit 132), ≤ 5 chips.

## 8. Cards

| Card | Art source | Sizes | Frame and code |
|---|---|---|---|
| Item (gear, goods) | Blender card render (blender-forge; 512 source) | 256 detail · 160 grid · 128 compact | rarity frame + studs on an INK back |
| Troop | TRP painted card, 4:5 (game-art-director units.md) | 320 × 400 list · 640 × 800 muster | 12 px line band + line icon 56 |
| Lord | CMD portrait bust, 4:5 (commander-forge) | 320 × 400 roster · 720 × 900 detail | sworn = gilt rim light + gilt frame variant; role icon |
| Building | engine render (`core/build_thumbs.gd`, castle-forge) | ≥ 40% of screen height on its card | tier numeral tag |
| Offer / goods | SHP/JRN art, Blender goods | the goods ≥ 50% of the card (monetization.md §10) | no war imagery |
| Share card | chat-forge's layouts on this kit | 880 × 320 | — |

Grid columns = `floor((W − 2·24 + 16) / (card + 16))`. At W = 1080: 160 cards → 5 columns,
128 cards → 7.

## 9. Cost lines, timers, progress

- **Cost line**: icon 48 + "12.4K / 20K" at 42 px tabular. A shortfall shows the need in WAX,
  the delta "−7.6K" and a Quiet "Get" button that opens the resource sheet (free sources
  first, the shop last).
- **Time**: two units ("1 h 12 m"; "4 m 05 s" under 10 min), rounded UP, never "0 s" while
  running. Holding it shows the local end time (core-loop §4.5).
- **Bars**: 16 px in rows, 32 px in panels. GILT fill on a SOLID INK track (7.26:1). A 40%
  INK track over parchment gives the fill only 1.37:1. Warning bars use a WAX fill on a
  PARCHMENT track (6.53:1) plus the words ("Full in 2 h").
- **Rings** on chips: 6 px, same colours.
- A value change counts up over 800 ms (core-loop A1; motion.md).

## 10. Tooltips (long-press)

Hold 450 ms → the tooltip opens ≥ 96 px above the finger (below it near the top edge), max
width 640, text 36–42 px. It stays while the finger is held and hides 1.5 s after release.
**Never the only home of core information**: an "i" medallion (Icon S) opens the same text on
a plain tap.

## 11. Modals

Width 960. Title 60 px, body ≤ 3 lines at 42 px, buttons M/L in one row: the commit on the
hand side, Cancel on the other. The body names the loss in numbers ("Dismiss 1,200 Pikemen?
They do not come back."). INK scrim 60%. No tap-outside dismiss when the modal commits a spend
or a loss. At most 1 modal. At session open only for legal consent, a ban or maintenance.

## 12. Toasts

880 wide at y 316, ≤ 2 lines at 42 px, icon 72. Shown for
`clamp(1500 + 300 × words, 2500, 6000)` ms (reading speed ≈ 200 words per minute). Queue ≤ 3;
toasts of the same type merge ("+3 more"). Order: error > social > info. A tap opens the
toast's route; a swipe up dismisses it. Toasts never cover the tracker or the bottom band. A
problem that needs a decision is not a toast (states.md §3).

## 13. Badges and tags

The dot and the count pill are defined in hud.md §5. Tags: 40 px high, 32 px bold digits or a
single word, PARCHMENT on OAK or INK on PARCHMENT.

## 14. Inputs

- **Quantity picker**: slider (track 16, thumb 88 visual in a 144 hit), −/+ steppers (S),
  numeric field 42 px, and the time-first presets 1 h · 3 h · 8 h · "Until I'm back (hh:mm)"
  (core-loop A3). The result shows first: "Ends 14:20 · 1,200 Pikemen · cost".
- **Toggle**: 144 × 80, knob 64. Position is the shape code; the fill is GILT for on and IRON
  for off. The label sits on the left at 42 px.
- **Text field**: 120 high, 42 px, a clear button. The focused field stays ≥ 48 px above the
  keyboard (`DisplayServer.virtual_keyboard_get_height()`).
- **Search**: a text field + the last 5 searches.

## 15. The Theme (Godot 4)

One Theme resource (`ui/theme/cc_theme.tres`, path to confirm), set on the root Control of
every CanvasLayer, or as the project theme (`gui/theme/custom`). Default font size 42. Type
variations (`Theme.set_type_variation(name, base)`; a Control uses them through
`theme_type_variation`):

`ButtonPrimary · ButtonSecondary · ButtonQuiet · ButtonDanger · ButtonPremium · ButtonIcon ·
ButtonTab · PanelSheet · PanelFull · PanelCard · PanelTooltip · PanelToast · PanelModal ·
LabelDigits · LabelCaption · LabelBody · LabelTitle · LabelScreen · LabelOnWorld (outline) ·
ChipResource · ChipTracker · TagParchment · TagOak`

Shipped scenes carry no `theme_override_*` except values computed at runtime (safe-area
margins, fit-down sizes). A grep of `.tscn` files for `theme_override_` is part of qa.md §2.

## 16. Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| Gilt text on parchment "for the medieval look" | 1.74:1, unreadable in sunlight | [ ] `shot_contrast.py` |
| A per-node StyleBox override | the next Theme change misses this screen | [ ] `.tscn` grep |
| A nine-slice margin > 1/3 of the display size | frame swallows the content (UI-002) | [ ] `layout_audit` min-size check |
| Rarity by colour only | deuteranopes cannot tell Sound from Fine | [ ] colour-blind screenshot pass |
| A disabled button with no reason | "the button is broken" | [ ] `ux_flow_probe` taps every disabled control and expects a reason |
| A Premium button in the primary slot or focused by default | accidental spends | [ ] focus audit; footer rule |
| Swipe-to-reveal row actions | nobody finds them | [ ] review |
| A toast that asks for a decision | missed choices | [ ] review; states.md |

- [ ] Only scale spacing; ≤ 3 type sizes + digits; tabular figures on changing numbers.
- [ ] Every text pair in the bold cells of §2; scrims ≥ 70%; no gilt text on parchment.
- [ ] Every coded meaning has its shape, count or word (§4).
- [ ] Buttons: one Primary, Danger isolated, Premium two-step, disabled shows its reason.
- [ ] Chrome at 1×, margins ≤ 1/3, no line under 3 px, chrome in one atlas.
- [ ] Theme variations only; no `theme_override_` in shipped scenes.
