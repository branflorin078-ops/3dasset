# Alliance — belonging you can measure

The system that makes other players matter (game-director pillar 7, "Belonging"): ranks and offices, help, two currencies, charters (research), gifts, territory, rallies across time zones, leadership tools, hopping rules and public pacts. Implementation: **gameplay-forge** (rules, data, save), **ui-forge** (screens S6, calendar, badges), **cloud-forge** (membership, logs, server-side permission checks), **chat-forge** + **mail-forge** (§13), **world-forge** (Chapterhouse, standards, strongholds), **battle-forge** (rally flow), **story-forge** (names), **qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md) §7.

**Every number is a PROPOSAL** (verify against `data/alliance.gd`, path to confirm) unless it quotes a canonical fact or [core-loop.md](core-loop.md); a shipped sacred constant keeps its value and this file's number becomes a proposal to the owner. All names are proposals for story-forge canon (§16 lists the name clashes they avoid). `E` = embassy tier (1–6) of the member who asks for help (the embassy in the castle sets `H`; verify `data/buildings.gd`); `S` = spine tier 1–6 (the keep's age, which [progression.md](progression.md) writes `A`); "active" = opened the game inside the named window (48 h, 7 d); the day resets at 00:00 UTC; a season = **35 days** (1 Truce week + 4 contest weeks, [liveops.md](liveops.md) §3.1).

## 0. The four questions

