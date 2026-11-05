// Phase 06 - Transition Manager
// Controls how fast emotion changes. No instant fake jumps.
export const TRANSITION_MS = 500;
export function getTransitionTime(from: string, to: string): number {
  if (from === to) return 0;
  if ((from === 'crying' && to === 'laughing') || (from === 'angry' && to === 'love')) return 1200;
  return TRANSITION_MS;
}
