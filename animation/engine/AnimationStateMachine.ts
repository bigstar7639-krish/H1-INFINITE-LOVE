// Phase 05 - Animation State Machine - Real logic, no fake animation
// Works with Three.js AnimationMixer in web, and with VRM in Android WebView later.

export type AnimationState =
  | 'idle' | 'walking' | 'running' | 'dancing' | 'sitting' | 'standing'
  | 'sleeping' | 'talking' | 'laughing' | 'crying' | 'eating' | 'drinking'
  | 'looking-around' | 'hand-gestures';

export type EmotionForAnim = 'happy'|'sad'|'angry'|'shy'|'love'|'surprise'|'sleepiness'|'boredom'|'excitement'|'neutral';

const ALLOWED_TRANSITIONS: Record<AnimationState, AnimationState[]> = {
  'idle': ['walking','running','dancing','sitting','standing','sleeping','talking','laughing','crying','eating','drinking','looking-around','hand-gestures'],
  'walking': ['idle','running','standing','talking','looking-around'],
  'running': ['idle','walking','standing'],
  'dancing': ['idle','standing'],
  'sitting': ['idle','standing','eating','drinking','talking','sleeping'],
  'standing': ['idle','walking','sitting','dancing','talking'],
  'sleeping': ['idle','sitting'],
  'talking': ['idle','sitting','standing','hand-gestures','laughing'],
  'laughing': ['idle','talking','sitting','standing'],
  'crying': ['idle','sitting','standing'],
  'eating': ['idle','sitting','drinking'],
  'drinking': ['idle','sitting','eating'],
  'looking-around': ['idle','walking','standing'],
  'hand-gestures': ['idle','talking','standing','sitting'],
};

export class AnimationStateMachine {
  current: AnimationState = 'idle';
  private clipExists: (state: AnimationState) => boolean;

  constructor(clipExists: (s: AnimationState) => boolean) {
    this.clipExists = clipExists;
  }

  canTransitionTo(next: AnimationState): boolean {
    return ALLOWED_TRANSITIONS[this.current].includes(next);
  }

  transitionTo(next: AnimationState): { ok: boolean; reason: string } {
    if (!this.canTransitionTo(next)) {
      return { ok: false, reason: `Cannot go from ${this.current} to ${next}` };
    }
    if (!this.clipExists(next)) {
      return { ok: false, reason: `Clip for ${next} not found - NOT_IMPLEMENTED, not fake playing` };
    }
    this.current = next;
    return { ok: true, reason: `Playing ${next}` };
  }
}
