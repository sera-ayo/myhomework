package com.lxy.antiaddiction.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.lxy.antiaddiction.data.local.entity.SyncStateEntity
import com.lxy.antiaddiction.data.local.entity.UsageSessionEntity


@Database(
    entities = [UsageSessionEntity::class, SyncStateEntity::class],
    version = 1,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun usageSessionDao(): UsageSessionDao
    abstract fun syncStateDao(): SyncStateDao

    companion object {
        @Volatile
        private var instance: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "anti_addiction.db",
                ).fallbackToDestructiveMigration().build().also { instance = it }
            }
        }
    }
}
