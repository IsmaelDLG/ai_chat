from unittest.mock import AsyncMock, MagicMock
import pytest

from app.api.schemas.conversation import ConversationCreateDTO as requestDTO
from app.api.schemas.conversation import ConversationDTO as responseDTO
from app.services.conversation import (
    ConversationService,
)  # Ajusta este import a tu ruta real


@pytest.mark.asyncio
async def test_create_conversation_success():
    # Prepare
    mock_repository = MagicMock()

    dto_input = MagicMock(spec=requestDTO)
    expected_dto_response = MagicMock(spec=responseDTO)

    mock_repository.save = AsyncMock(return_value=expected_dto_response)

    service = ConversationService(mock_repository)

    # Act
    result = await service.create_conversation(dto_input)

    # Test
    mock_repository.save.assert_called_once_with(dto_input)

    assert result == expected_dto_response
