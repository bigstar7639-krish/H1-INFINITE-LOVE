// Phase 10 - Visual Q&A
// User: "Itha photo la enna irukku?" / "Ithu enna colour?"
// Aira answers from photo + AI Brain
export interface IVisualQA {
  answer(photoPath: string, question: string): Promise<string>;
}
