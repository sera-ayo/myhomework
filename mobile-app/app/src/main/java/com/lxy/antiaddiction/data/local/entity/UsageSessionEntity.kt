package com.lxy.antiaddiction.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey


@Entity(
    tableName = "usage_sessions",
    indices = [
        Index(value = ["package_name", "start_time_millis", "end_time_millis"], unique = true),
    ],
)
data class UsageSessionEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    @ColumnInfo(name = "package_name")
    val packageName: String,
    @ColumnInfo(name = "app_name")
    val appName: String,
    val category: String,
    @ColumnInfo(name = "start_time_millis")
    val startTimeMillis: Long,
    @ColumnInfo(name = "end_time_millis")
    val endTimeMillis: Long,
    @ColumnInfo(name = "duration_sec")
    val durationSec: Int,
    val synced: Boolean = false,
)
