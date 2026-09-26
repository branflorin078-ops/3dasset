export const meta = {
  name: 'forge-commander-kits',
  description: 'blender-forge team: skill-engineer upgrades the skill; 7 builders forge every commander kit (24 game items + hall lords props) at 4 rarities; critic reviews all',
  phases: [
    { title: 'Forge', detail: 'skill-engineer + 7 builders in parallel, Blender serialized by lock' },
    { title: 'Critique', detail: 'art-critic reviews every card' },
  ],
}

const SK = 'D:/CastleConquest/.claude/skills/blender-forge'
const RUN = `py ${SK}/tools/forge_run.py run <script.py> <mode> <outdir> [tier]`

const COMMON = `
CONTEXT — Castle Conquest (Godot 4 mobile medieval castle-strategy game, repo D:/CastleConquest, Windows, PowerShell 5.1 only: no &&, use ';').
You work with the blender-forge skill at ${SK}. BEFORE building, read: ${SK}/SKILL.md, ${SK}/references/lessons.md (every item), forms.md, materials.md, glow.md, lighting-render.md, export.md, qa.md, and study ${SK}/examples/sunforged_greatsword.py (the proven reference build: loft/lathe/sweep forms, layered materials, add_glow masks, embers, backdrop_radial, frame_camera, make_bake_target+bake_pbr+export_glb, quality_report) and ${SK}/lib/forge.py (the library).
QUALITY BAR: open D:/CastleConquest/art/forge/baseline/sunforged_final.png with Read — that is the canon Legendary card. Match that craft level.

ENVIRONMENT (verified today): Blender 5.2.1, RTX 3500 Ada via OptiX (forge.render_setup auto-selects GPU now), 20 CPU cores. The full Sunforged chain (bake+export+verify+1600px final) takes 74 s. Previews at 768 px / 48 samples take seconds.

HARD RULES:
1. Launch Blender ONLY through the lock runner: ${RUN}
   It serializes ALL Blender jobs machine-wide (8 agents share one GPU; you will sometimes wait — that is normal). Never call blender.exe directly. Never kill any blender process. Use the PowerShell tool with timeout 600000.
   The runner passes argv after '--' as [mode, outdir, tier...]; your script reads MODE=argv[0], OUT=argv[1], TIER=argv[2] if present. Import the lib exactly like the example: sys.path.insert(0, os.environ.get("FORGE_LIB") or <skill>/lib); import forge as F.
2. You may NOT edit anything under ${SK} (the skill-engineer owns lib/forge.py, tests, tools, docs). Put helper operators you invent in your own asset folder (e.g. a <set>_lib.py beside your build scripts). Report reusable ones so they can be promoted into the library.
3. Original designs only — real medieval history is the reference, the design is ours. Never imitate any existing game's items. Never model a face or a body.
4. Look at EVERY render you produce (Read the PNG). A render you did not inspect is not a result.
5. Build at real scale in metres, +Z = the object's length/up. Pivot: grip centre (weapons, horns, staffs), bottom of neck ring (helms), base centre (armour, tokens, plinth).

THE GAME'S RARITY (source of truth, data/equipment.gd): every item exists at FOUR tiers, per instance: common="Issued", rare="Sound", epic="Fine", legendary="Masterwork". Map to F.TIERS: common = NO add_glow, neutral cool-white rim at low power; rare/epic/legendary = add_glow(mb, mask, tier) with F.TIERS[tier] (rare is PROVISIONAL — sapphire, the skill-engineer is calibrating it in parallel) and rim colour F.TIERS[tier]['rim']. The GEOMETRY is identical across tiers; the light, rim, glow and (optionally) one finish step (field -> polished -> gilded accents) carry the rank. The rune/glow lives in engraved grooves or inlay (object-space masks), never as floating effects. Do not use the 'mythic' tier.

PER-ASSET PROCESS (definition of done):
 a) Brief: asset id, the game description (below) — every noun in it must be visible — 3 real-history construction facts, 1 original twist, triangle budget (source <= 40k).
 b) Silhouette blockout, judged as a black shape (render it small); fix until it reads.
 c) Real forms: loft/lathe/sweep/subdivided cages. No primitive is final. Bevel every hard edge (F.hard_surface).
 d) Layered materials (mat_metal/mat_leather/mat_cloth/mat_gem ... with wear + cavity), glow masks for rare+.
 e) Preview (768 px) -> open it -> score the 12-point checklist in qa.md -> fix the first failure -> repeat. MAX 5 critique loops per asset. If an asset cannot reach the bar after 5 (likely candidates: fur, mail, soft cloth), STOP on it, keep your best, and report honestly with evidence and a proposed alternative route (e.g. card-only image pipeline).
 f) Final cards: 1024 px, square, identical camera and rig for all four tiers: card_common.png, card_rare.png, card_epic.png, card_legendary.png. Then tile them into one labelled sheet.png (Pillow is available: py -c "from PIL import Image").
 g) Export (legendary tier look): make_bake_target(parts, name, decimate=...) to <= 12,000 triangles, bake_pbr(size=1024, sources=parts), set pivot AFTER bake, quality_report (all topology gates must be 0: non_manifold, open_boundary, uv_zero_area, loose_verts, degenerate), export_glb as <ID>.glb. Then round trip: ${RUN.replace('<script.py>', SK + '/examples/verify_glb.py').replace('<mode>', 'verify').replace(' [tier]', '')} with outdir = your asset's out folder (it takes the newest .glb there) and open the _roundtrip.png.
 h) Write <asset folder>/REPORT.md: id, status (SHIP / ITERATE / CARD_ONLY / FAILED), the design brief, critique loops used, QA_GAME and IMPORT numbers VERBATIM, file list, lessons learned (new traps), problems.
FOLDERS: each asset gets D:/CastleConquest/art/forge/assets/<ID>/ with build.py and out/ (renders, logs, GLB, textures). Do not write anywhere else except your own set helper file in D:/CastleConquest/art/forge/assets/.
KNOWN, NOT YOURS TO FIX: baked emission_strength on Blender 5.2 reads lower than the old 4.0 baseline (3.054 vs 13.383) — the skill-engineer is bisecting it; just report your numbers.
Your FINAL message must follow the schema: per asset status, paths, QA numbers, and any reusable operator you wrote.`

