import { X } from "lucide-react";
import type { Conversation } from "../../types";

interface HeaderProps {
  conversation: Conversation | null;
  onClose: () => void;
}

const ChatHeader: React.FC<HeaderProps> = ({ conversation, onClose }) => {
  return (
    <header className="flex w-full">
      <div className="w-9/10 mx-auto pt-5 pb-2 px-5 bg-white flex flex-row justify-between">
        {conversation?.id && (
          <>
            <h2 className="text-xl font-bold text-gray-900">
              {conversation?.title}
            </h2>
            <button className="text-xl" onClick={onClose}>
              <X className="w-6 h-6" />
            </button>
          </>
        )}
      </div>
      <div className="py-5 bg-linear-to-t from-transparent to-white"></div>
    </header>
  );
};
export default ChatHeader;
