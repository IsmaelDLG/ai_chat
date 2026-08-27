from openai import AsyncOpenAI
from app.core.config import get_settings

from app.api.schemas.message import MessageCreateFullDTO, MessageDTO, Role
from app.dataaccess.repositories.message import MessageRepository

settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)


class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repository = repo

    async def send_message(self, message: MessageCreateFullDTO) -> MessageDTO:
        await self.repository.save(message)

        response = await client.responses.create(
            model=settings.llm_model,
            input=message.content,
        )

        assistant_message = MessageCreateFullDTO(
            conversation_id=message.conversation_id,
            role=Role.ASSISTANT,
            content=response.output_text,
        )
        result: MessageDTO = await self.repository.save(assistant_message)

        return result
