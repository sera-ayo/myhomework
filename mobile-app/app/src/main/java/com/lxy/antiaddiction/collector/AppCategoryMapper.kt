package com.lxy.antiaddiction.collector


object AppCategoryMapper {
    private val knownMap = mapOf(
        "com.ss.android.ugc.aweme" to "short_video",
        "tv.danmaku.bili" to "video_music",
        "com.netease.cloudmusic" to "video_music",
        "com.tencent.mm" to "social",
        "com.tencent.mobileqq" to "social",
        "com.zhihu.android" to "social",
        "cn.wps.moffice_eng" to "study",
        "com.notion.id" to "study",
        "com.android.chrome" to "tool",
        "com.eg.android.AlipayGphone" to "shopping",
        "com.taobao.taobao" to "shopping",
    )

    fun resolveCategory(packageName: String, appName: String): String {
        return knownMap[packageName] ?: when {
            appName.contains("微信") || appName.contains("QQ") -> "social"
            appName.contains("抖音") || appName.contains("快手") -> "short_video"
            appName.contains("WPS") || appName.contains("Notion") -> "study"
            else -> "other"
        }
    }

    fun isEntertainment(category: String): Boolean {
        return category in setOf("short_video", "video_music", "game")
    }
}
