from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone as tz

from app.dataaccess.db import Base


class Conversations(Base):
    __tablename__ = "Conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
