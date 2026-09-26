# Chat UI — the ticker, the panel, the row, the thumb

Chat lives inside the one continuous castle ↔ realm space: it is a sheet over the world, never a
scene change. **ui-forge** implements it with its painted component kit (oak / parchment / gilt
frames as `NinePatchRect` / `StyleBoxTexture`); design-forge ux.md owns the HUD zones, the red-dot
budget and the global text and tap minimums; **transition-forge** owns the global motion tokens.
Numbers here are chat's PROPOSALS inside those rules, at the 1080 × 1920 portrait reference.

Unit note: 1080 px ≈ 400–430 dp on current phones, so **1 dp ≈ 2.5 px**. 48 dp ≈ 120 px.

## 1. The ticker (always visible in the HUD)

| Property | Value (PROPOSAL) |
|---|---|
| Position | directly above the bottom action bar; 24 px side margins (ux.md places the bar) |
| Size | visual strip 1032 × 84 px; **hit area 1032 × 120 px** (transparent parent `Control`; the extra 36 px extends upward, never over the action bar) |
| Content | one line: channel icon 48 px · sender name 32 px bold · text 34 px, ellipsis at the end |
| Source | the Fireside; the Market Cross only if the player opted it in (sampled ≤ 1 per 10 s, [channels.md](channels.md) §7); no alliance → Market Cross sampled |
| Cadence | each line holds ≥ 3.0 s; lines arriving faster are dropped from the ticker (never from the channel), and the newest shows with "+N" |
| Badge | WAX count badge (white numerals 9.12:1) for unread whispers + mentions only; 1–99, then "99+"; no red dot for Fireside or Market Cross |
| Tap | opens the panel at half height on the ticker's channel |
| Long-press (400 ms) | channel switcher for the ticker: Fireside / Market Cross / Off |
| Hidden | during battle presentation and full-screen ceremonies (battle-forge, feel-forge); returns ≤ 200 ms after |

Stickers show in the ticker as a 56 px thumbnail plus the sender name; share cards as their
48 px type icon plus the card title.

## 2. The panel (bottom sheet)

| State | Height | What stays visible above |
|---|---|---|
| Closed | 0 (ticker only) | full HUD |
| Half (default on open) | 960 px (50%) | the castle or realm view and the top resource bar |
| Full | 1690 px (88%) | the top resource bar |

Layout from the top of the sheet (half state; full adds list height only):

| Part | Height | Notes |
|---|---|---|
| Grab handle | 24 px bar in a 48 px strip | drag between Closed / Half / Full; the tab row below is also a drag area (a move > 12 px is a drag, less is a tap), so the drag target is ≥ 168 px tall |
| Channel tabs | 120 px | Fireside · Council (members only) · Market Cross · Whispers · Circles; icon 56 px (Blender-made art, never a line glyph) + label 28 px + count; labels shrink to 26 px then go icon-only when a translation is 30–40% longer |
| Pinned announcement | 0 or 96 px | one line, tap to expand; Fireside only |
| Message list | the rest | newest at the bottom |
| "N new ↓" pill | 88 px (hit 120 px) | appears when the player is > 1 screen above the bottom and messages arrive; never auto-jumps |
| Input bar | 132 px | sticker 120 px · quick call 120 px · text field 624 × 108 px (hit: full bar height) · send 120 px; 24 px margins, 12 px gaps (24 + 3 × 120 + 624 + 4 × 12 + 24 = 1080) |

- **One-hand rule**: the input bar, send, sticker and quick-call buttons sit in the bottom 700 px
  (the comfortable thumb zone); the tabs of the half sheet sit at 960 px from the bottom, in the
  stretch zone. Swiping left/right on the list also switches tabs (so the top row is never needed).
- **Keyboard**: when the soft keyboard (typically 700–900 canvas px tall) or the sticker picker
  opens, the sheet goes to Full first (a half sheet would leave no list); the input bar rises by
  `DisplayServer.virtual_keyboard_get_height()` (device px → canvas px by the stretch scale); the
  list shrinks and keeps its bottom message visible (≥ 3 rows stay visible above the keyboard).
- The Whispers and Circles tabs open a thread list first (row 120 px: avatar 80 px, name, last line,
  time, unread count); a thread opens in the same sheet with a back button (120 px) top-left.

## 3. The message row

