package com.lxy.antiaddiction.util

import android.content.Context
import android.os.Build
import android.provider.Settings


object DeviceInfoProvider {
    fun deviceCode(context: Context): String {
        val androidId = Settings.Secure.getString(
            context.contentResolver,
            Settings.Secure.ANDROID_ID,
        ) ?: Build.MODEL
        return "android-$androidId"
    }

    fun brand(): String = Build.BRAND ?: "Unknown"

    fun model(): String = Build.MODEL ?: "Unknown"

    fun androidVersion(): String = Build.VERSION.RELEASE ?: "Unknown"
}
