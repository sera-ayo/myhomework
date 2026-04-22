<template>
  <AppShell title="仪表盘" description="查看最近一天的使用概览、风险分级和趋势变化。">
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
        <p>当日总使用时长</p>
        <strong>{{ formatHours(summary?.total_duration_sec) }}</strong>
      </article>
      <article class="metric-card glass-card">
        <p>近 7 日平均</p>
        <strong>{{ formatHours(summary?.seven_day_avg_duration_sec) }}</strong>
      </article>
      <article class="metric-card glass-card">
        <p>Top App</p>
        <strong>{{ summary?.top_app_name ?? "暂无" }}</strong>
      </article>
      <article class="metric-card glass-card">
        <p>风险等级</p>
        <span class="status-pill" :class="summary?.risk_level ?? 'low'">
          {{ summary?.risk_label ?? "低风险" }}
        </span>
      </article>
    </section>

    <section class="hero-panel glass-card">
      <div>
        <p class="eyebrow">Latest Insight</p>
        <h3>{{ summary?.reason_summary ?? "暂无数据，请先导入样例或同步设备数据。" }}</h3>
      </div>
      <div class="score">
        <small>综合评分</small>
        <strong>{{ summary?.final_score?.toFixed(1) ?? "0.0" }}</strong>
      </div>
    </section>

    <section class="chart-grid">
      <article class="panel glass-card">
        <div class="panel-header">
          <div>
            <h3 class="section-title">近 7 日趋势</h3>
            <p class="section-subtitle">总时长和风险评分的同步变化</p>
          </div>
        </div>
        <BaseChart :option="trendOption" />
      </article>

      <article class="panel glass-card">
        <div class="panel-header">
          <div>
            <h3 class="section-title">用途分布</h3>
            <p class="section-subtitle">娱乐、社交、学习、生活四类时间占比</p>
          </div>
        </div>
        <BaseChart :option="categoryOption" />
      </article>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { apiRequest, ApiError } from "../api/http";
import AppShell from "../components/AppShell.vue";
import BaseChart from "../components/BaseChart.vue";
import { useAuthStore } from "../stores/auth";


type SummaryResponse = {
  available: boolean;
  total_duration_sec: number;
  seven_day_avg_duration_sec: number;
  top_app_name: string;
  risk_level: "low" | "medium" | "high";
  risk_label: string;
  final_score: number;
  reason_summary: string;
};

type TrendItem = {
  date: string;
  total_duration_sec: number;
  night_duration_sec: number;
  final_score: number;
};

type CategoryResponse = {
  available: boolean;
  categories: Array<{ key: string; label: string; ratio: number }>;
};

const authStore = useAuthStore();
const summary = ref<SummaryResponse | null>(null);
const trend = ref<TrendItem[]>([]);
const categories = ref<CategoryResponse["categories"]>([]);
const errorMessage = ref("");

function formatHours(value?: number) {
  if (!value) {
    return "0.0h";
  }
  return `${(value / 3600).toFixed(1)}h`;
}

const trendOption = computed(() => ({
  tooltip: { trigger: "axis" },
  grid: { left: 36, right: 24, top: 40, bottom: 28 },
  xAxis: {
    type: "category",
    boundaryGap: false,
    data: trend.value.map((item) => item.date.slice(5)),
  },
  yAxis: [
    { type: "value", name: "时长(h)", axisLabel: { formatter: (value: number) => `${value}h` } },
    { type: "value", name: "风险分", max: 100 },
  ],
  series: [
    {
      name: "总时长",
      type: "line",
      smooth: true,
      data: trend.value.map((item) => Number((item.total_duration_sec / 3600).toFixed(2))),
      lineStyle: { width: 3, color: "#0a84c6" },
      areaStyle: { color: "rgba(10, 132, 198, 0.18)" },
    },
    {
      name: "风险评分",
      type: "line",
      yAxisIndex: 1,
      smooth: true,
      data: trend.value.map((item) => item.final_score),
      lineStyle: { width: 2, color: "#db8f2e" },
    },
  ],
}));

const categoryOption = computed(() => ({
  tooltip: { trigger: "item", formatter: "{b}: {(d)}%" },
  series: [
    {
      type: "pie",
      radius: ["45%", "72%"],
      padAngle: 4,
      itemStyle: {
        borderRadius: 14,
      },
      data: categories.value.map((item) => ({
        value: Number((item.ratio * 100).toFixed(2)),
        name: item.label,
      })),
    },
  ],
}));

async function loadData() {
  errorMessage.value = "";
  try {
    const [summaryData, trendData, categoryData] = await Promise.all([
      apiRequest<SummaryResponse>("/api/dashboard/summary", {}, authStore.token),
      apiRequest<{ items: TrendItem[] }>("/api/dashboard/trend?days=7", {}, authStore.token),
      apiRequest<CategoryResponse>("/api/dashboard/categories", {}, authStore.token),
    ]);
    summary.value = summaryData;
    trend.value = trendData.items;
    categories.value = categoryData.categories;
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.message : "无法加载仪表盘数据，请确认后端已启动。";
  }
}

onMounted(loadData);
</script>

<style scoped>
.metric-card,
.hero-panel,
.panel {
  border-radius: 24px;
}

.metric-card {
  padding: 20px 22px;
}

.metric-card p {
  margin: 0 0 10px;
  color: var(--text-subtle);
}

.metric-card strong {
  font-size: 32px;
}

.hero-panel {
  padding: 26px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.hero-panel h3 {
  margin: 0;
  font-size: 28px;
  line-height: 1.35;
}

.score {
  min-width: 160px;
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.55);
  text-align: right;
}

.score small,
.score strong {
  display: block;
}

.score small {
  color: var(--text-subtle);
}

.score strong {
  margin-top: 8px;
  font-size: 40px;
}

.panel {
  padding: 24px;
}

.panel-header {
  margin-bottom: 8px;
}

@media (max-width: 760px) {
  .hero-panel {
    flex-direction: column;
    align-items: start;
  }

  .score {
    width: 100%;
    text-align: left;
  }
}
</style>
