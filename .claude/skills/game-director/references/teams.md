# Teams — how to staff a change set with agents

## Proven patterns (all used on this project, 2026-09-26)
- **Mapper → author → verifier-fixer** (skills, specs, audits): mappers read the
  code into structured notes; the author writes from the notes; the verifier
  checks ≥ 25 claims against the repo and fixes the draft. Pipeline it, so
  each verifier starts when its author finishes.
- **Builder ↔ critic** (art): builders render previews, LOOK at every image,
  score the 12-point checklist, iterate ≤ 5 loops; a critic scores all
  finished pieces afterwards. Add reference-forge's side-by-side compare
  when proportion/construction is the weak axis.
- **Skill-engineer beside builders**: one agent owns the library; everyone
  else imports it. The engineer edits a STAGED copy (`FORGE_LIB` preset) and
  swaps atomically only when its tests are green.

- **Designer → red-team → builder** (systems): a design-forge agent writes
  SYSTEM.md with numbers; a second agent red-teams it (the ten checks,
  re-running curve.py / econ_sim.py); only a REVIEWED spec is built.

## Rules for every agent prompt
1. **Quote the owner's own words** for the order. Delegated agents have
   refused work that looked "script-computed" (lessons #1).
2. **Name the files the agent owns**, and forbid the rest (one writer per file).
3. **Never let an agent write into `.claude/`** — agents write drafts to
   `art/skills_draft/<name>/`; the lead installs.
4. **Blender only through the lock**: `py .claude/skills/blender-forge/tools/forge_run.py run …`
   (one GPU; many agents queue). Never call blender.exe directly, never kill it.
5. **Give the evidence standard**: verdict lines verbatim, renders opened,
   honest stop after 5 loops with the residual gap stated.
6. **Effort**: the owner authorized Opus at max effort, up to 10 agents per team.

## Where outputs land
| kind | folder |
|---|---|
| 3D assets | `art/forge/assets/<ID>/` (build.py, out/, REPORT.md) |
| references | `art/references/<ID>/` (refs.json, refs_sheet.png) |
| UI renders | `art/ui_forge/…` |
| story drafts | `art/story_forge/…` |
| skill drafts | `art/skills_draft/<name>/` (+ VERIFY.md) |
| system designs | `design/<system>/` (SYSTEM.md, tuning, econ/curve outputs) |
| genre benchmarks (numbers only) | `art/benchmarks/<game>/` |
| critic reports | next to what they judge (`CRITIC_REPORT.md`, `CRITIC.md`) |
| game changes | in place, after a checkpoint |
