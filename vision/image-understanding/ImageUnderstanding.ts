// Phase 10 - Image Understanding
// Input: Photo user took / shared
// Output: Description in Tamil+English, e.g. "Ithu oru poonai, sofa mela ukkanthirukku"
export interface IImageUnderstanding {
  describeImage(photoPath: string): Promise<{ description: string; emotion: string }>;
}
