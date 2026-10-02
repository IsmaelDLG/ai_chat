export type Role = 'user' | 'assistant' | 'system'

export interface MessageResponse {
    id: number;
    conversationId: number;
    role: Role;
    content: string;
    createdAt: string;
}
export interface Message {
    id: number | null;
    conversationId: number;
    role: Role;
    content: string;
    createdAt: Date;
}