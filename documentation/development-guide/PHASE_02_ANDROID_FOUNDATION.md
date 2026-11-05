# Phase 02 — Android Foundation

**Status**: Implemented (structure + basic working overlay service)

## What was created

### Project structure
- Full modular folder tree for all 16 modules
- Android multi-module Gradle project (`:app` + `:core`)

### Android application foundation
- `H1Application` — notification channels, global entry
- `MainActivity` — basic control shell with overlay permission + start/stop buttons
- `FloatingCharacterService` — real `SYSTEM_ALERT_WINDOW` overlay + foreground service
  - Draggable
  - Persistent notification
  - START_STICKY
- `CompanionForegroundService` — core companion process placeholder
- `BootReceiver` — ready for future auto-restore
- `PermissionManager` — centralized runtime permission helpers

### Resources
- Dark Material 3 theme
- Main activity layout
- Floating character placeholder layout + drawable
- Notification icon
- Backup / data-extraction rules (excludes sensitive memory)

### Configuration
- `minSdk 26`, `targetSdk 35`, `compileSdk 35`
- Kotlin 2.0 + Android Gradle Plugin 8.7
- ViewBinding enabled
- ProGuard rules prepared

## Important notes for Termux / on-device development

1. You still need a proper Android SDK + Gradle wrapper to build the APK.
2. On a pure Termux environment you will typically:
   - Use Git to push this structure to GitHub
   - Use GitHub Actions to build the APK
   - Or install Android SDK command-line tools inside Termux (advanced)
3. The floating overlay **requires** the user to grant “Display over other apps” permission.
4. Foreground service notification is mandatory on modern Android.

## Next recommended step (after your approval)

Phase 03 — Original anime character definition  
(character identity, appearance description, personality base, technical model requirements)

## How to test the foundation (once built)

1. Install the debug APK
2. Open the app
3. Tap “Grant Overlay Permission” → allow in system settings
4. Tap “Start Floating Character”
5. The placeholder character should appear over other apps and be draggable
6. Tap “Stop Floating Character” to remove it
