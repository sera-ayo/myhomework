package com.lxy.antiaddiction.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST


interface ApiService {
    @POST("api/auth/login")
    suspend fun login(@Body body: LoginRequest): LoginResponse

    @POST("api/devices/register")
    suspend fun registerDevice(
        @Header("Authorization") authorization: String,
        @Body body: DeviceRegisterRequest,
    )

    @POST("api/usage/sessions/bulk")
    suspend fun uploadSessions(
        @Header("Authorization") authorization: String,
        @Body body: BulkUploadRequest,
    ): BulkUploadResponse

    @GET("api/risk/latest")
    suspend fun latestRisk(
        @Header("Authorization") authorization: String,
    ): RiskLatestResponse
}
