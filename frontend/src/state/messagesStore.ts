import { create } from "zustand";
import type { Message } from "../types";
import {
  generateMessageResponse,
  getMessages,
  saveMessage,
} from "../api/messages";

interface MessageStore {
  messages: Message[];
  clear: () => void;
  send: (conversationId: number, content: string) => Promise<void>;
  getByConversationId: (conversationId: number) => Promise<void>;
}

const useStore = create<MessageStore>((set) => ({
  messages: [],
  clear: () => {
    set(() => ({ messages: [] }));
  },
  send: async (conversationId: number, content: string) => {
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
      const response = await generateMessageResponse(newMessage.id);
      set((state) => ({
        messages: [...state.messages, response],
      }));
    } catch (error) {
      console.error("Error al generar la respuesta:", error);
    }
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
