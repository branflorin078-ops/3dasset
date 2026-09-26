# Defence — setup, warnings, reinforcements, walls, wards

What a lord does to be ready, what they see when an attack comes, and how allies help. The
rules (who defends, loss buckets when defending, wall durability and what happens at zero,
reinforcement capacity, ward rules) belong to design-forge `combat.md`; this file is how they
are shown and operated. Every number is a **PROPOSAL**. Taps as in [flows.md](flows.md).

## 1. What defends a castle

| Layer | Source | Shown in battle as (beats.md §3) | Art owner |
|---|---|---|---|
| Garrison troops | troops at home | squads, one per line | hero3d rig + units.md kit |
| Garrison lord pair | chosen in §3, else the fallback | `garrison_lord` chip + sworn gilt rim on the garrison | commander-forge |
| Wall and gate | castle kit, durability | `ram_hit`, `engine_shot`, `wall_state`, `breach` | castle-forge (states), blender-forge (kit) |
| Towers | the tower archetype (6 tiers) | `tower_fire` salvos | castle-forge |
| Defence tools | stocked tools (DEF-* art prefix exists; siege-forge's defensive tools: drop-stones, murder holes, hoardings) | `trap` | siege-forge |
| Stationed allies | reinforcements (§5) | `reinforce` with the allies' pennons | — |
| Infirmary beds | the hospital archetype | outcome card numbers | — |
| Ward | earned or held item | blue-free pale-gold dome on the map, no battle | effects.md shield/ward language |

## 2. Warnings — ETA bands and information tiers

The genre's watchtower warns of incoming attacks and improves reports with level; the pattern
we keep is **time to react, shown honestly**. Four bands by time to contact:

| Band | Trigger | Castle view | Realm view | Sound | Push (app closed) |
|---|---|---|---|---|---|
| Scouted | an enemy scout reached the castle | tracker row "Scouted by <name> 14:02"; readiness bubble (§4) shows | — | none | none; in the next digest |
| Detected | a hostile march targets the castle, any ETA | tracker row with ETA; fortress bubble "Attack 2:40"; Defence button | hostile line 8 px, pulse ≤ 1 Hz | `bt_warn_horn` once, −6 dB | 1 push if ETA ≥ 90 s and war alerts are on |
| Near | ETA ≤ 60 s | top banner ≤ 12% of the short side: countdown + **Call allies · Recall marches · Defence** | "Show attacker" (1 tap pans) | drum pulse every 2 s, −9 dB, ≤ 60 s | none |
| Contact | ETA 0 | battle-view offer; automatic when in castle view | clash marker for `T_fight` | contact stinger | 1 push with the result after the battle |

- Several marches: the banner counts them — "3 marches — first 0:42". Pushes group into ONE per
  60 s (core-loop A8 push budget: ≤ 4 per day; war alerts are a separate opt-in channel).
- Quiet hours (22:00–08:00 local, core-loop A8) mute war pushes unless the player turned on
  "Wake me for attacks". Default off: a castle is never lost for good while its lord sleeps
  (combat.md's loss table must hold that promise; outcome.md shows it).
- The warning band never changes the camera by itself (flows.md §7).

**What the warning reveals, by watchtower tier** — display PROPOSAL; combat.md's scouting tiers
win if they differ. The "Incoming" card (tap the tracker row) shows known rows and, for each
unknown row, "?" plus the tier that reveals it (the next goal stays visible):

| Watchtower tier | The Incoming card shows |
|---|---|
| 1 | attack incoming, ETA, arrival clock |
| 2 | + attacker name and alliance tag |
| 3 | + army size band (±25%) |
| 4 | + line mix (% per line, rounded to 10%) and the matchup strip vs the current garrison |
| 5 | + the lord pair |
| 6 | + exact counts per line and tier |

| Fails when | Caught by |
|---|---|
| An attack lands with no Detected row ever shown (hidden attack) | [ ] `warning_probe`: every hostile march creates the row at launch |
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
| 5 | Wall: Repair when below 100% | 1 | 3 |
| 6 | Allies may station troops: toggle (default on) | 1 | 2 |
| 7 | War alerts: on / off, and "Wake me for attacks" | 1 | 3 |
| | **Total** | **12** | **≤ 60 incl. reading** |

After the first setup every later check is ≤ 3 taps (bubble → Defence → one change).

**The Defence panel** (one screen, no sub-tabs):

| Zone | Content |
|---|---|
| Garrison | lord pair portraits, troops at home per line (medallions + counts), a matchup strip against the last known attacker |
| Walls | wall and gate durability bars with the state name (§6), repair time, Extinguish when burning |
| Towers and tools | tower tier; each tool type with stock / target and its DEF icon |
| Allies stationed | list: ally name, lines, count, arrival time; Send home (2 taps); capacity bar |
| Ward | state, time left, "Raise ward" (held items only) or the reason it is unavailable |

**Fallback lord** (PROPOSAL for combat.md): with no garrison lord set, or the set lord away,
the highest-level lord at home defends. The panel says it in one line: "Maud is marching —
Edwin will hold the walls". No lord at home at all: "No lord at home — the castle defends
without one" + Recall a lord (2 taps).

No stance picker unless combat.md defines garrison stances; if it does, ≤ 2 choices, 1 tap.

| Failure | Message | Offered |
|---|---|---|
| Tools at 0 | "No drop-stones stocked" | Stock tools (2 taps) |
| Infirmary full | "Infirmary full — wounded defenders will be lost" | Heal all (2 taps) |
| Wall burning | "Wall burning — losing 1% per minute" (rate from combat.md) | Extinguish (1 tap) |
| Ally capacity full | the ally sees "Castle full — 0 places" before sending | — |

## 4. The readiness bubble

A status bubble on the fortress (ui-forge status bubbles; counts inside the ux.md bubble
budget) shows **"Defence 3/4"** only when a check fails or a hostile march is Detected:

| # | Check | Pass when |
|---|---|---|
| 1 | Lord | a garrison lord is set and at home |
| 2 | Walls | wall ≥ 90% and not burning |
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
| Defender asks | Near banner → **Call allies** | 1 | a post in the alliance feed + a chat share card (chat-forge): "<name>'s castle — attack in 0:48 — Reinforce" |
| Ally answers | card → Reinforce → Send (defence preset) | 3 | "Arrives 0:38 before the attack ✓" or "Arrives 0:12 after ✗ — will defend the next attack" |
| Defender sees help | banner line | 0 | "2 allies marching — first arrives 0:21 before contact" |
| Defender sends home | Defence panel → ally row → Send home | 2 | the march leaves at once |

- **Arrival honesty**: the battle is resolved at contact (design-forge SKILL.md rule 5), so a
  reinforcement arriving after contact cannot join that battle. The Send button states it
  before the ally commits; it never blocks the send (the troops may be wanted for a second wave).
- In battle, stationed allies fight inside the garrison squads and show as pennons (≤ 6, then
  "+N"); their losses follow combat.md's "defending an ally" context and appear in THEIR outcome
  card with the defender's name ([outcome.md](outcome.md) §3).

## 6. Wall, gate and tower states

castle-forge supplies the meshes and decals; blender-forge builds kit pieces; battle-forge picks
the state from beat values and shows it the same way in castle view, battle view and report.

| State | Durability | Castle and battle view | Realm map (city 48–96 px) |
|---|---|---|---|
| Intact | 67–100% | kit mesh | normal |
| Cracked | 34–66% | crack decals, 2–3 merlons missing on the struck module | normal |
| Holed | 1–33% | one wall module holed, loose stones at its foot | thin smoke wisp |
| Breached | 0% (gate or one section) | breached mesh | smoke wisp |
| Burning (if combat.md chooses a burning state at 0) | — | fire on 2–4 wall modules, smoke column | smoke column + ember glow readable at 48 px (blender-forge architecture.md read distance) |

Repair and burning rates are combat.md's; the panel shows them as times ("Full in 1 h 10 m"),
never as rates per tick.

## 7. Wards (shields)

| Rule (PROPOSAL; combat.md and design-forge `monetization.md` decide) | Shown as |
|---|---|
| No ward can be raised once a hostile march targets the castle (the genre bars relocation while attacked; monetization bars selling shields during an attack) | "Ward unavailable — an attack is on its way (0:48)" |
| A ward ends when its owner attacks (the genre's newcomer shield breaks on attack) | march form confirm: "Attacking ends your ward (3 h 12 m left)" |
| Ward state is public | pale-gold dome on the map; target cards say "Warded — 3 h 12 m" |
| Outcome cards never sell a ward | a held ward item may appear as "Raise ward (held: 2)"; never a gem price (outcome.md §5) |

## 8. Under attack — the response budget

From the Near banner every response is ≤ 3 taps, and the whole set fits the 60 s band:

| Response | Taps | Deadline |
|---|---|---|
| Call allies | 1 | any time before contact (arrival honesty shows who can make it) |
| Recall one march / all | 2 / 2 | shows each march's home ETA vs contact, ✓ or ✗ |
| Swap the garrison lord | 3 | until contact − 5 s (PROPOSAL; combat.md) |
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
- [ ] Wall states identical in castle view, battle view and report; burning readable at 48 px.
- [ ] No gem price on any defence surface during a Detected or Near band.
