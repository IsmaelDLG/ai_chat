import MessageInput from "./MessageInput"
import MessagesList from "./MessagesList"

import useConversationStore from "../../state/conversationsStore"
import useMessageStore from "../../state/messagesStore"
import { useEffect } from "react"

interface ChatProps {
}

const Chat: React.FC<ChatProps> = ({}) => {
  const conversationId = useConversationStore((state) => state.current)
  const sendMessage = useMessageStore((state) =>  state.send)
  const getMessages = useMessageStore((state) => state.getByConversationId)

  const messages = useMessageStore((state) => state.messages)

  useEffect(() => {
    if (!!conversationId) {
      getMessages(conversationId)
    }
  }, [conversationId, getMessages])

  const handleSendMessage = (message: string) => {
    if (!conversationId) {
      console.log("Conversation ID is not defined")
    } else {
      sendMessage(conversationId, message)
    }
  }

  return (
    <main className="bg-green-400 flex-3 relative p-4">
      <MessagesList messages={messages} />
      <MessageInput handleSend={handleSendMessage} />
    </main>
  )
}
export default Chat