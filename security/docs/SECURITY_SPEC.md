# Security & Privacy Spec - Phase 16

## What we NEVER save
- Passwords, OTP, Bank, Card, PIN, CVV, Aadhaar, PAN
- PrivacyManager.shouldSave() blocks these keywords

## Encryption
- Local backup: AES-256-GCM
- Key: Android Keystore (full build)
- No plain-text backup

## Permissions - Central Check
- Mic, Camera, Contacts, Calendar, Overlay - all checked before use
- Denied -> Feature says "Permission illa", never bypass

## User Controls
- View Memory / Edit / Delete single / Delete ALL / Export / Backup / Restore
- Disable Memory - toggle off = nothing saved
- Auto-delete: 7 / 30 / 90 days / Never - user chooses

## No Tracking
- No background capture, no secret screenshots, no face recognition of others
- No auto cloud upload - Share tap pannina mattum

## Data Storage
- All local on phone, SQLite + SharedPreferences
- Cloud ONLY if user enables + gives own API key (Phase 08)

Next: Phase 17 Website
