# Screens — a spec per major surface

Each spec gives: the one question the screen answers, its route and surface type, its entries,
the layout in design px (1080 × 1920; y measured from the sheet's or screen's top), the hero art
and its size, the footer, the states that matter, and the rules owned by other skills. Content
and data belong to the named skill. The frame, components and tap budget are ui-forge's. **All
sizes are PROPOSALS**; compare them with the shipped scene before changing anything.

Shared frame for every full screen: the title bar (72 px title, 120 high, y 0–120 of the safe
area), content, then the tab strip (112, if any), then the footer (144 + s5 padding). The footer
holds: back (opposite corner from the hand), Secondary, Primary (hand side). Sheets use the same
footer. Their title row is 96 high.

## S1 Building card — `building/{id}` · sheet 70% (1344 px) · depth 1

- **Answers**: "What is this building doing, and what do its next tier and its cost look like?"
- **Entries**: tap the building; the Build chip when a crew is idle (suggested building);
  its bubble; the next-goal card.
- **Layout**: 24 · title row 96 (name 60 px + tier tag "2 → 3") · 16 · **hero: the next-tier
  engine render, 768 px high = 40% of the screen** (`core/build_thumbs.gd`, castle-forge),
  with the current tier as a 200 px inset in its top-left corner · 16 · cost and time row 120
  (up to 3 cost lines side by side + the time) · 16 · "Requires: Keep tier 5 ✓" line 56 ·
  32 · footer 144. Total 1312.
- **Footer**: [Close] · [Work: "Train" / "Research" / "Produce" — Secondary, opens the
  function surface] · [Upgrade — Primary]. While it upgrades: Primary = "Speed up" (opens S18),
  plus the tag "Help asked ✓".
- **Tap the hero** → `building/{id}/tiers`: the 6-tier strip (6 renders of 160 × 200), current
  tier outlined. The silhouette change per tier is what the player is buying (blender-forge
  architecture.md §4).
