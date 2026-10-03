import type { Message, MessageResponse } from "../types";
import { api } from "./client";

type StreamMessageResponse = Omit<MessageResponse, "id"> & { id: number | null };

const messageAdapter = (data: StreamMessageResponse): Message => {
  const result: Message = {
    id: data.id,
    conversationId: data.conversation_id,
    role: data.role,
    content: data.content,
    createdAt: new Date(data.created_at),
  };
  return result;
};

export const saveMessage = async (
  conversationId: number,
  content: string,
): Promise<Message> => {
  const { data } = await api.post<MessageResponse>(
    `/conversations/${conversationId}/messages`,
    { content },
  );
  return messageAdapter(data);
};

export const generateMessageResponse = async (
  messageId: number,
): Promise<Message> => {
  const { data } = await api.post<MessageResponse>(
    `/messages/${messageId}/response`,
  );
  return messageAdapter(data);
};

export const streamMessageResponse = async (
  messageId: number,
  onChunk: (message: Message) => void,
): Promise<Message> => {
  const response = await fetch(
    `http://localhost:8000/api/messages/${messageId}/response/sse`,
    { method: "POST" },
  );
  if (!response.ok) {
    throw new Error(`Error en el stream: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("El servidor no devolvió un stream de mensajes.");
  }

  const decoder = new TextDecoder();
  let buffer = "";
  let savedResponse: Message | undefined;

  let previousChunk: Message | null = null;
  const processLine = (line: string) => {
    if (!line.trim()) return;
    const message = messageAdapter(
      JSON.parse(line) as StreamMessageResponse,
    );
    if (previousChunk && message.id === null) {
      message.content = previousChunk.content + message.content;
    }
    onChunk(message);
    if (message.id !== null) savedResponse = message;
    previousChunk = message;
  };

  while (true) {
    const { done, value } = await reader.read();
    buffer += decoder.decode(value, { stream: !done });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    lines.forEach(processLine);
    if (done) break;
  }
  processLine(buffer);

  if (!savedResponse) {
    throw new Error("El stream terminó sin un mensaje de respuesta guardado.");
  }
  return savedResponse;
};

export const getMessages = async (conversationId: number): Promise<Message[] | void> => {
    try {
        const { data } = await api.get<MessageResponse[]>(`/conversations/${conversationId}/messages`)
        return data.map(d => messageAdapter(d))
    } catch (error) {
      console.log('Error al cargar historial:', error);
    }
}