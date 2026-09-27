# HUD — the frame around the painted world

The HUD at rest over the castle and the realm, in design px on the 1080 × 1920 canvas. The
zone percentages, the thumb-zone principle, the red-dot budget and the rail cap are
design-forge `references/ux.md`, core-loop §9 A7 and liveops §6.2. When ux.md sets a
different number, ux.md wins and this table is re-derived. **Every rect is a PROPOSAL** until
it is compared with the shipped HUD scene (path to confirm) on a screenshot.

## 1. Canvas, safe area, shapes

1. **Coordinates** are design px on 1080 × 1920. Top zones are measured from the top of the
   safe area and bottom zones from its bottom. On a taller phone the extra height goes to the
   clear world window (§3), never to bigger chrome.
2. **Safe area**: the SafeArea container (godot.md §3) applies
   `DisplayServer.get_display_safe_area()`, converted to design px, as margins. Typical
   insets at 1080 wide: top 80–150 px (notch, punch hole), bottom 48–66 px (gesture bar).
   Rounded corners (radius ≈ 40–110 px) cut the four corners: no tap target has its centre
   within 120 px of a screen corner.
3. **Shapes the HUD must pass** (the `w1f_aspect_sweep` 6 shapes are read from the harness;
   if they differ, add the missing ones to this list and ask qa-forge):

| Shape | Example device class | Viewport in design px (expand) | What breaks first |
|---|---|---|---|
| 9:16 | 1080×1920 reference | 1080 × 1920 | nothing: the plan below |
| 9:19.5 | modern phone 1080×2340 | 1080 × 2340 | a wide empty band if zones anchor to the centre |
| 9:20 / 9:21 | tall phone 1080×2400 / 1080×2520 | 1080 × 2400–2520 | the tracker drifts away from the thumb if anchored to the top |
| 3:4 | tablet 1536×2048 | 1440 × 1920 (at scale 1.0) | the bottom bar stretches; sheets become too wide |
| 10:16 | tablet 1600×2560 | 1200 × 1920 | as 3:4, milder |
| ~5:6 | foldable inner screen | ≈ 1600 × 1920 | as 3:4, plus the hinge crease at x ≈ 50% |

## 2. Thumb zones (right hand; the Hand setting mirrors every rect)

A PROPOSAL from general thumb-reach studies for 6.1–6.7-inch phones held in one hand
[observational]. ux.md owns the principle. Verify it with ≥ 5 testers on two phone sizes:
tap misses per zone must be ≤ 2%.

| Zone | Rect on 1080 × 1920 | May hold |
|---|---|---|
| **Easy** | y ≥ 1150, except the two 120 × 120 bottom corners | actions used ≥ 3 times per check-in; primaries; confirms |
| **Stretch** | 700 ≤ y < 1150, plus the bottom corners | actions used 1–2 times per check-in; drawers; tabs of sheets |
| **Hard** | y < 700 | read-only status; entries used once a day or less (mail, profile, events, offer slot) |

Tall phones: easy zone = the bottom 40% of the viewport height; hard zone = the top 36%.

## 3. The HUD plan at rest (castle, right hand)

