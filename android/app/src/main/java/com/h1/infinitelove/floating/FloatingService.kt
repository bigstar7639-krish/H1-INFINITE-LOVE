package com.h1.infinitelove.floating

import android.app.Service
import android.content.Intent
import android.os.IBinder

/**
 * Phase 02 - PLACEHOLDER ONLY. NOT STARTED.
 * Real floating overlay will be implemented in Phase 11.
 * Do NOT start this service until overlay permission is granted.
 */
class FloatingService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Phase 02: Do nothing. Return NOT_STICKY to avoid background work.
        return START_NOT_STICKY
    }
}