- **Want**: time back (help); shared strength (charters, territory); standing (rank, office, the alliance's name on the realm map); safety in numbers (rallies, reinforcement).
- **Obstacle**: other members' presence across time zones; Treasury, earned only by members' effort; trust (ranks, two-key actions); rival alliances.
- **Wait**: first help ≤ 15 min after the first request (waking hours, median alliance); first charter level on day 1; full charter tree 33 / 76 / 100 days (top / median / small, §5); 100 seats ≈ day 47 for a median alliance that funds seats first (§10).
- **Witness**: each help shows its minutes; each gift names the deed and the member; pacts appear in the realm feed; territory tints the realm map; rank badge and office on the profile card.
- **Free path**: every alliance benefit comes from membership and play; the one personal gate is `H`, by the member's own embassy tier. Nothing in the alliance is sold (§4 rule 4).

## 1. The alliance in the five timescales ([core-loop.md](core-loop.md) §1)

**Glance**: Help all, 1 tap ("Allies saved you 42 m"). **Check-in** (inside core-loop §8.2, no new taps): Help all is step 2 (1 tap); step 10 becomes one sheet — **Claim all** (chests + alliance gifts, 1 tap) + **Donate ×5** to the recommended charter (1 tap) = the same 2 taps core-loop budgets. A rally join from its chat card (2 taps) happens when the card appears, outside the plate refill. **Day**: the order "Give to the alliance" = 1 donation or 1 works march (core-loop §7, 10 points; its wording "gift or research donation" should read "donation or works march" — members do not send gifts here). **Week** (contest weeks): 2–3 scheduled rallies at muster hours, war windows on Tue / Thu / Sat, a charter row, a Great chest about every 6 days. **Season** (35 days): alliance standing → banner trims (liveops.md §3.4); pacts end on Truce day 1. No alliance reward needs the player online at one single clock hour (§8).

**Where it lives**: the embassy in the castle and the HUD alliance button open ui-forge's screen S6 — 8 tiles (Help, Gifts, Members, Charters, Territory, Rallies with the muster calendar, Pacts, the Roll) + the Quartermaster from the Merit balance in the header; each ≤ 2 taps from the castle or the realm. Red dots only for claimable gifts and, for the Gatekeeper, waiting applicants (core-loop A7) — never for charters, rallies or pacts.

**Checks**: [ ] session_audit check-in pass — fails when: the alliance steps push core-loop §8.2 step 10 above 2 taps or the late profile above 30 · [ ] ux_flow_probe — fails when: any S6 tile is > 2 taps from the castle or the realm.

## 2. Ranks, offices and permissions

Five ranks; rank 4 holds four named offices, so the leader hands off whole jobs. The genre gives all officers the same broad powers — nobody owns a job, so the leader ends up doing all of them.

| Rank | Name | Seats | Reached by |
|---|---|---|---|
| 5 | **Liege** | 1 | founding, transfer or succession (§9) |
| 4 | **Officer** — Marshal (war, rallies, pacts), Treasurer (Treasury, charters, standards), Crier (announcements, recruiting, mail), Gatekeeper (membership, chat order) | 4, one per office; one person holds ≤ 1 office | appointed by the Liege |
| 3 | **Companion** | no cap | promoted by the Gatekeeper or Liege |
| 2 | **Yeoman** | no cap | automatic at 72 h membership + 30 helps given, or promoted |
| 1 | **Recruit** | no cap | joining |

| # | Action | Liege | Officer | Companion | Yeoman | Recruit |
|---|---|---|---|---|---|---|
| 1 | Help, donate, claim gifts, join or pledge to rallies, chat, buy in the Quartermaster, set own "On leave" (§9) | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | Read the Roll; own contribution score and others' badges; last-active buckets | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 | Launch a rally on a stronghold or AI lord | ✓ | ✓ | ✓ | ✓ | — |
| 4 | Launch a rally on a castle; pin map targets (≤ 10 pins per alliance) | ✓ | ✓ | ✓ | — | — |
| 5 | Cancel another member's rally before departure (a leader may always cancel their own) | ✓ | Marshal | — | — | — |
| 6 | Schedule rallies; set muster hours; Banner League sign-up, window and roster ([liveops.md](liveops.md) §4.4) | ✓ | Marshal | — | — | — |
| 7 | Set the recommended charter; spend Treasury on charters; place, move or abandon standards | ✓ | Treasurer | — | — | — |
| 8 | Place or move the Chapterhouse, raise its tier | ✓ | — | — | — | — |
| 9 | Accept applicants; set auto-accept and auto-release rules (§9) | ✓ | Gatekeeper | accept only, if the Gatekeeper allows | — | — |
| 10 | Send an invite card (chat-forge `invite`) | ✓ | Crier, Gatekeeper | ✓ (arrives as an application) | — | — |
| 11 | Promote or demote within ranks 1–3 | ✓ | Gatekeeper | — | — | — |
| 12 | Release (kick) a member | ranks 1–4 | Gatekeeper: ranks 1–2 | — | — | — |
| 13 | Chat order in alliance chat: remove a message, mute 1 h or 24 h (chat-forge safety §8) | ranks 1–4 | any officer: ranks 1–3 | — | — | — |
| 14 | Pinned announcement, `@all` (≤ 3 per day), `@council` (≤ 10 per day) (chat-forge channels §4–5) | ✓ | any officer | — | — | — |
| 15 | Scheduled announcements, alliance mail, alliance profile and recruiting text | ✓ | Crier | — | — | — |
| 16 | Propose a pact; sign or end one (two keys, §12) | proposes; key 1 | Marshal proposes; any officer turns key 2 | — | — | — |
| 17 | Exact last-active hours; the sorted contribution list (§4 rule 2) | ✓ | ✓ | — | — | — |
| 18 | War Council channel (chat-forge) | ✓ | ✓ | if the Liege grants it, per member | — | — |
| 19 | Appoint or remove officers; grant War Council access | ✓ | — | — | — | — |
| 20 | Apply for an office that has been empty ≥ 48 h | — | — | ✓ | — | — |
| 21 | Change name, tag, sigil or tinctures (once per 30 days) | ✓ | — | — | — | — |
| 22 | Name heir or regent; transfer leadership; disband; merge (§9, §10) | ✓ | merge key 2; "take the seat" during a disband | — | — | — |
| 23 | Lead an alliance move at a Truce (liveops.md §7 rule 6; each member confirms, nobody is moved without consent) | ✓ | Marshal | — | — | — |

1. **The server enforces the matrix** (cloud-forge): every alliance action is ONE server call that re-reads the caller's membership row (alliance, rank, office, grants) in the same transaction as its write. The client's claimed rank is never trusted; the client only hides buttons (ui-forge S6). A rank or office change applies from the next call (0 s permission cache). A refused call writes nothing and returns a reason code ("Treasurer or Liege only"); refused officer-level calls are also written to the Roll. A regent (§9) holds every Liege power except row 22.
2. **Safety limits** (server counters, reset 00:00 UTC): releases ≤ 5 per officer and ≤ 10 per alliance per 24 h (auto-release not counted); promotions + demotions ≤ 20 per officer per 24 h; chat order ≤ 50 actions per day (chat-forge); one officer's Treasury spends ≤ 50% of the balance per 24 h — above it the Liege turns a second key. A stolen officer account cannot empty the alliance or its Treasury.
3. **Two keys**: pacts (Liege + one officer), merges (the same on each side), Treasury spends over the 50% limit. Transfer needs the receiver's accept; disband waits 72 h (§9). An officer removed from office keeps nothing: their scheduled rallies and announcements stay, listed for the next holder to keep or cancel.
4. **The Roll** (chat-forge calls it the alliance log) records every officer action, refusal and Treasury spend, visible to all members, kept 30 days. Members see last-active buckets ("today", "this week", "over 7 days"); officers see hours.
5. Rank badges (RNK) and office seals are Blender-made art (ui-forge + blender-forge), shape AND word, never colour alone; ≥ 48 dp when tappable.

**Checks**: [ ] alliance_perm_test: 23 actions × 5 ranks × 4 offices + grants, allowed and refused, sent as crafted server calls — fails when: a refused call writes anything · [ ] alliance_perm_test limit cases — fails when: one account releases > 5 members, or spends > 50% of the Treasury in 24 h without the second key · [ ] a11y_audit on the member list — fails when: a rank is readable only by colour.

## 3. Help — the dials quoted from core-loop §6

[core-loop.md](core-loop.md) §6 owns the formula and its worked math. Each help removes `h = max(c·R, f)`, `c = 1%` of the remaining time `R`, `f = 120 s`, raised to **180 s by the charter Open Door** (§5); `H = 10 + 4·(E − 1)` = 10, 14, 18, 22, 26, 30 helps per request; helpable: build, research, heal — never training. Added here:

| Dial | PROPOSAL | Why |
|---|---|---|
| Helper reward | **5 Merit per help**, first 30 helps per day (150 Merit) | ≈ 1.25 min of hourglass per help at store prices (5 ÷ 4 Merit per minute, §4); 30 helps ≈ 5 of core-loop's 8 daily Help-all taps |
| Unpaid helps | after 30 per day; from accounts < 72 h old or at S1; between accounts linked by device ([economy.md](economy.md) F8) | the ally still gets the time; farm accounts earn nothing |
| Help all | helps every open request (≤ 50 per tap) = ONE help-log append | core-loop §6 cost rule |
| Requests | auto-asked (core-loop A4); live until the timer ends; **never a push** | help is ambient, never a summons |
| Join hook | a new member's requests sit at the top of every ally's list for 24 h ("New: Rowan's first request") | first help ≤ 15 min |
| Saturation | ≥ H + 1 = 31 members active in the same 4-h window give every request its full H | why seats can stop at 100 (§10) |

**Checks**: [ ] alliance_sim first-help line — fails when: median first help > 15 min (07:00–23:00 asker's local time) in a 45-active alliance · [ ] server cap test (shared with core-loop) + hop_exploit_test — fails when: a request gets > H helps, or a helper is paid past 30 per day or again after a leave-and-rejoin.

## 4. Two currencies — Treasury and Merit (the free-rider fix)

Pattern ([benchmark.md](benchmark.md) §7): collective goods paid by many small acts, each actor paid privately, so riding free earns nothing and contributing always pays. **Our move**: every act counts the same for a small castle and a large one — a donation costs 15 min of the donor's OWN production, never a flat pile of resources and never gems, so a large account cannot buy standing.

| | **Treasury** (collective, counted in marks) | **Merit** (personal) |
|---|---|---|
| Earned by | donations (10 each); Spoils (300 × stronghold level per kill); held landmarks: `50·P − 8·P^1.5` marks per day for `P` held points (hold values 1 / 2 / 4 / 8 / 16 by tier; best +289 at 17 points, negative above 39 — [world.md](world.md) §3 rule 4), settled on read; event milestones (Banner League, liveops.md §4.4), each ≤ 4,500 (one day of a median alliance's donations) | helps 5; donations 10 (15 on the recommended charter); rallies joined 20 (first 5 per day); works marches 1 per march-minute (≤ 60 per day); war windows 50 (≥ 1 engagement; ≤ 2 per war day — 3 war days per contest week, 0 in the Truce week, [liveops.md](liveops.md) §3.2) |
| Spent on | charters (§5), standards, upkeep, Chapterhouse tiers (§7) | the Quartermaster (below) |
| Spent by | Liege and Treasurer; every spend in the Roll | the member |
| Leaves the alliance | never — no withdrawal, no transfer to a member | travels with the member (§11) |
| Cap | none; standard upkeep drains it | 10,000 (≈ 28 days of median income); at cap earning pauses and the store says so |
| Sold for money | never | never |

**Merit per day** in a contest week, median free player (P50) → maximum: helps 150 → 150; donations 125 (10 donations, half on the recommended charter) → 360 (24 × 15); rallies 40 → 100; works 20 → 60; war windows 21 (one window on each of 3 war days: 150 ÷ 7) → 43 (two windows: 300 ÷ 7). **Total ≈ 356 → 713 per day (2,490 → 4,990 per week)**; in the Truce week 335 → 670.

**The Quartermaster** (alliance store). The genre has officers stock the store from collective funds; ours has endless stock and every cap is **per player per week**, carried across alliances.

| Item | Merit | Weekly cap | Merit per week at cap | Note |
|---|---|---|---|---|
| 15 m Works hourglass | 60 | 14 | 840 | 4.0 Merit per minute; core-loop §5 names this store as its source |
| 1 h Universal hourglass | 220 | 7 | 1,540 | 3.7 per minute (degressive, as core-loop §5) |
| Resolve 50 | 150 | 7 | 1,050 | lifts the pool toward 300 (core-loop §3) |
| Field journal (lord XP, the 480-XP size) | 400 | 2 | 800 | [lords.md](lords.md) §4 names this size; 960 XP per week = +8% on its 1,680 XP per day |
| Gold leaf, 1 pouch | 250 | 4 | 1,000 | Fine and Masterwork tempering (lords.md §9 lists this store as a source); pouch size: economy.md |
| Gathering writ, 8 h | 200 | 3 | 600 | +20% gathering ([economy.md](economy.md) §5 rule 7) |
| Peace ward, 8 h | 1,500 | 1 | 1,500 | never inside a war window or while a hostile march is inbound ([combat.md](combat.md) §9) |
| Chapterhouse summons (relocate into own territory) | 1,000 | 1 | 1,000 | same locks as the ward; relocation rules: world.md |
| Plain Seal | 150 | 5 | 750 | lords.md counts 5 per week in the free Seal total |
| Tabard dyes, pennon patterns | 1,500–3,000 | once each | — | stat-free cosmetics |

Weekly shelf capacity **9,080 Merit** > the maximum income of 4,990, so nobody hoards Merit waiting for stock. Favour for Guild Patronage is NOT sold here: [monetization.md](monetization.md) §6 rule 1 feeds Favour from activity points only.

1. **Every benefit reaches every member**: charters, gifts and help received are not rationed. The free rider loses Merit (0 earned) and seat safety (§9 "idle contributor" rule).
2. **Contribution score** (weekly) = donations × 10 + helps × 2 + rally joins × 20 + works minutes (median member ≈ 1,540). Officers see a sorted list; members see their own score and others' badges only ("Steady" ≥ 500, "Stalwart" ≥ 1,500 per week) — no public ranking, so giving never becomes a race.
3. **Donations**: 20 charges, regen 1 per 60 min (full in 20 h, so the 15-hour promise holds); "Donate ×5" = 1 tap; resource by charter row (§5); the donor's cost is ≤ 24 × 15 min = 6 h of one resource per day (economy.md counts it as a sink). Accounts < 72 h old or at S1–S2 earn Merit but add **0 Treasury** (farm accounts cannot fund a main's alliance); a realm's first 7 days are exempt, so new alliances can fund Open Door on day 1.
4. **Never sold**: rank, seat, Treasury, charter, help count, gift level, pact, Merit. Gems cannot be donated.

**Checks**: [ ] alliance_sim Merit line — fails when: median member's Merit balance > 7 days of income at day 30 (hoarding) · [ ] donation unit test: S3 and S6 donors add 10 each — fails when: a donation's Treasury depends on city size or payment · [ ] shop-forge offer-data grep returns 0 — fails when: any alliance good appears on a paid surface · [ ] ward/summons server test — fails when: either starts inside a war window or with a hostile march inbound.

## 5. Charters — alliance research funded by donations

Five branches × six rows; a row opens when the row above it in the same branch is complete. Cost per level `C_r = 3,000 · 1.55^(r−1)` Treasury (rounded to 50) × size factor `s = clamp(M / 40, 0.5, 1)` (`M` = 7-day-active members) × realm discount `(1 − d)`. Progress is stored as a fraction (a donation adds `10 / price_now`), so a change in `M` never loses progress. A charter works the moment it fills: no timer, no tick.

**Realm discount** (our move — the genre lets the first alliance keep its lead for good): `d = 30%` once ≥ 3 alliances in the realm hold that level, `50%` once ≥ half of the realm's alliances with ≥ 20 members hold it ("Known in the realm: −30%"). `s` counts only ACTIVE members, so releasing inactive players never makes research cheaper; from 20 to 40 actives the price per active member is constant, and growth above 40 costs nothing.

| Row | Cost/level | Fellowship | Stores | Works | Arms | Land |
|---|---|---|---|---|---|---|
| 1 | 3,000 | Open Door: help floor 120 → 180 s (1 lv) | Foragers: gathering +3%/lv (3) | Masons: build speed +1%/lv (3) | Drill: march speed +2%/lv (3) | Surveyors: standard cost −5%/lv (3) |
| 2 | 4,650 | Great Table I: +5 seats (1) | Cellars: warehouse allowance `Wp` +5%/lv (3) | Scribes: research speed +1%/lv (3) | Rally Horn: rally capacity +5%/lv (3) | Roadwardens: march speed in own territory +5%/lv (3) |
| 3 | 7,200 | Feasting: gift XP +10%/lv (3) | Wagonways: gathering load +4%/lv (3) | Masons II: build +1%/lv (3) | Shield Wall: troop defence +0.5%/lv (3) | Stewardship: standard upkeep −5%/lv (3) |
| 4 | 11,150 | Great Table II: +5 seats (1) | Foragers II: gathering +3%/lv (2) | Scribes II: research +1%/lv (2) | Keen Edge: troop attack +0.75%/lv (2) | Beacons: marches into own territory seen 30 s earlier/lv (2) |
| 5 | 17,300 | Great Table III: +5 seats (1) | Herb Gardens: healing cost −5%/lv (2) | Master Builders: build +1%/lv (2) | Surgeons: infirmary beds +5%/lv (2) | Summons: relocation cooldown −12 h/lv (2) |
| 6 | 26,850 | Great Table IV: +5 seats (1) | Market Rights: caravan tax 20% → 15% (1; economy.md F2) | Great Works: research +2% (1) | Iron Discipline: troop health +1.5% (1) | High Walls: Chapterhouse and standard durability +10% (1) |

Totals: 64 levels (13 / 13 / 15 / 9 / 9 / 5 per row), **597,750 Treasury** at full price. Branch maxima: gathering +15%, build +8%, research +7%, **troop attack / defence / health +1.5% each** — collective combat stats stay small so charters never bury a counter (+20–50%, [numbers.md](numbers.md) §4; combat.md §5 books them as ≈ 0.05 TS in its realm budget).

Days to finish with all net Treasury on charters (landmark and event Treasury left out — a bonus on top). Net Treasury per day: top 90 active × 16 donations × 10 + 5 kills × level 5 × 300 − upkeep 3,600 = 18,300; median 45 × 10 × 10 + 2 × 3 × 300 − 800 = 5,500; small 12 × 10 × 10 + 0.5 × 2 × 300 − 0 = 1,500.

| After row | Treasury (full price) | Top: 90 active, s 1, d 0% | Median: 45 active, s 1, d 30% | Small: 12 active, s 0.5, d 50% |
|---|---|---|---|---|
| 1 | 39,000 | 2.1 d | 5.0 d | 6.5 d |
| 2 | 99,450 | 5.4 d | 12.7 d | 16.6 d |
| 3 | 207,450 | 11.3 d | 26.4 d | 34.6 d |
| 4 | 307,800 | 16.8 d | 39.2 d | 51.3 d |
| 5 | 463,500 | 25.3 d | 59.0 d | 77.3 d |
| 6 | 597,750 | **32.7 d** | **76.1 d** | **99.6 d** |

Everything (charters + Chapterhouse tier 6 + standards: 200 top, 60 median) ≈ 72 d top (1,309,968 ÷ 18,300), ≈ 120 d median (662,194 ÷ 5,500). The top : small spread is 3 : 1, not the 12 : 1 of one flat price with no discount (398 d vs 33 d).

1. The Treasurer (or Liege) sets one **recommended charter**; donations to it pay 15 Merit instead of 10. Any open charter accepts donations.
2. Donated resource by row: rows 1–2 food or wood, 3–4 stone, 5–6 iron (the resource ladder of numbers.md §2; economy.md may override).
3. Joining gives the new alliance's charters at once; leaving loses the old ones (belonging, not a reward — nothing to gain by hopping).
4. Each charter has a Blender-made icon (30 icons, ui-forge + blender-forge; never line glyphs); the card shows the effect as a number before and after ("gathering +6% → +9%").

**Checks**: [ ] alliance_sim charter line — fails when: median full tree < 45 d (nothing left to fund) or > 120 d, or a small alliance needs > 2 d for Open Door or > 7 d for row 1 once the 50% discount applies · [ ] data lint (gameplay-forge) — fails when: the sum of charter combat stats exceeds combat.md's budget.

## 6. Gifts — deeds shared, never purchases

Pattern: one member's deed becomes a small gift to every member, so success is shared and seen. **Our move**: only deeds in play create gifts. A purchase creates at most an anonymous cosmetic token — it never raises gift level, never gives resources or hourglasses, never names the buyer (owner, §16).

| Gift | Created when | Each member receives ("own output" = minutes of that member's own production) | Gift XP |
|---|---|---|---|
| **Hunt** | a member first clears a camp level (camp ladder, world.md) | 5 min own food + wood | 1 |
| **Spoils** | the alliance destroys a stronghold of level L (1–6, world.md §5) | 10·L min own output (all five) + one 15 m Universal at L ≥ 4 | 5·L |
| **Feast** | a member reaches a spine tier, unlocks a troop tier in any line, or completes a lord's four-piece set (≤ 1 per member per day) | 15 min own output + 5 Resolve | 10 |
| **Newcomer** ([onboarding.md](onboarding.md) §5) | a member < 7 days old closes onboarding chapter 3 and stays 72 h; ≤ 10 per alliance per week | 5 min own output | 2 |
| **Great chest** | every 400 gift XP | 1 h Universal + 1 h own output | — |
| **Patron token** | any member's purchase — buyer never named, ≤ 3 per alliance per day; a refund withdraws its unclaimed tokens | 1 cosmetic fragment (10 = a pennon dye or a chat sticker, chat-forge) | 0 |

**Gift level** 1–10, +5% contents per level (level 10 = +45%); XP to the next level `200 · 1.3^(ℓ−1)` = 200, 260, 338, 439, 571, 743, 965, 1,255, 1,631 (6,402 in total). Median ≈ 70 XP per day (10 hunts, 2 level-3 strongholds, 3 feasts: 10 + 30 + 30) → level 10 at ≈ day 91, a Great chest every ≈ 6 days (400 ÷ 70); top ≈ 205 (20 hunts, 5 level-5 strongholds, 6 feasts) → day 31. Feasting (§5) shortens both by up to 23%.

1. **Daily cap per member: 240 min of own output from gifts** (Great chests excluded); above it contents turn into gift XP. Median ≈ 155 min per day at level 1 (50 + 60 + 45), 225 at level 10; a top alliance (≈ 440 raw: 100 + 250 + 90) hits the cap — its edge over a median alliance is ≤ 85 min of production per day. In week 1, when members first-clear several camp levels a day, the cap binds for every alliance.
2. **Not retroactive**: a member receives only gifts created after joining; Spoils and Great chests need ≥ 24 h membership. Gifts are bound to the account; resources land in the yard under the warehouse allowance (economy.md §7 rule 3, core-loop §7 rule 7).
3. "Claim all" = 1 tap (shared with the chests, §1); each line names the deed ("Spoils — level-4 stronghold, rally led by <member>"). Unclaimed gifts expire after 72 h; on leaving, pending gifts are claimed automatically.
4. A gift is ONE append to the alliance gift log; claim-all moves one per-member cursor — never one write per member per gift (§15).

**Checks**: [ ] alliance_sim gift line — fails when: gift output > 240 min per member per day · [ ] shop-forge offer-data grep + gift unit test — fails when: a purchase creates a non-cosmetic gift, or names the buyer · [ ] hop_exploit_test — fails when: a new member receives gifts created before joining.

## 7. Territory — the Chapterhouse and standards

[world.md](world.md) owns map geometry, landmarks, strongholds, relocation and the relationship palette; this section owns who, cost, upkeep and cap.

| Item | Rule (PROPOSAL) |
|---|---|
| **Chapterhouse** (the alliance's seat on the realm map; a chapterhouse is the hall where a medieval order met; world.md and older drafts say "the Hall" — renamed, §16) | one per alliance, placed by the Liege; tier 1 costs 0 Treasury + 300 works march-minutes, so a new alliance plants it on day 1. Tiers 2–6 cost 10k / 20k / 35k / 55k / 80k Treasury (200k total) + 300 × tier works-minutes (6,000 in total, ≈ 7 days of a median alliance's 900 per day); each tier +8 seats (§10); the tier card shows the next tier's render at ≥ 40% of screen height (ART SHOWN BIG) |
| **Standard** (a planted war flag that marks alliance ground) | placed by the Treasurer or Liege, touching own territory. Cost of the b-th standard `500 · 1.15^floor((b−1)/10)`: #1 500, #51 1,006, #101 2,023, #200 7,116; 60 standards 43,769 in total, 200 standards 512,218 |
| Cap and fading | cap `min(200, 3 × 7-day-active members)` (median 45 actives → 135; small 12 → 36) — territory follows activity, not history. Over the cap, or at Treasury 0, the standard farthest from the Chapterhouse fades every 6 h; the Chapterhouse never fades |
| Upkeep | first 20 standards free, then 20 Treasury per standard per day (−5% per Stewardship level); a function of time, settled on any Treasury read — 0 server ticks. Median 60 standards = 800 per day (13% of gross income 6,300); top 200 = 3,600 (16% of 21,900) |
| Works | members build the Chapterhouse and standards with works marches: Merit 1 per march-minute (≤ 60 per day) |
| Benefits | gathering +20% inside ([economy.md](economy.md) §6), march speed inside (Roadwardens), Chapterhouse summons, owned resource points — values in economy.md and world.md |
| No seats from standards | the genre adds a member seat per 10 territory markers; we do not — seats never reward sprawl |

**Fiction and art**: the Chapterhouse is a 3D building made through blender-forge, following the tier language of game-art-director `references/buildings.md` (tier 1 rough timber → tier 6 fine ashlar with gilt civic trim). Chapterhouse, standards and pennons carry the alliance's two tinctures only through the tint mask (blender-forge `references/architecture.md` §7); the sigil is ALS art (game-art-director); tinctures never match a relationship colour or a line accent.

**Checks**: [ ] alliance_sim standard-vs-activity line — fails when: an alliance with < 10 active members still holds > 30 standards after 14 days · [ ] sd_cost_probe: 0 scheduled writes — fails when: upkeep or fading needs a server job · [ ] contrast_test + a11y_audit on the realm-zoom map — fails when: a tincture pair reads as a relationship colour.

## 8. Rallies across time zones

[combat.md](combat.md) §9 owns rally capacity, the < 2% token-join floor and losses; battle-forge the rally flow and its taps; [liveops.md](liveops.md) the war windows (two ≤ 60-min windows 12 h apart on Tue, Thu and Sat of contest weeks, core-loop §8.3). An alliance's war-day score is the better of its two windows (liveops.md §3.4), so no time zone is behind. This section: scheduling and joining.

| Tool | Rule (PROPOSAL) |
|---|---|
| Rally wait, pledge | 5 / 10 / 30 min against players, up to 60 min on PvE ([combat.md](combat.md) §9), or **scheduled** 15 min – 24 h ahead on a 15-min grid, shown in each member's local time. A scheduled rally carries a **Pledge** button (2 taps): the march leaves at launch if the member is online, or offline if they allowed it |
| **Muster hours** | the Marshal sets ≤ 3 per day. The calendar shows a 24-hour activity strip (7-day-active members per hour, last 14 days, in the viewer's local time) and the coverage: share of 7-day-active members usually active within ±1 h of a muster hour. Target ≥ 60%. Counts only — the strip never shows who is online when |
| **Standing pledge** (auto-join) | PvE targets only (strongholds, AI lords, the Warlord's Hold of liveops.md §4.2): ≤ 20% of the field army by default (max 50%), ≤ 3 per day (max 5), a lord preset, never the last free march banner (core-loop §2). It fills only places still open at 50% of the wait — people first |
| Castle rallies | no offline auto-join: attacking a castle is the costliest loss context ([combat.md](combat.md) §6). A "war pledge" inside realm war windows, ≤ 20% of army, is an owner decision (§16) |
| Rewards | stronghold rewards: **50% shared equally** among participants, 50% by damage share (the genre pays by damage share alone, so the biggest accounts take most); then liveops.md R8's floor (40% of the median share) and cap (3×) — world.md §5 works the example. The equal half needs a march ≥ 2% of rally capacity (combat.md §9 rule 6) and ≥ 20% of the rally's median march (world.md's proposal, accepted). ≤ 5 reward shares per player per day — the same 5 rallies that pay 20 Merit. Auto-joiners earn the same |
| Guards | auto-join needs S3+ and an account ≥ 72 h old (farm guard); no auto-join while an attack on the member's castle is incoming; departures use the march arrival trigger of world.md (no new server job) |

**Fairness target**: three clusters (UTC−5, UTC+1, UTC+8; 15 members each) — every muster hour fills ≥ 80% of rally capacity with standing pledges on, and a member never online at a muster hour still earns ≥ 60% of the median member's stronghold rewards.

**Checks**: [ ] alliance_sim rally line, 3 clusters — fails when: fill < 80% at any muster hour, or the never-online member earns < 60% of the median stronghold rewards · [ ] server test (combat side, cloud-forge) — fails when: an offline member's troops join a castle rally without a war pledge · [ ] rally unit test — fails when: auto-joiners take places before 50% of the wait.

## 9. Leader burnout tools

Target: with auto-rules on, the Liege has **0 required daily actions**, and a week of leadership takes **≤ 15 min** (set the recommended charter, schedule ≤ 3 rallies, glance at the Roll). Measured, not hoped.

| Tool | Rule (PROPOSAL) |
|---|---|
| Offices | four officers own four jobs (§2). An office empty for 48 h shows "Seat open" to Companions, who may apply. An officer 7 days without a session loses the office (becomes a Companion); mail to the Liege |
| Scheduled announcements | ≤ 5 queued; once, daily or weekly; ≤ 300 characters (chat-forge's pinned limit is 400); shown as the pinned line by schedule on read (0 server jobs); optional alliance mail (mail-forge); optional push (members opt in; the push service's scheduled send) |
| Auto-accept, auto-promote | filters: S ≥ x; language; activity overlap ≥ y% with the alliance strip; alliances in the last 30 days ≤ z. Others wait for the Gatekeeper; applications expire after 72 h. Recruit → Yeoman at 72 h + 30 helps given |
| Auto-release, inactive | off / 7 / 10 / 14 days without a session; default 14 with "only when ≥ 90% full" ON; warning mail at N − 3 days; members "On leave" exempt; a released member may rejoin within 30 days with no cooldown, as a Yeoman |
| Auto-release, idle contributor | optional: < 100 contribution in 14 days while active |
| On leave | a member marks ≤ 14 days, once per 30 days; inactivity clocks pause. A Liege on leave names a regent (any officer) with all powers except transfer and disband |
| **Succession** | Liege without a session: day 5 mail to officers; day 7 mail to all + pinned countdown; **day 10** leadership passes to (1) the named heir if active in the last 48 h, else (2) the officer with the most 30-day contribution among those active in 48 h, else (3) the Companion with the most, else (4) the Yeoman with the most; nobody active in 48 h → "fading" (§10). The old Liege becomes a Companion. Evaluated on the next alliance read — no server job |
| Transfer | voluntary: 24 h delay, cancellable, the receiver must accept (a stolen account cannot hand the alliance away at once) |
| Disband | 72 h delay; any officer may "take the seat" in that time — leadership passes to them and the disband is cancelled. Treasury is lost on disband |

Rejected: **votes of no confidence** (politics become the game; burnout grows); **one leader with every power** (the genre's burnout source).

**Checks**: [ ] alliance_sim leader-minutes line + ux_flow_probe on the 3 weekly tasks — fails when: Liege leadership > 15 min per week in the sim · [ ] succession_probe (clock skip, 6 cases) — fails when: leadership does not pass at day 10, passes to someone inactive, or a member "On leave" is released.

## 10. Size, growth, founding, merging and joining

**Seats = 40 + 5 × (Great Table levels, 0–4) + 8 × (Chapterhouse tier − 1, 0–5)** → 40 … 100. Hard cap **100** (the genre sits around 150 [unverified]). Why 100: help saturates at H + 1 = 31 members active in one 4-h window (§3), so members beyond about 50 active add Treasury, not help; chat stays readable (100 members × ~6 lines = 600 lines per day, chat-forge); a realm holds more full alliances, so more of them contest the top ([world.md](world.md)). Seat path for a median alliance: Great Table I–IV need the whole Fellowship branch (84,550 at full price, 59,185 after the 30% discount ≈ 11 days), then Chapterhouse tiers 2–6 (200k) → 100 seats ≈ day 47 (259,185 ÷ 5,500) when seats come first.

| Rule | PROPOSAL |
|---|---|
| Founding | S ≥ 3; costs 8 h of own output (all five), never gems; name and 3–4 letter tag (through chat-forge's name filter), sigil (ALS), two tinctures; one founding per account per 30 days |
| Fading, merging | < 10 seven-day-active members for 14 days → listed on the merge board. A merge needs both Lieges (two keys per side); members move in one step with no cooldown; each charter keeps the higher level; Treasury adds up; absorbed officers become Companions; the absorbed Chapterhouse is removed, its touching standards transfer, the rest fade |
| Suggestion, nudge | when [onboarding.md](onboarding.md) §5 places it (minute ≈ 8 of the first session): 3 alliances with the same language, activity overlap ≥ 50%, open seats, auto-accept on, ≥ 60% of members active in 72 h; join = 1 tap. Unaffiliated players at S2+ see one digest line per day: "An alliance would have saved you 34 m today", computed from their real helpable timers |
| **Welcome chest** | once per account, ever: 3 × 1 h Universal + 8 h own output + the alliance tabard (cosmetic). Opens after 24 h membership AND 5 helps given — it teaches helping. The genre gives premium currency; the "join purse" (gems worth 1 h Universal, monetization.md and onboarding.md) is an owner decision (§16) |

**Checks**: [ ] telemetry per cohort — fails when: < 70% of players at S2+ are in an alliance by day 3 · [ ] hop_exploit_test — fails when: the welcome chest pays twice to one account.

## 11. Alliance hopping

| Rule | Value (PROPOSAL) | Stops |
|---|---|---|
| Cooldown after leaving | 1st leave in 30 days: 4 h; 2nd: 24 h; 3rd and later: 72 h | serial hopping for gifts and rally rewards |
| Released | by an officer: first release in 30 days has no cooldown, later ones count as leaves; for inactivity: never a cooldown | punishing a player for others' choices; "kick me to reset" tricks |
| Locks | no leaving or joining during a war window, with marches in a rally or reinforcing, or with an attack incoming | escaping a fight; spying |
| Rank, tenure, weekly contribution | reset; rank → Recruit | carrying standing |
| Merit | kept; the store's weekly caps, the 30 paid helps per day and donation charges follow the player | resetting caps by hopping |
| Gifts, welcome chest | pending gifts auto-claimed on leave; the new alliance's only from after joining; Spoils and Great chests need 24 h; welcome chest once per account | gift sniping; chest farming |
| Season and event rewards | the alliance part of a season (35 days) needs ≥ 7 days membership at award time; of an event shorter than 14 days, half its length; otherwise the personal part only | joining the winner at the end |
| War roster | joined < 24 h before a war window: may defend own castle, may not score alliance objectives in that window | last-minute stacking |
| Visibility | profile shows "alliances in the last 30 days: n"; auto-accept can filter on it | informs the Gatekeeper |

**Checks**: [ ] hop_exploit_test: 9 rules, each tried — fails when: any row above can be bypassed.

## 12. Diplomacy — public pacts

| Pact | Effect (enforced by the server, not by trust) | Term | Sign | End early |
|---|---|---|---|---|
| **Treaty** | members of the two alliances cannot attack, scout or rally against each other's castles, standards, Chapterhouse or gatherers | 1–7 days, renewable up to 28 days in a row (the 4 contest weeks), then 7 days with no pact between the same two | two keys per side (Liege + one officer) | 12 h public notice |
| **Accord** | Treaty + members may reinforce each other's castles; shared map pins; partner marches in the ally colour with a distinct marker shape (world.md) | until season end | same | 24 h public notice |

1. **≤ 3 pacts per alliance, ≤ 1 of them an Accord** — no realm-wide web of non-aggression.
2. **Public**: pacts show on both alliance profiles, as a realm feed line (chat-forge realm channel), and as a marker at realm zoom (world.md). Profiles list the last 90 days of pacts and early ends. Because the server enforces the effect, officers never judge "who broke the peace" from reports.
3. **Suspended** at the realm's top landmark contest (world.md) and in the last 72 h of contest week 4: the top is always contested. All pacts end at season end (Truce day 1, liveops.md §3.6).
4. Ending a pact before half its term marks the alliance "Pactbreaker" for 7 days — a word on its profile, no stat effect.

**Checks**: [ ] pact_test: 5 action types blocked — fails when: an attack between Treaty partners resolves · [ ] pact_test notice, renewal and suspension cases — fails when: a pact ends without its notice, a Treaty runs > 28 days in a row, or a pact holds at the top landmark · [ ] alliance_sim realm line; liveops.md reviews — fails when: a realm freezes (≥ 60% of the top 10 alliances in pacts with each other for 14 days).

## 13. Chat and mail hooks (chat-forge, mail-forge)

| Event | Alliance chat (chat-forge Herald feed) | Mail (mail-forge) | Push (opt-in) |
|---|---|---|---|
| Member joins, leaves, is promoted, released, warned | system line (not for warnings) | to the member: promotion or office; release reason and rejoin rule; auto-release warning at N − 3 days | — |
| Help | none (digest only) | — | never |
| Gifts | Spoils: 1 line each, naming the deed; Hunt, Feast and Newcomer merge into ≤ 1 line per 2 h ("6 feasts, 14 hunts since 14:00") | — | never |
| Rally launched | rally card with Join (2 taps; battle-forge emits it) | — | opted-in members, only when the wait is ≥ 10 min |
| Rally scheduled | pinned card + calendar entry | alliance mail if ≥ 6 h ahead | 10 min before, pledged members only |
| Charter level or Great chest | 1 line; ≥ 3 per hour merge into one | — | — |
| Announcement | pinned line | optional | optional |
| Liege absent day 5 / 7 / 10 | pinned countdown from day 7 | officers (5), all (7, 10) | all at day 10 |
| Pact proposed / signed / notice / ended | line + realm feed line | officers (proposed); all members (signed, notice) | officers at notice |
| Standard fading (Treasury 0 or over cap) | line | Treasurer and Liege | — |

Budgets: this file emits ≤ 30 system lines per alliance per day into the Herald feed (chat-forge `channels.md` §5; its 30-per-hour cap is the hard ceiling; extra lines merge into one "Alliance news" line); ≤ 3 alliance-wide mails per day, each stored once per alliance, never copied per member (mail-forge `tools/mail_cost.py` prices that trap); ≤ 1 alliance push per member per day besides pledged rallies. Share cards (coordinates, reports, invites) are chat-forge's; mail templates and claim rules are mail-forge's.

**Checks**: [ ] chat-forge Herald merge test fed 100 alliance events in one hour — fails when: this file's lines exceed 30 per day or any line pushes · [ ] mail_cost trap run — fails when: alliance mail is stored per member.

## 14. Genre weak spots → our fix

| Weak spot ([benchmark.md](benchmark.md) §7, §13) | Our fix | Number |
|---|---|---|
| Leader burnout: diplomacy, schedules and discipline on one person | four offices, auto-rules, scheduled announcements, succession on read | Liege ≤ 15 min per week; succession day 10 |
| Rallies bound to one time zone | muster hours from the activity strip; scheduled rallies; standing pledges | fill ≥ 80% at every muster hour |
| Alliance hopping | cooldown ladder; tenure-gated rewards; caps follow the player | 4 h / 24 h / 72 h |
| Gifts from purchases make spending a social duty | anonymous cosmetic tokens only, 0 gift XP | ≤ 3 per alliance per day |
| Truces between rivals freeze the map | public, capped, server-enforced pacts, suspended at the top | ≤ 3 pacts; Treaty ≤ 7 d |
| One dominant alliance holds a late realm | standard cap by activity; upkeep; realm charter discount; seats ≤ 100 | cap = 3 × 7-day actives |
| Farm accounts feed a main through the alliance | no Treasury or helper pay from new or low accounts; bound gifts | < 72 h or S ≤ 2 → 0 Treasury |
| Stronghold rewards by damage share alone | half shared equally | 50 / 50 |
| Officers stock the alliance store from collective funds | endless stock, per-player weekly caps | 0 stocking taps |
| Late systems never taught | the first scheduled rally is a guided first-time moment ([onboarding.md](onboarding.md)) | week 1 |

## 15. Harness, save, server cost, metrics

| Proof | Measures | Verdict line (PROPOSED — qa-forge fixes the wording) |
|---|---|---|
| alliance_sim (new, headless; qa-forge; path to confirm) | 90 days; top / median / small; 3 time-zone clusters: charter days, Merit, gift minutes, first help, rally fill per muster hour, Liege minutes, standards vs activity, realm pacts | `ALLIANCE SIM OK - charters 33/76/100 d, merit p50 356/d, gifts <= 240 m/d, first help p50 <= 15 m, fill >= 80% x3, liege <= 15 m/wk` |
| alliance_perm_test (unit; gameplay-forge + cloud-forge) | the §2 matrix, allowed and refused, limits and two keys | `PERMS OK - 23 actions x 5 ranks x 4 offices, 0 faults` |
| succession_probe (clock skip) · hop_exploit_test · pact_test | heir, officer, Companion, fading, regent, return · every §11 row · blocks, notices, suspensions | `SUCCESSION OK - 6 cases, 0 faults` · `HOP OK - 9 rules, 0 exploits` · `PACT OK - 5 blocks, 2 notices, 1 renewal cap, 2 suspensions` |
| ux_flow_probe · ux_touch_probe · a11y_audit | Help all 1 tap, Claim all 1, Donate ×5 1, Join from card 2; badges by shape + word | existing verdict lines |
| `core/sd_cost_probe.gd` | alliance writes, reads and bytes per player per day | alliance share ≤ €20 of the €200 per month |

**Save migration** (gameplay-forge): if an alliance system already ships (check `data/*.gd`), old ranks map by order to ranks 1–5, offices start empty, old collective funds convert 1:1 into Treasury, old tech levels map to the nearest charter, members already in an alliance get the welcome chest flagged as claimed. No alliance → unchanged.

**Server cost** (estimate; measure before tuning). ≈ 708 alliances (50,000 × 85% in alliances ÷ 60). Per member per day: Donate ×N calls 3 × 2 writes (member row + one of 10 counter shards per charter), claim-all 3, store purchase 1, works march 1, rank/Roll ≈ 0.1 → ≈ 11.1 writes × 42,500 ≈ 0.47 M; plus gift appends (708 × 20) and Roll appends (708 × 30) → **≈ 0.51 M writes per day, ≈ 15 M per month**, on top of core-loop's help log (0.4 M per day). Reads: the alliance head document (≈ 1 KB) cached 60 s on the client, ≈ 6 opens × 42,500 ≈ 0.26 M per day (7.7 M per month); the member list (≈ 5 KB) only when Members opens. **0 server ticks**: upkeep, fading, landmark Treasury, succession, auto-release, announcements and charters are evaluated on read. Price: on a per-operation document store at chat-forge's range (`backend-cost.md` §7.7: writes $0.09–0.27, reads $0.03–0.06 per 100k) this is $16–46 ≈ **€14–€43 per month** — inside the €20 alliance share only at the low price; on a flat-priced server the writes add ≈ €0. Lever if needed: one write per donation call (the shard row carries member id and Merit) → 11.4 M writes per month. cloud-forge picks the store; sd_cost_probe decides.

**After ship**: ≥ 70% of S2+ players in an alliance by day 3; D30 of members ≥ 2× that of unaffiliated players (validate on our cohorts); median first help ≤ 15 min; ≥ 85% of alliances with ≥ 20 members have all 4 offices filled; < 5% of alliances disband per month; < 10% of members leave in any 30 days; median Merit ≤ 7 days of income.

Spec checklist: [ ] every §2 action mapped to a server check and a reason code · [ ] help dials identical to core-loop §6 (`c` 1%, `f` 120 / 180 s, `H` 10–30) · [ ] charter table recomputed for the shipped Treasury rates · [ ] alliance_sim verdict pasted · [ ] offer grep: 0 alliance goods on paid surfaces · [ ] sd_cost_probe alliance line · [ ] §16 sent to the owner.

## 16. Owner decisions required

1. **Purchase gifts**: anonymous cosmetic tokens, ≤ 3 per alliance per day, 0 gift XP (recommended) — or none at all. Never resources, hourglasses or the buyer's name.
2. **Welcome chest**: hourglasses + tabard (recommended), with or without the join purse of gems worth 1 h Universal (monetization.md, onboarding.md).
3. **Seat cap 100** (genre about 150 [unverified]).
4. **Merit store goods**: Peace ward (Merit only, never sold for money), Plain Seals (lords.md counts 5 per week), field journals (+8% lord XP; lords.md should count them) and gold leaf. Favour stays out (monetization.md §6).
5. **Offline war pledge** for castle rallies inside war windows (recommended: not at launch). **Succession at day 10; auto-release default 14 days.**
6. **Charter combat stats** (+1.5% attack, defence, health) against shipped sacred constants and combat.md's stat budget.
7. **Names** (story-forge canon): Liege, Officer, Marshal, Treasurer, Crier, Gatekeeper, Companion, Yeoman, Recruit, Treasury (marks), Merit, Quartermaster, charters and their branches, Chapterhouse, standards, Hunt / Spoils / Feast / Great chest, muster hours, pledge, Treaty, Accord, the Roll, Pactbreaker. Chosen to avoid clashes: rank "Knight" = cavalry t6 (units.md); "Herald" = chat-forge's system feed and liveops' Herald's Board; "Warden" = chat-forge's realm warden; "Hall" = chat-forge's alliance channel; "Realm" branch = progression's Realm charter; "Truce" = liveops' peace week; "banners" = core-loop's march slots. Files still saying "the Hall" for the alliance seat (world.md §3, §5, §8, §9; onboarding.md §7) should read "the Chapterhouse", "Hall summons" → "Chapterhouse summons".
8. Any dial here that collides with a shipped value (the shipped value wins until the owner decides).
