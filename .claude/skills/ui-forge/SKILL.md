---
name: ui-forge
description: Builds the menus, HUD and every screen of Castle Conquest in Godot 4. Covers the navigation map for the one castle-realm space, the 1080×1920 portrait HUD with thumb zones, and the painted chrome kit (Theme, StyleBoxTexture/NinePatchRect frames, buttons, tabs, lists, cards, modals, toasts). Also the type, spacing and contrast rules, Blender-made UI icons, status bubbles, the red-dot budget, the queue and march tracker, the event rail, panel motion, empty/loading/error states, one-hand, tablet and aspect sweep, accessibility, localization and UI performance, all proven by the layout and UX harnesses. Use for "build or fix the X screen", "HUD", "menu", "button", "icon", "the UI is cluttered", "too many red dots", "one-hand", "tablet layout". Not for camera moves (transition-forge), chat, mail or report content (chat-forge, mail-forge, report-forge), system design (design-forge) or painted art prompts (game-art-director).
---

# ui-forge — every core action one thumb away, the art never buried

The painted world is the product. The UI is the frame around it. It must never hide
the art, never make the player hunt for an action, and never talk about money
where the player expects a war. This skill turns design-forge's UX principles
(`design-forge/references/ux.md`) and each system's SYSTEM.md §9 into Godot 4
scenes. Every rule has a number, and a harness checks every number.

**Every value here is a PROPOSAL unless it quotes a canonical fact.** The owner's
repo (D:/CastleConquest) is not in this folder. Check the shipped Theme, scenes
and `project.godot` first (paths to confirm). When a shipped value differs, the
shipped value wins until the owner decides, and this skill records the difference.

## The reference frame (every rule uses these numbers)

| Quantity | Value | Why |
|---|---|---|
| Design canvas | **1080 × 1920 px portrait** (1 design px = 1 px on a 1080-wide phone) | the brief's frame; `session_audit` runs at 1080×1900, so a layout must pass both |
| Stretch | `display/window/stretch/mode = canvas_items`, `aspect = expand` (verify in `project.godot`) | tall phones add height, tablets add width, nothing is letterboxed |
| Design px per dp | 2.5–3.0 on phones 360–430 dp wide | 48 dp ≈ 126–144 px |
| Touch target (hit rect) | **≥ 132 px and ≥ 7.6 mm on the device**; primary/frequent **144 px** | 48 dp on a 360 dp phone = 144 px; 7.6 mm = 48 dp |
| Visual control height | L 144 · M 120 · S 96 (S only inside a ≥ 132 hit rect) | components.md §5 |
| Text | 32 px digits/badges only · 36 px any sentence · **42 px body** · 50 labels · 60 titles · 72 screen · 96 display | components.md §1 |
| Spacing scale | **4 / 8 / 12 / 16 / 24 / 32 / 48 / 64** px, nothing else | components.md §1 |
| Contrast | body ≥ 4.5:1 · large text (≥ 64 px, or ≥ 50 px bold) and icons/controls ≥ 3:1 | WCAG 2.x 1.4.3 / 1.4.11 |
| Clear world window | ≥ 40% of the screen has no persistent chrome (x 152–916, y 316–1416) | hud.md §3 |
| Motion | sheet 240 ms open / 180 ms close; nothing blocks input; reduced-motion honoured | motion.md |

## Hard rules

1. **The binding rulings are UI rules too.** Painted identity: chrome is oak,
   parchment, gilt, iron and wax as real crafted material, never flat vector panels.
   Live realm: the app resumes straight into the castle or realm; no title menu, no
   "Play" button, and back at HUD rest never opens a menu. ART SHOWN BIG: each
   screen's hero art covers ≥ 30% of the screen area, and the building card's
   next-tier render is ≥ 40% of the screen height (core-loop §8.2).
2. **Icons and chrome ornaments are Blender-made art.** The owner's order
   (2026-09-26): *"the icons need to be art ... not white and black ... hight
   quality art made with blender"*. They are built through blender-forge with
   [references/icons.md](references/icons.md). Never white, monochrome, line or
   pixel glyphs. Never words baked into art.
3. **One continuous space.** Castle ⇄ realm is one camera move (transition-forge,
   ≤ 700 ms), and the HUD changes in place during it. No scene change, no loading
   screen, no second HUD.
4. **≤ 3 taps** from HUD rest to commit any core action
   ([architecture.md](references/architecture.md) §3). Every screen is ≤ 3 taps
   deep. Count taps from the route table and `ux_flow_probe`; never estimate them.
5. **Touch.** Hit rects ≥ 132 px and ≥ 7.6 mm; 144 px for primary and frequent
   actions. Hit rects never overlap. Visual targets are ≥ 16 px apart. A buy
   button is ≥ 48 px (16 dp) from any frequently tapped control, and never sits
   where Claim or Help all sit on other screens (monetization.md §9). No
   horizontal gesture starts within 72 px of the left or right edge (the system
   back gesture).
