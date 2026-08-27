from app.dataaccess.models.message import Messages
from app.api.schemas.message import MessageCreateFullDTO, MessageDTO
from app.dataaccess.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    async def save(self, dto: MessageCreateFullDTO) -> MessageDTO:
        message = Messages(**dto.model_dump())

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        result = MessageDTO.model_validate(message)
        return result
