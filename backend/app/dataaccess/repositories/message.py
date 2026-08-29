from sqlalchemy import select

from app.dataaccess.models.message import Messages
from app.models.message import MessageCreateFullDTO, MessageDTO
from app.dataaccess.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    async def get_by_conversation_id(self, conversation_id: int) -> list[MessageDTO]:
        stmt = (
            select(Messages)
            .where(Messages.conversation_id == conversation_id)
            .order_by(Messages.created_at.asc())
        )
        result = await self.session.execute(stmt)
        messages = result.scalars().all()
        return [MessageDTO.model_validate(message) for message in messages]

    async def save(self, dto: MessageCreateFullDTO) -> MessageDTO:
        message = Messages(**dto.model_dump())

        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)

        result = MessageDTO.model_validate(message)
        return result