| Element | Size / rule |
|---|---|
| Row side padding | 24 px |
| Avatar | 80 px circle crop of the player's chosen portrait (painted lane art; faces never code-built) |
| Gap avatar → bubble | 16 px |
| Bubble max width | 760 px (others, left) · 760 px (own, right-aligned, no avatar) |
| Header line | name 32 px bold INK · alliance tag `[ABC]` 28 px IRON · rank icon 32 px (alliance.md ranks) · relationship marker 24 px · time 28 px IRON right-aligned |
| Body text | 36 px, line height 1.3 (47 px), INK on PARCHMENT (12.66:1) |
| Grouping | same sender within 2 min: no avatar, no header, 6 px gap instead of 12 px |
| Mention of me | static WAX left bar 6 px + parchment tint; no blinking, no shake |
| System (Tidings) line | centred, 30 px IRON (7.46:1), no bubble, 16 px vertical padding |
| Tombstone | "Message removed" 28 px italic IRON; no content, no reason text in public |
| Emoji-only message (1–3 emoji) | 72 px glyphs, no bubble |
| Sticker | 240 × 240 px, no bubble; header line as text |
| Share card | 800 × 248 px ([share-cards.md](share-cards.md) §5) |

**Relationship colour** (self / ally / enemy / neutral) is a RESERVED channel (design-forge ux.md,
game-art-director readability.md own the values). In chat it appears only as the 24 px marker next
to a name, always with a shape (circle self, shield ally, crossed blades enemy, square neutral —
PROPOSAL shapes) so colour-blind players read it. Name text stays INK.

**Contrast table** (WCAG 2.x ratios computed from the canonical palette; ≥ 4.5:1 for text,
≥ 3:1 for non-text):

| Foreground on background | Ratio | Use |
|---|---|---|
| INK #1E1712 on PARCHMENT #E8D9B5 | 12.66:1 | body text, names |
| OAK #4A2E1B on PARCHMENT | 8.85:1 | secondary text |
| IRON #3B4048 on PARCHMENT | 7.46:1 | tags, time, system lines |
| WAX #8A1F24 on PARCHMENT | 6.53:1 | error and hold text |
| PARCHMENT on OAK | 8.85:1 | tab labels on the oak frame |
| GILT #C9A04C on OAK | 5.07:1 | selected tab label |
| White on WAX | 9.12:1 | count badges |
| **GILT on PARCHMENT** | **1.74:1** | **never for text**; decoration only |
| Troop line colours on PARCHMENT | 1.63–3.97:1 | **never for text**; swatches only, with a 2 px INK outline |

## 4. Share cards in the list

Rendered by the rules in [share-cards.md](share-cards.md); the whole card is the button (≥ 800 ×
248 px target). A card whose target is gone renders its stale state, never an error dialog.

## 5. Unread counts and mentions

| Rule | PROPOSAL |
|---|---|
| Per tab | count of messages after the read cursor; "99+" above 99; Tidings lines do not count |
| HUD | only the ticker badge (whispers + mentions); chat adds **no red dot** to the HUD (core-loop.md A7: dots only for claimable items and idle plates; ux.md decides whether the badge counts in the dot budget) |
| Opening a channel | ≤ 50 unread: scroll to the first unread with a "New" divider; > 50: open at the newest with "312 unread — jump to first" (one tap) |
| Read cursor | advanced when a message has been on screen ≥ 500 ms; written to the server at most once per 10 s and on close ([backend-cost.md](backend-cost.md) §5) |
| Mentions list | the @ icon in the panel header lists the last 50 mentions of 7 days; one tap jumps to the message |

## 6. Translation

- Channel header menu → "Translate messages: On / Off" (per channel, default Off). On means
  **on-device** translation of messages whose detected language differs from the reader's.
- First use shows one sheet: model size per language (≈ 30 MB on current Android on-device models
  — verify at integration), download on Wi-Fi by default, works offline after.
- Under a translated message: "Translated from Polski · Original" at 28 px IRON; tap swaps text.
- Devices without on-device support: long-press → Translate uses the capped cloud fallback
  (≤ 5 per player per day; a global monthly euro breaker, [backend-cost.md](backend-cost.md) §7.5).
  When the breaker trips, the menu item reads "Translation resting until the 1st".
- The ticker shows the translated text when that channel's translation is On.
- Quick calls, system lines and card titles never need translation: they are string keys.

