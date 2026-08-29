from app.dataaccess.models.conversation import Conversations
from app.api.schemas.conversation import ConversationCreateDTO, ConversationDTO
from app.dataaccess.repositories.base import BaseRepository
from datetime import datetime, timezone as tz
from sqlalchemy import update, select


class ConversationRepository(BaseRepository):
    async def save(self, dto: ConversationCreateDTO) -> ConversationDTO:
        conversation = Conversations(**dto.model_dump())

        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)

        result = ConversationDTO.model_validate(conversation)
        return result

    async def get_all(self) -> list[ConversationDTO]:
        stmt = select(Conversations).order_by(Conversations.updated_at.desc())
        result = await self.session.execute(stmt)
        conversations = result.scalars().all()
        return [
            ConversationDTO.model_validate(conversation)
            for conversation in conversations
        ]

    async def get_by_id(self, conversation_id: int) -> ConversationDTO | None:
        result = await self.session.get(Conversations, conversation_id)
        if result:
            result = ConversationDTO.model_validate(result)
        return result

    async def update_updated_at(
        self, conversation_id: int, updated_at: datetime = datetime.now(tz.utc)
    ):
        query = (
            update(Conversations)
            .where(Conversations.id == conversation_id)
            .values(updated_at=updated_at)
        )
        await self.session.execute(query)
        await self.session.commit()
