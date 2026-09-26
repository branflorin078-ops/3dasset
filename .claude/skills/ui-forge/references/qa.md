# QA — the battery, the measurements, the critique, the evidence

A UI change is done when the harnesses say so, the numbers are pasted, and the screenshots were
looked at. The owner's harnesses exist and run on their machine. Their exact verdict wording is
quoted from a real run, never from memory. The only line known here is
`ASPECT SWEEP OK - 6 shapes, 0 faults`. The new probes in §2 are requests to qa-forge, with
PROPOSED verdict lines.

## 1. The battery for UI work

Godot on the owner's machine is `$g` (game-director §2). The windowed suites run at
`--resolution 1080x1900`, as `session_audit` does. The script paths other than `core/*.gd` are
to be confirmed.

| Harness | Mode | ui-forge relies on it for | Run when |
|---|---|---|---|
| `layout_audit` | windowed | clipped or overflowing text, overlaps, min sizes, off-screen controls | every UI change |
| `w1f_aspect_sweep` | windowed | the 6 shapes: no fault in any HUD zone or panel; verdict `ASPECT SWEEP OK - 6 shapes, 0 faults` | every UI change |
| `ux_touch_probe` | windowed | hit rects ≥ 132 / 144 px, no overlap, no target within 120 px of a corner, buy-button isolation | every change to a control |
| `ux_flow_probe` | windowed | tap counts of the core actions (architecture.md §3), marks at open, pop-up rules, no offer on war screens, dead ends | every change to a route or the HUD |
| `a11y_audit` | windowed | focus order, flashing, reduced motion, colour-alone coding, screen-reader names | every UI change |
| `mm_probe`, `map_trap_probe` | windowed | the realm HUD over the map, input traps at the castle ⇄ realm switch | HUD or realm overlay changes |
| `menu_test` | headless | no title menu; the live realm resumes into the world | router or boot changes |
| `contrast_test` | headless | theme colour pairs against the targets in components.md §2 | Theme changes |
| `core/session_audit.gd` | windowed 1080×1900 | the check-in: ≤ 30 taps, ≤ 5 min, 0 idle plates at exit (core-loop §11) | HUD, tracker, building card |
| the core gate (game-director) | both | nothing else broke | after every change set |

If a harness does not check what the middle column needs, that is a qa-forge request (§2), not a
reason to skip the check. Until then, do the check by hand and paste the numbers.

```powershell
& $g --path godot --resolution 1080x1900 --script res://<path to confirm>/layout_audit.gd
& $g --path godot --resolution 1080x1900 --script res://<path to confirm>/w1f_aspect_sweep.gd
& $g --path godot --resolution 1080x1900 --script res://core/session_audit.gd
```

## 2. Probes and checks to request from qa-forge (PROPOSED verdict lines)

| Probe or check | What it does | Verdict line (PROPOSED) |
|---|---|---|
| `ui_route_probe` | opens every route in architecture.md §5 with fake data and stale ids; checks depth, parent, blank surfaces | `UI ROUTES OK - 64 routes, max depth 3, 0 blank, 0 orphan` |
| core-tap pass in `ux_flow_probe` | walks the 20 core actions from HUD rest | `CORE TAPS OK - 20 actions, max 3 taps, 0 over budget` |
| marks pass in `ux_flow_probe` | counts marks on the session-open screenshot of the median save | `MARKS OK - 3 at open, 1 event badge, 0 on offers` |
| `states_probe` | every list in states.md §6 × empty, error, 16 s delay, offline | `STATES OK - 23 lists x 4 states, 0 blank, 0 raw codes` |
| pseudo pass in `layout_audit` | pseudolocalization at 0.4 (must be clean) and 1.0 (counted) | `PSEUDO 0.40 OK - 0 overflow, 12 fit-down, 0 untranslated` |
| text-scale pass in `layout_audit` | Theme sizes × 1.30 | `TEXT 130 OK - 0 overflow` |
| `ui_perf_probe` | opens each route twice; draw calls, frame times, first-open and warm-open hitches | `UI PERF OK - HUD 36 calls, worst screen 71, first open <= 1 hitch, warm 0` |
| physical line in `ux_touch_probe` | converts hit rects to mm with the device dpi (hud.md §10.2) | `TOUCH OK - min hit 132 px / 7.0 mm, 0 overlaps, 0 corner targets` |
| theme grep (CI script) | `theme_override_` in shipped `.tscn` files, except SafeArea and fit-down | `THEME OK - 0 overrides in shipped scenes` |
| `icon_check.py` (icons.md §5) | per icon: fill, value groups, value range, lit rim | `ICON <name> {...} PASS` |
| `shot_contrast.py` (§5) | per text rect of a screenshot | `CONTRAST OK - 0 label(s) below target` |

## 3. Shapes × passes — the screenshot matrix

