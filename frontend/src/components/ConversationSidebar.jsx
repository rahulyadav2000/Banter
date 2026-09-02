import { useAuthStore } from "../store/authStore";
import { useChatStore } from "../store/chatStore";

import UserSearchComp from "./userSearchComp";

function ConversationSidebar() {
  const currentUser = useAuthStore((state) => state.user);
  const conversations = useChatStore((state) => state.conversations);
  const selectedConversation = useChatStore(
    (state) => state.selectedConversation,
  );
  const selectConversation = useChatStore((state) => state.selectConversation);

  const getOtherUser = (conversation) => {
    return conversation.members
      .map((member) => member.user)
      .find((user) => user.id !== currentUser.id);
  };

  return (
    <aside className="conversation-sidebar">
      <UserSearchComp />
      <div className="conversation-list">
        {conversations.map((convo) => {
          const otherUser = getOtherUser(convo);
          console.log("Other User:", otherUser); // Debugging line
          return (
            <button
              key={convo.id}
              className={
                selectedConversation?.id === convo.id
                  ? "conversation-active"
                  : "conversation"
              }
              onClick={() => selectConversation(convo)}
            >
              {otherUser.name || "Unknown User"}
            </button>
          );
        })}
      </div>
    </aside>
  );
}

export default ConversationSidebar;
