// Phase 07 - TTS Interface
// Android: Use android.speech.tts.TextToSpeech first (free, offline voices).
// Later: Plug cloud TTS via ITTSProvider.
export interface ITTSProvider {
  speak(text: string, pitch: number, speed: number): Promise<void>;
  stop(): Promise<void>;
  setVoice(voiceId: string): Promise<void>;
  getVoices(): Promise<string[]>;
}
