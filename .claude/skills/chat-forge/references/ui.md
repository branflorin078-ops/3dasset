# Chat UI — the ticker, the panel, the row, the thumb

Chat lives inside the one continuous castle ↔ realm space: it is a **sheet** over the world
(ui-forge architecture.md §2), never a scene change. **ui-forge** builds it with its painted kit
and owns every global number used here: the 1080 × 1920 reference and 2.5–3.0 design px per dp;
hit rects ≥ 132 px, ≥ 144 px for frequent actions; type sizes 32 (digits and badges only) · 36
(any sentence) · 42 (body) · 50 (labels); the spacing scale 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64;
the contrast table; sheet snaps; tab rules; motion tokens (ui-forge SKILL.md "reference frame",
components.md, motion.md). design-forge ux.md will own HUD zones and the red-dot budget when it
exists (not on disk at this writing — ui-forge hud.md carries them today). This file sets chat's
layouts inside those numbers; a value here that breaks a ui-forge rule is a bug in THIS file
(ui-forge screens.md S19). All values are PROPOSALS at 1080 × 1920 portrait.

## 1. The ticker (HUD slot H9)

| Property | Value (PROPOSAL) |
|---|---|
| Slot | ui-forge hud.md H9: visual strip x 24, y 1576, 1032 × 84; hit rect 1032 × 132 (y 1570–1702), easy zone, 42 px above the bottom bar (y 1744) |
| Two targets | **read area** 884 × 132 hit → panel opens at 70% to read · 16 px gap · **Reply quill** 132 × 132 hit (icon 64 px, Blender-made) → panel at 92% with the keyboard up. "Reply in alliance chat" = Reply (1) → type → Send (2), ui-forge architecture.md §3 core action 17 |
| Content | channel icon 48 px · sender name 36 px bold INK · text 36 px INK (caption size), one line, ellipsis; rally calls and system lines start with their icon (hud.md §9) |
| Source | the Fireside; Market Cross only if the player opted it in (sampled ≤ 1 per 10 s, [channels.md](channels.md) §7); no alliance → Market Cross sampled |
| Cadence | each line holds ≥ 3.0 s (the realm cap of 20 per min = one line per 3 s); faster lines are dropped from the ticker only, never from the channel; the newest shows with "+N" |
| Count pill | ui-forge hud.md §5: 44 px high, ≥ 44 px wide, digits 32 px bold PARCHMENT on WAX (6.53:1); unread whispers + mentions only; 1–99, then "99+"; chatter in the Fireside or Market Cross never makes a mark |
| Ticker off (Settings) | the strip hides; the whisper + mention count moves to the Alliance entry of the bottom bar (hud.md §5, P3 count) |
| Long-press (400 ms) | a shortcut to the ticker's channel switch (Fireside / Market Cross / Off); the same switch sits in the panel's channel menu — nothing depends on the hidden gesture |
| Hidden | during battle presentation and full-screen ceremonies (battle-forge presentation.md, feel-forge) and while a full screen is open (hud.md §9); back ≤ 200 ms after |

