# UI — the Letters screen, the letter, the claim, the compose sheet

**ui-forge builds** these screens with its kit (Theme, rows, tabs, footer slots, states, router).
This file is the content spec: what each surface shows, in which order, with which numbers.
ui-forge's numbers win where they differ. Report a clash to ui-forge rather than patching around
it (ui-forge screens.md S19). Canvas: 1080 × 1920 portrait, right hand; the Hand setting mirrors
everything. Numbers are **PROPOSALS** within ui-forge's rules: touch ≥ 132 px, primary 144 px;
type 32 digits / 36 sentence minimum / 42 body / 50 labels / 60 titles / 72 screen; spacing
4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.

## 1. Entry points and the tap budget

| From | To | Taps | ui-forge core action |
|---|---|---|---|
| HUD slot H4 (x 920, y 148, 144 × 144, icon 96) | Letters, full screen, route `mail/{tab}` | 1 | — |
| Letters → footer **Claim all · n** | every claimable reward | **2** | #16 "Claim all mail rewards: 2" |
| Letters → a row | the letter (route `mail/{tab}/{id}`, full screen, depth 2) | 2 | — |
| A row's **Claim** action | that letter's rewards, without opening it | 2 | — |
| Report toast, or Letters → Reports → row | report-forge's layout (`report/{id}`) | 1–2 | #15 "Read the last battle report: 1–2" |
| Letter → **Reply** → type → Send | a letter back | 3 + typing | — |
| Player profile card → **Write** → type → Send | a new letter | 2 + typing | — |
| Alliance screen → Mail → template → fill → Send | alliance-wide mail (Liege, Herald office) | 5 | not a core action |
| A share card in chat ("a report", "coordinates") | its route | 1 | chat-forge |

The screen opens on the tab that holds the newest unviewed item among Rewards, Personal and
Alliance, else the last tab used this session (ui-forge tabs rule), else Rewards.

## 2. The Letters screen (full screen, 1080 × 1920)

| Band | y (safe area top = 0) | Content |
|---|---|---|
| Title bar | 0–144 | "Letters" 72 px; the ⋯ menu (Select, Mark all read, Delete read, Settings) 132 × 132 on the hand side; search 132 × 132 beside it |
| Filter chips | 160–256 (hit 132) | ≤ 4 chips: Unread · Rewards to claim · Kept · From my alliance — 96 high, 36 px words |
| List | 272–1560 | rows of 144 px (§3): 8.9 rows visible; a virtual list above 60 rows (ui-forge godot.md §10) |
| Tab strip | 1576–1688 | 5 tabs × 216 px, 112 high (ui-forge: tabs above the footer, the easy zone) |
| Footer | 1704–1848 | Primary **Claim all · n** 440 × 144 on the hand side, shown only when n ≥ 1; Secondary on its inner side: **Write** on Personal, **Mark all read** elsewhere; back control in the opposite corner |

Tabs: icon 64 px (Blender-made) + label 42 px, fit-down to 36 px; below that, icon only, with the
word on long-press. Each tab shows its unviewed count as a pill (32 px digits, WAX with a
PARCHMENT ring, "99+" cap). A tab with a claimable reward carries the dot. No swiping between tabs.

## 3. Row anatomy (ui-forge "Standard" row, 144 px)

```
| 24 | seal 96 | 16 | line 1: subject, 42 px (bold when unviewed), 1 line, ellipsis        | 16 | action | 24 |
|    |         |    | line 2: sender · time · tag, 36 px OAK                                 |    | 220×132|    |
```

