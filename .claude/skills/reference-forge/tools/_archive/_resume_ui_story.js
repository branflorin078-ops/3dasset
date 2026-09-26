export const meta = {
  name: 'ui-story-forge',
  description: 'Map UI/events/alliance/story ground truth, author ui-forge + story-forge skill drafts, produce high-quality UI chrome, event/alliance art and story content, then critique',
  phases: [
    { title: 'Map', detail: '3 readers: UI system, event/alliance/menu screens, story canon' },
    { title: 'Make', detail: '2 skill authors + 3 asset makers in parallel' },
    { title: 'Critique', detail: 'critic scores renders and writing' },
  ],
}

const SK = 'D:/CastleConquest/.claude/skills/blender-forge'
const RUN = `py ${SK}/tools/forge_run.py run <script.py> <mode> <outdir> [extra]`
const OWNER = `The game owner asked for this directly, in their own words: "create another skill for event design, menu design, alliance, buttons... and another for story... make them very high quality... add up to 10 Opus max agents... the assets for those need to be very high quality." You are one of those agents. Repo: D:/CastleConquest (Godot 4.7 landscape-only mobile medieval castle-strategy game; Windows; PowerShell 5.1 only — no &&, use ';'). Project rules are in D:/CastleConquest/CLAUDE.md (binding: keep the painted identity; no title menus; real construction elements never boxes with stripes; verify never assume). Owner status docs: D:/CastleConquest/PROJECT_MASTER_MEMORY.md (read §99 CURRENT STATE and grep for your topic), D:/CastleConquest/upgrade/TASK_BOARD.md.`

const NOTES = {
  type: 'object',
  properties: {
    sections: {
      type: 'array',
      items: {
        type: 'object',
        properties: { title: { type: 'string' }, bullets: { type: 'array', items: { type: 'string' } } },
        required: ['title', 'bullets'],
      },
    },
  },
  required: ['sections'],
}

