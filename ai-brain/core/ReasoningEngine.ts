// Phase 08 - Reasoning Engine - Simple steps, no fake reasoning
// Steps: 1. Understand intent 2. Check memory 3. Choose skill 4. Draft reply 5. Add emotion
export type Intent = 'chat'|'programming'|'math'|'translation'|'creative'|'planning'|'decision'|'general';
export function detectIntent(text: string): Intent {
  const t = text.toLowerCase();
  if (t.includes('code') || t.includes('python') || t.includes('kotlin')) return 'programming';
  if (t.includes('translate') || t.includes('tamil') && t.includes('english')) return 'translation';
  if (t.match(/\d+\s*[+\-*/]/)) return 'math';
  if (t.includes('plan') || t.includes('schedule')) return 'planning';
  if (t.includes('story') || t.includes('poem')) return 'creative';
  if (t.includes('should i') || t.includes('decide')) return 'decision';
  return 'chat';
}
