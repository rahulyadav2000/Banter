import { useState, useEffect } from "react";
import { useChatStore } from "../store/chatStore";

function UserSearchComp() {
  const [query, setQuery] = useState("");

  const searchResults = useChatStore((state) => state.searchResults);
  const searchUsers = useChatStore((state) => state.searchUsers);
  const clearSearchResults = useChatStore((state) => state.clearSearchResults);
  const createConversation = useChatStore((state) => state.createConversation);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.trim()) {
        searchUsers(query);
      } else {
        clearSearchResults();
      }
    }, 300);

    return () => {
      clearTimeout(timer);
    };
  }, [query, searchUsers, clearSearchResults]);

  const handleUserClick = async (user) => {
    await createConversation(user.id);
    setQuery("");
  };

  return (
    <div className="user-search">
      <input
        placeholder="Search for users"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
        }}
      />
      {searchResults.length > 0 && (
        <div className="user-search-results">
          {searchResults.map((user) => (
            <button key={user.id} onClick={() => handleUserClick(user)}>
              {user.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default UserSearchComp;
