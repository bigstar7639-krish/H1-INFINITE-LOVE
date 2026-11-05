package com.h1.infinitelove.assistant

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import com.h1.infinitelove.receivers.AlarmReceiver

/**
 * Phase 14 - Reminder Manager - REAL AlarmManager
 * Uses exact alarm where permitted, else inexact.
 * Reminders stored in SharedPreferences (Phase 09 SQLite in full build).
 */
class ReminderManager(private val context: Context) {

    fun createReminder(id: Int, title: String, message: String, triggerAtMillis: Long): Boolean {
        return try {
            val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
            val intent = Intent(context, AlarmReceiver::class.java).apply {
                putExtra("title", title)
                putExtra("message", message)
            }
            val pi = PendingIntent.getBroadcast(context, id, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            try {
                am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, triggerAtMillis, pi)
            } catch (e: SecurityException) {
                // No exact alarm permission -> fallback to inexact
                am.set(AlarmManager.RTC_WAKEUP, triggerAtMillis, pi)
            }
            // Save to prefs
            val prefs = context.getSharedPreferences("h1_reminders", Context.MODE_PRIVATE)
            prefs.edit().putLong("reminder_$id", triggerAtMillis).putString("reminder_${id}_title", title).apply()
            true
        } catch (e: Exception) { false }
    }

    fun cancelReminder(id: Int) {
        val am = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(context, AlarmReceiver::class.java)
        val pi = PendingIntent.getBroadcast(context, id, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        am.cancel(pi)
        context.getSharedPreferences("h1_reminders", Context.MODE_PRIVATE).edit().remove("reminder_$id").apply()
    }
}
