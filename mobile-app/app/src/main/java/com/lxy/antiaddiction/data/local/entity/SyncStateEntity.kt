package com.lxy.antiaddiction.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey


@Entity(tableName = "sync_state")
data class SyncStateEntity(
    @PrimaryKey
    val id: Int = 0,
    val lastSyncAtMillis: Long = 0,
    val lastCollectedAtMillis: Long = 0,
    val latestRiskLevel: String = "low",
    val latestRiskReason: String = "",
)
