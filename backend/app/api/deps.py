from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dataaccess.db import get_db
from app.dataaccess.repositories.conversation import ConversationRepository
from app.services.conversation import ConversationService


def get_conversation_repository(
    db: AsyncSession = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_conversation_service(
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationService:
    return ConversationService(repo)
