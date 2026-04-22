package com.lxy.antiaddiction.ui

import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.lxy.antiaddiction.R
import com.lxy.antiaddiction.data.repository.UsageRepository
import com.lxy.antiaddiction.worker.SyncWorker


class DashboardActivity : AppCompatActivity() {
    private val viewModel: DashboardViewModel by viewModels {
        DashboardViewModelFactory(UsageRepository(this))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)
        SyncWorker.schedule(this)

        val todayUsageText = findViewById<TextView>(R.id.todayUsageText)
        val riskLevelText = findViewById<TextView>(R.id.riskLevelText)
        val reasonText = findViewById<TextView>(R.id.reasonText)
        val lastSyncText = findViewById<TextView>(R.id.lastSyncText)
        val statusMessageText = findViewById<TextView>(R.id.statusMessageText)
        val syncNowButton = findViewById<MaterialButton>(R.id.syncNowButton)
        val settingsButton = findViewById<MaterialButton>(R.id.settingsButton)
        val permissionButton = findViewById<MaterialButton>(R.id.permissionButton)

        viewModel.state.observe(this) { state ->
            todayUsageText.text = state.todayUsage
            riskLevelText.text = state.riskLevelText
            reasonText.text = state.reasonText
            lastSyncText.text = state.lastSyncText
            statusMessageText.text = state.statusMessage
            syncNowButton.isEnabled = !state.sampleMode
        }

        syncNowButton.setOnClickListener { viewModel.syncNow() }
        settingsButton.setOnClickListener {
            startActivity(Intent(this, SyncSettingsActivity::class.java))
        }
        permissionButton.setOnClickListener {
            startActivity(Intent(this, PermissionGuideActivity::class.java))
        }
    }

    override fun onResume() {
        super.onResume()
        viewModel.refresh()
    }
}
