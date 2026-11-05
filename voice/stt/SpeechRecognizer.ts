// Phase 07 - STT Interface
// Android: Use android.speech.SpeechRecognizer first.
// Web: Use Web Speech API.
export interface STTResult { text: string; confidence: number; isFinal: boolean; }
export interface ISTTProvider {
  startListening(): Promise<void>;
  stopListening(): Promise<void>;
  onResult(cb: (r: STTResult) => void): void;
  onError(cb: (e: Error) => void): void;
}
// Interruption: If user speaks while Aira is speaking, TTS must stop immediately.
export const INTERRUPTION_ENABLED = true;
