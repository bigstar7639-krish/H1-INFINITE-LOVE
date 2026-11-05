package com.h1.infinitelove.security

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat

/**
 * Phase 16 - Central Permission Manager
 * Every feature checks permission BEFORE using it.
 * If denied -> feature says "Permission illa", never crashes, never bypasses.
 */
object PermissionManager {
    fun has(context: Context, permission: String): Boolean {
        return ContextCompat.checkSelfPermission(context, permission) == PackageManager.PERMISSION_GRANTED
    }
    fun hasOverlay(context: Context): Boolean {
        return android.provider.Settings.canDrawOverlays(context)
    }
    fun hasMic(context: Context): Boolean = has(context, Manifest.permission.RECORD_AUDIO)
    fun hasCamera(context: Context): Boolean = has(context, Manifest.permission.CAMERA)
    fun hasContacts(context: Context): Boolean = has(context, Manifest.permission.READ_CONTACTS)
    fun hasCalendar(context: Context): Boolean = has(context, Manifest.permission.READ_CALENDAR)
}
