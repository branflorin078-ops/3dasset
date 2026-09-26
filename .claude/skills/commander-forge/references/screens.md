# Screens — the lords' screens, specified for ui-forge

ui-forge builds every screen and owns the HUD zones, components, spacing,
type and motion rules; where its numbers differ from the proposals below,
ui-forge wins. This file says what the LORD screens must contain, in which
states, at what tap cost, and how they keep the lord shown big. Numbers from
lords.md (levels, skills, talents, set bonuses, pity) are shown, never
invented here.

## 1. Screen map and tap budget

Entry points: the Hall (a castle building), the HUD lord button, and any
lord chip (march tracker, report, chat share card, alliance feed).

| Screen | Reached from | Holds |
|---|---|---|
| Hall | castle, HUD | the 3D stage with ONE lord big on the plinth + a chip strip of all lords |
| Roster list | Hall (toggle) | cards filterable by owned / line / role |
| Lord detail | Hall, any chip | tabs: Overview · Skills · Talents · Kit (· Oath/Bonds if the shipped OATHS/BONDS surface) |
| Pairing | march screen, lord detail | primary + secondary, presets |
| Ceremonies | events | acquire, sworn, level-up, set complete |
| Rework notice | mail | what changed, the refund |

| Core action | Max taps (PROPOSAL) |
|---|---|
| Castle → any lord detail | 2 |
| Any lord chip → that lord | 1 |
| Equip a piece | 3 (Kit tab → slot → piece) |
| Level a skill | 3 (Skills tab → skill → confirm) |
| Spend a talent point | 2 per point; batch mode: 1 per point + 1 confirm |
| Set a pair preset | 3 (the last preset is kept, core-loop.md) |

## 2. Hall — the lords in person

- The 3D stage (hero3d's `mm_hero_stage.gd`, feel-forge's living light)
  shows the selected lord on the plinth, figure ≥ 55% of screen height.
- The chip strip at the bottom: all lords at 112–128 px, swipe or tap to
  switch; switching cross-fades the stage ≤ 250 ms (the next lord's GLB
  preloaded while the chip is held).
- Unowned lords stand on the stage as a dark silhouette (the lineup
  silhouette) with "Earn at: …" and the free path length from lords.md —
  never hidden, never greyed-out portraits.
- The plinth ring: dark unsworn, warm gold sworn (kit-sets.md §2).

## 3. Lord detail — zones on 1080 × 1920 (PROPOSAL)

| Zone | Height | Content |
|---|---|---|
| Top bar | 0–6% | back, name + epithet, the lord's currency (XP, duplicate currency) |
| Art | 6–58% (≈ 1000 px) | the figure on the plinth (fallback: the CMF painting at the same framing) |
| Name plate (over the art foot) | — | role icon, line icon, level ring, rarity frame (if lords.md uses rarity) |
| Tabs | 58–63% | 4–5 tabs, targets ≥ 48 dp |
| Tab content | 63–92% | per tab (§4) |
| Action bar | 92–100% | the primary action at the right thumb |

Rules: the lord never leaves his own screen — on every tab the art zone
keeps ≥ 45% of the height (SKILL rule 4). On the Kit tab tapping a slot
moves the stage camera to that part (helm → head close-up) in ≤ 400 ms
(transition-forge easing); leaving the tab returns it.

## 4. Tab contents

| Tab | Must show | States |
|---|---|---|
| Overview | role in one sentence, lead line, level + XP bar with the next level's number, the sworn state and what it does in one line, duplicate currency with the pity counter "N of M" | owned · sworn · max |
| Skills | per skill: SKL emblem 96 px, name, level pips, active/passive, meter cost as a number, "next level: …" from lords.md; tapping plays the skill moment on the stage (≤ 1.2 s, skippable) | locked · learnable · levelled · max |
| Talents | the whole tree on one screen, no panning at 1080 wide (≤ 3 branches, nodes 88–104 px); points left; reset cost; one recommended preset per role | node: locked · available · taken |
| Kit | four slots around the figure (weapon, armour, helm, token), each with its tier frame (Issued · Sound · Fine · Masterwork); set counter 0/4 → 4/4 with the set bonus text from lords.md | slot: empty (outline + where to get) · equipped · upgradeable (an arrow, not a red dot) · locked |
| Pairing | primary slot 60% width, secondary 40%; the rule in one line; what APPLIES lit (primary talents and gear), the secondary's greyed with the words "applies only as primary"; 3 preset slots (PROPOSAL) | preset: empty · saved · in use |

