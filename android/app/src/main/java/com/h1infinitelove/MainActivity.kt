package com.h1infinitelove

import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import com.h1infinitelove.databinding.ActivityMainBinding
import com.h1infinitelove.overlay.FloatingCharacterService
import com.h1infinitelove.permission.PermissionManager

/**
 * Main entry point of H1 Infinite Love.
 * Phase 02: Foundation — basic UI shell + permission + overlay launch controls.
 *
 * Later phases will replace this with the full 3D environment and companion UI.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var permissionManager: PermissionManager

    private val overlayPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) {
        if (Settings.canDrawOverlays(this)) {
            Toast.makeText(this, "Overlay permission granted", Toast.LENGTH_SHORT).show()
            startFloatingCharacter()
        } else {
            Toast.makeText(this, "Overlay permission is required for the floating character", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        permissionManager = PermissionManager(this)

        setupUI()
    }

    private fun setupUI() {
        binding.btnRequestOverlay.setOnClickListener {
            requestOverlayPermission()
        }

        binding.btnStartFloating.setOnClickListener {
            if (Settings.canDrawOverlays(this)) {
                startFloatingCharacter()
            } else {
                requestOverlayPermission()
            }
        }

        binding.btnStopFloating.setOnClickListener {
            stopFloatingCharacter()
        }

        binding.tvStatus.text = "H1 Infinite Love — Phase 02 Foundation\nReady for character & modules"
    }

    private fun requestOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                val intent = Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:$packageName")
                )
                overlayPermissionLauncher.launch(intent)
            } else {
                Toast.makeText(this, "Overlay permission already granted", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun startFloatingCharacter() {
        val intent = Intent(this, FloatingCharacterService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        Toast.makeText(this, "Floating character service started", Toast.LENGTH_SHORT).show()
    }

    private fun stopFloatingCharacter() {
        val intent = Intent(this, FloatingCharacterService::class.java)
        stopService(intent)
        Toast.makeText(this, "Floating character service stopped", Toast.LENGTH_SHORT).show()
    }
}
