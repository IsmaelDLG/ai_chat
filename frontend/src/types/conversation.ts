
export interface ConversationResponse {
    id: number
    title: string
    created_at: string
    updated_at: string
}
export interface Conversation {
    id: number
    title: string
    createdAt: Date
    updatedAt: Date
}


export interface ConversationCreate {
    title: string
}