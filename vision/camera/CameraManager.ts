// Phase 10 - Camera Manager
// Rules:
// 1. Camera only when user taps Camera button
// 2. Show camera indicator (Phase 16)
// 3. Stop camera when user closes / app backgrounds
export interface ICameraManager {
  requestPermission(): Promise<boolean>;
  startCamera(): Promise<void>;
  stopCamera(): Promise<void>;
  capturePhoto(): Promise<string>; // returns local path, not uploaded
  isCameraOn(): boolean;
}
export const CAMERA_PRIVACY = "Camera photo stays on phone. Upload only if user taps Share.";
