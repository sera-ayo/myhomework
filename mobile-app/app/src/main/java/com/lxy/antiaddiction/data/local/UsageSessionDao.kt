package com.lxy.antiaddiction.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.lxy.antiaddiction.data.local.entity.UsageSessionEntity


@Dao
interface UsageSessionDao {
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertAll(sessions: List<UsageSessionEntity>): List<Long>

    @Query("SELECT * FROM usage_sessions WHERE synced = 0 ORDER BY start_time_millis ASC LIMIT :limit")
    suspend fun getUnsynced(limit: Int): List<UsageSessionEntity>

    @Query("UPDATE usage_sessions SET synced = 1 WHERE id IN (:ids)")
    suspend fun markSynced(ids: List<Long>)

    @Query("SELECT * FROM usage_sessions WHERE start_time_millis >= :sinceMillis ORDER BY start_time_millis DESC")
    suspend fun getSessionsSince(sinceMillis: Long): List<UsageSessionEntity>

    @Query("DELETE FROM usage_sessions")
    suspend fun clearAll()
}