Every changed screen is captured in these cells. Screenshots go to `art/ui_forge/<id>/`, named
`<route>_<shape>_<pass>.png`.

| Pass \ shape | 9:16 | 9:19.5 | 9:20–21 | 3:4 | 10:16 | foldable |
|---|---|---|---|---|---|---|
| default | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| pseudo 0.4 | ✔ | | ✔ | | | |
| text 130% | ✔ | | ✔ | | | |
| Hand = left | ✔ | | | ✔ | | |
| reduced motion (frame capture) | ✔ | | | | | |
| offline flag | ✔ | | | | | |
| colour-blind sims (`cb_sim.py`) | ✔ | | | | | |
| fake insets (top 132, bottom 63) | ✔ | ✔ | ✔ | | | |

## 4. Frame-time capture

Open each changed route twice on the reference phone (ship-forge names it), or in a windowed
run with the frame limiter off. Record the maximum frame time in the 500 ms after the tap, the
count of frames > 16.7 ms, and the draw calls at rest once the panel has settled. Targets:
motion.md §5. A route with a first-open hitch over 33 ms gets pre-instancing or threaded
loading (motion.md §5.1–2), never a longer tween to hide it.

## 5. Measurement scripts (Python 3; Pillow + numpy for images; tested 2026-09-26)

**Text contrast on a screenshot.** Rects come from `layout_audit`'s dump (ask qa-forge for a
JSON export of Label rects and font sizes), or are written by hand.

```python
"""shot_contrast.py <screenshot.png> <rects.json> - rects: [{"id": "...", "rect": [x, y, w, h], "px": 42, "bold": false}, ...]"""
import sys, json, numpy as np
from PIL import Image

def lum(rgb):
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c @ np.array([0.2126, 0.7152, 0.0722])

img = np.asarray(Image.open(sys.argv[1]).convert("RGB")); fails = 0
for r in json.load(open(sys.argv[2])):
    x, y, w, h = r["rect"]; L = lum(img[y:y + h, x:x + w].reshape(-1, 3))
    bg = float(np.median(L))                                   # background = the majority of the rect
    ink = min(float(np.percentile(L, 3)), float(np.percentile(L, 97)), key=lambda v: -abs(np.log((v + .05) / (bg + .05))))
    cr = (max(ink, bg) + 0.05) / (min(ink, bg) + 0.05)
    need = 3.0 if r.get("px", 42) >= 64 or (r.get("bold") and r.get("px", 42) >= 50) else 4.5
    ok = cr >= need; fails += not ok
    print(f"{r['id']:<28} {cr:5.2f}:1 need {need}  {'ok' if ok else 'FAIL'}")
print(f"CONTRAST {'OK' if fails == 0 else 'FAIL'} - {fails} label(s) below target")
```

Test result: INK body text on PARCHMENT → `12.66:1 ok`; GILT text on PARCHMENT → `1.74:1 FAIL`,
the same values as the palette table in components.md §2.

**Colour-blind screenshots** for the review (the same matrices produced components.md §4):

```python
"""cb_sim.py <screenshot.png> - writes <name>_protan/_deutan/_tritan.png (Machado 2009, severity 1.0)."""
import sys, os, numpy as np
from PIL import Image
M = {"protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
     "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
     "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}
src = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float64) / 255.0
lin = np.where(src <= 0.04045, src / 12.92, ((src + 0.055) / 1.055) ** 2.4)      # simulate in linear light
base = os.path.splitext(sys.argv[1])[0]
for kind, m in M.items():
    out = np.clip(lin @ np.array(m).T, 0, 1)
    enc = np.where(out <= 0.0031308, out * 12.92, 1.055 * out ** (1 / 2.4) - 0.055)
    Image.fromarray((enc * 255 + 0.5).astype(np.uint8)).save(f"{base}_{kind}.png")
    print("CB", kind, f"{base}_{kind}.png")
```

**Palette check**: reproduces every contrast ratio in components.md §2 and every ΔE in §4.
Run it again whenever a token or an accent colour changes:

