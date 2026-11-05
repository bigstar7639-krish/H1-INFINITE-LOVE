// Phase 08 - Pluggable Provider Interface
export interface AIProvider {
  name: string;
  generate(prompt: string, context: string[]): Promise<{ text: string; emotion: string }>;
  isAvailable(): Promise<boolean>;
}
// Providers to implement later:
// - LocalProvider: On-device small model (offline)
// - CloudProvider: API-based model (needs key, user opt-in)
// - OfflineFallback: Canned safe replies when no provider available
export const OFFLINE_FALLBACK_REPLIES = [
  "Naan ippo offline la irukken, aana unakku help panna try pannuren. Konjam detail ah sollu.",
  "Internet / AI model connect aagala. Aana naan inga thaan irukken, enna venum nu sollu.",
];
