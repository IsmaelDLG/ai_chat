
export interface ConversationResponse {
    id: number
    title: string
    createdAt: string
    updatedAt: string
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