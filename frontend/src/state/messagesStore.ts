import { create } from "zustand";
import type { Message } from "../types";
import {
  getMessages,
  saveMessage,
  streamMessageResponse,
} from "../api/messages";

interface MessageStore {
  loading: boolean;
  messages: Message[];
  clear: () => void;
  send: (conversationId: number, content: string) => Promise<void>;
  getByConversationId: (conversationId: number) => Promise<void>;
}

const useStore = create<MessageStore>((set) => ({
  loading: false,
  messages: [],
  clear: () => {
    set(() => ({ messages: [] }));
  },
  send: async (conversationId: number, content: string) => {
    set(() => ({ loading: true }));
    let newMessage: Message;
    try {
      newMessage = await saveMessage(conversationId, content);
    } catch (error) {
      console.error("Error al guardar el mensaje:", error);
      return;
    }

    set((state) => ({
      messages: [...state.messages, newMessage],
    }));

    if (newMessage.id === null) {
      console.error("The saved message response did not include a message ID.");
      return;
    }

    try {
      await streamMessageResponse(newMessage.id, (chunk) =>
        set((state) => {
          const newMessages = state.messages.filter(msg => !!msg.id);
          return {
            messages: [...newMessages, chunk],
          };
        }),
      );
    } catch (error) {
      console.error("Error al generar la respuesta:", error);
    }
    set(() => ({ loading: false }));
  },
  getByConversationId: async (conversationId: number) => {
    const messages = await getMessages(conversationId);
    if (messages)
      set(() => ({
        messages,
      }));
  },
}));

export default useStore;
