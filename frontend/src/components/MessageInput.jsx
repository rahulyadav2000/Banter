import { useChatStore } from "../store/chatStore";
import { useSocketStore } from "../store/socketStore";
import { useState } from "react";

function MessageInput() {
  const [content, setContent] = useState("");
  const sendMessage = useSocketStore((state) => state.sendMessage);
  const conversation = useChatStore((state) => state.selectedConversation);
  const socketStatus = useSocketStore((state) => state.status);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!conversation) return;
    const cleanContent = content.trim();
    if (!cleanContent) return;
    const success = sendMessage(conversation.id, cleanContent);
    if (success) {
      setContent("");
    }
  };
  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <input
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder={
          socketStatus === "connected" ? "Type a message" : "Connecting..."
        }
      />
      <button disabled={socketStatus !== "connected"}></button>
    </form>
  );
}

export default MessageInput;
