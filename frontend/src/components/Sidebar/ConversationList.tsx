import { useEffect } from 'react'
import useConversationsStore from "../../state/conversationsStore"
import { ConversationItem } from './ConversationItem'
import type { Conversation } from '../../types'

interface ConversationListProps {

}

const ConversationList: React.FC<ConversationListProps> = () => {
    const getAllConversations = useConversationsStore((state) => state.getAll)
    const conversations = useConversationsStore((state) => state.conversations)

    useEffect(() => {
        getAllConversations()
    }, [])

    const handleOnSelectConversation = (conversation: Conversation) => {
        console.log(`Handle on click conversation id: ${conversation.id}`)
    }

    return (
        <div id="history" className="mx-4 mt-4">
            {
                conversations.map((conversation, index) => (
                    <ConversationItem key={index} conversation={conversation} onSelect={handleOnSelectConversation} />
                ))
            }
        </div>
    )
}

export default ConversationList