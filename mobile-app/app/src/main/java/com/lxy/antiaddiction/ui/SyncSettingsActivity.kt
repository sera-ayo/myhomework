package com.lxy.antiaddiction.ui

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.android.material.button.MaterialButton
import com.google.android.material.switchmaterial.SwitchMaterial
import com.google.android.material.textfield.TextInputEditText
import com.lxy.antiaddiction.R
import com.lxy.antiaddiction.data.repository.UsageRepository
import com.lxy.antiaddiction.util.DeviceInfoProvider
import com.lxy.antiaddiction.util.Prefs
import kotlinx.coroutines.launch


class SyncSettingsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sync_settings)

        val repository = UsageRepository(this)
        val deviceCodeText = findViewById<TextView>(R.id.deviceCodeText)
        val serverUrlInput = findViewById<TextInputEditText>(R.id.serverUrlInput)
        val sampleModeSwitch = findViewById<SwitchMaterial>(R.id.sampleModeSwitch)
        val manualSyncButton = findViewById<MaterialButton>(R.id.manualSyncButton)
        val clearCacheButton = findViewById<MaterialButton>(R.id.clearCacheButton)

        deviceCodeText.text = "设备标识：${DeviceInfoProvider.deviceCode(this)}"
        serverUrlInput.setText(Prefs.getServerUrl(this))
        sampleModeSwitch.isChecked = Prefs.getSampleMode(this)

        sampleModeSwitch.setOnCheckedChangeListener { _, isChecked ->
            Prefs.setSampleMode(this, isChecked)
        }

        manualSyncButton.setOnClickListener {
            Prefs.setServerUrl(this, serverUrlInput.text?.toString().orEmpty().trim())
            lifecycleScope.launch {
                runCatching { repository.syncNow() }
                    .onSuccess {
                        Toast.makeText(this@SyncSettingsActivity, it.message, Toast.LENGTH_SHORT).show()
                    }
                    .onFailure {
                        Toast.makeText(
                            this@SyncSettingsActivity,
                            "同步失败：${it.message}",
                            Toast.LENGTH_SHORT,
                        ).show()
                    }
            }
        }

        clearCacheButton.setOnClickListener {
            lifecycleScope.launch {
                repository.clearCache()
                Toast.makeText(this@SyncSettingsActivity, "本地缓存已清空。", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
