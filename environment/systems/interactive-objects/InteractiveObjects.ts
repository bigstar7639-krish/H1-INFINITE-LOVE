// Phase 12 - Interactive Objects
// Tap object -> Aira reacts + animation + reply
export interface InteractiveObject { id: string; world: string; action: string; animation: string; reply: string; }
export const INTERACTIVE_OBJECTS: InteractiveObject[] = [
  { id: 'bed', world: 'bedroom', action: 'tap', animation: 'sitting', reply: 'Bed la ukkanthukalama?' },
  { id: 'lamp', world: 'bedroom', action: 'tap', animation: 'hand-gestures', reply: 'Light ah on/off pannattuma?' },
  { id: 'bench', world: 'garden', action: 'tap', animation: 'sitting', reply: 'Garden bench la ukkanthukalam, super ah irukkum!' },
  { id: 'swing', world: 'garden', action: 'tap', animation: 'dancing', reply: 'Swing aadalama?' },
  { id: 'sofa', world: 'living-room', action: 'tap', animation: 'sitting', reply: 'Sofa la ukkanthu TV paakalama?' },
  { id: 'tv', world: 'living-room', action: 'tap', animation: 'talking', reply: 'TV on pannattuma?' },
];
