# Flows — from choosing a target to the march coming home

The attack experience end to end, step by step, with taps, seconds and every failure state.
Defence is [defence.md](defence.md), rallies are [rally.md](rally.md), the battle itself is
[beats.md](beats.md) + [presentation.md](presentation.md), the result is [outcome.md](outcome.md).

A **tap** is one touch that changes state or opens a screen; scrolls and drags do not count
(design-forge `core-loop.md` §8). Marches are **banners** (march slots: 2 → 5 by play, never
sold — core-loop §2). Times exclude travel unless stated. All numbers are **PROPOSALS**; rules
(who may attack whom, loot, loss buckets, speeds) are design-forge `combat.md` / `world.md`.

## 1. Choosing a target

| Target | Actions on its card | Battle context (beats.md §4) | Rules owner |
|---|---|---|---|
| Barbarian camp | Attack · Hunt (up to 5 in a row) · Rally (large camps) | camp | world.md, core-loop §3 |
| AI lord outpost or castle | Scout · Attack · Rally | outpost / castle | world.md |
| Player castle | Scout · Attack · Rally · Bookmark | castle | combat.md |
| Player march on the map | Intercept · Scout | intercept | combat.md |
| Occupied resource node | Scout · Attack | field | economy.md |
| Alliance structure, landmark, stronghold | Scout · Rally | stronghold | world.md, alliance.md |
| Ally castle | Reinforce ([defence.md](defence.md) §5) | — | alliance.md |

**Find panel** (1 tap from the realm HUD): filters "Camps at my level — nearest 5", "AI lords
in range", "Enemy castles ≤ 3 min march", "Bookmarks". A row tap pans the camera to the target
(transition-forge, ≤ 700 ms) and opens its card: ≤ 2 taps from anywhere on the realm to a card.

**Target card** — a card covering ≤ 45% of the screen with the target still visible:

| Line | Content | Honesty rule |
|---|---|---|
| Header | name, alliance tag, relationship colour + shape marker | — |
| Strength | power band vs the player: much weaker / weaker / even / stronger / much stronger (±20%, ±60% bands) with a shape icon; exact power on tap | never hidden, never a guess dressed as fact |
| Intel | "Scouted 4 m ago" + the three facts that matter (garrison lines %, lord, wall %) or "Not scouted" | unknown fields show "?", never an estimate |
| Protection | ward state and time left; "Much weaker — <combat.md's rule, e.g. reduced loot>" when it applies | the rule text comes from combat.md |
| Travel | ETA per ready preset ("Preset 1: 2:14 · arrives 14:32") | server time (core-loop §4.6) |
| Actions | ≤ 3 buttons, the most likely first (Attack for camps, Scout for unscouted castles) | disabled buttons say why in one line |

| Fails when | Caught by |
|---|---|
| The player attacks blind because the card hid the intel age | [ ] `ux_flow_probe` screenshot: intel age visible on every castle card |
| A disabled button gives no reason | [ ] probe: every disabled action has a reason string (l10n key) |

## 2. Scouting — the decide loop

1. Card → **Scout** (1) → **Send scout** (1). A scout uses no banner (PROPOSAL; world.md).
2. Scout speed PROPOSAL 3× the fastest army line: a 2-minute war march is a 40 s scout trip.
3. The report arrives as a toast "Scout report: <target>" (6 s, 1 tap) and in the tracker.
   Report content and information tiers are report-forge's (`scout.md`) and combat.md's.
4. battle-forge owns the step after reading: the report's action row is **Attack with counter
   pick** (opens the march form pre-filled from §3 "Auto by counter") and **Rally**.
5. Target of a scout: sees "Scouted by <name>" in the tracker and a defence prompt
   ([defence.md](defence.md) §2) — the watchtower's first job.

| Failure | What the player sees | Next action offered |
|---|---|---|
| Target is warded | "Warded — 3 h 12 m. Scouts cannot enter." | Bookmark (1 tap) |
| Scout turned back (watchtower beats scout level) | the partial report with "?" fields, never "failed" alone | Scout again after research X (link) |
| Target moved before arrival | "Target moved — scout returning" | the new location if visible |

## 3. Forming a march — the march form

One screen, opened pre-filled by the last preset used against this target type.

