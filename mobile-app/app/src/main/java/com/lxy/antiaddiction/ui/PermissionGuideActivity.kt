package com.lxy.antiaddiction.ui

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.lxy.antiaddiction.R
import com.lxy.antiaddiction.collector.UsageCollector


class PermissionGuideActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_permission_guide)

        val openSettingsButton = findViewById<MaterialButton>(R.id.openSettingsButton)
        val checkPermissionButton = findViewById<MaterialButton>(R.id.checkPermissionButton)

        openSettingsButton.setOnClickListener {
            startActivity(Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS))
        }

        checkPermissionButton.setOnClickListener {
            if (UsageCollector.hasUsageStatsPermission(this)) {
                startActivity(Intent(this, DashboardActivity::class.java))
                finish()
            } else {
                Toast.makeText(this, "尚未检测到 Usage Access 授权。", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
