package com.h1.infinitelove.receivers

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.h1.infinitelove.services.NotificationService

/**
 * Phase 13 - Alarm / Reminder Receiver
 * Fires ONLY when user set alarm/reminder in Phase 14.
 */
class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        val title = intent?.getStringExtra("title") ?: "H1 Reminder"
        val msg = intent?.getStringExtra("message") ?: "Unakku oru reminder irukku!"
        if (context != null) {
            NotificationService.show(context, title, msg)
        }
    }
}
