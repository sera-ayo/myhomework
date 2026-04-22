package com.lxy.antiaddiction.collector

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Process
import androidx.core.content.ContextCompat
import java.util.Locale


data class CapturedSession(
    val packageName: String,
    val appName: String,
    val category: String,
    val startTimeMillis: Long,
    val endTimeMillis: Long,
    val durationSec: Int,
)


class UsageCollector(private val context: Context) {
    private val usageStatsManager =
        context.getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
    private val packageManager: PackageManager = context.packageManager

    fun hasPermission(): Boolean = hasUsageStatsPermission(context)

    fun collectSessionsSince(startMillis: Long, endMillis: Long): List<CapturedSession> {
        if (!hasPermission() || endMillis <= startMillis) {
            return emptyList()
        }

        val events = usageStatsManager.queryEvents(startMillis, endMillis)
        val activeStarts = mutableMapOf<String, Long>()
        val result = mutableListOf<CapturedSession>()
        val event = UsageEvents.Event()

        while (events.hasNextEvent()) {
            events.getNextEvent(event)
            val packageName = event.packageName ?: continue
            if (shouldIgnorePackage(packageName)) {
                continue
            }

            when (event.eventType) {
                UsageEvents.Event.MOVE_TO_FOREGROUND,
                UsageEvents.Event.ACTIVITY_RESUMED -> {
                    activeStarts[packageName] = event.timeStamp
                }

                UsageEvents.Event.MOVE_TO_BACKGROUND,
                UsageEvents.Event.ACTIVITY_PAUSED -> {
                    val startedAt = activeStarts.remove(packageName) ?: continue
                    buildSession(packageName, startedAt, event.timeStamp)?.let(result::add)
                }
            }
        }

        for ((packageName, startedAt) in activeStarts) {
            buildSession(packageName, startedAt, endMillis)?.let(result::add)
        }

        return result.sortedBy { it.startTimeMillis }
    }

    private fun buildSession(packageName: String, startedAt: Long, endedAt: Long): CapturedSession? {
        if (endedAt <= startedAt) {
            return null
        }
        val durationSec = ((endedAt - startedAt) / 1000L).toInt()
        if (durationSec < 10) {
            return null
        }

        val appName = try {
            val label = packageManager.getApplicationLabel(
                packageManager.getApplicationInfo(packageName, 0),
            )
            label.toString()
        } catch (_: Exception) {
            packageName
        }

        val category = AppCategoryMapper.resolveCategory(packageName, appName)
        return CapturedSession(
            packageName = packageName,
            appName = appName,
            category = category,
            startTimeMillis = startedAt,
            endTimeMillis = endedAt,
            durationSec = durationSec,
        )
    }

    private fun shouldIgnorePackage(packageName: String): Boolean {
        val normalized = packageName.lowercase(Locale.ROOT)
        return normalized == context.packageName ||
            normalized.startsWith("com.android.systemui") ||
            normalized.startsWith("com.google.android.permissioncontroller") ||
            normalized.startsWith("com.android.launcher")
    }

    companion object {
        fun hasUsageStatsPermission(context: Context): Boolean {
            val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
            val mode = appOps.checkOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                context.packageName,
            )
            return mode == AppOpsManager.MODE_ALLOWED
        }
    }
}
