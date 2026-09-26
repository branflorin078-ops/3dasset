# blender-forge — install

1. Install Blender 4.0 or newer and make sure `blender` runs from a terminal.
2. Copy this folder into your project as `.claude/skills/blender-forge/`.
   Claude Code reads `SKILL.md` automatically.
3. Test it: `./run_chain.sh` (Linux/macOS) or `.\run_chain.ps1` (Windows —
   goes through the lock runner `tools/forge_run.py chain`). It rebuilds the Sunforged greatsword,
   bakes and exports `EQ-leg-blade_sunforged.glb`, re-imports it to verify, and
   renders the final card into `out/`.
4. Ask Claude Code for any asset: "Build the Vigilkeeper Sallet with
   blender-forge." It will follow SKILL.md: brief → blockout → real forms →
   materials → preview + critique → bake → export → round-trip proof.

Scope: weapons, armour, jewellery, props, castle pieces. Not faces or
characters — those stay in the image pipeline (commander-forge).
