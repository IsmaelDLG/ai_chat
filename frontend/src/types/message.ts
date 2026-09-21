export type Role = 'user' | 'assistant' | 'system'

export interface Message {
    id: number | null;
    conversationId: number;
    role: Role;
    content: string;
    createdAt: Date;
}