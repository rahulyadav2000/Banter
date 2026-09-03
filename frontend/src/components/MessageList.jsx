import { useChatStore } from "../store/chatStore";
import { useAuthStore } from "../store/authStore";

function MessageList() {
  const currentUser = useAuthStore((state) => state.user);
  const conversation = useChatStore((state) => state.selectedConversation);
  const allMessages = useChatStore((state) => state.messages);
  const loading = useChatStore((state) => state.loadingMessages);

  if (!conversation) return null;
  const messages = allMessages[conversation.id] || [];
  console.log("Messages:", messages);
  if (loading) {
    return <div className="message-list">loading messages...</div>;
  }

  return (
    <div className="message-list">
      {messages.map((message) => {
        const mine = message.user_id === currentUser.id;
        return (
          <div
            key={message.id}
            className={mine ? "message-row mine" : "message-row"}
          >
            <div className="message-bubble">
              <div>{message.content}</div>
              <small>
                {new Date(message.created_at).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </small>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default MessageList;