Stickers show in the ticker as a 56 px thumbnail plus the sender name; share cards as their
48 px type icon plus the card title (icons pass ui-forge's 44 px survival test, icons.md §1).

## 2. The panel (a ui-forge sheet)

| State | Height (ui-forge sheet snaps) | What stays visible above |
|---|---|---|
| Closed | 0 (ticker only) | full HUD |
| Open (default) | 70% = 1,344 px | top 576 px: the resource strip (H1) and the world, dimmed 40% |
| Full (keyboard, sticker picker, or a drag up) | 92% = 1,766 px | the resource strip |
| 40% snap | not used: the list would hold fewer than 4 rows | — |

Route: `chat/{channel}` through `UIRouter.open()` (ui-forge godot.md §4), in the L20_Panels layer;
drag, snaps and interruptible tweens come from ui-forge's panel base (`UIPanel.gd`, godot.md §5).
The sheet's content ends on the safe area's bottom edge (gesture-bar inset 48–66 px, hud.md §1).

Layout, top to bottom (Open; Full adds list height only):

| Part | Height | Notes |
|---|---|---|
| Sheet top edge + grabber | 96 px | ui-forge kit piece (components.md §3); a move > 12 px is a drag, less is a tap |
| Header | 96 px | channel name 50 px label · @ mentions button and channel menu (each 132 px hit, Blender-made icons); rare actions only — stretch zone at Open, hard zone at Full |
| Pinned announcement | 0 or 96 px | one line 36 px + pin icon; tap expands to the full ≤ 400 graphemes; Fireside only |
| Message list | the rest: 872 px at Open (776 with a pin), 1,294 px at Full | newest at the bottom |
| "N new ↓" pill | 96 px visual, 132 px hit, over the list's bottom edge | appears when the player is > 1 screen above the bottom and messages arrive; never auto-jumps |
| Tab strip | 112 px visual, 132 px hit (ui-forge components.md §6) | **directly above the input bar** (ui-forge: tabs sit above the footer): Fireside · Council (members only) · Market Cross · Whispers · Circles — 5 × 206 px ≥ the 180 px minimum; icon 64 px (Blender-made art, never a line glyph) + a one-word 42 px label + count pill; a label that does not fit at 42 px after the +40% pass goes icon-only, and the header shows the full name |
| Input bar | 168 px (12 + 144 + 12) | sticker · quick call · text field · send: 24 + 3 × 144 + 552 + 3 × 16 + 24 = 1,080 px. Buttons 120 px visual inside 144 px hit rects; field 552 × 120 px, 42 px text (components.md §14), its hit rect = the full 144 px row |

- **One-hand rule**: the input bar and the tab strip fill the bottom 280 px of the sheet
  (y ≈ 1,574–1,854, ui-forge's easy zone y ≥ 1,150); every frequent action is there. The header
  holds only rare actions. **No swipe between tabs** (ui-forge components.md §6: it fights the
  edge-back gesture).
- **Keyboard**: opening the keyboard or the sticker picker moves the sheet to Full first; the tab
  strip hides while typing (typing happens in one channel); the input bar rises by
  `DisplayServer.virtual_keyboard_get_height()` converted from device px to canvas px (÷ the
  stretch scale); the focused field stays ≥ 48 px above the keyboard (components.md §14); the list
  keeps its bottom message visible (≥ 3 rows above the keyboard).
- **Whispers and Circles** open a thread list first (ui-forge standard row, 144 px: avatar 96 px,
  name 42 px, last line 36 px, time 32 px digits, count pill); a thread opens in the same sheet;
  back = the system back or the header's back arrow (132 px hit).

| Fails when | Caught by |
|---|---|
| A tab strip at the top of the sheet (y ≈ 600, hard zone) | [ ] `ux_touch_probe` zone check on the chat scenes |
| The keyboard covers the field on a tall or short phone | [ ] `w1f_aspect_sweep` with the keyboard height mocked (6 shapes) |

## 3. The message row

| Element | Size / rule |
|---|---|
| Row side padding | 24 px |
| Avatar | 96 px circle crop of the player's chosen lord portrait (CMD crop computed from `crop.json`, commander-forge portrait-lane.md §3, head 80–90% of the crop; its table lists 64 / 44 px chat avatars — 96 px is chat's PROPOSAL to match ui-forge's ≥ 96 px row art, a derived crop, no new art). Faces never code-built. **Tap** → the player card (ui-forge `profile/{id}`) with Whisper · Report · Block · Mute as visible buttons |
| Gap avatar → bubble | 16 px |
| Bubble | max width 760 px (others: left, after the avatar; own: right-aligned, no avatar); 12 px padding; ≈ 33 characters per line at 42 px, inside ui-forge's 28–60 rule |
| Header line | name 36 px bold INK · alliance tag `[ABC]` 36 px IRON · rank badge 36 px (RNK art, shape AND word, alliance.md §2 rule 5) · relationship marker 32 px · chat seals 36 px · time 32 px digits IRON, right-aligned |
| Body text | 42 px, line height 1.3 (55 px), INK on PARCHMENT (12.66:1) |
| Grouping | same sender within 2 min: no avatar, no header, 8 px gap instead of 16 px |
| Mention of me | static WAX left bar 8 px; no blinking, no shake |
| System (Tidings) line | centred, 36 px IRON (7.46:1), event icon 48 px, no bubble, 16 px vertical padding |
| Tombstone | "Message removed" 36 px italic IRON; no content, no reason text in public |
| Emoji-only message (1–3 emoji) | 96 px glyphs, no bubble |
| Sticker | 240 × 240 px, no bubble; header line as text |
| Share card | 880 × 320 px (ui-forge components.md §8; [share-cards.md](share-cards.md) §5); fits beside the avatar: 1,080 − 24 − 96 − 16 − 24 = 920 px |
| Typical heights | one-line message ≈ 142 px (header 47 + body 55 + 2 × 12 padding + 16 gap); three lines ≈ 252 px; Open shows 4–6 rows |

**Relationship marker**: colour AND shape come from design-forge
[world.md](../../design-forge/references/world.md) §12, the single source (self circle · ally
heater shield, Accord shield with a bar · enemy crossed blades · neutral square; its stroke
recipe with the 2 px INK keyline). Chat does not restate the hex values. Name text stays INK.

**Chat seals** (monetization.md §1 lists them as stat-free cosmetics; patronage rank VII adds a
second, §6): ≤ 2 seals, 36 px each, after the name. A seal never tints the name or the text,
never animates, is never larger than the rank badge, and never shows the patronage rank
(monetization.md §6 rule 5). That is the only purchasable thing that may appear in a row.

**Contrast** (WCAG 2.x ratios of the canonical palette; the same values as ui-forge
components.md §2; ≥ 4.5:1 for text, ≥ 3:1 for icons and controls):

| Foreground on background | Ratio | Use |
|---|---|---|
| INK #1E1712 on PARCHMENT #E8D9B5 | 12.66:1 | body text, names |
| OAK #4A2E1B on PARCHMENT | 8.85:1 | card line 2 |
| IRON #3B4048 on PARCHMENT | 7.46:1 | tags, time, system lines, tombstones |
| WAX #8A1F24 on PARCHMENT | 6.53:1 | error and hold text |
| PARCHMENT on OAK | 8.85:1 | tab labels and card type tags on the oak frame |
| GILT #C9A04C on OAK | 5.07:1 | selected tab underline and label |
| PARCHMENT on WAX | 6.53:1 | count pills |
| **GILT on PARCHMENT** | **1.74:1** | **never for text**; decoration only |
| IRON on OAK | 1.19:1 | **never** |
| Troop line colours on PARCHMENT | 1.63–3.97:1 | **never for text**; swatches only, with a 2 px INK outline |

## 4. Share cards in the list

Rendered by the rules in [share-cards.md](share-cards.md); the whole 880 × 320 card is the
button. A card whose target is gone renders its stale state, never an error dialog.

## 5. Unread counts and mentions

| Rule | PROPOSAL |
|---|---|
| Per tab | count of messages after the read cursor; "99+" above 99; Tidings lines do not count |
| HUD marks | ui-forge hud.md §5: mentions and whispers are **P3** marks (count pill; cleared when viewed; expire after 72 h unviewed). They count toward the ≤ 3 marks at session open (core-loop §9 A7); Fireside and Market Cross chatter never makes a mark |
| Opening a channel | ≤ 50 unread: scroll to the first unread with a "New" divider; > 50: open at the newest with "312 unread — jump to first" (one tap) |
| Read cursor | advanced when a message has been on screen ≥ 500 ms; written to the server at most once per 10 s and on close ([backend-cost.md](backend-cost.md) §5) |
| Mentions list | the @ button in the header lists the last 50 mentions of 7 days; one tap jumps to the message |

## 6. Translation

- Channel menu → "Translate messages: On / Off" (per channel, default Off). On means
  **on-device** translation of messages whose detected language differs from the reader's.
- **Godot 4 has no translation API.** On-device translation needs a native plugin per platform
  (ship-forge builds and sizes them): Android — a Godot Android plugin (v2 format, Godot 4.2+)
  wrapping Google ML Kit Translation and ML Kit Language Identification; iOS — an iOS plugin
  wrapping Apple's Translation framework (`TranslationSession`, iOS 18+) and the NaturalLanguage
  framework for detection. Devices below those versions use the capped cloud fallback. Verify each
  API, its terms, its language list and its model size at integration.
- First use shows one sheet: model size per language (≈ 30 MB per ML Kit language model —
  verify), download on Wi-Fi by default, works offline after.
- Under a translated message: "Translated from Polski · Original" at 36 px IRON; tap swaps text.
- Devices without on-device support: long-press → Translate uses the capped cloud fallback
  (≤ 5 per player per day; a global monthly euro breaker, [backend-cost.md](backend-cost.md) §7.5).
  When the breaker trips, the menu item reads "Translation resting until the 1st".
- The ticker shows the translated text when that channel's translation is On.
- Quick calls, system lines and card titles never need translation: they are string keys.

## 7. Stickers and emoji

| Item | Rule (PROPOSAL) |
|---|---|
| Sticker art lane | painted image lane through **game-art-director** (new `stickers` group; id prefix `STK-` — confirm free in INTAKE_MAP.md); object-only stickers may instead be Blender renders through **blender-forge**; faces only on the painted lane (lord faces on-model through commander-forge's face-structure sheets, portrait-lane.md §4), never code-built |
| Source / display | 512 × 512 px source, magenta-key cutout (the house cutout language, game-art-director ui-icons.md), displayed 240 px in chat, 200 px in the picker, 56 px in the ticker |
| Readability | one subject filling ~80% of the frame, 3–5 value groups, INK outline, passes the 44 px survival test (ui-forge icons.md §1) |
| Content | the master style block; **no text in the art** (the house negative); no war gore; no money or offer imagery |
| Starter set | 16 free for everyone: 8 object/animal scenes + 8 lord expressions (one per lord, matched to portraits.md) |
| Earned stickers | alliance gift fragments (alliance.md §6: 10 fragments = a pennon dye or a chat sticker); season track cosmetics if monetization.md §7 lists them |
| Picker | replaces the keyboard area (height = last keyboard height, min 720 px); 4 columns × 258 px cells (4 × 258 = 1,032 px); last-used row first |
| Emoji (keyboard) | allowed in text; count as graphemes; rendered by a `SystemFont` fallback (`font_names` = "Noto Color Emoji", "Apple Color Emoji" — verify per device); no bundled emoji font (APK size) |
| Selling | stickers never carry stats; whether sticker packs are ever sold is an owner decision (money-law, design-forge monetization.md §1); the free set covers every chat function |

## 8. Message actions — visible path first, long-press as the shortcut

- **Visible path** (ui-forge's rule against hidden-only gestures): a tap on the avatar or name
  opens the player card with **Report · Block · Mute** as buttons. Report = name (1) → Report (2)
  → reason (3), sent at once; an optional note field follows.
- **Shortcut**: long-press a message (400 ms; in chat rows this replaces ui-forge's long-press
  tooltip, components.md §10) → a bottom action sheet of 144 px rows in the thumb zone: Reply ·
  Copy · Translate · Mention · **Report** · **Block** · **Mute sender** (1 h / 8 h / 24 h / always,
  this channel). For the Liege (targets ranks 1–4) and any officer (targets ranks 1–3), per
  alliance.md §2 row 13, in the Fireside: Remove message · Mute in the Fireside (1 h / 24 h).
- Details and effects: [safety.md](safety.md) §8.

## 9. States (every list and every send has one)

| State | What the player sees |
|---|---|
| Empty Fireside | painted empty-state art (a banked fire, Blender-made) + "The Fireside is quiet." + Horn call button (144 px) |
| Empty Council / Circle | "No one has spoken here yet." + Horn call button |
| Empty Market Cross | "Market Cross is quiet." (T0: "You can read Market Cross now; you can write here after 48 h.") |
| No whispers | "No whispers yet. Tap a name to whisper." |
| Loading | 3 skeleton rows after 300 ms; nothing before 300 ms (no flash) |
| Offline | ticker shows "Reconnecting…" in IRON; sends queue (≤ 5); queued sends older than 2 min are dropped with "Not sent — tap to retry" |
| Sending | own row at 60% opacity until the server ack |
| Failed | WAX "Not sent · Retry" under the row after 10 s without ack |
| Rate limited / slow mode | send button shows the countdown ("18 s", 32 px digits); the text stays in the field |
| Held for review | "Waiting for review" under the message, visible only to the sender ([safety.md](safety.md) §7) |
| Muted / banned | the field is replaced by "You can write again in 42 min — why?" (opens the sanction mail from mail-forge) |
| Age band without free text | "Free text is off for your account. Horn calls and stickers are on." |
| Whisper request | Accept · Ignore · Block (each 144 px hit), text hidden until Accept |
| Blocked sender | messages hidden completely, no placeholder |
| Chat box down | ticker "Chat resting — the realm goes on"; panel shows the cached messages marked "Saved 14:20" (ui-forge states.md §4 wording) |

## 10. Motion (ui-forge motion.md tokens; chat-only lines marked)

| Motion | Duration | Easing |
|---|---|---|
| Ticker line out / in (chat-only) | 160 ms / 200 ms | CUBIC IN / CUBIC OUT |
| Panel open (`sheet_in`) | 240 ms | CUBIC OUT |
| Panel close (`sheet_out`) | 180 ms | CUBIC IN |
| Drag release (`snap`) | 200 ms; a fling ≥ 1,800 px/s picks the direction | CUBIC OUT |
| New row (chat-only) | fade + rise 12 px, 150 ms | QUAD OUT |
| Optimistic send | row visible ≤ 1 frame (16.7 ms) after the tap (ui-forge states.md §4) | — |
| Reduced motion | every slide becomes a 120 ms linear fade (motion.md §4) | linear |

No tween ever blocks input; no bounce; nothing flashes more than 3 times per second (a11y_audit).

## 11. Godot 4 implementation (ui-forge builds; rules chat requires)

```
ChatClient   (autoload Node)  WebSocketPeer, sync, local cache, send queue
ChatTicker   (Control in L10_HUD, H9 slot, 1032 × 132 hit) → strip 84 px (PanelContainer, ui-forge Theme)
ChatPanel    (UIPanel sheet in L20_Panels, opened by UIRouter.open("chat/fireside"))
 └ Sheet (StyleBoxTexture frame) → Grabber · Header · Pinned
   · List (ScrollContainer → Content: Control sized to the sum of row heights; pooled MessageRow
     children placed by hand, not by a VBoxContainer) · NewPill · Tabs (HBoxContainer) · InputBar
MessageRow   HBoxContainer: Avatar (TextureRect 96 px) · VBoxContainer: Header (HBoxContainer of
             Labels + TextureRects) · Body (RichTextLabel, fit_content = true,
             autowrap_mode = TextServer.AUTOWRAP_WORD_SMART)
```

1. **User text is never markup.** Body text is inserted with `RichTextLabel.add_text()`; mention
   highlight uses `push_color()` / `add_text()` / `pop()`. Never `append_text()` or the `text`
   property with `bbcode_enabled = true` on player content — `[url]`, `[img]` or `[font_size]`
   typed by a player must render as the literal characters. Names and tags use `Label` (no BBCode).
2. **Variable-height virtual list** (ui-forge godot.md §10 is fixed-height; chat extends it):
   ≤ 40 `MessageRow` instances; row heights cached per message and width (re-measured on a
   text-scale change); prefix sums of the heights give `Content.custom_minimum_size.y` and, by a
   binary search, the first visible row; only visible rows + 8 buffer are bound; ≤ 200 messages per
   channel in memory; older pages (30) load on scroll and keep the scroll anchor on the row in
   view. `scroll_deadzone = 24` (a scroll never becomes a tap).
3. **Socket life**: `WebSocketPeer.connect_to_url("wss://…", TLSOptions.client())`;
   `poll()` in `_process` only while the state is not `STATE_CLOSED`; read with
   `get_available_packet_count()` / `get_packet().get_string_from_utf8()`; send with
   `send_text()`. Keep `inbound_buffer_size` at ≥ 64 KB (the default 65,535 B holds a 15 KB page).
   On `NOTIFICATION_APPLICATION_PAUSED` close with code 1000; on `NOTIFICATION_APPLICATION_RESUMED`
   reconnect and sync ([backend-cost.md](backend-cost.md) §5).
4. **Local cache**: last 100 messages per channel in `user://chat/` via
   `FileAccess.open_encrypted_with_pass()` (per-account key fetched from the game backend at login,
   so a logged-out device cannot read it); wiped on logout, account switch, alliance leave
   (Fireside/Council files) and when rows pass their retention.
5. **Stickers load on demand** with `ResourceLoader.load_threaded_request()` (then
   `load_threaded_get_status()` / `load_threaded_get()`); the picker shows a parchment placeholder
   until loaded (≤ 100 ms target on the reference phone).
6. **Input**: a one-line `LineEdit` (no line breaks from the stock client) with `max_length = 200`
   (a client guard counted in characters; the server counts graphemes), a counter from 160
   ("40 left", 32 px digits), `text_submitted` sends. Announcements use a `TextEdit` that enforces
   ≤ 3 line breaks and 400 graphemes in `text_changed`.

## 12. Performance budgets (on ship-forge's reference low-end phone)

| Budget | Value |
|---|---|
| Panel open | ≤ 1 dropped frame at 60 fps |
| Scroll with 200 rows loaded | 60 fps, ≤ 16.7 ms frame time p95 |
| Draw calls, panel open | ≤ 40 (chrome and icons from atlases, ui-forge godot.md §13) |
| Chat memory | ≤ 12 MB (history ≤ 2 MB, stickers ≤ 8 MB with VRAM compression) |
| Network in foreground | ≤ 50 KB per minute at the base scenario (typical 3–8 KB) |
| Tap to first rows (cached) | ≤ 300 ms; from network p95 ≤ 1.0 s |

## 13. Failure modes

| Fails when | Caught by |
|---|---|
| A player's `[img]…[/img]` or `[url]` renders as markup | [ ] `chat_injection_probe` (qa.md): 0 parsed tags |
| A chat control has a hit rect < 132 px, or send / tabs / ticker < 144 px | [ ] `ux_touch_probe` on the chat scenes |
| Text below 36 px (other than 32 px digits) or off the ui-forge type scale | [ ] `layout_audit` font-size scan of the chat scenes |
| Tabs overflow with +40% German/French labels | [ ] `layout_audit` with the l10n long-string pass |
| Keyboard covers the input field on some aspect | [ ] `w1f_aspect_sweep` with keyboard height mocked (6 shapes) |
| GILT or line colours used as text on parchment | [ ] `contrast_test` over chat scenes (≥ 4.5:1 text) |
| List stutters with 200 rows | [ ] frame-time capture in `ux_flow_probe` chat pass |
| Unread count differs from the server after reconnect | [ ] `chat_catchup_probe` |
| Report reachable only by long-press | [ ] `ux_flow_probe` chat pass: Report via the player card in 3 taps |

## 14. UI checklist

- [ ] Every hit rect ≥ 132 px; send, tabs, ticker and the Reply quill ≥ 144 px (ticker 132 high by
      hud.md H9 — ui-forge's slot); every frequent action in the bottom 280 px of the sheet.
- [ ] Type only from the ui-forge scale: 42 body, 36 captions and names, 32 digits, 50 the header
      label; ≤ 3 sizes per surface plus digits; 100 / 115 / 130% text scale reflows without clipping.
- [ ] Spacing only from 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.
- [ ] All text pairs from the contrast table; no GILT text on parchment.
- [ ] User text only through `add_text()` / `Label`.
- [ ] Every state in §9 designed and screenshot in the ux_flow_probe chat pass.
- [ ] Relationship marker taken from world.md §12 (shape AND colour), not restated.
- [ ] Motion inside §10; reduced-motion path works; no flashing.
- [ ] Icons are Blender-made art (ui-forge icon rules), stickers from the painted lane.
