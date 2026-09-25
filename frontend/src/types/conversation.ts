export interface Conversation {
    id: number
    title: string
    createdAt: Date
    updatedAt: Date
}

export interface ConversationCreate {
    title: string
}