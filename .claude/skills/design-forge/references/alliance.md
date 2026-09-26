# Alliance — belonging you can measure

The alliance is the system that makes other players matter (game-director pillar 7, "Belonging"):
ranks and offices, help, two currencies, charters (research), gifts, territory, rallies across time
zones, leadership tools, hopping rules and public pacts. Implementation: **gameplay-forge** (rules,
data, save), **ui-forge** (alliance screens, calendar, badges), **cloud-forge** (membership, logs,
server-side permission checks), **chat-forge** and **mail-forge** (§13), **world-forge** (Hall,
banners, strongholds on the map), **battle-forge** (rally flow), **story-forge** (names),
**qa-forge** (harness). Genre patterns: [benchmark.md](benchmark.md), alliance section.

**Every number here is a PROPOSAL** (verify against `data/alliance.gd`, path to confirm) unless it
quotes a canonical fact or [core-loop.md](core-loop.md). A shipped sacred constant keeps its value
and this file's number becomes a proposal to the owner. All names are proposals for story-forge
canon. Symbols: `E` = embassy tier (1–6) of the member who asks for help (the embassy archetype is
the alliance building — verify `data/buildings.gd`); `S` = spine tier ([progression.md](progression.md));
"active" = opened the game inside the named window (48 h, 7 d); the day resets at 00:00 UTC.

## 0. The four questions

