import { useEffect } from 'react'
import useConversationsStore from "../../state/conversationsStore"
import { ConversationItem } from './ConversationItem'

interface ConversationListProps {

}

const ConversationList: React.FC<ConversationListProps> = () => {
    const getAllConversations = useConversationsStore((state) => state.getAll)
    const setCurrentConversation = useConversationsStore((state) => state.set)
    const conversations = useConversationsStore((state) => state.conversations)

    useEffect(() => {
        getAllConversations()
    }, [getAllConversations])

    const handleOnSelectConversation = (id: number) => {
        setCurrentConversation(id)
    }

    return (
        <div id="history" className="mx-4 mt-4">
            {
                conversations.map((conversation) => (
                    <ConversationItem key={conversation?.id} conversation={conversation} onSelect={handleOnSelectConversation} />
                ))
            }
        </div>
    )
}

export default ConversationList