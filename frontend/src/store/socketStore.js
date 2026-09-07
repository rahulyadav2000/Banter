import { create } from "zustand";

import { useAuthStore } from "./authStore";
import { useChatStore } from "./chatStore";

const WS_URL = import.meta.env.VITE_WS_URL;

export const useSocketStore = create((set, get) => ({
  socket: null,
  status: "disconnected",
  error: null,

  connect: () => {
    const token = useAuthStore.getState().accessToken;

    if (!token) return;

    const existingSocket = get().socket;
    if (
      existingSocket?.readyState === WebSocket.OPEN ||
      existingSocket?.readyState === WebSocket.CONNECTING
    ) {
      return;
    }

    const socket = new WebSocket(
      `${WS_URL}/ws?token=${encodeURIComponent(token)}`,
    );

    set({ socket, status: "connecting", error: null });

    socket.onopen = () => {
      if (get().socket !== socket) return;
      set({ status: "connected" });
    };

    socket.onmessage = (event) => {
      let data;
      try {
        data = JSON.parse(event.data);
      } catch {
        return;
      }

      switch (data.type) {
        case "message.created":
          useChatStore.getState().receiveMessage(data.message);
          break;
        case "error":
          set({ error: data.message || "WebSocket error!" });
          break;
        default:
          break;
      }
    };

    socket.onerror = () => {
      if (get().socket !== socket) return;
      set({ error: "WebSocket connection error!" });
    };

    socket.onclose = () => {
      if (get().socket !== socket) return;
      set({ socket: null, status: "disconnected" });
    };
  },

  disconnect: () => {
    const socket = get().socket;

    if (socket) {
      socket.onclose = null;
      socket.close();
    }

    set({ socket: null, status: "disconnected", error: null });
  },

  sendMessage: (conversationId, content) => {
    const socket = get().socket;
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      set({ error: "WebSocket not connected!" });
      return false;
    }

    const cleanContent = content.trim();
    if (!cleanContent) return false;

    socket.send(
      JSON.stringify({
        type: "message.send",
        conversation_id: conversationId,
        content: cleanContent,
      }),
    );
    return true;
  },
}));
