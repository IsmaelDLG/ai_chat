import { useState } from "react";

interface MessageInputProps { 
    handleSend: (message: string) => void;
    isLoading: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ handleSend, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = () => {
        const trimmed = input.trim()
        if (!trimmed) return;

        handleSend(trimmed)

        setInput('');
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        console.log(event)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    };
      return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t border-gray-700 ">
      <textarea
        rows={1}
        value={input}
        onChange={event => setInput(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Escribe tu mensaje..."
        disabled={isLoading}
        className="flex-1 p-2 border border-gray-700 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="px-4 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-500 disabled:opacity-50 transition-colors"
      >
        {isLoading ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  );
}
export default MessageInput