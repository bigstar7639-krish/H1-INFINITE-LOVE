package com.h1.infinitelove
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.h1.infinitelove.databinding.ActivityMainBinding
import com.h1.infinitelove.floating.FloatingService
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.tvStatus.text = "Phase 02 Ready\n3D World: Planned Phase 12\nFloating: Planned Phase 11"
        binding.btnEnableFloating.setOnClickListener {
            if (!Settings.canDrawOverlays(this)) {
                Toast.makeText(this, "Allow Display over other apps", Toast.LENGTH_LONG).show()
                startActivity(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName")))
                return@setOnClickListener
            }
            startService(Intent(this, FloatingService::class.java))
            Toast.makeText(this, "Floating service started", Toast.LENGTH_SHORT).show()
        }
        binding.btnOpenWorld.setOnClickListener { binding.tvStatus.text = "Full 3D World - Planned Phase 12. Not fake." }
        binding.btnVoice.setOnClickListener { binding.tvStatus.text = "Voice - Planned Phase 07" }
        binding.btnPrivacy.setOnClickListener { binding.tvStatus.text = "Privacy - Planned Phase 16. No data collected in Phase 02." }
    }
}
