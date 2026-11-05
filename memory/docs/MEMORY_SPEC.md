# Memory Spec - Phase 09

## Types
- Short-term: Current session, last 20, auto-clear on new session if user wants
- Long-term: Preferences, important info, goals - persists in SQLite
- Conversation History: Full history, user can delete any / all
- Preferences: Language, voice pitch/speed, world, outfit
- Important Info: User-marked important facts

## Controls (User)
- View, Edit, Delete single, Delete all, Export, Backup, Restore, Disable memory
- Auto-delete: 7 / 30 / 90 days or never

## Privacy
- Local only by default
- Encrypted in Phase 16
- No cloud sync without explicit permission
- Memory NEVER includes passwords / OTP / bank - blocked

## Backup / Restore
- Backup: Local JSON + SQLite, encrypted
- Restore: Confirm + overwrite warning

Next: Phase 10 Vision
