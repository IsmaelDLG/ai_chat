from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import (
    ConversationNotFoundError,
    ConversationSaveError,
    MessageSaveError,
    LLMNotAvailableError,
)

from app.api.routes.health import router as health_router
from app.api.routes.conversation import router as conversation_router
from app.api.routes.message import router as message_router

app = FastAPI(
    title="AI Chat API",
    version="0.1.0",
)


@app.exception_handler(ConversationNotFoundError)
async def conversation_not_found_handler(
    request: Request, exc: ConversationNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(MessageSaveError)
async def message_save_handler(request: Request, exc: MessageSaveError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(ConversationSaveError)
async def conversation_save_handler(request: Request, exc: ConversationSaveError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(LLMNotAvailableError)
async def llm_not_available_handler(request: Request, exc: LLMNotAvailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"detail": str(exc)}
    )


# Generic catch-all handler for any unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred."},
    )


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(conversation_router)
app.include_router(message_router)
