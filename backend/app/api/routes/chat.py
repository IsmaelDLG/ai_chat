from fastapi import APIRouter

from app.api.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter(prefix="/api", tags=["chat"])

chat_service = ChatService()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await chat_service.chat(request.content)

    return ChatResponse(response=response)
