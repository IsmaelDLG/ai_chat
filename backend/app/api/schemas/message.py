from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone as tz
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageCreateDTO(BaseModel):
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))


class MessageCreateFullDTO(MessageCreateDTO):
    conversation_id: int
    role: Role


class MessageDTO(BaseModel):
    id: int
    conversation_id: int
    role: Role
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
