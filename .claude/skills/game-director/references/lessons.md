# Lessons — running the studio (real, 2026-09-24 → 2026-09-26)

1. **Delegated agents refused to author skill files** when the order reached
   them through a workflow script (commander-forge, first attempt): they judged
   `.claude/` config changes "not authorized by a script-computed task". Fix
   that worked: quote the owner's own words in the prompt AND have agents write
   drafts to `art/skills_draft/` for the lead to install.
2. **Blender 5.x broke the 4.0-proven toolkit in two places** (compositor
   `scene.node_tree` removed; Glare settings became sockets) and a third
   silently (GPU prefs wiped by `read_factory_settings`) — a baseline run
   before fanning out agents found all three in minutes.
3. **One GPU, many agents**: without the `forge_run.py` lock, parallel builders
   would have raced renders and bakes. With it, 8 builders shared one RTX with
   no collisions; previews stay small so the lock turns over.
4. **Shared ledger files get locked by readers.** Appending to
   `PROJECT_MASTER_MEMORY.md` while dozens of agents read it failed with "used
   by another process" — and the script still printed success. Retry the
   append in a loop and VERIFY the line landed (Select-String).
5. **Status polling is not free.** Parsing whole agent transcripts to see "what
   are they doing" timed out and wasted budget; check the output folders
   (renders, reports, locks) instead.
6. **Assumed facts are the costliest.** The design docs the owner's brief
   named were not on disk; the game's own data (`data/equipment.gd`) turned out
   to be the better brief — its 24 items are 6 four-piece sets, one per lord.
7. **Budgets are measured, not guessed.** "Is €200 enough for 50k players?" was
   answered from `core/sd_cost_probe.gd` (≈€20 worst case), not from rules of
   thumb — and the audit's own history shows one read-path bug cost more than
   everything else combined (≈€145/mo at 100k).
