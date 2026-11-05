# Personal Assistant Spec - Phase 14

## Commands (Tamil+English)
- "Aira, naalaiku 9 mani ku paal vaangu nu reminder vei" -> Reminder + Alarm
- "Meeting add pannu - Naalaiku 10 mani" -> Calendar event (permission needed)
- "Amma ku call pannu" -> Contact search + CONFIRM + dial (never auto-call without confirm)
- "To-do la paal vaangu add pannu" -> Task add
- "Enna tasks irukku?" -> List tasks

## Rules (IMPORTANT)
- Sensitive actions: Call / Delete calendar / Delete task -> ALWAYS confirm first
- Permission denied -> Say "Permission illa", NEVER fake success
- Contacts / Calendar NEVER upload, stay on phone
- Reminders: Exact alarm where permitted, else inexact fallback
- All data local: SharedPreferences / SQLite (Phase 09)

## What is NOT done
- Full UI - Phase 17 Website / Phase 19 APK
- Voice parsing - Phase 07 STT + Phase 14 parseIntent together in final build

Next: Phase 15 Personality
