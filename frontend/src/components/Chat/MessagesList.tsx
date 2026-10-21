import { useEffect, useRef, useState } from "react";
import type { Message } from "../../types";
import MessageItem from "./MessageItem";

interface MessagesListProps {
  conversationId: number;
  messages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({
  conversationId,
  messages,
}) => {
  const messagesListRef = useRef<HTMLDivElement>(null);
  const previousConversationId = useRef<number | null>(null);

  useEffect(() => {
    const element = messagesListRef.current;

    if (!element) return;
    if (messages.length === 0) return;

    const conversationChanged =
      previousConversationId.current !== conversationId;
    element.scrollTo({
      top: element.scrollHeight,
      behavior: conversationChanged ? "auto" : "smooth",
    });

    previousConversationId.current = conversationId;
  }, [messages, conversationId]);

  const [showTopGradient, setShowTopGradient] = useState(false);
  const [showBottomGradient, setShowBottomGradient] = useState(false);

  const handleMessagesScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const element = e.currentTarget;

    const hasMoreAbove = element.scrollTop > 0;

    const hasMoreBelow =
      element.scrollTop + element.clientHeight < element.scrollHeight - 1;

    setShowTopGradient(hasMoreAbove);
    setShowBottomGradient(hasMoreBelow);
  };

  return (
    <div
      id="messagesListContainer"
      className="w-9/10 mx-auto flex flex-grow min-h-0"
    >
      <div
        id="messagesList"
        ref={messagesListRef}
        onScroll={handleMessagesScroll}
        className="h-full w-full overflow-y-auto px-5"
      >
        {/* Gradient superior */}
        <div className="sticky top-0 z-10 h-0 pointer-events-none">
          {showTopGradient && (
            <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-white to-transparent" />
          )}
        </div>

        <ul className="flex w-full flex-col">
          {messages.map((message) => (
            <MessageItem
              key={
                message.id ??
                `${message.conversationId}-${message.createdAt.getTime()}`
              }
              message={message}
            />
          ))}
        </ul>

        {/* Gradient inferior */}
        <div className="sticky bottom-0 z-10 h-0 pointer-events-none">
          {showBottomGradient && (
            <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-white to-transparent" />
          )}
        </div>
      </div>
    </div>
  );
};

export default MessagesList;
