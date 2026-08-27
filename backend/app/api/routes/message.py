from fastapi import APIRouter, Depends

from app.api.schemas.message import (
    MessageCreateDTO,
    MessageCreateFullDTO,
    MessageDTO,
    Role,
)
from app.services.message import MessageService

from app.api.deps import get_message_service

router = APIRouter(
    prefix="/api/conversations/{conversation_id}/messages", tags=["message"]
)


@router.post("", response_model=MessageDTO)
async def message(
    conversation_id: int,
    dto: MessageCreateDTO,
    service: MessageService = Depends(get_message_service),
):
    fullDTO = MessageCreateFullDTO(
        **dto.model_dump(), conversation_id=conversation_id, role=Role.USER
    )
    response: MessageDTO = await service.send_message(fullDTO)

    return response
