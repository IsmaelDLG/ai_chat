from fastapi import APIRouter, Depends

from app.models.message import (
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


@router.get("", response_model=list[MessageDTO])
async def get(
    conversation_id: int,
    service: MessageService = Depends(get_message_service),
):
    response: list[MessageDTO] = await service.get_messages(conversation_id)
    return response


@router.post("", response_model=MessageDTO)
async def create(
    conversation_id: int,
    dto: MessageCreateDTO,
    service: MessageService = Depends(get_message_service),
):
    fullDTO = MessageCreateFullDTO(
        **dto.model_dump(), conversation_id=conversation_id, role=Role.USER
    )
    response: MessageDTO = await service.send_message(fullDTO)

    return response
