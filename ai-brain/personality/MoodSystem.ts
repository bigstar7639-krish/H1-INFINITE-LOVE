// Phase 15 - Mood System
export type AiraMood = 'happy' | 'calm' | 'excited' | 'supportive' | 'playful';
export interface MoodState { mood: AiraMood; energy: number; warmth: number; }
export const MOOD_DEFAULT: MoodState = { mood: 'calm', energy: 0.7, warmth: 0.9 };
export function moodFromUserText(text: string): AiraMood {
  const t = text.toLowerCase();
  if (t.includes('sad') || t.includes('kashtam') || t.includes('azhugai')) return 'supportive';
  if (t.includes('happy') || t.includes('santhosham') || t.includes('jolly')) return 'happy';
  if (t.includes('bore')) return 'playful';
  if (t.includes('excited') || t.includes('semma')) return 'excited';
  return 'calm';
}
