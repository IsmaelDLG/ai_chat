from app.dataaccess.models.conversation import Conversations
from app.api.schemas.conversation import ConversationCreateDTO, ConversationDTO
from app.dataaccess.repositories.base import BaseRepository


class ConversationRepository(BaseRepository):
    async def save(self, dto: ConversationCreateDTO) -> ConversationDTO:
        conversation = Conversations(**dto.model_dump())

        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        result = ConversationDTO.model_validate(conversation)
        return result

    async def get_by_id(self, conversation_id: int) -> Conversations | None:
        return await self.db.get(Conversations, conversation_id)
