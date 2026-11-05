// Phase 10 - Screen Understanding - WITH PERMISSION ONLY
// User must explicitly enable + show indicator.
// Use cases: "Itha screen la enna error?" - user shares screenshot
// NEVER auto-capture screen in background.
export interface IScreenUnderstanding {
  requestScreenPermission(): Promise<boolean>;
  analyzeScreenshot(screenshotPath: string): Promise<string>;
}
export const SCREEN_PRIVACY = "Screen capture ONLY when user shares screenshot. No background capture.";
