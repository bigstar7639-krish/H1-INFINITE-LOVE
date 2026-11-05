# Mobile Integrations Spec - Phase 13

## Integrations (8)
1. Notifications - Reminders, Alarms, Aira messages user enabled. No spam.
2. Alarms - Exact alarm via AlarmManager, re-scheduled after reboot
3. Calendar - Read / Add events ONLY with permission (Phase 14)
4. Contacts - For calling / messaging ONLY with permission, never upload
5. App Launching - Launch installed app on user voice command + confirm for sensitive apps
6. File Management - Download / H1 folder only, list / open / share user files
7. Boot Restore - Floating + Alarms restore ONLY if user enabled
8. Battery / Doze - Use WorkManager / AlarmManager, respect battery optimization, no wake-lock abuse

## Permissions (Only when used)
- POST_NOTIFICATIONS
- SCHEDULE_EXACT_ALARM
- READ_CALENDAR / WRITE_CALENDAR (Phase 14, optional)
- READ_CONTACTS (Phase 14, optional)
- READ_MEDIA_* / READ_EXTERNAL_STORAGE (File, optional)

## Privacy
- No reading other apps data
- No background tracking
- No uploading contacts / files without user tap

## What is NOT done
- Full Calendar / Contacts integration in Phase 14
- Full Assistant logic in Phase 14

Next: Phase 14 Personal Assistant
