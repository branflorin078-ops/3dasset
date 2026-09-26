export const meta = {
  name: 'shop-gameplay-forge',
  description: 'Map shop/bundles and gameplay systems, author shop-forge + gameplay-forge skill drafts, verify them against the code',
  phases: [
    { title: 'Map', detail: '2 readers: monetization/shop, gameplay systems' },
    { title: 'Author', detail: '2 skill authors' },
    { title: 'Verify', detail: '1 verifier spot-checks every cited rule' },
  ],
}

const OWNER = `The game owner asked for this directly, in their own words: "add another team to make a skill for the bundles shop... high quality... and another skill for gameplay... create them very high level, add up to 5 Opus max." You are one of those agents. Repo: D:/CastleConquest (Godot 4.7 landscape-only mobile medieval castle-strategy game, a LIVE persistent realm; Windows; PowerShell 5.1 only — no &&, use ';'). Binding rules: D:/CastleConquest/CLAUDE.md (verify, never assume; server authority within ~50 EUR/month at 100k players; SACRED balance constants stay; no single-player conventions). Owner ledger: D:/CastleConquest/PROJECT_MASTER_MEMORY.md (read §99 CURRENT STATE, grep your topic), D:/CastleConquest/upgrade/TASK_BOARD.md, D:/CastleConquest/upgrade/MASTER_OVERHAUL_DIRECTIVE.md.`
const NOTES = {
  type: 'object',
  properties: { sections: { type: 'array', items: { type: 'object',
    properties: { title: { type: 'string' }, bullets: { type: 'array', items: { type: 'string' } } },
    required: ['title', 'bullets'] } } },
  required: ['sections'],
}
const J = x => JSON.stringify(x || {}).slice(0, 34000)

phase('Map')
const [shopMap, playMap] = await parallel([
  () => agent(`${OWNER}
READ-ONLY MAPPING — THE SHOP, BUNDLES AND MONETIZATION exactly as built. Read: godot/ui/mm_shop.gd (every tab, card, bundle layout, the published gem rate, the free-route line per bundle, limited-offer rules), godot/core/offers.gd and godot/core/iap.gd (catalogues, PRODUCTS ids, deliver(), provider seam), godot/data/items.gd (speed-ups, packs, boosts), godot/data/game_data.gd (grep FAIR_STALLS, CHESTS, bundle/offer tables, gem sinks/sources), godot/core/offers_test.gd and any shop-police tests (grep -l 'police' 'unsellable' 'never sold' in godot/core — list every guardrail and what it asserts), the VIP/subscription code (grep 'vip' 'subscription'), the shop art in use (godot/assets/shop, bundles, premium, vip — naming + sizes), and the owner rulings in PROJECT_MASTER_MEMORY.md: MON-001 (the free-viable gem map verdict), MON-002 (billing blocked), FEAT-002 (IAP catalogue), FEAT-003 (the Fair), the W6 shop overhaul notes (published gem rate, free-route line, limited offers that withhold nothing, the money law: war imagery never over a buy button — BND-siege/BND-warlord refused), the iap_play subscriptions-as-inapp bug on the TASK_BOARD, PEGI-7. Return exact ids, constants, prices, test names, rulings with ledger ids.`,
    { label: 'map:shop', phase: 'Map', schema: NOTES, effort: 'max' }),
  () => agent(`${OWNER}
READ-ONLY MAPPING — GAMEPLAY SYSTEMS exactly as built. Cover: the core loop (castle economy tick in godot/core/game_state.gd + economy code: TICK_SECONDS, production, storage, upkeep, offline catch-up), building/upgrade ladders (godot/data/game_data.gd, castle/town_plan.gd), troops (godot/data/troop_roster.gd: 5 lines x tiers, training), combat (godot/core/battle_engine.gd: the six phases, what is FROZEN, the balance corridor and its tests — grep 'corridor' 'SACRED' 'FROZEN' 'balance_test' 'attack_audit'), commanders (godot/data/commanders.gd: levels, signatures, clamp ledger, CMD_FX_CAP, chairs), equipment ladder (godot/data/equipment.gd), research (godot/data/research_data.gd size and branches), the world map / marches / AI lords (godot/world/world_map.gd, grep AI lords), events (6 families, weekly cadence), seasons, the Chronicle, alliances/the Muster, journeys and the Challenge Road, progression pacing (grep 'Curve' 'pacing' in PROJECT_MASTER_MEMORY.md; the W8 economy wave is queued). List every gameplay HARNESS in godot/core with what it gates (balance_test, attack_audit, playthrough_test, session_audit, economy_test, event_test, meta_test, ai_test, w2_probe, w4 probes, the QA agent tools/qa/agent.py) and the exact run commands from CLAUDE.md. List the SACRED constants and the resolver freeze rules with file:line. Return exact names, values, test names.`,
    { label: 'map:gameplay', phase: 'Map', schema: NOTES, effort: 'max' }),
])

