<template>
  <main class="login-page page-shell">
    <section class="panel glass-card">
      <div class="copy">
        <p class="eyebrow">Android + Django + Vue</p>
        <h1>基于手机软件使用行为的网络防沉迷预警系统</h1>
        <p>
          当前为单用户演示模式。使用内置 Demo 账号即可进入系统，查看行为画像、风险分级和实验结果。
        </p>
      </div>

      <el-form class="form" label-position="top" @submit.prevent="handleSubmit">
        <el-form-item label="用户名">
          <el-input v-model="username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" show-password />
        </el-form-item>
        <p class="hint">默认账号：`demo` / `demo123456`</p>
        <el-alert v-if="errorMessage" :closable="false" show-icon type="error" :title="errorMessage" />
        <el-button class="submit" :loading="loading" native-type="submit" type="primary">
          进入系统
        </el-button>
      </el-form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import { ref } from "vue";
import { useRouter } from "vue-router";

import { ApiError } from "../api/http";
import { useAuthStore } from "../stores/auth";


const username = ref("demo");
const password = ref("demo123456");
const loading = ref(false);
const errorMessage = ref("");

const router = useRouter();
const authStore = useAuthStore();

async function handleSubmit() {
  loading.value = true;
  errorMessage.value = "";
  try {
    await authStore.login(username.value, password.value);
    ElMessage.success("登录成功");
    await router.push({ name: "dashboard" });
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.message : "登录失败，请检查后端服务状态。";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  display: grid;
  place-items: center;
}

.panel {
  width: min(980px, 100%);
  border-radius: 32px;
  padding: 36px;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 28px;
}

.copy h1 {
  margin: 0 0 16px;
  font-size: clamp(36px, 5vw, 60px);
  line-height: 1.05;
}

.copy p {
  margin: 0;
  color: var(--text-subtle);
  font-size: 18px;
  line-height: 1.8;
}

.form {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.5);
}

.hint {
  margin: 0 0 16px;
  color: var(--text-subtle);
}

.submit {
  width: 100%;
  margin-top: 18px;
  height: 46px;
}

@media (max-width: 900px) {
  .panel {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  .copy h1 {
    font-size: 36px;
  }
}
</style>