| Id | Element | Visual rect (x, y, w × h) | Hit rect | Zone | Use per check-in |
|---|---|---|---|---|---|
| H1 | Resource strip: 6 chips (food, wood, stone, iron, gold, gems — the shipped order wins) | x 12 + i·177, y 8, 169 × 88 | 169 × 132 (reaches 44 px down) | hard | read; tap rarely |
| H2 | Profile badge: crest (SGL) + keep tier numeral | x 16, y 148, 144 × 144 | same | hard | rare |
| H3 | Power line (42 px) + realm line (36 px) | x 176, y 156, 480 × 104 | part of H2 | hard | read |
| H4 | Mail (mail-forge) | x 920, y 148, 144 × 144, icon 96 | same | hard | 1–3 per day |
| H4b | Offer slot, ≤ 1 icon (monetization.md §10) | x 944, y 316, 120 × 120 | 132 × 132 | hard | — |
| H5 | Event rail: Herald's Board head + ≤ 4 events (liveops C2) | x 16, y 316 + i·136, 120 × 120 | 144 × 136 | hard/stretch | 1 per day |
| H6 | Tracker: 5 group chips (infirmary, research, muster, build, banners, top → bottom) | x 932, y 548 + i·144, 132 × 132 | 144 × 144 (reaches 12 px inward) | stretch/easy | 1 each |
| H6h | Tracker head, contextual: "Finish all free (n)" while it applies; the line "All busy — first free 14:20" for 4 s after the last plate starts | x 664, y 1272, 400 × 132 | same | easy | 1 |
| H7 | Help all + count (only while ≥ 1 request) | x 920, y 1420, 144 × 144 | same | easy | 1–3 |
| H8 | Next-goal card: icon 96 + one line + progress | x 16, y 1432, 540 × 120 | 540 × 132 | easy | 1–2 |
| H9 | Chat ticker, one line 36 px (chat-forge ui.md §1 proposes the strip) | x 24, y 1576, 1032 × 84 | 1032 × 132 (y 1570–1702) | easy | read; tap 1–5 |
| H10 | Bottom bar, 5 slots: Lords · Alliance · WORLD SEAL · Chronicle · More | y 1744, 5 × 216 × 176; seal Ø 176 raised to y 1712 | 216 × 176 | easy | many |

- **Clear world window**: x 152–916, y 316–1416 = 764 × 1100 = **40.5% of the screen**, with
  no persistent chrome in it. Contextual chrome may enter it: status bubbles, batch tabs
  (§6), toasts, the digest. At most 3 such pieces at once.
- **Coverage**: opaque plus scrim pixels at rest, with every contextual element shown,
  come to ≈ 35% of the screen on this plan (layout_audit rect union). Budget ≤ 36%
  (PROPOSAL; ux.md may set it).
- **Gaps**: every neighbouring pair of visual rects above is ≥ 16 px apart, and no two hit
  rects overlap. `ux_touch_probe` checks both on every shape.
- **Labels on the bottom bar**: icon 96 px + a 36 px label under it. The seal has no label;
  its art shows the destination (architecture.md §1.3).

## 4. Castle vs realm

| Element | Castle | Realm (region and realm zoom) |
|---|---|---|
| H1–H4b, H9, H10 | shown | shown; the seal shows the player's keep |
| H3 second line | realm name | coordinates of the camera centre (world-forge format) |
| H5 event rail | shown | shown |
| Left rail lower slot x 16, y 1016–1400 | empty (world) | realm tools: Search · Bookmarks · Home, 3 × 120 px, 12 px gaps |
| H6 tracker | all chips | all chips; marches listed first when the Banners drawer opens |
| H7 Help all, H8 next goal | shown | shown |
| Status bubbles (§7) | castle close and overview | hidden |
| Tile sheet | — | 40% sheet on a tile tap (screens.md S14) |

The switch happens at B2 on `level_changed`, as a 150 ms crossfade on the frame of the town
swap (architecture.md §1). Elements that exist in both modes never move. Only the ones that
differ cross-fade.

## 5. Red dots and marks — the budget

**Marks** are how the HUD says "something is waiting for you". There are two kinds: the red
dot and the tracker's Idle tag (core-loop §2 rule 2: gilt outline + the word "Idle"). Both
count toward the budget.

| Priority | Source | Mark | Clears when | Expires |
|---|---|---|---|---|
| P1 | a claim that ends in < 24 h; a war call the player pledged to | dot | claimed / answered | at the claim's end (daily chests auto-claim at reset, core-loop §7.4; event rewards go to mail, liveops R7) |
| P2 | a claimable reward: chest, attachment, milestone, gift | dot | claimed | never, until claimed |
| P3 | addressed to the player: @mention, personal mail, application (officers) | dot or count | viewed | 72 h unviewed |
| P4 | an idle plate | Idle tag on its chip | the plate starts | never |

