// Phase 06 - Emotion Blender - Real blending logic
export type EmotionName = 'happy'|'sad'|'angry'|'crying'|'laughing'|'shy'|'love'|'jealousy'|'fear'|'surprise'|'excitement'|'confusion'|'curiosity'|'thinking'|'sleepiness'|'boredom'|'embarrassment'|'confidence'|'empathy';
export interface EmotionState { name: EmotionName; intensity: number; }
export class EmotionBlender {
  current: EmotionState = { name: 'happy', intensity: 0.5 };
  private transitionMs = 500;
  setEmotion(next: EmotionName, intensity: number): EmotionState {
    const clamped = Math.max(0, Math.min(1, intensity));
    // Cannot jump crying -> laughing instantly, must go via neutral-ish blend
    if (this.current.name === 'crying' && next === 'laughing' && clamped > 0.7) {
      this.current = { name: 'happy', intensity: 0.5 };
      return this.current;
    }
    this.current = { name: next, intensity: clamped };
    return this.current;
  }
  blend(a: EmotionState, b: EmotionState, t: number): EmotionState {
    return { name: t < 0.5 ? a.name : b.name, intensity: a.intensity + (b.intensity - a.intensity) * t };
  }
}
