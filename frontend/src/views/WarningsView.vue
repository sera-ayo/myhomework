<template>
  <AppShell title="预警中心" description="查看最新风险解释，以及系统生成的历史预警记录。">
    <el-alert
      v-if="errorMessage"
      :closable="false"
      class="glass-card"
      show-icon
      type="warning"
      :title="errorMessage"
    />

    <section class="latest glass-card">
      <div>
        <p class="eyebrow">Latest Risk Result</p>
        <h3>最近一次风险评估</h3>
        <p class="summary">{{ risk?.reason_summary ?? "暂无风险评估结果。" }}</p>
      </div>
      <div class="latest-score">
        <span class="status-pill" :class="risk?.risk_level ?? 'low'">
          {{ riskLabel }}
        </span>
        <strong>{{ risk?.final_score?.toFixed(1) ?? "0.0" }}</strong>
      </div>
    </section>

    <section class="panel glass-card">
      <div class="panel-header">
        <div>
          <h3 class="section-title">触发原因</h3>
          <p class="section-subtitle">系统按分值贡献高低给出可解释原因</p>
        </div>
      </div>
      <div class="reason-grid">
        <article v-for="reason in risk?.top_reasons_json ?? []" :key="reason.key" class="reason-card">
          <strong>+{{ reason.points }}</strong>
          <p>{{ reason.detail }}</p>
        </article>
      </div>
    </section>

    <section class="panel glass-card">
      <div class="panel-header">
        <div>
          <h3 class="section-title">历史预警记录</h3>
          <p class="section-subtitle">支持老师答辩时按条解释系统如何输出柔性干预建议</p>
        </div>
      </div>
      <el-table :data="warnings" empty-text="暂无预警记录">
        <el-table-column label="时间" prop="warning_time" min-width="180" />
        <el-table-column label="等级" min-width="110">
          <template #default="{ row }">
            <span class="status-pill" :class="row.risk_level">
              {{ levelLabel(row.risk_level) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="原因" prop="reason_text" min-width="280" />
        <el-table-column label="建议" prop="action_text" min-width="260" />
      </el-table>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { apiRequest, ApiError } from "../api/http";
import AppShell from "../components/AppShell.vue";
import { useAuthStore } from "../stores/auth";


type RiskResult = {
  available: boolean;
  final_score: number;
  risk_level: "low" | "medium" | "high";
  reason_summary: string;
  top_reasons_json: Array<{ key: string; points: number; detail: string }>;
};

type WarningItem = {
  id: number;
  warning_time: string;
  risk_level: "low" | "medium" | "high";
  reason_text: string;
  action_text: string;
};

const authStore = useAuthStore();
const risk = ref<RiskResult | null>(null);
const warnings = ref<WarningItem[]>([]);
const errorMessage = ref("");

const riskLabel = computed(() => levelLabel(risk.value?.risk_level ?? "low"));

function levelLabel(level: string) {
  if (level === "high") {
    return "高风险";
  }
  if (level === "medium") {
    return "中风险";
  }
  return "低风险";
}

async function loadData() {
  errorMessage.value = "";
  try {
    const [riskData, warningData] = await Promise.all([
      apiRequest<RiskResult>("/api/risk/latest", {}, authStore.token),
      apiRequest<{ items: WarningItem[] }>("/api/warnings/list", {}, authStore.token),
    ]);
    risk.value = riskData;
    warnings.value = warningData.items;
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.message : "无法加载预警中心数据。";
  }
}

onMounted(loadData);
</script>

<style scoped>
.latest,
.panel {
  border-radius: 24px;
  padding: 24px;
}

.latest {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.latest h3 {
  margin: 0 0 10px;
  font-size: 28px;
}

.summary {
  margin: 0;
  color: var(--text-subtle);
  line-height: 1.8;
}

.latest-score {
  min-width: 180px;
  display: grid;
  justify-items: end;
  gap: 12px;
}

.latest-score strong {
  font-size: 46px;
}

.panel-header {
  margin-bottom: 18px;
}

.reason-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.reason-card {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.55);
}

.reason-card strong {
  font-size: 26px;
  color: var(--accent);
}

.reason-card p {
  margin: 10px 0 0;
  color: var(--text-subtle);
  line-height: 1.7;
}

@media (max-width: 760px) {
  .latest {
    flex-direction: column;
    align-items: start;
  }

  .latest-score {
    justify-items: start;
  }
}
</style>