- **Budget**: ≤ 3 marks visible at session open for the median player's save (core-loop
  A7); ≤ 1 event badge at a time (liveops C8). The runtime cap is 5 root marks: past that,
  lower priorities are HELD (never lost) and appear as higher ones clear. `ux_flow_probe`
  counts marks on the session-open screenshot of the median save.
- **Never marked**: offers, the shop, "new" or "started" events, news, rank changes, new bag
  items that cannot be claimed, unread system mail without an attachment (mail-forge rule).
- **Aggregation**: a leaf key (`alliance/gifts`) raises a dot on its root entry (Alliance in
  H10). A root shows a number only for counted things (mail, mentions), capped at "99+".
- **Visual**: dot = WAX #8A1F24 disc 24 px + PARCHMENT ring 4 px = 32 px, at the entry's
  top-right corner (top-left for left hand), inset 6 px. The ring keeps it visible on
  dark chrome: WAX on OAK is 1.36:1, PARCHMENT on OAK is 8.85:1. Count pill: 44 px high,
  ≥ 44 px wide, digits 32 px bold PARCHMENT on WAX (6.53:1).
- **Motion**: appears with a 200 ms scale-up (motion.md). Never loops, never pulses, never
  flashes.
- **Player control**: Settings → Notifications → "Marks for: mentions · alliance · events"
  (all on by default).

## 6. The queue and march tracker

One always-visible tracker holds every plate (core-loop §2 rule 2). An idle plate is ≤ 3 taps
from running (architecture.md §3).

**Chip (132 × 132)**: plate-type icon 72 px (Blender art, icons.md). Around the icon, a 6 px
progress ring (GILT on a solid INK track, 7.26:1) for the plate that ends soonest. At the bottom, a tag of
88 × 40 with the busy count "2/3" in 32 px bold INK on PARCHMENT. **Idle**: the frame gets a
6 px GILT_LIT outline, and the tag says "Idle" instead of the count. Not colour alone, never
flashing.

**Head (H6h)**, contextual, so the clear window stays clear: "Finish all free (3)" while
≥ 1 plate is under the free-finish threshold (core-loop §4.3). When the last idle plate
starts: the line "All busy — first free 14:20" (36 px on an INK scrim of 70%) for 4 s. The
same line closes the resume digest. Holding a chip shows its local end time.

**Batch tabs**: 216 × 132 quiet buttons attached to the inner side of their chip
(x 700–916). They are "Refill all" (muster), "Heal all" (infirmary) and "Resend all"
(banners), and they appear only while the batch applies. ≤ 3 at once. They slide out in
200 ms.

**Chip tap**: with an idle plate, go straight to that plate's action surface (the suggested
building card, the research screen). Otherwise open the **drawer**: 720 wide, anchored at the
bottom to y 1416, top ≥ 316. Header 120 px (group name + batch action). Rows 144 px: icon 96 ·
name 42 px · remaining time 42 px tabular + a 16 px bar · one action button of 200 × 112
("Speed up", "Finish free", "Start", or the state "Help asked"). A tap on the row outside the
button opens the plate's route.

**March rows** (Banners drawer): lord portrait 96 px (commander-forge), target name, state
word (Outbound · Gathering 62% · Returning · In battle), ETA. A row tap moves the camera to
the march (`realm/march/{id}`, transition-forge). The action is "Recall" (Danger variant,
two-step, components.md §5).

**Timers**: one hub Timer ticks once a second and updates only visible labels (core-loop
§4.6; godot.md §7). Remaining time = `end_unix − now`, where now = the device clock
+ server offset.

## 7. Status bubbles over buildings

