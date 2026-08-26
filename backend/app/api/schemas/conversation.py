from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ConversationCreateDTO(BaseModel):
    title: str
    created_at: datetime = datetime.now()


class ConversationUpdate(BaseModel):
    title: str | None = None
    updated_at: datetime | None = None


class ConversatioDTO(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
