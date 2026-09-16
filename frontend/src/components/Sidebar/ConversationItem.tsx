import type { Conversation } from "../../types"

interface ConversationItemProps {
    conversation: Conversation,
    onSelect: (conversation: Conversation) => void
}

export const ConversationItem: React.FC<ConversationItemProps> = ({ conversation, onSelect }) => {
    const { title, updatedAt } = conversation

    return (
        <li className="flex flex-col mt-2 hover:bg-gray-100 cursor-pointer" onClick={() => onSelect(conversation)}>
            <div className="text-gray-900 text-xl">{title}</div>
            <div className="self-end text-gray-600 text-sm">Last updated: {updatedAt.toLocaleDateString()}</div>
        </li>
    )
}
