# Onboarding — the first ten minutes, the first week, and the lessons the genre never gives

How a new player goes from the first tap to a named house with a sworn lord, an alliance and a
first rally — and how every LATE system is taught at the moment it opens, not on a video site.
Implementation: **onboarding-forge** (script runner, chapters, first-time moments, save fields),
**ui-forge** (overlay, pointer, cards), **transition-forge** (march-out and first zoom-out),
**battle-forge** (raids, first battle, first rally), **commander-forge** (the swearing),
**cloud-forge** + **world-forge** (peace ward, placement, realm routing), **story-forge** +
**l10n-forge** (every line), **feel-forge** / **audio-forge** (ceremonies, cues), **qa-forge**
(harness). Genre patterns: [benchmark.md](benchmark.md) §10.

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Shipped values in
`data/*.gd` (paths to confirm) win; a collision with a sacred balance constant becomes an owner
proposal (§14). Dials shared with other references are quoted, never redefined: plates, free
finish (5 min), help `max(1%·R, 120 s)` with `H = 10` for a new alliance, Resolve, daily orders —
[core-loop.md](core-loop.md); spine stages `S1–S6` — [progression.md](progression.md); loss
buckets — [combat.md](combat.md); lords — [lords.md](lords.md); map — [world.md](world.md).

## 0. The four questions

- **Want**: minute 0–10: a win, two buildings, a sworn lord, a first camp cleared, the realm seen,
  a named house. Week 1: an alliance, a second lord, a first rally, a set piece, a garrison.
- **Obstacle**: in the first 10 minutes only a tap — every timer is under the free finish. From
  day 2 the core-loop plates. Other players are no obstacle for 7 days (the peace ward, §4).
- **Wait**: first win ≤ 60 s; first session ≈ 10 min scripted + free play; the exit hook ends in
  15–60 min; one new chapter every 20 h.
- **Witness**: the house banner and name on the realm map (minute ≈ 7); "<house> joined" in the
  alliance feed; the sworn lord's gilt rim on the map token; the Founder title after chapter 7.

## 1. Rules of the first week

1. **The live realm from second 0.** No title menu, no tutorial island, no practice world: the
   first raid hits the player's real castle at its real place on the realm map.
2. **Every guided step is a real action with a real result.** No sandbox with fake rewards — a
   player who learns that tutorials are fake skips every later lesson.
3. **Wins are guaranteed by data, not by a cheat flag.** Scripted fights run through the real
   resolver (gameplay-forge) with fixed armies sized so all three lord picks win (§12 harness).
4. **Forced taps only in the first 110 s** (steps 1–2 of §2). After that the pointer suggests;
   the player may wander; a "Next" card in the queue tracker holds the path.
5. **Text budget**: ≤ 12 cards in 10 min, ≤ 14 English words per card, ≤ 2 lines at 1080 px
   width after the +40% l10n expansion; ≤ 90 s of reading in total. Never a card over a decision.
6. **Idle rule**: no input for 12 s → the pointer pulses; 30 s → the line repeats once; a decision
   is never auto-advanced.
7. **No purchase prompt inside a guided step, and no offer pop-up before day 2** (§14). The shop
   stays reachable — never hidden, never pushed.
8. **Resume at the step**: app killed, call received, crash → the next launch resumes at the last
   finished step with every reward kept. Steps 1–4 run on a flaky connection and sync after; from
   step 5 (realm) "Reconnecting…" ≤ 10 s, then a retry card — never a silent freeze.
9. **ART SHOWN BIG**: lord portraits ≥ 30% of screen height at the pick, ≥ 60% at the swearing;
   building cards show the next tier render at ≥ 40% of screen height ([core-loop.md](core-loop.md) §8.2).
