export type Role = 'user' | 'assistant' | 'system'

export interface MessageResponse {
    id: number;
    conversation_id: number;
    role: Role;
    content: string;
    created_at: string;
}
export interface Message {
    id: number | null;
    conversationId: number;
    role: Role;
    content: string;
    createdAt: Date;
}