phase('Author')
const STAGE = `FILE RULE: write the skill ONLY as a DRAFT in the staging folder named below — never into .claude/. The lead installs it into .claude/skills/ himself (the owner authorized that directly).`
const SHAPE = `Quality bar — read the installed house skills for structure and tone: D:/CastleConquest/.claude/skills/blender-forge/SKILL.md, D:/CastleConquest/.claude/skills/reference-forge/SKILL.md, D:/CastleConquest/.claude/skills/game-art-director/SKILL.md. A skill = SKILL.md (YAML frontmatter name + a precise triggering description; HARD RULES first; the workflow in order; a router to references) + focused reference files (60-160 lines each) + lessons.md seeded ONLY with real recorded traps (cite ledger ids). Every rule grounded in code: cite file paths and exact constant names/values from the map. Never invent a system; if something does not exist, say so and give the proposal shape.`
const [shopSkill, playSkill] = await parallel([
  () => agent(`${OWNER}
${STAGE} Staging folder: D:/CastleConquest/art/skills_draft/shop-forge/
Author SHOP-FORGE: professional design of the bundles shop, offers and monetization for THIS game — ethical, free-viable, and high-converting within the owner's laws.
${SHAPE}
Required: SKILL.md (hard rules FIRST: gems buy time and goods, NEVER power; equipment is structurally unsellable; every bundle states its free route truthfully; one published gem rate, no fake discounts or fake scarcity; limited offers withhold nothing and state their return; no war imagery over a buy button; PEGI-7; the shop police tests must stay green — each rule cites its test/ledger id); references/economy.md (the gem map: every source and sink with numbers, the published rate, MON-001's verdict, how to price a new bundle against it); references/bundles.md (bundle anatomy in the code's data shape: fields, badges, value statement, free-route line; the catalogue as it stands; how to design a new bundle end to end with a worked example); references/layout.md (the shop screen: tabs, card grid, featured card, pages, states — the MM components used; how bundle art is sized and where it installs); references/art.md (bundle key-art and shop-goods art: the painted route via game-art-director + tools/assets.json groups, the 3D-rendered goods route via blender-forge + reference-forge, the money-law imagery rules, naming SHP-/BND-/VIP-); references/billing.md (IAP catalogue, provider seam, deliver(), restore, MON-002 blocker, the subscriptions-as-inapp bug to fix before launch); references/qa.md (offers_test and every police test, iap_test, menu_test, the exact commands, what green looks like); references/lessons.md.
MAP — shop: ${J(shopMap)}
Return: file list with line counts + a 10-line summary of the laws as encoded.`,
    { label: 'author:shop-forge', phase: 'Author', effort: 'max' }),
  () => agent(`${OWNER}
${STAGE} Staging folder: D:/CastleConquest/art/skills_draft/gameplay-forge/
Author GAMEPLAY-FORGE: professional gameplay/systems design for THIS live realm — designing and changing mechanics without breaking the tuned game.
${SHAPE}
Required: SKILL.md (hard rules FIRST: SACRED balance constants never change without the owner; the combat resolver's frozen shape and the one-re-tune rule; every multiplier declares its clamp (the clamp ledger pattern); server-authority budget; no single-player conventions; free-viable economy; every change proven by the harness battery with pasted output — each cites file:line or ledger id); references/core-loop.md (economy tick, production/storage/upkeep, offline catch-up, pacing curves with numbers); references/combat.md (the six phases, what each reads, the fx keys, clamps, the corridor and how to test against it); references/progression.md (buildings, troops 5 lines, research, commanders, equipment ladder, seasons — the ladders with their numbers and where they live); references/live-systems.md (events 6 families + weekly cadence, the Chronicle, alliances/Muster, journeys, Challenge Road, AI lords — shapes and extension points); references/design-process.md (how to design a feature here: problem -> which system owns it -> data shape -> clamp -> harness -> ledger entry; a worked example from the ledger, e.g. FEAT-005 territory or the W2 commander system); references/qa.md (every gameplay harness: exact command, what it gates, green output; the QA agent); references/lessons.md (real traps from the ledger: e.g. KC-C ceremony into zero listeners, the negative-order exploit, lambdas capturing locals by value, the season never advancing).
MAP — gameplay: ${J(playMap)}
Return: file list with line counts + a 10-line summary of the laws as encoded.`,
    { label: 'author:gameplay-forge', phase: 'Author', effort: 'max' }),
])

phase('Verify')
const verdict = await agent(`${OWNER}
You are the VERIFIER (read-only except your report). Two skill drafts were written: D:/CastleConquest/art/skills_draft/shop-forge/ and D:/CastleConquest/art/skills_draft/gameplay-forge/. Adversarially verify them against the code: for EACH skill pick at least 20 checkable claims (constant names and values, file paths, test names and commands, ledger ids, prices, rules) and confirm each in the repo (Grep/Read). Also check: frontmatter valid; description would trigger on the right requests; hard rules actually match the owner's rulings; nothing invented presented as existing; references complete and actionable. Write D:/CastleConquest/art/skills_draft/VERIFY_shop_gameplay.md: per skill, a table of every checked claim (HOLDS / WRONG / INEXACT + evidence file:line) and a ranked defect list with exact fixes. Return: per skill counts HOLDS/WRONG/INEXACT and the top defects.
Author summaries: shop ${JSON.stringify(shopSkill).slice(0, 3000)} | gameplay ${JSON.stringify(playSkill).slice(0, 3000)}`,
  { label: 'verify', phase: 'Verify', effort: 'max' })

return { shopSkill, playSkill, verdict }
