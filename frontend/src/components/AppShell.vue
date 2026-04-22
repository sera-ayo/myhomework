<template>
  <div class="shell page-shell">
    <aside class="sidebar glass-card">
      <div class="brand">
        <p class="eyebrow">Digital Wellbeing</p>
        <h1>网络防沉迷预警系统</h1>
      </div>

      <nav class="nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          class="nav-link"
          :class="{ active: route.path === item.to }"
          :to="item.to"
        >
          <span>{{ item.label }}</span>
          <small>{{ item.caption }}</small>
        </RouterLink>
      </nav>

      <section class="account glass-card">
        <p class="account-label">当前账号</p>
        <strong>{{ authStore.user?.username ?? "未登录" }}</strong>
        <button class="logout" type="button" @click="handleLogout">退出登录</button>
      </section>
    </aside>

    <main class="content">
      <header class="topbar glass-card">
        <div>
          <p class="eyebrow">Graduation Project Prototype</p>
          <h2>{{ title }}</h2>
        </div>
        <p class="topbar-note">{{ description }}</p>
      </header>

      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRoute, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";


defineProps<{
  title: string;
  description: string;
}>();

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const navItems = [
  { to: "/dashboard", label: "仪表盘", caption: "今日概览与趋势" },
  { to: "/analysis", label: "行为画像", caption: "时段、类别与习惯分析" },
  { to: "/warnings", label: "预警中心", caption: "风险原因与历史记录" },
  { to: "/experiments", label: "实验结果", caption: "模型对比与指标展示" },
];

function handleLogout() {
  authStore.logout();
  router.push({ name: "login" });
}
</script>

<style scoped>
.shell {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 20px;
}

.sidebar {
  position: sticky;
  top: 24px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 24px;
  border-radius: 28px;
}

.brand h1,
.topbar h2 {
  margin: 0;
  font-size: clamp(26px, 3vw, 36px);
  line-height: 1.15;
}

.eyebrow {
  margin: 0 0 8px;
  color: #6a87a2;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.nav {
  display: grid;
  gap: 10px;
}

.nav-link {
  display: block;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid rgba(163, 181, 204, 0.2);
}

.nav-link span,
.nav-link small {
  display: block;
}

.nav-link span {
  font-weight: 700;
}

.nav-link small {
  margin-top: 4px;
  color: #5e7691;
}

.nav-link.active {
  background: linear-gradient(135deg, rgba(10, 132, 198, 0.14), rgba(255, 183, 77, 0.16));
  border-color: rgba(10, 132, 198, 0.18);
}

.account {
  margin-top: auto;
  padding: 18px;
  border-radius: 20px;
}

.account-label {
  margin: 0 0 6px;
  color: #6a87a2;
  font-size: 13px;
}

.logout {
  margin-top: 14px;
  width: 100%;
  border: 0;
  border-radius: 14px;
  padding: 12px 14px;
  background: #102033;
  color: white;
  cursor: pointer;
}

.content {
  display: grid;
  gap: 20px;
}

.topbar {
  padding: 24px 28px;
  border-radius: 28px;
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 20px;
}

.topbar-note {
  margin: 0;
  max-width: 420px;
  color: #54708d;
  line-height: 1.7;
}

@media (max-width: 1080px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .topbar {
    flex-direction: column;
    align-items: start;
  }
}
</style>
