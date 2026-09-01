import { create } from "zustand";

import { authRequests } from "../api/client";
import { useAuthStore } from "./authStore";

export const useChatStore = create((set, get) => ({
  conversations: [],
  selectedConversation: null,
  messages: {},
  searchResults: [],

  loadingConversations: false,
  loadingMessages: false,
  searchingUsers: false,
  sendingMessage: false,
  error: null,

  fetchConversations: async () => {
    const token = useAuthStore.getState().accessToken;

    if (!token) return;

    set({ loadingConversations: true, error: null });

    try {
      const data = await authRequests("/conversations", {
        token,
      });

      set({ data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loadingConversations: false });
    }
  },

  createConversation: async (userId) => {
    const token = useAuthStore.getState().accessToken;
    if (!token) return;

    try {
      const conversation = await authRequests("/conversations", {
        method: "POST",
        token,
        body: {
          user_id: userId,
        },
      });

      set((state) => {
        const exists = state.conversations.some(
          (item) => item.id == conversation.id,
        );
        return {
          selectedConversation: conversation,
          conversations: exists
            ? state.conversations
            : [conversation, ...state.conversations],
          searchResults: [],
        };
      });
      await get().fetchMessages(conversation.id);
      return conversation;
    } catch (error) {
      set({ error: error.message });
      return null;
    }
  },

  selectConversation: async (conversation) => {
    set({ selectedConversation: conversation });
    await get().fetchMessages(conversation.id);
  },

  searchUsers: async (query) => {
    const token = useAuthStore.getState().accessToken;

    if (!token) return;

    if (!query.trim()) {
      set({ searchResults: [] });
      return;
    }

    set({ searchingUsers: true, error: null });

    try {
      const data = await authRequests(
        `/users/search?q=${encodeURIComponent(query)}`,
        {
          token,
        },
      );
      console.log("Search results:", data);
      set({ searchResults: data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ searchingUsers: false });
    }
  },

  clearSearchResults: () => {
    set({ searchResults: [] });
  },

  fetchMessages: async (conversationId) => {
    const token = useAuthStore.getState().accessToken;

    if (!token) return;

    set({ loadingMessages: true, error: null });

    try {
      const data = await authRequests(
        `/conversations/${conversationId}/messages`,
        {
          token,
        },
      );

      set((state) => ({
        messages: { ...state.messages, [conversationId]: data },
      }));
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loadingMessages: false });
    }
  },

  sendMessage: async (content) => {
    const conversation = get().selectedConversation;
    if (!conversation) return;

    const clearContent = content.trim();
    if (!clearContent) return;

    const token = useAuthStore.getState().accessToken;
    if (!token) return;

    set({ sendingMessage: true, error: null });

    try {
      const data = await authRequests(
        `/conversations/${conversation.id}/messages`,
        {
          method: "POST",
          token,
          body: {
            content: clearContent,
          },
        },
      );

      set((state) => ({
        messages: {
          ...state.messages,
          [conversation.id]: [...(state.messages[conversation.id] || []), data],
        },
      }));
      return true;
    } catch (error) {
      set({ error: error.message });
      return false;
    } finally {
      set({ sendingMessage: false });
    }
  },

  clearMessages: () => {
    set({
      conversations: [],
      messages: {},
      selectedConversation: null,
      searchResults: [],
    });
  },
}));
