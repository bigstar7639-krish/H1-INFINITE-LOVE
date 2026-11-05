// Phase 07 - Realtime Conversation Pipeline
// Flow: Mic -> STT -> AI Brain -> Emotion -> TTS + LipSync + Animation
// Steps:
// 1. User speaks / types
// 2. STT -> text (if voice)
// 3. AI Brain -> reply text + emotion (Phase 08)
// 4. EmotionVoiceMapper -> pitch/speed
// 5. TTS -> audio
// 6. LipSync -> visemes from audio timing
// 7. Animation -> talking + hand-gestures
// Interruption: User speaks during step 5 -> stop TTS, go to step 2.
export const PIPELINE_STEPS = ['STT','AI_BRAIN','EMOTION','TTS','LIPSYNC','ANIMATION'];
