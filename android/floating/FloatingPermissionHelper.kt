package com.h1.infinitelove.floating

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings

object FloatingPermissionHelper {
    fun canDrawOverlays(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) return true
        return Settings.canDrawOverlays(context)
    }
    fun openOverlaySettings(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:" + context.packageName))
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
        }
    }
    fun startFloating(context: Context) {
        if (!canDrawOverlays(context)) {
            openOverlaySettings(context)
            return
        }
        val intent = Intent(context, FloatingService::class.java).apply {
            action = FloatingService.ACTION_SHOW
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(intent)
        } else {
            context.startService(intent)
        }
    }
    fun stopFloating(context: Context) {
        val intent = Intent(context, FloatingService::class.java).apply {
            action = FloatingService.ACTION_HIDE
        }
        context.startService(intent)
    }
}
