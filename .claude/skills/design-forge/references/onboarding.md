# Onboarding — the first ten minutes, the first week, and the lessons the genre never gives

How a new player goes from the first tap to a named house with a sworn lord, an alliance and a first
rally — and how every LATE system is taught at the moment it opens, not on a video site.
Implementation: **onboarding-forge** (script runner, chapters, first-time moments, save fields),
**ui-forge** (overlay, pointer, cards), **transition-forge** (march-out, first zoom-out),
**battle-forge** (raids, first battle, first rally), **commander-forge** (the swearing),
**cloud-forge** + **world-forge** (ward, placement, routing, passage), **story-forge** + **l10n-forge**
(every line), **feel-forge** / **audio-forge** (ceremonies, cues), **qa-forge** (harness). Genre
patterns: [benchmark.md](benchmark.md) §10.

**Every number here is a PROPOSAL** unless it quotes a canonical fact or a sibling reference. Shipped
values in `data/*.gd` (paths to confirm) win; a collision with a sacred balance constant becomes an
owner proposal (§14). Quoted, never redefined: plates, free finish (5 min), help `max(1%·R, 120 s)`
with `H = 10` for a new alliance, Resolve, daily orders — [core-loop.md](core-loop.md); keep curve,
key graph, Age Trials — [progression.md](progression.md); loss rows — [combat.md](combat.md); lords,
Seals, talents, sets — [lords.md](lords.md); join hook, gifts, Welcome chest —
[alliance.md](alliance.md) §3, §6, §10; realm router, Founding races, Trial Grounds —
[liveops.md](liveops.md); pop-up rule, red lines — [monetization.md](monetization.md); camps, fog,
seat moves, zoom — [world.md](world.md). This file owns the King's Peace (§4), the newcomer's passage
and the return ward (§8).

## 0. The four questions

