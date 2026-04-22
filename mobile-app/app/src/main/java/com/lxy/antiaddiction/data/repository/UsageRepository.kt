package com.lxy.antiaddiction.data.repository

import android.content.Context
import com.lxy.antiaddiction.collector.CapturedSession
import com.lxy.antiaddiction.collector.UsageCollector
import com.lxy.antiaddiction.data.local.AppDatabase
import com.lxy.antiaddiction.data.local.entity.SyncStateEntity
import com.lxy.antiaddiction.data.local.entity.UsageSessionEntity
import com.lxy.antiaddiction.data.remote.ApiClientFactory
import com.lxy.antiaddiction.data.remote.BulkUploadRequest
import com.lxy.antiaddiction.data.remote.DeviceRegisterRequest
import com.lxy.antiaddiction.data.remote.LoginRequest
import com.lxy.antiaddiction.data.remote.SessionPayload
import com.lxy.antiaddiction.util.DeviceInfoProvider
import com.lxy.antiaddiction.util.Prefs
import com.lxy.antiaddiction.warning.LocalRiskChecker
import com.lxy.antiaddiction.warning.WarningNotifier
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone
import java.util.concurrent.TimeUnit
import java.time.ZoneId
import java.time.ZonedDateTime


data class DashboardSummary(
    val totalDurationSec: Long,
    val lastSyncAtMillis: Long,
    val riskLevel: String,
    val riskReason: String,
    val sampleMode: Boolean,
)

data class SyncResult(
    val createdLocalCount: Int,
    val uploadedCount: Int,
    val lastSyncAtMillis: Long,
    val riskLevel: String,
    val riskReason: String,
    val message: String,
)


