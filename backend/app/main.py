from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.conversation import router as conversation_router
from app.api.routes.message import router as message_router

app = FastAPI(
    title="AI Chat API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(conversation_router)
app.include_router(message_router)
