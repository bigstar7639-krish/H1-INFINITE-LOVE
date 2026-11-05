package com.h1.infinitelove.floating

import android.content.Context

/**
 * Phase 11 - Persistent state
 * Saved in SharedPreferences (Phase 13 will move to DataStore).
 * Restored on restart where Android permits.
 */
data class FloatingState(
    val x: Int = 100,
    val y: Int = 300,
    val sizePx: Int = 220,
    val isVisible: Boolean = true,
    val isEnabled: Boolean = false, // User must enable explicitly
    val restoreAfterReboot: Boolean = false,
    val lastTapTime: Long = 0L
) {
    companion object {
        private const val PREFS = "h1_floating_state"
        fun load(context: Context): FloatingState {
            val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            return FloatingState(
                x = prefs.getInt("x", 100),
                y = prefs.getInt("y", 300),
                sizePx = prefs.getInt("sizePx", 220),
                isVisible = prefs.getBoolean("isVisible", true),
                isEnabled = prefs.getBoolean("isEnabled", false),
                restoreAfterReboot = prefs.getBoolean("restoreAfterReboot", false)
            )
        }
        fun save(context: Context, state: FloatingState) {
            val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            prefs.edit()
                .putInt("x", state.x)
                .putInt("y", state.y)
                .putInt("sizePx", state.sizePx)
                .putBoolean("isVisible", state.isVisible)
                .putBoolean("isEnabled", state.isEnabled)
                .putBoolean("restoreAfterReboot", state.restoreAfterReboot)
                .putLong("lastTapTime", state.lastTapTime)
                .apply()
        }
    }
}
