// Phase 07 - Emotion -> Voice Mapper - Must cover all 19 emotions
export type EmotionName = 'happy'|'sad'|'angry'|'crying'|'laughing'|'shy'|'love'|'jealousy'|'fear'|'surprise'|'excitement'|'confusion'|'curiosity'|'thinking'|'sleepiness'|'boredom'|'embarrassment'|'confidence'|'empathy';
export interface VoiceParams { pitch: number; speed: number; volume: number; }
export const EMOTION_VOICE_MAP: Record<EmotionName, VoiceParams> = {
  happy: { pitch: 1.1, speed: 1.05, volume: 0.9 },
  sad: { pitch: 0.9, speed: 0.85, volume: 0.7 },
  angry: { pitch: 1.0, speed: 1.1, volume: 0.95 },
  crying: { pitch: 0.95, speed: 0.8, volume: 0.6 },
  laughing: { pitch: 1.15, speed: 1.1, volume: 0.95 },
  shy: { pitch: 1.05, speed: 0.85, volume: 0.6 },
  love: { pitch: 1.08, speed: 0.9, volume: 0.8 },
  jealousy: { pitch: 1.0, speed: 0.95, volume: 0.8 },
  fear: { pitch: 1.2, speed: 1.1, volume: 0.7 },
  surprise: { pitch: 1.25, speed: 1.15, volume: 0.9 },
  excitement: { pitch: 1.2, speed: 1.2, volume: 0.95 },
  confusion: { pitch: 1.0, speed: 0.9, volume: 0.8 },
  curiosity: { pitch: 1.05, speed: 1.0, volume: 0.85 },
  thinking: { pitch: 0.95, speed: 0.8, volume: 0.7 },
  sleepiness: { pitch: 0.85, speed: 0.7, volume: 0.6 },
  boredom: { pitch: 0.9, speed: 0.85, volume: 0.65 },
  embarrassment: { pitch: 1.1, speed: 0.95, volume: 0.7 },
  confidence: { pitch: 1.0, speed: 1.0, volume: 0.95 },
  empathy: { pitch: 1.0, speed: 0.9, volume: 0.8 },
};
export function getVoiceForEmotion(e: EmotionName): VoiceParams {
  return EMOTION_VOICE_MAP[e];
}