| Part | Rule |
|---|---|
| Seal (96 px, Blender-made art) | unviewed = **intact** wax seal; viewed = **broken** seal. Shape carries the state, never colour alone. The Chancery seal, an alliance sigil (ALS) or a player's crest identifies the sender |
| Subject | template subject in the reader's language (≤ 32 characters English), or a letter's first 40 characters |
| Line 2 | sender name · relative time ("3 h", "2 d"; the local date-time on long-press) · one tag at most: "Kept", "Request · removed in 2 d", "Claimed", "Claimed for you" |
| Action (one, hand side) | Rewards: **Claim** with the first item's icon 64 px and "+n" for more lines · Requests: **Accept** · Reports: none (the row opens) · others: none |
| Tap on the rest of the row | opens the letter (a report row opens report-forge's layout) |
| No swipe actions | ui-forge rule: hidden gestures fail discoverability. Select comes from the ⋯ menu; long-press 500 ms is only a shortcut |

Icons needed from blender-forge via ui-forge icons.md (44 px survival check): seal intact, seal
broken, the Chancery seal, 5 tab icons, Claim-all, Kept ribbon, Request, and one empty-state
still life per tab (§8).

## 4. The letter view (full screen, depth 2)

| Band | Content |
|---|---|
| Header | painted header 1080 × 432 ([templates.md](templates.md) §6), or none for players' letters and reports |
| Panel | parchment panel overlapping the header by 48 px; subject 60 px, ≤ 2 lines; meta 36 px OAK: sender, local date-time, "Kept" |
| Body | 42 px INK on PARCHMENT (12.66 : 1), line height 1.3, measure ≤ 960 px; player text with BBCode off; ≤ 1 share card (chat-forge, 800 × 248) |
| Goods | tiles 200 × 200 (icon 128, count in 32 px digits), 4 per row, 24 px gaps; each tile's name on tap; a claimed letter shows a "Claimed 14 Oct" line under the tiles |
| Footer | Primary 440 × 144 on the hand side: **Claim** (Rewards, unclaimed) / **Reply** (Personal) / **Accept** (Request) / none; Secondary: **Keep**; ⋯ (Delete, Report, Share, Block) 132 × 132; back control in the opposite corner |

Delete on a letter with unclaimed goods is replaced by **Claim & delete** (one tap does both;
[categories.md](categories.md) §3). Report and Block are ≤ 2 taps from any player letter
(chat-forge safety.md §8).

## 5. The claim — button states and timings

The claim is never optimistic (ui-forge states.md §4 rule 3). The server's answer decides.

| Moment | Row action / footer Primary shows | Input |
|---|---|---|
| 0 ms (tap) | Busy: the label dims, a ring starts only after 150 ms | a second tap does nothing |
| usually < 300 ms | result arrives → the ceremony (below) → the row turns "Claimed", its badge share clears | free |
| 3 s | "Waiting for the courier…" under the button (ui-forge wording) | free |
| 10 s without answer | the client reads the letters (idempotent read) and shows the true state; if unclaimed, the button returns | free |
| refused | a toast with the reason ("Claimed on another device — added to your stores" counts as success; "This reward was withdrawn"; "The claim window has closed") | free |

**Ceremony** (feel-forge owns it): the goods fly from the tiles or the row to the bag and resource
strip, with a count-up. It takes ≤ 1.5 s (90 frames at 60 fps) and can be skipped after 300 ms
(core-loop A9). A claim-all merges into ONE ceremony ≤ 2.5 s and one summary: "Claimed from 7
letters · 1 withdrawn". Audio: the reward burst with its duck (audio-forge). Never a wheel, reel,
card flip or any gambling look (monetization.md §9, PEGI-7). Auto-claims have no ceremony, only
the digest line "The Chancery claimed 3 rewards for you" (core-loop §8.1 digest, ≤ 3 lines).

## 6. Compose

**Letter** (sheet at 92% = 1766 px; ui-forge sheet heights):

| Part | Rule |
|---|---|
| To | a recipient chip (from the profile, a reply, or a picker of alliance mates and contacts); diplomacy targets for a Liege or Marshal |
| Text | a text field of 42 px, grows to 8 lines; counter "123 / 500"; the field stays ≥ 48 px above the keyboard (`DisplayServer.virtual_keyboard_get_height()`) |
| Share card | + Card: ≤ 1 (a report, coordinates, a lord) from chat-forge's card set |
| Send | Primary 440 × 144; disabled with a reason when the server would refuse (T0, the recipient's setting, the day's limit): "Aldric accepts letters from his alliance only" |
| Held | if the server holds it (duplicate text), the sent letter shows "Waiting for review" (chat-forge safety.md §12) |

**Alliance-wide mail** (Alliance screen, Liege and Herald office only): a template picker (sheet
40%) with the six officer templates ([templates.md](templates.md) §2.3) and "Free text". Args use
pickers, never typed values: a map point picker for `coords`, a local-time wheel that stores unix
time, a member picker. A preview renders the letter as a member in another time zone would see
it. The counter shows "2 of 3 today".

## 7. Search, filters, select

- **Search** (ui-forge: a text field + the last 5 searches) runs **on the phone** over cached letters:
  rendered subject, sender name, letter text, in the reader's language. Server cost 0. ≤ 50 ms for
  600 cached items.
- **Filters**: the 4 chips in §2 combine with the tab ("Personal + Unread").
- **Select**: from ⋯ → Select (or long-press). Rows show check boxes of 132 px hit. The bulk actions
  in the footer are Mark read, Keep, Delete. Delete skips unclaimed rewards and Kept letters, and the
  result line counts what was skipped, offering "Claim & delete the 3 with rewards".

## 8. States (ui-forge states.md patterns; mail's copy and objects)

| State | Letters screen | Copy key (English) |
|---|---|---|
| LOADING | the cache shows at once; with no cache: nothing for 150 ms, then 8 skeleton rows of 144 px | "Waiting for the courier…" at 3 s |
| EMPTY · Notices | still life: a rolled notice under an unbroken seal | "No notices. The Chancery writes when the realm has news." |
| EMPTY · Rewards | an open tally chest, empty | "No rewards waiting. Event rewards arrive within an hour of an event's end." |
| EMPTY · Alliance | a bare pin board | in an alliance: "No orders from the Hall." · without one: "Join an alliance to receive its letters." + Find an alliance |
| EMPTY · Personal | a quill in a dry inkwell | "No letters yet. Write to an ally from their profile." |
| EMPTY · Reports | a war-table marker box, closed | "No reports. They arrive after battles, scouting and hunts." |
| ERROR | the cache with a line; small code | "The courier did not come back. Your letters are safe." + Retry |
| OFFLINE | the cache, marked "Saved 14:20"; Claim, Send, Delete disabled | "Needs the realm road" |
| A letter that cannot render (old client) | the tab's generic subject | "Update the game to read this letter." + Update |

Empty-state objects are Blender-made still lifes of 256–320 px (ui-forge icons.md), one per tab.

## 9. Motion

| Motion | ms | Frames | Curve | Owner |
|---|---|---|---|---|
| Letters opens (`full_in`) | 260 | 16 | ease-out quart | ui-forge motion.md |
| Letters closes (`full_out`) | 200 | 12 | ease-in cubic | ui-forge |
| Rows appear (`stagger`) | ≤ 400 total, first 8 rows | ≤ 24 | ease-out quart | ui-forge |
| Letter view replaces the list | as `full_in` / `full_out` | — | — | ui-forge |
| Seal breaks when a letter opens | 180 | 11 | ease-out cubic | feel-forge (off in reduced motion: an instant swap) |
| Claim ceremony | ≤ 1,500 (≤ 2,500 merged) | ≤ 90 (≤ 150) | feel-forge | feel-forge |

No motion blocks input for more than 300 ms (core-loop A9), and every motion honours reduced motion.

## 10. Accessibility and language

- Unviewed = intact seal + bold. Claimable = the word **Claim** + an item icon. Kept = a ribbon + the
  word. Nothing relies on colour alone (`a11y_audit`).
- Contrast on parchment: INK 12.66 : 1 (text), OAK 8.85 : 1 (meta), WAX 6.53 : 1 (badges, danger).
  **GILT is never a text colour on PARCHMENT (1.74 : 1)**. It is used for outlines, focus and the
  Primary plate only.
- Pseudo-locale +40%: row subjects may ellipsize; the letter view title wraps to 2 lines, and tabs
  fit down, then show the icon only. Buttons never clip (UI-004).
- Times: local time everywhere; the UTC offset on long-press; officer templates show the reader's
  local time ([templates.md](templates.md) §2.3).

## 11. Godot implementation notes (ui-forge and cloud-forge own the code)

1. Open from cache: the cache is one encrypted file (`FileAccess.open_encrypted_with_pass`, key per
   install, path `user://mail/` to confirm), ≤ 600 items ≈ 300 KB. It loads in ≤ 100 ms, and the first
   rows appear ≤ 300 ms after the tap on the reference phone. It is wiped on logout, and alliance mail
   is wiped on leaving the alliance.
2. Lists above 60 rows use ui-forge's `VirtualList` (fixed 144 px rows, a pool of visible + 4).
   Rewards and Personal (caps 200) always do.
3. Headers: `ResourceLoader.load_threaded_request(path)` on letter open; the panel shows parchment
   until `load_threaded_get_status()` is `THREAD_LOAD_LOADED`; the texture is freed on close.
4. Player text: a `RichTextLabel` with `bbcode_enabled = false` (or a `Label`). Template text may use
   the §3 whitelist of [templates.md](templates.md).
5. No `Timer` node polls mail. Refresh comes only from the head that rides the resume read, from
   opening the screen (if the head moved), and from an FCM data message when push is integrated
   (ship-forge, to confirm).
6. Routes: `mail/notices`, `mail/rewards`, `mail/alliance`, `mail/personal`, `mail/reports`,
   `mail/{tab}/{id}`. Toasts and chat cards open letters only through `UIRouter` (ui-forge
   architecture.md §5).

## 12. Failure modes and review checklist

| Fails when | Caught by |
|---|---|
| Claim all takes more than 2 taps from the HUD, or a letter more than 2 to read | [ ] `ux_flow_probe` paths `mail_claim_all`, `mail_read` |
| A touch target < 132 px, or Primary not 440 × 144 on the hand side | [ ] `ux_touch_probe` |
| Unviewed state readable only by colour | [ ] `a11y_audit` (seal shape + weight) |
| A tab label clips at +40% | [ ] `layout_audit` pseudo-locale; `w1f_aspect_sweep` prints `ASPECT SWEEP OK - 6 shapes, 0 faults` |
| First rows later than 300 ms from cache on the reference phone | [ ] mail_ui timing capture |
| A second tap during Busy sends a second claim | [ ] mail_ui double-tap case (the gate refuses it anyway) |
| Player BBCode takes effect | [ ] mail_ui injection case |
| A gambling-like claim animation | [ ] feel-forge review against monetization.md §9 |

- [ ] Every surface above has its route; empty, loading, error and offline states are designed.
- [ ] Every icon is Blender-made art that passes the 44 px survival check.
- [ ] Tap counts measured by `ux_flow_probe` and pasted.
- [ ] `contrast_test`, `a11y_audit`, `ux_touch_probe`, `layout_audit`, `w1f_aspect_sweep` green.
