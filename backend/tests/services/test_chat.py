from unittest.mock import AsyncMock, patch

import pytest

from app.core.config import get_settings
from app.services.chat import ChatService


@pytest.mark.asyncio
async def test_chat():
    settings = get_settings()

    mock_response = AsyncMock()
    mock_response.output_text = "Esta es una respuesta del LLM"

    with patch("app.services.chat.AsyncOpenAI") as mock_client_class:
        mock_client = mock_client_class.return_value

        mock_client.responses.create = AsyncMock(
            return_value=mock_response
        )

        service = ChatService()

        result = await service.chat("¿Qué es Docker?")

        assert result == "Esta es una respuesta del LLM"

        mock_client.responses.create.assert_awaited_once_with(
            model=settings.llm_model,
            input="¿Qué es Docker?",
        )