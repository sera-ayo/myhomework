import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import "./style.css";
import { useAuthStore } from "./stores/auth";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(ElementPlus);

const authStore = useAuthStore();
authStore.restoreSession();

app.mount("#app");
