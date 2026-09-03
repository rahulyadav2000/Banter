import { useEffect } from "react";
import { useNavigate } from "react-router";

import { useAuthStore } from "../store/authStore";
import { useChatStore } from "../store/chatStore";

import ChatWindow from "../components/ChatWindow";
import ConversationSidebar from "../components/ConversationSidebar";

export default function ChatPage() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);

  const logout = useAuthStore((state) => state.logout);

  const fetchConversations = useChatStore((state) => state.fetchConversations);

  const clearChat = useChatStore((state) => state.clearMessages);

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  const handleLogout = () => {
    clearChat();
    logout();

    navigate("/login");
  };

  return (
    <div className="chat-page">
      <div className="top-bar">
        <span>
          Logged in as <strong>{user.name}</strong>
        </span>

        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="chat-layout">
        <ConversationSidebar />

        <ChatWindow />
      </div>
    </div>
  );
}