const SETS = [
  { key: 'household', lord: 'Lord Edwin — the inherited veteran; steady, unspectacular, has never lost a rearguard. House colour: household blue (#2B4A99 family); plain, well-kept, old-fashioned gear.',
    items: [
      ['EQ-armingsword', 'Arming Sword', 'weapon', 'A knight\'s sword, gold wheel pommel, crimson grip.', 'Nothing clever about it. It has never once failed him.'],
      ['EQ-gambeson', 'Gambeson', 'armour', 'Quilted oak-brown, brass points.', 'Thirty layers of linen. It has stopped more than mail has.'],
      ['EQ-nasal', 'Nasal Helm', 'helm', 'An older shape, with a mail aventail.', 'His father\'s. He has never seen a reason for a newer one.'],
      ['EQ-banner', 'War Standard', 'token', 'Furled on a dark oak pole, gold finial.', 'While it is up, they know where the line is meant to be.'],
    ] },
  { key: 'hammer', lord: 'Lord Alric — wins quickly or not at all; aggressive; house crimson (#8E1B1B family); heavy, blackened-and-bright plate, no shield.',
    items: [
      ['EQ-greatsword', 'Greatsword', 'weapon', 'Two-handed, leather-bound, the fuller engraved.', 'You cannot hold a shield and swing this. He made his choice.'],
      ['EQ-fullplate', 'Full Plate', 'armour', 'Cuirass and pauldrons, hammered finish.', 'He can fight all day in it. He cannot march all day in it.'],
      ['EQ-bascinet', 'Bascinet', 'helm', 'Visored, the visor raised.', 'He fights with it up. He has been told about this.'],
      ['EQ-relic', 'Reliquary', 'token', 'Small gold pendant with an amber window.', 'Nobody asks whose finger it is.'],
    ] },
  { key: 'longshot', lord: 'Lady Elena — archer-commander; decides a siege on the approach; house green (#3E6B3A family); light, quiet, leather-and-cloth gear.',
    items: [
      ['EQ-warbow', 'War Bow', 'weapon', 'Tall yew, gold tip nocks, a cream string.', 'Drawn to the ear, not the chest. That is the whole difference.'],
      ['EQ-brigandine', 'Brigandine', 'armour', 'Crimson cloth over plates, gilt rivet rows.', 'Plates on the inside. From the outside it is only a coat.'],
      ['EQ-hood', 'Archer\'s Hood', 'helm', 'Soft leather, a gold clasp at the throat.', 'Nothing over the ears. She needs to hear the string.'],
      ['EQ-wolfcloak', 'Wolf-fur Cloak', 'token', 'Grey wolf fur, a gold chain clasp.', 'She has slept in worse places than this cloak has.'],
    ] },
  { key: 'charge', lord: 'Ser Rowan — cavalry commander; rides at the flank and does not look back; crimson-and-cream tourney colours; polished, showy, built for the charge.',
    items: [
      ['EQ-lance', 'Lance', 'weapon', 'Crimson-and-cream spiral, steel point, leather vamplate.', 'One use, properly done, and the line is already broken.'],
      ['EQ-cuirass', 'Cuirass', 'armour', 'Polished steel with a gold rope border.', 'Polished every morning, whatever the night was like.'],
      ['EQ-greathelm', 'Great Helm', 'helm', 'Gold cross reinforcement over the face.', 'You can see almost nothing in it. That is rather the point.'],
      ['EQ-warhorn', 'War Horn', 'token', 'Aurochs horn, silver bands, a leather strap.', 'One note. Everyone on both sides knows what it means.'],
    ] },
  { key: 'measuredwall', lord: 'Master Godric — siege engineer; has never stormed a wall he could take down instead; bronze instruments, soot, practical iron; nothing decorative that is not also a tool.',
    items: [
      ['EQ-warhammer', 'Engineer\'s Warhammer', 'weapon', 'Faceted steel head, oak haft, iron langets.', 'He uses it on timber far more often than on men.'],
      ['EQ-hauberk', 'Mail Hauberk', 'armour', 'Riveted, oiled steel rings.', 'Twenty thousand rings. He knows, because he counted once.'],
      ['EQ-kettle', 'Kettle Helm', 'helm', 'Iron, wide-brimmed, honestly dented.', 'A brim keeps the rain off the drawings. And other things off the head.'],
      ['EQ-rule', 'Engineer\'s Rule', 'token', 'Brass, folding, on a leather thong.', 'He measures the wall before he agrees to break it.'],
    ] },
  { key: 'standingline', lord: 'Dame Maud — the defender who held a breach for two days; the line did not move; household blue with gold; dented, maintained, formidable plate.',
    items: [
      ['EQ-pike', 'Tower Pike', 'weapon', 'Leaf blade, a tassel of crimson cord.', 'Set the butt, brace, and do not move. That is the drill.'],
      ['EQ-oathplate', 'Oathplate', 'armour', 'Masterwork plate, gold inlay, a wax-sealed oath ribbon. OWNER NOTE: it must read as ARMOUR first — a breastplate with an oath engraved into the metal; the ribbon is secondary.', 'The ribbon is the oath. The plate is only what carries it.'],
      ['EQ-crownhelm', 'Crown Helm', 'helm', 'A commander\'s bascinet under a gold circlet.', 'Worn so the line can find her without asking.'],
      ['EQ-signet', 'Signet Ring', 'token', 'Gold, with a carnelian seal.', 'Pressed into wax, it has ended more sieges than she has.'],
    ] },
  { key: 'hall', lord: 'The two lords of the HALL — Master Faber (the King\'s Armourer: leather and bronze, fire at the rim, rune-struck tools) and Old Fable (the King\'s Chronicler: road-grey wool, one gilt line, lantern light). These are their SIGNATURE OBJECTS plus the hall\'s stage plinth. No rarity sheet needed for the plinth (render it lit sworn/unsworn instead: ring glow on vs off).',
    items: [
      ['CMD-faber-hammer', 'Faber\'s Forge Hammer', 'signature', 'The great forge hammer: faceted iron head, oak haft, rune-struck cheeks, iron langets, a peen cap.', 'It has made more war than it has fought.'],
      ['CMD-fable-staff', 'Fable\'s Lantern Staff', 'signature', 'An iron-shod walking staff; a small bronze reading lantern with glass panes hangs under the head, its flame the one warm light.', 'The realm\'s memory travels at night.'],
      ['CMD-fable-chronicle', 'The Chronicle', 'signature', 'A thick bound chronicle: tooled leather boards, brass corners, a clasp, and an iron chain from its spine.', 'He remembers every deed, including yours.'],
      ['CST-hall-plinth', 'The Hall Plinth', 'castle-kit', 'An octagonal two-course stone dais, ~1.15 m across, gilt fillet between courses, a recessed rune ring inlaid flush in the top face (the ring is the glow: dark for an unsworn lord, warm gold for a sworn one).', 'Status is light, never particles.'],
    ] },
]

