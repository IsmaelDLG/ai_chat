from app.dataaccess.models.conversation import Conversations
from app.api.schemas.conversation import ConversationCreateDTO
from app.api.schemas.conversation import ConversatioDTO
from app.dataaccess.repositories.base import BaseRepository


class ConversationRepository(BaseRepository):
    async def create(self, dto: ConversationCreateDTO) -> Conversations:
        conversation = Conversations(**dto.model_dump())
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return self.entity2model(conversation, ConversatioDTO)

    async def get_by_id(self, conversation_id: int) -> Conversations | None:
        return await self.db.get(Conversations, conversation_id)
