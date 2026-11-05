# Performance Targets - Phase 18

## Targets
- App launch: < 3 sec
- Floating bubble: < 100ms drag lag
- Chat reply: < 1 sec (local), < 3 sec (cloud)
- Website load: < 2 sec
- APK size: < 50 MB (Phase 19 target)
- Battery: No wake-lock, WorkManager only
- Memory: < 200 MB RAM in normal use
- 3D World: 30 FPS min on mid-range phone

## Optimizations Done
- NOT_STICKY service - no auto restart waste
- SharedPreferences for small data, SQLite for large
- No background polling
- Images compressed, no large assets in repo
- Lazy load 3D worlds - load only selected world

## If Slow?
- Check: Too many animations running?
- Check: Floating + World both running? -> Pause one
- Check: Memory leak in service? -> Stop + restart
