# Godot 4 patterns — how the kit is built

Patterns for the shipped Godot (4.7.2, per game-director). Node, autoload and file names are
PROPOSALS: map them to the shipped `ui/` tree first (paths to confirm). Test two APIs on 4.7
before relying on them: the screen-reader properties (§11) and hinge reporting (hud.md §10.4).

## 1. Project settings

| Setting | Value | Why |
|---|---|---|
| `display/window/size/viewport_width` / `_height` | 1080 / 1920 | the design canvas |
| `display/window/stretch/mode` / `aspect` | `canvas_items` / `expand` | crisp 2D at every resolution; tall phones and tablets gain space |
| `display/window/handheld/orientation` | portrait | the game is portrait |
| `input_devices/pointing/emulate_touch_from_mouse` | true | desktop test runs behave like touch |
| `gui/theme/custom` | the project Theme (components.md §15) | one Theme for every Control |

## 2. Scene tree and CanvasLayer order

```
Main (Node3D: the world, CameraDirector from transition-forge)
UIRoot (Node)                      autoloads: UIRouter · UIPool · Toasts · Badges · TimerHub · Settings
├─ L05_WorldUI  (CanvasLayer 5)    status bubbles, building focus labels (hud.md §7)
├─ L10_HUD      (CanvasLayer 10)   SafeArea → H1–H10 zones
├─ L20_Panels   (CanvasLayer 20)   drawers, sheets, full screens, pickers (UIRouter stack)
├─ L30_Modal    (CanvasLayer 30)   ≤ 1 modal + its scrim
├─ L40_Toast    (CanvasLayer 40)   toasts, the digest, the offline band
├─ L50_Guide    (CanvasLayer 50)   onboarding overlay, pointer, cards (screens.md S16)
├─ L60_Cover    (CanvasLayer 60)   transition-forge's veil or cover, if it uses a 2D layer
└─ L90_Debug    (CanvasLayer 90)   probes' overlays (never in release builds)
```

Each layer has one full-rect root Control with the Theme and a SafeArea child. Toasts sit above
modals; the guide sits above everything tappable; nothing gameplay-related uses a layer above 50.

## 3. Safe area, anchors and the Hand mirror

```gdscript
## SafeArea.gd - a full-rect MarginContainer under each CanvasLayer's root Control.
class_name SafeArea extends MarginContainer

@export var debug_insets := Vector4i(0, 0, 0, 0)   # left, top, right, bottom in design px (desktop sweeps)

func _ready() -> void:
	get_viewport().size_changed.connect(_apply)
	_apply()

func _apply() -> void:
	var ins := Vector4(debug_insets)
	if OS.has_feature("mobile"):
		var safe := Rect2(DisplayServer.get_display_safe_area())
		var win := Vector2(DisplayServer.window_get_size())
		var k := get_viewport().get_visible_rect().size.x / win.x   # window px -> design px
		ins = Vector4(safe.position.x, safe.position.y, win.x - safe.end.x, win.y - safe.end.y) * k
	add_theme_constant_override("margin_left", maxi(0, int(ins.x)))
	add_theme_constant_override("margin_top", maxi(0, int(ins.y)))
	add_theme_constant_override("margin_right", maxi(0, int(ins.z)))
	add_theme_constant_override("margin_bottom", maxi(0, int(ins.w)))
```

The aspect sweep sets `debug_insets` to real device insets (e.g. top 132, bottom 63), so a
desktop run shows notch problems too.

**Anchoring**: top zones to the top corners, bottom zones to the bottom; nothing is anchored to
the centre except the bottom bar's slot row (216 px slots, hud.md §10.3).

```gdscript
## Mirror one HUD zone around the vertical centre line (Hand = Left). Never use RTL for this.
static func mirror_x(c: Control) -> void:
	var l := c.anchor_left; var r := c.anchor_right
	var ol := c.offset_left; var o_r := c.offset_right
	c.anchor_left = 1.0 - r
	c.anchor_right = 1.0 - l
	c.offset_left = -o_r
	c.offset_right = -ol
```

A zone at x 16–136 anchored left becomes x W−136 … W−16 anchored right; a full-width zone stays
full width. Apply it to every zone root and footer; text direction never changes.

## 4. The router and the Android back button

