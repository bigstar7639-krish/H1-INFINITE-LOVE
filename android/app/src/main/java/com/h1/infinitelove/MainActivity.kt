package com.h1.infinitelove

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Phase 02 - Foundation Screen ONLY.
 * This is NOT the final UI. No fake buttons, no fake chat.
 * Shows real build info: version + phase + module status.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                FoundationScreen()
            }
        }
    }
}

@Composable
fun FoundationScreen() {
    Column(
        modifier = Modifier.fillMaxSize().padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("H1 INFINITE LOVE", style = MaterialTheme.typography.headlineMedium)
        Text("Phase 02 - Android Foundation - TEST BUILD", style = MaterialTheme.typography.bodyMedium)
        Text("Version: 0.2.0-phase02")
        Text("Status: Foundation OK. Character / Voice / AI not yet implemented.")
        Text("Next: Phase 03 - Original Anime Character")
    }
}
