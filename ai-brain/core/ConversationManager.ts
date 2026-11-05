// Phase 08 - Conversation Manager
export interface ChatMessage { role: 'user'|'assistant'|'system'; text: string; emotion?: string; timestamp: number; }
export class ConversationManager {
  history: ChatMessage[] = [];
  maxHistory = 20;
  add(msg: ChatMessage) {
    this.history.push(msg);
    if (this.history.length > this.maxHistory) this.history.shift();
  }
  getContext(): ChatMessage[] { return this.history.slice(-10); }
  clear() { this.history = []; }
}
