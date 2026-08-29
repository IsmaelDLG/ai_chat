from app.models.conversation import ConversationCreateDTO as requestDTO
from app.models.conversation import ConversationDTO as responseDTO
from app.dataaccess.repositories.conversation import ConversationRepository
from app.core.exceptions import ConversationSaveError


class ConversationService:
    def __init__(self, repo: ConversationRepository):
        self.repository = repo

    async def create_conversation(self, conversation: requestDTO) -> responseDTO:
        try:
            model: responseDTO = await self.repository.save(conversation)
        except Exception:
            raise ConversationSaveError()
        return model

    async def get_all_conversations(self) -> list[responseDTO]:
        models: list[responseDTO] = await self.repository.get_all()
        return models
