// Phase 09 - Long-term: Preferences + Important info, persists
// Stored in SQLite long_term_memory table. User can edit/delete.
export interface LongTermItem { key: string; value: string; category: string; }
export class LongTermMemory {
  // In real app, these methods read/write SQLite via Room.
  // Here interface only, implementation in Phase 13 Mobile Integrations.
  async save(item: LongTermItem): Promise<void> { /* Room insert */ }
  async get(key: string): Promise<LongTermItem | null> { return null; }
  async delete(key: string): Promise<void> { /* Room delete */ }
  async getAll(): Promise<LongTermItem[]> { return []; }
}
