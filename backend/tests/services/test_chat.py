from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.core.config import get_settings
from app.services.chat import ChatService


@pytest.mark.asyncio
async def test_chat():
    # Prepare
    settings = get_settings()

    mock_response = MagicMock()
    mock_response.output_text = "Esta es una respuesta del LLM"

    with patch("app.services.chat.client") as mock_client:
        mock_client.responses.create = AsyncMock(return_value=mock_response)

        service = ChatService()
        # Act
        result = await service.send_message("¿Qué es Docker?")

        # Assert
        assert result == "Esta es una respuesta del LLM"

        mock_client.responses.create.assert_awaited_once_with(
            model=settings.llm_model,
            input="¿Qué es Docker?",
        )
