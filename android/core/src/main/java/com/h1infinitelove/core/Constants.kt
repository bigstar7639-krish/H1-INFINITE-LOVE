package com.h1infinitelove.core

/**
 * Shared constants used across the Android application.
 */
object Constants {
    const val APP_NAME = "H1 Infinite Love"
    const val PACKAGE_NAME = "com.h1infinitelove"

    // Notification IDs
    const val NOTIFICATION_FLOATING = 1001
    const val NOTIFICATION_COMPANION = 1002

    // Preference keys (will move to secure storage later)
    const val PREF_FLOATING_ENABLED = "floating_character_enabled"
    const val PREF_FIRST_LAUNCH = "first_launch_completed"
}
