package com.lxy.antiaddiction.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.lxy.antiaddiction.data.local.entity.SyncStateEntity


@Dao
interface SyncStateDao {
    @Query("SELECT * FROM sync_state WHERE id = 0 LIMIT 1")
    suspend fun getState(): SyncStateEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(state: SyncStateEntity)
}
