package com.h1.infinitelove.floating

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

/**
 * Phase 11 - REAL Floating Service
 * Starts ONLY when user enables Floating in Settings.
 * Uses ForegroundService + WindowManager overlay.
 */
class FloatingService : Service() {

    private lateinit var windowManager: FloatingWindowManager
    private var isShowing = false

    override fun onCreate() {
        super.onCreate()
        windowManager = FloatingWindowManager(this)
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_SHOW -> {
                startForeground(NOTIFICATION_ID, buildNotification())
                if (!isShowing) {
                    windowManager.show()
                    isShowing = true
                }
            }
            ACTION_HIDE -> {
                windowManager.hide()
                isShowing = false
                stopForeground(true)
                stopSelf()
            }
            ACTION_TOGGLE -> {
                if (isShowing) {
                    windowManager.hide()
                    isShowing = false
                } else {
                    startForeground(NOTIFICATION_ID, buildNotification())
                    windowManager.show()
                    isShowing = true
                }
            }
        }
        // NOT_STICKY: If system kills, do NOT auto-restart without user.
        // BootReceiver in Phase 13 will restore ONLY if user enabled "Restore after reboot".
        return START_NOT_STICKY
    }

    private fun buildNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Aira H1 is here")
            .setContentText("Tap to talk • Drag to move • Long-press to hide")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setOngoing(true)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(CHANNEL_ID, "H1 Floating", NotificationManager.IMPORTANCE_LOW)
            val nm = getSystemService(NotificationManager::class.java)
            nm.createNotificationChannel(channel)
        }
    }

    override fun onDestroy() {
        windowManager.hide()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val CHANNEL_ID = "h1_floating"
        const val NOTIFICATION_ID = 1001
        const val ACTION_SHOW = "com.h1.infinitelove.SHOW_FLOATING"
        const val ACTION_HIDE = "com.h1.infinitelove.HIDE_FLOATING"
        const val ACTION_TOGGLE = "com.h1.infinitelove.TOGGLE_FLOATING"
    }
}
