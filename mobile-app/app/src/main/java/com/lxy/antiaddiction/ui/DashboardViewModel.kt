package com.lxy.antiaddiction.ui

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.lxy.antiaddiction.data.repository.DashboardSummary
import com.lxy.antiaddiction.data.repository.UsageRepository
import com.lxy.antiaddiction.util.TimeFormatters
import kotlinx.coroutines.launch


data class DashboardUiState(
    val todayUsage: String = "0.0 小时",
    val lastSyncText: String = "尚未同步",
    val riskLevelText: String = "低风险",
    val reasonText: String = "同步后会显示风险解释。",
    val statusMessage: String = "",
    val sampleMode: Boolean = false,
)


class DashboardViewModel(private val repository: UsageRepository) : ViewModel() {
    private val _state = MutableLiveData(DashboardUiState())
    val state: LiveData<DashboardUiState> = _state

    fun refresh() {
        viewModelScope.launch {
            val summary = repository.loadDashboardSummary()
            _state.value = summary.toUiState(statusMessage = if (summary.sampleMode) "当前为样例模式，真机同步已暂停。" else "")
        }
    }

    fun syncNow() {
        viewModelScope.launch {
            _state.value = _state.value?.copy(statusMessage = "正在采集并同步数据...")
            val result = repository.syncNow()
            val summary = repository.loadDashboardSummary()
            _state.value = summary.toUiState(statusMessage = result.message)
        }
    }

    private fun DashboardSummary.toUiState(statusMessage: String): DashboardUiState {
        val riskText = when (riskLevel) {
            "high" -> "高风险"
            "medium" -> "中风险"
            else -> "低风险"
        }
        return DashboardUiState(
            todayUsage = TimeFormatters.hoursText(totalDurationSec),
            lastSyncText = "最近同步：${TimeFormatters.dateTimeText(lastSyncAtMillis)}",
            riskLevelText = riskText,
            reasonText = riskReason,
            statusMessage = statusMessage,
            sampleMode = sampleMode,
        )
    }
}


class DashboardViewModelFactory(
    private val repository: UsageRepository,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return DashboardViewModel(repository) as T
    }
}