```gdscript
## UIRouter.gd - autoload. The only code that opens, stacks and closes surfaces.
extends Node

const ROUTES := {   # route head -> [scene, layer]; the full table is architecture.md §5 (paths to confirm)
	"building": ["res://ui/sheets/building_card.tscn", "panels"],
	"plates": ["res://ui/hud/tracker_drawer.tscn", "panels"],
	"lords": ["res://ui/screens/lords.tscn", "panels"],
}
var _stack: Array[UIPanel] = []
var _back_armed_until := 0

func _ready() -> void:
	get_tree().quit_on_go_back = false

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		back()

func open(route: String) -> void:
	var parts := route.split("/")
	var row: Array = ROUTES.get(parts[0], [])
	if row.is_empty():
		push_warning("UIRouter: unknown route " + route)
		return
	var panel: UIPanel = UIPool.take(row[0])     # pre-instanced or warm (motion.md §5)
	UIPool.attach(panel, row[1])                 # adds it under the layer's SafeArea
	panel.enter(parts.slice(1))                  # ids only, never display text
	_stack.append(panel)

func back() -> void:
	if _stack.is_empty():                        # HUD rest: never a menu (live realm)
		var now := Time.get_ticks_msec()
		if now < _back_armed_until:
			get_tree().quit()
		else:
			_back_armed_until = now + 2000
			Toasts.show_key("TOAST_BACK_AGAIN_TO_LEAVE")
		return
	var top: UIPanel = _stack.back()
	if top.on_back():                            # the panel closed its own picker first
		return
	_stack.pop_back()
	top.close_panel()
```

Deep links open each parent first, without its tween, to build the back history
(architecture.md §5.2). The modal-count assertion (≤ 1) lives in `open()`.

## 5. The panel base — interruptible, distance-proportional, never blocking

```gdscript
## UIPanel.gd - base of every sheet, drawer and full screen. This node is full-rect; `sheet` is the
## painted body in a plain Control (a Container would re-sort it and undo the tween).
class_name UIPanel extends Control

const SHEET_IN := 0.24
const SHEET_OUT := 0.18
@export var sheet: Control
@export var first_focus: Control
var _tw: Tween
var _opener: Control

func enter(_args: PackedStringArray) -> void:
	_opener = get_viewport().gui_get_focus_owner()
	if not visible:
		sheet.position.y = size.y                  # start below the screen
	show()
	var shown_y := size.y - sheet.size.y
	if Settings.reduced_motion:
		sheet.position.y = shown_y
		modulate.a = 0.0
		_fade(1.0)
	else:
		modulate.a = 1.0
		_slide(shown_y, SHEET_IN, Tween.EASE_OUT)
	if first_focus:
		first_focus.grab_focus()                   # input is live from this frame on

func on_back() -> bool:
	return false                                   # override: close an inner picker, return true

func close_panel() -> void:
	var t: Tween = _fade(0.0) if Settings.reduced_motion else _slide(size.y, SHEET_OUT, Tween.EASE_IN)
	t.tween_callback(hide)
	if is_instance_valid(_opener):
		_opener.grab_focus()

func _slide(target_y: float, full_s: float, ease_type: Tween.EaseType) -> Tween:
	var dist := absf(sheet.position.y - target_y)
	var dur := maxf(0.06, full_s * dist / maxf(sheet.size.y, 1.0))   # motion.md §3.3
	_new_tween().set_trans(Tween.TRANS_CUBIC).set_ease(ease_type) \
		.tween_property(sheet, "position:y", target_y, dur)
	return _tw

func _fade(to: float) -> Tween:
	_new_tween().tween_property(self, "modulate:a", to, 0.12)
	return _tw

func _new_tween() -> Tween:
	if _tw and _tw.is_valid():
		_tw.kill()                                 # interrupt: the next move starts from here
	_tw = create_tween()
	_tw.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)  # UI keeps moving while the game tree is paused
	return _tw
```

Test it: open, then close at frame 3; open again at frame 5. The sheet must reverse twice with
no jump and no hide in between (the `hide` callback dies with the killed tween).

## 6. Collapsing portrait header (lord detail, screens.md S5)

The portrait sits BEHIND the ScrollContainer; the content starts with a 580 px transparent
spacer. On scroll value `v`: portrait `position.y = -v * 0.5`, name band `modulate.a = 1 -
clamp(v / 300, 0, 1)`, and a compact 320 px header fades in at `v ≥ 580`. Nothing is resized.

## 7. One timer for every countdown

```gdscript
## TimerHub.gd - autoload: ONE 1 s tick for every visible countdown (core-loop §4.6).
extends Node
var server_offset := 0.0            # set at each sync (cloud-forge)
var _ends := {}                     # Label -> end_unix

func _ready() -> void:
	var t := Timer.new()
	t.wait_time = 1.0
	t.timeout.connect(_tick)
	add_child(t)
	t.start()

func watch(label: Label, end_unix: float) -> void:
	if not _ends.has(label):
		label.tree_exiting.connect(func(): _ends.erase(label))
	_ends[label] = end_unix
	_render(label)

func _tick() -> void:
	for l: Label in _ends.keys():
		if l.is_visible_in_tree():
			_render(l)

func _render(l: Label) -> void:
	var left := ceili(_ends[l] - (Time.get_unix_time_from_system() + server_offset))
	l.text = UIFormat.duration(left) if left > 0 else tr("TIMER_CONFIRMING")   # never "0 s" while running
```

