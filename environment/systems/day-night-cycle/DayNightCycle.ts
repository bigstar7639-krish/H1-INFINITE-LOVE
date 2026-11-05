// Phase 12 - Day / Night Cycle
export type TimeOfDay = 'morning'|'afternoon'|'evening'|'night';
export function getTimeOfDay(hour: number): TimeOfDay {
  if (hour >= 5 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 17) return 'afternoon';
  if (hour >= 17 && hour < 20) return 'evening';
  return 'night';
}
export const DAY_NIGHT_LIGHT: Record<TimeOfDay, { ambient: number; sunColor: string }> = {
  morning: { ambient: 0.8, sunColor: '#FFE8B0' },
  afternoon: { ambient: 1.0, sunColor: '#FFFFFF' },
  evening: { ambient: 0.6, sunColor: '#FF9A5A' },
  night: { ambient: 0.3, sunColor: '#5A6AFF' },
};
