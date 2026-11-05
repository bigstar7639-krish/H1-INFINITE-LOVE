package com.h1.infinitelove.security

import android.content.Context

/** Phase 16 - Data Deletion - User right to delete */
object DataDeletion {
    fun deleteSingleMemory(context: Context, memoryId: String) {
        // Remove one memory entry - Phase 09 table
        val prefs = context.getSharedPreferences("h1_memory", Context.MODE_PRIVATE)
        prefs.edit().remove(memoryId).apply()
    }
    fun deleteAll(context: Context) { PrivacyManager.deleteAll(context) }
}
