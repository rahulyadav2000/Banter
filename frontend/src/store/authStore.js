import { create } from "zustand";
import { persist } from "zustand/middleware";

import { authRequests } from "../api/client";

export const useAuthStore = create(
  persist(
    (set, get) => ({
      accessToken: null,
      user: null,
      initialized: false,
      loading: false,
      error: null,

      login: async (email, password) => {
        set({ loading: true, error: null });
        try {
          const data = await authRequests("/auth/login", {
            method: "POST",
            body: {
              email,
              password,
            },
          });

          set({ accessToken: data.access_token });
          await get().fetchUser();
          return true;
        } catch (error) {
          set({ error: error.message });
          return false;
        } finally {
          set({ loading: false });
        }
      },

      fetchUser: async () => {
        const token = get().accessToken;

        if (!token) {
          set({ user: null, initialized: true });
          return;
        }
        try {
          const data = await authRequests("/auth/me", {
            token,
          });
          set({ user: data });
        } catch (error) {
          set({ user: null, accessToken: null, error: error.message });
        } finally {
          set({ initialized: true });
        }
      },

      logout: async () => {
        const token = get().accessToken;

        try {
          if (token) {
            await authRequests("/auth/logout", {
              method: "POST",
              token,
            });
          }
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ accessToken: null, user: null, error: null });
        }
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: "chat-auth",
      partialize: (state) => ({ accessToken: state.accessToken }),
    },
  ),
);
