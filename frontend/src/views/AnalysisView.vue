<template>
  <AppShell title="行为画像" description="从更长时间窗口观察夜间使用、用途分布和风险波动。">
    <el-alert
      v-if="errorMessage"
      :closable="false"
      class="glass-card"
      show-icon
      type="warning"
      :title="errorMessage"
    />

    <section class="chart-grid">
      <article class="panel glass-card">
        <h3 class="section-title">近 30 日总时长</h3>
        <p class="section-subtitle">观察整体使用趋势和高峰期</p>
        <BaseChart :option="durationOption" />
      </article>

      <article class="panel glass-card">
        <h3 class="section-title">夜间使用对比</h3>
        <p class="section-subtitle">重点关注 22:00 后的持续使用行为</p>
        <BaseChart :option="nightOption" />
      </article>
    </section>

    <section class="chart-grid">
      <article class="panel glass-card">
        <h3 class="section-title">最新用途分布</h3>
        <p class="section-subtitle">用类别和时段近似描述用户使用目的</p>
        <BaseChart :option="categoryOption" />
      </article>

      <article class="panel glass-card insight-panel">
        <h3 class="section-title">分析提示</h3>
        <p class="insight" v-for="item in insights" :key="item">{{ item }}</p>
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
const trend = ref<TrendItem[]>([]);
const categories = ref<CategoryResponse["categories"]>([]);
const errorMessage = ref("");

const durationOption = computed(() => ({
  tooltip: { trigger: "axis" },
  xAxis: {
    type: "category",
    data: trend.value.map((item) => item.date.slice(5)),
  },
  yAxis: { type: "value", axisLabel: { formatter: (value: number) => `${value}h` } },
  series: [
    {
      type: "bar",
      data: trend.value.map((item) => Number((item.total_duration_sec / 3600).toFixed(2))),
      itemStyle: { color: "#0a84c6", borderRadius: [10, 10, 0, 0] },
    },
  ],
}));

const nightOption = computed(() => ({
  tooltip: { trigger: "axis" },
  legend: { top: 0 },
  xAxis: { type: "category", data: trend.value.map((item) => item.date.slice(5)) },
  yAxis: [
    { type: "value", axisLabel: { formatter: (value: number) => `${value}h` } },
    { type: "value", max: 100, name: "风险分" },
  ],
  series: [
    {
      name: "夜间使用",
      type: "line",
      smooth: true,
      data: trend.value.map((item) => Number((item.night_duration_sec / 3600).toFixed(2))),
      lineStyle: { color: "#db8f2e", width: 3 },
    },
    {
      name: "风险评分",
      type: "line",
      yAxisIndex: 1,
      smooth: true,
      data: trend.value.map((item) => item.final_score),
      lineStyle: { color: "#c45c42", width: 2 },
    },
  ],
}));

const categoryOption = computed(() => ({
  radar: {
    indicator: categories.value.map((item) => ({ name: item.label, max: 1 })),
    radius: 90,
  },
  series: [
    {
      type: "radar",
      data: [
        {
          value: categories.value.map((item) => Number(item.ratio.toFixed(3))),
          areaStyle: { color: "rgba(10, 132, 198, 0.16)" },
          lineStyle: { color: "#0a84c6", width: 2 },
        },
      ],
    },
  ],
}));

const insights = computed(() => {
  if (!trend.value.length || !categories.value.length) {
    return ["当前暂无足够数据，导入样例或同步设备后可自动生成画像分析。"];
  }

  const latest = trend.value[trend.value.length - 1];
  const nightRatio = latest.total_duration_sec
    ? latest.night_duration_sec / latest.total_duration_sec
    : 0;
  const entertainment = categories.value.find((item) => item.key === "entertainment")?.ratio ?? 0;
  const study = categories.value.find((item) => item.key === "study")?.ratio ?? 0;

  return [
    `最近一天总使用时长约 ${(latest.total_duration_sec / 3600).toFixed(1)} 小时，综合风险分 ${latest.final_score.toFixed(1)}。`,
    `夜间使用占比约 ${(nightRatio * 100).toFixed(1)}%，适合写入论文中的作息风险分析。`,
    `娱乐类占比 ${(entertainment * 100).toFixed(1)}%，学习类占比 ${(study * 100).toFixed(1)}%，可作为“使用目的近似刻画”的展示证据。`,
  ];
});

async function loadData() {
  errorMessage.value = "";
  try {
    const [trendData, categoryData] = await Promise.all([
      apiRequest<{ items: TrendItem[] }>("/api/dashboard/trend?days=30", {}, authStore.token),
      apiRequest<CategoryResponse>("/api/dashboard/categories", {}, authStore.token),
    ]);
    trend.value = trendData.items;
    categories.value = categoryData.categories;
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.message : "无法加载行为画像数据。";
  }
}

onMounted(loadData);
</script>

<style scoped>
.panel {
  padding: 24px;
  border-radius: 24px;
}

.insight-panel {
  display: grid;
  align-content: start;
  gap: 14px;
}

.insight {
  margin: 0;
  padding: 16px 18px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.55);
  color: var(--text-subtle);
  line-height: 1.8;
}
</style>
