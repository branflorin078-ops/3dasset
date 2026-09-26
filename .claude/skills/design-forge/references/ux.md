# UX — one thumb, one space, calm signals

What every player-facing spec must meet on screen — zones, reach, tap budgets, touch and text
floors, read distances, colour channels, bubbles, the tracker, marks, notifications, the event rail,
accessibility — and how a spec's §9 UX is reviewed. **This file owns the principles and the
budgets; ui-forge implements them** (rects in [`hud.md`](../../ui-forge/references/hud.md), kit in
[`components.md`](../../ui-forge/references/components.md), timings in
[`motion.md`](../../ui-forge/references/motion.md)); transition-forge owns cameras and zoom
thresholds; [world.md](world.md) owns what each zoom shows and the relationship values;
game-art-director [`readability.md`](../../game-art-director/references/readability.md) owns how marks
are painted; chat-, mail-, battle- and report-forge build inside these budgets. Loop numbers:
[core-loop.md](core-loop.md); genre: [benchmark.md](benchmark.md) §11.
**Every number is a PROPOSAL** unless it quotes a canonical fact or a sibling file.

## 0. Four promises

| Promise | Number | Proof |
|---|---|---|
| **Read** — state at a glance | idle plates, danger and ready rewards readable within 1 s of the castle frame; a new tester names a screen's purpose and main action in 5 s | ux_flow_probe screenshot at open; §15 pass 2 |
| **Act** — one thumb, ≤ 3 taps | every core action (§4) ≤ 3 taps from rest; its commit tap in the easy zone of the chosen hand | ux_flow_probe paths; ux_touch_probe |
| **Calm** — no nagging | ≤ 3 marks at open (core-loop A7); 1 toast at a time; ≤ 4 pushes per day (A8); one animated call for attention at a time | attention audit (§16) |
| **See** — the art stays big | a clear world window ≥ 40% of the screen with no persistent chrome; coverage ≤ 36% with every contextual element shown | layout_audit |

## 1. Units and the reference screen

- Canvas **1080 × 1920 portrait**; session_audit runs at 1080 × 1900 (game-director), so zones anchor to safe-area edges (`DisplayServer.get_display_safe_area()`), never to an absolute y.
- **1 dp = 2.75 canvas px** on a phone: 1080 px across a 62 mm screen, the narrowest we design for. 8 dp = 22 px · 16 dp = 44 px · 48 dp = 132 px. Tablets scale so a 144 px target measures 10–12 mm (ui-forge `hud.md` §10).
- A **tap** is one touch that changes state or opens a screen (core-loop §8); scrolls, drags and typing are not taps; confirms are. **Rest** = castle view, no panel open. 60 fps: 1 frame = 16.7 ms.

## 2. One continuous space (live-realm ruling)

1. Castle and realm are one world and one camera; the castle is a place on the realm map. No title menu, no loading screen, no "enter the map" modal. Resume lands in the castle (core-loop §8.1).
2. The centre slot of the bottom bar (the world seal) toggles Castle ⇄ Realm as one camera move ≤ 700 ms (core-loop §8.2); pinch does the same continuously. Home is 1 tap from anywhere; an off-screen own castle gets a 64 px edge arrow with its distance.
3. The HUD stays through the zoom: elements that exist in both modes never move; only those that differ cross-fade (150 ms, `hud.md` §4). Battle view and full screens swap in their own chrome.
4. Four bands (thresholds and hysteresis: transition-forge; content per band: [world.md](world.md) §13): castle close, castle overview, region, realm. **Each band shows one layer** (lessons G-10): close = craft and bubbles; overview = silhouettes and bubbles; region = castles, camps, marches, plates; realm = markers, tags, territory, landmarks.
5. Camera memory: closing a panel restores the camera, zoom and selection it opened from. Deep links: every toast, push, report, share card and mark lands on the exact place in 1 tap.
6. Interrupt: back within 10 min → the same screen and state; later → the castle and the digest (the realm has moved on).

## 3. HUD zones (1080 × 1920, % of the safe area; rects: `hud.md` §3)

