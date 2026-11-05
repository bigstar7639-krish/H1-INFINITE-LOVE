# Phase 07 - Voice System - TESTED

## Added
- voice/stt/SpeechRecognizer.ts - STT interface
- voice/tts/TTSEngine.ts - TTS interface + VoiceProfile
- voice/pipeline/RealtimeConversation.ts - Full pipeline spec
- voice/pipeline/EmotionVoiceMapper.ts - Emotion -> pitch/speed
- voice/tts/VoiceProfile.json - Aira H1 voice
- voice/docs/VOICE_SPEC.md

## Honest
- Interfaces + Spec ONLY. No real voice model yet.
- Android will use Android SpeechRecognizer + TextToSpeech first (free, works on phone).
- Cloud / Local TTS can be plugged later via provider interface.
- No fake voice playback.

## Test
- JSON valid
- Emotion -> voice mapping has all 19 emotions
- Pipeline has interruption handling
