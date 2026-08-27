from openai import AsyncOpenAI
from app.core.config import get_settings

from app.api.schemas.message import MessageCreateDTO, MessageDTO, Role
from app.dataaccess.repositories.conversation import ConversationRepository


settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)

class MessageService:
    def __init__(self, repo: ConversationRepository):
        self.repository = repo

    async def send_message(self, message: MessageCreateDTO) -> MessageDTO:
        await self.repository.save(message)

        response = await client.responses.create(
            model=settings.llm_model,
            input=message.content,
        )

        responseDTO = MessageCreateDTO(
            conversation_id=message.conversation_id,
            role=Role.ASSISTANT,
            content= response.output_text
        )
        result: MessageDTO = await self.repository.save(responseDTO)

        return result