```python
"""palette_check.py - WCAG contrast of palette pairs + CIE76 dE after Machado 2009 colour-blind simulation."""
import itertools, math
C = dict(PARCHMENT="#E8D9B5", INK="#1E1712", OAK="#4A2E1B", IRON="#3B4048", GILT="#C9A04C", GILT_LIT="#E0BC6A",
         WAX="#8A1F24", infantry="#B4432E", spearmen="#8B8F95", archers="#4F7A4A", crossbows="#6D8AA8",
         cavalry="#C9A76A", sound="#6A8FD8", fine="#8F6ADB", masterwork="#E8A33C")
M = {"protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
     "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
     "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}
lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
rgb = lambda h: [lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5)]          # linear RGB
Y = lambda v: 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def ratio(a, b):
    hi, lo = max(Y(rgb(C[a])), Y(rgb(C[b]))), min(Y(rgb(C[a])), Y(rgb(C[b]))); return (hi + .05) / (lo + .05)
def lab(v):                                                                  # linear RGB -> CIELAB (D65)
    x = (0.4124 * v[0] + 0.3576 * v[1] + 0.1805 * v[2]) / 0.95047; y = Y(v)
    z = (0.0193 * v[0] + 0.1192 * v[1] + 0.9505 * v[2]) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))
def see(name, kind):
    v = rgb(C[name])
    return v if kind == "normal" else [min(max(sum(M[kind][i][j] * v[j] for j in range(3)), 0), 1) for i in range(3)]
for fg in ("INK", "OAK", "WAX", "PARCHMENT", "GILT", "GILT_LIT", "infantry", "cavalry", "fine"):
    print(f"{fg:<10}", " ".join(f"{bg}:{ratio(fg, bg):5.2f}" for bg in ("PARCHMENT", "OAK", "INK", "IRON")))
for a, b in [("spearmen", "crossbows"), ("infantry", "archers"), ("archers", "crossbows"), ("sound", "fine"),
             ("GILT", "masterwork"), ("GILT", "cavalry"), ("WAX", "infantry")]:
    print(f"dE {a}/{b}", [round(math.dist(lab(see(a, k)), lab(see(b, k))), 1) for k in ("normal", "protan", "deutan", "tritan")])
```

These three scripts and `icon_check.py` are PROPOSED as `ui-forge/tools/` (the lead installs
them with a test). Until then they live beside the screenshots they judge.

## 6. The screen critique — 14 points (inspect every screenshot)

1. **One question**: a new player can say what this screen is for within 3 s.
2. **Hero art at its size**: ≥ 30% of the area for a thing-screen, ≥ 40% of the height for the
   building card, ≥ 96 px art in every list row. The art holds the highest local contrast on
   the screen: the focal point is the art, not the chrome.
3. **One Primary** in the footer's hand-side slot, with a verb label. Danger isolated. Premium
   two-step.
4. **Thumb**: overlay the zone map (hud.md §2) on the screenshot. Frequent actions sit in the
   easy zone.
5. **Taps**: every core action it touches is within budget, measured.
6. **Text**: sizes on the scale, ≤ 3 sizes + digits, `shot_contrast.py` clean, no gilt text on
   parchment, scrims where text sits on art.
7. **Not colour alone**: look at the deutan and protan screenshots. Every coded meaning still
   reads.
8. **Chrome vs art**: chrome no brighter than GILT_LIT, no glow on chrome, no detail under
   3 px, patch margins ≤ 1/3.
9. **Marks**: only allowed sources; count at open within budget.
10. **Money-law**: no war imagery on or behind buy or gem controls; Close = Buy height,
    visible from frame 1; no offer on a war screen; no pulsing countdown.
11. **States**: every state present, each with art, one line and one action.
12. **Motion**: tokens only; input live during tweens; the reduced-motion capture shows fades
    only.
13. **Localisation**: the pseudo-0.4 screenshot is clean; no text inside art; the untranslated
    list is empty.
14. **Shapes**: all 6 shapes, Hand = left, fake insets. No overlap, no clipping, no target in
    a corner.

Fix the first failing point, re-capture, repeat. A screen that fails the same point 3 times goes
back to layout (step 4 of the workflow), not to more polish.

## 7. Evidence contract and lessons

Every UI delivery pastes: the harness verdict lines word for word (§1–2); the screenshot folder
and the matrix cells filled (§3); tap counts; draw calls and first-open times (§4); the
`CONTRAST` line; the states list; and, for icons, every `ICON … PASS` line with its survival
sheet. "Looks fine" is not evidence. A number without the run that produced it is not
evidence.

**Lessons and standing conflicts** (append-only, newest last):

1. **UI-002 — a nine-slice border swallowed its button.** A frame with a 58 px border shipped
   on a 60 px button, and the button's content vanished (game-art-director ui-icons.md).
   Rule: patch margin ≤ 1/3 of the smallest display size, and ship chrome near its display
   size (components.md §3.1–2).
2. **Measured while writing this skill (2026-09-26), not yet seen in the game**: GILT text on
   PARCHMENT is 1.74:1, and every troop line accent fails 4.5:1 as text on PARCHMENT
   (1.63–3.97:1). The warm "medieval" choice is the unreadable one. Rarity Sound vs Fine is
   ΔE 10.8 for deuteranopes. These are the first things to check on the shipped Theme.
3. **Sibling proposals below these minimums (to settle with the owners)**: chat-forge ui.md §1
   proposes 34 px message text, 28–26 px tab labels and a 120 px ticker hit. This skill's
   minimums are 36 px for sentences, 32 px for any text and a 132 px hit. The stricter number
   applies until the owner rules (SKILL.md reference frame).
