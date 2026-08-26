from fastapi import APIRouter, Depends

from app.api.schemas.conversation import ConversationCreateDTO, ConversatioDTO
from app.services.conversation import ConversationService
from app.api.deps import get_conversation_service

router = APIRouter(prefix="/api", tags=["conversation"])


@router.post("", response_model=ConversatioDTO)
async def create(
    dto: ConversationCreateDTO,
    service: ConversationService = Depends(get_conversation_service),
) -> ConversatioDTO:
    response: ConversatioDTO = await service.create_conversation(dto)
    return response
