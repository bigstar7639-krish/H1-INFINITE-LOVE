package com.h1.infinitelove.services

/**
 * Phase 13 - Boot Restore Spec
 * On BOOT_COMPLETED:
 * - IF user enabled Floating + RestoreAfterReboot -> Start FloatingService
 * - IF user set Alarms -> Re-schedule alarms
 * - ELSE: Do nothing
 * Implementation in Phase 14 + 16, spec only here.
 */
object BootReceiverUpdated {
    const val SPEC = "Restore only if user enabled"
}