phase('Map')
const READERS = [
  { key: 'ui-system', prompt: `Map the game's UI DESIGN SYSTEM exactly as the code defines it. Read: godot/ui/mm_theme.gd (all palette/material constants with values, ink pairing and contrast rules, spacing scale SPACE_*, type roles and sizes, TOUCH/dp rules, SPLIT_* layout laws, any asserts), godot/ui/mm.gd (the component library: grep for 'static func' and read the button/list_row/refuse/card/chip/badge/section/tab/empty_state/error_state/skeleton builders — what variants exist, PRIMARY/SECONDARY/DESTRUCTIVE etc., states), godot/ui/mm_window.gd (window families panel/sheet/modal, head_art, plates, nine-slice chrome, inner_width), godot/ui/mm_decor.gd. Find how painted chrome is referenced: MMT.raw ids (grep 'CHR-' 'A-' 'I-' 'UI3D_ICONS' in mm_theme.gd), and list asset folders godot/assets/mm, godot/assets/chrome, godot/assets/premium, godot/assets/ui, godot/assets/ui3d (counts + naming patterns + typical pixel sizes via PowerShell [System.Drawing] or file sizes). Read the UI rulings/lessons in PROJECT_MASTER_MEMORY.md (UI-001..UI-007, A11Y-001, the nine-slice lesson in UI-002, the Button-min-width law in UI-004/GAME-001) and upgrade/MASTER_OVERHAUL_DIRECTIVE.md sections on UI (grep 'UI', 'button', 'landscape', 'ART SHOWN BIG'), upgrade/UI_REFERENCE_DECODES.md if present. List the UI QA harnesses in godot/core (contrast_test, layout_audit, a11y_audit, ux_touch_probe, w1f_aspect_sweep, mm_probe) with what each gates. Return exact names and values.` },
  { key: 'screens', prompt: `Map the EVENT, ALLIANCE and MENU screens as they exist. Read godot/ui/mm_registry.gd (every registered screen id -> file), then the event screens (godot/ui/mm_event_panel.gd, grep EventFamilies / events data in godot/data and godot/core), the alliance/retinue screens (godot/ui/mm_retinue.gd, godot/data/retinue.gd, the Muster), the Kingdom menu / drawer / spine nav (godot/ui/mm_kingdom.gd, hud.gd nav), and the shop (godot/ui/mm_shop.gd) as the reference of a recently rebuilt screen. For each screen: purpose, layout (columns, head art, tabs), components used, states (empty/loading/error/locked/claimable), which painted art it uses (paths), and weak spots recorded in upgrade/TASK_BOARD.md backlog / PROJECT_MASTER_MEMORY.md. Also read C:/Users/Famil/Downloads/EVENT_UI_REDESIGN.md, SCREENS.md, MOBILE_UI.md and ART_BRIEF.md (owner-supplied design docs; note where they conflict with the shipped code and CLAUDE.md — the code + CLAUDE.md win). Return exact paths, ids and counts.` },
  { key: 'story', prompt: `Map the game's STORY CANON and narrative systems. Read godot/data/chronicle.gd, the quest/act data (grep 'q_wood' 'ACT_BEATS' 'act_' 'say' 'done' in godot/data/game_data.gd and godot/core/game_state.gd), the story paintings folder godot/assets/story (list), the event families' flavour text (grep EventFamilies and event 'flavour'/'txt' fields), the commander voice lines (godot/data/attack_data.gd COMMANDERS 'note', godot/data/commanders.gd SIGNATURES 'line', OATHS 'txt'/'nm', BONDS), the equipment flavour 'line' fields (godot/data/equipment.gd), the Chronicle deed kinds (deed_add kinds in godot/core/game_state.gd), and the story notes in PROJECT_MASTER_MEMORY.md (STORY-001, STORY-002, STORY-003, W5 Chronicle) and upgrade/ docs (grep -l 'Chronicle' 'Act V' 'story'). Extract: the realm's geography and factions, the five acts (names, quests, beats, paintings), the lords (8) with their voices, the VOICE rules (quote 12+ verbatim lines that show the register), where each kind of text lives in data and its length limits, and open threads (what the canon leaves unanswered). Also check C:/Users/Famil/Downloads/THE_LEDGER_manga_bible.md and LIVING_KINGDOM_Blender_Prompt_v2.md only to say whether they belong to THIS game (the Living Kingdom side-production was REJECTED by the owner — parts quarry only). Return exact quotes and paths.` },
]
const maps = await parallel(READERS.map(r => () =>
  agent(`${OWNER}\nYOUR JOB (read-only mapping): ${r.prompt}`, { label: `map:${r.key}`, phase: 'Map', schema: NOTES, effort: 'max' })))
const [uiMap, screensMap, storyMap] = maps
const J = x => JSON.stringify(x || {}).slice(0, 30000)

phase('Make')
const RESUME_UI = `RESUME NOTICE (read first): your earlier run of this exact job was cut off by a usage limit on 2026-09-26. Part of your output is ALREADY ON DISK (your staging/output folder named below). List and inspect what exists first — open your newest renders — then CONTINUE: keep what is good, redo only what is weak, finish what is missing. Never rebuild finished pieces from scratch. The owner is paying for this run: be economical.\n\n`
const STAGE = `IMPORTANT FILE RULE: write your skill files ONLY as DRAFTS under the staging folder named below (NOT into .claude/). The lead will review and install them into .claude/skills/ himself — the owner authorized that install directly.`

const SKILL_SHAPE = `Skill quality bar — match the house skills already installed: read D:/CastleConquest/.claude/skills/blender-forge/SKILL.md and D:/CastleConquest/.claude/skills/game-art-director/SKILL.md for structure and tone. A skill = SKILL.md (YAML frontmatter with name + a triggering description; hard rules; the pipeline in order; a router to references) + focused reference files (60-160 lines each) + lessons.md seeded with REAL recorded traps from this project (cite the ledger ids). Every rule must be grounded in the code/maps below — cite file paths and exact constant names/values. No invented systems: if something doesn't exist in the game, say so and give the proposal shape, never pretend.`

