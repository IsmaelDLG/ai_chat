import type { Conversation } from "../../types";

interface HeaderProps {
    conversation: Conversation | null;
}

const ChatHeader: React.FC<HeaderProps> = ({ conversation }) => {
    return (
        <header className="absolute top-0 left-0 left-0 z-10 w-full ">
            <div className="w-9/10 mx-auto pt-5 pb-2 bg-white">
                <h2 className="text-xl font-bold text-gray">{conversation?.title}</h2>
            </div>
            <div className="py-5 bg-linear-to-t from-transparent to-white">

            </div>
        </header>
        
    )
};
export default ChatHeader