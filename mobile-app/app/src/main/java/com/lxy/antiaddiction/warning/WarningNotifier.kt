package com.lxy.antiaddiction.warning

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.lxy.antiaddiction.R


object WarningNotifier {
    private const val CHANNEL_ID = "usage_warning_channel"

    fun ensureChannel(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            return
        }
        val manager = context.getSystemService(NotificationManager::class.java)
        val channel = NotificationChannel(
            CHANNEL_ID,
            context.getString(R.string.notification_channel_name),
            NotificationManager.IMPORTANCE_DEFAULT,
        ).apply {
            description = context.getString(R.string.notification_channel_desc)
        }
        manager.createNotificationChannel(channel)
    }

    fun showLongSessionWarning(context: Context, appName: String, durationSec: Int) {
        val content = "$appName 已连续使用 ${durationSec / 60} 分钟，建议休息 5 分钟。"
        showNotification(context, 101, "本地长时使用提醒", content)
    }

    fun showRiskLevelWarning(context: Context, riskLevel: String, reason: String?) {
        val title = when (riskLevel) {
            "high" -> "今日风险偏高"
            "medium" -> "今日需要关注"
            else -> "风险状态更新"
        }
        val content = reason ?: "请关注近期的娱乐类使用和夜间使用行为。"
        showNotification(context, 102, title, content)
    }

    private fun showNotification(context: Context, notificationId: Int, title: String, content: String) {
        ensureChannel(context)
        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(content)
            .setStyle(NotificationCompat.BigTextStyle().bigText(content))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()
        NotificationManagerCompat.from(context).notify(notificationId, notification)
    }
}
