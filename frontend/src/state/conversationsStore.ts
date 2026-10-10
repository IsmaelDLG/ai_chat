import { create } from "zustand";
import type { Conversation, ConversationCreate } from "../types";
import {
  fetchConversations,
  createConversation,
  generateTitle,
} from "../api/conversations";

interface ConversationStore {
  current: Conversation | null;
  conversations: Conversation[];
  getAll: () => Promise<void>;
  add: (title: string) => Promise<void>;
  set: (conversationId: number | void) => void;
  generateTitle: () => void;
}

const useStore = create<ConversationStore>((set, get) => ({
  current: null,
  conversations: [],
  getAll: async () => {
    const conversations = await fetchConversations();
    if (conversations)
      set({
        conversations,
      });
  },
  add: async (title: string) => {
    const conversationDTO: ConversationCreate = {
      title,
    };
    const conversation = await createConversation(conversationDTO);
    if (conversation) {
      set((state) => ({
        conversations: [conversation, ...state.conversations],
        current: conversation
      }))
    }
  },
  set: (conversationId: number | void) => {
    if (conversationId === null) {
      set({ current: null });
      return;
    }

    set((state) => ({
      current:
        state.conversations.find(({ id }) => id === conversationId) ?? null,
    }));
  },
  generateTitle: async () => {
    const currentConv = get().current;
    if (!currentConv?.id) return;

    const newConversation = (await generateTitle(currentConv.id)) ?? null;
    if (newConversation?.id)
      set((state) => ({
        current: newConversation,
        conversations: [
          newConversation,
          ...state.conversations.filter((c) => c.id !== newConversation.id),
        ],
      }));
  },
}));

export default useStore;