const makers = [
  () => agent(`${OWNER}
${STAGE} Staging folder: D:/CastleConquest/art/skills_draft/ui-forge/
Author the UI-FORGE skill: professional UI/UX design and production for this game — EVENT screen design, MENU design (kingdom drawer, spine nav, windows), ALLIANCE screens (retinue, muster, asks), and BUTTONS/components (every variant and state).
${SKILL_SHAPE}
Required files: SKILL.md; references/design-system.md (every token from mm_theme.gd with value and use: materials, ink pairings, contrast laws, spacing, type roles, dp/touch); references/components.md (buttons PRIMARY/SECONDARY/DESTRUCTIVE + states normal/hover/pressed/disabled/refused-with-reason; list rows, cards, tabs/tab rail, chips, badges, section blocks, empty/loading/error states — exact MM builder names and options); references/screens-events.md, references/screens-alliance.md, references/screens-menus.md (the screen patterns: layout law, two-pane split, one-hand reach, what each screen must show, states, the weak spots and the upgrade recipe for each); references/assets.md (how UI art is produced and installed: painted route via game-art-director / tools/assets.json groups panels & buttons; 3D-rendered chrome route via blender-forge (transparent film, orthographic front camera, nine-slice corner design); sizes/densities; the ship-nine-slice-near-display-size law; naming CHR-/A-/I-/UI3D ids; install paths); references/qa.md (the harness gates: contrast_test, layout_audit at the aspects, a11y_audit, ux_touch_probe 48dp, w1f_aspect_sweep, mm_probe — exact commands from CLAUDE.md, what green looks like); references/lessons.md (UI-001..UI-007, A11Y-001, the nine-slice lesson, the Button-min-width law, and others from the maps).
MAPS — UI system: ${J(uiMap)}
MAPS — screens: ${J(screensMap)}
Return: the file list with line counts and a 10-line summary of the design system as you encoded it.`,
    { label: 'author:ui-forge', phase: 'Make', effort: 'max' }),

  () => agent(`${RESUME_UI}${OWNER}
${STAGE} Staging folder: D:/CastleConquest/art/skills_draft/story-forge/
Author the STORY-FORGE skill: professional narrative design and writing for this game — canon, the house VOICE, quest and act writing, event flavour and choice events, oaths/signatures/equipment lines, Chronicle deed lines, commander voices, and story art briefs.
${SKILL_SHAPE}
Required files: SKILL.md (hard rules: original only — never imitate any existing game/novel/show; the realm's canon wins; the house voice; mobile length limits; no text baked into images; L10N-friendly strings); references/canon.md (the realm, geography, factions, the eight lords with one-line identities and verbatim voice lines, the five acts with quests and beats, open threads); references/voice.md (the register as RULES with 15+ verbatim examples from the data and 10 do/don't pairs); references/structures.md (every text type: where it lives in code, its field names, exact length limits, how it renders — quests say/done, ACT_BEATS, events families, choice events, oaths, chronicle deed kinds and args, equipment lines, commander notes); references/recipes.md (step-by-step: writing a quest chain, an act, a choice event, a chronicle line, a lord's voice line; worked examples); references/art.md (story paintings via the painted pipeline: act paintings in godot/assets/story, the house style lock verbatim from tools/assets.json style.base, prompt recipe, key dependency); references/qa.md (continuity checks, voice checks, length checks, the no-IP rule, how to verify in game with the harnesses); references/lessons.md (STORY-001/002/003 and others).
MAP — story: ${J(storyMap)}
Return: the file list with line counts and a 10-line summary of canon + voice as encoded.`,
    { label: 'author:story-forge', phase: 'Make', effort: 'max' }),

  () => agent(`${RESUME_UI}${OWNER}
You are a senior UI technical artist. Produce a HIGH-QUALITY 3D-RENDERED UI CHROME SET for this game with the blender-forge skill (read ${SK}/SKILL.md, references/lessons.md, materials.md, lighting-render.md, forms.md; study ${SK}/examples/sunforged_greatsword.py and ${SK}/lib/forge.py). The game's material language (from mm_theme.gd): GILT #C9A04C (THE accent, lit #E0BC6A), OAK #4A2E1B, PARCHMENT #E8D9B5, IRON #3B4048, LEATHER #5C3A24, WAX #8A1F24 (urgency/destructive only). The UI is painted-medieval: carved oak, gilt, wax, iron, parchment — real construction elements (joinery, pins, rivets, bevels), never flat gradients.
DELIVER into D:/CastleConquest/art/ui_forge/chrome/ (one build.py per piece + out/):
1. BUTTON SET — PRIMARY (gilt-framed, warm field), SECONDARY (carved oak), DESTRUCTIVE (wax-red lacquer with iron), each in NORMAL / PRESSED (sunk 1-2 px, darker, tighter shadow) / DISABLED (desaturated, matte) — 9 renders.
2. PANEL FRAME — a carved-oak window frame with gilt corner caps, designed for NINE-SLICE: fixed ornamental corners, plain stretchable edges, flat centre.
3. TAB (normal + active) and a small round ICON SOCKET plate (the 'medallion' behind nav glyphs).
RENDER RULES: transparent film (scene.render.film_transparent = True, no backdrop), ORTHOGRAPHIC front camera, the studio_rig key upper-left; export PNGs at 2x density sized for nine-slice (e.g. button 384x128, frame 512x512, tab 256x96, socket 160x160) plus a labelled contact sheet D:/CastleConquest/art/ui_forge/chrome/sheet.png. Write NINE_SLICE.md with the exact corner margins (px) for every piece. Fit the maps below (sizes, nine-slice law, the existing chrome ids) — MAPS: ${J(uiMap)}
Launch Blender ONLY via the lock runner: ${RUN} (it serializes all Blender jobs machine-wide; 8 equipment builders are also using it — waiting is normal; PowerShell timeout 600000; never call blender.exe directly; never kill blender). You may NOT edit anything under ${SK}. Look at EVERY render with Read. Critique each against: reads at 1x on a phone, corners crisp, the material reads as the named material, text would sit legibly on the field (test by overlaying a text layer in a test render), nine-slice corners don't need to stretch. Max 5 loops per piece. Return: files, the nine-slice margins, and honest verdicts per piece.`,
    { label: 'make:ui-chrome', phase: 'Make', effort: 'max' }),

  () => agent(`${RESUME_UI}${OWNER}
You are a senior prop/UI technical artist. Produce HIGH-QUALITY 3D-rendered EVENT and ALLIANCE art for this game with the blender-forge skill (read ${SK}/SKILL.md, references/lessons.md, forms.md, materials.md, glow.md, lighting-render.md; study ${SK}/examples/sunforged_greatsword.py and ${SK}/lib/forge.py). Material language: GILT #C9A04C, OAK #4A2E1B, PARCHMENT #E8D9B5, IRON #3B4048, LEATHER #5C3A24, WAX #8A1F24. ORIGINAL designs only; real medieval construction.
DELIVER into D:/CastleConquest/art/ui_forge/event_alliance/ (build.py per piece + out/):
1. EVENT BANNER PLAQUE — a hanging carved board on iron brackets with a clear title field (the game sets the text), for the event screen header; wide aspect.
2. EVENT MILESTONE MARKERS — an unclaimed / claimable / claimed trio (e.g. iron token -> glowing gilt token -> stamped wax seal), readable at 64 px.
3. ALLIANCE CREST — a heater-shield blank (gilt rim, oak/leather body) plus THREE original heraldic charges as separate pieces (e.g. a tower, a crossed-keys-and-hammer, a sun-in-splendour — design your own, original), each composable on the blank; and a MUSTER BANNER badge.
RENDER RULES: transparent film (no backdrop), 3/4 or front as each piece suits, key upper-left; PNG at 2x density (banner 1024x384, markers 256x256, crest 512x512, charges 512x512); labelled contact sheet D:/CastleConquest/art/ui_forge/event_alliance/sheet.png. Fit the screen maps: ${J(screensMap)}
Launch Blender ONLY via the lock runner: ${RUN} (serialized machine-wide; other builders share it; PowerShell timeout 600000; never call blender.exe directly; never kill blender). You may NOT edit anything under ${SK}. Look at EVERY render with Read; critique against the 12-point list in ${SK}/references/qa.md plus: reads at 64 px, claimable vs claimed readable in half a second, no text in the art. Max 5 loops per piece. Return files and honest verdicts per piece.`,
    { label: 'make:event-alliance', phase: 'Make', effort: 'max' }),

  () => agent(`${OWNER}
You are the lead narrative designer. Using the story map below and the game's own data (verify every canon fact in the code before relying on it), write HIGH-QUALITY story content in the house voice, as DRAFTS for owner approval (do NOT edit any game file). Deliver into D:/CastleConquest/art/story_forge/:
1. CANON_BIBLE.md — the realm consolidated: geography, factions, the eight lords (identity, voice, relationships incl. the BONDS pairs), the five acts, the Chronicle, open threads — every fact cited to its file.
2. EVENT_CHAIN_DRAFT.md — one complete new choice-event chain (3 beats, each with a situation line, 2-3 choices with outcomes) written in the EXACT data shape the event system uses (quote the field names from the code), respecting length limits, no balance numbers changed — rewards named only from existing reward kinds.
3. CHRONICLE_LINES.md — 12 new deed/realm chronicle lines per existing deed kind shapes (args placeholders as the code uses them).
4. ACT_VI_OUTLINE.md — a proposal for the next act (3 quests with say/done lines in the data shape, the closing beat, which existing systems it gives a voice to, and a painting brief for its act painting written with the painted house style lock from tools/assets.json style.base verbatim).
5. LORD_VOICE_PASS.md — for each of the 8 lords: 3 new voice lines (hall greeting, oath sworn, defeat) in their established register.
Rules: original only (never imitate any existing game, novel or show); the house register (quote examples you match); short lines for mobile; no text inside images; no invented mechanics — if an idea needs a new system, label it PROPOSAL.
STORY MAP: ${J(storyMap)}
Return: the files with word counts and 6 sample lines you are proudest of.`,
    { label: 'make:story', phase: 'Make', effort: 'max' }),
]
const made = await parallel(makers)
const [uiSkill, storySkill, chrome, eventArt, story] = made

