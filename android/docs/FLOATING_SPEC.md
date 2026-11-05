# Floating Spec - Phase 11 - REAL Overlay

## Features
- Android floating overlay - OVER other apps, NOT in-app widget
- Draggable - DragHandler, position saved
- Resize - Small 72dp / Medium 110dp / Large 160dp
- Tap to Talk - Opens Chat / Voice
- Long-press - Hide / Resize / Settings (Phase 13)
- Hide/Show - Notification + Settings + Long-press
- Background - ForegroundService, NOT_STICKY, notification shows "Aira H1 is here"
- Persistent - Position + Size + Enabled saved, restored after reboot ONLY if user enabled Restore

## Permissions (Legit)
- SYSTEM_ALERT_WINDOW - Overlay, user must grant in Settings
- FOREGROUND_SERVICE - Background
- POST_NOTIFICATIONS - Show floating notification

## How to Enable (User)
1. App > Settings > Floating Character > Enable
2. Overlay permission Settings opens > Allow H1
3. Back to app > Floating appears
4. Drag anywhere, Tap to talk, Long-press to hide

## How to Disable
- Long-press bubble > Hide
- OR Notification > Hide
- OR Settings > Floating > Off

## Privacy
- Floating does NOT record screen
- Floating does NOT read other apps
- Mic only when user taps Talk

## What is NOT yet
- Full 3D floating - Phase 12 (WebView 3D)
- Voice in bubble - Phase 07 + 13 integration

Next: Phase 12 Full-screen 3D World
