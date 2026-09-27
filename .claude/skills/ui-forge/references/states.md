# States — no blank panel, no raw error, no lost tap

Every list and every screen that shows server data has more states than "loaded". The genre
ships blank lists and spinners that never end. Our rule: each state has **art, one line, one
action**, and the player always knows what the game is doing. Copy lines are l10n keys
(l10n-forge). The wording below is English working text; story-forge owns the voice.

## 1. The state machine

```
            ┌──────────── retry ────────────┐
            ▼                               │
 IDLE → LOADING ──► READY ──► STALE (age > limit) ──► LOADING (refresh)
            │  └──► EMPTY                   │
            ├─────► ERROR ──────────────────┘
            └─────► OFFLINE (no connection) ──► LOADING when the connection returns
 READY + an action in flight → BUSY (that control only)      LOCKED = a gate, not a failure
```

| State | Means | Shows | Action |
|---|---|---|---|
| LOADING | a request is in flight and nothing cached can be shown | nothing for 150 ms, then skeleton rows | none (Cancel after 10 s) |
| READY | data shown | the content | the screen's own |
| EMPTY | the server answered, and there is nothing | art + why + what brings content | one action, or the time something will appear |
| ERROR | the request failed after retries, or the server refused | art + what happened + what to do + a small code | Retry (or the fix) |
| OFFLINE | no connection | the cached content (marked) or the offline art | automatic: it returns when the connection does |
| STALE | cached content older than its limit | the content + "Updated 12 min ago" | pull to refresh (rate-limited) |
| BUSY | one control's action waits for the server | that control in its Busy state | none: the rest of the screen stays live |
| LOCKED | a progression gate | padlock art + the requirement + where it is | Go to the requirement |
| FIRST_TIME | the screen opens for the first time | one ≤ 14-word card (onboarding-forge) | Got it / skip after 3 s |

## 2. Timing thresholds

| Elapsed since the request | What the player sees |
|---|---|
| 0–150 ms | the previous content, or the empty frame of the screen: no spinner (a spinner flash reads as a glitch) |
| 150 ms | skeleton rows in the list's real row height (parchment at 40%, no text); a shimmer of 1.2 s period, off with reduced motion |
| 3 s | a line under the skeleton: "Waiting for the courier…" |
| 10 s | a Cancel button beside that line |
| 15 s | timeout → ERROR |
| retries | idempotent reads only, automatically: 1 s, 2 s, 4 s (3 tries, inside the 15 s) |

**Spends, claims, marches and purchases are never retried automatically.** They go through the
server's idempotency key (mail-forge claim protocol; cloud-forge), and the Busy control shows
the true result when it arrives. A second tap during Busy does nothing.

## 3. What each state looks like

**Art**: a still life of ONE object, 256–320 px, Blender-made through icons.md (an empty
weapon rack, a quiet bell rope, a rolled map with a broken seal). It is never a blank frame,
never a line glyph, never a sad face. Each list has its own object (§6), so empty states
teach what the list is for.

**Copy**: one line of what happened, from the player's side, ≤ 12 words at 42 px. Then one line
of what to do or when it changes. The technical code goes last, at 32 px in INK 70%
("E-1042 · realm 12"), so support can find it. Never "Error", "Failed", "null" or
"No data" alone.

**Placement**: centred in the list area, art above text, the action button (M) below it,
≥ 48 px above the footer.

| State | Example line (English working text) | Button |
|---|---|---|
| ERROR (network) | "The courier did not come back. Your orders are safe." | Retry |
| ERROR (server refused) | "The Hall refused this: you left the alliance 2 h ago." | Close |
| ERROR (version) | "The realm has changed. Update the game to continue." | Update (opens the store) |
| OFFLINE banner | "No road to the realm. Your castle keeps working." | — |
| BUSY too long (> 15 s) | "Still waiting for the Hall. We will tell you when it answers." | Close (the action continues on the server) |
| LOCKED | "Opens at Keep tier 5 (you are at tier 3)." | Go |

## 4. Offline and optimistic rules

1. **Offline banner**: an IRON band of 764 × 72 at the top of the clear world window
   (x 152, y 316; hud.md §3): the offline line + a connection icon. Toasts move below it
   (y 404). When the threat banner shows (hud.md §9), the offline band goes under it. Spends, claims, marches and purchases are disabled
   with the reason "Needs the realm road". Cached screens stay browsable, marked "Saved
   14:20".
2. **Optimistic actions** (shown at once, confirmed later, rolled back with a toast on
   refusal): help all, marking mail read, chat send (chat-forge: the row shows ≤ 1 frame
   after the tap), UI settings, bookmarks.
3. **Never optimistic**: gem spends, purchases, claims, marches, starting or finishing plates,
   alliance joins and leaves. The server is the truth (design-forge rule 5). The Busy state
   covers the wait, usually < 300 ms.
4. **Timers survive offline**: every plate is `(start_unix, duration_s)`, so the tracker keeps
   counting from the last server offset (core-loop §2 rule 3, §4.6). A plate that ends
   offline shows "Done — confirming" until the server confirms.