- **Camera**: transition-forge frames the building in the top 30% while the sheet opens.
- **States**: locked (requirements unmet: the Requires line in WAX with a "Go" link); max tier
  (hero = the tier-6 render + "Crowned" seal; no Upgrade); no crew free ("All crews busy —
  first free 14:20", Primary disabled with that reason).

## S2 Research — `research/{desk}` · full screen · depth 1–2

- **Answers**: "What do I study next, and what does it give me?"
- **Layout**: title bar with a desk switcher when 2 desks exist (core-loop §2) · branch
  content: a vertical path of node cards 1032 × 200 (icon 128 Blender art · name 50 px ·
  effect "+8% wood output" 42 px · time and cost), done nodes collapsed into 120 px rows ·
  bottom tabs = branches (≤ 5) · footer [back] [Start — Primary].
- **Suggested node**: GILT_LIT outline + the "Suggested" tag, selected and scrolled into view
  when the screen opens from an idle desk (2 taps from HUD rest).
- **Rules**: a locked node shows its requirement; the effect line uses the same number the
  battle or economy code reads (one source of truth: data files, gameplay-forge).
- **States**: all done ("Every study at this desk is done — the next opens at Scriptorium
  tier 4"); desk busy (Start disabled, with the reason "Desk busy until 14:20"; there is no
  extra queue, because plate count is never sold or added, core-loop §2).

## S3 Muster yard — `muster/{line}` · sheet 92% (1766) · depth 1–2

- **Answers**: "Which troops, how many, until when?"
- **Layout**: 24 · title 96 · 16 · troop row 650: TRP card 520 × 650 (4:5 painting, units.md)
  + a stats column 496 wide (tier, attack/defence as numbers, "Strong vs" / "Weak vs" with line
  icons, upkeep per hour) · 16 · tier strip 132 (t1–t10/11 chips 120 × 120; locked tiers
  carry a padlock + requirement) · 16 · time-first presets 132: 1 h · 3 h · 8 h · "Until I'm
  back (hh:mm)" (core-loop A3) + a quantity picker link · 16 · result line 56 ("Ends 14:20 ·
  1,200 Pikemen · cost") · 16 · line tabs 112 (5 lines: silhouette + name) · 16 · footer 144
  [Close] [Muster — Primary]. Total 1488.
- **Money-law**: the gem finish of a running batch lives in its own footer row with hourglass
  art only, ≥ 48 px from the troop card. No troop, weapon or battle art on or behind it
  (core-loop §5 rule 5).
- **States**: short of resources (fill in the line priority; the missing resource named in one
  line, core-loop A2); yard busy (the running batch on top with its time and "Speed up").

## S4 Infirmary — `infirmary` · sheet 70% · depth 1–2

- **Answers**: "Who is wounded, how long to heal, is anyone about to die?"
- **Layout**: title 96 · beds bar 32 px ("840 / 1,200 beds", WAX warning bar with "Full in
  2 h" at ≥ 80%) · wounded by line: 5 rows of 144 (silhouette icon, line name, count, heal
  time) · cost and time row 120 · footer [Close] [Heal all — Primary]; a Premium "Finish now"
  with hourglass art on a separate row.
- **Rules**: the same money-law row rule as S3. The words say what dies at 100% (the combat.md
  loss model). Reports link here with "Heal".

## S5 Lords — `lords` roster, `lords/{id}/{tab}` detail · full screen · depth 1–3

- **Answers**: roster: "Who do I have, and who needs me?" Detail: "What makes this lord
  worth fielding, and what is the next step?"
- **Roster**: a 3-column grid of lord cards 320 × 400 (CMD portrait bust, name, role icon,
  level tag, sworn = gilt rim + gilt frame variant); a dot only when points or gear can be
  applied now. The ledger (onboarding.md §7) is a row at the grid's end: 2 taps from the hall.
- **Detail**: portrait 720 × 900 (47% of the height) at the top, with name and role over a 70%
  INK scrim band. It collapses to a 320 px header when the content scrolls (godot.md §6). Tabs
  (bottom): Overview · Skills · Talents · Gear · Pairing. Footer: [back] [the tab's batch action
  — "Equip best", "Spend on the suggested path", "Pair with…"].
- **Gear tab**: the 4-piece set as 4 item cards of 240 (rarity frame + studs), the 2- and
  4-piece bonus lines, missing pieces with "Where from" links (equipment.md sets; commander-forge
  owns the data).
- **Talents**: the recommended path for the lord's role is lit (onboarding.md FTM "Talents");
  points held / cap in the header.
- **Rule**: commander-forge owns portraits, hall figures and data. Portraits are never cropped
  above the chin or below the eyes' upper-third line (portraits.md).

## S6 Alliance — `alliance`, `alliance/{section}` · full screen · depth 1–2

- **Answers**: "What does my alliance need from me now, and what is it giving me?"
- **Home**: banner header 400 high (alliance sigil ALS, name, member count, the player's rank
  badge RNK: shape AND word) · quick row: Help all · Claim gifts (only while they apply) ·
  section grid 2 × 4 tiles of 492 × 200 (art + name + count or dot): Help · Gifts · Members ·
  Charters · Territory · Rallies · Pacts · the Roll.
- **No alliance**: 3 recommended alliance cards (880 × 320: sigil, name, language, members,
  activity at the player's hours) + the join purse line (onboarding.md §5) + Join (Primary),
  "Create" (Secondary), "Later" (back).
- **Members**: a virtual list; rows 144: crest, name, rank badge, last-active bucket
  (alliance.md §2 privacy); officers see exact hours.
- **Rallies**: rows 200: target art, leader, join countdown, banners filled "3 / 5", Join
  (battle-forge flow). The calendar strip of muster hours (alliance.md §8) at the top.
- **Rules**: the server enforces permissions; the client hides buttons the rank cannot use
  (alliance.md §2.1). Badges are Blender art with a word, ≥ 48 dp when tappable.

## S7 Events — `events/board` (the Herald's Board), `events/{id}` · full screen

- **Board — answers**: "What is coming in the next 3 weeks, and what does each ask of me?"
  Rows of 200 per event: type icon (Blender art) · name 50 px · tags as shaped chips (PvE ·
  PvP · alliance · loss-free · story) · start and end in local time with the UTC offset ·
  "what counts" in ≤ 12 words · "Top reward: about 3 visits a day" (liveops §6.1). Grouped by
  week, with a "Today" marker. Freeze notices appear as pinned rows in WAX with a seal.
- **Event — answers**: "How do I score, and what have I earned?" Header art 1080 × 620
  (32% of the screen area; a painted board from game-art-director, no text in the art) · the
  time left in days and hours · the milestone ladder as rows of 144 (threshold, reward cards
  128, Claim) · "How to score" rows, each a route link · rules ≤ 5 lines.
- **Rules**: no offer inside an event screen that sells what the event scores (liveops R5);
  claims follow the mail-forge claim protocol when the event has ended.

## S8 Shop frame — `shop`, `shop/{shelf}`, `offer/{id}` · full screen · depth 1–2

- **Answers**: "What can I buy, for how much, and what exactly do I get?"
- **Layout**: shelves as bottom tabs (≤ 5: the Fair · Purses · Chronicle · Gems · Looks —
  names from shop-forge); goods cards in 2 columns, 500 × 640, with the goods render ≥ 50% of
  the card; price button = the store's localized price (never a literal "€" in data); gem
  prices with "≈ €x.xx".
- **Offer card** (`offer/{id}`, also used as the pop-up): 960 wide, goods art ≥ 50%, contents
  as rows, the window in days and hours, the return line, **Close and Buy the same height**,
  Close visible from the first frame.
- **Rules** (monetization.md §5, §10): no war imagery anywhere on these surfaces; no dots; no
  pulsing; the store sheet is the confirm; the pop-up slot follows the pop-up rules. Personal
  budget: a link to Settings → Spending. States: purchase pending, failed, restored
  (states.md §5).

## S9 Bag — `bag`, `bag/{kind}` · full screen · depth 2

- **Answers**: "What do I hold, and what is it worth in minutes and resources?"
- **Layout**: the honest-inventory line on top: "Held: Works 38 h · Muster 12 h · Universal
  6 h — Queued work: 51 h" (core-loop §5.3) · a grid of item cards 160 with count tags · tabs:
  Hourglasses · Resources · Lord items · Chests · Other · item tap → 40% picker (art 256,
  description, Use / Use n).
- **Rule**: opening chests happens here or in the Chronicle, never in the shop.

## S10 Profile — `profile/{id}` · full screen · depth 1

- **Answers**: "Who is this lord of the realm, and what can I do with them?"
- **Layout**: their keep as seen on the realm map (engine render) 1080 × 640, crest, name,
  alliance tag, titles · power with the tooltip "Power is a guide; counters and lords decide
  battles" (numbers.md §3) · stats rows · actions for others: Message (chat-forge), Show on
  map, Block, Report (chat-forge safety) · own profile: change crest, name rules.
- **Rule**: no attack button on a profile. War actions start on the map (battle-forge).

## S11 Rankings — `rankings/{board}` · full screen · depth 2

- **Answers**: "Where do I stand, and who is near me?"
- **Layout**: board tabs · rows of 144 (rank 50 px digits, crest, name, alliance tag, score),
  the top 3 as rows of 200 · **own row pinned** above the tab strip · "Updated 12 min ago"
  (liveops snapshots every 15 min) · virtual list, pages of 50.
- **Rule**: pull-to-refresh at most once per 30 s (server cost; the snapshot cannot change
  faster anyway).

## S12 Settings — `settings/{section}` · full screen · depth 2–3

Sections (rows of 144 with toggles and pickers): **Account** · **Notifications** (push types,
quiet hours 22:00–08:00 by default, core-loop A8; marks per hud.md §5) · **Accessibility** (text
size 100/115/130%, reduced motion, no screen flashes, haptics, extra shape markers, subtitles)
· **Controls** (Hand: Right/Left; camera sensitivity) · **Audio** · **Language** ·
**Graphics** (quality, 30/60 fps) · **Spending** (personal monthly limit, monetization.md §5.6)
· **Privacy and data** (export, delete: cloud-forge) · **Help** · **About** (version,
licences). Every change applies at once. No "Save" button.

## S13 Chronicle — `chronicle`, `chronicle/{track}` · sheet 92% · depth 1

- **Answers**: "What is left today, this week and this season?"
- **Layout**: daily orders as rows of 120 (points, done seal) · the 30 / 60 / 100 chests as
  3 chest icons of 160 + "Open all" (core-loop §7) · weekly writ bar with 200 / 350 / 500
  marks · season track: a horizontal strip of reward cards, the free track above, the paid
  chronicle track below (monetization.md §7, no war imagery) · the 7-step return streak ·
  reset countdown in local time, with "(00:00 UTC)".

## S14 Realm overlay and the tile sheet — `realm/tile/{x}/{y}` · sheet 40%

- **Answers**: "What is this place, how far, and what can I do to it?"
- **Layout**: tile art 240 (camp, castle, node, ruin) · name, level, owner with its
  relationship marker (shape + colour, world-forge) · distance and march time · action row of
  ≤ 4 (Scout · Attack or "Hunt the nearest 5" · Gather · Rally), a More button for the rest.
- **War screen**: no buy button, gem button or offer here (monetization.md §10).
- Realm tools (hud.md §4): Search (coordinates, player, alliance; last 5), Bookmarks (a
  virtual list), Home.

## S15 March composer — battle-forge's flow on this kit · sheet 92%

- **Layout**: lord slots (primary 320 × 400 card + secondary 240; pairing rule from lords.md)
  · 5 line rows (silhouette, available count, slider, number) · presets A/B/C as a
  segmented control · capacity bar · ETA · a power estimate with counter hints as line icons
  ("+counter vs their cavalry") · footer [back] [Send — Primary].
- **Rules**: a war screen (no money); "Send" stays the same size and place in every march type
  so muscle memory works in a war window.

## S16 Guide overlay, pointer, cards and the ledger (onboarding-forge's content)

- **Overlay**: CanvasLayer 50 (godot.md §2). In forced steps, a full-screen INK 60% dim whose
  `_has_point()` returns false inside the hole, so only the one allowed tap passes to the
  button or the 3D pick below (onboarding.md §2). From step 3 on, no dim.
- **Pointer**: a gilt gauntlet (Blender art) 120 px. It is the ONE looping animation in the
  UI (a 1.2 s press loop); with reduced motion it is static.
- **Cards**: 880 wide, ≤ 14 words at 42 px, ≤ 3 per step. Never over the hole (≥ 48 px gap).
  Skippable after 3 s. "Guide: full / brief" toggle.
- **The ledger**: rows of 200, one per lesson, each opening a 20–40 s replay card.

## S17 Resource sheet — `resource/{id}` · sheet 70%

- **Answers**: "How much do I have, how much is safe, and where do I get more?"
- **Layout**: amount, protected amount (warehouse), production per hour · sources as rows,
  free sources first (buildings, gathering, camps, orders, alliance), each with a Go link · the
  shop row last, with no art louder than the others.

## S18 Speed-up picker — sheet 40% (picker)

- **Answers**: "When will it end if I use this?"
- **Layout**: **the new end time first** (60 px) · hourglass options by kind (Works · Muster ·
  Universal) with counts, the best fit selected · the change given back ("Returns 15 m + 5 m
  + 1 m + 1 m", core-loop §5.4) · Use (Primary) · a gem finish (Premium, two-step, price
  `p(minutes)`, hourglass art only).

## S19 Chat, mail, reports — shells only

chat-forge, mail-forge and report-forge own their layouts, data and rules. ui-forge supplies the
full-screen frame, the list and card kit, the ticker slot (H9), the mail slot (H4), share cards,
route strings and the empty, loading and error states. A layout in those skills that breaks a
rule here (tap targets, contrast, marks) is reported to that skill, not patched here.

## Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| The building render is < 40% of the height | the upgrade looks like a number, not a building | [ ] screenshot measure on S1 |
| A gem finish sits on the troop card | money-law breach on a military surface | [ ] monetization.md §10 scan in `ux_flow_probe` |
| Buy is taller than Close, or Close appears late | dark pattern | [ ] `ux_touch_probe` rect compare on S8 |
| The own row is not pinned in rankings | the player scrolls 400 rows to find themselves | [ ] review |
| A war screen shows an offer | money-law | [ ] scan of S14/S15 captures |
| A guide card covers its own hole | the step cannot be done | [ ] `ftue_probe` dead-end log |

- [ ] The screen answers ONE question, written at the top of its spec.
- [ ] Route, surface type and depth match architecture.md; the footer has back + Primary.
- [ ] Hero art at its size; list rows carry art ≥ 96 px.
- [ ] Tabs above the footer; ≤ 5.
- [ ] The rules of the owning skills (money-law, alliance permissions, liveops limits) applied.
- [ ] Every state in states.md present, with its screenshot.
