import MessageInput from "./MessageInput"
import MessagesList from "./MessagesList"

import useConversationStore from "../../state/conversationsStore"
import useMessageStore from "../../state/messagesStore"
import { useEffect } from "react"
import ChatHeader from "./Header"

interface ChatProps {
}

const Chat: React.FC<ChatProps> = ({}) => {
  const conversation = useConversationStore((state) => state.current)
  const sendMessage = useMessageStore((state) =>  state.send)
  const getMessages = useMessageStore((state) => state.getByConversationId)

  const messages = useMessageStore((state) => state.messages)

  useEffect(() => {
    if (!!conversation?.id) {
      getMessages(conversation?.id)
    }
  }, [conversation, getMessages])

  const handleSendMessage = (message: string) => {
    if (!conversation?.id) {
      console.log("Conversation ID is not defined")
    } else {
      sendMessage(conversation?.id, message)
    }
  }

  return (
    <main className="flex-3 relative">
      <ChatHeader conversation={conversation} />
      <MessagesList messages={messages} />
      <MessageInput handleSend={handleSendMessage} isLoading={false} />
    </main>
  )
}
export default Chat