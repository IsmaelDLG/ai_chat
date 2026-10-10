import type {
  Conversation,
  ConversationCreate,
  ConversationResponse,
} from "../types";
import { api } from "./client";

const conversationAdapter = (response: ConversationResponse): Conversation => {
  const result: Conversation = {
    id: response.id,
    title: response.title,
    createdAt: new Date(response.created_at),
    updatedAt: new Date(response.updated_at),
  };
  return result;
};

export const fetchConversations = async (): Promise<Conversation[] | void> => {
  try {
    const { data } = await api.get<ConversationResponse[]>("/conversations");
    return data.map((d) => conversationAdapter(d));
  } catch (error) {
    console.error("Error al cargar historial:", error);
  }
};

export const createConversation = async (
  dto: ConversationCreate,
): Promise<Conversation | void> => {
  try {
    const { data } = await api.post<ConversationResponse>(
      "/conversations",
      dto,
    );
    return conversationAdapter(data);
  } catch (error) {
    console.error("Error al crear conversación:", error);
  }
};

export const generateTitle = async (conversationId: number): Promise<Conversation | void> => {
  try {
    const { data } = await api.put<ConversationResponse>(`/conversations/${conversationId}/title/generate`, {})
    return conversationAdapter(data);
  } catch (error) {
    console.error("Error al generar título:", error);
  }
};

