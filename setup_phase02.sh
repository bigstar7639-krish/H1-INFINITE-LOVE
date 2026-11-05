#!/bin/bash
echo "Creating H1 Phase 02..."

mkdir -p android/app/src/main/java/com/h1/infinitelove/floating
mkdir -p android/app/src/main/java/com/h1/infinitelove/permissions
mkdir -p android/app/src/main/java/com/h1/infinitelove/webview
mkdir -p android/app/src/main/res/layout
mkdir -p android/app/src/main/res/values
mkdir -p android/app/src/main/res/drawable
mkdir -p .github/workflows
mkdir -p [STRIPPED 129 bytes]

# settings.gradle
cat > android/settings.gradle.kts << 'END'
rootProject.name = "H1-INFINITE-LOVE"
include(":app")
END

# build.gradle top
cat > android/build.gradle.kts << 'END'
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
END

# app build.gradle
cat > android/app/build.gradle.kts << 'END'
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.h1.infinitelove"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.h1.infinitelove"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "0.2.0-phase02"
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
}
END

# AndroidManifest
cat > android/app/src/main/AndroidManifest.xml << 'END'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.CAMERA" />
    <application android:name=".H1Application" android:label="H1 Infinite Love" android:theme="@style/Theme.H1InfiniteLove">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter>
        </activity>
        <service android:name=".floating.FloatingService" android:exported="false" android:foregroundServiceType="mediaPlayback" />
    </application>
</manifest>
END

# H1Application
cat > android/app/src/main/java/com/h1/infinitelove/H1Application.kt << 'END'
package com.h1.infinitelove
import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
class H1Application : Application() {
    companion object { const val CHANNEL_ID = "h1_floating" }
    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(CHANNEL_ID, "H1 Floating", NotificationManager.IMPORTANCE_LOW)
            getSystemService(NotificationManager::class.java).createNotificationChannel(ch)
        }
    }
}
END

# MainActivity
cat > android/app/src/main/java/com/h1/infinitelove/MainActivity.kt << 'END'
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
END

# FloatingService
cat > [STRIPPED 70 bytes].kt << 'END'
package com.h1.infinitelove.floating
import android.app.*
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.h1.infinitelove.*
class FloatingService : Service() {
    private var manager: FloatingViewManager? = null
    override fun onCreate() {
        super.onCreate()
        val pi = PendingIntent.getActivity(this, 0, Intent(this, MainActivity::class.java), PendingIntent.FLAG_IMMUTABLE)
        val notif = NotificationCompat.Builder(this, H1Application.CHANNEL_ID)
            .setContentTitle("H1 Infinite Love").setContentText("Floating active - tap to open").setSmallIcon(R.mipmap.ic_launcher).setContentIntent(pi).setOngoing(true).build()
        startForeground(1, notif)
        manager = FloatingViewManager(this)
        manager?.showPlaceholder()
    }
    override fun onDestroy() { manager?.hide(); super.onDestroy() }
    override fun onBind(intent: Intent?): IBinder? = null
}
END

# FloatingViewManager
cat > [STRIPPED 74 bytes].kt << 'END'
package com.h1.infinitelove.floating
import android.content.Context
import android.graphics.PixelFormat
import android.view.*
import com.h1.infinitelove.R
class FloatingViewManager(private val ctx: Context) {
    private var view: View? = null
    private var wm: WindowManager? = null
    private var params: WindowManager.LayoutParams? = null
    fun showPlaceholder() {
        if (view != null) return
        wm = ctx.getSystemService(Context.WINDOW_SERVICE) as WindowManager
        view = LayoutInflater.from(ctx).inflate(R.layout.view_floating_placeholder, null)
        val type = if (android.os.Build.VERSION.SDK_INT >= 26) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE
        params = WindowManager.LayoutParams(320, 320, type, WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE, PixelFormat.TRANSLUCENT)
        params?.gravity = Gravity.TOP or Gravity.START; params?.x = 100; params?.y = 300
        val drag = DragHandler { dx, dy -> params?.x = params!!.x + dx; params?.y = params!!.y + dy; wm?.updateViewLayout(view, params) }
        view?.setOnTouchListener(drag)
        wm?.addView(view, params)
    }
    fun hide() { try { if (view != null) wm?.removeView(view) } catch(e: Exception){} ; view = null }
}
END

cat > [STRIPPED 66 bytes].kt << 'END'
package com.h1.infinitelove.floating
import android.view.MotionEvent
import android.view.View
class DragHandler(private val onDrag: (dx: Int, dy: Int) -> Unit) : View.OnTouchListener {
    private var lastX = 0f; private var lastY = 0f
    override fun onTouch(v: View, e: MotionEvent): Boolean {
        when(e.action) {
            MotionEvent.ACTION_DOWN -> { lastX = e.rawX; lastY = e.rawY; return true }
            MotionEvent.ACTION_MOVE -> {
                val dx = (e.rawX - lastX).toInt(); val dy = (e.rawY - lastY).toInt()
                lastX = e.rawX; lastY = e.rawY
                if (kotlin.math.abs(dx) > 2 || kotlin.math.abs(dy) > 2) onDrag(dx, dy)
                return true
            }
        }
        return false
    }
}
END

# Layouts
cat > android/app/src/main/res/layout/activity_main.xml << 'END'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" android:orientation="vertical" android:layout_width="match_parent" android:layout_height="match_parent" android:padding="20dp" android:background="#FFF5F7">
<TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="H1 INFINITE LOVE" android:textSize="28sp" android:textStyle="bold" android:textColor="#D81B60"/>
<TextView android:id="@+id/tvStatus" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp" android:text="Phase 02 Ready" android:textSize="16sp"/>
<Button android:id="@+id/btnEnableFloating" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="20dp" android:text="Enable Floating Character"/>
<Button android:id="@+id/btnOpenWorld" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:text="Open 3D World - Planned Phase 12"/>
<Button android:id="@+id/btnVoice" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:text="Voice - Planned Phase 07"/>
<Button android:id="@+id/btnPrivacy" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:text="Privacy - Planned Phase 16"/>
</LinearLayout>
END

cat > android/app/src/main/res/layout/view_floating_placeholder.xml << 'END'
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="320dp" android:layout_height="320dp" android:background="@drawable/bg_floating">
<TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_gravity="center" android:gravity="center" android:text="H1\nDrag me\nPhase 11 = Full 3D" android:textColor="#FFFFFF" android:textSize="16sp" android:textStyle="bold"/>
</FrameLayout>
END

cat > android/app/src/main/res/drawable/bg_floating.xml << 'END'
<?xml version="1.0" encoding="utf-8"?><shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval"><solid android:color="#D81B60"/><stroke android:width="2dp" android:color="#FFFFFF"/></shape>
END

cat > android/app/src/main/res/values/themes.xml << 'END'
<resources><style name="Theme.H1InfiniteLove" parent="Theme.MaterialComponents.DayNight.NoActionBar"><item name="colorPrimary">#D81B60</item></style></resources>
END

cat > android/app/src/main/res/values/strings.xml << 'END'
<resources><string name="app_name">H1 Infinite Love</string></resources>
END

cat > .github/workflows/android-build.yml << 'END'
name: Android Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }
      - run: echo "Phase 02 build - Gradle wrapper in next step"
END

echo "# H1 INFINITE LOVE - Phase 02 Done" > README.md
echo "Phase 02 - Android Foundation DONE" > documentation/ROADMAP.md
echo "DONE - Phase 02 files created"
