<template>
  <AppShell title="实验结果" description="展示规则法与轻量模型对比结果，为论文实验章节提供直接材料。">
    <el-alert
      v-if="errorMessage"
      :closable="false"
      class="glass-card"
      show-icon
      type="warning"
      :title="errorMessage"
    />

    <section class="metric-grid">
      <article class="metric-card glass-card">
        <p>当前运行模式</p>
        <strong>{{ metrics?.active_model ?? "rule_engine" }}</strong>
      </article>
      <article class="metric-card glass-card">
        <p>指标文件状态</p>
        <strong>{{ metrics?.available ? "已生成" : "未生成" }}</strong>
      </article>
      <article class="metric-card glass-card">
        <p>生成时间</p>
        <strong>{{ metrics?.generated_at?.slice(0, 16).replace("T", " ") ?? "暂无" }}</strong>
      </article>
    </section>

    <section class="panel glass-card">
      <div class="panel-header">
        <div>
          <h3 class="section-title">模型对比指标</h3>
          <p class="section-subtitle">Accuracy、Precision、Recall、F1 四项展示</p>
        </div>
      </div>
      <el-table :data="metrics?.metrics ?? []" empty-text="暂无指标文件">
        <el-table-column label="模型" prop="model" min-width="220" />
        <el-table-column label="Accuracy" prop="accuracy" min-width="120" />
        <el-table-column label="Precision" prop="precision" min-width="120" />
        <el-table-column label="Recall" prop="recall" min-width="120" />
        <el-table-column label="F1" prop="f1" min-width="120" />
      </el-table>
    </section>

    <section class="panel glass-card">
      <div class="panel-header">
        <div>
          <h3 class="section-title">特征重要性</h3>
          <p class="section-subtitle">当前默认启用 RandomForestClassifier 模型</p>
        </div>
      </div>
      <BaseChart :option="featureOption" />
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { apiRequest, ApiError } from "../api/http";
import AppShell from "../components/AppShell.vue";
import BaseChart from "../components/BaseChart.vue";
import { useAuthStore } from "../stores/auth";


type MetricsResponse = {
  available: boolean;
  active_model: string;
  generated_at?: string;
  metrics: Array<{
    model: string;
    accuracy: number;
    precision: number;
    recall: number;
    f1: number;
  }>;
  feature_importance: Array<{
    feature: string;
    importance: number;
  }>;
};

const authStore = useAuthStore();
const metrics = ref<MetricsResponse | null>(null);
const errorMessage = ref("");

const featureOption = computed(() => ({
  tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
  grid: { left: 140, right: 24, top: 16, bottom: 24 },
  xAxis: { type: "value" },
  yAxis: {
    type: "category",
    data: (metrics.value?.feature_importance ?? []).map((item) => item.feature).reverse(),
  },
  series: [
    {
      type: "bar",
      data: (metrics.value?.feature_importance ?? [])
        .map((item) => item.importance)
        .reverse(),
      itemStyle: {
        color: "#0a84c6",
        borderRadius: [0, 10, 10, 0],
      },
    },
  ],
}));

async function loadData() {
  errorMessage.value = "";
  try {
    metrics.value = await apiRequest<MetricsResponse>(
      "/api/experiments/metrics",
      {},
      authStore.token,
    );
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.message : "无法加载实验指标。";
  }
}

onMounted(loadData);
</script>

<style scoped>
.metric-card,
.panel {
  padding: 24px;
  border-radius: 24px;
}

.metric-card p {
  margin: 0 0 10px;
  color: var(--text-subtle);
}

.metric-card strong {
  font-size: 28px;
}

.panel-header {
  margin-bottom: 16px;
}
</style>
