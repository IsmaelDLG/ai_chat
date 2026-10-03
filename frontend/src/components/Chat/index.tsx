import MessageInput from "./MessageInput";
import MessagesList from "./MessagesList";

import useConversationStore from "../../state/conversationsStore";
import useMessageStore from "../../state/messagesStore";
import { useEffect } from "react";
import ChatHeader from "./Header";
import StartConversation from "./StartConversation";


function Chat() {

  const conversation = useConversationStore((state) => state.current);
  const clearConversation = useConversationStore((state) => state.set);
  const createConversation = useConversationStore((state) => state.add);

  const clearMessages = useMessageStore((state) => state.clear);
  const sendMessage = useMessageStore((state) => state.send);
  const getMessages = useMessageStore((state) => state.getByConversationId);
  const isLoading = useMessageStore((state) => state.loading);

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
    clearConversation();
  };

  const handleCreateConversation = () => {
    createConversation(`New conversation ${new Date().getTime()}`);
  }


  return (
    <main className="flex flex-col min-w-0 w-full ">
      {conversation?.id && <>
      <ChatHeader
        conversation={conversation}
        onClose={handleCloseConversation}
      />
      <MessagesList conversationId={conversation?.id} messages={messages} />
      <MessageInput handleSend={handleSendMessage} isLoading={isLoading} />
      </>}
      {!conversation?.id && 
        <StartConversation onSubmit={handleCreateConversation} />
      }
    </main>
  );
};
export default Chat;
