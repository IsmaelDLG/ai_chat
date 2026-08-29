from fastapi import APIRouter, Depends

from app.api.schemas.conversation import ConversationCreateDTO, ConversationDTO
from app.services.conversation import ConversationService
from app.api.deps import get_conversation_service

router = APIRouter(prefix="/api/conversations", tags=["conversation"])


@router.post("", response_model=ConversationDTO)
async def create(
    dto: ConversationCreateDTO,
    service: ConversationService = Depends(get_conversation_service),
) -> ConversationDTO:
    response: ConversationDTO = await service.create_conversation(dto)
    return response


@router.get("", response_model=list[ConversationDTO])
async def get_all(
    service: ConversationService = Depends(get_conversation_service),
) -> list[ConversationDTO]:
    response: list[ConversationDTO] = await service.get_all_conversations()
    return response
