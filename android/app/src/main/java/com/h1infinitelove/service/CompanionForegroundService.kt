package com.h1infinitelove.service

import android.app.Notification
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import com.h1infinitelove.H1Application
import com.h1infinitelove.MainActivity
import com.h1infinitelove.R

/**
 * Core companion foreground service.
 * Keeps essential companion processes alive (memory, AI connection, etc.).
 * Phase 02: Foundation placeholder.
 */
class CompanionForegroundService : Service() {

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        Log.i(TAG, "CompanionForegroundService created")
        startForeground(NOTIFICATION_ID, createNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    private fun createNotification(): Notification {
        val pendingIntent = PendingIntent.getActivity(
            this, 0,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, H1Application.CHANNEL_COMPANION)
            .setContentTitle("H1 Infinite Love")
            .setContentText("Companion core is running")
            .setSmallIcon(R.drawable.ic_companion_notification)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setSilent(true)
            .build()
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.i(TAG, "CompanionForegroundService destroyed")
    }

    companion object {
        private const val TAG = "CompanionService"
        private const val NOTIFICATION_ID = 1002
    }
}
