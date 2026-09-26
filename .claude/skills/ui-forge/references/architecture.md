# Architecture — one space, few surfaces, every action ≤ 3 taps away

How the player moves through Castle Conquest. The design principles (zone percentages, the
≤ 3-tap rule, notification tiers) are design-forge `references/ux.md`. This file is how
ui-forge builds them. Camera moves are transition-forge's. **Every number is a PROPOSAL**
until it is checked against the shipped scenes (paths to confirm).

## 1. The space model — one world, two modes, four zoom levels

The castle and the realm are ONE continuous 3D space. The player never "goes to" the map:
the camera pulls back, and the HUD changes in place. transition-forge owns the zoom model
and its thresholds with hysteresis. ui-forge maps every HUD element onto its levels.

| Zoom level (transition-forge names) | Mode | HUD elements shown (hud.md §3 ids) | Hidden |
|---|---|---|---|
| Castle close | castle | H1–H10, status bubbles (all priorities), building quick labels | realm tools |
| Castle overview | castle | H1–H10, status bubbles (priority 1–3 only, ≤ 5) | building labels |
| Region | realm | H1–H4, realm tools (left rail), tracker with banners chip, H7–H10 | bubbles, next-goal card |
| Realm | realm | same as region + search and bookmarks open by default | bubbles |

1. **The mode flips at one threshold**: the castle-overview ⇄ region boundary from
   transition-forge, with its hysteresis band. The HUD never flickers between modes while
   a pinch sits inside that band.
2. **Elements cross-fade during the middle 40% of the zoom move** (motion.md §2). A
   700 ms zoom means fading from 210 ms to 490 ms. Nothing slides in from off-screen during
   a zoom: the eye is busy with the camera.
3. **The world toggle** (the centre seal in the bottom bar, H10) shows the DESTINATION:
   realm art while in the castle, the player's keep while in the realm. One tap starts the
   transition-forge zoom. A second tap during the move reverses it from the current point.
4. **Resume** returns to the same mode, camera and zoom level. Panels that were open come
   back if the app was away ≤ 5 min; after that the player lands at HUD rest with the
   digest (hud.md §9). Modals never come back: their action is re-asked.

## 2. Surface types — when to use which

| Surface | Size (1080×1920) | World behind | Dismiss | Stacks on | Use for |
|---|---|---|---|---|---|
| HUD | zones in hud.md §3 | live, interactive | — | — | always-on status and entries |
| Status bubble | 104 px visual, 144 hit | live | resolves itself | world | one action on one building (hud.md §7) |
| Drawer | 720 × ≤ 1100, from the hand-side edge, bottom at y 1416 | live, dimmed 30% | tap outside, swipe to the edge, back | HUD | the tracker's plate lists (hud.md §6) |
| Sheet | snap heights 40% / 66% / 92% (768 / 1268 / 1766 px) | live, dimmed 40%; camera frames the subject above | drag down ≥ 25% of its height or fling ≥ 1200 px/s; tap on the dimmed world; back | HUD, drawer | a building card, a tile, a resource, a lord preview |
| Full screen | whole safe area | paused (`disable_3d`), motion.md §5 | back control (footer, hand side), system back | HUD | deep management: lords, alliance, research tree, shop, settings, rankings |
| Picker | sheet at 40% | the surface below, dimmed 40% | choose, or back | sheet, full screen | hourglasses, quantity, lord preset |
| Modal | ≤ 960 wide, height fits content | scrim INK 60% | explicit buttons only | any | irreversible or paid confirms, ≤ 1 at a time |
| Toast | 880 × ≤ 2 lines, y 316 | untouched | time, swipe up, tap → deep link | any | results, social moments, errors that need no decision |
| Guide overlay | full screen, one hole | dimmed (only in forced FTUE steps) | the one allowed tap | everything but cover | onboarding-forge steps and first-time moments |

Choosing rules:
1. **A sheet if the player must keep seeing the world** (building, tile, march). A full
   screen only when the content needs > 1766 px of height or > 5 sections.
2. **A modal only for a decision that costs something that cannot be undone**: gems ≥ the
   two-step threshold, dismissing troops, leaving an alliance, breaking the peace ward
   (onboarding.md §4), spending an item worth ≥ 8 h. Never a modal to say "done": that is
   a toast.