class UsageRepository(private val context: Context) {
    private val database = AppDatabase.getInstance(context)
    private val usageDao = database.usageSessionDao()
    private val syncStateDao = database.syncStateDao()
    private val usageCollector = UsageCollector(context)
    private val localRiskChecker = LocalRiskChecker(context)
    private val isoFormatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US).apply {
        timeZone = TimeZone.getDefault()
    }

    suspend fun login(username: String, password: String) = withContext(Dispatchers.IO) {
        val service = ApiClientFactory.create(context)
        val response = service.login(LoginRequest(username = username, password = password))
        Prefs.saveLogin(context, response.user.username, response.token)
        response
    }

    suspend fun ensureDeviceRegistered() = withContext(Dispatchers.IO) {
        val token = requireToken()
        val service = ApiClientFactory.create(context)
        service.registerDevice(
            authorization = authHeader(token),
            body = DeviceRegisterRequest(
                device_code = DeviceInfoProvider.deviceCode(context),
                brand = DeviceInfoProvider.brand(),
                model = DeviceInfoProvider.model(),
                android_version = DeviceInfoProvider.androidVersion(),
            ),
        )
    }

    suspend fun loadDashboardSummary(): DashboardSummary = withContext(Dispatchers.IO) {
        val startOfDayMillis = ZonedDateTime.now(ZoneId.systemDefault())
            .toLocalDate()
            .atStartOfDay(ZoneId.systemDefault())
            .toInstant()
            .toEpochMilli()
        val sessions = usageDao.getSessionsSince(startOfDayMillis)
        val total = sessions.sumOf { it.durationSec.toLong() }
        val state = syncStateDao.getState()
        DashboardSummary(
            totalDurationSec = total,
            lastSyncAtMillis = state?.lastSyncAtMillis ?: 0L,
            riskLevel = state?.latestRiskLevel ?: "low",
            riskReason = state?.latestRiskReason ?: "同步后会显示最新风险解释。",
            sampleMode = Prefs.getSampleMode(context),
        )
    }

    suspend fun syncNow(): SyncResult = withContext(Dispatchers.IO) {
        if (Prefs.getSampleMode(context)) {
            return@withContext SyncResult(
                createdLocalCount = 0,
                uploadedCount = 0,
                lastSyncAtMillis = System.currentTimeMillis(),
                riskLevel = "low",
                riskReason = "样例模式已开启，当前不会上传真机数据。",
                message = "样例模式下已跳过真机同步。",
            )
        }

        val currentState = syncStateDao.getState() ?: SyncStateEntity()
        val now = System.currentTimeMillis()
        val collectFrom = if (currentState.lastCollectedAtMillis > 0) {
            currentState.lastCollectedAtMillis
        } else {
            now - TimeUnit.HOURS.toMillis(24)
        }

        val capturedSessions = usageCollector.collectSessionsSince(collectFrom, now)
        val inserted = insertCapturedSessions(capturedSessions)
        localRiskChecker.inspect(capturedSessions)

        val unsynced = usageDao.getUnsynced(limit = 200)
        if (unsynced.isEmpty()) {
            val updatedState = currentState.copy(
                lastCollectedAtMillis = now,
            )
            syncStateDao.upsert(updatedState)
            return@withContext SyncResult(
                createdLocalCount = inserted,
                uploadedCount = 0,
                lastSyncAtMillis = updatedState.lastSyncAtMillis,
                riskLevel = updatedState.latestRiskLevel,
                riskReason = updatedState.latestRiskReason.ifBlank { "暂无新的同步数据。" },
                message = "未发现新的会话记录。",
            )
        }

        val token = requireToken()
        val service = ApiClientFactory.create(context)
        service.registerDevice(
            authHeader(token),
            DeviceRegisterRequest(
                device_code = DeviceInfoProvider.deviceCode(context),
                brand = DeviceInfoProvider.brand(),
                model = DeviceInfoProvider.model(),
                android_version = DeviceInfoProvider.androidVersion(),
            ),
        )

        service.uploadSessions(
            authorization = authHeader(token),
            body = BulkUploadRequest(
                device_code = DeviceInfoProvider.deviceCode(context),
                sessions = unsynced.map { it.toPayload() },
            ),
        )
        usageDao.markSynced(unsynced.map { it.id })

        val latestRisk = runCatching { service.latestRisk(authHeader(token)) }.getOrNull()
        if (latestRisk?.risk_level == "high") {
            WarningNotifier.showRiskLevelWarning(context, latestRisk.risk_level, latestRisk.reason_summary)
        }

        val updatedState = SyncStateEntity(
            id = 0,
            lastSyncAtMillis = now,
            lastCollectedAtMillis = now,
            latestRiskLevel = latestRisk?.risk_level ?: currentState.latestRiskLevel,
            latestRiskReason = latestRisk?.reason_summary ?: currentState.latestRiskReason,
        )
        syncStateDao.upsert(updatedState)

        return@withContext SyncResult(
            createdLocalCount = inserted,
            uploadedCount = unsynced.size,
            lastSyncAtMillis = now,
            riskLevel = updatedState.latestRiskLevel,
            riskReason = updatedState.latestRiskReason,
            message = "同步完成：上传 ${unsynced.size} 条会话记录。",
        )
    }

    suspend fun clearCache() = withContext(Dispatchers.IO) {
        usageDao.clearAll()
        syncStateDao.upsert(SyncStateEntity())
    }

    private suspend fun insertCapturedSessions(capturedSessions: List<CapturedSession>): Int {
        if (capturedSessions.isEmpty()) {
            return 0
        }
        val entities = capturedSessions.map {
            UsageSessionEntity(
                packageName = it.packageName,
                appName = it.appName,
                category = it.category,
                startTimeMillis = it.startTimeMillis,
                endTimeMillis = it.endTimeMillis,
                durationSec = it.durationSec,
            )
        }
        val inserted = usageDao.insertAll(entities)
        return inserted.count { it != -1L }
    }

    private fun UsageSessionEntity.toPayload(): SessionPayload {
        return SessionPayload(
            package_name = packageName,
            app_name = appName,
            category = category,
            start_time = isoFormatter.format(Date(startTimeMillis)),
            end_time = isoFormatter.format(Date(endTimeMillis)),
            duration_sec = durationSec,
        )
    }

    private fun requireToken(): String {
        return Prefs.getToken(context) ?: error("请先完成登录。")
    }

    private fun authHeader(token: String): String = "Token $token"
}
