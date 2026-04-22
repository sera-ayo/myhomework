import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "../stores/auth";


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
      meta: { public: true },
    },
    {
      path: "/",
      redirect: "/dashboard",
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: () => import("../views/DashboardView.vue"),
    },
    {
      path: "/analysis",
      name: "analysis",
      component: () => import("../views/AnalysisView.vue"),
    },
    {
      path: "/warnings",
      name: "warnings",
      component: () => import("../views/WarningsView.vue"),
    },
    {
      path: "/experiments",
      name: "experiments",
      component: () => import("../views/ExperimentsView.vue"),
    },
  ],
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (!to.meta.public && !authStore.isAuthenticated) {
    return { name: "login" };
  }
  if (to.name === "login" && authStore.isAuthenticated) {
    return { name: "dashboard" };
  }
  return true;
});

export default router;