6. **Thumb zones.** An action used ≥ 3 times per check-in sits in the easy zone
   (y ≥ 1150, right hand by default; the Hand setting mirrors it). The top 700 px
   holds read-only information and entries used once a day or less
   ([hud.md](references/hud.md) §2).
7. **Text.** 32 px is the minimum and only for digits, badges and timers; 36 px for
   any sentence; 42 px body. **GILT is never a text colour on PARCHMENT (1.74:1)**.
   Muted text is INK at ≥ 70% opacity (5.55:1); 60% fails (4.12:1). Text over the
   world or over painted art sits on an INK scrim of ≥ 70%, or carries an INK
   outline (components.md §2).
8. **Never colour alone.** Every coded meaning also carries a shape, a count or a
   word: troop line, rarity, idle, shortfall, relationship, success and failure.
   Measured collisions: Sound vs Fine rarity ΔE 10.8 for deuteranopes, spearmen vs
   crossbows ΔE 15.9 even for full colour vision, infantry vs archers ΔE 10.6 for
   protanopes (components.md §4). Relationship colours are a reserved channel
   (game-art-director readability.md, design-forge ux.md) and never appear in chrome.
9. **The money-law on screen** (monetization.md §5, §10). The gems chip is the
   persistent shop entry, plus at most 1 offer icon on the HUD. That icon is never
   on the event rail and never in the easy thumb zone. No war imagery on or behind
   a control that spends money or gems. No buy button, gem button or offer on a war
   screen. Gem spends use the Premium button with a two-step confirm. Pop-ups follow
   the pop-up rules: ≤ 1/day, none in the first 60 s or within 30 min of a defeat.
   No red dot, rail slot, bubble or pulsing countdown on an offer.
10. **Red dots only for something claimable, idle or addressed to the player.**
    ≤ 3 visible at session open for the median player (core-loop A7); ≤ 1 event
    badge at a time (liveops C8). Dots auto-expire. Never on offers, news or "new
    event" ([hud.md](references/hud.md) §5).
11. **Every list and data screen ships all of its states**: loading, empty, error,
    offline, and locked where a gate applies. Each state has art, one line and one
    action. Never a blank panel. Never a raw error code on its own
    ([states.md](references/states.md)).
12. **Motion never blocks input.** Every tween can be interrupted. Durations come
    from [motion.md](references/motion.md). The reduced-motion setting is honoured.
    Nothing flashes more than 3 times per second.
13. **Kit only.** Every screen uses the project Theme, its type variations, the
    spacing scale and the type scale. A new look becomes a new Theme variation in
    the kit ([components.md](references/components.md) §15), never a per-node
    StyleBox override.
14. **Localisation-proof.** No text in art. Every string is a key (l10n-forge).
    Layouts pass Godot pseudolocalization at `expansion_ratio 0.4` with 0 overflows.
    A short label must hold +100%: first by width, then by fitting the font down
    to the minimum size, then on 2 lines ([godot.md](references/godot.md) §9).
15. **Nothing is done without evidence**: screenshots at the 6 aspect shapes,
    harness verdicts pasted word for word, tap counts and draw calls measured
    ([qa.md](references/qa.md)).

## The workflow (every UI task)

1. **Frame.** Write down the one question the screen answers ("Is anything ready?",
   "What does the next tier look like and cost?"). A new system with no reviewed
   SYSTEM.md → stop and route it to design-forge (game-director hard rule 9).
2. **Read the shipped UI first.** Read the Theme resource, the screen's scene, the
   route table and the ledger rows (paths to confirm). Take a screenshot of the
   current state at 1080×1920 before you change anything. That screenshot is the
   "before" image.
3. **Route it.** Add or confirm its route string, entry points and tap depth
   ([architecture.md](references/architecture.md) §4–5). Core actions ≤ 3 taps.
4. **Lay it out** on the 1080×1920 grid, in the HUD zones
   ([hud.md](references/hud.md)) or the screen spec
   ([screens.md](references/screens.md)). The primary action goes in the footer
   slot on the hand side. Set the size of the hero art. Check the thumb zone of
   every frequent action.
5. **Build from the kit.** Use Containers, anchors and Theme variations
   ([components.md](references/components.md), [godot.md](references/godot.md)).
   Fixed pixel positions are allowed only for the anchored HUD zones.
6. **Art.** Icons and chrome ornaments go through [icons.md](references/icons.md)
   → blender-forge, and each must pass the 44 px survival check. Painted boards and
   portraits go through game-art-director. Building renders come from
   `core/build_thumbs.gd` (castle-forge).
7. **States.** Build every state in [states.md](references/states.md), each with
   its art and l10n keys.
8. **Motion and sound.** Use the timings in [motion.md](references/motion.md). Ask
   transition-forge for camera moves, feel-forge for ceremonies and audio-forge
   for cues.
9. **Passes.** Pseudo-loc 0.4; text scale 130%; colour-blind simulation; reduced
   motion; Hand = left; a tablet shape; the offline toggle.
10. **Prove it.** Run the battery in [qa.md](references/qa.md) §1: the windowed
    suites, the core gate and the UI probes. Take screenshots at the 6 shapes. Run
    the contrast check on every text rect. Record the tap counts, draw calls and
    first-open time. Red → fix it or restore the checkpoint. Never ship red.
