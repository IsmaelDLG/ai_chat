import type { Message } from "../../types";

interface MessageBoxProps {
  message: Message;
}

const MessageBox: React.FC<MessageBoxProps> = ({ message }) => {
    const { content, role, createdAt } = message
    const messageTime = createdAt.getDay() !== new Date().getDay() ? `${createdAt.toLocaleDateString()} ${createdAt.toLocaleTimeString()}` : `${createdAt.toLocaleTimeString()}`
    
    const isRight = role === 'user'

    return (
        <li className={`flex flex-col w-fit ${isRight ? 'ml-auto' : 'mr-auto'}`}>
            <div className={`text-gray-900 text-base ${isRight ? 'text-right' : 'text-left'}`}>{content}</div>
            <div className="self-end text-gray-600 text-sm">
                {messageTime}
            </div>
        </li>
    );
};

export default MessageBox;
