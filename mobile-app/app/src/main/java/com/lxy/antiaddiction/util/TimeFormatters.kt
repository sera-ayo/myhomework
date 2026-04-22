package com.lxy.antiaddiction.util

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale


object TimeFormatters {
    private val dateTimeFormatter = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.CHINA)

    fun hoursText(totalSeconds: Long): String = String.format(Locale.CHINA, "%.1f 小时", totalSeconds / 3600f)

    fun dateTimeText(timestampMillis: Long?): String {
        if (timestampMillis == null || timestampMillis <= 0L) {
            return "尚未同步"
        }
        return dateTimeFormatter.format(Date(timestampMillis))
    }
}
