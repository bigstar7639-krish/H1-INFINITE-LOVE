package com.h1.infinitelove.floating

import android.view.MotionEvent
import android.view.View
import android.view.WindowManager

/**
 * Phase 11 - Drag + Tap detection
 * Drag: Move view, save position
 * Tap: < 200ms + < 10px movement = Tap
 * Long-press: Handled in BubbleView
 */
class DragHandler(
    private val view: View,
    private val params: WindowManager.LayoutParams,
    private val windowManager: WindowManager,
    private val onPositionChanged: (x: Int, y: Int) -> Unit
) : View.OnTouchListener {

    private var initialX = 0
    private var initialY = 0
    private var initialTouchX = 0f
    private var initialTouchY = 0f
    private var downTime = 0L

    init { view.setOnTouchListener(this) }

    override fun onTouch(v: View?, event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                initialX = params.x
                initialY = params.y
                initialTouchX = event.rawX
                initialTouchY = event.rawY
                downTime = System.currentTimeMillis()
                return true
            }
            MotionEvent.ACTION_MOVE -> {
                params.x = initialX + (event.rawX - initialTouchX).toInt()
                params.y = initialY + (event.rawY - initialTouchY).toInt()
                windowManager.updateViewLayout(view, params)
                return true
            }
            MotionEvent.ACTION_UP -> {
                val duration = System.currentTimeMillis() - downTime
                val dx = event.rawX - initialTouchX
                val dy = event.rawY - initialTouchY
                val isTap = duration < 200 && Math.abs(dx) < 10 && Math.abs(dy) < 10
                if (isTap) {
                    view.performClick()
                } else {
                    onPositionChanged(params.x, params.y)
                }
                return true
            }
        }
        return false
    }
}
