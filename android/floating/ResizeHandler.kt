package com.h1.infinitelove.floating

import android.content.Context

/**
 * Phase 11 - Resize: Small / Medium / Large
 * Sizes in dp -> px conversion in real app.
 */
enum class FloatingSize(val dp: Int) {
    SMALL(72),
    MEDIUM(110),
    LARGE(160)
}

object ResizeHandler {
    fun nextSize(current: FloatingSize): FloatingSize {
        return when (current) {
            FloatingSize.SMALL -> FloatingSize.MEDIUM
            FloatingSize.MEDIUM -> FloatingSize.LARGE
            FloatingSize.LARGE -> FloatingSize.SMALL
        }
    }
    fun toPx(context: Context, dp: Int): Int {
        val density = context.resources.displayMetrics.density
        return (dp * density).toInt()
    }
}
