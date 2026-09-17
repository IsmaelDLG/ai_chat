import MessageInput from "./MessageInput"
import MessagesList from "./MessagesList"

function Chat() {
    return (
      <main className="bg-green-400 flex-3 relative p-4">
        <MessagesList />
        <MessageInput />
      </main>
    )
}
export default Chat