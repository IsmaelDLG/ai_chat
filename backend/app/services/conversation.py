from app.api.schemas.conversation import ConversationCreateDTO as requestDTO
from app.api.schemas.conversation import ConversatioDTO as responseDTO
from app.dataaccess.repositories.conversation import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    async def create_conversation(self, conversation: requestDTO) -> dict:
        model: responseDTO = await self.repository.create(conversation)
        return model
