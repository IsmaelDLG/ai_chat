import { useEffect } from 'react'
import useConversationsStore from "../state/conversationsStore"

function Sidebar() {
    const getAllConversations = useConversationsStore((state) => state.getAll)
    const createConversation = useConversationsStore((state) => state.add)
    const conversations = useConversationsStore((state) => state.conversations)

    useEffect(() => {
        getAllConversations()
    }, [])

    return (
        <aside className="bg-red-400 flex-1">
            {
                conversations.map((conversation, index) => (
                    <div key={index}>{conversation.title}</div>
                ))
            }
        </aside>
    )
}

export default Sidebar