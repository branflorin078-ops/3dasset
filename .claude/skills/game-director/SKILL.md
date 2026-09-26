---
name: game-director
description: The autonomous improvement loop for Castle Conquest — measures the game, scores it against the player-experience pillars of the genre's best live strategy games, picks the highest-value improvement, sends new or changed systems through design-forge for a numbered spec, routes the build to the house skill that owns that domain (design, art, 3D, castle, world, UI, story, shop, gameplay, cloud, ship, QA, audio, feel, l10n, onboarding, battle), builds it with agent teams, proves it with the harness battery, records it in the ledger, teaches the owning skill, and repeats. Use for "improve the game", "make the game better", "make it like Rise of Kingdoms but ours", "what's next", "keep going", autonomous improvement cycles, or any request that spans several domains.
---

# game-director — run every house skill as one studio

The owner's standing order (2026-09-26): **"don't wait for my approval — go
ahead; once everything is ready use the skills to make the game, improve it."**
This skill is how that order is carried out without breaking the game.

## Hard rules (the owner's binding rulings win over speed)

1. **The binding rulings in `CLAUDE.md` are never traded for progress**: keep
   the painted identity and evolve the main game; a live realm (no title
   menus, no single-player conventions); real construction elements, never
   boxes with stripes; **sacred balance constants stay** (autonomy does not
   extend to them — gameplay-forge's clamp and corridor rules apply); server
   and database spend within **€200/month at 50,000 players**.
2. **Autonomy ≠ irreversibility.** Before any change set: a dated checkpoint
   folder `_checkpoint_<date>_<topic>/` holding every file about to change (no
   git — owner's choice). Never delete an owner file; replaced shipped art goes
   to the checkpoint first.
3. **Nothing is "done" without pasted evidence** — the owning skill's harness
   plus the core gate (below), verdict lines quoted, renders/screens opened.
4. **One writer per file.** Every agent owns named files; shared files
   (ledger, TASK_BOARD, lessons) are written only by the lead.
5. **Don't redo landed work.** Read the ledger first; a ledger row with
   evidence is the truth.
6. **Owner-only items stay owner items** (keys, keystore, store accounts,
   billing, real-phone smoke). List them; never fake them.
7. **Every improvement is written back into the skill that owns it** (owner
   order, 2026-09-26). A cycle is not closed until the owning skill's
   references carry the new recipe, numbers and traps, so the next cycle —
   and every future session — starts smarter. memory-forge audits that this
   happened.
8. **Every asset is built through the skill** (owner order, 2026-09-26:
   "everything you are creating need to use the skill ... dont create fuck up
   shapes ... create hight quality assets with blender ... reserch and do it").
   3D = `blender-forge` (its lib + `tools/forge_run.py` + gates), references
   pulled with `reference-forge` FIRST. No primitive / box / blocky shapes, no
   kitbashed townsfolk for named characters, no side tools that bypass the
   skill (the ComfyUI image-model lane was cancelled for this). A capability
   the skill lacks is added to it as a staged, tested module — never
   improvised in a one-off script. Human figures are the standing
   exception: code cannot sculpt a face (blender-forge scope), so people
   go through the `hero3d` rig or the painted image lane
   (game-art-director), and blender-forge only finishes, lights and bakes.
9. **Design before build for anything a player will learn.** A new system,
   a changed rule, a new currency, event, or progression step goes through
   `design-forge` first: a `SYSTEM.md` with numbers, the free-player path,
   the server-cost line and its harness. Polishing art or fixing a bug
   does not need one.

## The studio — which skill owns what

| Domain | Skill |
|---|---|
| **Design**: systems, loops, progression, economy, combat rules, lords, map rules, alliance, seasons, events, monetization design, genre benchmark | `design-forge` |
| Hero-quality 3D props, weapons, equipment, rarity cards, baked GLB | `blender-forge` |
| Real references (Met CC0, owner boards) and the gap-closing loop | `reference-forge` |
| 2D painted art: icons, portraits, boards, prompts, `tools/assets.json` | `game-art-director` |
| The castle, town and building kit (shipped low-poly), castle view | `castle-forge` |
| The realm map, camps, AI lords, marches, map performance | `world-forge` |
| UI: events, menus, alliance, buttons, components, layout | `ui-forge` |
| Narrative: canon, voice, quests, acts, events, chronicle | `story-forge` |
| Bundles shop, offers, gems, IAP, monetization laws | `shop-forge` |
| Systems, balance, combat, progression, live systems | `gameplay-forge` |
| Backend: saves, sync, rules, anti-cheat, cost within €200 | `cloud-forge` |
| Builds, APK size, VRAM, performance, Play release | `ship-forge` |
| Harness battery, probes, shot diff, QA fuzzer, gates | `qa-forge` |
| Music, ambience, SFX, ducking | `audio-forge` |
| Motion, juice, ceremonies, particles, villager life | `feel-forge` |
| Localization, strings, fonts | `l10n-forge` |
| First session, return hooks, retention | `onboarding-forge` |
| The battle EXPERIENCE: deploy, march out, live siege replay from the resolver's beats, report | `battle-forge` |
| Adding a NEW feature end to end (design → owners → data → save migration → harness → ledger) | `feature-forge` |
| Keeping knowledge: ledger, memory, lessons, handoffs — nothing important lost | `memory-forge` |

A skill named here but absent from `.claude/skills/` is still a draft in
`art/skills_draft/` — install it (copy the folder) before routing to it.

## The cycle (repeat until the owner says stop)

1. **Read state** — `PROJECT_MASTER_MEMORY.md` §99 and the newest addenda,
   `upgrade/TASK_BOARD.md`, the newest critic/verify reports under `art/`.
2. **Measure** — regenerate and read the numbers, never quote stale ones:
   ```powershell
   $g = "C:/Users/Famil/AppData/Local/Microsoft/WinGet/Packages/GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe/Godot_v4.7.2-stable_win64_console.exe"
   & $g --headless --path godot --script res://core/audit.gd          # area scores /10
   & $g --headless --path godot --script res://core/backlog_gen.gd    # -> godot/GAME_IMPROVEMENT_BACKLOG.md ("Do these next")
   & $g --path godot --resolution 1080x1900 --script res://core/session_audit.gd   # the full-session player
   ```
   (`$g` is this machine's Godot; on any other machine set `$env:GODOT`
   and use `$g = $env:GODOT`.)
3. **Pick** — first read the pillar scorecard (below); then score candidates: player impact (which audit area, how far
   below 10) × confidence × cost; owner orders outrank everything. Take ONE
   change set per cycle that one team can finish and prove. See
   [references/cycle.md](references/cycle.md).
4. **Plan** — for a system change, the `design-forge` SYSTEM.md comes first
   (hard rule 9) and its harness becomes this cycle's proof. Then: owning skill, files touched (one writer each), the harness that
   proves it, the checkpoint list, the agents needed.
5. **Checkpoint** — copy every file in the plan into `_checkpoint_<date>_<topic>/`.
6. **Build** — run the owning skill's workflow with agents (team patterns and
   prompt rules in [references/teams.md](references/teams.md)).
7. **Prove** — the owning skill's harness + the core gate + the windowed
   suites the change can affect; a skeptic diffs against the checkpoint.
   Red → fix or restore from the checkpoint; never ship red.
8. **Record and teach** — a ledger row (id, what, evidence) in
   `PROJECT_MASTER_MEMORY.md`, `TASK_BOARD.md` updated, `backlog_gen` re-run;
   the owning skill's references UPDATED with the recipe that worked and its
   numbers, new traps into its `lessons.md` and into
   [references/lessons.md](references/lessons.md) (hard rule 7).
9. **Show** — the owner sees the result (renders, screenshots, numbers), then
   the next cycle starts without waiting.

## The core gate (after every change set)

Headless: `contrast_test, collision_audit, skin_contract_test, menu_test,
structure_audit, cv_keep_reconcile, pm_render_probe, fenv_b_weather_probe,
pf1_field_leak_probe, placement_test` · plus a real boot test (CLAUDE.md
"Real boot test"). Windowed when UI/layout could move: `layout_audit,
mm_probe, map_trap_probe, ux_flow_probe, w1f_aspect_sweep` (must print
`ASPECT SWEEP OK - 6 shapes, 0 faults`), `ux_touch_probe`, `a11y_audit`.

## The pillar scorecard — "as good as the genre's best, and ours"

`audit.gd` scores the game's areas. Beside it, keep a player-experience
scorecard in `upgrade/PILLARS.md`, re-scored every 5 cycles (0–5 each, one
line of evidence each; genre patterns in design-forge `references/benchmark.md`):

| # | Pillar | 5 means |
|---|---|---|
| 1 | Next goal always visible | every screen shows what to want next and how far away it is |
| 2 | Sessions that pay off at every length | 30 s, 5 min and 30 min sessions each end with visible progress |
| 3 | A city that shows its growth | every upgrade changes a silhouette someone else can see |
| 4 | A living realm | marches, camps, lords and allies visibly move on the map |
| 5 | Battles that are understood | the player can say why they won or lost (counters, lords, beats) |
| 6 | Lords worth investing in | each lord has a role, a path, and a reason to be fielded |
| 7 | Belonging | alliance help, gifts, rallies and territory make other players matter |
| 8 | A season with a story | the realm has a lifecycle; events have a calendar and a meaning |
| 9 | Fair money | a free player who plays well reaches the top; paid surfaces obey the money-law |
| 10 | One-hand readability | every core action ≤ 3 taps, readable at arm's length |

The lowest pillar with a cheap, provable fix is a strong cycle candidate
(cycle.md scoring still applies). A pillar never outranks a red harness or
an owner order.
