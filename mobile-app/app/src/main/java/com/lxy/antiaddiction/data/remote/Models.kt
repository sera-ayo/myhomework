package com.lxy.antiaddiction.data.remote


data class LoginRequest(
    val username: String,
    val password: String,
)

data class UserPayload(
    val id: Int,
    val username: String,
)

data class LoginResponse(
    val token: String,
    val user: UserPayload,
)

data class DeviceRegisterRequest(
    val device_code: String,
    val brand: String,
    val model: String,
    val android_version: String,
)

data class SessionPayload(
    val package_name: String,
    val app_name: String,
    val category: String,
    val start_time: String,
    val end_time: String,
    val duration_sec: Int,
)

data class BulkUploadRequest(
    val device_code: String,
    val source: String = "android",
    val sessions: List<SessionPayload>,
)

data class BulkUploadResponse(
    val created_count: Int,
    val duplicate_count: Int,
    val processed_dates: List<String>,
    val last_sync_at: String?,
)

data class RiskLatestResponse(
    val available: Boolean = false,
    val final_score: Double? = null,
    val risk_level: String? = null,
    val reason_summary: String? = null,
)
