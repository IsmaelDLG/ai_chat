from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from datetime import datetime

from app.core.config import get_settings
from app.services.message import MessageService
from app.api.schemas.message import MessageCreateFullDTO, MessageDTO, Role


@pytest.mark.asyncio
async def test_message():
    # Prepare
    settings = get_settings()

    dto_input = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hola, ¿cómo estás?",
    )

    expected_dto_response = MessageDTO(
        id=1,
        conversation_id=1,
        role=Role.ASSISTANT,
        content="Bien, y tú?",
        created_at=datetime.now(),
    )
    mock_repository = MagicMock()
    mock_repository.save = AsyncMock(return_value=expected_dto_response)

    mock_ai_client = MagicMock()
    mock_ai_client.output_text = "Bien, y tú?"

    with patch("app.services.message.client") as mock_client:
        mock_client.responses.create = AsyncMock(return_value=mock_ai_client)

        service = MessageService(mock_repository)
        # Act
        result = await service.send_message(dto_input)

        # Assert
        mock_repository.save.assert_any_await(dto_input)

        assert result.conversation_id == expected_dto_response.conversation_id
        assert result.role == expected_dto_response.role
        assert result.content == expected_dto_response.content

        mock_client.responses.create.assert_awaited_once_with(
            model=settings.llm_model,
            input=dto_input.content,
        )