- **Want**: minutes 0–10: a win, two buildings, a sworn lord, a camp cleared, the realm seen, a named house. Week 1: an alliance, a second lord, a first rally, a set piece, a garrison.
- **Obstacle**: in the first 10 minutes only a tap (every script timer sits inside the free finish); from chapter 2 the core-loop plates; other players are no obstacle for 7 days (§4).
- **Wait**: first win ≤ 60 s; first session ≈ 10 min scripted + free play; the step-11 muster order runs 1–8 h (the player's pick); the first timer allies can shorten is keep L8–L9 (8–15 min, [progression.md](progression.md) §7), usually in session 2 of day 1; one new chapter every 20 h.
- **Witness**: the house banner and name on the realm map (minute ≈ 7); "<house> joined" in the alliance feed; the sworn lord's gilt rim on the map token; the chapter-7 banner charge on the house banner.

## 1. Rules of the first week

1. **The live realm from second 0.** No title menu, no tutorial island, no practice world: the first raid hits the player's real castle at its real place on the realm map. Practice exists only as a Trial Grounds stage that opens AFTER the real lesson (§7 rule 5).
2. **Every guided step is a real action with a real result.** No sandbox with fake rewards — a player who learns that tutorials are fake skips every later lesson.
3. **Wins are guaranteed by data, not by a cheat flag.** Scripted fights run through the real resolver (gameplay-forge) with fixed armies sized so every lord pick beats every first camp (§12: 3 picks × 3 camps).
4. **Forced taps only in the first 110 s** (steps 1–2). After that the pointer suggests; the player may wander; a "Next" card in the queue tracker holds the path.
5. **Text budget**: ≤ 12 cards in 10 min; ≤ 14 English words per card; ≤ 2 lines at 1080 px width after +40% l10n expansion; ≤ 90 s of reading in total; never a card over a decision.
6. **Idle rule**: no input for 12 s → the pointer pulses (scale 1.0 → 1.15 → 1.0 in 600 ms, `create_tween()`); 30 s → the line repeats once; a decision is never auto-advanced.
7. **No purchase prompt inside a guided step; no offer pop-up in the account's first 72 h** ([monetization.md](monetization.md) §5 rule 1); the guide's voice never sells (red line 15). The shop stays reachable — never hidden, never pushed.
8. **Resume at the step**: killed app, phone call or crash → the next launch resumes at the last finished step, every reward kept. Steps 1–4 survive a flaky connection and sync after; from step 5 (realm) "Reconnecting…" ≤ 10 s, then a retry card — never a silent freeze.
9. **ART SHOWN BIG**: lord portraits ≥ 30% of screen height at the pick, ≥ 60% at the swearing; building cards show the next tier render at ≥ 40% ([core-loop.md](core-loop.md) §8.2). People on screen (the rider, the lords) are painted portraits or hero3d rigs — never code-built figures.
10. **One hand**: every guided tap in the bottom 60% of the portrait screen (y ≥ 760 px in the 1080×1900 probe window; orientation: [ux.md](ux.md), [world.md](world.md) owner decision 7); targets ≥ 48 dp. The pointer is a gilt gauntlet (Blender-made render, GILT #C9A04C with a 2 px INK #1E1712 outline so it reads on sky and on ground, 96 px at 1080 width), never a relationship colour; every icon on the path is Blender-made art, never a line glyph.

## 2. The first ten minutes, step by step

Clock = p50 on the reference phone (ship-forge names it), from the tap on the app icon; the probe taps
as soon as a target is live. A tap = one touch that changes state or opens a screen ([core-loop.md](core-loop.md)
§8); **D** = decision, **M** = maintenance/guided; every counted tap is in **bold**. On guided steps
the tracker opens the suggested card directly (2 taps; core-loop §8.2 counts 3 when the player picks
another). Founding castle: keep L1, barracks, archery range, infirmary, academy (PROPOSAL; verify `data/buildings.gd`).

| # | Clock | Step | What the player does and sees | D/M | Done when | Owners |
|---|---|---|---|---|---|---|
| 0 | 0:00–0:08 | Cold start | painted keep vignette with one ≤ 10-word line → the castle at dawn, 2.0 s camera push-in; guest account created silently; locale from the device | 0/0 | castle frame ≤ 8 s p50, ≤ 15 s p90 | ship-forge, cloud-forge |
| 1 | 0:08–0:40 | **FIRST WIN**: raid at the gate | "Raiders at the gate. Sound the horn." → **Horn** → Hunters on the wall loose a volley (8 s) → "Open the gate." → **Gate** → the Peasants charge (10 s) → rout; the raiders' cart counts into the resource bar (800 ms) | 0/2 | victory banner at 0:40 = 32 s after the first input | battle-forge, feel-forge |
| 2 | 0:40–1:50 | **FIRST BUILDS**: two crews | **plot** → card row → **Farm: Build** (D — the pick is the tap; 4 s); "You have two crews." → **plot** → **Lumber camp: Build** (the only lit card; 4 s). Timers = 0.4 × K(1) ([progression.md](progression.md) §3); both finish by themselves | 1/3 | two buildings produce | castle-forge, ui-forge |
| 3 | 1:50–3:00 | **FIRST LORD** (§3) | a rider at the gate; three portraits → **tap one** (D) → role card → **Swear**; gilt rim ceremony ≤ 3.0 s | 1/1 | `sworn_first` set | commander-forge |
| 4 | 3:00–3:40 | First muster | **yard bubble** → **Muster 20** (20 s; completes by itself, core-loop §4 rule 4). Edwin → barracks, Elena → archery range, Rowan → barracks (the stable opens in Age II, progression.md §3) | 0/2 | batch in the yard | gameplay-forge |
| 5 | 3:40–4:10 | Choose a target | "Raiders' camps to the east." → **March** → three personal level-1 camps (§13), each tagged Easy with its main line (the counter hint) and spoils → **tap one** (D) → **Send** (lord preset automatic) | 1/2 | march leaves | world-forge, battle-forge |
| 6 | 4:10–4:50 | **FIRST ZOOM-OUT** | the camera follows the march out of the gate and pulls back to region zoom (≤ 3.5 s first time); "Other lords' castles. Real players." and "The realm of <name>, founded <n> days ago."; labels appear 1.5 s apart: neighbours, camps, an alliance's land if near, the great places printed on the fog ([world.md](world.md) §7); the march walks 25–35 s | 0/0 | region zoom reached | transition-forge, world-forge |
| 7 | 4:50–5:50 | **FIRST BATTLE** | beats 20–30 s at 1× (skippable after 3 s; 2× speed); report headline in 1 s naming the resolver's top cause ("Victory — your archers struck before their infantry closed."; words by report-forge); one casualty line (returned / infirmary / dead 0) → **Castle** (zoom-in ≤ 700 ms) | 0/1 | camp cleared; lord level 2 | battle-forge, report-forge |
| 8 | 5:50–6:40 | Infirmary | **infirmary bubble** → **Heal all** (≈ 40 s) → **Finish (free)** — the free finish, taught once | 0/3 | infirmary empty | ui-forge |
| 9 | 6:40–8:00 | **SPINE + HOUSE NAME** | **keep bubble** → **Upgrade** (L2 ≈ 18 s, progression.md §7) → **Finish (free)**; the keep grows, the house banner rises: **sigil** 1 of 6 (D) → **name** (D; suggested name pre-filled, accept = 1 tap) | 2/3 | banner visible on the realm | castle-forge, story-forge |
| 10 | 8:00–8:50 | **ALLIANCE NUDGE** (§5) | 3 alliance cards, each with its own Join → **Join** on one (D; alliance.md §10: join = 1 tap) or "Later"; the Welcome chest appears sealed with its two bars (24 h in the alliance · helps given 0/5) | 1/0 | member (or "Later") | ui-forge, gameplay-forge |
| 11 | 8:50–9:40 | **KEYS + THE LONG ORDER** | the keep card names its L3 keys (farm 2 + a line hall 2, progression.md §2 G1): **idle crew** → **Upgrade** farm · **idle crew** → **Upgrade** the lord's hall · **idle desk** → **Start** the suggested node · **yard** → **1 h / 3 h / 8 h / until I'm back** (D; core-loop A3 — the first long timer) · the orders card opens with the step points counted → **Open** (30 chest) | 1/8 | keys started; yard on its order; chest opened | ui-forge |
| 12 | 9:40–10:00 | **EXIT HOOK** | "Send word when work is done? (≤ 3 a day)" → **Yes** (the OS dialog's Allow tap is not counted); the Next card: "Keep 3 — keys ready · Welcome chest 0/5 helps · chapter 2 in 20 h" | 0/1 | hook shown = **tutorial complete** | onboarding-forge |
| | | **Total** | | **7/26 = 33** | | |

| Budget | Number | Why |
|---|---|---|
| First input | ≤ 8 s p50, ≤ 15 s p90 after the icon tap | every second before a tap costs installs |
| First win | ≤ 60 s p90 after the first input; target 32 s (0:08 → 0:40) | a win before any reading |
| Taps | ≤ 40, of which ≥ 5 decisions (script: 33, 7) | a script of only guided taps teaches nothing |
| Longest stretch without a decision | ≤ 3.5 min; script 3 m 10 s (step-5 pick ≈ 3:55 → step-9 sigil ≈ 7:05; the battle counts as pay-off) | steps 5 → 9 |
| Timers | every crew, desk and infirmary timer inside the free finish (Age I keep 10 s – 1 m 34 s; production ×0.4, military ×0.6 — progression.md §3, §7); the one long timer is the step-11 muster order | "every tap must produce a result" ([numbers.md](numbers.md) §1) |
| Ceremonies | 4 first-time ones (victory, swearing, house banner, first chest) ≤ 3.0 s each, skippable after 1.0 s — an exception to core-loop A9 (≤ 1.5 s, skip at 300 ms), which repeats follow | four big firsts, not forty small ones |
| Daily orders | the 30-point chest inside session 1: return 10 + 2 constructions 15 + muster 10 + research 10 = 45 (core-loop §7) | the loop is taught by paying it |

- **Free play** after step 12 (median first session 12–18 min, §11): Age I keep levels take 10 s – 1 m 34 s, so the keep reaches L4–5 in minutes and the First Counter trial opens at L4 (progression.md §1). Crews and the desk go idle within a minute of the script; core-loop §2 rule 4's exit rule (0 idle plates) binds from session 2.
- **Push permission** (Android 13+ asks at runtime): our card first; the system dialog only after Yes on it — Android stops showing it after 2 denials, so we never spend one on a "No". Godot 4: `OS.request_permission("android.permission.POST_NOTIFICATIONS")` (declared in the Android export preset, as a custom permission if it has no checkbox); the answer arrives on the `on_request_permissions_result(permission, granted)` signal of `MainLoop` (`get_tree()`). Godot has no push service of its own: the iOS prompt and the device token go through the plugin ship-forge and cloud-forge choose. Declined → one settings card in chapter 2, never the system dialog again.
- **Overlay** (ui-forge): steps 1–2 dim the screen with a full-screen `ColorRect` (INK #1E1712 at 55% alpha) on a `CanvasLayer` above the HUD; a canvas_item shader cuts a rounded hole with a 3 px GILT ring around the one allowed target. The rect keeps `mouse_filter = MOUSE_FILTER_STOP` and its script overrides `Control._has_point(point)` to return `not hole.has_point(point)` (`hole` is a `Rect2`): taps outside are swallowed; the tap inside reaches the button below or, if no Control takes it, the 3D pick (`_unhandled_input` ray, or `CollisionObject3D.input_event` with `Viewport.physics_object_picking` on). From step 3: no dim.
- **Veteran switch**: after the first win, a toggle "Guide: full / brief". Brief hides the cards and keeps the pointer on decisions; every step stays real. D1 is measured per branch (§11).

| Fails when | Caught by |
|---|---|
| First win > 60 s p90, or first input > 15 s p90 on the reference phone | [ ] ftue_probe timing + ship-forge device capture |
| A lord pick loses a first camp, or wins with > 20% of the march wounded | [ ] ftue_probe: 3 picks × 3 camps, `9/9 won` |
| The probe's tap log differs from this table (33 taps, 7 D) in any step | [ ] ftue_probe tap log per step |
| A forced step after 110 s; a card > 14 words; > 90 s of reading; no highlighted action for > 12 s | [ ] ftue_probe forced-step, word and dead-end logs |
| A kill at any step does not resume there with rewards kept | [ ] ftue_probe kill-resume pass (13 steps) |
| An offer, a shop pop-up or a title screen appears | [ ] ux_flow_probe capture per step; `menu_test` stays green |

## 3. The identity choice — whom you swear first

The genre makes a faction choice its first real decision (free to change about a day in) and early
investments later go out of date and are paid to redo ([benchmark.md](benchmark.md) §10). **Our move**:
play first (a win, two buildings), choose at minute 2, and make it safe — the pick decides which lord
comes FIRST, never which you can have.

| Pick | Lord ([portraits.md](../../game-art-director/references/portraits.md)) | Brings (t1 — t2 opens at keep L3, [progression.md](progression.md) §6; equal power, [numbers.md](numbers.md) §3) | The line's first lesson |
|---|---|---|---|
| The shield | Edwin — older infantry lord, crimson mantle | a batch of Peasants (infantry t1) | holds the front |
| The bow | Elena — archer lord, green hood | a batch of Hunters (archers t1) | strikes first, from range |
| The spur | Rowan — young cavalier, plume and kite shield | a batch of Peasant Outriders (cavalry t1) | fastest march |

1. **Reswear**: free, once per 24 h, until 168 h after founding. Lord XP and levels move 100% to the new first lord; Seals spent on the old lord's skills come back as Plain Seals 1:1 ([lords.md](lords.md) §10); talent points reset free (lords.md §7); crafted pieces stay (any lord may wear any piece, lords.md §9 rule 1); the starter batch stays.
2. **Chapter 4** gives a SECOND lord: the player picks one of the two not sworn (§6). Other lords follow [lords.md](lords.md) §11 acquisition; every lord has a free path (SKILL.md rule 6).
3. The pick's only gameplay effects: one batch of troops and which lord leads first. No permanent percentage bonus hangs on it. The house sigil (step 9) is cosmetic: 6 at founding, changeable any time for free.
4. Each starter owns one of the six four-piece sets (Edwin's, Elena's, Rowan's — lords.md §9; Faber and Fable have none): swearing unlocks its 4 patterns, so chapters 4 and 7 can craft and temper the sworn lord's pieces.

| Fails when | Caught by |
|---|---|
| One pick's D1 is > 5 pp below the others (a trap option) | [ ] D1 by `sworn_first` (§11) |
| A pick is chosen by < 15% (dead) or > 60% (no-brainer) of players | [ ] pick-share telemetry, weekly |
| Reswear loses a single XP point, Seal or resource | [ ] unit test: invest → reswear → totals equal |

## 4. Newcomer safety — the King's Peace and safe PvE

The genre starts new castles under a shield [duration unverified] that the player's own attack breaks,
so a learner who fights loses protection [derived] ([benchmark.md](benchmark.md) §10). **Our move**: PvE
never breaks the ward; it lasts long enough to learn defence; the garrison lesson comes before it ends;
the map shows it. Working name "the King's Peace": it binds lords, not raiders.

| Dial | PROPOSAL | Why |
|---|---|---|
| Length | 168 h (7 d) from founding | all 7 chapters open by 120 h (§6), + 2 days to use them |
| Warnings | −24 h and −1 h; the garrison lesson fires at −24 h if not done; push only if allowed | nobody learns about the end from a battle report |
| Ends early by choice | "Lay down the peace": 2 taps + confirm | players who want war are not held back |
| Ends early by growth | realm older than 14 d AND the player enters the realm's top 30% by power → ends 24 h later, with a notice | a fast spender in an old realm cannot grow behind the ward |
| Once | never restored, never sold ([monetization.md](monetization.md) §3 red line 7) | a ward on sale is a shield on sale |

| # | Action | Under the King's Peace |
|---|---|---|
| 1 | Attack, scout or rally a player's castle; join a rally on a player | **breaks it**, after a confirm showing the time left ("Ends your peace — 4 d 06 h left"); scouting too ([combat.md](combat.md) §11 rule 2) |
| 2 | Attack a player's march, or a landmark, standard or Hall held by players | **breaks it** — both fight players' troops |
| 3 | Camps, AI lords, rally-only strongholds, gathering, seat moves | allowed, ward kept (combat.md §6 rows 1–2: 0 dead; the ward survives seat moves, [world.md](world.md) §9) |
| 4 | Reinforce an ally; defend an alliance structure | allowed, ward kept; the march fights under combat.md §6 row 4 (15% dead) — the ward covers the castle, not troops sent out |
| 5 | Players attacking or scouting the warded castle; AI raids | rejected server-side; the only AI raids are step 1 and chapter 6 ([world.md](world.md) §6) |
| 6 | Players attacking the warded player's marches | rejected on camps, strongholds and nodes of level ≤ 2 (world.md §10); allowed on higher nodes, and the send card says "Outside your peace" (icon + words) — the ward is not a gathering shield for farm accounts |
| 7 | Starting any ward while a hostile march is on the road | never ([combat.md](combat.md) §9); binds the return ward (§8) — the King's Peace starts at founding |

- **Map signal**: the ward dome at region zoom, the warded icon at realm zoom ([world.md](world.md) §13) and the word "Warded" on the castle card (shape + word, never colour alone); no countdown for others; the owner sees it in the profile and the tracker.
- **Safe PvE in week 1**: camp fights produce 0 dead (combat.md §6 row 1: 90 light / 10 severe); home defence never kills (row 3); the median day-1 camp loss heals inside the 5-min free finish; camp levels open one by one on a win (world.md §4 rule 2).
- **Camp tags** from the deterministic resolver run on the camp's public army: **Easy** = predicted win with ≤ 10% of the march wounded; **Even** = win with 10–40%; **Hard** = predicted loss or > 40% — Hard asks one extra confirm tap in week 1.
- **Other wards** — alliance.md §4's 8 h Merit-store ward, liveops.md's 24 h arrival and 72 h merge wards — are earned (never money or gems) and never extend or restore the King's Peace. PROPOSAL to those files: rows 1–2 are the one break list for every ward (they say "breaks on attack"; scouting should break them too). The Merit item needs a name other than "peace ward" (story-forge).
- **Server**: `ward_end_unix` + `ward_broken` on the castle document; attack and scout validators read them; 0 ticks (SKILL.md rule 5).

| Fails when | Caught by |
|---|---|
| A warded castle is attacked or scouted by a player; a warded account scouts for a main | [ ] ward_test: `WARD OK - 13 rules, 0 leaks` (7 rows above + 6 passage rules, §8) |
| Churn in the 48 h after the ward ends > the cohort baseline + 5 pp | [ ] cohort churn around `ward_end_unix` |
| > 5% of players who break the ward lose ≥ 50% of their troops within 24 h (regret) | [ ] telemetry: break joined to losses |

## 5. The alliance nudge

Members retain; the genre pays premium currency for the first join ([benchmark.md](benchmark.md) §10), a
join reward that also invites hopping. **Our move**: the nudge comes at minute 8, into an alliance that
is awake NOW; the reward is felt within day 1 (help on a real timer) and paid once per account, after helping.

- **The moment** (alliance.md §10 leaves it to this file): step 10 — the house has a name to bring, and the first timer allies can shorten (keep L8–L9) comes within day 1, so helpers are in place before it starts; the Welcome chest's 24 h bar starts at once.
- **The cards**: eligible = alliance.md §10's suggestion filter (same language, activity overlap ≥ 50%, open seats, auto-accept on, ≥ 60% of members active in 72 h). Onboarding adds two exclusions: no officer active in 48 h; > 3 newcomers (< 7 d old) released in 7 days. The 3 best by `score` below; each card shows members online now, the median time to a first help (last 24 h), and the alliance's land on the map. Invite installs: §8.

```
score = 0.50·min(active_15m / 5, 1)          # members active in the last 15 min
      + 0.30·min(helps_per_request_24h / 10, 1)
      + 0.20·activity_overlap                  # alliance.md's overlap with the player's hours, 0–1
```

- **The first helped timer (the felt reward)**: Age I timers sit inside the free finish, so the first request allies can shorten is keep L8 (8 m 28 s) or L9 (14 m 50 s) ([progression.md](progression.md) §7), reached in free play or session 2 of day 1 (Age II at day 0.3, progression.md §9). Help is auto-asked (core-loop A4); alliance.md §3's join hook keeps the request on top of every ally's list for 24 h (first help ≤ 15 min). With `H = 10`, `f = 120 s`: L9's 14 m 50 s → 5 helps → 4 m 50 s = free finish; L10's 26 m 03 s → 6 m 03 s after 10 helps (progression.md §7 table). Next digest: "Allies saved you 10 m on your keep".
- **The Welcome chest** (alliance.md §10: once per account; opens after 24 h in the alliance AND 5 helps given). Onboarding shows it sealed at join with its two bars — a visible next goal that teaches helping. Its gem part (the "join purse", worth 1 h Universal) is an owner decision (alliance.md §16).
- "Later" is always a choice. The nudge returns at session 2 and in chapters 1 and 3 — at most once per session, never as a blocking modal after the first — plus alliance.md's daily digest line ("An alliance would have saved you 34 m today"). Chapter 3's chest is the alliance's welcome: a solo player loses that one chest, nothing else.
- **Newcomer gift** ([alliance.md](alliance.md) §6): a member < 7 days old who closes chapter 3 and stays 72 h sends every member 5 min of own output; ≤ 10 per alliance per week — alliances gain from recruiting, alt accounts do not.

| Fails when | Caught by |
|---|---|
| > 30% of first helped requests get < 5 helps within 30 min | [ ] telemetry `first_request_helps_30m` |
| > 5% of joiners are released by the suggested alliance within 72 h | [ ] telemetry; exclusion rule above |
| The Welcome chest or a newcomer gift pays twice for one account | [ ] alliance.md hop_exploit_test |

## 6. The founding week — seven chapters

The genre runs an 8-day new-server event that unlocks new tasks daily ([benchmark.md](benchmark.md) §10).
**Our move**: chapters follow the PLAYER's account age (late joiners get them too); a missed day is
never lost; systems open by progress — a chapter only adds tasks, a chest and a lesson.

1. Chapter N opens at founding + (N − 1) × **20 h** (0, 20 … 120 h) — 20, not 24, so a player who returns at about the same hour each day always finds the next one open. All stay open until day 14.
2. 5 tasks, chest at **4 of 5**, "Open" = 1 tap. Chapters are milestones, not points — never a second point system ([core-loop.md](core-loop.md) §1 rule 2).
3. Every task is an action the daily loop already asks for, or a first-time moment (§7); never "open the shop", "spend gems", "watch" or a clock time; extra effort ≤ 1.5× one day's orders (a task the orders already pay counts 0).
4. **The arc follows the gates, never the reverse**: if [progression.md](progression.md) opens a system later for the median free player, the chapter shows its tasks without it and the lesson fires at the real unlock.
5. **Chapters and the Founding**: in a realm's first 7 days its Founding races ([liveops.md](liveops.md) §2, by realm age) run beside the chapters (by account age): races are the realm's competition, chapters the player's lessons. ONE rail icon ("The Founding", two tabs); one action counts for both — never two lists asking for different chores. liveops.md's "guided that day" column is met by the FTM rules (§7): a lesson fires once, when the system is usable.

| Ch. (opens) | Working name | Lesson (§7) | Tasks (chest at 4 of 5) | Chest (week-1 values) | Next hook |
|---|---|---|---|---|---|
| 1 (0 h) | The Stockade | first battle, first zoom-out (§2); First Counter trial at keep L4; talents at lord level 10 | swear a lord · clear 3 camps · keep to level 5 · muster 2 batches · join an alliance | 1 h Universal + 3 h own output + lord XP | "The land opens" |
| 2 (20 h) | The Land | hunt order; gathering banner | 1 gathering march · 1 hunt of 5 camps · "Scout the frontier" once ([world.md](world.md) §7) · start 2 research · 2 check-ins ≥ 2 h apart | 3 h Works + 50 Resolve + 5 Plain Seals | "Your banner calls" |
| 3 (40 h) | The Banner | alliance land | help 10 times · claim an alliance gift · donate to a charter · move next to allies (free, once) · gather once on alliance land | 3 h Universal + 5 Plain Seals (+ the newcomer gift, §5) | "A second lord rides in" |
| 4 (60 h) | The Lord's Road | set piece; pairing when the chest's lord arrives | sworn lord to level 25 · raise 1 skill · craft the first piece of the lord's set at the smithy (30 m, lords.md §9) · equip it · 1 hunt of 5 camps | the SECOND LORD: 1 of the 2 not sworn (§3) + 3 h Muster | "Strongholds need many banners" |
| 5 (80 h) | The Rally | first rally, join and lead | join 1 rally or pass Join the Banner · lead 1 rally (Crown columns fill it if allies are offline, world.md §5) or pass The Muster (progression.md §1) · hunt 5 camps · heal all · muster 3 batches | 8 h Works + 3 h own output + 5 Plain Seals | "Walls before the peace ends" |
| 6 (100 h) | The Wall | garrison + the raid on the walls | set the garrison pair · win the raid on the walls · repair the wall once ([combat.md](combat.md) §10) · reinforce an ally once · upgrade the watchtower | 3 h Muster + 50 Resolve + 5 Plain Seals | "The whole realm, and its season" |
| 7 (120 h) | The Realm | seasons (kept / reset); war windows | read the season card · 1 bout in the Lists · 1 war-window action or 1 rally · chart 80% of the home region (world.md §7) · the 100-point daily chest on 3 days | one set piece tempered to **Sound** + 8 h Universal + 10 Plain Seals + a **banner charge** (cosmetic, seen on the map) | the weekly writ and the season track |

Chapter hourglasses total 29 h on top of core-loop's chests and writ; the 30 Plain Seals ARE
lords.md §11's "new-realm week" line, given by account age so late joiners get them too. Check the
hoarding line (held ≤ 2× queued at day 30, [core-loop.md](core-loop.md) §5). `tools/econ_sim.py` has
no time-window field (a line is `per` day, minute or session): model chapter rewards and the Welcome
chest as `per: "day"` lines of total ÷ 7 in a separate week-1 run with `--days 1,7`; keep them OUT of the day-30 model.

| Fails when | Caught by |
|---|---|
| A player who returns at the same hour daily finds a chapter locked | [ ] unit test: 20 h cadence over 7 days, arrival ±2 h |
| A task maps to no core-loop step or first-time moment (busywork) | [ ] task table vs [core-loop.md](core-loop.md) §8.2 |
| < 60% of day-7-active players close ≥ 6 of 7 chapters | [ ] telemetry per cohort |
| A solo player cannot close a chapter other than chapter 3 | [ ] table check: ≤ 1 alliance-only task per chapter (3 excepted); trials count for rallies |

## 7. First-time moments — teaching the late systems when they open

The genre's tutorial ends at the map view and chapter quests [observational]; the systems that decide
who stays (rallies, garrisons, war seasons, talent planning) are learned from video sites
([benchmark.md](benchmark.md) §10). **Our fix**: a first-time moment (FTM) fires when a system opens AND
the player can use it now, and teaches it with a real action.

1. **Trigger** = unlock + a usable situation (an open rally, a talent point in hand). Not triggered within 72 h of the unlock → it becomes a chapter task or opens as its Trial stage (rule 5), with the same reward.
2. **Size**: ≤ 90 s, ≤ 8 taps, ≤ 3 cards of ≤ 14 words; skippable after 3 s; never forced twice; never for a system already used (its counter in the save > 0).
3. It shows **the one number that decides the system**, in the player's own situation ("this rally leaves in 4 m 12 s; 3 of 5 banners filled").
4. **Spacing**: none during the §2 script (the script is the lesson); one at a time; none within 10 min of another FTM or a ceremony, none in a war window's Engage phase ([core-loop.md](core-loop.md) §8.3); queued ones fire at the next quiet moment.
5. **Practice and replay**: when an FTM fires or is skipped, the matching Trial Grounds stage ([liveops.md](liveops.md) §4.5: fixed armies, loss-free, one-time reward) opens as its practice, with a 20–40 s replay card beside it, forever. The FTM itself stays a real action (§1 rule 2): the trial is the practice, not the lesson (liveops.md §4.5's "opens as the guided moment" reads this way).
6. The first run is tuned to succeed (target ≤ 60% of the player's strength) and pays the normal reward; nothing is handed back artificially afterwards.
7. **Three lesson surfaces, one job each**: the FTM is the first real use; the Age Trial ([progression.md](progression.md) §1: keep-gated, loss-free, AI lords fill a solo rally) proves the skill before the next age; the Trial Grounds stage is the replayable practice. Where an Age Trial covers the system (join a rally L9, garrison L14, lead a rally L19, the equal-troops bout L24), the FTM fires at whichever comes first — the real situation or the trial — and never twice.

| FTM | Fires when | The real action | The one number shown | Taps | Works if (unaided use ≤ 7 d after) |
|---|---|---|---|---|---|
| Hunt order | session 2: Resolve ≥ 50 and ≥ 5 camps in range | one march, up to 5 camps | 10 Resolve per camp; bar full again in 10 h | 4 | ≥ 70% send a hunt |
| Gathering banner | chapter 2 opens and a banner is idle | a march to a level-1 node | the node's load and return time; "your peace covers nodes ≤ level 2" | 4 | ≥ 70% gather again |
| Join a rally | an alliance rally in its join window, or the L9 Age Trial | join with a preset march | the join countdown and the filled banners | 4 | ≥ 50% join again |
| Lead a rally | first rally-only stronghold in range, or the L19 Age Trial | lead; allies join, or world.md §5's Crown columns fill it (a leader's first 3 stronghold rallies) | capacity and the damage-share reward | 6 | ≥ 30% lead again |
| Garrison | chapter 6 opens (100 h) or the L14 Age Trial; at the latest 24 h before the ward ends | set the garrison pair; the raid on the walls | who defends first (stand-ins if unset, [combat.md](combat.md) §9); free infirmary beds | 6 | ≥ 80% have SET a garrison pair at ward end (stand-ins do not count) |
| Reinforce an ally | an ally's attack warning (or chapter 6) | send a march to the ally | arrival ETA vs attack ETA | 4 | ≥ 30% reinforce again |
| First defeat | first lost battle | the report's ranked cause (report-forge) + one next-step button | the cause's number ("their spearmen: counter vs your cavalry") | 3 | next attack on that target class wins ≥ 60% |
| First attacked by a player | first player attack after the ward | infirmary, protected resources ([economy.md](economy.md) §7), ask for help | lost vs protected; hours to recover | 4 | ≥ 70% active 48 h later |
| Infirmary near full | beds ≥ 80% filled | heal all; the bed count | free beds; overflow at 100%: camps → light, home → routed, field → dead (combat.md §6) | 3 | overflow deaths in week 2 ≤ 5% of players |
| Alliance land | in an alliance whose land exists, chapter 3 | move next to allies (free, once) and gather inside | the gathering bonus inside and the march time to the Hall ([world.md](world.md) §8) | 4 | ≥ 60% of members inside the land by day 7 |
| Lord pairing | chapter 4's chest brings the second lord | field both in one march | only the PRIMARY's talents and gear count ([lords.md](lords.md) §8) | 5 | ≥ 60% field a pair |
| Talents | lord level 10 (first hour; 9 points waiting, lords.md §4) | spend them; the path for the lord's role is lit | 34 points, 3 branches, 1 capstone; resets always free (lords.md §7) | 4 | ≥ 70% spend all points |
| Set piece | first piece of a lord's set | equip it | the 2-/4-piece set bonus and what is missing | 3 | ≥ 60% equip a 2nd piece |
| Second desk | the second research desk opens (Age IV) | start a 2nd research | both desks' end times | 3 | 2 desks busy at ≥ 70% of exits |
| Siege engines | the siege workshop stands (combat.md §4, siege-forge) | build one engine | its effect on walls vs troops | 4 | ≥ 30% field one |
| War window | the −10 min call of the first window after the ward | the 30-min shape: muster, scout, engage ([core-loop.md](core-loop.md) §8.3) | the window's end time and the alliance's objective | 5 | ≥ 40% act in a 2nd window |
| Season | the first season start the player lives, or chapter 7 | the season card: two columns KEPT / RESET + the track | days left; what resets (holdings, scores, the track — [liveops.md](liveops.md) §3.6) and what never does (city, troops, lords, gear, items, resources) | 2 | season-week-1 churn ≤ the previous week's + 2 pp |

| Fails when | Caught by |
|---|---|
| Two FTMs in one 10-min window, one in an Engage phase, one > 90 s or > 8 taps | [ ] ftm_probe: `FTM OK - 17 moments, 0 repeats, 0 blocked > 3s` |
| An FTM fires for a system already used, or its Trial stage does not open | [ ] ftm_probe on crafted saves |
| Unaided use below the "works if" line for 2 weeks | [ ] telemetry → rewrite that FTM (the lesson failed, not the player) |

## 8. Late joiners — routing, the newcomer's passage, returners

The genre opens new servers in pairs about every 12 h (about every 30 h later [unverified]) and lets
beginners move to a newer one within 10 days while the spine is low; after that window they are stuck
([benchmark.md](benchmark.md) §10). **Our move**: one routing rule, one free passage, catch-up by progression.

| Case | Route | Help |
|---|---|---|
| Fresh install, with or without an invite | the newest open realm, automatically, no realm menu ([liveops.md](liveops.md) §1.1, canonical: one router rule, no exception; registration closes at 21–35 days, so nobody lands in an older realm) | the Founding races if the realm is ≤ 7 days old; step 6 names the realm and its age |
| Invite link | same placement; at step 10 the friend's card comes first — "Ride to <friend> in <realm>": the passage below + the friend's alliance (if it has a seat) in one tap | settled ground ([progression.md](progression.md) §10) in an older realm |
| Warded player, days 1–7 | the newcomer's passage (below; liveops.md §7 rule 1 points here) | ward and chapters continue |
| Realm emptying | liveops.md §8 merges; the Writ of Passage (liveops.md §7) | — |
| Archived castle comes back ([world.md](world.md) §15 A8), or ≥ 14 d away | a "what changed" digest of ≤ 5 lines; a 24 h **return ward** (PROPOSAL), once per 60 d, §4 rows 1–2 and 7 apply; an unexpired King's Peace just continues | open FTMs re-queue |

**The newcomer's passage** (PROPOSAL; owned here; [world.md](world.md) §9 lists it as a seat move):
1. Once per account, free, never sold (monetization.md red line 7); the player chooses it — liveops.md §1.1 keeps realm choice to passage flows.
2. Only while the King's Peace holds (≤ 168 h, unbroken): refused after a break.
3. Destination: a realm with registration open (liveops.md §1.1), or a friend's realm of any age (invite link or friend list).
4. Blocked with a hostile march on the road, an own march out, or in a war window (world.md §9 rule 1); liveops.md §7 rule 3c's power test (≤ 1.5 × the destination's 90th-percentile active power) guards younger realms.
5. **Feeder guard**: resources travel only up to the warehouse allowance `Wp` ([economy.md](economy.md) §7, F11) — else alt accounts gather safely under the ward, then move to a main's realm. liveops.md §7 rule 5 ("resources in full") must name this exception.
6. Everything else travels; `founded_unix`, `ward_end_unix` and the chapters stay; alliance membership ends under [alliance.md](alliance.md) §11.

| Fails when | Caught by |
|---|---|
| A fresh install lands anywhere but the newest open realm; an invite install does not get the friend's card first at step 10 | [ ] route_test: `ROUTE OK - 1000 installs, newest open 1000/1000, invites 200/200 friend card first` |
| A passage after a ward break, twice, with an attack inbound, or carrying more than `Wp` | [ ] ward_test passage rules |

## 9. Return hooks in week 1

| Hook | Rule |
|---|---|
| Exit line | from session 2, every session ends on "All busy — first free at HH:MM" ([core-loop.md](core-loop.md) §2 rule 4) and names the next chapter in ≤ 6 words; session 1 ends on step 12's Next card |
| Day-1 return | the step-11 muster order ends in 1, 3 or 8 h (the player's pick); Resolve refills 10 per hour toward the hunt order (≥ 50); keep L6 waits on the First Counter trial (progression.md §1) |
| Push | only after the opt-in; ≤ 3 per day in week 1 (core-loop A8 allows 4); never for offers; declined → one settings card, no e-mail, no nagging |
| Digest at open | ≤ 3 lines: helps received, finished work, the next chapter's countdown |
| Account safety | the guest account is offered a link (store account or e-mail, cloud-forge) in chapter 2 or before a first purchase — never in the first 10 minutes; a lost guest castle is a lost player |

## 10. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md) §10, §13) | Our fix | Number |
|---|---|---|
| The tutorial never teaches the systems that decide retention | first-time moments at unlock, with a real action | 17 FTMs, ≤ 90 s each |
| Early investments go out of date and cost money to redo | play first, choose at minute 2; free reswear for 7 d; talent resets always free (lords.md §7) | 0 paid redo in week 1 |
| The shield breaks on the learner's own play | PvE never breaks the ward; garrison lesson before it ends; 0 dead in week-1 PvE; confirm with time left | 168 h |
| A free second builder that expires after 2 days; a cheap offer early | 2 crews from minute one, never sold ([core-loop.md](core-loop.md) §2); no pop-up offer in 72 h ([monetization.md](monetization.md)) | 0 pop-ups in 72 h |
| Too many event icons in week 1 | the chapters and the realm's Founding share ONE rail icon | 1 icon, not 2 ([ux.md](ux.md) owns the cap) |
| A premium reward for joining feeds alliance-hopping | one Welcome chest per account, opened only after 24 h and 5 helps given ([alliance.md](alliance.md) §10) | 1 per account |
| Late starters trapped in old realms | automatic routing to the newest open realm, the passage, catch-up | 1 free move in 7 d |

## 11. Metrics — the FTUE funnel and retention (PROPOSAL; replace with cohort baselines)

"Tutorial complete" = step 12 reached, reported for session 1 and within 24 h. Reach = % of first
launches. **Red line**: one step losing > 3 pp against the step before is a red finding; > 5 pp blocks
a release. Joining an alliance is a choice, reported beside the funnel, not in it.

| Step | 0 castle frame | 1 first win | 3 lord sworn | 7 battle won | 9 house named | **12 complete** | 10 alliance (choice) |
|---|---|---|---|---|---|---|---|
| Reach | ≥ 98% | ≥ 96% | ≥ 92% | ≥ 89% | ≥ 86% | **≥ 82%** session 1, ≥ 88% in 24 h | ≥ 55% session 1, ≥ 70% by chapter 3 |

| Retention and health | Target |
|---|---|
| D1 / D7 / D30 ([numbers.md](numbers.md) §8) | ≥ 40% / 15–20% / 6–10% |
| D1 of tutorial completers | ≥ 50% |
| D7 of day-1 alliance joiners vs solo players | ≥ 1.5× |
| First session length (median) · sessions on day 1 | 12–18 min · ≥ 3 for half of the completers |
| Push opt-in (of those asked) · crash-free FTUE sessions | ≥ 55% · ≥ 99.5% |

- **A/B rule**: one dial per test; the arm is `ftue_version`, fixed by a hash of the account id at first launch. To detect a D1 change of **3 points** (40% → 43% or 37%), two-sided α = 0.05, power 0.80: `n = (z₀.₉₇₅ + z₀.₈₀)² · (p₁q₁ + p₂q₂) / δ² = 2.80² · (0.240 + 0.245) / 0.03²` ≈ **4,230 installs per arm** (8,460 in all). 5 points ≈ 1,530; 2 points ≈ 9,490; power 0.90 at 3 points ≈ 5,660; three arms (Bonferroni, α 0.025 per comparison) ≈ 5,120 per arm. A ±3-point confidence interval on ONE arm needs only ≈ 1,025 — it cannot tell two arms apart. Duration = installs ÷ installs per day + 1 day for D1 to close (2,000 a day → ≈ 5 days). Fix n before the start and read once: daily peeking inflates α.
- **Telemetry**: one `ftue_step` event per step {step, ms since first input, taps D/M}, buffered on the client, sent in ≤ 3 batched writes per session (cloud-forge).

## 12. Harness, data, save migration, server cost

| Proof | Measures | Verdict line (PROPOSED — qa-forge fixes the wording) |
|---|---|---|
| `ftue_probe` (new, windowed 1080×1900; path to confirm) | fresh account on a test realm; 13 steps × 3 lord picks × 3 first camps; timings, tap log, words, dead-ends, kill-resume | `FTUE OK - first win 32s, 33 taps (7 decisions), 9m40s, 9/9 first camps won, 0 dead-ends` |
| `ward_test` (new, headless) | the 7 action rows of §4 and the 6 passage rules of §8 | `WARD OK - 13 rules, 0 leaks` |
| `route_test` (new, headless) | 1,000 synthetic installs, 200 of them with invites | `ROUTE OK - 1000 installs, newest open 1000/1000, invites 200/200 friend card first` |
| `ftm_probe` (new, headless, crafted saves) | 17 FTMs: fire once, spacing, skip ≥ 3 s, Trial stage opened | `FTM OK - 17 moments, 0 repeats, 0 blocked > 3s` |
| `core/session_audit.gd` from a FRESH save; `ux_flow_probe`, `ux_touch_probe`, `a11y_audit`, `layout_audit`, `w1f_aspect_sweep` | the script inside the full session; touch targets; +40% text; 6 screen shapes | existing lines; `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| `core/sd_cost_probe.gd` | writes per new player | inside the €200/month budget |

- **Data** (`data/onboarding.gd`, path to confirm): the step, chapter and FTM tables; the founding castle list (§2). **Save fields**: `ftue_step:int`, `ftue_version:int`, `founded_unix:int`, `ward_end_unix:int`, `ward_broken:bool`, `sworn_first:String`, `reswear_next_unix:int`, `passage_used:bool`, `return_ward_unix:int`, `chapters:Dictionary`, `ftm_done:PackedStringArray` (the Welcome chest keeps its flag in alliance.md data).
- **Save migration**: existing saves load with `ftue_step` = done when the spine is past its first level or any battle is won; chapters marked done by the counters they already hold; FTMs marked done where the counter is > 0 (unseen ones still fire once); no King's Peace for existing castles and `passage_used` = true; `founded_unix` = first save time, else load time.
- **Server cost** (estimate; measure): first session ≈ 13 writes (1 account + 1 house name and sigil + ≤ 4 step saves + ≤ 3 telemetry batches + 1 join + 1 muster order + 1 chest claim + 1 push token) + 1 routing read; week 1 adds 7 chapter claims + 1 Welcome chest ≈ **21 writes per new player**. At `I` installs per day ≈ `21·I` writes per day — 2,000 installs ≈ 42,000 writes, ≈ 1.5% of core-loop §11's 2.9 M. The ward is two fields read at attack time: 0 ticks.

## 13. Handoff to onboarding-forge

Every onboarding change lands first as `design/onboarding/SYSTEM.md` from [spec-template.md](spec-template.md);
its §13 compares these targets with the measured funnel.

| Deliverable | Owner (one writer per file) | Proof |
|---|---|---|
| Script runner, chapters, FTM triggers, save fields, migration | onboarding-forge | ftue_probe, ftm_probe |
| Overlay, pointer, cards, alliance cards, the replay cards | ui-forge (gauntlet render: blender-forge) | ux_flow_probe, ux_touch_probe, a11y_audit |
| March-out and first zoom-out shots | transition-forge | its frame-time probe: no hitch > 1 frame |
| Raid at the gate, first battle, first rally, raid on the walls | battle-forge (+ gameplay-forge data) | resolver harness; ftue_probe 9/9 |
| The swearing ceremony, lord cards, token rim | commander-forge + feel-forge | frame capture ≤ 3.0 s |
| Ward, routing, the passage, suggestion ranking, new-castle placement | cloud-forge + world-forge | ward_test, route_test, sd_cost_probe |
| Every line, chapter and place name | story-forge + l10n-forge | layout_audit at +40% text |
| Horn, victory and swearing cues · cold start and first frame | audio-forge · ship-forge | cue list · reference-phone capture |
| The four new harnesses | qa-forge | their verdict lines |

**Placement request to world-forge** (PROPOSAL to [world.md](world.md) §4 rule 5, which gives one personal
camp): three personal level-1 camps 4–6 tiles away (25–35 s at `v_ref`), one per main line (infantry,
archers, cavalry — the counter hint), visible to the owner for 24 h; ≥ 3 real castles (once the realm
has them) and, if one exists, an alliance's land inside the 5 × 5 chunks cleared at start (world.md §7 rule 3).

## 14. Owner decisions required

1. The King's Peace: 168 h, the break list (§4 rows 1–2, one list for every ward), and the growth end (top 30% in realms > 14 d old).
2. Free reswear for the first 168 h: XP moved 100%, Seals back as Plain Seals (lord economy; [lords.md](lords.md)).
3. Invite installs follow liveops.md §1.1 (newest open realm) and reach the friend by the passage at step 10; founding straight in the friend's realm would need an exception to §1.1.
4. The newcomer's passage as defined in §8 (friend's realm of any age; refused after a ward break; `Wp` cap).
5. The 24 h return ward, once per 60 d (§8), and three personal first camps (§13).
6. The first-time ceremony exception (4 ceremonies ≤ 3.0 s) to core-loop A9.
7. Names and voice (story-forge canon): the King's Peace, the seven chapter titles, the banner charge, a new name for the Merit-store ward; who speaks the first 10 minutes (the steward helper, onboarding-forge STW — verify; "Steward" is also an alliance office, alliance.md §2; the guide never sells).
8. Privacy consent at first launch if the law requires it (legal): ≤ 2 taps, before step 1, counted in the tap budget; the first-input clock then starts at the consent tap. The year-of-birth screen stays at the first purchase ([monetization.md](monetization.md) §9).
9. Any dial here that collides with a shipped sacred constant (the shipped value wins).

## 15. Reviewing an onboarding spec — checklist

- [ ] First win ≤ 60 s p90; ≤ 40 taps with ≥ 5 decisions, every counted tap named in the step table; ≤ 90 s of reading; forced taps end at 110 s.
- [ ] Every guided step is a real action on the live realm; no title screen; practice only after the real lesson.
- [ ] Every script timer matches progression.md's curve; every lord pick beats every first camp in the harness; reswear refunds 100%.
- [ ] Ward: length, warnings, break list, server rejection, map signal — each with a test.
- [ ] Week-1 PvE: 0 dead; the median day-1 loss heals under the free finish.
- [ ] Alliance cards: alliance.md's filter + the two exclusions + the score; the first helped timer is named with its math; one Welcome chest.
- [ ] Chapters every 20 h, open to day 14, chest at 4 of 5, no busywork, solo-closable (3 excepted), one rail icon.
- [ ] Every late system has an FTM with its trigger, one number and a "works if" line.
- [ ] Routing follows liveops.md §1.1; invites and the passage covered by route_test and ward_test.
- [ ] Funnel targets, red lines and the A/B sample size with α and power in the spec.
- [ ] Save migration named; server cost line with its formula; owner decisions listed.