- **Want**: time back (help); shared strength (charters, territory); standing (rank, office, the alliance's name on the realm map); safety in numbers (rallies, reinforcement).
- **Obstacle**: other members' presence across time zones; Treasury, earned only by members' effort; trust (ranks, two-key actions); rival alliances.
- **Wait**: first help ≤ 15 min after the first request (waking hours, median alliance); first charter level on day 1; full charter tree 33 / 76 / 100 days (top / median / small, §5); 100 seats ≈ day 60–90 for a median alliance (§10).
- **Witness**: each help shows its minutes; each gift names the deed and the member; pacts appear in the realm feed; territory tints the realm map; rank badge and office on the profile card.

## 1. The alliance in the five timescales ([core-loop.md](core-loop.md) §1)

| Scale | Alliance action | Taps | Pay-off |
|---|---|---|---|
| Glance | Help all (queue tracker) | 1 | digest "Allies saved you 42 m" |
| Check-in | Donate ×5 (3), claim all gifts (1), join a rally from its chat card (2) | 6 | Merit; gifts; the charter bar moves |
| Day | daily order "Give to the alliance" = 1 donation or 1 works march (core-loop §7) | 0 extra | 10 order points |
| Week | 2–3 scheduled rallies at muster hours; a charter row; a Great chest about every 6 days | — | Spoils, gift level, charters |
| Season | territory, pacts end, alliance standing ([liveops.md](liveops.md)) | — | titles, map presence |

Rules: (1) the alliance adds ≤ 6 taps to a check-in (core-loop §8.2 budget stays ≤ 30); (2) no alliance
reward needs the player online at one single clock hour (§8); (3) **nothing in the alliance is sold**
(§4 rule 5).

## 2. Ranks, offices and permissions

Five ranks. Rank 4 holds four named offices, so the leader hands off whole jobs. The genre gives all
officers the same broad powers — everyone may do everything, so nobody owns a job and the leader
does it all.

| Rank | Name | Seats | Reached by |
|---|---|---|---|
| 5 | **Liege** | 1 | founding, transfer or succession (§9) |
| 4 | **Officer** — Marshal (war), Steward (Treasury, charters, banners), Herald (announcements, recruiting, mail), Warden (membership) | 4, one per office; one person holds ≤ 1 office | appointed by the Liege |
| 3 | **Knight** | no cap | promoted by the Warden or Liege |
| 2 | **Yeoman** | no cap | automatic at 72 h membership + 30 helps given, or promoted |
| 1 | **Recruit** | no cap | joining |

| # | Action | Liege | Officer | Knight | Yeoman | Recruit |
|---|---|---|---|---|---|---|
| 1 | Help, donate, claim gifts, join or pledge to rallies, chat | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | Launch a rally on a stronghold or AI lord | ✓ | ✓ | ✓ | ✓ | — |
| 3 | Launch a rally on a castle | ✓ | ✓ | ✓ | — | — |
| 4 | Pin map targets (≤ 10 pins per alliance) | ✓ | ✓ | ✓ | — | — |
| 5 | Schedule rallies, set muster hours | ✓ | Marshal | — | — | — |
| 6 | Set the recommended charter, spend Treasury on charters | ✓ | Steward | — | — | — |
| 7 | Place or remove banners | ✓ | Steward | — | — | — |
| 8 | Place or move the Hall, raise its tier | ✓ | — | — | — | — |
| 9 | Accept applicants, set auto-accept filters | ✓ | Warden | if the Warden allows | — | — |
| 10 | Promote or demote up to Knight | ✓ | Warden | — | — | — |
| 11 | Appoint or remove officers | ✓ | — | — | — | — |
| 12 | Release (kick) a member | ranks 1–4 | Warden: ranks 1–2 | — | — | — |
| 13 | Post or schedule announcements, alliance mail, edit profile and recruiting text | ✓ | Herald | — | — | — |
| 14 | Propose a pact | ✓ | Marshal | — | — | — |
| 15 | Sign or end a pact (two keys: Liege + any officer) | key 1 | key 2 | — | — | — |
| 16 | Set auto-rules (§9) | ✓ | Warden | — | — | — |
| 17 | Name heir or regent, transfer leadership, disband | ✓ | — | — | — | — |
| 18 | Read the Roll (the alliance ledger) | ✓ | ✓ | ✓ | ✓ | ✓ |
| 19 | See exact last-active time | ✓ | ✓ | bucket | bucket | bucket |

1. **The server enforces the matrix** (cloud-forge); the client only hides buttons.
2. **Safety limits**: ≤ 5 releases per officer and ≤ 10 per alliance per 24 h (auto-release not counted) — a stolen account cannot empty the alliance.
3. **The Roll**: every officer action and every Treasury spend is written to it, visible to all members, kept 30 days.
4. **Privacy**: members see last-active buckets ("today", "this week", "over 7 days"); officers see hours.
5. Rank badges (RNK) and office seals are Blender-made art (ui-forge + blender-forge), shape AND word, never colour alone; ≥ 48 dp when tappable.

**Checks**: [ ] alliance_perm_test: 19 actions × 5 ranks × 4 offices, allowed and refused — fails when: a refused action succeeds through a crafted request · [ ] alliance_perm_test rate-limit cases — fails when: one account releases > 5 members in 24 h · [ ] a11y_audit on the member list — fails when: a rank is readable only by colour.

## 3. Help — the dials quoted from core-loop §6

One source of truth: [core-loop.md](core-loop.md) §6 owns the formula and its worked math. Each help
removes `h = max(c·R, f)`, `c = 1%`, `f = 120 s`, raised to **180 s by the charter Open Door**
(§5, Fellowship row 1); `H = 10 + 4·(E − 1)` = 10, 14, 18, 22, 26, 30 helps per request; helpable:
build, research, heal — never training. This file adds the alliance side:

| Dial | PROPOSAL | Why |
|---|---|---|
| Helper reward | **5 Merit per help**, first 30 helps per day (150 Merit) | ≈ 1.25 min of hourglass per help at store prices (§4); 30 helps ≈ 5 Help-all taps |
| Unpaid helps | after 30 per day; from accounts < 72 h old or at S1; between accounts cloud-forge links by device | the ally still gets the time; farm accounts earn nothing |
| Help all | helps every open request (≤ 50 per tap) = ONE help-log append | core-loop §6 cost rule |
| Requests | auto-asked (core-loop A4); live until the timer ends; **never a push** | help is ambient, never a summons |
| Join hook | a new member's requests sit at the top of every ally's list for 24 h ("New: Rowan's first request") | first help ≤ 15 min |
| Saturation | ≥ H + 1 = 31 members active in the same 4-h window give every request its full H | why seats can stop at 100 (§10) |

**Checks**: [ ] alliance_sim first-help line — fails when: median first help > 15 min (07:00–23:00 asker's local time) in a 45-active alliance · [ ] server cap test (shared with core-loop) + hop_exploit_test — fails when: a helper is paid past 30 per day, or across a leave-and-rejoin.

## 4. Two currencies — Treasury and Merit (the free-rider fix)

Pattern ([benchmark.md](benchmark.md)): collective goods paid by many small acts, each actor paid
privately, so riding free earns nothing and contributing always pays. **Our move**: every act counts
the same for a small castle and a large one — a donation costs 15 min of the donor's OWN production,
never a flat pile of resources and never gems, so a large account cannot buy standing.

| | **Treasury** (collective, counted in marks) | **Merit** (personal) |
|---|---|---|
| Earned by | donations (10 each); Spoils (300 × stronghold level per kill); held landmarks (rate: [world.md](world.md)) | helps 5; donations 10 (15 on the recommended charter); rallies joined 20 (first 5 per day); works marches 1 per march-minute (≤ 60 per day); war windows 50 (≥ 1 engagement, ≤ 2 per day) |
| Spent on | charters (§5), banners, upkeep, Hall tiers (§7) | the Quartermaster (below) |
| Spent by | Liege and Steward; every spend in the Roll | the member |
| Leaves the alliance | never — no withdrawal, no transfer to a member | travels with the member (§11) |
| Cap | none; banner upkeep drains it | 10,000 (≈ 26 days of median income); at cap earning pauses and the store says so |
| Sold for money | never | never |

| Merit per day | Median free player (P50) | Maximum |
|---|---|---|
| Helps | 150 | 150 |
| Donations | 125 (10 donations, half on the recommended charter) | 360 (24, all recommended) |
| Rallies | 40 | 100 |
| Works marches | 20 | 60 |
| War windows | 50 | 100 |
| **Total** | **385 (2,695 per week)** | **770 (5,390 per week)** |

**The Quartermaster** (alliance store). No stocking: the genre has officers buy stock for the store
with collective funds, a daily chore; our stock is endless and every cap is **per player per week**,
carried across alliances.

| Item | Merit | Weekly cap | Note |
|---|---|---|---|
| 15 m Works hourglass | 60 | 14 | 4.0 Merit per minute; core-loop §5 names this store as its source |
| 1 h Universal hourglass | 220 | 7 | 3.7 per minute (degressive, as core-loop §5) |
| Resolve 50 | 150 | 7 | lifts the pool toward 300 (core-loop §3) |
| Lord XP tome | 120 | 10 | size: commander-forge |
| Gathering writ, 8 h | 200 | 3 | bonus: [economy.md](economy.md) |
| Peace ward, 8 h | 1,500 | 1 | never while an attack is incoming ([combat.md](combat.md), [world.md](world.md)) |
| Hall summons (relocate into own territory) | 1,000 | 1 | world.md relocation rules |
| 100 patron points | 800 | 2 | the play path into [monetization.md](monetization.md)'s patron ladder |
| Tabard dyes, pennon patterns | 1,500–3,000 | once each | stat-free cosmetics |

Weekly shelf capacity 9,330 Merit > the maximum income of 5,390, so nobody hoards Merit waiting for stock.

1. **Every benefit reaches every member**: charters, gifts and help received are not rationed. The free rider loses Merit (0 earned) and seat safety (§9 "idle contributor" rule).
2. **Contribution score** (weekly) = donations × 10 + helps × 2 + rally joins × 20 + works minutes. Officers see a sorted list; members see their own score and others' badges only ("Steady" ≥ 500, "Stalwart" ≥ 1,500 per week) — no public ranking, so giving never becomes a race.
3. **Donations**: 20 charges, regen 1 per 60 min (full in 20 h, so the 15-hour promise holds); "Donate ×5" = 1 tap; resource by charter row (§5); the donor's cost is ≤ 24 × 15 min = 6 h of one resource per day (economy.md counts it as a sink).
4. Accounts < 72 h old or at S1–S2 earn Merit from donations but add **0 Treasury** (farm accounts cannot fund a main's alliance).
5. **Never sold**: rank, seat, Treasury, charter, help count, gift level, pact, Merit. Gems cannot be donated.

**Checks**: [ ] alliance_sim Merit line — fails when: median member's Merit balance > 7 days of income at day 30 (hoarding) · [ ] donation unit test: S3 and S6 donors add 10 each — fails when: a donation's Treasury depends on city size or payment · [ ] shop-forge offer-data grep returns 0 — fails when: any alliance good appears on a paid surface.

## 5. Charters — alliance research funded by donations

Five branches × six rows; a row opens when the row above it in the same branch is complete. Cost per
level `C_r = 3,000 · 1.55^(r−1)` Treasury × size factor `s = clamp(members / 40, 0.5, 1)` × realm
discount `(1 − d)`. Progress is stored as a fraction (each donation adds `10 / price_now`), so a change
in member count never loses progress. A charter takes effect the moment it fills: no timer, no tick.

**Realm discount** (our move — the genre lets the first alliance keep its lead for good): `d = 30%`
once ≥ 3 alliances in the realm hold that level; `d = 50%` once ≥ half of the realm's alliances with
≥ 20 members hold it. The card says "Known in the realm: −30%". The size factor stops a 20-member
alliance paying the same total as a 100-member one; above 40 members growth costs nothing extra.

| Row | Cost/level | Fellowship | Stores | Works | Arms | Realm |
|---|---|---|---|---|---|---|
| 1 | 3,000 | Open Door: help floor 120 → 180 s (1 lv) | Foragers: gathering +3%/lv (3) | Masons: build speed +1%/lv (3) | Drill: march speed +2%/lv (3) | Surveyors: banner cost −5%/lv (3) |
| 2 | 4,650 | Great Table I: +5 seats (1) | Cellars: protected storage +5%/lv (3) | Scribes: research speed +1%/lv (3) | Rally Horn: rally capacity +5%/lv (3) | Roadwardens: march speed in own territory +5%/lv (3) |
| 3 | 7,200 | Feast Hall: gift XP +10%/lv (3) | Wagonways: gathering load +4%/lv (3) | Masons II: build +1%/lv (3) | Shield Wall: troop defence +0.5%/lv (3) | Stewardship: banner upkeep −5%/lv (3) |
| 4 | 11,150 | Great Table II: +5 seats (1) | Foragers II: gathering +3%/lv (2) | Scribes II: research +1%/lv (2) | Keen Edge: troop attack +0.75%/lv (2) | Beacons: marches into own territory seen 30 s earlier/lv (2) |
| 5 | 17,300 | Great Table III: +5 seats (1) | Granaries: healing cost −5%/lv (2) | Master Builders: build +1%/lv (2) | Surgeons: infirmary beds +5%/lv (2) | Summons: relocation cooldown −12 h/lv (2) |
| 6 | 26,850 | Great Table IV: +5 seats (1) | Market Rights: member trade tax −5% (1) | Great Works: research +2% (1) | Iron Discipline: troop health +1.5% (1) | High Hall: Hall and banner durability +10% (1) |

Totals: 64 levels, **597,750 Treasury** at full price. Branch maxima: gathering +15%, build +8%,
research +7%, **troop attack / defence / health +1.5% each** — collective combat stats stay small so
charters never bury a counter (+20–50%, [numbers.md](numbers.md) §4; combat.md owns the stat budget).

Days to finish, all net Treasury to charters (Treasury per day: top 90 active × 16 donations × 10 +
5 kills × level 5 × 300 − upkeep 3,600 = 18,300; median 45 × 10 × 10 + 2 × 3 × 300 − 800 = 5,500;
small 12 × 10 × 10 + 0.5 × 2 × 300 = 1,500):

| After row | Treasury (full price) | Top: 100 members, d 0% | Median: 60 members, d 30% | Small: 20 members, s 0.5, d 50% |
|---|---|---|---|---|
| 1 | 39,000 | 2.1 d | 5.0 d | 6.5 d |
| 2 | 99,450 | 5.4 d | 12.7 d | 16.6 d |
| 3 | 207,450 | 11.3 d | 26.4 d | 34.6 d |
| 4 | 307,800 | 16.8 d | 39.2 d | 51.3 d |
| 5 | 463,500 | 25.3 d | 59.0 d | 77.2 d |
| 6 | 597,750 | **32.7 d** | **76.1 d** | **99.6 d** |

If 30% of Treasury goes to banners and the Hall, divide by 0.7 (median ≈ 109 d). The spread top :
small is 3 : 1, not the 12 : 1 of a flat price with no discount.

1. The Steward (or Liege) sets one **recommended charter**; donations to it pay 15 Merit instead of 10. Any open charter accepts donations.
2. Donated resource by row: rows 1–2 food or wood, 3–4 stone, 5–6 iron (the resource ladder of numbers.md §2; economy.md may override).
3. Joining gives the new alliance's charters at once; leaving loses the old ones (belonging, not a reward — nothing to gain by hopping).

**Checks**: [ ] alliance_sim charter line — fails when: median full tree < 45 d (nothing left to fund) or > 120 d · [ ] alliance_sim charter line — fails when: a small alliance needs > 7 d for row 1 · [ ] data lint (gameplay-forge) — fails when: sum of charter combat stats exceeds combat.md's budget.

## 6. Gifts — deeds shared, never purchases

Pattern: one member's deed becomes a small gift to every member, so success is shared and seen.
**Our move**: gifts come from deeds in play only. A purchase creates at most an anonymous cosmetic
token — spending never becomes a social duty (owner decision, §16).

| Gift | Created when | Each member receives ("own output" = minutes of that member's own production) | Gift XP |
|---|---|---|---|
| **Hunt** | a member first clears a camp level (camp ladder, world.md) | 5 min own food + wood | 1 |
| **Spoils** | the alliance destroys a stronghold of level L (1–6) | 10·L min own output (all five) + one 15 m Universal at L ≥ 4 | 5·L |
| **Feast** | a member reaches a spine tier, unlocks a troop tier in any line, or completes a lord's four-piece set (≤ 1 per member per day) | 15 min own output + 5 Resolve | 10 |
| **Great chest** | every 400 gift XP | 1 h Universal + 1 h own output | — |
| **Patron token** | any member's purchase — buyer never named, ≤ 3 per alliance per day | 1 cosmetic fragment (10 = a pennon dye or a feast emote) | 0 |

**Gift level** 1–10, +5% contents per level (level 10 = +45%). XP to the next level
`200 · 1.3^(ℓ−1)` = 200, 260, 338, 439, 571, 743, 965, 1,255, 1,631 (6,402 in total). Median alliance
≈ 70 XP per day (10 hunts, 2 level-3 strongholds, 3 feasts) → level 10 at ≈ day 91, a Great chest
every ≈ 6 days; top alliance ≈ 205 XP per day → level 10 at ≈ day 31.

1. **Daily cap per member: 240 min of own output from gifts**; above it contents turn into gift XP. Median ≈ 155 min per day at level 1, 225 at level 10; a top alliance (≈ 440 raw) hits the cap. The top's edge over a median alliance is therefore ≤ 85 min of production per day.
2. **Not retroactive**: a member receives only gifts created after joining; Spoils and Great chests need ≥ 24 h membership.
3. Bound to the account; resources land in protected storage (core-loop §7 rule 7).
4. "Claim all" = 1 tap; each line names the deed ("Spoils — level-4 stronghold, rally led by <member>"). Unclaimed gifts expire after 72 h; on leaving, pending gifts are claimed automatically.
5. A gift is ONE append to the alliance gift log; claim-all moves one per-member cursor — never one write per member per gift (§15).
6. Purchases never raise gift level, never give resources or hourglasses to others, never name the buyer.

**Checks**: [ ] alliance_sim gift line — fails when: gift output > 240 min per member per day · [ ] shop-forge offer-data grep + gift unit test — fails when: a purchase creates a non-cosmetic gift, or names the buyer · [ ] hop_exploit_test — fails when: a new member receives gifts created before joining.

## 7. Territory — the Hall and banners

[world.md](world.md) owns map geometry, landmarks, strongholds, relocation and the reserved relationship
palette. This section owns the alliance side: who, cost, upkeep, cap.

| Item | Rule (PROPOSAL) |
|---|---|
| **Hall** | one per alliance, placed by the Liege: 2,000 Treasury + 300 works march-minutes. Tiers 2–6 cost 10k / 20k / 35k / 55k / 80k Treasury (200k total) + 300 × tier works-minutes; each tier +8 seats (§10) |
| **Banner** | placed by the Steward or Liege, touching own territory. Cost of the b-th banner `500 · 1.15^floor((b−1)/10)`: #1 500, #51 1,006, #101 2,023, #200 7,116; 60 banners 43,769 in total, 200 banners 512,218 |
| Banner cap | `min(200, 3 × 7-day-active members)` — territory follows activity, not history |
| Upkeep | first 20 banners free, then 20 Treasury per banner per day (−5% per Stewardship level); a function of time, settled on any Treasury read — 0 server ticks. Median 60 banners = 800 per day (13% of income); top 200 = 3,600 (16%) |
| Unpaid | at Treasury 0 the banner farthest from the Hall fades every 6 h; the Hall never fades |
| Works | members build with works marches: Merit 1 per march-minute (≤ 60 per day) |
| Benefits | gathering bonus inside, march speed inside (Roadwardens), Hall summons, owned resource points — values in economy.md and world.md |
| No seats from banners | the genre adds a member seat per 10 flags; we do not — seats never reward sprawl |

**Fiction and art**: the Hall is a 3D building (blender-forge; tier language of game-art-director
`references/buildings.md`: tier 1 rough timber → tier 6 fine ashlar with gilt civic trim). Banners,
pennons and the Hall carry the alliance's two tinctures only through the tint mask (blender-forge
`references/architecture.md` §7); the self/ally/enemy/neutral colour stays a reserved channel. The
alliance sigil is ALS art (game-art-director); tinctures are chosen from a set that never collides
with the relationship colours or the five line accents.

**Checks**: [ ] alliance_sim banner-vs-activity line — fails when: an alliance with < 10 active members still holds > 30 banners after 14 days · [ ] sd_cost_probe: 0 scheduled writes — fails when: upkeep or fading needs a server job · [ ] contrast_test + a11y_audit on the realm-zoom map — fails when: a tincture pair reads as a relationship colour.

## 8. Rallies across time zones

[combat.md](combat.md) owns rally capacity and losses; battle-forge owns the rally flow and its taps;
[liveops.md](liveops.md) owns the realm's war windows (two ≤ 60-min windows 12 h apart, core-loop §8.3).
This section owns scheduling and joining.

| Tool | Rule (PROPOSAL) |
|---|---|
| Rally wait | 5 / 10 / 30 / 60 min, or **scheduled** 15 min – 24 h ahead on a 15-min grid, shown in each member's local time |
| **Muster hours** | the Marshal sets ≤ 3 per day. The calendar shows a 24-hour activity strip (7-day-active members per hour, last 14 days, in the viewer's local time) and the coverage: share of 7-day-active members usually active within ±1 h of a muster hour. Target ≥ 60% |
| **Pledge** | a scheduled rally carries a Pledge button (2 taps); the pledged march leaves at launch if the member is online, or offline if they allowed it |
| **Standing pledge** (auto-join) | PvE targets only (strongholds, AI lords): ≤ 20% of the field army by default (max 50%), ≤ 3 per day (max 5), a lord preset, never the last free banner. It fills only places still open at 50% of the wait — people first |
| Castle rallies | no offline auto-join: attackers' losses are heavy ([combat.md](combat.md)). A "war pledge" inside realm war windows, ≤ 20% of army, is an owner decision (§16) |
| Rewards | stronghold rewards: **50% shared equally** among participants, 50% by damage share (the genre pays by damage share alone, so the biggest accounts take most). Auto-joiners earn the same; Merit 20 for the first 5 rallies per day |
| Guards | auto-join needs S3+ and an account ≥ 72 h old (farm guard); no auto-join while an attack on the member's castle is incoming; departures use the march arrival trigger of world.md (no new server job) |

**Fairness target**: in an alliance of three clusters (UTC−5, UTC+1, UTC+8; 15 members each), every
muster hour fills ≥ 80% of rally capacity with standing pledges on, and a member who is never online
at a muster hour still earns ≥ 60% of the median member's Spoils.

**Checks**: [ ] alliance_sim rally line, 3 clusters — fails when: fill < 80% at any muster hour, or the never-online member < 60% of median Spoils · [ ] server test (combat side, cloud-forge) — fails when: an offline member's troops join a castle rally without a war pledge · [ ] rally unit test — fails when: auto-joiners take places before 50% of the wait.

## 9. Leader burnout tools

Target: with auto-rules on, the Liege has **0 required daily actions**, and a week of leadership takes
**≤ 15 min** (set the recommended charter, schedule ≤ 3 rallies, glance at the Roll). Measured, not hoped.

| Tool | Rule (PROPOSAL) |
|---|---|
| Offices | four officers own four jobs (§2); an office empty for 48 h shows "Seat open" to Knights, who may apply |
| Scheduled announcements | ≤ 5 queued; once, daily or weekly; ≤ 300 characters; a pinned chat line (chat-forge), optional alliance mail (mail-forge), optional push (members opt in) |
| Auto-accept | filters: S ≥ x; language; activity overlap ≥ y% with the alliance strip; alliances in the last 30 days ≤ z. Others wait for the Warden; applications expire after 72 h |
| Auto-promote | Recruit → Yeoman at 72 h membership + 30 helps given |
| Auto-release, inactive | off / 7 / 10 / 14 days without a session; default 14 with "only when ≥ 90% full" ON; warning mail at N − 3 days; members "On leave" exempt; a released member may rejoin within 30 days with no cooldown, as a Yeoman |
| Auto-release, idle contributor | optional: < 100 contribution in 14 days while active |
| On leave | a member marks ≤ 14 days, once per 30 days; inactivity clocks pause. A Liege on leave names a regent with all powers except transfer and disband |
| Officer absence | 7 days without a session → the office is vacated (the officer becomes a Knight); mail to the Liege |
| **Succession** | Liege without a session: day 5 mail to officers; day 7 mail to all + pinned countdown; **day 10** leadership passes to (1) the named heir if active in the last 48 h, else (2) the officer with the most 30-day contribution among those active in 48 h, else (3) such a Knight, else (4) such a Yeoman; nobody active in 48 h → "fading" (§10). The old Liege becomes a Knight. Evaluated on the next alliance read — no server job |
| Transfer | voluntary: 24 h delay, cancellable, the receiver must accept (a stolen account cannot hand the alliance away at once) |
| Disband | 72 h delay; any officer may "take the banner" in that time — leadership passes to them and the disband is cancelled. Treasury is lost on disband |

Rejected: **votes of no confidence** (politics become the game and burnout grows); **one leader holding
every power** (the genre's burnout source).

**Checks**: [ ] alliance_sim leader-minutes line + ux_flow_probe on the 3 weekly tasks — fails when: Liege leadership > 15 min per week in the sim · [ ] succession_probe (clock skip, 6 cases) — fails when: leadership does not pass at day 10, or passes to someone inactive · [ ] succession_probe — fails when: an inactive member is released while "On leave".

## 10. Size, growth, founding, merging and joining

**Seats = 40 + 5 × (Great Table levels, 0–4) + 8 × (Hall tier − 1, 0–5)** → 40 … 100. Hard cap
**100** (the genre sits around 150 [unverified]). Why 100: help saturates at H + 1 = 31 members active
in one 4-h window (§3), so members beyond about 50 active add Treasury, not help; chat stays readable
(100 members × ~6 lines = 600 lines per day, chat-forge); a realm of N players holds at least N/100
full alliances, so more alliances contest the top (anti-stagnation, [world.md](world.md)). A median
alliance reaches 60 seats with Great Table IV (≈ day 76, §5) and 100 with Hall tier 6 (200k Treasury).

| Rule | PROPOSAL |
|---|---|
| Founding | S ≥ 3; costs 8 h of own output (all five), never gems; name, 3–4 letter tag, sigil (ALS), two tinctures; one founding per account per 30 days |
| Fading | < 10 seven-day-active members for 14 days → listed on the merge board |
| Merging | both Lieges agree (two keys per side); members move in one step with no cooldown; each charter keeps the higher level; Treasury adds up; officers of the absorbed alliance become Knights; its Hall is removed, touching banners transfer, the rest fade |
| Suggestion | at S2 (onboarding.md picks the moment): 3 alliances with the same language, activity overlap ≥ 50%, open seats, auto-accept on, ≥ 60% of members active in 72 h; join = 1 tap |
| Honest nudge | an unaffiliated player at S2+ sees one digest line per day: "An alliance would have saved you 34 m today" — computed from their real helpable timers |
| **Welcome chest** | once per account, ever: 3 × 1 h Universal + 8 h own output + the alliance tabard (cosmetic). Opens after 24 h membership AND 5 helps given — it teaches helping. The genre gives premium currency; gems or not is an owner decision (§16) |

**Checks**: [ ] telemetry per cohort — fails when: < 70% of players at S2+ are in an alliance by day 3 · [ ] hop_exploit_test — fails when: the welcome chest pays twice to one account.

## 11. Alliance hopping

| Rule | Value (PROPOSAL) | Stops |
|---|---|---|
| Cooldown after leaving | 1st leave in 30 days: 4 h; 2nd: 24 h; 3rd and later: 72 h | serial hopping for gifts and rally rewards |
| Released by an officer | first release in 30 days: no cooldown; later ones count as leaves | punishing a player for others' choices; "kick me to reset" tricks |
| Released for inactivity | no cooldown | — |
| Locks | no leaving or joining during a war window, with marches in a rally or reinforcing, or with an attack incoming | escaping a fight; spying |
| Rank, tenure, weekly contribution | reset; rank → Recruit | carrying standing |
| Merit | kept; the store's weekly caps, the 30 paid helps per day and donation charges follow the player | resetting caps by hopping |
| Gifts | pending ones auto-claimed on leave; the new alliance's only from after joining; Spoils and Great chests need 24 h | gift sniping |
| Welcome chest | once per account | chest farming |
| Season and war rewards | the alliance part needs ≥ 7 days membership at award time (or half the season if shorter); otherwise the personal part only | joining the winner at the end |
| War roster | joined < 24 h before a war window: may defend own castle, may not score alliance objectives in that window | last-minute stacking |
| Visibility | profile shows "alliances in the last 30 days: n"; auto-accept can filter on it | informs the Warden |

**Checks**: [ ] hop_exploit_test: 11 rules, each tried — fails when: any row above can be bypassed.

## 12. Diplomacy — public pacts

| Pact | Effect (enforced by the server, not by trust) | Term | Sign | End early |
|---|---|---|---|---|
| **Truce** | members of the two alliances cannot attack, scout or rally against each other's castles, banners, Hall or gatherers | 1–7 days, renewable | two keys per side (Liege + one officer) | 12 h public notice |
| **Accord** | Truce + members may reinforce each other's castles; shared map pins; partner marches in the ally colour with a distinct marker shape (world.md) | until season end | same | 24 h public notice |

1. **≤ 3 pacts per alliance, ≤ 1 of them an Accord** — no realm-wide web of non-aggression.
2. **Public**: pacts show on both alliance profiles, as a realm feed line (chat-forge realm channel), and as a marker at realm zoom (world.md). Profiles list the last 90 days of pacts and early ends.
3. **Suspended** at the realm's top landmark contest (world.md) and in the last 72 h of a season: the top is always contested. All pacts end at season end.
4. Ending a pact before half its term marks the alliance "Oathbreaker" for 7 days — a word on its profile, no stat effect.
5. Because the server enforces the effect, officers never have to judge "who broke the truce" from reports.

**Checks**: [ ] pact_test: 5 action types blocked — fails when: an attack between Truce partners resolves · [ ] pact_test notice and suspension cases — fails when: a pact ends without its notice, or holds at the top landmark · [ ] alliance_sim realm line; liveops.md reviews — fails when: a realm freezes (≥ 60% of the top 10 alliances in pacts with each other for 14 days).

## 13. Chat and mail hooks (chat-forge, mail-forge)

| Event | Alliance chat (chat-forge) | Mail (mail-forge) | Push (opt-in) |
|---|---|---|---|
| Member joins, leaves, is released | system line | to the released member: reason and rejoin rule | — |
| Help, gifts | none (digest and gift list only) | — | never |
| Rally launched (wait ≥ 10 min) | rally card with Join (2 taps) | — | pledged and opted-in members |
| Rally scheduled | pinned card + calendar entry | alliance mail if ≥ 6 h ahead | 10 min before, pledged members only |
| Charter level or Great chest | 1 line; ≥ 3 per hour merge into one | — | — |
| Announcement | pinned line | optional | optional |
| Promotion, office change | line | to the member | — |
| Liege absent day 5 / 7 / 10 | pinned countdown from day 7 | officers (5), all (7, 10) | all at day 10 |
| Pact proposed / signed / notice / ended | line + realm feed line | officers (proposed); all members (signed, notice) | officers at notice |
| Auto-release warning | — | to the member at N − 3 days | — |
| Banner fading (Treasury 0) | line | Steward and Liege | — |

Budgets: ≤ 20 system lines per alliance per day (extra lines merge into one "Alliance news" line);
≤ 3 alliance-wide mails per day; ≤ 1 alliance push per member per day besides pledged rallies.
Share cards (coordinates, reports, invites) are chat-forge's; mail templates and claim rules are mail-forge's.

## 14. Genre weak spots → our fix

| Weak spot ([benchmark.md](benchmark.md)) | Our fix | Number |
|---|---|---|
| Leader burnout: diplomacy, schedules and discipline on one person | four offices, auto-rules, scheduled announcements, succession on read | Liege ≤ 15 min per week; succession day 10 |
| Rallies bound to one time zone | muster hours from the activity strip; scheduled rallies; standing pledges | fill ≥ 80% at every muster hour |
| Alliance hopping | cooldown ladder; tenure-gated rewards; caps follow the player | 4 h / 24 h / 72 h |
| Gifts from purchases make spending a social duty | anonymous cosmetic tokens only, 0 gift XP | ≤ 3 per alliance per day |
| Truces freeze the map | public, capped, server-enforced pacts, suspended at the top | ≤ 3 pacts; truce ≤ 7 d |
| One dominant alliance holds a late realm | banner cap by activity; upkeep; realm charter discount; seats ≤ 100 | cap = 3 × 7-day actives |
| Farm accounts feed a main through the alliance | no Treasury or helper pay from new/low accounts; bound gifts | < 72 h or S ≤ 2 → 0 Treasury |
| Rally rewards by damage alone | half shared equally | 50 / 50 |
| Officers stock the alliance store | endless stock, per-player weekly caps | 0 stocking taps |
| Wealth decides contribution | a donation = 15 min of own output → flat 10 Treasury | equal per act |
| Late systems never taught | the first scheduled rally is a guided first-time moment ([onboarding.md](onboarding.md)) | week 1 |

## 15. Harness, save, server cost, metrics

| Proof | Measures | Verdict line (PROPOSED — qa-forge fixes the wording) |
|---|---|---|
| alliance_sim (new, headless; qa-forge; path to confirm) | 90 days; top / median / small; 3 time-zone clusters: charter days, Merit, gift minutes, first help, rally fill per muster hour, Liege minutes, banners vs activity, realm pacts | `ALLIANCE SIM OK - charters 33/76/100 d, merit p50 385/d, gifts <= 240 m/d, first help p50 <= 15 m, fill >= 80% x3, liege <= 15 m/wk` |
| alliance_perm_test (unit; gameplay-forge + cloud-forge) | the §2 matrix, allowed and refused, rate limits | `PERMS OK - 19 actions x 5 ranks x 4 offices, 0 faults` |
| succession_probe (clock skip) | heir, officer, Knight, fading, regent, return | `SUCCESSION OK - 6 cases, 0 faults` |
| hop_exploit_test | every §11 row | `HOP OK - 11 rules, 0 exploits` |
| pact_test | blocks, notice timers, suspension | `PACT OK - 5 blocks, 2 notices, 2 suspensions` |
| ux_flow_probe · ux_touch_probe · a11y_audit | Help all 1 tap, Donate ×5 3 taps, Join from card 2, Claim all 1; badges by shape + word | existing verdict lines |
| `core/sd_cost_probe.gd` | alliance writes per player per day | alliance share ≤ €20 of the €200 per month |

**Save migration** (gameplay-forge): if an alliance system already ships (check `data/*.gd`), old ranks
map by order to ranks 1–5, offices start empty, old collective funds convert 1:1 into Treasury, old tech
levels map to the nearest charter, and members already in an alliance get the welcome chest flagged as
claimed. Players with no alliance load unchanged.

**Server cost** (estimate; measure before tuning). ≈ 700 alliances (50,000 × 85% in alliances ÷ 60).
Per member per day: Donate ×N calls 3 × 2 writes (member row + one of 10 counter shards per charter),
gift claim-all 3, store purchase 1, works march 1, rank/Roll ≈ 0.1 → ≈ 11 writes × 42,500 ≈ 0.47 M; plus
gift appends (700 × 20 = 14k) and Roll appends (700 × 30 = 21k) → **≈ 0.5 M writes per day, ≈ 15 M per
month**, on top of core-loop's help log (0.4 M per day). Reads: the alliance document cached 60 s on the
client, ≈ 6 opens × 42,500 ≈ 0.26 M per day. **0 server ticks**: upkeep, fading, succession, auto-release
and charters are evaluated on read. Cost = writes × price per write + reads × price per read (+ storage);
cloud-forge fills in the prices and the alliance share must stay ≤ 10% of the budget (€20 per month).

**After ship**: ≥ 70% of S2+ players in an alliance by day 3; D30 of members ≥ 2× that of unaffiliated
players (validate on our cohorts); median first help ≤ 15 min; ≥ 85% of alliances with ≥ 20 members
have all 4 offices filled; < 5% of alliances disband per month; < 10% of members leave in any 30 days;
median Merit balance ≤ 7 days of income; rally fill ≥ 80% at every muster hour.

Spec checklist: [ ] every §2 action mapped to a server check · [ ] help dials identical to core-loop §6 ·
[ ] charter table recomputed for the shipped Treasury rates · [ ] alliance_sim verdict pasted ·
[ ] offer grep: 0 alliance goods on paid surfaces · [ ] sd_cost_probe alliance line · [ ] §16 sent to the owner.

## 16. Owner decisions required

1. **Purchase gifts**: anonymous cosmetic tokens, ≤ 3 per alliance per day, 0 gift XP (recommended) — or none at all. Never resources, hourglasses or the buyer's name.
2. **Welcome chest**: hourglasses + tabard (recommended) or premium gems (the genre's choice).
3. **Seat cap 100** (genre about 150 [unverified]).
4. **Peace ward and patron points in the Merit store** (monetization.md must agree).
5. **Offline war pledge** for castle rallies inside war windows (recommended: not at launch).
6. **Succession at day 10; auto-release default 14 days.**
7. **Charter combat stats** (+1.5% attack, defence, health) against shipped sacred constants and combat.md's stat budget.
8. **Names** (story-forge canon): Liege, Marshal, Steward, Herald, Warden, Knight, Yeoman, Recruit, Treasury (marks), Merit, Quartermaster, charters, Hall, banners, Hunt / Spoils / Feast / Great chest, muster hours, pledge, Truce, Accord, the Roll, Oathbreaker.
9. Any dial here that collides with a shipped value (the shipped value wins until the owner decides).
