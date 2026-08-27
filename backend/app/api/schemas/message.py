from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageCreateDTO(BaseModel):
    conversation_id: int
    role: Role
    content: str
    created_at: datetime = datetime.now()


class MessageDTO(BaseModel):
    id: int
    conversation_id: int
    role: Role
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
