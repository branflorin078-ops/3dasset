---
name: design-forge
description: Game-design brain for Castle Conquest — designs and reviews systems at the depth of the genre's best live 4X strategy games (core loop, city progression, economy, troops and combat, lords/commanders, realm map and marches, alliances, seasons and live events, monetization, onboarding, HUD/UX). Benchmarks a system against the genre, extracts the underlying PATTERN (never the content), designs our improved version with real numbers, writes a SYSTEM.md spec with formulas, tuning sheet and the harness that will prove it, and hands implementation to the owning forge skill. Use for "design X", "how should X work", "make it like Rise of Kingdoms / the big strategy games but better", "is this system good", economy or progression balance questions, new features before feature-forge builds them, or any design review. Not for art (game-art-director / blender-forge) or for writing engine code (the domain forges).
---

# design-forge — the pattern, not the content; the number, not the adjective

The big mobile 4X games (Rise of Kingdoms is the reference point the owner
named) are not good because of their content. They are good because every
system answers four questions precisely: **what does the player want next,
what stands between them and it, how long is that wait, and who else sees
them get it.** This skill makes our systems answer the same four questions —
with our own fiction, our own numbers, and fixes for the places where those
games hurt their players.

## Hard rules

1. **Pattern, never content.** We may learn how a system is STRUCTURED
   (gates, curves, cadence, loops). We never copy names, numbers tables,
   UI layouts, art, characters, event names or text. Every borrowed pattern
   is written down as a principle in our words, then redesigned in our
   fiction with at least one deliberate difference ("our move").
2. **The binding rulings win** (CLAUDE.md, game-director hard rule 1): the
   painted identity; a live realm (no title menus, no single-player
   conventions); **sacred balance constants stay** — design proposals that
   touch them are written as proposals to the owner, never applied;
   server + database within **€200/month at 50,000 players**; the money-law
   (no war imagery over a buy button; paid surfaces sell goods, works and
   journeys — see references/monetization.md).
3. **Numbers or it isn't a design.** Every system spec carries: the loop it
   feeds, its sources and sinks, its curve (formula + a table of the first,
   middle and last levels), its timings in real minutes, and the metric
   that proves it works. "Feels rewarding" is not a spec line.
4. **Our game's shape, not theirs.** Five troop lines × 10–11 tiers, the
   four-tier rarity ladder (Issued → Sound → Fine → Masterwork), lords with
   four-piece sets, the frozen resolver shape and its battle beats, the
   barbarian camps and AI lords. A pattern that needs a different shape is
   adapted to ours or rejected — never used to reshape the game silently.
5. **Cost is a design constraint, not an afterthought.** Anything that
   ticks on the server (real-time marches, live battles, map scans) is
   costed with `core/sd_cost_probe.gd` before it is proposed (game-director
   lesson 7). Prefer designs that are **functions of time** (a march is
   `start, end, path` → position is computed, never simulated) and
   **resolved deterministically** at a moment (arrival → resolver → beats
   replayed on the client).
6. **Fairness is a feature.** For every system, write down how a
   non-paying player who plays well reaches its top, and how long it takes.
   If the honest answer is "never", the system is redesigned or flagged to
   the owner — this is where the genre loses its players (references/benchmark.md).
7. **Specs end in a harness.** A design is handed off with the probe or
   audit that will measure it (qa-forge writes it if missing). No harness,
   no handoff.

## The design loop

1. **Frame** — which player want does this serve (power, progress, social
   standing, collection, mastery, story)? Which audit area / backlog line /
   owner order asked for it? Write the four questions above for it.
2. **Read our game first** — the existing data files (`data/*.gd`), the
   systems it touches, the ledger rows that already landed. A design that
   ignores shipped systems is a rewrite in disguise.
3. **Benchmark** — read the matching section of
   [references/benchmark.md](references/benchmark.md): how the genre does it,
   the transferable pattern, and where it falls short for players.
4. **Design our version** — the pattern restated in our fiction, plus the
   fix for the genre's weak spot, plus our twist. Use the system reference
   for the domain (table below).