5. **Rollback**: when an optimistic action is refused, the UI returns to the server state in
   one step (no animation back through intermediate values) and shows a toast with the reason.

## 5. Purchases (shop-forge owns billing)

| State | Shows |
|---|---|
| Pending (store sheet open) | the offer card stays, Buy in Busy, Close still active |
| Paid, not yet granted | "Payment received — delivering…" (grant ≤ 10 s normally) |
| Granted | toast + the goods count-up; the offer's limit updated |
| Failed or cancelled at the store | back to the card, no error art: "Purchase cancelled." |
| Pending for days (e.g. cash payment methods) | a row in Settings → Spending "Waiting for payment" |
| Restored or refunded | a mail (mail-forge) explains; the UI shows the new balance |

## 6. The empty-state catalogue (every list in the game)

| List (route) | Data owner | Empty-state object | Line (why + what brings content) | Action |
|---|---|---|---|---|
| Tracker drawer (`plates/*`) | gameplay-forge | — (never empty: idle plates show "Idle") | — | — |
| Research nodes (`research/*`) | gameplay-forge | a closed book with a ribbon | "Every study at this desk is done. More open at Scriptorium tier 4." | Go |
| Muster tiers (`muster/*`) | gameplay-forge | an empty weapon rack | "This line trains at the Barracks. Build it to start." | Go |
| Infirmary rows | gameplay-forge | folded clean linen | "No one is wounded. Beds: 1,200." | — |
| Lords roster | commander-forge | — (never empty: the starting lord) | — | — |
| Gear for a slot | commander-forge | an empty armour stand | "No gear for this slot yet. The smithy forges it." | Go to the smithy |
| Bag (`bag/*`) | gameplay-forge | an open empty satchel | "Hourglasses come from daily chests and the writ." | Chronicle |
| Alliance home (no alliance) | gameplay-forge | a bare banner pole | "You ride alone. Allies cut every timer." | Join · Create |
| Help requests | gameplay-forge | a quiet bell rope | "No one needs help right now." | — |
| Gifts | gameplay-forge | an empty gift shelf | "Gifts arrive when allies finish great works." | — |
| Rallies | battle-forge | a cold fire basket | "No rally is gathering. Officers start rallies from the map." | — |
| Members (search result) | gameplay-forge | a closed roll | "No member by that name." | Clear search |
| Herald's Board | liveops (design) | never empty (21 days ahead) | if it is: "The herald is late. The Board refreshes at 00:00 UTC." | Retry |
| Event milestones | gameplay-forge | a milestone post | "Score to reach the first mark: 200 points." | How to score |
| Rankings | cloud-forge | a blank tally board | "No scores yet this season. The first update comes in 15 min." | — |
| Realm search | world-forge | a rolled map | "No place by that name or those coordinates." | Clear |
| Bookmarks | world-forge | a map pin in its box | "Tap a place, then the pin, to keep it here." | — |
| Mail folders | mail-forge | (mail-forge's catalogue) | — | — |
| Chat channels | chat-forge | (chat-forge's catalogue) | — | — |
| Reports | report-forge | (report-forge's catalogue) | — | — |
| Blocked players | chat-forge | an unlatched gate | "You have blocked no one." | — |
| Shop shelf | shop-forge | an empty market stall | "This shelf restocks on Monday (2 d 4 h)." | — |
| Daily orders (all done) | gameplay-forge | a sealed scroll | "Today's orders are done. New ones in 7 h 12 m (00:00 UTC)." | — |

The `states_probe` (qa.md §2) opens every route in this table with a fake empty answer, a fake
error, a 16 s delay and the offline flag, and saves a screenshot of each: 4 states × N routes.

## 7. Failure modes and checklist

| Fails when | Symptom | Caught by |
|---|---|---|
| A spinner shows for fast loads | flicker on every open | [ ] frame capture: no loading visual before 150 ms |
| A spinner never ends | the player kills the app | [ ] `states_probe` 16 s delay → ERROR at 15 s |
| A spend is retried automatically | a double purchase or a double spend | [ ] a server log in the probe: one request per tap |
| An empty list with no art or line | "is it broken?" | [ ] `states_probe` screenshots |
| A raw code alone ("Error 500") | support tickets without context | [ ] a grep of the l10n table for bare codes |
| An optimistic claim | the reward shows, then vanishes | [ ] review against §4.3 |
| The offline banner covers the rail, the tracker or a toast | the player loses the HUD when they need it most | [ ] `layout_audit` overlap list with the offline flag on |

- [ ] Every list in §6 has its object, its line and its action (or "—" by design).
- [ ] Loading shows nothing before 150 ms, a skeleton after, a line at 3 s, Cancel at 10 s, error at 15 s.
- [ ] Only idempotent reads retry automatically.
- [ ] Offline: banner, disabled spends with the reason, cached content marked.
- [ ] Busy is per control; the rest of the screen stays live.
- [ ] Purchase states follow §5.
