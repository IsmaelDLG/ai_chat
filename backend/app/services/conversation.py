from app.api.schemas.conversation import ConversationCreateDTO as requestDTO
from app.api.schemas.conversation import ConversationDTO as responseDTO
from app.dataaccess.repositories.conversation import ConversationRepository


class ConversationService:
    def __init__(self, repo: ConversationRepository):
        self.repository = repo

    async def create_conversation(self, conversation: requestDTO) -> responseDTO:
        model: responseDTO = await self.repository.save(conversation)
        return model
