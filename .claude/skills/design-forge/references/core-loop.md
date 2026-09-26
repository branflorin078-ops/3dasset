# Core loop — five timescales, parallel plates, honest timers

What a player does between opening the game and putting the phone down, at five lengths: a 30-second glance, a 5-minute check-in, a day, a week, a season.
Implementation: **gameplay-forge** (rules, data, save), **ui-forge** (queue tracker, cards), **feel-forge** (ceremonies), **cloud-forge** (server time, help log), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md).

**Every number here is a PROPOSAL** unless it quotes a canonical fact. Check the shipped data first (`data/*.gd`, files to confirm); a dial that already exists as a sacred balance constant keeps its shipped value, and this file's value becomes a proposal to the owner.
`S` = tier (1–6) of the spine building that gates progression (keep/fortress or townhall — [progression.md](progression.md) names it; verify in `data/buildings.gd`, path to confirm).

## 0. The four questions

- **Want**: every visit finishes something (a building tier, a research, a batch, a lord level); every day a chest; every week the writ chest and a visible city change.
- **Obstacle**: plate timers (time), costs (resources), Resolve (camp attacks), plate count (grows only by play).
- **Wait**: first session 5 s – 3 min; week 1: a plate ends inside every 2–4 h waking gap; endgame: long plates 2–14 d, short plates (musters, gathering, hunts) 1–8 h, length chosen by the player.
- **Witness**: allies see their help as minutes saved; the city silhouette changes per building tier (34 archetypes × 6 tiers); march lines on the realm map; the alliance feed.

## 1. The five timescales

| Scale | Budget | Player's question | Touches | Visible pay-off | Target |
|---|---|---|---|---|---|
| Glance (the 30 s tap) | ≤ 30 s, ≤ 5 taps | "Is anything ready?" | help all, free finish, ≤ 1 refill | digest "Allies saved you 42 m"; a finished tier | 2–4 per day |
| Check-in | ≤ 5 min, ≤ 30 taps | "Set everything running." | every plate, Resolve, chests | 0 idle plates at exit; a chest opened | 2–4 per day |
| Day | 4–8 sessions engaged, 2 casual | "Finish today's orders." | daily orders, sheds, Resolve | 100-point chest; ≥ 1 city change per day in weeks 1–2 | 100 points in ≤ 2 check-ins |
| Week | 7 days | "Close the writ; defend our land." | weekly writ, war windows, camp ladder | writ chest; alliance standing; territory | top chest with 5 of 7 days |
| Season | [liveops.md](liveops.md) (PROPOSAL 4–6 weeks) | "Reach the big goal." | season track (same points) | spine tier, a troop tier, a lord's four-piece set, a title | free-track top at 70% of days |

Rules: (1) every scale pays off on its own; (2) ONE activity counter feeds day, week and season (§7) — never a second point system; (3) **the 15-hour promise**: nothing the player owns is lost if they return within 15 h (Resolve §3, sheds A1, finished work waits, chests auto-claim).

| Fails when | Caught by |
|---|---|
| 3 glances in a row offer nothing to do → the player stops glancing | [ ] loop sim: ≥ 70% of glances ≥ 2 h apart offer ≥ 1 action |
| A check-in needs > 30 taps or > 5 min → chores | [ ] session_audit check-in pass (§11) |
| A day pays off only at fixed clock hours → unfair across time zones | [ ] no order or chest tied to a clock time (§7) |

## 2. Plates — the parallel queues

A plate works while the player is away and needs one decision to restart. The genre runs ≤ 5 timers and ≤ 5 marches, all refillable in one short visit: one research queue, one training queue per military building and one heal queue (the last two [observational]).
It sells the second builder behind a paid status tier, which players read as a paywall on a core queue.

**Plate → cap → unlock → refill cadence (PROPOSAL)** — w1 / m1 / end = week 1 / month 1 / endgame ([numbers.md](numbers.md) §1).

