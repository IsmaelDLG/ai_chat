from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dataaccess.db import get_db

from app.dataaccess.repositories.conversation import ConversationRepository
from app.services.conversation import ConversationService

from app.dataaccess.repositories.message import MessageRepository
from app.services.message import MessageService


def get_conversation_repository(
    db: AsyncSession = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)

def get_message_repository(
    db: AsyncSession = Depends(get_db),
) -> MessageRepository:
    return MessageRepository(db)

def get_conversation_service(
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
    msg_repo: MessageRepository = Depends(get_message_repository),
) -> ConversationService:
    return ConversationService(conv_repo, msg_repo)

def get_message_service(
    msg_repo: MessageRepository = Depends(get_message_repository),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> MessageService:
    return MessageService(msg_repo, conv_repo)
