from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    conversation_id: int
    role_id: int
    content: str
    created_at: datetime = datetime.now()


class ChatResponse(BaseModel):
    response: str
