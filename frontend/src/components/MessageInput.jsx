import { useChatStore } from "../store/chatStore";
import { useState } from "react";

function MessageInput() {
  const [content, setContent] = useState("");
  const sendMessage = useChatStore((state) => state.sendMessage);
  const sending = useChatStore((state) => state.sending);

  const handleSubmit = (e) => {
    e.preventDefault();
    const cleanContent = content.trim();
    if (!cleanContent) return;
    const success = sendMessage(cleanContent);
    if (success) {
      setContent("");
    }
  };
  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <input
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Type your message here..."
      />
      <button disabled={sending || !content.trim()}>↑</button>
    </form>
  );
}

export default MessageInput;
