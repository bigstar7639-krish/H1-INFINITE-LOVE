// Phase 09 - Short-term: Current session only, last 20 messages
export class ShortTermMemory {
  private items: { text: string; role: string; time: number }[] = [];
  add(role: string, text: string) {
    this.items.push({ role, text, time: Date.now() });
    if (this.items.length > 20) this.items.shift();
  }
  getAll() { return this.items; }
  clear() { this.items = []; }
}
