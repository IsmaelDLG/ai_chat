from pydantic import BaseModel, ConfigDict, Field, PlainSerializer
from datetime import datetime, timezone as tz
from enum import Enum
from typing import Annotated


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageCreateDTO(BaseModel):
    content: str
    created_at: Annotated[
        datetime, PlainSerializer(lambda x: x.isoformat(timespec="milliseconds"))
    ] = Field(default_factory=lambda: datetime.now(tz.utc))


class MessageCreateFullDTO(MessageCreateDTO):
    conversation_id: int
    role: Role


class MessageDTO(BaseModel):
    id: int | None = None
    conversation_id: int
    role: Role
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatCompletionMessage(BaseModel):
    role: Role
    content: str