| Zone | y % | x % | Holds (`hud.md` ids) | Reach class | Budget |
|---|---|---|---|---|---|
| Z1 status band | 0–15 | full | 6 resource chips H1; profile + power H2–H3; mail H4 | hard | read; taps ≤ 3 per day |
| Z2 upper rails | 16–52 left · 16–23 right | 0–13 · 87–100 | event rail H5 (Herald's Board + ≤ 4 events) · offer slot H4b (≤ 1 icon) | hard → stretch | entries used ≤ once per session |
| Z3 tracker | 28–66 chips · 66–82 head and Help all | 86–100, hand side | tracker H6, head H6h, Help all H7 | stretch → easy | ≤ 6 fixed chips; batch actions lowest |
| Z4 clear world window | 16.5–74 | 14–85 | nothing persistent; ≤ 3 contextual pieces at once (bubbles, toasts, digest, batch tabs) | — | ≥ 40% of the screen |
| Z5 goal + chat | 74–87 | full | next-goal card H8; chat ticker H9 (chat-forge) | easy | 1 line each |
| Z6 bottom bar | 91–100 | full | 5 × 216 px: Lords · Alliance · **world seal** · Chronicle · More | easy | no target centre within 120 px of a corner |

1. **Read at the top, act at the bottom.** The top 36% (y < 700) holds read-only information and entries used once a day or less; any action used ≥ 3 times per check-in sits in the easy zone (§4).
2. **The zones are full.** A new persistent HUD element replaces or merges an existing one (§15 UX-16).
3. **Coverage** (opaque + scrim pixels, every contextual element shown) ≤ 36% (`hud.md` measures ≈ 35%); ≤ 12% in battle view (battle-forge keeps the central 60% × 60% clear). More → Hide HUD = 0% until the next tap. Growth comes out of chrome, never out of the window.
4. **Nothing moves under the finger**: fixed elements keep their places for the session; contextual pieces (batch tabs, the head, Help all) appear beside fixed ones and never displace them; reorders wait for the next resume.
5. **Handedness**: right hand by default — tracker and Help all on the right, rail and offer slot on the left (the genre puts the queues away from most thumbs). The Hand setting mirrors every rect by anchors, never by RTL (`hud.md` §10).
6. Taller phones give the extra height to the world window, never to bigger chrome.

## 4. Thumb reach and the ≤ 3-tap rule

| Reach class | Distance from the grip pivot (bottom corner on the hand side) | ≈ mm | May hold |
|---|---|---|---|
| Easy | 250–1000 px | 15–59 | core actions; every commit tap |
| Stretch | 1000–1300 px, or < 250 px (the thumb folds) | 59–77 (or < 15) | entries used 1–2 times per check-in |
| Hard | > 1300 px | > 77 | read-only; entries used ≤ once a day; never timed |

`hud.md` §2 uses a band proxy — easy y ≥ 1150 minus the two 120 × 120 bottom corners, stretch
700–1150, hard < 700 — which matches this model within one chip for the right hand; where the two
disagree, the radial class decides. Both hands share the easy class only in a lens at the bottom
centre (x 11–89% at 84–88% of the height): the world seal, the next-goal card and full-screen
commit buttons live there. Calibrate with ≥ 5 testers on two phone sizes: misses ≤ 2% per zone.

1. **Core actions ≤ 3 taps from rest**; other features ≤ 5; any setting ≤ 4. Panel depth ≤ 3; every panel closes in 1 tap (the back control + Android back).
2. The commit tap sits in the easy zone of the chosen hand; an entry may be stretch. No core action needs two fingers (the seal and tracker jumps replace pinch).
3. One Primary action per surface, on the hand side of the footer (ui-forge `components.md` §9).

| Core action | Path from rest | Taps |
|---|---|---|
| Help allies · finish every free timer | Help all (H7) · the tracker head "Finish all free (n)" | 1 |
| Castle ⇄ realm, or home | world seal | 1 |
| Upgrade with an idle crew | build chip → suggested building card (next tier ≥ 40% of screen height, core-loop §8.2) → Upgrade | 2 |
| Start research | research chip → pick → Start | 2–3 |
| Refill musters · heal all · resend gathering | the chip's batch tab → commit | 2 |
| Hunt | banners chip → Hunt nearest 5 → Send | 3 |
| Answer an attack | the Incoming row → Call allies / Recall / Defence (battle-forge [`defence.md`](../../battle-forge/references/defence.md) §2) | 2 |
| Join a rally | rally toast or Alliance → Join (lord preset kept) → Send | 3 |
| Read a report · claim mail | its toast, or Mail → report · Mail → Claim all | 1–2 · 2 |
| Open daily chests · Herald's Board · shop | Chronicle → Open all · rail head · gem chip | 2 · 1 · 1 |

The tracker's shape must keep the core-loop §8.2 check-in at ≤ 24 taps (mid) and ≤ 30 (late).

## 5. Touch, feedback, timing

| Rule | Number |
|---|---|
| Hit rect | ≥ 132 × 132 px (48 dp); the visual may be smaller (grow it with `Control._has_point()`); hit rects never overlap; visual gaps ≥ 16 px |
| Commit | on release (`BaseButton.action_mode = ACTION_MODE_BUTTON_RELEASE`): a finger can slide off to cancel |
| Gem spend | two-step Premium button ("Confirm ◆120" for 3 s, `components.md` §9); **the Confirm state ignores taps for its first 400 ms**, so a double tap cannot buy; at or above shop-forge's large-spend threshold, a modal (PROPOSAL for the threshold: the 1 h hourglass price `p(60)`, core-loop §5) |
| Money Buy button | the same height as Close; ≥ 48 px from frequent controls; never where Claim or Help all sit on other screens ([monetization.md](monetization.md) §9) |
| Touch slop · long press · double tap | 22 px (8 dp) makes a drag · 450 ms opens details, never spends · never used (waiting for a second tap delays every tap by ≈ 300 ms) |
| World tap tolerance | the nearest object within 44 px, if it is the only candidate |
| Feedback | pressed visual on the same frame; sound ≤ 50 ms (audio-forge); 10 ms haptic on commits and claims (`motion.md`, switchable) |
| Result | ≤ 1 s, or a progress mark in place from 300 ms; busy 15 s → the error state with a plain reason + Retry (`components.md` §9) |
| Panels · input | enter ≤ 260 ms (16 frames), exit ≤ 200 ms (`motion.md` tokens); a tap mid-animation finishes it; input never blocked > 300 ms (core-loop A9) |
| Confirm modals | only for a large gem spend, an irreversible act named in numbers ("Dismiss 1,200 Pikemen?"), or ending the peace ward. Everything else acts at once or uses the Danger two-step |

## 6. Text and read distances

**6.1 The math.** A phone is read at ≈ 35 cm: 1 arcminute = 0.102 mm = **1.77 px** on the narrowest
62 mm screen (1.69 px on a typical 65 mm one). Running text needs an x-height near 12′ (**≥ 20 px**);
one short line 9′ (**≥ 16 px**); a bold number or ≤ 2 words ≈ 7.5′ (**≥ 13 px**). With the text
face's x-height ≥ 0.47 em (`components.md` §2) the size floors are:

| Text | x-height | Floor | ui-forge token |
|---|---|---|---|
| Numbers, timers, ≤ 2 words | ≥ 13 px | **28 px**, bold, on a plate or with a 3 px INK outline (`LabelSettings.outline_size`); HUD numbers use digits 32 | digits 32 |
| One line ≤ 40 characters | ≥ 16 px | **34 px** | caption 36 |
| Running text (more than one line) | ≥ 20 px | **42 px**, line height 1.3, 28–60 characters per line | body 42 |

1. Nothing below 28 px, and 28 px only for bold numbers and ≤ 2 words (battle-forge totals, chat-forge meta, world.md level plates); any line below 34 px or running text below 42 px is a return.
2. Text over the painted world sits on an INK scrim ≥ 70% or carries the INK outline — never bare. Tablets at 45 cm give more px per arcminute: the phone binds.
3. Changing numbers use tabular digits (`tnum` on the FontVariation). HUD numbers: 3 significant digits + K/M/B ("12.4K"); exact in costs, confirms and long-press; timers in two units, rounded up (core-loop §4).
4. Strings fit with +40% length (l10n-forge); a button never truncates a verb or a number. Text size 100 / 115 / 130% scales every floor; layouts pass at 130% with +40%.
5. **Transient text** stays `clamp(1500 + 300 × words, 2500, 6000)` ms (`components.md` §12). Needs more → not transient. Exempt: the resume digest (2.5 s, core-loop §8.1), whose lines stay readable in the tracker and the chronicle.
6. One verb per action everywhere ("Upgrade", never "Improve" elsewhere); the l10n glossary holds the verbs.

**6.2 World read distances.** What each zoom band shows, label caps and marker sizes: [world.md](world.md)
§13 (e.g. ≤ 40 labels at region, 0 overlaps); building sizes per band: blender-forge
[`architecture.md`](../../blender-forge/references/architecture.md) §2 (180–320 / 60–120 / 48–96 px); smallest mark sizes: `readability.md` §1. The UX
rules on top: a world object is tapped through a ≥ 132 px hit (its bubble, plate or marker when the
model is smaller); world text obeys §6.1 with the INK outline; plates never stack or overlap — the
lower priority fades out in 150 ms.

## 7. Colour channels — one meaning per colour

A **signal** is a flat colour that changes with state (fill, ring, line, text colour). Painted art
and fixed chrome ornament are not signals, and a signal never borrows an ornament's shape.

| Colour | Its one meaning as a signal | Never |
|---|---|---|
| GILT #C9A04C / lit #E0BC6A | value and "yours": Primary button, Idle outline (on OAK or INK), progress fills, the onboarding pointer, success (a seal + the word) | text on PARCHMENT (1.74:1); relationship |
| WAX #8A1F24 | the negative state: the HUD danger alert, Danger buttons, failure (a broken seal + the word), shortfall ("−7.6K" + Get) | relationship; decoration; buy screens |
| Relationship (§7.1) | who it belongs to | chrome, buttons, rarity, lord kit |
| Line accents · rarity | the troop line (medallion ring, banner trim) · item rarity (rims and glow on INK card backs) | the map layer as fills; chrome |

No "success green", no "info blue": both would read as relationship. Contrast musts (full table:
`components.md` §2): never GILT text on PARCHMENT (1.74:1), never a WAX mark on OAK without a
PARCHMENT ring (1.36:1), never a line accent as text on PARCHMENT (1.63–3.97:1); GILT on IRON
(4.28:1) for large text and shapes only.

**7.1 Relationship — the reserved channel.** Classes, values and stroke: [world.md](world.md) §12, its
single source; painted marks: `readability.md` §4, which still proposes another set (world.md's
owner decision 6 picks one). Classes: **Self** (circle) · **Ally**, Accord partners included (heater
shield) · **Enemy** — anything aimed at you or your alliance's holdings, and for 24 h the alliance
that attacked you (crossed blades) · **Neutral** — everyone else, camps and AI lords included
(square). Red is earned by a threat, not by strangers. This file owns the pass line and where the
channel may appear.

1. **Pass line**: every pair ≥ 20 ΔE2000 in normal vision and in each full-severity simulation (Machado 2009) — world.md §12's check, run by a11y_audit. Re-measured here, worst pairs normal / protan / deutan / tritan: world.md's set 30.2 / 23.7 / 30.3 / 26.5 — **passes**; readability.md's set 26.4 / 24.1 / 18.4 / 19.8 — fails deutan and tritan; a genre-style green / blue / red / white set (#5BC44F, #3B78D8, #D63A2E, #D9D4C7) 27.5 / 22.4 / 13.8 / 19.2 — fails.
2. **Casing that holds on any ground**: world.md's recipe (colour core + 2 px INK keyline + 1 px PARCHMENT halo at 60%) leaves 2.74:1 on a mid-grey ground (#5E5E5E). A 2 px halo at 100% gives ≥ 3.57:1 on every ground — the worst ground sits between the two rings in luminance. Proposal to world.md; high-contrast setting: 3 + 3 px.
3. **Never colour alone**: shape + line pattern + the name or tag. Greyscale and simulation test: ≥ 19 of 20 random marks named correctly in each version.
4. **Where**: marker rings and plates, march lines and heads, name-plate frames, territory edges and fills (never the only cue), battle banner fields and side bars, chat markers (24 px). Never text colour on the map, chrome, buttons, rarity, lord kit, events, offers or buy screens. The HUD alert about an attack is WAX; the attacker on the map is Enemy.
5. Alliance tinctures stay on flag cloth (tint mask, blender-forge `architecture.md` §7), ≥ 15 ΔE2000 from every relationship colour; rarity and line colours never fill anything on the map layer.

## 8. Status bubbles over buildings

| Rule | Number |
|---|---|
| Caps | ≤ 1 per building; ≤ 5 at castle overview (priorities 0–3 only), ≤ 8 at castle close (`hud.md` §7) |
| Look | Ø 104 parchment medallion, 6 px rim (gilt; WAX for priority 0), Blender-made icon 64 px (never a glyph), hit 144 |
| Text | ≤ 4 characters in the digits token ("6", "4m", "3/4"); never seconds |
| Overlap | centres < 120 px apart merge (the higher shows with a "+1"); a bubble touching a HUD zone hides, never draws over chrome |
| When | castle close and overview only; the building ≥ 60 px on screen; fades in 150 ms after the camera settles; no idle bobbing |
| Tap | free and reversible → done at once (Finish free, Claim: 1 tap); anything that spends → its card, on the commit (2 taps) |

Priority: **0** danger or a failed defence check (battle-forge `defence.md` §4) → **1** Finish free
→ **2** Idle (muster yard, desk) → **3** Wounded waiting → **4** Claim → **5** the Advisor's pick:
the next-goal building, only when affordable and a crew is idle, max 1 ([progression.md](progression.md)
§11 N5). Never: collect bubbles (production is collected on open, core-loop A1 — the genre's tap
chore), "could upgrade" anywhere else (N6), bubbles on paid goods or the shop, looping motion.

## 9. Queue and march tracker

1. **One tracker for every plate** (core-loop §2 rule 2), in castle and realm; hidden in battle view and full screens. ≤ 6 fixed chips on the hand side (`hud.md` §6 ships 5: infirmary, research, muster, build, banners); order fixed for the session.
2. A chip shows the soonest end as a ring, busy/total ("2/3") in the digits token, and **Idle** as a GILT_LIT outline + the word — never colour alone, never flashing.
3. **Batch actions sit nearest the thumb**: the head "Finish all free (n)" and Help all in the easy zone; batch tabs (Refill all, Heal all, Resend all) attach to their chip only while they apply.
4. **Chip tap**: an idle plate → its action surface; else the drawer, bottom-anchored. A march row tap flies the camera to the march (transition-forge); Recall is a Danger two-step.
5. **Incoming** (battle-forge `defence.md` §2): the Detected row appears in the easy zone without moving a chip. At Near its actions — Call allies · Recall marches · Defence — stay in the easy zone; the top banner (≤ 12% of the short side) counts down. Read at the top, act at the bottom (proposal to battle-forge, whose banner carries the buttons today).
6. **The next goal** ([progression.md](progression.md) §11 N1, 0 taps: "the tracker's top row") is drawn as the card H8 above the ticker, because a 132 px chip cannot hold "Keep 17 · needs Hospital 16 · ~2 h"; ≤ 40 characters; tap → its route.
7. When every plate runs: "All busy — first free at 14:20" for 4 s (core-loop §2 rule 4).

## 10. Marks — the attention budget

`hud.md` §5 ships the mark: a WAX dot 24 px with a 4 px PARCHMENT ring, and a count pill. **Proposal
(§17)**: the same geometry in GILT_LIT with an INK ring. A claimable reward is value, not urgency;
WAX keeps one meaning, the negative state (§7). Every rule below holds for either colour.

| Class | Source | Mark | Clears | Expires |
|---|---|---|---|---|
| danger | attack Detected or Near, wall burning | warning bands (§11), never a mark | when the threat ends | — |
| **P1** | a claim that ends in < 24 h; a war call the player pledged to | dot | claimed or answered | at its end (auto-claimed at reset, core-loop §7) |
| **P2** | claimable: chest, attachment, milestone, gift; a step payable from held items ([lords.md](lords.md): ≤ 1 on the hall) | dot | claimed | never, until claimed |
| **P3** | addressed to the player: @mention, personal mail, application (officers) | dot or count | viewed | 72 h unviewed |
| **P4** | an idle plate | the Idle tag on its chip | the plate starts | never |

1. **Budget**: ≤ 3 marks visible at session open for the median save, Idle tags included (core-loop A7); a runtime cap of 5 root marks — lower priorities are held, never lost; ≤ 1 event mark ([liveops.md](liveops.md) C8).
2. **Propagation**: a leaf raises a dot on its root entry; only counted things (mail, mentions) show a number, "99+" at most. The marked child is visible on the next screen without scrolling (marked rows sort first) and every mark is ≤ 3 taps from its action. A root mark with no visible child is an **orphan** — a bug.
3. **Never marked**: offers, the shop, the gem chip, the offer slot, the chronicle purchase, the cosmetic shelf, "new" or "started" events, news, rank changes, "could upgrade" (progression N6), unclaimable bag items, system mail without an attachment (mail-forge), realm-channel chat.
4. Appear once with a 200 ms scale-up; never loop, pulse or flash. Settings → Marks for: mentions · alliance · events. Danger cannot be switched off.
5. **One call at a time**: at most one element animates for attention at any moment (pointer, warning pulse, a bubble's arrival); counting timers are exempt.
6. **The attention ledger** (`design/ux/ATTENTION.md`, path to confirm): one row per source — `system · signal (mark / bubble / toast / push / rail) · class · trigger · clears · expires · max visible`. A spec adds its rows; the reviewer re-sums the caps (§15 pass 6).

## 11. Notification tiers

| Class | Push (app closed) | In game | Digest · archive |
|---|---|---|---|
| Danger | the war-alert channel (battle-forge `defence.md` §2): its own opt-in, grouped ≤ 1 per 60 s, ≤ 6 per day, none when ETA < 90 s, muted in quiet hours unless "Wake me for attacks" (default off) | Detected: Incoming row + fortress bubble + hostile line pulse ≤ 1 Hz. Near (ETA ≤ 60 s): WAX countdown banner (PARCHMENT text 6.53:1) + actions in the easy zone (§9 rule 5); audio (audio-forge); haptic | one digest line, never a stack of modals · reports in Mail (report-forge) |
| P1 | only when asked (Remind me on the Herald's Board; an alliance-call opt-in) | toast + mark | ✓ · — |
| Work done | grouped per batch ("3 works done · 2 crews idle") | merged toast + tracker | ✓ · chronicle |
| P2 · P4 | never | mark · Idle tag | ✓ · mail when mailed |
| Social (P3) | whisper, mention, rally call: chat-forge [`channels.md`](../../chat-forge/references/channels.md) §8 | ticker + mark | — · chat |

1. **Push budget** outside the war channel: ≤ 4 per day (core-loop A8); ≤ 3 in week 1 ([onboarding.md](onboarding.md), which owns the permission card); event pushes ≤ 1 per day inside it (liveops C9); chat ≤ 2 of the 4 (chat-forge). Quiet hours 22:00–08:00 local. Never for offers or anything paid (money-law).
2. **Push copy**: title ≤ 30 characters, body ≤ 60; names the thing and the time; no urgency words ("hurry", "last chance"); string keys, never baked text (l10n-forge).
3. **Toasts** (`components.md` §12): 880 px wide at the top of the world window, ≤ 2 lines; 1 on screen, ≤ 3 queued; same-type toasts merge; never over the tracker or the bottom bar; none during a battle replay (they wait). A decision is never a toast.
4. **Modals**: confirms (§5) only; at session open only for legal consent, a ban or maintenance (`components.md` §11). Offer pop-ups follow [monetization.md](monetization.md) §5 rule 1 and never land between a tap and its result.

## 12. Event rail and the Herald's Board

1. **The rail holds ≤ 4 event icons** — the season first, then events by end time ([liveops.md](liveops.md) C2) — under its head, the Herald's Board. Never an offer: the one offer slot sits apart and outside the easy zone ([monetization.md](monetization.md) §10).
2. Icons are Blender-made art, never glyphs. Each carries its remaining time in the digits token — days + hours, hours + minutes on the last day, never seconds — and ≤ 1 mark on the whole rail, P2 only (liveops C8).
3. Onboarding chapters and the realm's founding event share ONE icon ([onboarding.md](onboarding.md)). Order is fixed within a session.
4. More live events than slots is a design error that liveops C1/C2 prevent; if data breaks it, the head shows "+n" and ux_flow_probe reports the breach.
5. **Herald's Board** (liveops §6.1): 1 tap from the rail; 21 days ahead, 14-day freeze; local time with the UTC offset; Remind me per event (an opt-in P1 push inside the budget).

## 13. Accessibility and settings

| Need | Rule | Proof |
|---|---|---|
| Colour vision | relationship by shape + pattern + the §7.1 pass line; rarity by frame studs and the tier word; the line by its silhouette icon (`components.md` §4) | a11y_audit simulation pass; greyscale screenshots |
| Low vision · contrast | §6 floors; text 100 / 115 / 130%; high-contrast marks (3 + 3 px); §7 musts | a11y_audit at 130%; contrast_test |
| Motion | Reduced motion: camera moves become ≤ 200 ms cross-fades, no shake, slides become 120 ms fades (`motion.md`); never > 3 flashes per second (WCAG 2.3.1); no pulse faster than 1 Hz | a11y_audit flash counter |
| Hearing · motor | every sound cue has a visual twin; voiced lines captioned (story-forge) · 48 dp targets, no gesture-only action, no timed input, the Hand setting | review · ux_touch_probe |
| Reading · attention | plain words, one verb per action, +40% fits · mark, toast and push budgets, per-category toggles, quiet hours | l10n pseudo-locale · attention audit |

Settings (each ≤ 4 taps): Hand · Text size · Reduced motion · High-contrast marks · Haptics · Marks
for · Push categories · Quiet hours · Wake me for attacks · Chat ticker · Hide HUD. Read OS
accessibility flags where Godot exposes them (verify in the shipped 4.7); the saved setting wins.

## 14. Genre weak spots → our fix

| Weak spot ([benchmark.md](benchmark.md) §11) | Our fix | Number |
|---|---|---|
| Icon clutter; offers crowding navigation | fixed zones; rail cap; one offer slot, off the rail, outside the easy zone | rail ≤ 4 + head; ≤ 1 offer slot |
| Red-dot fatigue | mark classes, expiry, held overflow, orphan rule; no false urgency (§17-1) | ≤ 3 at open, cap 5 |
| Colour-only relationship | shape + line pattern + a ≥ 20 ΔE2000 pass line + a full-opacity halo | worst pair ≥ 20 vs the genre-style 13.8 |
| Collect bubbles as a tap chore | collect on open; no harvest bubbles | 0 collect taps |
| Queues away from the thumb; deep screens | tracker on the hand side; ≤ 3 taps; depth ≤ 3; first-time guides ([onboarding.md](onboarding.md)) | commit taps easy |
| Chrome fighting the painted world | clear world window; coverage cap; Hide HUD | ≥ 40% · ≤ 36% |

## 15. Reviewing a spec's UX (SYSTEM.md §9)

This answers red-team check 9 of [../SKILL.md](../SKILL.md). A system a player can see or touch has
a §9; the reviewer returns a missing or generic §9 as if it were ★ ([spec-template.md](spec-template.md)). **Paste and fill:**

```markdown
## 9. UX
- Lives in: <building / realm object / HUD zone / panel> · bands: <close/overview/region/realm>
- Entry points (taps from rest): <entry — n taps> …   Core action? <yes → ≤ 3>
- One-hand flow: 1. <target> (<zone>, <reach class>) → 2. … → commit (<reach class>)
- Attention added: <mark class · bubble priority · toast · push class>
  ledger after: marks <n>/3 at open · bubbles <n>/5 · rail <n>/4 · push <n>/4
- Strings: <key — English characters — fits +40% at 130%? y/n>
- States: empty · loading (> 300 ms) · error (reason + 1 action) · locked (keys + distance) · max
- Colour and shape: channels used; reserved colours only for their meaning
- Motion: enter/exit ms; reduced-motion variant; input never blocked > 300 ms
- Art: what is shown big, at what % of screen height
- Harness: ux_flow_probe path · ux_touch_probe · a11y_audit · layout_audit · w1f_aspect_sweep
```

**Reviewer's passes** (one line of evidence each): (1) **paper walk** — every tap from rest and its
reach class; (2) **5-second test** — a tester new to the mock names its purpose and main action;
(3) **greyscale + simulation** — every state and class still differs; (4) **thumb overlay** — the
§4 map on the screen, both hands; (5) **stress strings** — +40% pseudo-locale at 130%; (6)
**budget sum** — its ledger rows added, every cap holds; (7) **interrupt** — kill the app mid-flow:
§2 rule 6 resume, nothing lost or spent twice.

| # | Check | Returned when |
|---|---|---|
| UX-01 | Place and bands | "somewhere in the menu" |
| UX-02 | Tap counts | a core action > 3, anything else > 5 |
| UX-03 | Reach | a commit tap outside the easy zone; a two-finger step |
| UX-04 | Targets | a hit rect < 132 px; overlapping hit rects; a one-step gem spend |
| UX-05 | Text | a size below its §6 floor; a string without the +40% check |
| UX-06 | Colour | a reserved colour outside its meaning; greyscale fails |
| UX-07 | Relationship | colour without shape and pattern; a token change without the §7.1 numbers |
| UX-08 | Attention | a signal without class, clear rule or expiry; a cap exceeded |
| UX-09 | States | any of the five states missing |
| UX-10 | Timing | feedback later than the same frame; no progress mark after 300 ms; input blocked > 300 ms |
| UX-11 | Interrupt | lost input or a double spend on resume |
| UX-12 | Money-law | war imagery on a buy surface; a mark on a paid surface; a second offer slot |
| UX-13 | Accessibility | no reduced-motion variant; a sound without a visual twin |
| UX-14 | First vs hundredth time | no first-time guide ([onboarding.md](onboarding.md)), or the repeat path over budget |
| UX-15 | Harness | no probe named with its verdict line |
| UX-16 | Art and HUD | art below its size rule; a new persistent HUD element that replaces nothing |

Verdict (PROPOSED wording): `UX REVIEWED - 16/16, core max 3 taps, commit easy, marks 3/3, push
4/4` — or a numbered list of returns.

## 16. Failure modes → harness (the checklist)

| § | Fails when | Caught by |
|---|---|---|
| 2 | a loading screen or modal between castle and realm; a shared element moves between modes; Home > 1 tap | [ ] transition probe (transition-forge); layout_audit per mode; map_trap_probe |
| 3 | world window < 40% or coverage > 36%; persistent chrome in the window; a zone breaks on a shape | [ ] layout_audit rect union; `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| 4 | a core action > 3 taps; a commit tap outside the easy zone; a check-in over 24 / 30 taps; depth > 3 | [ ] ux_flow_probe paths; ux_touch_probe reach map; session_audit; menu_test crawl |
| 5 | a hit rect < 132 px or overlapping; a Confirm state live < 400 ms; input blocked > 300 ms | [ ] ux_touch_probe; frame capture of panel opens (ui-forge qa) |
| 6 | text below its floor at 130%; a verb or number truncated at +40% | [ ] a11y_audit at 130%; l10n pseudo-locale pass |
| 7 | a worst pair under the pass line; a mark readable only by colour; a §7 "never" pair shipped | [ ] a11y_audit simulation + greyscale; contrast_test |
| 8 | > 5 bubbles at overview; a collect or "could upgrade" bubble; a bubble over chrome | [ ] layout_audit bubble count and overlap list |
| 9 | an idle plate > 3 taps from running; a chip moves in a session; no next-goal line on a castle screen | [ ] ux_flow_probe per plate; layout_audit snapshot; ux_flow_probe (progression §11) |
| 10 | > 3 marks at open; an orphan; a mark on a paid surface | [ ] ux_flow_probe screenshot at open; attention audit |
| 11 | > 4 non-war pushes a day; a push in quiet hours without the opt-in; 2 toasts on screen; a modal on resume | [ ] push probe on a fake clock (`warning_probe` / `chat_push_probe` pattern); ux_flow_probe |
| 12 | > 4 rail icons; an offer on the rail; seconds in a countdown | [ ] ux_flow_probe rail scan; label string scan |
| 13 | > 3 flashes per second; a surface without its reduced-motion variant | [ ] a11y_audit flash counter |

New (qa-forge writes it; path to confirm): an **attention audit** that sums the ledger and replays
a 7-day fake-clock session — `ATTENTION OK - marks 3/3 at open, rail 4/4, bubbles 5/5, push 4/4 per
day, 0 orphans` (PROPOSED wording).

## 17. Owner decisions required

1. **Gilt marks instead of WAX dots** (§10): a claimable reward is value, not urgency, and WAX keeps one meaning. Until decided, `hud.md` §5's WAX dot with its PARCHMENT ring stands.
2. **Which relationship set** (world.md owner decision 6): by this file's pass line, world.md §12's set passes and readability.md §4's fails for deuteranopes (18.4) and tritanopes (19.8).
3. **The halo at 100% and 2 px** (§7.1 rule 2) — a change to world.md §12's stroke recipe.
4. **Near-warning actions in the easy zone** (§9 rule 5) — a change to battle-forge `defence.md` §2's top banner.
