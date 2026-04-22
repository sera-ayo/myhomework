package com.lxy.antiaddiction.warning

import android.content.Context
import com.lxy.antiaddiction.collector.AppCategoryMapper
import com.lxy.antiaddiction.collector.CapturedSession


class LocalRiskChecker(private val context: Context) {
    fun inspect(sessions: List<CapturedSession>) {
        sessions.forEach { session ->
            if (AppCategoryMapper.isEntertainment(session.category) && session.durationSec >= 45 * 60) {
                WarningNotifier.showLongSessionWarning(context, session.appName, session.durationSec)
            }
        }
    }
}
