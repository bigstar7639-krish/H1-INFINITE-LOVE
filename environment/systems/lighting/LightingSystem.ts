// Phase 12 - Lighting
// Ambient + Directional (Sun/Moon) + Point (Lamp) + Spot (TV)
// Lighting changes with Day/Night + Weather + User setting
export interface LightingSettings { brightness: number; warm: number; lampOn: boolean; }
export const DEFAULT_LIGHTING: LightingSettings = { brightness: 0.9, warm: 0.5, lampOn: true };
