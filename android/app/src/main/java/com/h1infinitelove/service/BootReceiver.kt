package com.h1infinitelove.service

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.h1infinitelove.overlay.FloatingCharacterService

/**
 * Restores floating character after device reboot
 * if the user previously enabled persistent companion mode.
 * Phase 02: Foundation — logic will be expanded with user preference storage.
 */
class BootReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent?) {
        if (intent?.action == Intent.ACTION_BOOT_COMPLETED) {
            Log.i(TAG, "Boot completed — checking whether to restore floating character")
            // Future: read user preference from encrypted storage
            // For now we do not auto-start (user must enable it explicitly)
        }
    }

    companion object {
        private const val TAG = "BootReceiver"
    }
}
