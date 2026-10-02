import type { Message, MessageResponse } from "../types";
import { api } from "./client";

const messageAdapter = (data: MessageResponse): Message => {
  const result: Message = {
    id: data.id,
    conversationId: data.conversationId,
    role: data.role,
    content: data.content,
    createdAt: new Date(data.createdAt),
  }
  return result
}

const streamMessage = async (conversationId: number, dto: Message) => {
  
  const response = await fetch(`http://localhost:8000/api/conversations/${conversationId}/messages/sse`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dto),
  });

  if (!response.ok) {
    throw new Error(`Error en el stream: ${response.statusText}`);
  }

  // Leer el ReadableStream...
};

export const getMessages = async (conversationId: number): Promise<Message[] | void> => {
    try {
        const { data } = await api.get<MessageResponse[]>(`/conversations/${conversationId}/messages`)
        return data.map(d => messageAdapter(d))
    } catch (error) {
      console.log('Error al cargar historial:', error);
    }
}