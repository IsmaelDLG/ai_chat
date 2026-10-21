from openai import AsyncOpenAI

from app.core.config import get_settings

settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)
