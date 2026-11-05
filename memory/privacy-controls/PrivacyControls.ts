// Phase 09 - Privacy Controls - USER OWNS MEMORY
export const PRIVACY_CONTROLS = {
  viewMemory: true,
  editMemory: true,
  deleteSingleMemory: true,
  deleteAllMemory: true,
  exportMemory: true,
  backupMemory: true,
  restoreMemory: true,
  disableMemory: true, // User can turn off memory completely
  autoDeleteDays: 0, // 0 = never, user can set 7/30/90
};
export function deleteAllMemoryConfirm(): string {
  return "Are you sure? This will delete ALL memory permanently. This cannot be undone.";
}
