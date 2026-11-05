package com.h1.infinitelove.services

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager

/**
 * Phase 13 - App Launching
 * User says "WhatsApp open pannu" -> Launch ONLY if app installed + user confirmed.
 * NEVER launch banking / sensitive apps without extra confirm.
 */
object AppLauncher {
    fun launch(context: Context, packageName: String): Boolean {
        return try {
            val pm = context.packageManager
            val intent = pm.getLaunchIntentForPackage(packageName) ?: return false
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
            true
        } catch (e: Exception) {
            false
        }
    }
    fun isInstalled(context: Context, packageName: String): Boolean {
        return try {
            context.packageManager.getPackageInfo(packageName, 0)
            true
        } catch (e: PackageManager.NameNotFoundException) {
            false
        }
    }
}