const BUILD_SCHEMA = {
  type: 'object',
  properties: {
    set: { type: 'string' },
    assets: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          status: { type: 'string' },
          sheet: { type: 'string' },
          glb: { type: 'string' },
          qa: { type: 'string' },
          loops: { type: 'number' },
          problems: { type: 'string' },
        },
        required: ['id', 'status'],
      },
    },
    reusable_operators: { type: 'array', items: { type: 'string' } },
    lessons: { type: 'array', items: { type: 'string' } },
  },
  required: ['set', 'assets'],
}

const SKILL_PROMPT = `You are the SKILL-ENGINEER for the blender-forge skill at ${SK}. You alone own ${SK}/lib/forge.py, ${SK}/tests/, ${SK}/tools/, ${SK}/examples/, ${SK}/SKILL.md, ${SK}/references/*.md, ${SK}/TEAM.md. Eight other agents (asset builders) are importing lib/forge.py LIVE in parallel right now.
${COMMON.split('HARD RULES:')[0]}
SAFETY RULE FOR THE LIBRARY: never leave lib/forge.py broken even for a moment. Work on a staged copy: copy lib/ to D:/CastleConquest/art/forge/_staging_lib/, edit there, run tests with $env:FORGE_LIB = 'D:/CastleConquest/art/forge/_staging_lib' set before calling the runner (the runner respects a preset FORGE_LIB), and only when the whole suite is green replace lib/forge.py atomically (Copy to forge.py.new then Move-Item -Force). Keep backward compatibility with Blender 4.0-4.x AND 5.x (the live env is 5.2.1). Launch Blender ONLY via: ${RUN} (serialized lock; never call blender.exe directly; never kill blender).

ALREADY DONE BY THE LEAD TODAY (verify, don't redo): render_setup was patched for 5.x (compositing_node_group + NodeGroupOutput; Glare settings as sockets via _glare_bloom; Size mapped 2^(size-9); Strength 0.35 provisional); gpu_setup() probes OptiX>CUDA>HIP>Metal; TIERS['rare'] added PROVISIONALLY; tools/forge_run.py (lock runner, --factory-startup, FORGE_LIB preset honoured) and run_chain.ps1 written; run_chain.sh verify-arg bug fixed. Baseline on 5.2: 11,946 tris, all topology gates 0, round trip OK, chain 74 s — BUT baked emission_strength = 3.054 where the 4.0 baseline recorded 13.383.

YOUR TASKS, in priority order (test-first; one change at a time; whole suite green before each swap):
1. EMISSION REGRESSION. Bisect on the real Sunforged data at tiny resolution (lessons #16): why does bake_pbr's emission peak read 3.054 on 5.2 vs 13.383 on 4.0? Candidates to test, not guess: Noise Texture output range/normalize changes, Math POWER, Map Range defaults, ColorRamp, the EMIT bake pass in 5.x, Principled emission socket linkage via IN table, sample count. Find the root cause with evidence; fix it if it is a regression, or document that 13.383 was the anomaly. Sunforged topology numbers must not change.
2. CALIBRATE GLOW + BLOOM UNDER 5.2: render the Sunforged greatsword at common/rare/epic/legendary/mythic with IDENTICAL camera and rig (mythic kept for the library) at 768 px; open each; tune the provisional TIERS['rare'] (sapphire, contained, dimmer than epic, must read in half a second) and the 5.x Glare Strength/Size mapping so bloom is a halo not a haze. Write tools/rarity_sheet.py (Pillow: tile N labelled PNGs into one sheet). Deliver D:/CastleConquest/art/forge/calibration/tier_sheet.png.
3. REGRESSION SUITE: ${SK}/tests/ runnable with ONE command via the runner, < 5 min: forms watertight (loft with tip, lathe with caps, sweep welded), every mat_* builds, a tiny glowing bake gives emission > 1 and the joined target has 0 zero-area UV faces, a GLB round trip keeps 1 mesh / 1 material / emission strength / triangle count. Document the command in SKILL.md.
4. NEW OPERATORS (test-first, in this order, as many as you can finish green): helm_shell (lathe bowl + tail loft), boolean_cut with bevel cleanup (visor slits, sights), plate (armour plate from a profile curve with thickness, rolled edges, and lames), rivet_row (instanced rivets along a path), strap_buckle, gem cuts (gem_brilliant, gem_cabochon). Each with a watertight test.
5. MISSING FILES the SKILL.md already references: examples/_template_asset.py (args: mode outdir tier; renders a probe finial — the one-command smoke test) and TEAM.md (the agent team: skill-engineer, forge-builder, art-critic, qa-engineer, godot-integrator; ownership; the lock).
6. DOCS: SKILL.md environment notes for Blender 5.x / Windows / GPU (OptiX) / forge_run / real timings; append NUMBERED lessons to references/lessons.md: scene.node_tree removed in 5.0 (compositing_node_group + NodeGroupOutput); Glare settings are input sockets on 4.5+; run_chain verify-arg bug; user add-ons (MCP bridges, human generators) load into background jobs unless --factory-startup; plus whatever the emission bisection proves.
Look at every render you make. Report: per task DONE/PARTIAL with evidence (test output verbatim, calibrated numbers, file paths, timings) and a diff summary of lib/forge.py.`