`UIFormat.duration()` gives "1 h 12 m" / "4 m 05 s", rounded up (core-loop §4.5).

## 8. Status bubbles over buildings

```gdscript
## BubbleLayer.gd - root Control of L05_WorldUI. Moves bubbles only when the camera moved.
extends Control
@export var cam: Camera3D
var _last := Transform3D()

func _ready() -> void:
	get_viewport().size_changed.connect(func(): _last = Transform3D())   # force a re-place

func _process(_dt: float) -> void:
	var xf := cam.global_transform
	if xf.is_equal_approx(_last):
		return
	_last = xf
	for b: Control in get_children():
		var anchor: Vector3 = b.get_meta("anchor")       # the building's ui_bubble empty (hud.md §7)
		b.visible = not cam.is_position_behind(anchor)
		if b.visible:
			var p := cam.unproject_position(anchor)
			b.position = (p - Vector2(b.size.x * 0.5, b.size.y + 24.0)).round()   # whole px: no shimmer
```

Caps, merging (< 120 px) and priority run after placement, once per camera change. Verify once
that a bubble on a known building lines up at 1080×1920 AND in a 1440×3200 window.

## 9. Text that fits: fit-down, wrap, ellipsis

```gdscript
## UIText.fit_label - shrink in 2 px steps to the minimum, then wrap to max_lines, then ellipsis.
static func fit_label(label: Label, max_px: int, min_px: int, max_lines := 1) -> void:
	var font := label.get_theme_font("font")
	var width := label.size.x * max_lines             # an approximation of the lines' width
	var px := max_px
	while px > min_px and font.get_string_size(label.text, HORIZONTAL_ALIGNMENT_LEFT, -1, px).x > width:
		px -= 2
	label.add_theme_font_size_override("font_size", px)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART if max_lines > 1 else TextServer.AUTOWRAP_OFF
	label.max_lines_visible = max_lines
	label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	if font.get_string_size(label.text, HORIZONTAL_ALIGNMENT_LEFT, -1, px).x > width:
		label.tooltip_text = label.text               # the long-press tooltip shows it; layout_audit counts it
```

Minimums: buttons 50 → 42, body 42 → 36, digits never below 32 (components.md §1). Check on 4.7
that the ellipsis lands on the last wrapped line; if not, trim the string by measuring it.

## 10. Virtual lists (> 60 rows)

```gdscript
## VirtualList.gd - fixed row height, a pool of (visible + 4) rows placed by hand.
extends ScrollContainer
@export var row_scene: PackedScene
@export var row_h := 144
var data: Array = []
var _content := Control.new()
var _pool: Array[Control] = []

func _ready() -> void:
	scroll_deadzone = 24                              # a scroll never becomes a tap
	_content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_child(_content)
	get_v_scroll_bar().value_changed.connect(func(_v): _layout())
	resized.connect(_layout)

func set_data(rows: Array) -> void:
	data = rows
	_content.custom_minimum_size = Vector2(0, rows.size() * row_h)
	_layout()

func _layout() -> void:
	var need := ceili(size.y / row_h) + 4
	while _pool.size() < need:
		var r: Control = row_scene.instantiate()
		_content.add_child(r)
		_pool.append(r)
	var first := maxi(0, scroll_vertical / row_h - 2)
	for i in _pool.size():
		var idx := first + i
		var r := _pool[i]
		r.visible = idx < data.size()
		if r.visible:
			r.position = Vector2(0, idx * row_h)
			r.size = Vector2(size.x, row_h)
			r.call("bind", data[idx])                 # each row scene implements bind(item)
```

Ship it with a rebind only when a row's index changes. Rankings pin the own row outside the list;
chat-forge's variable-height list follows its ui.md §11.

## 11. Focus, screen readers, text scale

- **Focus**: `FOCUS_ALL` on interactive controls, `FOCUS_NONE` on decoration; `first_focus` per
  panel; `focus_neighbor_*` on grids; the ring is the Theme's `focus` StyleBox (4 px GILT_LIT).
- **Screen readers**: Godot 4.5 added AccessKit screen-reader support with accessibility
  properties on Control. Confirm the names on 4.7, then name every icon-only button from an l10n
  key ("Mail, 3 unread"); `a11y_audit` lists unnamed controls.
