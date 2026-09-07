import { useEffect } from "react";
import { useNavigate } from "react-router";

import { useAuthStore } from "../store/authStore";
import { useChatStore } from "../store/chatStore";
import { useSocketStore } from "../store/socketStore";

import ChatWindow from "../components/ChatWindow";
import ConversationSidebar from "../components/ConversationSidebar";

export default function ChatPage() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const fetchConversations = useChatStore((state) => state.fetchConversations);
  const clearChat = useChatStore((state) => state.clearMessages);

  const connect = useSocketStore((state) => state.connect);
  const disconnect = useSocketStore((state) => state.disconnect);
  const socketStatus = useSocketStore((state) => state.status);

  useEffect(() => {
    fetchConversations();
    connect();
    return () => {
      disconnect();
    };
  }, [fetchConversations, connect, disconnect]);

  const handleLogout = () => {
    disconnect();
    clearChat();
    logout();
    navigate("/login");
  };

  return (
    <div className="chat-page">
      <div className="top-bar">
        <span>
          Logged in as <strong>{user?.name}</strong>
        </span>
        <span>Socket: {socketStatus}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="chat-layout">
        <ConversationSidebar />

        <ChatWindow />
      </div>
    </div>
  );
}
