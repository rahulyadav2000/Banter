import { useChatStore } from "../store/chatStore";
import { useAuthStore } from "../store/authStore";

import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

function ChatWindow() {
  const currentUser = useAuthStore((state) => state.user);
  const conversation = useChatStore((state) => state.selectedConversation);

  if (!conversation) {
    return (
      <main className="chat-window empty-chat">
        Select a conversation to start chatting
      </main>
    );
  }

  const otherUser = conversation.members
    .map((member) => member.user)
    .find((user) => user.id !== currentUser.id);

  return (
    <main className="chat-window">
      <header className="chat-header">
        <strong>{otherUser?.name}</strong>
      </header>
      <MessageList />
      <MessageInput />
    </main>
  );
}

export default ChatWindow;
