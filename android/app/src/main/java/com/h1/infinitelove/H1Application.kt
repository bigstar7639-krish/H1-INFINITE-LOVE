package com.h1.infinitelove
import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
class H1Application : Application() {
    companion object { const val CHANNEL_ID = "h1_floating" }
    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(CHANNEL_ID, "H1 Floating", NotificationManager.IMPORTANCE_LOW)
            getSystemService(NotificationManager::class.java).createNotificationChannel(ch)
        }
    }
}
