# backend/tests/services/test_conversation.py
from unittest.mock import AsyncMock, MagicMock
import pytest

from app.api.schemas.conversation import ConversationCreateDTO as requestDTO
from app.api.schemas.conversation import ConversationDTO as responseDTO
from app.services.conversation import (
    ConversationService,
)  # Ajusta este import a tu ruta real
from app.core.exceptions import ConversationSaveError


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


@pytest.mark.asyncio
async def test_create_conversation_error():
    # Prepare
    mock_repository = MagicMock()

    dto_input = MagicMock(spec=requestDTO)
    expected_exception = Exception("Failed to save conversation")

    mock_repository.save = AsyncMock(side_effect=expected_exception)

    service = ConversationService(mock_repository)

    with pytest.raises(ConversationSaveError):
        await service.create_conversation(dto_input)


@pytest.mark.asyncio
async def test_get_all_conversations_success():
    # Prepare
    mock_repository = MagicMock()

    expected_dto_responses = [MagicMock(spec=responseDTO), MagicMock(spec=responseDTO)]
    mock_repository.get_all = AsyncMock(return_value=expected_dto_responses)

    service = ConversationService(mock_repository)

    # Act
    result = await service.get_all_conversations()

    # Test
    mock_repository.get_all.assert_called_once_with()
    assert len(result) == 2
    assert all(isinstance(item, responseDTO) for item in result)