| Plate (in-world name) | Start | Cap | Unlock | Timer range w1 / m1 / end | Refill cadence target | Help | Free finish |
|---|---|---|---|---|---|---|---|
| Build crews (masons' crews) | 2 | 3 | 3rd crew at S5 | 5 m–4 h / 4 h–2 d / 2–14 d | w1: ≥ 1 crew ends inside every 3 h waking gap | yes | yes |
| Research (scriptorium desk) | 1 | 2 | 2nd desk at S4 | as crews | 1 new choice per 1–2 check-ins | yes | yes |
| Training (muster yards) | 1 per troop line whose building stands | 5 | with the line's training building (map: verify `data/troops.gd`) | player-chosen 1 h / 3 h / 8 h / "until I'm back" | the player's next gap (A3) | no | yes |
| Healing (infirmary) | 1 | 1; beds grow | beds by hospital tier ([combat.md](combat.md)) | one lost full march heals ≤ 8 h, no speed-ups | after losses | yes | yes |
| Marches (banners) | 2 | 5 | +1 at S3, S4, S5 | gathering 1–8 h; hunts in-session; war marches 60–180 s | gathering: the gap; hunts: each check-in | — | — |
| Resolve pool (§3) | 150 (full) | 150 regen, 300 items | fixed | regen 10 per hour | bar full at 10 h, pool at 15 h | — | — |
| Production sheds | — | ≥ 15 h of output | building tier ([economy.md](economy.md)) | — | collected on open (A1) | — | — |
| Daily orders / weekly writ (§7) | 0 pts | 100 per day / 700 per week | — | reset 00:00 UTC / Monday 00:00 UTC | ≤ 2 check-ins / 5 of 7 days | — | — |

Siege engines, scouts and equipment crafting belong to siege-forge, [world.md](world.md) and [lords.md](lords.md); if one of them gets a timer, it joins this table under these rules.

1. **We NEVER sell plate count.** Crews, desks, yards, beds and banners come only from play (spine tier, buildings, research) — never from gems, bundles, a paid status ladder or a rental.
2. **Refill in one visit**: every plate sits in ONE always-visible queue tracker (ui-forge); an idle plate is ≤ 3 taps from running; all plates together ≤ 30 taps and ≤ 5 min (§8.2). Idle = gilt outline (GILT #C9A04C) AND the word "Idle" — never colour alone, never flashing. Plate icons are Blender-made art, never line glyphs.
3. Every plate is a function of time `(start_unix, duration_s, help log)`; remaining time is computed, never ticked by the server (SKILL.md rule 5).
4. A check-in ends with 0 idle plates and the line "All busy — first free at 14:20" (the next reason to return).
5. A new plate type ships only with a batch action (Refill all / Resend all) or by removing a check-in step: the late profile already sits at 30 taps.

| Fails when | Caught by |
|---|---|
| A plate idles > 25% of a free player's waking hours in week 1 | [ ] loop sim idle plate-hours ≤ 25% |
| A plate needs > 3 taps from the tracker | [ ] ux_flow_probe path per plate |
| A plate, bed or banner count appears on a paid surface | [ ] grep of the shop-forge offer data returns 0 |

## 3. Resolve — energy for camp attacks (PROPOSAL)

Resolve limits PvE attacks on barbarian camps and AI-lord targets ([world.md](world.md) decides which). Three reasons: pacing (two check-ins a day are enough), resistance to bots and farm accounts, and a server ceiling (≤ 24 camp resolutions per player per day from regen).
The genre sizes its energy to refill in about 12 h [community estimate] and wastes all regen at the cap.

| Dial | PROPOSAL | Why |
|---|---|---|
| Bar | 100 | two hunts of 5 camps per visit |
| Regen | 10 per hour (1 per 6 min) | bar full in 10 h; 240 per day |
| Reserve | +50 above the bar, filled at full regen speed once the bar is full | pool 150 = 15 h without loss |
| Camp attack | 10 (AI-lord target 20) | 24 camps per day from regen |
| Hunt order | one march, up to 5 camps in a row, 10 each | the march does not walk home between camps (saves time, not Resolve) |
| Rally on a camp | leader pays, joiners pay 0 | rewards joining; banners and march time are the limit |
| Items | chest/event Resolve lifts the pool up to 300; regen pauses above 150 | item Resolve is never wasted |

Resolve collected per day when the player spends everything at each visit; per gap of `g` hours the player gets `min(10·g, pool)`:

| Play pattern (gaps) | No reserve (genre shape) | Reserve 50, full speed (**recommended**) |
|---|---|---|
| 6 visits (3, 3, 3, 3, 4, 8 h) | 240 (100%) | 240 (100%) |
| 2 visits (12 + 12 h) | 200 (83%) | 240 (100%) |
| 2 visits (16 + 8 h) | 180 (75%) | 230 (96%) |
| 1 visit (24 h) | 100 (42%) | 150 (62%) |

Rejected: a half-speed reserve of 60 (`100 + min(60, 5·(g − 10))` per gap) gives 92% / 88% / 67% — harder to explain, and it still loses Resolve during sleep. The recommended rule reads in one line ("nothing is lost for 15 hours"), matches the sheds, and two visits a day still beat one (240 vs 150).
Store `(P0, t0)` only: `P(t) = min(150, P0 + 10·(t − t0)/3600)` when `P0 ≤ 150`; the bar shows `min(P, 100)`, the reserve `P − 100`. Resolve never gates PvP, gathering, scouting, joining rallies, help or healing. Selling it is an owner decision (§12).

| Fails when | Caught by |
|---|---|
| A 2-visit player loses Resolve (15-hour promise broken) | [ ] loop sim loss 0% for the 2-visit profile |
| A full bar cannot be spent in one 5-min check-in | [ ] hunt orders in §8.2: 6 taps spend 100 Resolve |
| Camp resolutions per player per day > 24 + item Resolve | [ ] sd_cost_probe resolution count |

## 4. Timers and the free finish

1. Lengths come from player time ([numbers.md](numbers.md) §1): first session 5 s – 3 min; week 1: 5 m – 4 h; month 1: 4 h – 2 d; endgame 2 – 14 d.
2. **Ceiling: no single timer on any plate exceeds 14 d base** (the top of [numbers.md](numbers.md) §1). If [progression.md](progression.md) sets a lower cap for the spine ladder (its brief proposes 7–10 d), the lower cap wins. The genre's top spine upgrade runs about four months base; its last levels become a test of spending and a speed-up hoarding game.
3. **Free finish**: when remaining ≤ threshold, "Finish (free)" appears — one tap; "Finish all free" = 1 tap. Threshold 5 min, raised to 7 and 10 min by research nodes that open at S3 and S5. Earned only: never gems, never a paid status.
4. **Auto-complete**: a finished timer completes without a tap and the plate turns idle (ceremonies: A9).
5. **Honest display**: two units ("1 h 12 m"; "4 m 05 s" under 10 min), rounded UP (never "0 s" while running); tap-and-hold shows the end time on the local clock; the help button shows the next help's value ("next help −4 m 48 s"); the speed-up picker shows the new end time first.
6. Server time is the truth: remaining = `end_unix − now`, `now = Time.get_unix_time_from_system() + server_offset` (offset set at each sync); labels refresh from a 1 s `Timer` node only while visible.

Worked example (week 1, new alliance, §6 dials): a 39 m 51 s build gets 10 helps × 2 min = −20 min → 19 m 51 s left; it runs 14 m 51 s, then the last 5 min are a free finish. Real wait ≈ 15 min instead of 40.

| Fails when | Caught by |
|---|---|
| A timer shows a length it will not keep (hidden gate, "soon", rounding down) | [ ] display-rounding unit test (gameplay-forge) |
| A timer > 14 d base ships, or the free threshold appears in a paid offer | [ ] curve.py table per ladder, top rung ≤ 14 d; offer grep |
| A finished plate waits for a "collect" tap before it can restart | [ ] session_audit: 0 collect taps on plates |

## 5. Speed-ups priced in minutes (hourglasses)

One table ([numbers.md](numbers.md) §7). Price `p(m) = k · m^β` with β = 0.9, degressive; `k` = gems for the 1 m item, set by shop-forge (spend: owner).
β = 0.9 is mild — the 24 h hourglass costs 48% per minute of the 1 m one; β = 0.85 (34%) pushes bulk buying and hoarding; β = 1 removes the bulk incentive.

| Hourglass | Minutes | Price (× k) | Per minute (× k) | Earned mainly from |
|---|---|---|---|---|
| 1 m | 1 | 1.0 | 1.00 | change given back (rule 4) |
| 5 m | 5 | 4.3 | 0.85 | daily chest 30 |
| 15 m | 15 | 11.4 | 0.76 | alliance shop ([alliance.md](alliance.md)) |
| 1 h | 60 | 39.8 | 0.66 | daily chest 60 |
| 3 h | 180 | 107 | 0.59 | daily chest 100 |
| 8 h | 480 | 259 | 0.54 | weekly writ 200 and 350 |
| 24 h | 1,440 | 696 | 0.48 | weekly writ 500, season track |

1. Three kinds: **Works** (build + research), **Muster** (training + healing), **Universal**. Events can add war-prep time without speeding the city, and the reverse. Rewards use only these seven sizes.
2. A direct gem finish costs `p(remaining minutes, rounded up)` — the same curve, never a markup.
3. **Honest inventory**: "Held: Works 38 h · Muster 12 h · Universal 6 h — Queued work: 51 h".
4. **Change is given back**: an hourglass larger than the remaining time returns the unused minutes as the largest sizes that fit (60 m on 38 m → 15 m + 5 m + 1 m + 1 m). No minute is lost.
5. **Money-law**: an hourglass sells works (allowed); the gem-finish button shows hourglass art and the price only — no troop, weapon or battle art on or behind it, also on the muster and infirmary plates. Hourglass icons are Blender-made art (ui-forge).
6. War windows cap gem finishes on muster and infirmary plates per player (owner, §12; recommended ≤ 480 min per window).

| Fails when | Caught by |
|---|---|
| Median free player holds > 2× their queued minutes at day 30 (hoarding) | [ ] telemetry held ÷ queued; econ_sim line |
| A direct finish costs more than the items that do the same | [ ] price unit test over 1–20,160 min |
| Minutes lost to an oversized hourglass | [ ] change-back unit test (60 m on 38 m) |

## 6. Alliance help — `max(cut · T, floor)`

Each help removes `h = max(c · R, f)` from the remaining time `R` (never below 0). The helped player gets time, the helper gets a reward: the social speed-up pays both sides ([alliance.md](alliance.md) owns ranks, currency, research; it must quote the same `c`, `f`, `H`).

| Dial | PROPOSAL | Note |
|---|---|---|
| `c` cut | 1% of remaining | long timers lose `1 − 0.99^H` |
| `f` floor | 120 s; 180 s after one alliance research node | our move: the genre starts at 60 s; a 2-min floor lets a brand-new alliance erase first-week timers from day 1 |
| `H` helps per request | `10 + 4·(E − 1)` = 10, 14, 18, 22, 26, 30 for alliance-building tier E = 1–6 | likely the embassy archetype (verify `data/buildings.gd`) |
| Helpable | build, research, heal | training is not: war production stays a personal cost |
| Crossover | `R = f / c` = 3 h 20 m (120 s), 5 h (180 s) | below it every help is worth the floor |

Worked math — `tools/curve.py` (cut 0.01 is its default), helps applied at request time; reproduce with
`python tools/curve.py --levels 9 --first 5m --last 14d --shape geometric --helps H --help-floor F` for (H, F) = (10, 120s), (18, 120s), (30, 180s):

| Timer | H 10, f 2 m (new alliance) | H 18, f 2 m | H 30, f 3 m (mature alliance) |
|---|---|---|---|
| 5 m 00 s and 14 m 07 s | 0 | 0 | 0 |
| 39 m 51 s | 19 m 51 s (−50%) | 3 m 51 s → free finish | 0 |
| 1 h 52 m | 1 h 32 m (−18%) | 1 h 16 m (−32%) | 22 m 28 s (−80%) |
| 5 h 17 m | 4 h 47 m (−10%) | 4 h 24 m (−17%) | 3 h 46 m (−29%) |
| 14 h 56 m | 13 h 30 m (−10%) | 12 h 27 m (−17%) | 11 h 02 m (−26%) |
| 1 d 18 h | 1 d 14 h (−10%) | 1 d 11 h (−17%) | 1 d 07 h (−26%) |
| 4 d 23 h | 4 d 11 h (−10%) | 4 d 03 h (−17%) | 3 d 16 h (−26%) |
| 14 d 00 h | 12 d 15 h (−10%) | 11 d 16 h (−17%) | 10 d 08 h (−26%) |

Read it: helps plus free finish erase every timer up to `H·f + threshold` = 25 min (H 10), 41 min (H 18), 100 min (H 30 with the 10-min free finish). Long timers lose 10% / 17% / 26%. Help decides week 1 and still removes 3 d 16 h from a 14-day timer, but never replaces planning.

- **Witness**: the helper sees each help's value ("−14 m 24 s on <ally>'s mill"); digests say "Allies saved you 3 h 12 m" (daily) and "Your help saved allies 9 h 40 m" (weekly).
- **Helper reward** (alliance currency) for the first 30 helps per day; later helps still count for the ally but pay nothing. Accounts < 72 h old or at S1 give helps that pay nothing (stops farm accounts).
- **Cost**: one "help all" tap = ONE append to the alliance help log (request ids + timestamp); each request's remaining time is recomputed from the log. Writes scale with taps, not helps: ≤ 50,000 × 8 = 400,000 appends per day. Never one write per help (cloud-forge owns storage).

| Fails when | Caught by |
|---|---|
| A new alliance cannot erase a 20-min week-1 timer (weak reason to join) | [ ] curve.py row for the shipped H, f |
| A request gets more than `H` helps, or a helper is paid past 30 per day | [ ] server-side cap test (cloud-forge) |
| Help writes grow per help, not per tap | [ ] sd_cost_probe help-log line |
| A top alliance takes > 30% off a 14 d timer (the ceiling stops pacing) | [ ] `1 − 0.99^H_max ≤ 0.30` → `H_max ≤ 35` |

## 7. Daily orders, weekly writ, season track (task chests)

1. **A fixed list**, the same every day, plus 2 rotating slots: a known list gets done inside the normal loop; a random list turns orders into chores.
2. Every order is an action the loop already asks for (§8.2). Never "open the shop", "buy", "spend gems", "watch", or a fixed clock time.
3. 100 points count per day; 150 are available, so the player can skip what they dislike. The §8.2 check-in alone gives 95; a second visit ≥ 2 h later reaches 110.
4. **Three chests at 30 / 60 / 100**; "Open all" = 1 tap. Unclaimed chests are auto-claimed at reset (00:00 UTC, shown in local time with a countdown).
5. Daily points feed the weekly writ (≤ 100 per day → 700 per week) and the season track 1:1. **Writ chests at 200 / 350 / 500**: the top chest needs 5 full days of 7. **Season free-track top = 0.70 × season days × 100, rounded up to the next 100** (6 weeks: 2,940 → 3,000 = 30 full days of 42; 4 weeks: 1,960 → 2,000; [liveops.md](liveops.md) sets the length); a paid track is a [monetization.md](monetization.md) question under the money-law.
6. **Return streak**: 7 steps; a missed day moves back ONE step, never to step 1.
7. Rewards are bound to the account (hourglasses, Resolve, lord XP; resources land in protected storage): a farm account cannot pass chests to a main ([economy.md](economy.md) owns transfers).

| Daily order | Points | §8.2 step |
|---|---|---|
| Return to the castle (first open of the day) | 10 | 1 |
| Help allies 10 times | 10 | 2 |
| Start 2 constructions | 15 | 4 |
| Start 1 research | 10 | 5 |
| Muster 1 batch (any line) | 10 | 6 |
| Send 1 gathering march | 10 | 8 |
| Clear 4 camps (40 Resolve) | 20 | 9 |
| Give to the alliance (gift or research donation) | 10 | 10 |
| Return again ≥ 2 h after the first visit | 15 | 2nd check-in |
| Rotating A: join or lead 1 rally at any hour (week 1: the guided first rally), else heal or scout | 20 | varies |
| Rotating B: a lord task (skill level, equip a piece) | 20 | varies |

Chest contents, week-1 values. Resources are given as hours of the player's OWN production, so they scale with the city and never inflate out of relevance ([economy.md](economy.md) may override):

| Chest | Contents |
|---|---|
| Daily 30 / 60 / 100 | 3 × 5 m Works + 1 h own food and wood / 1 h Universal + 30 Resolve / 3 h Universal + 3 h own output (all five resources) + lord XP (commander-forge sets it) |
| Writ 200 / 350 / 500 | 8 h Works / 8 h Muster + 50 Resolve / 24 h Universal + 6 h own output |

Hourglass total for a player who takes every chest: 255 min per day + 2,400 min per week ≈ 10 h per day. Model it in `tools/econ_sim.py`: add `"hourglass_min"` to `resources`, the chests as `per: "day"` sources (writ chests ÷ 7), queued minutes per day as the sink; resource lines copy the `growth` of the production line they mirror. The day-30 free-player band 0.90–1.10 of [numbers.md](numbers.md) §6 applies.

| Fails when | Caught by |
|---|---|
| < 70% of daily actives reach 100, or > 20% reach it in ONE visit (no reason for a 2nd visit) | [ ] telemetry per cohort |
| An order needs a screen the loop never visits | [ ] every order mapped to a §8.2 step (table above) |
| The weekly top chest needs 7 of 7 days (fear of breaking a streak) | [ ] writ top ≤ 5 × 100 |

## 8. Session shapes

A **tap** = one touch that changes state or opens a screen; scrolls and drags do not count; reading time counts in the time budget.
Profiles: **mid** = 2 crews, 1 desk, 3 yards, infirmary, 3 banners; **late** = 3 crews, 2 desks, 5 yards, infirmary, 5 banners. Measured at 1080×1900 (the session_audit window, game-director SKILL.md).

**8.1 The glance — ≤ 30 s, ≤ 5 taps.** Resume straight into the castle (live realm: no title menu); a digest of ≤ 3 lines ("Allies saved you 42 m · Mill tier 3 done · 2 plates idle") hides after 2.5 s or on the first tap; resume to first input ≤ 2.0 s on the reference phone (ship-forge). Then help all (1), finish all free if shown (1), refill one idle plate (2–3), leave.

**8.2 The check-in — ≤ 5 min, ≤ 30 taps, 0 idle plates at exit**

| # | Step | Taps mid | Taps late | Seconds (mid) |
|---|---|---|---|---|
| 1 | Resume → digest; production counts up over 800 ms (A1) | 0 | 0 | 5 |
| 2 | Help all (tracker) | 1 | 1 | 2 |
| 3 | Finish all free | 1 | 1 | 2 |
| 4 | Each idle crew: tracker → building card with the suggested upgrade and the next tier's render at ≥ 40% of screen height (ART SHOWN BIG) → Upgrade; help auto-asked (A4) | 6 | 9 | 30 |
| 5 | Each idle desk: tracker → choose research → Start | 3 | 6 | 20 |
| 6 | Muster yards: Refill all + confirm (A2) | 2 | 2 | 8 |
| 7 | Infirmary: Heal all + confirm | 2 | 2 | 5 |
| 8 | Gathering banners: Resend all (A2) | 1 | 1 | 4 |
| 9 | Two hunts: Hunt (tracker) → "nearest 5 at my level" (last lord preset kept) → Send (A6) | 6 | 6 | 30 |
| 10 | Chests: Open all; alliance gifts: claim | 2 | 2 | 20 |
| 11 | Leave: "All busy — first free at 14:20" | 0 | 0 | 3 |
| | **Total** | **24** | **30** | **129 + reading** |

Inside the 5 min: ≤ 4 castle ↔ realm transitions, each ≤ 700 ms (transition-forge); ceremonies ≤ 45 s in total (A9); touch targets ≥ 48 dp ([ux.md](ux.md) owns the number). Decision taps (which building, research, camps) ≥ 5 per check-in; maintenance taps ≤ 12 — or the visit is only upkeep.

**8.3 The war session — 30 min inside a war window.** Windows last ≤ 60 min, at two fixed times 12 h apart so every time zone has one at a reasonable hour ([liveops.md](liveops.md) owns the calendar).

| Minute | Phase | Player actions | Taps |
|---|---|---|---|
| −10 | Call | alliance call (chat-forge / mail-forge); one opt-in push | 0 |
| 0–3 | Muster | compressed check-in: heal all, refill all, resend all | ≤ 8 |
| 3–6 | Scout, plan | scout (2); report read ≤ 20 s (report-forge); lord pair preset (commander-forge) | ≤ 6 |
| 6–20 | Engage | 3–5 engagements: launch or join rallies (2–3 each), reinforce an ally (3) | 20–35 |
| 20–27 | Recover | heal all (2), top up musters (2), swap the garrison (3) | ≤ 10 |
| 27–30 | Tally | contribution, territory, alliance score, next window time | 1 |

- **Empty time ≤ 90 s**: while marches walk, a useful action (scout, reinforce, heal, chat) is ≤ 2 taps away; ≥ 1 decision per 90 s.
- War marches from staging ground to objective take 60–180 s ([world.md](world.md) places objectives to fit). Battle presentation 20–45 s at 1×, skippable after 3 s, 2× speed (battle-forge plays the resolver's beats; siege steps: siege-forge).
- A lost war session costs at most one night: median losses heal in ≤ 8 h without speed-ups ([combat.md](combat.md) sizes the beds).

| Fails when | Caught by |
|---|---|
| Late profile > 30 taps, or any profile > 5 min | [ ] session_audit check-in pass, both profiles |
| > 90 s with nothing useful to do in a war session | [ ] windowed replay of the 8.3 timeline, gaps logged |
| War results depend on being online at one single hour | [ ] two windows 12 h apart in the liveops calendar |

## 9. Anti-chore rules (PROPOSAL)

| # | Rule | Number |
|---|---|---|
| A1 | **Collect on open**: production is collected when the app opens; the resource bar counts up (`create_tween()`, `Tween.TRANS_QUART`, `Tween.EASE_OUT`) | 800 ms; sheds hold ≥ 15 h |
| A2 | **Standing orders**: each muster yard and gathering banner keeps its last order; "Refill all" / "Resend all" re-issue them. Short of resources → fill in the player's line priority and name the missing resource in one line | 1–2 taps for all |
| A3 | **Time-first batches**: training and gathering offer 1 h / 3 h / 8 h / "until I'm back (hh:mm)"; batch size is computed from the time | ends within ±15 min of the chosen time |
| A4 | **Auto-ask help**: default ON for helpable timers longer than the free threshold | 0 taps |
| A5 | **Auto-complete** plus "Finish all free" | 0–1 tap |
| A6 | **Hunt orders**: one march, up to 5 camps | 3 taps per hunt |
| A7 | **Red-dot budget**: dots only for claimable items and idle plates; never on offers or the shop ([ux.md](ux.md) owns the full rule) | ≤ 3 dots at open (median player) |
| A8 | **Push budget**: grouped per batch; quiet hours 22:00–08:00 local by default; never for offers | ≤ 4 per day |
| A9 | **Ceremony budget** (feel-forge): skippable after 300 ms; ≥ 3 completions merge into one digest | ≤ 1.5 s (90 frames at 60 fps) each, ≤ 2.5 s merged, ≤ 45 s per check-in |
| A10 | **No busywork orders** (§7 rule 2) | 0 |

Rejected on purpose: **build or research sequencing** (a second order waiting behind the first) removes the check-in's main decision — choosing the next building IS the game; **auto-help** removes the social gesture that makes help visible, and the tap costs 1 s; **server-side auto-refill while offline** needs server ticks (SKILL.md rule 5) and removes the reason to return.

| Fails when | Caught by |
|---|---|
| Maintenance taps > 12 per check-in | [ ] session_audit tap log by type |
| > 3 red dots at open, or any dot on a paid surface | [ ] ux_flow_probe screenshot at session open |
| A ceremony blocks input > 300 ms | [ ] feel-forge timing capture in frames |

## 10. Genre weak spots → our fix

| Genre weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| Second builder behind a paid status tier | plate count never sold; 2 crews from minute one | 2 → 3 by play |
| Energy wasted at the cap | bar + reserve; the 15-hour promise | 0% loss for gaps ≤ 15 h |
| Top spine upgrade of about four months base | single-timer ceiling (§4 rule 2) | ≤ 14 d, or progression.md's lower cap |
| Speed-up hoarding as the main strategy | honest inventory; change given back; events score work finished, not hourglasses spent ([liveops.md](liveops.md)) | held ≤ 2× queued |
| Paid shortcuts decide persistent war | gem-finish cap on muster and infirmary in war windows | owner decision |
| The loop becomes a "second job" | anti-chore rules A1–A10; tap budgets | ≤ 30 taps / 5 min |
| Red-dot fatigue | dot budget; no dots on offers | ≤ 3 at open |
| Long, time-zone-bound wars; burnout | 30-min sessions in ≤ 60-min windows, two windows 12 h apart | ≤ 60 min |
| Login rewards that climb only on consecutive days | a miss costs one step; writ needs 5 of 7 | −1 step |
| Tutorial never teaches late systems | a guided first rally as a rotating daily order in week 1 ([onboarding.md](onboarding.md)) | week 1 |
| Farm accounts feeding a main | bound chest rewards; helper pay cap; no helper pay from accounts < 72 h | 30 paid helps per day |

## 11. Harness, save, server cost, metrics

| Proof | Measures | Verdict line (PROPOSED, example values — qa-forge fixes the wording) |
|---|---|---|
| `core/session_audit.gd` + a check-in pass (qa-forge) | taps, seconds, idle plates at exit, mid and late | `CHECKIN OK - mid 24 taps 3m05s, late 30 taps 4m10s, idle 0` |
| loop sim, headless (new; qa-forge; path to confirm) | 7 days × 6/2/1-visit profiles: Resolve capture, shed loss, idle plate-hours, helps | `LOOP SIM OK - loss 0%/0%/38%, idle plate-hours <= 25%` |
| `tools/curve.py --helps` · `tools/econ_sim.py` | help math; chests and hourglasses as sources | tables in SYSTEM.md §5; `RED-TEAM #6` line |
| `ux_flow_probe`, `ux_touch_probe`, `a11y_audit`, `w1f_aspect_sweep` | tracker flows, touch targets, no flashing, 6 screen shapes | existing lines; `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| `core/sd_cost_probe.gd` | writes per player per day | € at 50,000 players inside the €200 budget |

**Save migration** (gameplay-forge): old saves load with Resolve full (`P0 = 150`, `t0` = load time), no standing orders, plate counts recomputed from S and buildings — never below what the save already had.

**Server cost** (estimate; measure before tuning): per player per day ≈ 15 plate starts + 8 help-all appends + 8 march orders + ≤ 24 camp resolutions + 3 chest claims ≈ 58 writes → ≈ 2.9 M writes per day, ≈ 87 M per month at 50,000 players (upper bound: every player engaged). Plates, Resolve and sheds are functions of time: 0 server ticks.
Budget test: 87 M writes per month use the whole €200 at €2.30 per million writes (€200 ÷ 87 M); the store cloud-forge picks must cost far less, because reads, chat and the map share the same budget. The owner's `core/sd_cost_probe.gd` answered ≈ €20/month worst case for the shipped game (game-director lessons) — re-run it with these write counts before tuning.

**After ship** ([numbers.md](numbers.md) §8): 4–8 sessions per day for engaged players; median session 6–12 min; D1 ≥ 40%, D7 15–20%, D30 6–10%; ≥ 70% of daily actives reach 100 order points; Resolve loss ≤ 5% for 2-visit players; ≥ 90% of check-ins exit with 0 idle plates.

**Handoff checklist** (a core-loop SYSTEM.md is not handed off until every box is ticked):
[ ] plate table filled with shipped values, or each cell marked PROPOSAL with its `data/*.gd` file · [ ] curve.py help table for the shipped `H`, `f` pasted · [ ] Resolve capture table for 6/2/1-visit profiles · [ ] check-in pass for mid and late ≤ 30 taps, ≤ 5 min · [ ] every daily order mapped to a §8.2 step · [ ] offer grep: 0 plate counts on paid surfaces · [ ] sd_cost_probe line with the loop's writes · [ ] §12 decisions sent to the owner.

## 12. Owner decisions required

1. Sell Resolve or not — recommended: never; if yes, ≤ 1 pool (150) per day, never inside war windows.
2. War-window cap on gem finishes for muster and infirmary plates — recommended ≤ 480 min per window.
3. The hourglass price constant `k` (spend; shop-forge proposes).
4. In-world names (story-forge canon): masons' crews, scriptorium desk, muster yards, infirmary, banners, Resolve, daily orders, weekly writ, hourglasses.
5. Any dial here that collides with a shipped sacred constant (the shipped value wins until the owner decides).
6. One reset clock (00:00 UTC) for every realm, or per-realm local time.