| Zone | Content | Taps |
|---|---|---|
| Lords | primary + secondary portraits (commander-forge art); only the primary's talents and gear apply (design-forge `lords.md`) — the form says so under the pair | 2 per change |
| Lines | 5 rows: medallion, tier stack chips, slider, count | drag = 0 taps |
| Siege row | only when the target has structures: engine chips from siege-forge with load and speed | 1 per engine |
| Presets | 5 named slots; tap applies, hold saves | 1 |
| Auto by counter | fills lines against the scouted garrison using combat.md's counter graph (a helper in gameplay-forge; deterministic); greyed with "Scout first" when there is no report | 1 |
| Matchup strip | each own line → the enemy line it meets, with the favoured / even / unfavoured medallion from presentation.md §4 | 0 |
| Summary | capacity bar, ETA "2:14 · arrives 14:32", speed (the slowest line governs, named), load, Resolve cost (camps), infirmary line (below) | 0 |
| Send | bottom-right, thumb zone, 64 dp tall | 1 |

**Infirmary line** — the genre's death spiral is a full hospital: players lose troops they
thought were safe. The form shows free beds and the worst case: "Beds free 3,200 · at risk if
this march loses: 4,100". It turns WAX-rimmed (never flashing) when the worst case exceeds the
free beds; it never blocks Send. The worst-case share per context is combat.md's loss table.

Blocked sends — one line, the reason and the next useful action:

| Failure | Message (l10n key text) | Offered |
|---|---|---|
| No free banner | "All 3 banners are out — first back at 14:32" | Recall one (2 taps) |
| Lord busy | "Rowan is marching — back 2:10" | next preset with a free lord |
| Not enough Resolve | "Needs 10 Resolve — you have 4; 10 more at 15:06" | — |
| Target warded now | "Warded — 3 h 12 m" | Bookmark |
| Pact with the target's alliance | confirm: "You have a pact with [TAG]. Attacking breaks it for both alliances." | Cancel / Attack |
| No road | "No road to <target> — <the pass> is held by [TAG]" (world.md) | show the pass |
| Connection lost at Send | "Sending…" ≤ 3 s, then "Not sent — tap to retry". The send carries a request id; a retry never makes two marches | Retry |

| Fails when | Caught by |
|---|---|
| A preset send takes > 3 taps from the target card | [ ] `ux_flow_probe` flow C (§9) |
| The form lets a march leave with more than the free beds at risk and no warning shown | [ ] form unit test: worst case > beds → WAX rim present |
| A retried send creates two marches | [ ] cloud-forge idempotency test with a duplicated request id |

## 4. March out through the gate

transition-forge owns the camera shot ("marching out through the gate"); castle-forge owns the
gate and its `open` clip. battle-forge owns what leaves the gate and in what order.

| Rule | Number |
|---|---|
| Column order | cavalry vanguard → infantry with the lord's banner → spearmen → archers and crossbows → siege train last |
| Spacing | one squad every 250 ms (first time in a session); 125 ms on repeats |
| Horn | `bt_horn_depart` on the gate's first open frame (the War Horn, EQ-warhorn, is the fiction) |
| Length | first march-out in a session ≤ 2,500 ms; repeats ≤ 700 ms (the gate stays open 60 s after a departure) |
| Input | never blocked > 400 ms on a repeat action (transition-forge rule); a tap anywhere skips to the realm |
| Sent from the realm view | no gate shot: the march token appears at the castle gate on the map with a 400 ms banner-raise |

## 5. The march on the map

world-forge owns paths, speeds and map rendering; battle-forge owns what a march tells the player.

| Element | Rule |
|---|---|
| Line | relationship colour; 6 px at the 1080 px short side; dashes flow toward the target at 40 px/s. A hostile march aimed at the player: 8 px with a pulse ≤ 1 Hz |
| Token (mid zoom) | 3 figures of the march's largest line + lord banner + line medallion 44 px + ETA label 24 px |
| Token (far zoom) | banner icon 32 px only |
| ETA label | "2:14" under 10 min, "1 h 12 m" above; rounded up; refreshed at 1 Hz only while visible (core-loop §4) |
| March card (tap the token) | composition, ETA + arrival clock, **Recall** (2 taps), **Follow** (1), **Scout target** (2), speed-up items (war-window caps: core-loop §5.6) |
| Recall | the march turns back at once; time home = time already walked (a function of time); impossible after contact |
| Dead air | while a march walks, Scout target and Reinforce are ≤ 2 taps away (core-loop §8.3: dead air ≤ 90 s) |

