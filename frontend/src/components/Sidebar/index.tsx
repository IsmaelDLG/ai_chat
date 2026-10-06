import { Clock } from "lucide-react"
import ConversationList from "./ConversationList"

function Sidebar() {
    return (
        <aside className="w-80 overflow-y-auto">
            <header className="flex items-center  gap-2 px-4 py-4">
                <Clock />
                <h2 className="text-gray-900 font-bold text-3xl">Recent</h2>
            </header>
            <ConversationList />
        </aside>
    )
}

export default Sidebar