import { useEffect, useRef } from "react";
import type { Message } from "../../types";
import MessageItem from "./MessageItem";

interface MessagesListProps {
  messages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLLIElement>(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);
  return (
    <div id="messagesList" className="flex flex-grow w-full overflow-y-auto scrollbar-none w-9/10 mx-auto py-20">
      <ul className="flex-col">
        {messages.map((message) => (
          <MessageItem
            key={
              message.id ??
              `${message.conversationId}-${message.createdAt.getTime()}`
            }
            message={message}
          />
        ))}
        <li ref={messagesEndRef}></li>
      </ul>
    </div>
  );
};

export default MessagesList;
