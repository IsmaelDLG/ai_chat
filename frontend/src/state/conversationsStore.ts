import { create } from 'zustand';
import type { Conversation } from '../types';

interface ConversationStore {
    current: number | null;
    conversations: Conversation[];
    getAll: () => Promise<void>;
    add: (title: string) => Promise<void>;
    set: (conversationId: number | null) => void;
}

function delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function createConversation(title: string): Promise<Conversation> {
    // TODO: Call POST /conversations
    await delay(500);

    return {
        id: 3,
        title,
        createdAt: new Date(),
        updatedAt: new Date(),
    };
}

async function getConversations(): Promise<Conversation[]> {
    // TODO: Call GET /conversations
    await delay(500);

    const result = []
    for(let i = 0; i<100; i++) {
        result.push({
            id: i,
            title: `Conversation title ${i}`,
            createdAt: new Date(),
            updatedAt: new Date()
        })
    }
    
    return result
}

const useStore = create<ConversationStore>((set) => ({
    current: null,
    conversations: [],
    getAll: async () => {
        const conversations = await getConversations();

        set({
            conversations,
        });
    },
    add: async (title: string) => {
        const conversation = await createConversation(title);

        set((state) => ({
            conversations: [
                ...state.conversations,
                conversation,
            ],
        }));
    },
    set: (conversationId: number | null) => {
        set(() => ({ current: conversationId }));
    }
}));

export default useStore;