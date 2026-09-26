# The cycle in detail — picking and sizing work

## Candidate sources (in priority order)
1. **Owner orders** in the conversation or the newest ledger addenda.
2. **Red evidence**: a failing harness, a QA fuzzer inbox finding, a critic
   ITERATE verdict, a verifier WRONG claim. Red is fixed before new work.
3. **`GAME_IMPROVEMENT_BACKLOG.md` → "Do these next"** (regenerated, never
   hand-edited) and the "Quality assessment" area scores from `audit.gd`.
4. **TASK_BOARD queued waves** (W7 i18n, W8 economy — deliberately last,
   W9 difficulty, W10 retention/FTUE, W11 device pass, W12 polish, M1 alive).
5. **Pillar gaps**: the lowest pillars in `upgrade/PILLARS.md` (SKILL.md
   scorecard), turned into a design-forge SYSTEM.md before any build.
6. **Asset quality**: pieces with critic scores below 10/12, set sheets whose
   kit does not read as one lord's.

## Scoring a candidate
`value = impact × confidence ÷ cost`
- impact 1–5: how many players see it × how bad the gap is (an audit area at
  6/10 on the core loop beats a 9/10 corner).
- confidence 1–3: 3 = the owning skill has a proven recipe and a harness.
- cost 1–5: agents × hours × risk of touching shared files.
Take the top candidate that fits ONE team. Log the runners-up in TASK_BOARD.

## Sizing a change set
- One domain owner, ≤ 10 agents, ≤ ~12 files written, every file with one writer.
- A system change carries its design-forge `SYSTEM.md` (REVIEWED) in the
  plan; the spec's harness is the cycle's proof, and its predictions are
  checked against the measured numbers after ship (spec §13).
- It must end in a harness verdict. If no harness can prove it, the first
  change set is WRITING that harness (qa-forge).
- Art change sets end in renders the owner can see; engine change sets end in
  a screenshot from a windowed suite.

## Things that are never a cycle's shortcut
- Editing sacred balance constants, the frozen resolver shape, or the clamp
  ledger to make a test pass (gameplay-forge).
- Hand-editing generated files (`GAME_IMPROVEMENT_BACKLOG.md`, catalogue).
- Blessing a shot-diff baseline to make drift disappear without inspecting it.
- Replacing shipped painted art with a render without a checkpoint and a
  side-by-side shown to the owner.

## Cycle record (append to the ledger)
```
| <ID> | P<n> | <what changed, why, owning skill> | evidence: <harness verdict lines>,
  <render/screenshot paths>, checkpoint _checkpoint_<date>_<topic>/ | TESTED |
```