- **Text scale** (100 / 115 / 130%): scale the Theme's font sizes, never `content_scale_factor`
  (it grows the chrome too and breaks the HUD plan).

```gdscript
## base = {"Label": {"font_size": 42}, "ButtonPrimary": {"font_size": 50}, ...} captured at boot
## with theme.get_type_list() and theme.get_font_size_list(type).
static func apply_text_scale(theme: Theme, base: Dictionary, k: float) -> void:
	for type in base:
		for size_name in base[type]:
			theme.set_font_size(size_name, type, roundi(base[type][size_name] * k))
	theme.default_font_size = roundi(42 * k)
```

## 12. Pseudolocalization and the +40% pass

```
internationalization/pseudolocalization/use_pseudolocalization = true
internationalization/pseudolocalization/expansion_ratio = 0.4       # the +40% pass; 1.0 for the short-label stress pass
internationalization/pseudolocalization/replace_with_accents = true # catches clipped ascenders and descenders
internationalization/pseudolocalization/prefix = "["                # a missing bracket = clipped text
internationalization/pseudolocalization/suffix = "]"
internationalization/pseudolocalization/fake_bidi = false           # true only for an RTL pass
```

At runtime: `TranslationServer.pseudolocalization_enabled = true`, then
`TranslationServer.reload_pseudolocalization()`. A string that does not change was never passed
through `tr()`: the pass lists untranslated strings for free. Expansion by English length (IBM
globalisation guidance): ≤ 10 characters +100–200%, 11–20 +80–100%, 21–30 +60–80%, 31–50
+40–60%, 51–70 +31–40%, > 70 +30%. The 0.4 pass: 0 overflows. The 1.0 pass: fit-down and
ellipsis allowed, counted. RTL (if shipped): locale direction on text containers only.

## 13. Draw calls, atlases, fonts

- **Measure**: `Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)` with the
  HUD shown minus hidden = the HUD's cost. Budgets (PROPOSAL): HUD at rest ≤ 40, full screen
  ≤ 80, scrolling list ≤ 100. `RENDER_TEXTURE_MEM_USED` for the texture budget (icons.md §7).
- **Batching**: draw-order neighbours sharing texture and material batch. Breakers: a texture
  switch (atlas everything), another material or shader, `clip_contents` (scroll areas only),
  `BackBufferCopy`, a Label with another font or outline between icons of one atlas.
- **No real-time blur** behind panels on mobile: the INK scrim costs nothing.
- **Fonts**: the display face with `multichannel_signed_distance_field = true` (scales 60–96 px
  and in ceremonies); the text face as a normal dynamic font (sharper at 32–42 px); l10n-forge's
  `fallbacks` on the FontFile, so a missing glyph never shows as a box.
- **No `_process` in UI nodes** except the bubble layer (§8) and active tweens.

## 14. Godot traps (each one cost somebody a day)

| Trap | Symptom | Fix |
|---|---|---|
| A decorative `TextureRect` or `Panel` left at `MOUSE_FILTER_STOP` | taps "do nothing" in one area | `MOUSE_FILTER_IGNORE` on all decoration; the probe lists visible STOP controls with no input handler |
| A 96 px visual button used as its own hit rect | mis-taps; `ux_touch_probe` fails | a 132/144 px parent Control is the hit rect, and the visual sits centred with IGNORE. Prefer this to a `_has_point()` override, which layout tools cannot see |
| Tweening `position` of a child inside a Container | it snaps back on the next sort | put the moving child in a plain Control wrapper (§5) |
| Mirroring with `layout_direction = RTL` | English punctuation at the wrong end | swap anchors (§3) |
| `get_display_safe_area()` on desktop | insets 0, notch bugs unseen | `debug_insets` in the sweep (§3) |
| `quit_on_go_back` left true | the back button quits from any screen | router `_ready()` (§4) |
| Fonts without fallbacks | boxes instead of CJK or Cyrillic | FontFile `fallbacks` (l10n-forge) |
| A Timer or `_process` per countdown label | 16 ticking nodes, CPU at rest | the TimerHub (§7) |

Checklist for any UI code change:
- [ ] Opens through `UIRouter.open(route)`; back handled; focus returns; tweens via the panel base, no `await` before input.
- [ ] SafeArea tested with `debug_insets`; no `theme_override_*` except computed values; decoration at `MOUSE_FILTER_IGNORE`.
- [ ] Draw calls measured; icons from atlases; no timer `_process`; pseudo-0.4 and 130% screenshots attached.
