// Phase 08 - Context Manager
// Keeps: user name, preferences, current world, current emotion, time of day
export interface UserContext {
  userName: string;
  language: string;
  currentWorld: 'bedroom'|'garden'|'living-room';
  currentEmotion: string;
  timeOfDay: string;
}
export const DEFAULT_CONTEXT: UserContext = {
  userName: 'Krish',
  language: 'Tamil+English',
  currentWorld: 'bedroom',
  currentEmotion: 'happy',
  timeOfDay: 'day',
};
