import type { Message } from "../../types";

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
    const { content, role, createdAt } = message
    
    
    const isUser = role === 'user'

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
        <div
            className={`max-w-[80%] p-3 rounded-lg ${
            isUser ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-100'
            }`}
        >
            <p className="text-sm whitespace-pre-wrap">{content}</p>
            <span className="text-[10px] opacity-70 block text-right mt-1">
            {createdAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
        </div>
        </div>
    );
};

export default MessageItem;