| Priority | Bubble | Building | Tap does |
|---|---|---|---|
| 0 | Threat: "Attack 2:40", or readiness "Defence 3/4" (battle-forge defence.md §2, §4) | the fortress | opens the Defence panel at the first failing check |
| 1 | Finish free (hourglass art) | any building with a plate under the threshold | finishes (1 tap) |
| 2 | Idle (plate icon + "Idle" tag) | an idle muster yard or scriptorium desk | opens its action surface |
| 3 | Wounded waiting (bed count tag) | infirmary | opens the infirmary |
| 4 | Claim (chest or gift art) | the building holding the claim | claims (1 tap) + toast |
| 5 | Suggested upgrade (max 1 bubble) | only the next-goal building, only when affordable and a crew is idle | opens its card |

- **Anchor**: an empty named `ui_bubble` at the roof peak (castle-forge to add it to the kit;
  fallback: the top centre of the building's AABB + 0.5 m). Screen position =
  `Camera3D.unproject_position()`, rounded to whole px, updated only when the camera moves
  (godot.md §8).
- **Size**: a parchment medallion Ø 104 with a 6 px gilt rim, icon 64 px, hit 144. Its bottom
  sits 24 px above the anchor point.
- **Caps**: ≤ 5 visible at castle overview (P0–P3 only), ≤ 8 at castle close. Two bubbles
  whose centres are < 120 px apart merge: the higher priority shows, with a "+1" pip (32 px).
  P0 is never merged away, and it shows only while a check fails or a threat exists.
- **Zoom**: shown at C1 and C2, hidden at R and M; fade in 150 ms, out 120 ms on
  `level_changed` (transition-forge zoom-model.md §6).
- **Motion**: appear = scale 0.6 → 1 + fade in 180 ms. Resolve = shrink in 120 ms, then
  feel-forge's result float. **No idle bobbing**: a loop on 8 bubbles is constant motion in
  the corner of the eye, and a draw cost every frame.
- **Layering**: bubbles live on the world-UI layer, below the HUD. A bubble whose rect
  touches a HUD zone is hidden, not drawn over the chrome.

## 8. Event rail and the Herald's Board

- **Head**: the Herald's Board (a notice board with pinned sheets, Blender art). One tap
  opens the Board: 21 days ahead (liveops §6.1).
- **Icons**: ≤ 4 (liveops C2). Season first, then events by end time. Each icon has a
  remaining-time tag ("2 d", "5 h"; 32 px; days and hours, never seconds) and a 6 px
  milestone ring.
- **Dot**: only for a claimable milestone, and only one event dot at a time (C8).
- **Never on the rail**: offers (C2); paid-only or gacha events (liveops §4); "new" markers.
- **Overflow**: C1 caps concurrent scoring events at 3, so the rail never overflows. If data
  breaks the cap, the rail shows 4 and the Board's head shows "+n", and `ux_flow_probe`
  reports the breach.
- **Onboarding**: the chapter and the realm's founding event share ONE icon
  (onboarding.md §10).

## 9. Ticker, next goal, digest, Help all

- **Chat ticker (H9)**: the last line of the selected channel (chat-forge ui.md §1 owns the
  source and cadence rules). Sender in bold, 36 px, one line, cut with an ellipsis. Rally calls
  and system lines start with their icon. Mentions show a count pill at its end. Hidden while
  a full screen, a battle presentation or a ceremony is on screen. Settings can turn it off.
- **Next-goal card (H8)**: one goal (data from gameplay-forge / story-forge): icon 96, one
  line ≤ 40 characters in English at 36 px, then progress ("2/3") or time. A tap opens its
  route. The card stays stable until the goal is done; then a 1.5 s seal (feel-forge) and the
  next goal.
- **Digest on resume** (core-loop §8.1): ≤ 3 lines of 42 px on an INK scrim of 70%,
  880 wide, at y 316. It hides after 2.5 s or on the first tap, whichever comes first.
- **Threat banner** (battle-forge defence.md §2, the "Near" band, ETA ≤ 60 s): 764 × ≤ 130
  at the top of the clear window (x 152, y 316): the countdown and **Call allies · Recall
  marches · Defence** (3 buttons, 132 px hits). The offline band and toasts move below it. It
  is a war surface: no offer or gem button appears while it shows (monetization.md §10).
  Hostile marches also appear as WAX-edged rows at the top of the Banners drawer.
- **Help all (H7)**: art of two clasped gauntlets (Blender), with the request count pill. It
  appears only while a request exists. A tap sends ONE append to the help log (core-loop §6).
  Toast: "Helped 7 allies — −1 h 12 m in total".

## 10. One hand, two hands, tablets

1. **Hand setting** (Settings → Controls → Hand: Right / Left). Left mirrors every rect in §3
   around x = 540: tracker and Help all move to the left edge; event rail and offer slot
   move to the right; footers mirror (primary bottom-left, back bottom-right). **Mirror by
   swapping anchors and offsets, never with `layout_direction = RTL`**: RTL also flips the
   text direction of inherited labels, and English punctuation jumps to the wrong end.
2. **Tablets** (shortest side ≥ 600 dp): set `get_window().content_scale_factor` so that a
   144 px target measures 10–12 mm. Physical size: `mm = px × s ÷ dpi × 25.4`, where
   `s` = window px per design px. Example: a 1536 × 2048 tablet at 264 dpi has s = 1.067 at
   factor 1.0, so 144 px = 14.8 mm (too big). Factor 0.8 gives s = 0.853 → 11.8 mm, and a
   viewport of 1800 × 2400.
3. **Wide viewports** (≥ 1400 design px): the HUD stays anchored to the edges; the bottom bar
   keeps 216 px slots, centred; sheets have a max width of 1080, centred; full screens with
   lists use two panes (list 40% | detail 60%).
4. **Foldables**: no text or tap target within 48 px of the hinge line when the device reports
   one (`DisplayServer.get_display_cutouts()` covers notches; hinge support: verify on the
   shipped Godot build).

## 11. Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| Zones anchored to the centre on a 9:20 phone | a band of dead space; the tracker out of reach | [ ] `w1f_aspect_sweep` + the thumb-zone overlay screenshot |
| Safe area ignored | chips under the notch; the bar under the gesture line | [ ] sweep with fake insets (godot.md §3) |
| > 3 marks at open for the median save | red-dot fatigue | [ ] `ux_flow_probe` session-open count |
| A bubble drawn over the HUD, or bubbles bobbing | clutter; GPU cost at rest | [ ] `layout_audit` overlap list; profiler draw calls at rest |
| An offer on the rail, or the offer slot in the easy zone | money-law breach; mis-taps into the shop | [ ] `ux_flow_probe` rail scan; `ux_touch_probe` rect check |
| Mirroring done with RTL | "Help all!" reads "!Help all" | [ ] Hand = left screenshot review |
| Tablet targets at 15 mm | a giant HUD that hides the art | [ ] physical-size line from `ux_touch_probe` |
| A timer label ticking in `_process` | CPU time at rest; battery | [ ] profiler: the timer hub is the only 1 Hz source |

- [ ] Every rect in §3 checked on a screenshot at all 6 shapes; clear window ≥ 40%; coverage ≤ 36%.
- [ ] No hit-rect overlap; every visual gap ≥ 16 px; no target centre within 120 px of a corner.
- [ ] Marks: sources limited to §5, budget measured, dots have the PARCHMENT ring.
- [ ] Tracker: idle is outline + word; batch tabs only while they apply; the head in the easy zone.
- [ ] Bubbles: ≤ 5 / ≤ 8, merge at 120 px, hidden at region zoom, no loop.
- [ ] Rail ≤ 4, season first, no offer, ≤ 1 event dot.
- [ ] Hand = left mirrored by anchors; tablet factor gives 10–12 mm.
