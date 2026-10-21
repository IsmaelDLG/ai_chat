from fastapi import APIRouter, Depends, Response

from app.models.conversation import ConversationCreateDTO, ConversationDTO
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


@router.put("/{conversation_id}/title/generate", response_model=ConversationDTO)
async def generate_title(
    conversation_id: int,
    service: ConversationService = Depends(get_conversation_service),
) -> None:
    response: ConversationDTO = await service.generate_title(conversation_id)
    return response
