import type { Conversation } from "../../types";

interface HeaderProps {
  conversation: Conversation | null;
  onClose: () => void;
}

const ChatHeader: React.FC<HeaderProps> = ({ conversation, onClose }) => {
  return (
    <header className="absolute top-0 left-0 left-0 z-10 w-full ">
      <div className="w-9/10 mx-auto pt-5 pb-2 bg-white flex flex-row justify-between">
        {conversation?.id && (
          <>
            <h2 className="text-xl font-bold text-gray">
              {conversation?.title}
            </h2>
            <button className="text-xl" onClick={onClose}>
              Close
            </button>
          </>
        )}
      </div>
      <div className="py-5 bg-linear-to-t from-transparent to-white"></div>
    </header>
  );
};
export default ChatHeader;