phase('Critique')
const critic = await agent(`${OWNER}
You are the exacting ART + NARRATIVE CRITIC (read-only except your two reports). Review:
A) UI renders: D:/CastleConquest/art/ui_forge/chrome/ (sheet.png, out/*.png, NINE_SLICE.md) and D:/CastleConquest/art/ui_forge/event_alliance/ (sheet.png, out/*.png). OPEN EVERY IMAGE with Read. Score each piece: material reads as named; construction is real (joinery/rivets/bevels, not flat gradients); reads at 1x/64 px; states distinguishable in half a second (normal/pressed/disabled; unclaimed/claimable/claimed); nine-slice corners sane; fits the game's painted-medieval language (compare with a shipped screen: D:/CastleConquest/shots/hero3d/hall_edwin_16x9.png); no text in art. Verdict SHIP/ITERATE with <=3 concrete fixes. Write D:/CastleConquest/art/ui_forge/CRITIC.md.
B) Story drafts in D:/CastleConquest/art/story_forge/: voice fidelity vs the verbatim house lines, continuity with canon (spot-check facts in godot/data), data-shape correctness, length limits, originality. Verdict per file with concrete fixes. Write D:/CastleConquest/art/story_forge/CRITIC.md.
C) The two skill drafts in D:/CastleConquest/art/skills_draft/ (ui-forge, story-forge): are rules grounded (spot-check 10 cited constants/paths each), complete, actionable? List defects.
Maker summaries: UI chrome ${JSON.stringify(chrome).slice(0, 4000)} | event/alliance ${JSON.stringify(eventArt).slice(0, 4000)} | story ${JSON.stringify(story).slice(0, 3000)}
Return a concise summary: per area SHIP/ITERATE counts, the top 5 fixes overall, skill-draft defects.`,
  { label: 'critic', phase: 'Critique', effort: 'max' })

return { uiSkill, storySkill, chrome, eventArt, story, critic }
