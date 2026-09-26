# Defence — setup, warnings, reinforcements, walls, wards

What a lord does to be ready, what they see when an attack comes, and how allies help. The
rules (who defends, loss buckets when defending, wall durability and what happens at zero,
reinforcement capacity, ward rules) belong to design-forge `combat.md` (§6 losses, §9
garrison and reinforcements, §10 walls, §11 scouting and warnings); this file is how they are
shown and operated. Numbers quoted from combat.md are marked with their section; the rest are
**PROPOSALS**. Taps as in [flows.md](flows.md).

## 1. What defends a castle

| Layer | Source | Shown in battle as (beats.md §3) | Art owner |
|---|---|---|---|
| Garrison troops | troops at home | squads, one per line | hero3d rig + units.md kit |
| Garrison lord pair | chosen in §3, else the highest-level lords at home (combat.md §9) | `garrison_lord` chip + sworn gilt rim on the garrison | commander-forge |
| Walls & Gate | ONE durability bar W (combat.md §10); structure bonus up to +0.5 tier | `ram_hit`, `engine_shot`, `wall_state`, `breach` | castle-forge (states), blender-forge (kit) |
| Towers | the tower archetype (6 tiers) | `tower_fire` salvos | castle-forge |
| Defence tools | stocked tools (DEF-* art prefix exists; siege-forge's defensive tools: drop-stones, murder holes, hoardings) | `trap` | siege-forge |
| Stationed allies | reinforcements (§5) | `reinforce` with the allies' pennons | — |
| Infirmary beds | the hospital archetype | outcome card numbers | — |
| Ward | earned or held item | no battle: a pale-gold dome over the castle on the map | game-art-director effects.md shield/ward language |

## 2. Warnings — ETA bands and information tiers

The genre's watchtower warns of incoming attacks and improves reports with level; the pattern
we keep is **time to react, shown honestly**. Four bands by time to contact:

| Band | Trigger | Castle view | Realm view | Sound | Push (app closed) |
|---|---|---|---|---|---|
| Scouted | an enemy scout reached the castle | tracker row "Scouted by <house> (level 3) 14:02" (combat.md §11 rule 2); readiness bubble (§4) shows | — | none | none; in the next digest |
| Detected | a hostile march targets the castle, any ETA | tracker row with ETA; fortress bubble "Attack 2:40"; Defence button | hostile line 8 px, pulse ≤ 1 Hz | `bt_warn_horn` once, −6 dB | 1 push if ETA ≥ 90 s and war alerts are on |
| Near | ETA ≤ 60 s | top banner ≤ 12% of the short side: countdown + **Call allies · Recall marches · Defence** | "Show attacker" (1 tap pans) | drum pulse every 2 s, −9 dB, ≤ 60 s | none |
| Contact | ETA 0 | battle-view offer; automatic when in castle view | clash marker for `T_fight` | contact stinger | 1 push with the result after the battle |

- Several marches: the banner counts them — "3 marches — first 0:42". Pushes group into ONE per
  60 s. War alerts are a separate opt-in channel beside core-loop A8's ≤ 4 pushes per day,
  capped at 6 war pushes per day (PROPOSAL); after the 6th, one summary push at the end of the
  war window. Under 90 s of ETA no push is sent: it would arrive too late to act on.
- Quiet hours (22:00–08:00 local, core-loop A8) mute war pushes unless the player turned on
  "Wake me for attacks". Default off is safe because home never kills (combat.md §6 rule 1:
  a defender's casualties are light or severe; beds full → routed, back free after 24 h).
- Returning after attacks while away: the resume digest (core-loop §8.1, ≤ 3 lines) carries ONE
  line — "2 attacks while you were away: walls held once, raided once" — with the reports in the
  tracker. Never a stack of modal pop-ups (feel-forge's one-popup rule per the studio notes).
- The warning band never changes the camera by itself (flows.md §7).

**What the warning reveals, by the defender's watchtower tier E** (combat.md §11 rule 3; the
ETA is always exact). The "Incoming" card (tap the tracker row) shows known rows and, for each
unknown row, "?" plus the tier that reveals it (the next goal stays visible):

| Watchtower tier | The Incoming card shows (combat.md) | battle-forge adds |
|---|---|---|
| E1 | exact ETA | arrival clock in local time |
| E2 | + attacker and kind (single march or rally) | alliance tag, rally joiner count |
| E3 | + size ±20% | size vs the garrison ("about 1.4× your garrison") |
| E4 | + lines ±10% | the matchup strip + "+0.4 tier" vs the current garrison |
| E5 | + lords | lord portraits (painted CMD art) |
| E6 | + engines by class | engine icons (siege-forge) and the expected Walls & Gate loss band |

| Fails when | Caught by |
|---|---|
| An attack lands with no Detected row ever shown (hidden attack) | [ ] `warning_probe`: every hostile march creates the row at launch |
| A player returns to 3 modal pop-ups for 3 attacks | [ ] `warning_probe` offline case: 1 digest line, 0 modals |
| The Near banner appears later than 60 s or not at all | [ ] `warning_probe`: band change within ±1 s of ETA 60 s |
| A push fires per march (5 attackers = 5 pushes) | [ ] `warning_probe`: pushes grouped, ≤ 1 per 60 s |

## 3. Defence setup — the flow

Entry: tap the fortress (or the wall / gatehouse) → **Defence** tab. First time:

| # | Step | Taps | Seconds |
|---|---|---|---|
| 1 | Fortress → Defence tab | 2 | 3 |
| 2 | Garrison lord: slot → pick (list sorted with defence-role lords first; lords.md roles) → confirm | 3 | 10 |
| 3 | Secondary lord: slot → pick | 2 | 6 |
| 4 | Defence tools: set a stock target; a standing order refills it (core-loop A2 pattern) | 2 | 6 |
| 5 | Walls & Gate: **Repair** (+10% at once, free, 30-min cooldown — combat.md §10) when below 100% | 1 | 3 |
| 6 | Allies may station troops: toggle (default on) | 1 | 2 |
| 7 | War alerts: on / off, and "Wake me for attacks" | 1 | 3 |
| | **Total** | **12** | **≤ 60 incl. reading** |

After the first setup every later check is ≤ 3 taps (bubble → Defence → one change).

**The Defence panel** (one screen, no sub-tabs):

| Zone | Content |
|---|---|
| Garrison | lord pair portraits, troops at home per line (medallions + counts), a matchup strip against the last known attacker |
| Walls | the Walls & Gate bar with the state name (§6), time to full, Repair with its cooldown; in a breach truce: its time left and Stay / Relocate |
| Towers and tools | tower tier; each tool type with stock / target and its DEF icon |
| Allies stationed | list: ally name, lines, count, arrival time; Send home (2 taps); capacity bar |
| Ward | state, time left, "Raise ward" (held items only) or the reason it is unavailable |

**Stand-in lords** (combat.md §9: unset or away → the highest-level lords at home stand in —
never a castle without a command). The panel says it in one line: "Maud is marching — Edwin
will hold the walls", with Recall Maud (2 taps).

No stance picker unless combat.md defines garrison stances; if it does, ≤ 2 choices, 1 tap.

| Failure | Message | Offered |
|---|---|---|
| Tools at 0 | "No drop-stones stocked" | Stock tools (2 taps) |
| Infirmary full | "Infirmary full — wounded defenders would be routed for 24 h (never killed at home)" | Heal all (2 taps) |
| Repair on cooldown | "Repair ready in 18 m · auto-repair +12.5% per hour after 15 min without an assault" (combat.md §10) | — |
| Breached (burning) | "Breach truce 7 h 12 m — no attacks or rallies on you; scouting stays open. Walls restart at 25%." | **Stay** or **Relocate** (1 tap, once, free, to your alliance's territory or region — combat.md §10) |
| Ally capacity full | the ally sees "Castle full — 0 places" before sending | — |

## 4. The readiness bubble

A status bubble on the fortress (ui-forge status bubbles; counts inside the ux.md bubble
budget) shows **"Defence 3/4"** only when a check fails or a hostile march is Detected:

| # | Check | Pass when |
|---|---|---|
| 1 | Lord | a garrison lord is set and at home |
| 2 | Walls | Walls & Gate ≥ 90%, or a breach truce is running |
| 3 | Tools | stock ≥ 50% of the target |
| 4 | Beds | infirmary free beds ≥ 30% of troops at home (combat.md sizes the beds) |

Tapping the bubble opens the Defence panel scrolled to the first failing check (1 tap).

| Fails when | Caught by |
|---|---|
| The bubble shows while 4/4 (noise; red-dot fatigue) | [ ] `defence_flow_probe`: bubble hidden at 4/4 with no threat |
| A check fails silently | [ ] probe: each of the 4 failure fixtures shows the bubble |

## 5. Reinforcements from allies

| Side | Steps | Taps | What they see |
|---|---|---|---|
| Defender asks | Near banner → **Call allies** | 1 | a post in the alliance feed + an under-attack card in the alliance channel (chat-forge `channels.md`: ≤ 1 per member per 10 min, members opt in): "<name>'s castle — attack in 0:48 — Reinforce"; inside the 10 min the button reads "Called 4 m ago" |
| Ally answers | card → Reinforce → Send (defence preset) | 3 | "Arrives 0:38 before the attack ✓" or "Arrives 0:12 after ✗ — will defend the next attack"; the host's free places (cap by embassy tier, 1.0–3.0 × a full march — combat.md §9) |
| Defender sees help | banner line | 0 | "2 allies marching — first arrives 0:21 before contact" |
| Defender sends home | Defence panel → ally row → Send home | 2 | the march leaves at once |

- **Arrival honesty**: the battle is resolved at contact (design-forge SKILL.md rule 5), so a
  reinforcement arriving after contact cannot join that battle. The Send button states it
  before the ally commits; it never blocks the send (the troops may be wanted for a second wave).
- In battle, stationed allies fight under the host's garrison lord inside the garrison squads
  and show as pennons (≤ 6, then "+N"); their losses follow combat.md §6 row 4 (25 / 60 / 15
  light / severe / dead) and appear in THEIR outcome card with the host's name
  ([outcome.md](outcome.md) §3–4). The ally may recall them any time (combat.md §9).
- Assaults are fought in arrival order (combat.md §9): the banner lists the queue ("3 marches —
  first 0:42, then 1:10, 1:55") so the defender sees that the garrison shrinks between them.

## 6. Wall, gate and tower states

One bar, **Walls & Gate** (combat.md §10: one decision, one bar). castle-forge supplies the
meshes and decals; blender-forge builds kit pieces; battle-forge picks the state from the bar
and shows it the same way in castle view, battle view and report.

| State | Walls & Gate | Castle and battle view | Realm map (city 48–96 px) |
|---|---|---|---|
| Intact | 67–100% | kit mesh | normal |
| Cracked | 34–66% | crack decals, 2–3 merlons missing on the struck module | normal |
| Holed | 1–33% | one wall module holed, gate planks split, loose stones at the foot | thin smoke wisp |
| Breached (burning) | 0% | breached gate mesh, fire on 2–4 wall modules, smoke column | smoke plume + the word "Burning" (combat.md §10; world-forge), readable at 48 px |

Rates are combat.md's (−30% per won assault with a standard engine train, auto-repair +12.5% per
hour); the panel shows them as times ("Full in 1 h 10 m"), never as rates per tick.

## 7. Wards (shields)

| Rule (combat.md §9, §11; onboarding.md §4 owns the peace ward) | Shown as |
|---|---|
| No ward, truce or shield can START while a hostile march targeting the castle is on the road | "Ward unavailable — an attack is on its way (0:48)" |
| The peace ward ends when its owner attacks or scouts a player | march form and scout confirms: "Attacking ends your ward (3 h 12 m left)" |
| The breach truce (8 h) ends if the owner attacks or scouts a player; camps, gathering, healing and reinforcing keep it | same confirm, naming the truce |
| Ward state is public | pale-gold dome on the map; target cards say "Warded — 3 h 12 m" |
| Outcome cards never sell a ward | a held ward item may appear as "Raise ward (held: 2)"; never a gem price (outcome.md §1 rule 5) |

## 8. Under attack — the response budget

From the Near banner every response is ≤ 3 taps, and the whole set fits the 60 s band:

| Response | Taps | Deadline |
|---|---|---|
| Call allies | 1 | any time before contact (arrival honesty shows who can make it) |
| Recall one march / all | 2 / 2 | shows each march's home ETA vs contact, ✓ or ✗ |
| Swap the garrison lord | 3 | until contact: the resolver reads the castle as of arrival (combat.md §8 rule 4); the button locks 2 s before to absorb network delay (PROPOSAL) |
| Repair Walls & Gate (+10%, 30-min cooldown) | 1 | before contact |
| Heal all (beds for the defence) | 2 | before contact |
| Watch the attacker | 1 | — |

A player who does nothing still defends: the garrison, the fallback lord, towers and tools all
act on their own. Doing something must visibly matter (the report names it: "Your recall
brought 2,400 cavalry home 0:12 before contact").

| Fails when | Caught by |
|---|---|
| A response takes > 3 taps from the banner | [ ] `defence_flow_probe` response set |
| The first-time setup takes > 12 taps or > 60 s | [ ] `defence_flow_probe` setup pass: `DEFENCE FLOW OK - setup 12 taps 54s, checks 4/4` |
| A ward can be raised with a hostile march inbound | [ ] `warning_probe` ward case |

## 9. Checklist — any defence change

- [ ] Each warning band has its trigger, view, sound and push rule; bands re-tested with `warning_probe`.
- [ ] The Incoming card shows "?" plus the revealing tier for every unknown row.
- [ ] Setup ≤ 12 taps / 60 s; every response ≤ 3 taps from the banner.
- [ ] Reinforcement arrival honesty line present on every Reinforce send.
- [ ] Walls & Gate states identical in castle view, battle view and report; "Burning" readable at 48 px.
- [ ] No gem price on any defence surface during a Detected or Near band.
