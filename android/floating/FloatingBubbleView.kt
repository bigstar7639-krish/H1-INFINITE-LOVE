package com.h1.infinitelove.floating

import android.content.Context
import android.view.View
import android.widget.FrameLayout
import android.widget.TextView

/**
 * Phase 11 - Bubble View
 * Phase 11: Shows Aira avatar placeholder + name.
 * Phase 12: Replaced with 3D WebView / SurfaceView showing full Aira.
 * Tap -> onTap callback (opens Talk)
 */
class FloatingBubbleView(context: Context, private val onTap: () -> Unit) : FrameLayout(context) {
    init {
        val text = TextView(context).apply {
            text = "Aira H1\nTap to Talk"
            textSize = 12f
            setPadding(20, 20, 20, 20)
        }
        addView(text)
        setOnClickListener { onTap() }
        // Long-press: Show Hide menu in Phase 13
        setOnLongClickListener {
            // TODO Phase 13: Show Hide / Resize / Settings menu
            true
        }
    }
}
