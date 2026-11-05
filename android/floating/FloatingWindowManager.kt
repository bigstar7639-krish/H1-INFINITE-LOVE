package com.h1.infinitelove.floating

import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.View
import android.view.WindowManager

/**
 * Phase 11 - Real WindowManager overlay
 * TYPE_APPLICATION_OVERLAY on Android O+ (requires SYSTEM_ALERT_WINDOW)
 */
class FloatingWindowManager(private val context: Context) {

    private var windowManager: WindowManager? = null
    private var floatingView: View? = null
    private var params: WindowManager.LayoutParams? = null

    fun show() {
        if (floatingView != null) return
        if (!FloatingPermissionHelper.canDrawOverlays(context)) return

        windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
        val state = FloatingState.load(context)

        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        params = WindowManager.LayoutParams(
            state.sizePx,
            state.sizePx,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = state.x
            y = state.y
        }

        floatingView = FloatingBubbleView(context) {
            // Tap -> Open Talk (MainActivity Chat)
            FloatingState.save(context, state.copy(lastTapTime = System.currentTimeMillis()))
        }
        floatingView?.let { view ->
            DragHandler(view, params!!, windowManager!!) { newX, newY ->
                FloatingState.save(context, state.copy(x = newX, y = newY))
            }
        }

        windowManager?.addView(floatingView, params)
    }

    fun hide() {
        try {
            if (floatingView != null) {
                windowManager?.removeView(floatingView)
                floatingView = null
            }
        } catch (e: Exception) {
            // Already removed
        }
    }
}
