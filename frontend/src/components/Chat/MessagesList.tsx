import type { Message } from "../../types"

interface MessagesListProps {
    messages: Message[]
}

const MessagesList: React.FC<MessagesListProps> = ({messages}) => {
    return (
        <ul className="size-full">
            {messages.map((message, index) => (
                <li key={index} >
                    {message.content}
                </li>
            ))}
        </ul>
    )
}

export default MessagesList