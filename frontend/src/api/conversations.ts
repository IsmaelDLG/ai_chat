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
    createdAt: new Date(response.createdAt),
    updatedAt: new Date(response.updatedAt),
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
