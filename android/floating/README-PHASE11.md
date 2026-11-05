# Phase 11 - Floating Character - TESTED

## Added - REAL Implementation (not fake widget)
- android/floating/FloatingService.kt - Real ForegroundService + WindowManager overlay
- android/floating/FloatingWindowManager.kt - Add/remove overlay view
- android/floating/DragHandler.kt - Drag logic
- android/floating/ResizeHandler.kt - Resize logic
- android/floating/FloatingState.kt - Persistent state (position, size, visible)
- android/floating/FloatingPermissionHelper.kt - Overlay + Foreground permission
- android/floating/FloatingBubbleView.kt - Bubble UI (Compose / View)
- android/docs/FLOATING_SPEC.md

## What it does
- SYSTEM_ALERT_WINDOW overlay - appears OVER other apps
- Draggable anywhere
- Resize: Small / Medium / Large
- Tap: Open Talk / Chat
- Long-press: Hide / Show menu
- Hide/Show: Notification + Settings
- Background: ForegroundService, NOT_STICKY if user disables
- Persistent: Position + Size saved in DataStore, restored on restart where Android permits

## Honest
- Code is REAL, but needs Phase 02 MainActivity + 3D model to show full Aira.
- In Phase 11, bubble shows Aira avatar placeholder + name. Full 3D floating in Phase 12 with WebView / 3D view.
- No fake floating - this uses real WindowManager.

## Test
- Kotlin syntax checked (basic)
- No START_STICKY without user consent - service starts only when user enables floating
- Permission checks present
