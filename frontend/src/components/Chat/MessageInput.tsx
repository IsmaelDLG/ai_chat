import { useState } from "react";

interface MessageInputProps { 
    handleSend: (message: string) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ handleSend }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = () => {
        const trimmed = message.trim()
        if (!trimmed) return;

        // enviar mensaje
        handleSend(trimmed)

        setMessage('');
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        console.log(event)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    };
    return (
        <div className="pointer-events-none absolute bottom-5 left-0 flex w-full justify-center">
            <div
                className="
                    pointer-events-auto
                    flex w-[min(768px,calc(100%-32px))]
                    items-end gap-2
                    rounded-3xl
                    border border-gray-300
                    bg-white
                    p-2
                    shadow-sm
                "
            >
                <button
                    type="button"
                    className="
                        flex h-10 w-10 shrink-0
                        items-center justify-center
                        rounded-full
                        hover:bg-gray-100
                    "
                >
                    +
                </button>

                <textarea
                    placeholder="Pregunta lo que quieras"
                    rows={1}
                    className="
                        max-h-32
                        min-h-10
                        flex-1
                        resize-none
                        bg-transparent
                        px-2 py-2
                        outline-none
                    "
                    onChange={event => setMessage(event.target.value)}
                    onKeyDown={handleKeyDown}
                    value={message}
                />

                <button
                    type="button"
                    className="
                        flex h-10 w-10 shrink-0
                        items-center justify-center
                        rounded-full
                        bg-black text-white
                        hover:bg-gray-800
                    "
                    onClick={handleSubmit}
                >
                    ↑
                </button>
            </div>
        </div>
    );
}
export default MessageInput

function handleSend(trimmed: string) {
    throw new Error("Function not implemented.");
}