phase('Forge')
const RESUME = `RESUME NOTICE (read first): an earlier run of this exact job was cut off by a usage limit at ~10:10 on 2026-09-26. Your work is ON DISK. Before anything else, inspect everything you own (list your folders, open your newest renders and sheets, read your build.py/logs/notes) and CONTINUE from where it stands. Never rebuild a finished piece from scratch; never overwrite a better earlier result without comparing both. A piece that already has its GLB may need only the missing steps (round trip, REPORT.md, set sheet). The owner is paying for this run: be economical — no re-reading of material you already applied, no redundant renders. The reference-forge skill is installed (D:/CastleConquest/.claude/skills/reference-forge/) — use its compare loop on any piece whose proportions or construction are the weak axis.\n\n`
const skill = () => agent(RESUME + `SKILL-ENGINEER RESUME: check which of your 6 tasks are already done by inspecting ${SK}/tests/ (run the suite once via 'py ${SK}/tools/forge_run.py test'), ${SK}/TEAM.md, ${SK}/examples/_template_asset.py, D:/CastleConquest/art/forge/calibration/, the staged lib at D:/CastleConquest/art/forge/_staging_lib/ vs ${SK}/lib/forge.py, and ${SK}/references/lessons.md; finish only what is missing.\n\n` + SKILL_PROMPT, { label: 'skill-engineer', phase: 'Forge', effort: 'max' })
const builders = SETS.map(s => () => agent(
  RESUME + `You are a FORGE-BUILDER (senior hard-surface technical artist). You own the "${s.key}" set: ${s.lord}
${COMMON}
YOUR ASSETS (build in this order; the FIRST finished piece becomes the set's CANON — every sibling must match its materials, finish, glow hue and strength, and motif scale, so the four read as one lord's kit):
${s.items.map(([id, nm, slot, desc, line], i) => `${i + 1}. ${id} — "${nm}" (${slot}). Game description: "${desc}" Flavour line: "${line}"`).join('\n')}
Folder per asset: D:/CastleConquest/art/forge/assets/<ID>/ . Shared helpers for your set: D:/CastleConquest/art/forge/assets/_${s.key}_lib.py (yours alone).
Pace yourself: keep previews small and quick so the shared lock turns over fast; finals and exports only after the critique passes. When all assets are done (or honestly stopped), also tile your set's four legendary cards into D:/CastleConquest/art/forge/assets/_${s.key}_set_sheet.png and open it — judge set coherence and fix the weakest outlier if a loop remains.`,
  { label: `builder:${s.key}`, phase: 'Forge', schema: BUILD_SCHEMA, effort: 'max' }))