5. **Number it** — formulas and a tuning table in
   [references/numbers.md](references/numbers.md) style: curves, timings,
   source/sink balance, and a simulation of day 1 / day 7 / day 30 / day 90
   for three player types (free, light spender, heavy spender).
6. **Spec it** — `design/<system>/SYSTEM.md` from the template in
   [references/spec-template.md](references/spec-template.md). Name the
   owning skill, the data files, the save migration, the harness.
7. **Review** — the red-team checklist (below). Then hand off: small
   change → the owning forge; a new feature → `feature-forge`; anything
   touching sacred constants or spend → the owner, as a proposal.
8. **Learn** — after it ships, compare the harness numbers with the spec's
   predictions; write the gap and the fix into
   [references/lessons.md](references/lessons.md).

## Which reference for which system

| System | Reference | Implementing skill |
|---|---|---|
| Moment-to-moment, session, daily and weekly loops; timers, speed-ups, help | [core-loop.md](references/core-loop.md) | gameplay-forge |
| Castle/keep level gates, building graph, queues, research, visual evolution | [progression.md](references/progression.md) | gameplay-forge + castle-forge |
| Resources, sources/sinks, protection, gathering, upkeep, inflation | [economy.md](references/economy.md) | gameplay-forge + cloud-forge |
| Troop lines, tiers, counters, wounds and hospital, power, marches, rallies | [combat.md](references/combat.md) | gameplay-forge + battle-forge |
| Lords: rarity, skills, talents, pairing, sets, acquisition, power creep | [lords.md](references/lords.md) | gameplay-forge + story-forge |
| Realm map, zones, camps, AI lords, territory, scouting, zoom levels | [world.md](references/world.md) | world-forge |
| Alliance ranks, help, gifts, tech, territory, rallies, diplomacy | [alliance.md](references/alliance.md) | gameplay-forge + ui-forge |
| Realm lifecycle, seasons, event calendar, competitive modes | [liveops.md](references/liveops.md) | gameplay-forge + story-forge |
| Shop, bundles, VIP-like ladders, what may be sold | [monetization.md](references/monetization.md) | shop-forge |
| First session, first week, return hooks | [onboarding.md](references/onboarding.md) | onboarding-forge |
| HUD, information architecture, notifications, read distances | [ux.md](references/ux.md) | ui-forge |
| The genre teardown itself (all of the above, per system) | [benchmark.md](references/benchmark.md) | — |
| Formulas, curves, simulations, the tuning sheet | [numbers.md](references/numbers.md) | — |

## Red-team checklist (every spec, before handoff)

1. **Next goal visible?** At every moment the player can see the next
   thing to want and roughly how far away it is.
2. **Wait honest?** Every timer shows its real length; every speed-up says
   exactly what it saves. No hidden gates behind a "soon".
3. **Free path to the top** exists and its length is written down (rule 6).
4. **Loss recoverable?** A bad fight costs time, not the account: what
   comes back (wounded → healed), what is gone, how long to rebuild.
5. **Others see it?** Progress that nobody sees is progress nobody chases
   (city visuals, map presence, titles, alliance feed).
6. **Sources = sinks** within ±10% at day 30 for the median free player
   (numbers.md simulation), or the surplus/deficit is deliberate and named.
7. **Server cost** measured or estimated with its formula (rule 5).
8. **Exploit pass**: multi-accounting, farm accounts, time-zone abuse,
   alliance-hopping, refund abuse, bot gathering — each has an answer.
9. **Readable on a phone in one hand**, in 10-second sessions and 20-minute
   ones (ux.md).
10. **Fits the fiction**: it is a medieval lord's realm, not a spreadsheet.
    Every system has a diegetic name and place in the castle or the realm.

## Output contract

Every design task ends with: the SYSTEM.md path; the four questions answered
in four lines; the tuning table; the free-player path length; the server
cost line; the harness named; the owning skill named; and the owner
decisions required (if any) listed separately. Nothing else is "a design".
