import { create } from "zustand";
import type { Conversation, ConversationCreate } from "../types";
import { fetchConversations, createConversation } from "../api/conversations";

interface ConversationStore {
  current: Conversation | null;
  conversations: Conversation[];
  getAll: () => Promise<void>;
  add: (title: string) => Promise<void>;
  set: (conversationId: number | void) => void;
}


const useStore = create<ConversationStore>((set) => ({
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
      title
    }
    const conversation = await createConversation(conversationDTO);
    if (conversation)
      set((state) => ({
        conversations: [...state.conversations, conversation],
      }));
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
}));

export default useStore;