## 7. Stickers and emoji

| Item | Rule (PROPOSAL) |
|---|---|
| Sticker art lane | painted image lane through **game-art-director** (new `stickers` group; id prefix `STK-` — confirm free in INTAKE_MAP.md); object-only stickers may instead be Blender renders through **blender-forge**; faces only on the painted lane or hero3d, never code-built |
| Source / display | 512 × 512 px source, transparent (magenta-key cutout), displayed 240 px in chat, 200 px in the picker, 56 px in the ticker |
| Readability | one subject filling ~80% of the frame, 3–5 value groups, INK outline, survives 56 px (squint test) |
| Content | the master style block; **no text in the art** (the house negative); no war gore; no money or offer imagery |
| Starter set | 16 free for everyone: 8 object/animal scenes + 8 lord expressions (one per lord, matched to portraits.md) |
| Picker | replaces the keyboard area (height = last keyboard height, min 720 px); 4 columns × 258 px cells; last-used row first |
| Emoji (keyboard) | allowed in text; count as graphemes; rendered by a `SystemFont` fallback (`font_names` = "Noto Color Emoji", "Apple Color Emoji" — verify per device); no bundled emoji font (APK size) |
| Selling | stickers never carry stats; whether sticker packs are ever sold is an owner decision (money-law, design-forge monetization.md); the free set covers every chat function |

## 8. Long-press action sheet

Long-press a message (400 ms) → a bottom action sheet (rows 120 px, in the thumb zone):
Reply · Copy · Translate · Mention · **Report** · **Block** · **Mute sender** (1 h / 8 h / 24 h / always,
this channel) · for officers in the Fireside: Remove message · Mute member in the Fireside (1 h / 24 h).
Report is 3 taps: long-press → Report → reason (sent at once; an optional note field follows).
Details and effects: [safety.md](safety.md) §8.

## 9. States (every list and every send has one)

| State | What the player sees |
|---|---|
| Empty channel | "The Fireside is quiet." + a Quick-call button (120 px) |
| Loading | 3 skeleton rows after 300 ms; nothing before 300 ms (no flash) |
| Offline | ticker shows "Reconnecting…" in IRON; sends queue (≤ 5), queued sends older than 2 min are dropped with "Not sent — tap to retry" |
| Sending | own row at 60% opacity until the server ack |
| Failed | WAX "Not sent · Retry" under the row after 10 s without ack |
| Rate limited / slow mode | send button shows the countdown ("18 s"); the text stays in the field |
| Held for review | "Waiting for review" under the message, visible only to the sender ([safety.md](safety.md) §7) |
| Muted / banned | the field is replaced by "You can write again in 42 min — why?" (opens the sanction mail from mail-forge) |
| Age band without free text | "Free text is off for your account. Horn calls and stickers are on." |
| Whisper request | Accept · Ignore · Block (each 120 px), text hidden until Accept |
| Blocked sender | messages hidden completely, no placeholder |

## 10. Motion (PROPOSAL inside transition-forge / ui-forge tokens)

| Motion | Duration | Easing |
|---|---|---|
| Ticker line out / in | 160 ms / 200 ms | ease-in cubic / ease-out cubic (`Tween.TRANS_CUBIC`) |
| Panel open to half | 240 ms | ease-out cubic |
| Panel close | 180 ms | ease-in cubic |
| Drag release snap | 200 ms; fling > 1,800 px/s picks the direction | ease-out cubic |
| New row | fade + rise 12 px, 150 ms | ease-out quad |
| Optimistic send | row visible ≤ 1 frame (16.7 ms) after tap | — |
| Reduced-motion setting | every slide becomes a 120 ms fade | linear |

No tween ever blocks input; no bounce; nothing flashes (a11y_audit).

## 11. Godot 4 implementation (ui-forge builds; rules chat requires)

```
ChatClient        (autoload Node)  WebSocketPeer, sync, local cache, send queue
ChatTicker        (Control, 120 px hit area) → strip 84 px (PanelContainer, Theme from ui-forge)
ChatPanel         (Control in the HUD CanvasLayer; layer order from ui-forge)
 └ Sheet (PanelContainer, StyleBoxTexture) → Handle · Tabs (HBoxContainer) · Pinned
   · List (ScrollContainer → Content: Control sized to the sum of row heights; pooled MessageRow
     children placed by hand, not by a VBoxContainer) · NewPill · InputBar (HBoxContainer)
MessageRow        HBoxContainer: Avatar (TextureRect 80 px) · VBoxContainer: Header (HBoxContainer of
                  Labels + TextureRects) · Body (RichTextLabel, fit_content = true,
                  autowrap_mode = TextServer.AUTOWRAP_WORD_SMART)
```