3. **Never two modals.** A second confirm inside a modal replaces it.
4. **Depth cap**: HUD + at most 3 layers (e.g. full screen → picker → modal). Opening a
   full screen from a full screen REPLACES it and keeps a back history of ≤ 5 entries.

## 3. Core actions and their tap budget

A tap is one touch that changes state or opens a surface. Scrolls, drags and typing do not
count. Counted from HUD rest, with the commit tap included. The core-loop check-in
(design-forge core-loop §8.2) is the source of the first ten rows.

| # | Core action | Path (right-hand default) | Taps | Budget |
|---|---|---|---|---|
| 1 | Help all allies | Help all button (H7) | 1 | 1 |
| 2 | Finish all free | tracker head "Finish all free (n)" | 1 | 1 |
| 3 | Start an upgrade on an idle crew | Build chip (goes straight to the suggested building's card when a crew is idle) → Upgrade | 2 | 3 |
| 4 | Start research on an idle desk | Research chip (straight to the research screen, suggested study selected) → choose → Start | 2–3 | 3 |
| 5 | Refill every muster yard | Muster chip's "Refill all" tab → confirm | 2 | 2 (core-loop A2) |
| 6 | Heal all wounded | Infirmary chip's "Heal all" tab → confirm | 2 | 2 |
| 7 | Resend every gathering banner | Banners chip's "Resend all" tab | 1 | 1 |
| 8 | Send a hunt (up to 5 camps) | camp on the map → "Hunt the nearest 5 at my level" → Send (last preset pre-filled; changing it is optional) | 3 | 3 |
| 9 | Open all chests | Chronicle (H10) → Open all | 2 | 2 |
| 10 | Claim alliance gifts | Alliance → Gifts → Claim all | 3 | 3 |
| 11 | Upgrade the building on screen | tap building → Upgrade | 2 | 2 |
| 12 | Speed up one plate | tracker chip → row "Speed up" (picker opens with the best-fit hourglass selected and the new end time first) → Use | 3 | 3 |
| 13 | Join a rally | rally toast or alliance card → Join with preset → Send | 3 | 3 |
| 14 | Reinforce an ally | ally toast → Reinforce → Send | 3 | 3 |
| 15 | Read the last battle report | report toast, or Mail → report | 1–2 | 2 |
| 16 | Claim all mail rewards | Mail (H4) → Claim all | 2 | 2 |
| 17 | Reply in alliance chat | ticker (H9) → type → send | 2 + typing | 2 |
| 18 | Open the calendar (Herald's Board) | event rail head | 1 | 2 (liveops §6.1) |
| 19 | Equip the best gear on a lord | Lords → lord → "Equip best" | 3 | 3 |
| 20 | Change a setting | More → Settings → toggle | 3 | 3 |

**The chip goes where the work is**: a tracker chip whose group has an idle plate opens that
plate's action surface directly. With nothing idle, it opens the drawer (timers, speed-up,
help). Batch tabs ("Refill all", "Heal all", "Resend all") appear beside a chip only while the
batch applies (hud.md §6). Against core-loop §8.2, crews and desks cost fewer taps and chests
plus gifts cost 3 more, so the mid profile lands at about 25 taps and the late profile at ≤ 30.
`ux_flow_probe` walks every row from HUD rest and prints the measured count. A row over
budget is a red result, not a note.

Deep management (talent trees, the gear of each slot, alliance administration) is exempt
from the 3-tap rule but stays ≤ 5 taps. Each such screen has a one-tap batch action
("Equip best", "Spend points on the suggested path", "Accept all requests").

## 4. The navigation map

```
HUD REST (castle or realm)
├─ H1 resource chip ×6 ─── resource sheet (1) ── source row → building / camp / shop (2–3)
│   └─ gems chip ───────── shop full screen (1)                              [money: one entry]
├─ H2 profile badge ────── profile (1) ── titles · history · settings shortcut (2)
├─ H4 mail ─────────────── mail full screen (1) [mail-forge] ── Claim all (2) · report (2) [report-forge]
├─ H4b offer slot (≤ 1) ── offer card (1) ── Buy → store sheet (2)          [monetization.md §5]
├─ H5 event rail ───────── Herald's Board (1) ── event (2);  event icon → event (1)
├─ H6 tracker chip ×5 ──── idle? action surface (1) → act (2) · else drawer (1) → row (2) → act (3)
│   └─ batch tab (while it applies): Refill all · Heal all · Resend all (1) → confirm (2)
├─ H7 Help all (1)         H8 next-goal card → target surface (1) → act (2)
├─ H9 chat ticker ──────── chat (1) [chat-forge]
├─ WORLD TAP  castle: building → building card sheet (1) → Upgrade / function tab (2) → act (3)
│             realm:  tile → tile sheet (1) → Scout / Attack / Gather / Rally (2) → composer → Send (3)
└─ H10 bottom bar
    ├─ Lords ───────────── roster (1) → lord (2) → tab: skills · talents · gear · pairing (3)
    ├─ Alliance ────────── alliance home (1) → help · gifts · members · charters · territory · rallies · pacts · Roll (2)
    ├─ WORLD SEAL ──────── castle ⇄ realm (1)
    ├─ Chronicle ───────── daily orders · weekly writ · season track, Open all (1–2)
    └─ More ────────────── grid (1) → bag · research · rankings · Herald's Board · reports · the ledger · settings · help (2)
```

The bottom bar has exactly five slots. **No sixth button and no expanding menu**: an
expanding menu adds one tap to everything inside it. A new top-level destination replaces
one of the five, or it goes into More and gets a contextual entry where the player needs it.

## 5. Route strings — the contract other skills use

Every surface has a route. Toasts, mail (mail-forge), chat share cards (chat-forge), reports
(report-forge), push notifications, the next-goal card, onboarding steps and the tracker all
open surfaces ONLY through routes, never by instancing scenes themselves.

| Route (pattern) | Surface | Depth | Parent for back |
|---|---|---|---|
| `hud` | HUD rest | 0 | — |
| `building/{id}` · `building/{id}/{tab}` | building card sheet 66% | 1 | hud |
| `plates/{group}` | tracker drawer (build, research, muster, infirmary, banners) | 1 | hud |
| `research/{desk}` · `research/{desk}/{node}` | research full screen | 1–2 | hud |
| `muster/{line}` | muster yard sheet 92% | 1–2 | hud |
| `infirmary` | infirmary sheet 66% | 1–2 | hud |
| `lords` · `lords/{id}` · `lords/{id}/{tab}` | lords full screen | 1–3 | hud |
| `alliance` · `alliance/{section}` | alliance full screen | 1–2 | hud |
| `events/board` · `events/{id}` | Herald's Board / event | 1–2 | hud |
| `chronicle` · `chronicle/{track}` | chronicle sheet 92% | 1 | hud |
| `shop` · `shop/{shelf}` · `offer/{id}` | shop full screen / offer card | 1–2 | hud |
| `bag` · `bag/{kind}` | bag full screen | 2 | more |
| `rankings/{board}` | rankings full screen | 2 | more |
| `profile/{player_id}` | profile full screen | 1 | hud |
| `settings` · `settings/{section}` | settings full screen | 2–3 | more |
| `realm/tile/{x}/{y}` · `realm/march/{id}` | tile sheet 40% / camera to march | 1 | hud |
| `chat/{channel}` · `mail/{folder}` · `report/{id}` | chat-forge, mail-forge and report-forge surfaces | 1–2 | hud |
| `ledger` · `ledger/{lesson}` | the ledger (onboarding.md §7) | 2 | lords |

Rules:
1. **Every route resolves**: `ui_route_probe` (qa.md §2) opens each route with fake data and
   fails on a missing scene, a depth > 3 or a missing parent.
2. **Depth in the table is the maximum.** A deep link to depth 2 builds the back history
   (`hud → alliance → alliance/gifts`), so back from a deep link never exits the app.
3. **Unknown or stale ids** (a finished event, a deleted report) open the parent with a
   toast: "That event has ended — see the Board". Never a blank surface.
4. Route parameters are ids, never display text: localisation never breaks a link.

## 6. The stack, back and resume

1. **One router** (`UIRouter` autoload, godot.md §4) owns the stack. Panels never
   `queue_free()` their siblings or open each other directly.
2. **Back order**: close the topmost picker → modal (only when it has a safe "Cancel") →
   sheet or drawer → full screen → at HUD rest, a toast "Press back again to leave" with a
   2 s window, then quit. Never a title menu, never a "Leave the realm?" dialog.
3. **The back control on full screens** is in the footer on the hand side's opposite corner
   (bottom-left for right-handed players), 144 × 144, the same place on every full screen.
   It is not at the top-left: that is the hardest reach on the phone. The system back and an
   edge swipe do the same thing.
4. **Sheets** close with a drag down or a tap on the dimmed world above them. Every sheet
   also has a visible close control at its top-right (132 px hit) for players who do not
   know the gesture.
5. **Focus returns to the opener** on close (keyboard, gamepad, screen reader; godot.md §11).
6. **No dead ends.** Every surface shows either the next action or the way back in the
   footer. `ux_flow_probe` fails any surface whose footer is empty.

## 7. Entry points — one fact, one home

1. **Every fact has ONE home screen**: the canonical place where it is explained in full
   (resource sources → resource sheet; a lord's power → lord overview). Every other place
   shows a summary that links to the home. Two full explanations drift apart after the
   first patch.
2. **Persistent entries are only these**: H1–H10 (hud.md §3) and the More grid. A new
   persistent entry must replace one, and the replacement goes through design-forge ux.md.
3. **Contextual entries** appear where the need arises: the "Get" link on a cost shortfall
   (to the resource sheet, whose rows put free sources first and the shop last), "Heal" on a
   report, "Speed up" on a bubble. A contextual entry disappears when its reason does.
4. **Offers** enter only through the gems chip, the single offer slot H4b and the pop-up slot,
   inside the pop-up rules (monetization.md §5.1). Never on the event rail, never on a war
   screen, never inside a guided step (onboarding.md §1).

## 8. Words on the surfaces

1. **Buttons start with a verb** ("Upgrade", "Heal all", "Send"). ≤ 2 words in English, so
   the +100% rule for short labels still fits (components.md §5).
2. **Diegetic names come from story-forge canon.** Until the owner decides (core-loop §12.4),
   these are working names: masons' crews, scriptorium desk, muster yards, infirmary,
   banners, Resolve, daily orders, weekly writ, hourglasses, the Herald's Board, the Roll.
   The UI shows the diegetic name; the tooltip or subtitle carries the plain function the
   first time ("Scriptorium desk — research").
3. **Numbers**: two time units ("1 h 12 m", "4 m 05 s" under 10 min), rounded UP, never "0 s"
   while running (core-loop §4.5). Offer windows in days and hours, never seconds
   (monetization.md §5.3). Large counts: 4 significant characters + suffix ("12.4K",
   "1.24M"); the exact value appears on long-press.
4. **Onboarding cards** ≤ 14 words, ≤ 3 cards per step (onboarding.md §2, §7).

## 9. Failure modes

| Fails when | Symptom | Caught by |
|---|---|---|
| A core action needs 4+ taps | players leave plates idle | [ ] `ux_flow_probe` row table §3 |
| A route opens a blank surface after a deep link | "broken button" reports | [ ] `ui_route_probe` with stale ids |
| Back at HUD rest opens a menu or quits at once | title-menu feel; accidental exits | [ ] `menu_test` + a back-button step in `ux_flow_probe` |
| Two modals stack | the player cannot tell which one is asking | [ ] router assertion: modal count ≤ 1 |
| The HUD switches mode many times while a pinch sits at the threshold | flicker | [ ] a pinch sweep in `map_trap_probe` / the transition probe |
| A new feature adds a sixth bottom button | the bar overflows at +40% text | [ ] `layout_audit` under pseudo-loc 0.4 |
| An offer appears on the rail or on a war screen | money-law breach | [ ] `ux_flow_probe` capture per surface; monetization.md §10 scan |
| A screen explains a fact that another screen also explains in full | the two drift apart | [ ] review checklist below |

Review checklist (every new surface):
- [ ] One route, depth ≤ 3, parent set, resolves with stale ids.
- [ ] The right surface type (§2); modals only for irreversible or paid confirms.
- [ ] Every core action it touches is within the §3 budget, measured.
- [ ] Back control in the footer; the system back does the same thing; focus returns to the opener.
- [ ] One home for each fact it shows; links instead of copies.
- [ ] No offer entry except the three allowed; none on war screens.
