from app.core.config import get_settings

from app.core.exceptions import LLMNotAvailableError
from openai import AsyncOpenAI

settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)

async def generate_response(messages: list[dict[str, str]]) -> str:
    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
        )
    except Exception:
        raise LLMNotAvailableError()
    
    response_str = response.choices[0].message.content

    return response_str
