import { Clock, RotateCcw } from "lucide-react"
import ConversationList from "./ConversationList"
import useConversationStore from "../../state/conversationsStore";


function Sidebar() {
    const onReload = useConversationStore((state) => state.getAll);

    return (
        <aside className="w-80 overflow-y-auto">
            <header className="flex items-center justify-between">
                <div className="flex items-center  gap-2 px-4 py-4">
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