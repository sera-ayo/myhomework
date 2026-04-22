package com.lxy.antiaddiction.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.lxy.antiaddiction.R
import com.lxy.antiaddiction.collector.UsageCollector
import com.lxy.antiaddiction.util.Prefs
import com.lxy.antiaddiction.warning.WarningNotifier
import com.lxy.antiaddiction.worker.SyncWorker


class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        WarningNotifier.ensureChannel(this)
        SyncWorker.schedule(this)

        val nextActivity = when {
            !Prefs.isLoggedIn(this) -> LoginActivity::class.java
            !UsageCollector.hasUsageStatsPermission(this) -> PermissionGuideActivity::class.java
            else -> DashboardActivity::class.java
        }
        startActivity(Intent(this, nextActivity))
        finish()
    }
}
