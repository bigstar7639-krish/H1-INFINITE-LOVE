// Phase 10 - Scene Understanding
// Where is Aira? What is around? Bedroom / Garden / Outside?
export interface ISceneUnderstanding {
  describeScene(photoPath: string): Promise<string>;
}
