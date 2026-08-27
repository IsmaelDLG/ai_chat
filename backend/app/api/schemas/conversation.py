from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone as tz


class ConversationCreateDTO(BaseModel):
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))


class ConversationDTO(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