## 6. Interception

Both marches are functions of time, so the server solves the earliest meeting point on the
target's path (combat.md / world-forge own the math and whether interception exists at all).

| Side | Steps | Taps | Sees |
|---|---|---|---|
| Interceptor | tap the enemy token → Intercept → Send (preset) | 3 | "Contact in 0:48 at Ashford ford" or the block "Cannot catch — it arrives first" |
| Target | — | 0 | token label "Intercept — contact 0:42"; tracker row; options Recall (2 taps) or keep going |
| Both | contact → field battle (beats.md context "intercept") | — | the normal watch offer (§7) |

| Fails when | Caught by |
|---|---|
| The shown contact time differs from the server's by > 1 s | [ ] `march_eta_probe` (extends world-forge's `march_probe`) |
| An interception the target could not see coming (no warning at all) | [ ] probe: every intercept creates a target-side warning row at launch |

## 7. Contact — watching the battle

| Situation | Behaviour |
|---|---|
| Following the march, or its contact point is on screen | enter battle view automatically (transition-forge shot ≤ 700 ms) |
| Anywhere else in the game | toast "Battle at <place> — Watch" for 6 s (1 tap); the report arrives either way |
| Two own battles within 5 s | the second waits: "Next: <place> — Watch" after the first outcome |
| A defence warning in the Near band during a watched battle | banner only ([defence.md](defence.md) §2); the camera never switches by itself |
| PvE after the player's first 10 battles | result chip only, "Watch" in the chip; setting "Auto-watch: war only / all / none" |
| App closed | nothing is lost: the battle resolved on the server; the report and the replay wait |

## 8. Coming home

1. The surviving march departs at `contact + T_fight` (beats.md §6) along the same path.
2. Castle view at arrival: the column enters through the gate ≤ 1,200 ms (skipped when not in
   castle view). Loot flies to the resource bar and counts up (core-loop A1, 800 ms).
3. Wounded go to the infirmary at resolution, not at arrival; the tracker shows "412 in the
   infirmary — Heal all" (2 taps). Details: [outcome.md](outcome.md) §4.

## 9. Tap budget per flow

| Flow | Steps | Taps | Seconds (no travel) |
|---|---|---|---|
| A Hunt 5 camps | camp → "nearest 5 at my level" → Send (core-loop A6) | 3 | ≤ 15 |
| B Attack an unscouted player castle | tap castle · Scout · Send scout · report toast · Attack with counter pick · Send | 6 | ≤ 90 incl. 20 s reading |
| C Attack a known target with a preset | tap target · Attack · Send | 3 | ≤ 10 |
| D Intercept a march | tap token · Intercept · Send | 3 | ≤ 10 |
| E Recall a march | tap token · Recall · confirm | 3 | ≤ 5 |
| F Try again after a defeat | outcome "Try <counter line>" (form pre-filled) · Send | 2 | ≤ 10 |
| G Watch a battle from anywhere | toast · Watch | 1 | — |

Every flow ≤ 3 taps to its first useful result except B, whose extra taps are the scouting
decision itself (pillar 10: every core action ≤ 3 taps).

| Fails when | Caught by |
|---|---|
| Any flow above exceeds its taps | [ ] `ux_flow_probe` flows A–G: `BATTLE FLOWS OK - 7 flows, max taps 6 (B)` |
| Touch targets under 48 dp on the form or the card | [ ] `ux_touch_probe` |
| The form breaks on a narrow screen shape | [ ] `w1f_aspect_sweep`: `ASPECT SWEEP OK - 6 shapes, 0 faults` |

## 10. Checklist — a new or changed attack flow

- [ ] Each step has taps, seconds, and every failure with its message and next action.
- [ ] Intel shown is only what the scout tier revealed; unknowns are "?".
- [ ] The infirmary line is present on every form that can lose troops.
- [ ] ETA and contact times are server-time functions; `march_eta_probe` green.
- [ ] No purchase button on the card, the form or the march card except speed-up items the player holds (money-law: no war imagery over a buy button).
- [ ] `ux_flow_probe`, `ux_touch_probe`, `w1f_aspect_sweep` verdict lines pasted.
