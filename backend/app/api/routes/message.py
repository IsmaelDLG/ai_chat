from fastapi import APIRouter, Depends

from app.api.schemas.message import MessageCreateDTO, MessageDTO
from app.services.message import MessageService

from app.api.deps import get_message_service

router = APIRouter(prefix="/api", tags=["message"])

@router.post("/", response_model=MessageDTO)
async def message(dto: MessageCreateDTO, service: MessageService = Depends(get_message_service)):
    response: MessageDTO = await service.send_message(dto)

    return response
