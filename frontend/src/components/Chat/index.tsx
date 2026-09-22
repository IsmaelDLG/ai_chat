import MessageInput from "./MessageInput";
import MessagesList from "./MessagesList";

import useConversationStore from "../../state/conversationsStore";
import useMessageStore from "../../state/messagesStore";
import { useEffect } from "react";
import ChatHeader from "./Header";

interface ChatProps {}

const Chat: React.FC<ChatProps> = ({}) => {
  const conversation = useConversationStore((state) => state.current);
  const setConversation = useConversationStore((state) => state.set);
  const clearMessages = useMessageStore((state) => state.clear);
  const sendMessage = useMessageStore((state) => state.send);
  const getMessages = useMessageStore((state) => state.getByConversationId);

  const messages = useMessageStore((state) => state.messages);

  useEffect(() => {
    if (conversation) {
      getMessages(conversation.id);
      return;
    }

    clearMessages();
  }, [conversation, getMessages, clearMessages]);

  const handleSendMessage = (message: string) => {
    if (!conversation?.id) {
      console.log("Conversation ID is not defined");
    } else {
      sendMessage(conversation?.id, message);
    }
  };

  const handleCloseConversation = () => {
    setConversation(null);
  };

  return (
    <main className="relative min-w-0 flex-3">
      <ChatHeader
        conversation={conversation}
        onClose={handleCloseConversation}
      />
      <MessagesList messages={messages} />
      <MessageInput handleSend={handleSendMessage} isLoading={false} />
    </main>
  );
};
export default Chat;
