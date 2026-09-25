import type { Conversation, ConversationCreate } from '../types';
import {api} from './client'; 

export const fetchConversations = async (): Promise<Conversation[] | void> => {
  try {
    const { data } = await api.get<Conversation[]>('/conversations');
    return data;
  } catch (error) {
    console.error('Error al cargar historial:', error);
  }
};

export const createConversation = async (dto: ConversationCreate): Promise<Conversation | void > => {
  try {
    const response = await api.post('/conversations', dto)
    // TODO: createdDate is a string. Must be converted to a Date
    return response.data;
  } catch (error) {
    console.error('Error al crear conversación:', error);
  }
}