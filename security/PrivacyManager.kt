package com.h1.infinitelove.security

import android.content.Context

/**
 * Phase 16 - Privacy Manager
 * User controls: View / Edit / Delete single / Delete ALL / Export / Backup / Disable Memory
 * NEVER save: passwords, OTP, bank, card numbers.
 */
object PrivacyManager {
    private val BLOCKED_KEYWORDS = listOf("password", "otp", "bank", "card number", "pin", "cvv", "aadhaar", "pan number")

    fun shouldSave(text: String): Boolean {
        val t = text.lowercase()
        return BLOCKED_KEYWORDS.none { it in t }
    }

    fun deleteAll(context: Context) {
        // Delete all H1 local data
        val prefsNames = listOf("h1_tasks", "h1_reminders", "h1_floating_state", "h1_memory", "h1_preferences")
        prefsNames.forEach { context.getSharedPreferences(it, Context.MODE_PRIVATE).edit().clear().apply() }
        // SQLite tables cleared in Phase 09 MemoryManager.deleteAll()
    }

    fun exportData(context: Context): String {
        // Returns JSON summary - real export in full build via Phase 09
        return "{\"export\":\"H1 data export - local only\",\"note\":\"No cloud upload\"}"
    }
}
