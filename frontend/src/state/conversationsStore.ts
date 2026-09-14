import { create } from 'zustand';
import type { Conversation } from '../types';

interface ConversationStore {
    current: number | null;
    conversations: Conversation[];
    add: (title: string) => Promise<void>;
    getAll: () => Promise<void>;
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
        created_at: new Date(),
        updated_at: new Date(),
    };
}

async function getConversations(): Promise<Conversation[]> {
    // TODO: Call GET /conversations
    await delay(500);

    return [
        {
            id: 1,
            title: 'Primera conversación',
            created_at: new Date(),
            updated_at: new Date(),
        },
        {
            id: 2,
            title: 'Segunda conversación',
            created_at: new Date(),
            updated_at: new Date(),
        },
    ];
}

const useStore = create<ConversationStore>((set) => ({
    current: null,
    conversations: [],

    add: async (title: string) => {
        const conversation = await createConversation(title);

        set((state) => ({
            conversations: [
                ...state.conversations,
                conversation,
            ],
        }));
    },

    getAll: async () => {
        const conversations = await getConversations();

        set({
            conversations,
        });
    },
}));

export default useStore;