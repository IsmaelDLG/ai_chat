from openai import AsyncOpenAI
import asyncio

from app.core.config import get_settings
from app.core.exceptions import (
    ConversationNotFoundError,
    MessageSaveError,
    LLMNotAvailableError,
)

from app.api.schemas.message import MessageCreateFullDTO, MessageDTO, Role
from app.dataaccess.repositories.conversation import ConversationRepository
from app.dataaccess.repositories.message import MessageRepository
from app.api.schemas.conversation import ConversationDTO

settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)


class MessageService:
    def __init__(self, msg_repo: MessageRepository, conv_repo: ConversationRepository):
        self.repository = msg_repo
        self.conv_repository = conv_repo

    async def get_messages(self, conversation_id: int) -> list[MessageDTO]:
        conversation: ConversationDTO = await self.conv_repository.get_by_id(
            conversation_id
        )
        if not conversation:
            raise ConversationNotFoundError(conversation_id)

        return await self.repository.get_by_conversation_id(conversation_id)

    async def send_message(self, message: MessageCreateFullDTO) -> MessageDTO:
        conversation_id = message.conversation_id
        conversation: ConversationDTO = await self.conv_repository.get_by_id(
            conversation_id
        )
        if not conversation:
            raise ConversationNotFoundError(conversation_id)

        llm_task = asyncio.create_task(
            client.responses.create(
                model=settings.llm_model,
                input=message.content,
            )
        )

        try:
            await self.repository.save(message)
        except Exception:
            if not llm_task.done():
                llm_task.cancel()
            raise MessageSaveError(message.content)

        try:
            response = await llm_task
        except Exception:
            raise LLMNotAvailableError()

        assistant_message = MessageCreateFullDTO(
            conversation_id=message.conversation_id,
            role=Role.ASSISTANT,
            content=response.output_text,
        )
        result: MessageDTO = await self.repository.save(assistant_message)
        await self.conv_repository.update_updated_at(conversation_id)

        return result