## 5. Card and chip states

| State | Card (256 × 320) | Chip (128 / 64 / 44) |
|---|---|---|
| Unowned | lineup silhouette on the card ground, "Earn at: …", free path length | silhouette, no ring |
| Owned | CMD crop, name, level | face crop, level ring |
| Sworn | + inner gilt edge 2–3 px `#E0BC6A` | + gilt ring |
| In march | + banner mark and ETA | + banner mark |
| Max | + laurel mark | + laurel |
| New | one "new" badge, gone after the first view (ux.md red-dot budget) | badge |

Lord rarity (if any) is the card FRAME material; the sworn state is the
inner gilt edge; they never swap (design.md §4).

## 6. Ceremonies and notices (feel-forge owns motion)

| Moment | Content | Length (PROPOSAL) |
|---|---|---|
| Acquire (first time) | stage lights come up, the lord steps onto the plinth (hero3d clip), `hall_greeting` line | ≤ 4 s, once per lord |
| Sworn | rim 0 → full in 600 ms, plinth ring warms, `oath_sworn` line | ≤ 2 s |
| Level up | numeral rolls and lands | ≤ 800 ms |
| Set complete | motif lights across the four pieces | 4 × 120 ms |
| Rework | a letter: what changed, why, the refund (mail-forge) | no ceremony |

All skippable after 300 ms; with `UI.reduced_motion` every one becomes a
≤ 200 ms cross-fade. Several ceremonies queue, never stack (one-popup law,
feel-forge).

## 7. Money-law on lord surfaces

- No battle imagery on or next to a buy button; skill-moment previews
  never appear on paid surfaces.
- Whatever monetization.md allows to be sold for lords, the card shows the
  free path length beside the paid one ("free: ≈ N days by camps and
  events").
- The pity counter is visible on the lord detail at all times, with its
  published math one tap away.

## 8. Empty, loading and error states

| Case | Shown |
|---|---|
| Figure GLB still loading | the CMF painting (or CMD) at the same framing, cross-fade ≤ 250 ms when the figure is ready; never a spinner in the art zone |
| Figure missing for a lord (`art_status` missing) | the CMF painting; a stand-in render only if tagged `stand_in` |
| Equip refused by the server | optimistic swap reverted with a toast naming the reason (cloud-forge) |
| No skills learnable | the next unlock and its level, never an empty list |
| Talent reset unaffordable | the cost and the shortfall |

## 9. Text

Names ≤ 18 characters, epithets ≤ 32, all through l10n keys with +35%
room; no text in any art (portraits, emblems, sigils).

## 10. Harnesses

`menu_test`, `layout_audit`, `ux_flow_probe` (the §1 tap counts),
`ux_touch_probe` (≥ 48 dp), `a11y_audit`, `contrast_test`,
`w1f_aspect_sweep` (must print `ASPECT SWEEP OK - 6 shapes, 0 faults`).
Proposed for qa-forge: `lord_screen_probe` — opens every tab of every lord
in every state (§4, §5), asserts the art zone ≥ 45% of the height on each,
counts taps for the six core actions, and screenshots the Hall per lord for
the lineup and look-dev checks.

## 11. Failure modes

| Failure | Looks like | Cause | Fix |
|---|---|---|---|
| Spreadsheet lord | a stats page with a thumbnail | art zone given to tables | §3 zones; art ≥ 45% on every tab |
| Hidden rule | players field a secondary for its talents | "primary only" not shown | Pairing tab greys what does not apply, in words |
| Red-dot rash | every lord badged daily | badges for "could upgrade" | arrows for upgradeable, one "new" badge only |
| Spinner hall | a loader where the lord should be | GLB loaded on open | painting fallback + preload on chip hold |
| Tree maze | talents need panning | too many nodes | ≤ 3 branches, whole tree on one screen |

## 12. Checklist

- [ ] Tap budget §1 measured by `ux_flow_probe`
- [ ] Art zone ≥ 45% on every tab, every aspect (`w1f_aspect_sweep`)
- [ ] Every state of §4 and §5 rendered for every lord
- [ ] Ceremonies skippable, reduced-motion variants present
- [ ] Money-law checks on every lord surface that sells anything
- [ ] Fallbacks of §8 shown in screenshots
