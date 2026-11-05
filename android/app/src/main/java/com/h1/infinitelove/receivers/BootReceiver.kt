package com.h1.infinitelove.receivers

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

/**
 * Phase 02: Boot receiver does NOT auto-start anything.
 * Phase 11+ will restore floating state ONLY if user enabled it.
 */
class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent?.action == Intent.ACTION_BOOT_COMPLETED) {
            // Intentionally empty in Phase 02
        }
    }
}