const results = await parallel([skill, ...builders])
const skillOut = results[0]
const built = results.slice(1).filter(Boolean)
log(`forge done: ${built.length} sets returned; skill-engineer ${skillOut ? 'returned' : 'missing'}`)

phase('Critique')
const critic = await agent(
  `You are the ART-CRITIC (exacting art director, read-only except your one report). Review every asset the forge team produced for Castle Conquest.
Read D:/CastleConquest/.claude/skills/blender-forge/references/qa.md (the 12-point checklist) and lessons.md. The canon quality bar: D:/CastleConquest/art/forge/baseline/sunforged_final.png (open it).
Assets live under D:/CastleConquest/art/forge/assets/<ID>/ (REPORT.md, out/sheet.png, out/card_*.png, out/*_roundtrip.png) and set sheets at D:/CastleConquest/art/forge/assets/_<set>_set_sheet.png. Builder summaries: ${JSON.stringify(built).slice(0, 12000)}
For EVERY asset: open its legendary card and its sheet with Read and LOOK. Score all 12 checklist items PASS/FAIL, each with one sentence of visual evidence. Judge tier readability (does each of Issued/Sound/Fine/Masterwork read in half a second?) and set coherence (does each lord's four-piece kit read as one kit?). Verdict SHIP or ITERATE; for ITERATE give at most 3 ranked, concrete fixes (the form/parameter, the new value, why). Never pass anything you have not seen.
Write the full review to D:/CastleConquest/art/forge/CRITIC_REPORT.md (a table: asset, verdict, score x/12, top fix; then per-set coherence notes; then the 5 most common failure patterns across the whole batch as proposed new numbered lessons). Return a concise summary: counts SHIP/ITERATE/other, the worst 5 assets with their top fix, and the common patterns.`,
  { label: 'art-critic', phase: 'Critique', effort: 'max' })

return { skill: skillOut, sets: built, critic }
