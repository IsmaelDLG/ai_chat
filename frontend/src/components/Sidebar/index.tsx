import ConversationList from "./ConversationList"

function Sidebar() {
    return (
        <aside className="bg-red-400 flex-1 overflow-scroll">
            <header >
                <h2 className="mx-4 mt-4 text-gray-900 font-bold text-3xl">Recent</h2>
            </header>
            <ConversationList />
        </aside>
    )
}

export default Sidebar