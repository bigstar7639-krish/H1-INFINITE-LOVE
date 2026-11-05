package com.h1.infinitelove

import android.app.Application

/**
 * Phase 02 - Android Foundation
 * No AI / Floating / Voice started here. Only app-level init.
 */
class H1Application : Application() {
    override fun onCreate() {
        super.onCreate()
        // Phase 02: No background work started automatically.
        // Future phases will init DI / Database / Memory here with user consent.
    }
}
