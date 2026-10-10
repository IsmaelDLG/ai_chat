import { Clock, RotateCcw } from "lucide-react"
import ConversationList from "./ConversationList"
import useConversationStore from "../../state/conversationsStore";


function Sidebar() {
    const onReload = useConversationStore((state) => state.getAll);

    return (
        <aside className="w-100 overflow-y-auto border-r border-gray-300">
            <header className="flex items-center justify-between mx-4  border-b border-gray-300">
                <div className="flex items-center gap-2 px-4 py-4">
                    <Clock />
                    <h2 className="text-gray-900 font-bold text-3xl">Recent</h2>
                </div>
                <button onClick={onReload}>
                    <RotateCcw />
                </button>
            </header>
            <ConversationList />
        </aside>
    )
}

export default Sidebar