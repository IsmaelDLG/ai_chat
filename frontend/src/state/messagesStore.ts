import { create } from "zustand";
import type { Message } from "../types";
import { getMessages } from "../api/messages";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sendMessage(message: Message): Promise<Message> {
  // TODO: Call send message to the database
  await delay(500);
  const response: Message = {
    id: new Date().getTime(),
    conversationId: message.conversationId,
    role: "assistant",
    content: `"${message.content}" responsed by AI."`,
    createdAt: new Date(),
  };

  return response;
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
    set(() => ({ messages: [] }));
  },
  send: async (conversationId: number, content: string) => {
    const id = new Date().getTime();
    const newMessage: Message = {
      id,
      conversationId,
      role: "user",
      content,
      createdAt: new Date(),
    };
    const response = await sendMessage(newMessage);
    set((state) => ({
      messages: [...state.messages, newMessage, response],
    }));
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
