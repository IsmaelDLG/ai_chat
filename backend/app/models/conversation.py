from pydantic import BaseModel, ConfigDict, Field, PlainSerializer
from datetime import datetime, timezone as tz
from typing import Annotated


class ConversationCreateDTO(BaseModel):
    title: str
    created_at: Annotated[
        datetime, PlainSerializer(lambda x: x.isoformat(timespec="milliseconds"))
    ] = Field(default_factory=lambda: datetime.now(tz.utc))


class ConversationDTO(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
