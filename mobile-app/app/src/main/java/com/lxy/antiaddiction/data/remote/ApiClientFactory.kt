package com.lxy.antiaddiction.data.remote

import android.content.Context
import com.google.gson.GsonBuilder
import com.lxy.antiaddiction.util.Prefs
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


object ApiClientFactory {
    fun create(context: Context): ApiService {
        return Retrofit.Builder()
            .baseUrl(Prefs.getServerUrl(context))
            .addConverterFactory(GsonConverterFactory.create(GsonBuilder().create()))
            .build()
            .create(ApiService::class.java)
    }
}
