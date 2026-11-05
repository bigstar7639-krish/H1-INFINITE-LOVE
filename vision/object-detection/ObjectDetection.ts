// Phase 10 - Object Detection
// Detects: person, cat, dog, car, book, phone, etc. - on-device first
export interface DetectedObject { label: string; confidence: number; }
export interface IObjectDetection {
  detect(photoPath: string): Promise<DetectedObject[]>;
}
