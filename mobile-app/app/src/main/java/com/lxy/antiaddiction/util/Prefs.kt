package com.lxy.antiaddiction.util

import android.content.Context


object Prefs {
    private const val PREFS_NAME = "anti_addiction_prefs"
    private const val KEY_TOKEN = "token"
    private const val KEY_USERNAME = "username"
    private const val KEY_SAMPLE_MODE = "sample_mode"
    private const val KEY_SERVER_URL = "server_url"

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getToken(context: Context): String? = prefs(context).getString(KEY_TOKEN, null)

    fun saveLogin(context: Context, username: String, token: String) {
        prefs(context).edit()
            .putString(KEY_USERNAME, username)
            .putString(KEY_TOKEN, token)
            .apply()
    }

    fun clearLogin(context: Context) {
        prefs(context).edit()
            .remove(KEY_USERNAME)
            .remove(KEY_TOKEN)
            .apply()
    }

    fun isLoggedIn(context: Context): Boolean = !getToken(context).isNullOrBlank()

    fun getSampleMode(context: Context): Boolean = prefs(context).getBoolean(KEY_SAMPLE_MODE, false)

    fun setSampleMode(context: Context, enabled: Boolean) {
        prefs(context).edit().putBoolean(KEY_SAMPLE_MODE, enabled).apply()
    }

    fun getServerUrl(context: Context): String {
        val value = prefs(context).getString(KEY_SERVER_URL, "http://10.0.2.2:8000/") ?: "http://10.0.2.2:8000/"
        return if (value.endsWith("/")) value else "$value/"
    }

    fun setServerUrl(context: Context, value: String) {
        val raw = value.ifBlank { "http://10.0.2.2:8000/" }
        val normalized = if (raw.endsWith("/")) raw else "$raw/"
        prefs(context).edit().putString(KEY_SERVER_URL, normalized).apply()
    }
}
