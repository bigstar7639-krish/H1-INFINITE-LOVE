package com.h1infinitelove

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import android.util.Log

/**
 * H1 Infinite Love — Application class
 * Phase 02: Android Foundation
 *
 * Responsibilities:
 * - Global application context
 * - Notification channels (required for foreground services)
 * - Future: dependency injection / module initialization
 */
class H1Application : Application() {

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannels()
        Log.i(TAG, "H1 Infinite Love Application started — Phase 02 Foundation")
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NotificationManager::class.java)

            // Channel for the floating character / companion service
            val companionChannel = NotificationChannel(
                CHANNEL_COMPANION,
                "H1 Companion",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Keeps your AI companion running in the background"
                setShowBadge(false)
            }

            // Channel for important alerts (alarms, reminders later)
            val alertChannel = NotificationChannel(
                CHANNEL_ALERTS,
                "H1 Alerts",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Alarms, reminders and important notifications"
            }

            manager?.createNotificationChannel(companionChannel)
            manager?.createNotificationChannel(alertChannel)
        }
    }

    companion object {
        private const val TAG = "H1Application"

        const val CHANNEL_COMPANION = "h1_companion_channel"
        const val CHANNEL_ALERTS = "h1_alerts_channel"

        @Volatile
        private var instance: H1Application? = null

        fun getInstance(): H1Application {
            return instance ?: throw IllegalStateException("Application not initialized")
        }
    }
}
