import { defineStore } from "pinia";

import { apiRequest } from "../api/http";


type LoginResponse = {
  token: string;
  user: {
    id: number;
    username: string;
    is_staff: boolean;
    date_joined: string;
  };
};

const TOKEN_KEY = "anti-addiction-token";
const USER_KEY = "anti-addiction-user";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "" as string,
    user: null as LoginResponse["user"] | null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    restoreSession() {
      const token = window.localStorage.getItem(TOKEN_KEY);
      const rawUser = window.localStorage.getItem(USER_KEY);
      if (!token || !rawUser) {
        return;
      }
      this.token = token;
      this.user = JSON.parse(rawUser);
    },
    async login(username: string, password: string) {
      const payload = await apiRequest<LoginResponse>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      this.token = payload.token;
      this.user = payload.user;
      window.localStorage.setItem(TOKEN_KEY, payload.token);
      window.localStorage.setItem(USER_KEY, JSON.stringify(payload.user));
      return payload;
    },
    logout() {
      this.token = "";
      this.user = null;
      window.localStorage.removeItem(TOKEN_KEY);
      window.localStorage.removeItem(USER_KEY);
    },
  },
});
