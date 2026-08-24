from openai import OpenAI
from app.core.config import get_settings

class ChatService:
    async def chat(self, message: str) -> str:
        settings = get_settings()

        client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
        )

        response = client.responses.create(
            model=settings.llm_model,
            input=message,
        )

        return response.output_text