1. **User text is never markup.** Body text is inserted with `RichTextLabel.add_text()`; mention
   highlight uses `push_color()` / `add_text()` / `pop()`. Never `append_text()` or the `text`
   property with `bbcode_enabled = true` on player content — `[url]`, `[img]` or `[font_size]`
   typed by a player must render as the literal characters. Names and tags use `Label` (no BBCode).
2. **Pooled virtual list**: ≤ 40 `MessageRow` instances exist; `Content.custom_minimum_size.y` is
   the sum of cached row heights (measured once per message and width, re-measured on text-scale
   change); only visible rows + 8 buffer are bound and positioned; the client keeps ≤ 200 messages
   per channel in memory; older pages (30) load on scroll and keep the scroll anchor on the row in view.
3. **Socket life**: `ChatClient` polls `WebSocketPeer.poll()` in `_process` only while connected;
   on `NOTIFICATION_APPLICATION_PAUSED` it closes (code 1000) and on
   `NOTIFICATION_APPLICATION_RESUMED` it reconnects and syncs ([backend-cost.md](backend-cost.md) §5).
4. **Local cache**: last 100 messages per channel in `user://chat/` via
   `FileAccess.open_encrypted_with_pass()` (per-account key fetched from the game backend at login,
   so a logged-out device cannot read it); wiped on logout, account switch,
   alliance leave (Fireside/Council files) and when rows pass their retention.
5. **Stickers load on demand** with `ResourceLoader.load_threaded_request()`; the picker shows a
   parchment placeholder until loaded (≤ 100 ms target on the reference phone).
6. **Input**: `LineEdit` with `max_length = 200` (client guard; the server counts graphemes),
   character counter from 160 ("40 left"), `text_submitted` sends.

## 12. Performance budgets (on ship-forge's reference low-end phone)

| Budget | Value |
|---|---|
| Panel open | ≤ 1 dropped frame at 60 fps |
| Scroll with 200 rows loaded | 60 fps, ≤ 16.7 ms frame time p95 |
| Draw calls, panel open | ≤ 40 (chrome and icons from atlases) |
| Chat memory | ≤ 12 MB (history ≤ 2 MB, stickers ≤ 8 MB with VRAM compression) |
| Network in foreground | ≤ 50 KB per minute at the base scenario (typical 3–8 KB) |
| Tap to first rows (cached) | ≤ 300 ms; from network p95 ≤ 1.0 s |

## 13. Failure modes

| Fails when | Caught by |
|---|---|
| A player's `[img]…[/img]` or `[url]` renders as markup | [ ] `chat_injection_probe` (qa.md): 0 parsed tags |
| Ticker or panel buttons < 120 px hit area | [ ] `ux_touch_probe` on the chat scenes |
| Tabs overflow with +40% German/French labels | [ ] `layout_audit` with the l10n long-string pass |
| Keyboard covers the input field on some aspect | [ ] `w1f_aspect_sweep` with keyboard height mocked (6 shapes) |
| GILT or line colours used as text on parchment | [ ] `contrast_test` over chat scenes (≥ 4.5:1 text) |
| List stutters with 200 rows | [ ] frame-time capture in `ux_flow_probe` chat pass |
| Unread count differs from server after reconnect | [ ] `chat_catchup_probe` |

## 14. UI checklist

- [ ] Every control ≥ 120 px hit area; bottom 700 px holds every frequent action.
- [ ] Text ≥ 28 px everywhere; body 36 px; 100/115/130% text scale reflows without clipping.
- [ ] All text pairs from the contrast table; no GILT text on parchment.
- [ ] User text only through `add_text()`/`Label`.
- [ ] Every state in §9 designed and screenshot in the ux_flow_probe chat pass.
- [ ] Relationship marker has a shape as well as a colour.
- [ ] Motion inside §10; reduced-motion path works; no flashing.
- [ ] Icons are Blender-made art (ui-forge icon rules), stickers from the painted lane.
