package com.lxy.antiaddiction.ui

import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.lxy.antiaddiction.R
import com.lxy.antiaddiction.collector.UsageCollector
import com.lxy.antiaddiction.data.repository.UsageRepository
import kotlinx.coroutines.launch


class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        val usernameInput = findViewById<TextInputEditText>(R.id.usernameInput)
        val passwordInput = findViewById<TextInputEditText>(R.id.passwordInput)
        val statusText = findViewById<TextView>(R.id.statusText)
        val loginButton = findViewById<MaterialButton>(R.id.loginButton)
        val repository = UsageRepository(this)

        loginButton.setOnClickListener {
            val username = usernameInput.text?.toString().orEmpty().trim()
            val password = passwordInput.text?.toString().orEmpty()
            loginButton.isEnabled = false
            statusText.text = "正在登录..."

            lifecycleScope.launch {
                runCatching { repository.login(username, password) }
                    .onSuccess {
                        val target = if (UsageCollector.hasUsageStatsPermission(this@LoginActivity)) {
                            DashboardActivity::class.java
                        } else {
                            PermissionGuideActivity::class.java
                        }
                        startActivity(Intent(this@LoginActivity, target))
                        finish()
                    }
                    .onFailure { throwable ->
                        loginButton.isEnabled = true
                        statusText.text = throwable.message ?: "登录失败，请检查服务地址和后端状态。"
                        Toast.makeText(
                            this@LoginActivity,
                            "登录失败：${throwable.message}",
                            Toast.LENGTH_SHORT,
                        ).show()
                    }
            }
        }
    }
}
