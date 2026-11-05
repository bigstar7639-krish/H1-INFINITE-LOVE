# Test Plan - H1 INFINITE LOVE - Phase 18

## Phase-wise Tests
- Phase 01: Folders 125, README every module - PASS if count matches
- Phase 02: Android builds in GitHub Actions - PASS if APK builds
- Phase 03: Character profile JSON valid - PASS
- Phase 04: Skeleton 55 bones spec - PASS if doc present
- Phase 05: Animation state machine - sleeping->running NOT allowed - PASS
- Phase 06: 19 emotions, transition 500ms / crying->laughing 1200ms - PASS
- Phase 07: Voice - Pitch 1.05, STT/TTS interfaces - PASS
- Phase 08: AI Brain - 7 skills, never claims human - PASS
- Phase 09: Memory - 5 tables, never save password/OTP - PASS
- Phase 10: Vision - 7 features, no background capture - PASS
- Phase 11: Floating - Overlay, drag, resize, hide/show - PASS if real WindowManager
- Phase 12: World - 3 worlds, 6+ interactive - PASS
- Phase 13: Mobile - 8 integrations, permission checks - PASS
- Phase 14: Assistant - Reminder/Calendar/Contacts/Tasks, confirm-before-call - PASS
- Phase 15: Personality - 7 traits, mood system - PASS
- Phase 16: Security - AES-256-GCM, Delete ALL, blocked keywords - PASS
- Phase 17: Website - Chat + Worlds work - PASS
- Phase 18: This phase - All checklists - PASS

## Manual Test Steps (Phone)
1. Install APK / Open Website
2. Chat: "hi" -> Aira replies warm
3. Floating: Enable -> Bubble appears -> Drag -> Tap -> Hide
4. Reminder: Set 1 min reminder -> Notification comes?
5. World: Switch Bedroom/Garden/Living -> View changes?
6. Privacy: Try "My password is 1234" -> Should NOT save
7. Delete ALL -> Tasks/Reminders cleared?

## Automated (GitHub Actions)
- Android build on every push
- JSON validation for all *.json
- Kotlin syntax check (basic)