10. **One-hand**: every guided tap sits in the bottom 60% of a 1080×1920 portrait screen; the
    pointer is a gilt hand (GILT #C9A04C outline plus shape), never a relationship colour
    ([ux.md](ux.md)). Every icon on the path is Blender-made art, never a line glyph.

## 2. The first ten minutes, step by step

Clock = p50 on the reference phone (ship-forge names it), from the tap on the app icon. Taps
counted as in [core-loop.md](core-loop.md) §8: **D** = decision, **M** = maintenance/guided.

| # | Clock | Step | What the player does and sees | D/M | Done when | Owners |
|---|---|---|---|---|---|---|
| 0 | 0:00–0:08 | Cold start | painted keep vignette, one ≤ 10-word line, → the castle at dawn, 2.0 s camera push-in; account created silently (guest), locale from device | 0/0 | castle frame ≤ 8 s p50, ≤ 15 s p90 | ship-forge, cloud-forge |
| 1 | 0:08–0:40 | **FIRST WIN**: raid at the gate | "Raiders at the gate. Sound the horn." → volley beat (8 s) → "Open the gate." → the levy charges (10 s) → rout; the raiders' cart counts into the resource bar (800 ms, collected with 0 taps) | 0/2 | victory banner ≤ 60 s p90 after first input | battle-forge, feel-forge |
| 2 | 0:40–1:50 | **FIRST BUILDS**: two crews | plot → farm card → Build (5 s); "You have two crews." → plot → lumber (10 s); both finish by themselves (auto-complete) | 1/3 | two buildings produce | castle-forge, ui-forge |
| 3 | 1:50–3:00 | **FIRST LORD**: the identity choice (§3) | a rider at the gate; three lords; tap one → role card → Swear; gilt rim ceremony ≤ 3.0 s (first time only) | 1/1 | `sworn_first` set | commander-forge |
| 4 | 3:00–3:40 | First muster | the sworn lord's line yard → muster 20 (20 s → Finish free) | 0/2 | batch in the yard | gameplay-forge |
| 5 | 3:40–4:10 | Choose a target | "Raiders' camp to the east." → March → three level-1 camps tagged Easy; one pre-selected → Send (lord preset automatic) | 1/2 | march leaves | world-forge, battle-forge |
| 6 | 4:10–5:10 | **FIRST ZOOM-OUT** | the camera follows the march through the gate and pulls back to region zoom (≤ 3.5 s first time); card: "Other lords' castles. Real players."; neighbours, an AI lord's hold, camps, one alliance's land; the march walks 25 s | 0/0 | region zoom reached | transition-forge, world-forge |
| 7 | 5:10–6:00 | **FIRST BATTLE** | beats 20–30 s at 1× (skippable after 3 s, 2× speed); report headline in 1 s naming the resolver's top cause (e.g. "Victory — your archers out-ranged their axemen."; words by report-forge); one casualty line (returned / infirmary / dead) | 0/1 | camp cleared; lord level 2 | battle-forge, report-forge |
| 8 | 6:00–6:50 | Home and infirmary | Castle (zoom-in ≤ 700 ms) → infirmary bubble → Heal all → Finish free | 0/3 | infirmary empty | ui-forge |
| 9 | 6:50–8:00 | **SPINE + HOUSE NAME** | keep bubble → Upgrade → Finish free; the house banner rises: sigil (1 of 6) + name (a suggested name pre-filled; accept = 1 tap) | 2/3 | banner visible on the realm | castle-forge, story-forge |
| 10 | 8:00–9:00 | **ALLIANCE NUDGE** (§5) | card with 3 recommended alliances → Join → the join purse opens | 1/2 | member (or "Later") | ui-forge, gameplay-forge |
| 11 | 9:00–9:40 | Set everything running | tracker → keep upgrade 14 min (help auto-asked) + farm 6 min + first research → daily orders open with the step points already counted → Open (30 chest) | 1/7 | 0 idle plates | ui-forge |
| 12 | 9:40–10:00 | **EXIT HOOK** | "Tell you when the keep is done?" → Yes → system dialog (its Allow tap is the OS's, not counted); "All busy — first free at 14:20. Next: the land opens." | 0/1 | hook shown = **tutorial complete** | onboarding-forge |
| | | **Total** | | **7/27 = 34** | | |

Budgets for the whole script:

| Budget | Number | Why |
|---|---|---|
| First input | ≤ 8 s p50, ≤ 15 s p90 after the icon tap | every second of black screen before a tap costs installs |
| First win | ≤ 60 s p90 after the first input (target 32 s p50) | the brief's bar; a win before any reading |
| Taps | ≤ 40, of which ≥ 5 decisions | a script of only guided taps teaches nothing |
| Longest stretch without a decision | ≤ 3.5 min (battle viewing counts as pay-off) | steps 5 → 9 |
| Timers | every one ≤ 5 min (free finish) until step 11 | "every tap must produce a result" ([numbers.md](numbers.md) §1) |
| Ceremonies | first-time ≤ 3.0 s, skippable after 1.0 s; repeats follow core-loop A9 (≤ 1.5 s) | four big firsts, not forty small ones |
| Daily orders reached | the 30-point chest inside session 1 (steps 1–11 earn 45 points) | the loop is taught by paying it |

**Push permission** (Android 13+ asks at runtime): our own card first; the system dialog only
after the player taps Yes on it — Android stops showing the dialog after 2 denials, so we never
spend one on a "No". Godot 4: `OS.request_permission("android.permission.POST_NOTIFICATIONS")`,
answer on the `on_request_permissions_result` signal (`MainLoop`, reached as `get_tree()`). Declined → a settings card on day 2, never
the system dialog again.

**Overlay** (ui-forge): the forced steps dim the screen with a `ColorRect` on a `CanvasLayer`
above the HUD; the dim overrides `Control._has_point()` to return `false` inside the hole, so the
one allowed tap passes through to the button or the 3D pick underneath. From step 3 no dim.

**Veteran switch**: after the first win a small toggle "Guide: full / brief". Brief hides the
cards, keeps the pointer on decisions; every step stays real. Measure D1 per branch (§11).

| Fails when | Caught by |
|---|---|
| First win > 60 s p90, or first input > 15 s p90 on the reference phone | [ ] ftue_probe timing + ship-forge device capture |
| A lord pick loses the first battle, or wins with > 20% of the march wounded | [ ] ftue_probe runs all 3 picks: `3/3 won` |
| A dim/forced step after 110 s; a card > 14 words; > 90 s of reading | [ ] ftue_probe forced-step log and word count |
| A dead end: no highlighted action for > 12 s | [ ] ftue_probe dead-end log |
| Kill at any step does not resume at that step with rewards kept | [ ] ftue_probe kill-resume pass (13 steps) |
| An offer, a shop pop-up or a title screen appears | [ ] ux_flow_probe capture per step; `menu_test` stays green |

## 3. The identity choice — whom you swear first

The genre asks for its faction choice BEFORE any play, and early choices later go out of date
and cost money to redo ([benchmark.md](benchmark.md)). **Our move**: play first (a win, two
buildings), choose at minute 2, and make the choice safe — it decides which lord comes FIRST,
never which lords you can have.

| Pick | Lord ([portraits.md](../../game-art-director/references/portraits.md)) | Brings (equal power, [numbers.md](numbers.md) §3) | The line's first lesson |
|---|---|---|---|
| The shield | Edwin — older infantry lord, crimson mantle | a batch of Levy (infantry t2) | holds the front |
| The bow | Elena — archer lord, green hood | a batch of Archers (archers t2) | strikes first, from range |
| The spur | Rowan — young cavalier, plume and kite shield | a batch of Mounted Scouts (cavalry t2) | fastest march |

1. **Reswear**: free, once per 24 h, until 168 h after founding. Lord XP and levels move 100% to
   the new first lord; anything spent on the old lord's gear or skills is refunded 100%.
2. **Day 4**: the chapter chest gives a SECOND lord — the player picks one of the two not sworn
   (§6). Lords beyond these three follow [lords.md](lords.md) acquisition; every lord has a free
   path (SKILL.md rule 6).
3. The pick's only gameplay effects are one batch of troops and which lord leads first. No
   permanent percentage bonus hangs on it.
4. Each starter must own one of the six four-piece sets (24 items = 6 sets for 8 lords; verify in
   `data/equipment.gd`) — chapters 4 and 7 hand out pieces of the sworn lord's set.
5. The house sigil (step 9) is pure cosmetic: 6 at founding, changeable any time for free.

| Fails when | Caught by |
|---|---|
| One pick's D1 is > 5 pp below the others (a trap option) | [ ] D1 by `sworn_first` (§11) |
| A pick is chosen by < 15% (dead) or > 60% (no-brainer) of players | [ ] pick-share telemetry, weekly |
| Reswear loses a single XP point or resource | [ ] unit test: invest → reswear → totals equal |

## 4. Newcomer safety — the peace ward and safe PvE

The genre starts new castles under a shield [duration unverified] that the player's own attack
breaks, so learners lose protection by playing; the player is zeroed soon after it ends and
quits ([benchmark.md](benchmark.md) §10). **Our move**: PvE never breaks the ward; it lasts long
enough to learn defence; the garrison lesson comes before it ends; the map shows it. Working
name "the King's Peace" (story-forge): it binds lords, not raiders.

| Dial | PROPOSAL | Why |
|---|---|---|
| Length | 168 h (7 d) from founding | all 7 chapters open by 120 h (§6) + 2 days to use them |
| Warnings | −24 h and −1 h; the garrison lesson fires at −24 h if not done yet; push only if allowed | nobody learns about the end from a battle report |
| Ends early by choice | "Lay down the peace": 2 taps + confirm | players who want war are not held back |
| Ends early by growth | realm older than 14 d AND the player enters the realm's top 30% by power → ends 24 h later, with a notice | a fast spender in an old realm cannot grow behind the ward |
| Once | never restored, never sold ([monetization.md](monetization.md)); the return ward of §8 is separate | a ward on sale is a shield on sale |

| Action | Under the ward |
|---|---|
| Attack, scout or rally a player's castle; attack a player's march; join a rally on a player | **breaks it**, after a confirm that shows the time left ("Ends your peace — 4 d 06 h left") |
| Camps, AI lords, rally-only strongholds, gathering, relocating, reinforcing an ally | allowed, ward kept |
| Players attacking or scouting the warded castle | rejected server-side |
| Players attacking the warded player's marches | rejected on camps and on gathering nodes of level ≤ 2 ([world.md](world.md)); allowed on higher nodes (the ward is not a gathering shield for farm accounts) |
| Reinforcements the warded player sends | fight under normal loss rules ([combat.md](combat.md)) |

- **Map signal**: others see a painted seal on the castle and the word "Warded" (shape + word,
  never colour alone), no countdown; the owner sees the countdown in the profile and tracker.
- **Safe PvE in week 1**: camp and raid fights of a warded player produce **0 dead**; the median
  day-1 camp loss heals under the 5-min free finish. Camp levels open one by one on a win
  ([world.md](world.md)). Camp tags come from the deterministic resolver run on the camp's public
  army: **Easy** = predicted win with ≤ 10% of the march wounded, **Even** = win with 10–40%,
  **Hard** = predicted loss or > 40%; Hard asks one extra confirm tap in week 1. Raiders attack a
  castle only in the two scripted lessons (step 1 and day 6) unless world.md designs raids.
- Server: one field `ward_end_unix` (+ `ward_broken`) on the castle document; the attack and
  scout validators read it; 0 ticks (SKILL.md rule 5).

| Fails when | Caught by |
|---|---|
| A warded castle is attacked or scouted by a player | [ ] ward_test: `WARD OK - 11 rules, 0 leaks` |
| Churn in the 48 h after the ward ends > the cohort baseline + 5 pp | [ ] cohort churn around `ward_end_unix` |
| > 5% of players who break the ward lose ≥ 50% of their troops within 24 h (regret) | [ ] telemetry break → losses join |
| Warded accounts scout for a main (spies) | [ ] scouting breaks the ward; ward_test covers it |

## 5. The alliance nudge

Alliance members retain; the genre pays premium currency for the first join
([benchmark.md](benchmark.md)), which also pays alliance-hopping. **Our move**: join at minute 8
into an alliance that is awake NOW, felt at once as help on a real timer, paid once per account.

**Recommendation** (the 3 cards at step 10; alliance data from [alliance.md](alliance.md)):
```
score = 0.35·min(active_15m / 5, 1)          # members active in the last 15 min
      + 0.25·min(helps_per_request_24h / 10, 1)
      + 0.20·tz_match                          # median member time zone within ±3 h of the device
      + 0.15·lang_match
      + 0.05·open_slots / cap
```
Excluded: fewer than 5 members; no officer active in 48 h; more than 3 newcomers (< 7 d old)
kicked in the last 7 days; full. Each card shows: members online now, the median time to a first
help (last 24 h), language, time zone, the alliance's land on the map.

**The first request (the felt reward)**: step 11 starts a 14-min keep upgrade with help
auto-asked. With `H = 10`, `f = 120 s` each help removes 2 min: 14 → 12 → 10 → 8 → 6 → **4 min
after 5 helps = free finish**. The session-2 digest says "Allies saved you 10 m on your keep".

**The join purse** (bound to the account, once): at join — 1 h Universal hourglass + 3 h of own
output (all five resources); after 72 h in ANY alliance — 3 h Works hourglass + a gem amount set
by [monetization.md](monetization.md) (0 is a valid answer).

- "Later" is always a choice. The nudge returns at session 2 start and in chapters 1 and 3 —
  never more than once per session, never as a blocking modal after the first.
- Chapter 3's chest is the alliance's welcome: a solo player loses that one chest, nothing else.
- A newcomer who closes chapter 3 sends a small gift to every member (≤ 10 newcomer gifts per
  alliance per week; the newcomer must stay 72 h) — alliances gain from recruiting, alts do not.

| Fails when | Caught by |
|---|---|
| > 30% of first requests get < 5 helps within 30 min | [ ] telemetry `first_request_helps_30m` |
| > 5% of joiners are kicked by the recommended alliance within 72 h | [ ] telemetry; auto-exclusion rule above |
| Join purse paid twice to one account | [ ] cloud-forge claim test (idempotent) |

## 6. The founding week — seven chapters

The genre runs an 8-day new-server event that opens new tasks each day ([benchmark.md](benchmark.md)).
**Our move**: the chapters follow the PLAYER's account age (a late joiner gets them too); a
missed day is never lost; the systems open by progress, and the chapter only adds tasks, a chest
and a lesson.

1. Chapter N opens at founding + (N − 1) × **20 h** (0, 20, 40 … 120 h) — 20, not 24, so a player
   who comes back at about the same hour each day always finds the next one open. All stay open
   until day 14.
2. 5 tasks per chapter; the chest at **4 of 5**; "Open" = 1 tap. Chapters are milestones, not
   points: they never add a second point system ([core-loop.md](core-loop.md) §1 rule 2).
3. Every task is an action the daily loop already asks for, or a first-time moment (§7); never
   "open the shop", "spend gems", "watch", or a clock time. Effort ≤ 1.5× one day's orders.
4. **The arc follows the gates, never the reverse**: if progression.md opens a system after the
   chapter's day for the median free player, the chapter shows its day's tasks without it and
   the lesson fires at the real unlock.
5. In a new realm the realm's own founding event ([liveops.md](liveops.md)) counts the same
   actions and sits under the SAME rail icon — never two lists asking for different chores.

| Ch. (opens) | Chapter (working name) | Lesson (§7) | Tasks (chest at 4 of 5) | Chest (week-1 values) | Next hook |
|---|---|---|---|---|---|
| 1 (0 h) | The Stockade | first battle, first zoom-out (§2) | swear a lord · clear 3 camps · keep to level 3 · muster 2 batches · join an alliance | 1 h Universal + 3 h own output + lord XP | "The land opens" |
| 2 (20 h) | The Land | hunt order + Resolve bar; first gathering banner; fog | send 1 gathering march · 1 hunt of 5 camps · scout 1 fog patch · start 2 research · 2 check-ins ≥ 2 h apart | 3 h Works + 50 Resolve | "Your banner calls" |
| 3 (40 h) | The Banner | alliance land + the free move to it | help 10 times · claim an alliance gift · donate to alliance research · move next to allies (free, once) · gather once on alliance land | 3 h Universal + the newcomer gift to all members | "A second lord rides in" |
| 4 (60 h) | The Lord's Road | pairing (primary + secondary); first talent point if open | level the sworn lord to 5 · raise 1 skill · equip the first piece of the lord's four-piece set · choose the second lord · field both in one march | the SECOND LORD (§3) + 3 h Muster | "Strongholds need many banners" |
| 5 (80 h) | The Rally | first rally, join and lead | join 1 rally · lead 1 rally (companions if allies are offline) · hunt 5 camps · heal all · muster 3 batches | 8 h Works + 3 h own output | "Walls before the peace ends" |
| 6 (100 h) | The Wall | garrison + the raid on the walls | set the garrison lord · win the raid on the walls · reinforce an ally once · upgrade the watchtower · turn on attack alerts | 3 h Muster + 50 Resolve | "The whole realm, and its season" |
| 7 (120 h) | The Realm | seasons (kept / reset); war windows | open the realm view · open the calendar · read the season card · 1 war-window action or 1 rally · reach the 100-point daily chest on 4 days | a **Sound** piece of the sworn lord's set + 8 h Universal + the **Founder** title (chapters 1–7 done inside the realm's founding window) | the weekly writ and the season track |

Hourglasses from chapters: 29 h in total, on top of core-loop's daily chests and writ. Check the
hoarding line (held ≤ 2× queued at day 30, [core-loop.md](core-loop.md) §5): `econ_sim.py` has no
time-window field, so model the chapter and purse rewards in a separate week-1 model run with
`--days 1,7`, and keep them OUT of the day-30 model.

| Fails when | Caught by |
|---|---|
| A player who returns at the same hour daily finds a chapter locked | [ ] unit test: 20 h cadence over 7 days, arrival ±2 h |
| A task maps to no core-loop step or first-time moment (busywork) | [ ] task table vs [core-loop.md](core-loop.md) §8.2 |
| < 60% of day-7-active players close ≥ 6 of 7 chapters | [ ] telemetry per cohort |
| A solo player cannot close any chapter except chapter 3 | [ ] table check: ≤ 1 alliance-only task per chapter (3 excepted) |

## 7. First-time moments — teaching the late systems when they open

The genre's tutorial ends at the map view and chapter quests [observational]; the systems that
decide who stays (rallies, garrisons, war seasons, talent planning) are learned from video
sites ([benchmark.md](benchmark.md)). **Our fix**: a first-time moment (FTM) fires when a system
opens AND the player can use it now, and teaches it with a real action.

**The FTM contract**
1. Trigger = unlock + a usable situation (an open rally, a talent point in hand). Not triggered
   within 72 h of the unlock → it becomes a chapter or ledger task with the same reward.
2. ≤ 90 s, ≤ 8 taps, ≤ 3 cards of ≤ 14 words; skippable after 3 s; never forced twice.
3. It teaches **the one number that decides the system** (table) — on screen, in the player's
   own situation ("this rally leaves in 4 m 12 s; 3 of 5 banners filled").
4. One FTM at a time; none within 10 min of another, of a ceremony, or during a war window's
   Engage phase ([core-loop.md](core-loop.md) §8.3); queued ones fire at the next quiet moment.
5. Skipped or done → it stays in **the ledger** (working name "Fable's ledger", story-forge):
   a 20–40 s replay card per lesson, 2 taps from the lord hall, forever.
6. The first run is tuned to succeed (target ≤ 60% of the player's strength) and pays the
   normal reward; nothing is returned artificially afterwards.
7. A system the player already used (counter > 0 in the save) never fires its FTM.

| FTM | Fires when | The real action | The one number shown | Taps | Works if (unaided use ≤ 7 d after) |
|---|---|---|---|---|---|
| Hunt order | Resolve ≥ 50 and ≥ 5 camps in range | one march, up to 5 camps | Resolve 10 per camp; full again in 10 h | 4 | ≥ 70% send a hunt |
| Gathering banner | first free banner on day 2 | a march to a level-1 node | the node's load and return time | 4 | ≥ 70% gather again |
| Join a rally | rallies open + an alliance rally in its join window | join with a preset march | the join countdown and the filled banners | 4 | ≥ 50% join again |
| Lead a rally | first rally-only stronghold in range | lead; allies or two crown columns join (PROPOSAL, [world.md](world.md)) | capacity and the damage-share reward | 6 | ≥ 30% lead again |
| Garrison | chapter 6 opens (100 h), at the latest 24 h before the ward ends | set the garrison lord; the raid on the walls | who defends first; beds free in the infirmary | 6 | ≥ 80% have a garrison lord at ward end |
| Reinforce an ally | an ally under attack warning (or chapter 6) | send a march to the ally | the arrival ETA vs the attack ETA | 4 | ≥ 30% reinforce again |
| First defeat | first lost battle | the report with its ranked cause (report-forge) + one next-step button | the cause's number (e.g. "their spearmen: +counter vs your cavalry") | 3 | next attack on that target class wins ≥ 60% |
| First attacked by a player | first player attack after the ward | infirmary, protected resources, request help | lost vs protected; hours to recover | 4 | ≥ 70% active 48 h later |
| Infirmary near full | beds ≥ 80% filled | heal all; see bed count | beds free; what dies at 100% | 3 | overflow deaths in week 2 ≤ 5% of players |
| Lord pairing | the second lord arrives | field both in one march | only the PRIMARY's talents and gear count ([lords.md](lords.md)) | 5 | ≥ 60% field a pair |
| Talents | first talent point | spend it; the recommended path for the lord's role is lit | points held of the cap; free resets until day 14, then [lords.md](lords.md) | 4 | ≥ 70% spend all points |
| Set piece | first piece of a lord's set | equip it | the 2-/4-piece set bonus and what is missing | 3 | ≥ 60% equip a 2nd piece |
| Second desk | the second research desk opens | start a 2nd research | both desks' end times | 3 | 2 desks busy at ≥ 70% of exits |
| Siege engines | the siege workshop stands | build one engine | its effect on walls vs troops (siege-forge) | 4 | ≥ 30% field one |
| War window | the first window after the ward ends: at the −10 min call | the 30-min shape: muster, scout, engage ([core-loop.md](core-loop.md) §8.3) | the window's end time and the alliance's objective | 5 | ≥ 40% act in a 2nd window |
| Season | the first season start the player lives, or chapter 7 | the season card: two columns KEPT / RESET + the track | days left; what resets (track, season ranking) and what stays (castle, troops, lords, gear) | 2 | ≤ 10% churn in the season's first week vs the previous week |

| Fails when | Caught by |
|---|---|
| Two FTMs in one 10-min window, or one during an Engage phase | [ ] ftm_probe: `FTM OK - 16 moments, 0 repeats, 0 blocked > 3s` |
| An FTM > 90 s or > 8 taps, or it fires for a system already used | [ ] ftm_probe on crafted saves |
| Unaided use below the "works if" line for 2 weeks | [ ] telemetry → rewrite that FTM (a lesson, not a player, failed) |
| A lesson is not in the ledger after it fired or was skipped | [ ] ftm_probe ledger check |

## 8. Late joiners — routing and the newcomer's passage

The genre opens new servers every day or two and lets very new players move to a newer one
within their first days ([benchmark.md](benchmark.md)); outside that window players are stuck in
old servers. **Our move**: route by default, move once for free, and catch up by progression.

| Case | Route | Help |
|---|---|---|
| Fresh install, no invite | the youngest realm in the player's region cluster whose **founding window** is open: age ≤ 10 d AND population ≤ 80% of its cap ([world.md](world.md) sets the cap) | the realm's founding event ([liveops.md](liveops.md)) |
| Install from a friend's invite link | the friend's realm, any age | the friend's alliance first on the step-10 cards; [progression.md](progression.md) catch-up |
| Warded player, first 7 days | **newcomer's passage**: once, free, to a realm in its founding window or to a friend's realm; castle, lords, items and troops move; alliance membership ends | the ward and chapters continue |
| Player whose realm is emptying | [liveops.md](liveops.md) merges and migration | — |
| Return after ≥ 14 d away | a "what changed" digest of ≤ 5 lines; a 24 h return ward, once per 60 d, broken by the same acts as §4 | open FTMs re-queue |

- The next realm opens when the newest one reaches 80% of its cap or 7 days of age, whichever
  comes first (liveops.md and world.md own the cadence; each realm's fixed server cost is
  measured with `core/sd_cost_probe.gd` before the rule ships).
- The first zoom-out names the realm and its age: "The realm of <name>, founded 3 days ago."
- The passage ends the moment the ward breaks; it can never carry resources above the
  protected amount into an older realm ([economy.md](economy.md) owns transfers — feeder guard).

| Fails when | Caught by |
|---|---|
| A fresh install lands in a realm outside its founding window | [ ] route_test: `ROUTE OK - 1000 installs, window 100%, invites 100%` |
| An invite does not place the friend in the same realm | [ ] route_test invite pass |
| A passage is used after the ward broke, or twice | [ ] ward_test passage rules |

## 9. Return hooks in week 1

| Hook | Rule |
|---|---|
| Exit line | every session ends on "All busy — first free at HH:MM" ([core-loop.md](core-loop.md) §2 rule 4) |
| Session 2 on day 1 | the step-11 plates end in 6–14 min; the longest in ≤ 60 min |
| Push | only after the opt-in; ≤ 3 per day in week 1 (core-loop A8 allows 4); never for offers |
| Digest at open | ≤ 3 lines: helps received, finished work, the next chapter's countdown |
| Tomorrow line | the exit card names tomorrow's chapter in ≤ 6 words |
| Day-2 fallback | declined push → one settings card on day 2; no e-mail, no nagging |
| Account safety | the guest account is offered a link (store account or e-mail, cloud-forge) on day 2 or before a first purchase — never in the first 10 minutes; a lost guest castle is a lost player |

## 10. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| The tutorial never teaches the systems that decide retention | first-time moments at unlock, with a real action | 16 FTMs, ≤ 90 s each |
| The identity choice comes before any play | play first, choose at minute 2 | first win ≤ 60 s |
| The second builder is a timed gift that expires | 2 crews from minute one, never sold ([core-loop.md](core-loop.md) §2) | 2 → 3 by play |
| The shield breaks on the learner's own PvE | camps, AI lords and strongholds never break the ward | 0 PvE breaks |
| Early choices go out of date and cost money to redo | free reswear (7 d), free talent resets (14 d), 100% move or refund | 0 paid redo in week 1 |
| A cheap offer in the first minutes | no pop-up offer before day 2; none inside a guided step | 0 |
| Too many event icons in week 1 | the chapter and the realm's founding event share ONE rail icon | 1 icon, not 2 ([ux.md](ux.md) owns the rail cap) |
| New castles zeroed soon after the shield ends | 7-day ward + garrison lesson on day 6 + 0 dead in week-1 PvE | 168 h |
| Accidental shield breaks | a confirm that shows the time left | 1 extra tap |
| A premium reward for joining feeds alliance-hopping | the join purse once per account, second half after 72 h | 1 per account |
| Late starters trapped in old realms | routing, one free passage, catch-up | window 10 d |

## 11. Metrics — the FTUE funnel and retention (PROPOSAL targets; replace with cohort baselines)

"Tutorial complete" = step 12 reached, reported for session 1 and within 24 h. Reach = % of
first launches. **Red line**: any single step that loses > 3 pp is a red finding; > 5 pp blocks
a release. Joining an alliance is a choice and is reported beside the funnel, not in it.

| Step | 0 castle frame | 1 first win | 3 lord sworn | 7 battle won | 9 house named | **12 complete** | 10 alliance (choice) |
|---|---|---|---|---|---|---|---|
| Reach | ≥ 98% | ≥ 96% | ≥ 92% | ≥ 89% | ≥ 86% | **≥ 82%** session 1, ≥ 88% in 24 h | ≥ 55% session 1, ≥ 70% by day 3 |

| Retention and health | Target |
|---|---|
| D1 / D7 / D30 ([numbers.md](numbers.md) §8) | ≥ 40% / 15–20% / 6–10% |
| D1 of tutorial completers | ≥ 50% |
| D7 of day-1 alliance joiners vs solo | ≥ 1.5× |
| First session length (median) | 12–18 min |
| Sessions on day 1 (completers) | ≥ 3 for half of them |
| Push opt-in (of those asked) | ≥ 55% |
| Crash-free FTUE sessions | ≥ 99.5% |

**A/B rule**: one dial per test. Seeing ±3 pp on a 40% D1 needs ≈ **4,200 installs per arm**
(80% power, α 0.05); ±5 pp needs ≈ 1,500. Smaller tests read noise. The arm is stored as
`ftue_version`.

Telemetry: one `ftue_step` event per step {step, ms since first input, taps D/M}, buffered on the
client and sent in ≤ 3 batched writes per session (cloud-forge).

## 12. Harness, data, save migration, server cost

| Proof | Measures | Verdict line (PROPOSED — qa-forge fixes the wording) |
|---|---|---|
| `ftue_probe` (new, windowed 1080×1900; path to confirm) | fresh account on a test realm; the 13 steps × 3 lord picks; timings, taps, words, dead-ends, kill-resume | `FTUE OK - first win 32s, 34 taps (7 decisions), 9m40s, 3/3 picks won, 0 dead-ends` |
| `ward_test` (new, headless) | every break rule, server rejection, passage rules | `WARD OK - 11 rules, 0 leaks` |
| `route_test` (new, headless) | 1,000 synthetic installs and invites | `ROUTE OK - 1000 installs, window 100%, invites 100%` |
| `ftm_probe` (new, headless on crafted saves) | 16 FTMs: trigger once, spacing, skip ≥ 3 s, ledger | `FTM OK - 16 moments, 0 repeats, 0 blocked > 3s` |
| `core/session_audit.gd` from a FRESH save; `ux_flow_probe`, `ux_touch_probe`, `a11y_audit`, `layout_audit`, `w1f_aspect_sweep` | the script inside the full session; touch targets; +40% text; 6 screen shapes | existing lines; `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| `core/sd_cost_probe.gd` | writes per new player | inside the €200/month budget |

**Data** (gameplay-forge + onboarding-forge; `data/onboarding.gd`, path to confirm): the step
table, the chapter table, the FTM table. **Save fields**: `ftue_step:int`, `ftue_version:int`,
`founded_unix:int`, `ward_end_unix:int`, `ward_broken:bool`, `sworn_first:String`,
`reswear_next_unix:int`, `chapters:Dictionary`, `ftm_done:PackedStringArray`,
`passage_used:bool`, `join_purse:int` (0/1/2).

**Save migration**: existing saves load with `ftue_step` = done when the spine is past its first
level or any battle is won; chapters marked done by the counters they already have; FTMs marked
done where the counter is > 0 (unseen ones still fire once); no ward for existing castles;
`founded_unix` = first save time, or load time if unknown.

**Server cost** (estimate; measure): a new player's first session ≈ 1 account + 1 routing read +
≤ 4 step saves + ≤ 3 telemetry batches + 1 join + 1 help request + 3 claims ≈ 14 writes; week 1
adds 7 chapter claims; FTM flags ride the normal save sync (0 extra). At `I` installs per day:
≈ `21·I` writes per day — 2,000 installs a day ≈ 42,000 writes, ≈ 1.5% of the core loop's
2.9 M. The ward is a field read at attack time: 0 ticks.

## 13. Handoff to onboarding-forge

Every onboarding change lands first as `design/onboarding/SYSTEM.md` from
[spec-template.md](spec-template.md); its §13 compares these targets with the measured funnel.

| Deliverable | Owner (one writer per file) | Proof |
|---|---|---|
| Script runner, chapters, FTM trigger system, save fields, migration | onboarding-forge | ftue_probe, ftm_probe |
| Overlay, pointer, cards, alliance cards, the ledger screen | ui-forge | ux_flow_probe, ux_touch_probe, a11y_audit |
| March-out and first zoom-out shots | transition-forge | its frame-time probe: no hitch > 1 frame |
| Raid at the gate, first battle, first rally, raid on the walls | battle-forge (+ gameplay-forge data) | resolver harness; ftue_probe 3/3 |
| The swearing ceremony, lord cards, token rim | commander-forge + feel-forge | frame capture ≤ 3.0 s |
| Ward, routing, passage, recommendation data, placement of new castles | cloud-forge + world-forge | ward_test, route_test, sd_cost_probe |
| Every line, chapter and place name | story-forge + l10n-forge | layout_audit at +40% text |
| Horn, victory and swearing cues | audio-forge | cue list |
| Cold start and first frame | ship-forge | reference-phone capture |
| The four new harnesses | qa-forge | their verdict lines |

**Placement request to world-forge**: a new castle within a 25 s march of ≥ 3 level-1 camps, with
≥ 3 real castles and (if any exists) one alliance's land inside the first region view.

## 14. Owner decisions required

1. The ward: 168 h, the break list, and the growth end (top 30% in realms > 14 d old).
2. No offer pop-up before day 2 and none inside a guided step (spend; shop-forge).
3. The join purse contents, including the gem amount (spend; 0 allowed).
4. Free reswear for 7 d and free talent resets for 14 d (lord economy; lords.md).
5. The second starter lord as the chapter-4 chest (lord acquisition; lords.md).
6. Crown columns that join a first rally when allies are offline (fiction and world.md).
7. Names and voice (story-forge canon): the King's Peace, chapter titles, Fable's ledger, the
   newcomer's passage, the join purse, Founder; who speaks the first 10 minutes (a steward or Fable).
8. The founding window (10 d, 80%) and realm cadence (with liveops.md and world.md, after cost).
9. Consent and age screens if the law requires them (legal) — ≤ 2 taps, before step 1, counted
   in the tap budget; the first-input clock then starts at the consent tap.
10. Any dial here that collides with a shipped sacred constant (the shipped value wins).

## 15. Reviewing an onboarding spec — checklist

- [ ] First win ≤ 60 s p90; ≤ 40 taps with ≥ 5 decisions; ≤ 90 s of reading; forced taps end at 110 s.
- [ ] Every guided step is a real action on the live realm; no title screen, no practice world.
- [ ] All three lord picks win the first battle in the harness; reswear refunds 100%.
- [ ] The ward: length, warnings, break list, server rejection, map signal — each with a test.
- [ ] Week-1 PvE: 0 dead; the median day-1 loss heals under the free finish.
- [ ] Alliance cards follow the score and exclusions; the first request math is shown.
- [ ] Chapters open every 20 h, stay to day 14, chest at 4 of 5, no busywork, one rail icon.
- [ ] Every late system has an FTM with its trigger, one number and a "works if" line.
- [ ] Routing, invite and passage covered by route_test and ward_test.
- [ ] Funnel targets, red lines and the A/B sample size are in the spec.
- [ ] Save migration named; server cost line with its formula; owner decisions listed.
