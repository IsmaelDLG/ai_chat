import type { Conversation } from "../../types"

interface ConversationItemProps {
    conversation: Conversation,
    onSelect: (id: number) => void
}

export const ConversationItem: React.FC<ConversationItemProps> = ({ conversation, onSelect }) => {
    const { id, title } = conversation

    return (
        <li className="flex flex-col px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-300" onClick={() => onSelect(id)}>
            <div className="text-gray-900 text-normal">{title}</div>
        </li>
    )
}
