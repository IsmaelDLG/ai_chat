import { useEffect, useRef } from "react";
import type { Message } from "../../types";
import MessageBox from "./MessageBox";

interface MessagesListProps {
  messages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({ messages }) => {
const messagesEndRef = useRef<HTMLLIElement>(null)
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);
  return (
    <div className="size-full overflow-y-auto scrollbar-none w-8/10 mx-auto" >
        <ul className="flex-col">
        {messages.map((message, index) => (
            <MessageBox key={index} message={message} />
        ))}
        <li ref={messagesEndRef}></li>
        </ul>
    </div>
  );
};

export default MessagesList;
