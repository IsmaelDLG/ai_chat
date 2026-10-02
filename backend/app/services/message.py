import datetime
from typing import AsyncGenerator

from openai import AsyncOpenAI
import asyncio

from app.core.config import get_settings
from app.core.exceptions import (
    ConversationNotFoundError,
    InvalidMessageRoleError,
    MessageNotFoundError,
    MessageSaveError,
    LLMNotAvailableError,
)

from app.models.message import ChatCompletionMessage, MessageCreateFullDTO, MessageDTO, Role
from app.dataaccess.repositories.conversation import ConversationRepository
from app.dataaccess.repositories.message import MessageRepository
from app.models.conversation import ConversationDTO

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

    async def create_message(self, message: MessageCreateFullDTO) -> MessageDTO:
        conversation_id = message.conversation_id
        conversation: ConversationDTO = await self.conv_repository.get_by_id(
            conversation_id
        )
        if not conversation:
            raise ConversationNotFoundError(conversation_id)

        try:
            result = await self.repository.save(message)
        except Exception:
            raise MessageSaveError(message.content)

        await self.conv_repository.update_updated_at(conversation_id)
        return result

    async def _get_response_context(
        self, message_id: int
    ) -> tuple[MessageDTO, list[dict[str, str]]]:
        message = await self.repository.get_by_id(message_id)
        if message is None:
            raise MessageNotFoundError(message_id)
        if message.role != Role.USER:
            raise InvalidMessageRoleError(message_id)

        conversation_id = message.conversation_id
        conversation = await self.conv_repository.get_by_id(conversation_id)
        if not conversation:
            raise ConversationNotFoundError(conversation_id)

        conversation_messages = await self.repository.get_by_conversation_id(conversation_id)
        messages_parsed = [ChatCompletionMessage.model_validate(message.model_dump()) for message in conversation_messages]
        messages = [message.model_dump() for message in messages_parsed]
        return message, messages

    async def generate_response(self, message_id: int) -> MessageDTO:
        message, messages = await self._get_response_context(message_id)
        conversation_id = message.conversation_id
        
        try:
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
            )
        except Exception:
            raise LLMNotAvailableError()

        response_str = response.choices[0].message.content

        assistant_message = MessageCreateFullDTO(
            conversation_id=message.conversation_id,
            role=Role.ASSISTANT,
            content=response_str,
        )

        try:
            result: MessageDTO = await self.repository.save(assistant_message)
        except Exception:
            raise MessageSaveError(assistant_message.content)

        await self.conv_repository.update_updated_at(conversation_id)

        return result

    async def generate_response_stream(
        self, message_id: int
    ) -> AsyncGenerator[str, None]:
        message, messages = await self._get_response_context(message_id)
        return self._stream_response(message, messages)

    async def _stream_response(
        self, message: MessageDTO, messages: list[dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        conversation_id = message.conversation_id
        full_response = ""
        created_at = datetime.datetime.now(datetime.timezone.utc)
        try:
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                stream=True
            )
            async for chunk in response:
                delta = chunk.choices[0].delta.content
                if not delta:
                    continue
                full_response += delta
                dto = MessageDTO(
                    id=None,  # El ID de BD aún no existe mientras streameamos
                    conversation_id=conversation_id,
                    role=Role.ASSISTANT,
                    content=delta,
                    created_at=created_at
                )

                yield dto.model_dump_json() + "\n"  
        except asyncio.CancelledError:
            # Manejar la cancelación de la solicitud
            print("La solicitud fue cancelada por el cliente.")
        except Exception as e:
            print(f"Error al generar la respuesta: {e}")
            raise LLMNotAvailableError()

        if full_response:
            assistant_message = MessageCreateFullDTO(
                conversation_id=conversation_id,
                role=Role.ASSISTANT,
                content=full_response,
            )

            try:
                result: MessageDTO = await self.repository.save(assistant_message)
                await self.conv_repository.update_updated_at(conversation_id)
                yield result.model_dump_json() + "\n"
            except Exception:
                raise MessageSaveError(assistant_message.content)
        