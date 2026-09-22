import { create } from 'zustand';
import type { Message, Role } from '../types';


function delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sendMessage(message: Message): Promise<Message> {
    // TODO: Call send message to the database
    await delay(500)
    const response: Message = {
        id: new Date().getTime(),
        conversationId: message.conversationId,
        role: 'assistant',
        content: `"${message.content}" responsed by AI."`,
        createdAt: new Date()
    };

    return response
}

async function getMessagesByConversationId(conversationId: number): Promise<Message[]>  {
    // TODO: Call get messages from the database
    await delay(500)
    const result = []
    
    for (let i = 0; i<100; i++) {
        let isUser = i % 2 === 0
        let role: Role, content
        if (isUser) {
            role = 'user'
            content = `User message ${i}`
        } else {
            role = 'assistant'
            content = `Assistant response ${i}`
        }

        let createdAt = new Date()
        createdAt.setHours(new Date().getHours() - (100-i))

        let message: Message = {
            id: i,
            conversationId,
            role,
            content,
            createdAt
        }
        result.push(message);
    }
    return result
}

interface MessageStore {
    messages: Message[];
    clear: () => void;
    send: (conversationId: number, content: string) => Promise<void>;
    getByConversationId: (conversationId: number) => Promise<void>;
}

const useStore = create<MessageStore>((set) => ({
    messages: [],
    clear: () => {
        set(() => ({messages: []}))
    },
    send: async (conversationId: number, content: string) => {
        const id = new Date().getTime()
        const newMessage: Message = {
            id,
            conversationId,
            role: 'user',
            content,
            createdAt: new Date()
        };
        const response = await sendMessage(newMessage);
        set((state) => ({
            messages: [
                ...state.messages,
                newMessage,
                response
            ]
        }))
    },
    getByConversationId: async (conversationId: number) => {
        const response = await getMessagesByConversationId(conversationId);
        set(() => ({
            messages: [...response]
        }))
    }
}))

export default useStore