11. **Record and teach.** Add a ledger row (game-director). Write the numbers that
    worked into these references and new traps into [qa.md](references/qa.md)
    §7 (game-director hard rule 7).

## Who owns what around the UI

| Need | Owner | ui-forge's part |
|---|---|---|
| Why a system exists, its numbers, the UX principles (zone %, red-dot budget, notification tiers, rail cap) | design-forge (`references/ux.md`, SYSTEM.md §9) | implements them; reports numbers that do not fit on screen |
| Camera: castle ⇄ realm zoom, focus on a building, world fades behind full screens, march-out | transition-forge | panel tweens slaved to its clock ([motion.md](references/motion.md) §1) |
| Ceremonies (tier-up, victory), juice, particles | feel-forge | the panel the ceremony lands on |
| Chat panel, ticker content, safety | chat-forge | ticker slot, share-card component, route strings |
| Inbox, claim protocol, mail templates | mail-forge | shell, list component, Claim-all button states |
| Battle, scout and rally reports | report-forge | shell, the card and list kit |
| Target → march composer → rally → defence flows | battle-forge (+ siege-forge for engines) | the components and the tap budget |
| Lord data, portraits, hall figures | commander-forge | lord screens ([screens.md](references/screens.md) S5) |
| Offers, prices, store rules | shop-forge (design: monetization.md) | shop frame, Premium button, pop-up slot |
| Strings, fonts, RTL | l10n-forge | overflow-proof layouts, fit-down |
| Guided steps, first-time moments | onboarding-forge | overlay, pointer, cards (≤ 14 words), the ledger screen |
| Castle view, building anchors, build thumbnails | castle-forge | status bubbles, building card |
| Realm map, markers, march lines | world-forge | realm HUD overlay, tile sheet |
| 3D icon objects, chrome ornaments | blender-forge | the brief and the survival check ([icons.md](references/icons.md)) |
| Painted boards, event headers, portraits | game-art-director | the frame and the crop sizes |
| UI sounds, haptics | audio-forge | the cue list and when each fires |
| Probes the battery lacks | qa-forge | the spec and the verdict line ([qa.md](references/qa.md) §2) |
| Device matrix, VRAM and draw-call totals | ship-forge | the UI share of the budget |

## Reference index

| File | Holds |
|---|---|
| [references/architecture.md](references/architecture.md) | the one-space model, surface types, the core-action tap budget, the navigation map, route strings, the stack and back, entry points |
| [references/hud.md](references/hud.md) | safe areas, thumb zones, the HUD plan in px, castle vs realm HUD, the red-dot budget, the queue and march tracker, status bubbles, event rail, ticker, one-hand and tablet |
| [references/components.md](references/components.md) | spacing and type scales, colour tokens with measured contrast, painted chrome and nine-slice, colour-blind coding, buttons, tabs, lists, cards, cost lines, timers, tooltips, modals, toasts, badges, inputs, Theme variations |
| [references/screens.md](references/screens.md) | a spec per major screen: building card, research, muster, infirmary, lords, alliance, events and the Herald's Board, shop frame, bag, profile, rankings, settings, chronicle, realm overlay, guide overlay |
| [references/motion.md](references/motion.md) | the timing table (ms, frames, Godot trans/ease), who owns what, interruption, reduced motion, first-open cost |
| [references/states.md](references/states.md) | loading / empty / error / offline / stale / locked / busy, timing thresholds, optimistic rules, the empty-state catalogue for every list |
| [references/icons.md](references/icons.md) | the Blender icon and chrome-ornament lane: sizes, construction, the render recipe, the 44 px survival check (code), families, atlas and import |
| [references/godot.md](references/godot.md) | project settings, the CanvasLayer order, safe area, Theme, Containers, router and back, interruptible panels, badges, timers, bubbles, fit-down text, virtual lists, focus, pseudo-loc |
| [references/qa.md](references/qa.md) | the harness battery, new probes and verdict lines, the aspect shapes, the contrast check (code), the 14-point screen critique, the evidence contract, lessons |

## Output contract

A UI task is finished only when the reply carries all of these:

1. **Screenshots** at 1080×1920, 1080×2400 and 1536×2048 at minimum, plus every
   other shape of the sweep, saved under `art/ui_forge/<id>/` (game-director
   teams.md). Before and after images come in pairs.
2. **Harness verdicts, word for word**: the windowed suites that can be affected,
   including `ASPECT SWEEP OK - 6 shapes, 0 faults`, and the core gate.
3. **Tap counts** for every core action the change touches, measured.
4. **Draw calls and first-open time** of each changed screen on the reference
   phone profile (qa.md §4).
5. **Contrast output** of `shot_contrast.py` (qa.md §5) for the changed screens.
6. **States covered**: the list of states each changed list shows, with screenshots.
7. **Owner decisions required**, listed on their own (spend, shipped art, sacred
   constants), or the word "none".

"Looks good" is not a result.
