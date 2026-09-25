import type { Message } from "../types";
import { api } from "./client";

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
        const { data } = await api.get<Message[]>(`/conversations/${conversationId}/messages`)
        return data
    } catch (error) {
      console.log('Error al cargar historial:', error);
    }
}