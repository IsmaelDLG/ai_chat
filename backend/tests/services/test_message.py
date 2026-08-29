from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from datetime import datetime

from app.core.config import get_settings
from app.services.message import MessageService
from app.api.schemas.message import MessageCreateFullDTO, MessageDTO, Role
from app.api.schemas.conversation import ConversationDTO
from app.core.exceptions import (
    ConversationNotFoundError,
    MessageSaveError,
    LLMNotAvailableError,
)


@pytest.mark.asyncio
async def test_send_message_conversation_not_found():
    # Arrange
    dto_input = MessageCreateFullDTO(
        conversation_id=999,  # ID que no existe
        role=Role.USER,
        content="Hola",
    )

    mock_message_repository = MagicMock()
    mock_conversation_repository = MagicMock()

    mock_conversation_repository.get_by_id = AsyncMock(return_value=None)

    service = MessageService(mock_message_repository, mock_conversation_repository)

    # Act & Assert
    with pytest.raises(ConversationNotFoundError):
        await service.send_message(dto_input)

    mock_conversation_repository.get_by_id.assert_awaited_once_with(
        dto_input.conversation_id
    )
    mock_message_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_send_message_user_save_error():
    # Arrange

    dto_input = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hola, ¿cómo estás?",
    )

    conversation_dto = ConversationDTO(
        id=1, title="test", created_at=datetime.now(), updated_at=datetime.now()
    )

    mock_message_repository = MagicMock()
    expected_exc = Exception("Cannot save message")
    mock_message_repository.save = AsyncMock(side_effect=expected_exc)

    mock_conversation_repository = MagicMock()
    mock_conversation_repository.get_by_id = AsyncMock(return_value=conversation_dto)
    mock_conversation_repository.update_updated_at = AsyncMock()

    service = MessageService(mock_message_repository, mock_conversation_repository)

    # Act & Assert
    with pytest.raises(MessageSaveError):
        await service.send_message(dto_input)

    mock_conversation_repository.get_by_id.assert_awaited_once_with(
        dto_input.conversation_id
    )

    mock_message_repository.save.assert_awaited_once_with(dto_input)


@pytest.mark.asyncio
async def test_send_message_llm_error():
    # Arrange
    settings = get_settings()

    dto_input = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hola, ¿cómo estás?",
    )

    conversation_dto = ConversationDTO(
        id=1, title="test", created_at=datetime.now(), updated_at=datetime.now()
    )

    mock_message_repository = MagicMock()
    mock_message_repository.save = AsyncMock()

    mock_conversation_repository = MagicMock()
    mock_conversation_repository.get_by_id = AsyncMock(return_value=conversation_dto)
    mock_conversation_repository.update_updated_at = AsyncMock()

    with patch("app.services.message.client") as mock_client:
        mock_client.responses.create = AsyncMock(side_effect=Exception("LLM Error"))

        service = MessageService(mock_message_repository, mock_conversation_repository)

        # Act & Arrange
        with pytest.raises(LLMNotAvailableError):
            await service.send_message(dto_input)

        mock_conversation_repository.get_by_id.assert_awaited_once_with(
            dto_input.conversation_id
        )
        mock_message_repository.save.assert_awaited_once_with(dto_input)
        mock_client.responses.create.assert_awaited_once_with(
            model=settings.llm_model,
            input=dto_input.content,
        )
        mock_conversation_repository.update_updated_at.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_message():
    # Arrange
    settings = get_settings()

    dto_input = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hola, ¿cómo estás?",
    )

    conversation_dto = ConversationDTO(
        id=1, title="test", created_at=datetime.now(), updated_at=datetime.now()
    )

    assistant_dto_response = MessageDTO(
        id=2,
        conversation_id=1,
        role=Role.ASSISTANT,
        content="Bien, y tú?",
        created_at=datetime.now(),
    )

    mock_message_repository = MagicMock()
    mock_message_repository.save = AsyncMock(return_value=assistant_dto_response)

    mock_conversation_repository = MagicMock()
    mock_conversation_repository.get_by_id = AsyncMock(return_value=conversation_dto)
    mock_conversation_repository.update_updated_at = AsyncMock()

    mock_ai_client = MagicMock()
    mock_ai_client.output_text = "Bien, y tú?"

    with patch("app.services.message.client") as mock_client:
        mock_client.responses.create = AsyncMock(return_value=mock_ai_client)

        service = MessageService(mock_message_repository, mock_conversation_repository)

        # Act
        result = await service.send_message(dto_input)

        # Assert
        mock_conversation_repository.get_by_id.assert_awaited_once_with(
            dto_input.conversation_id
        )

        mock_client.responses.create.assert_awaited_once_with(
            model=settings.llm_model,
            input=dto_input.content,
        )

        mock_conversation_repository.update_updated_at.assert_awaited_once_with(
            dto_input.conversation_id
        )

        assert result.conversation_id == assistant_dto_response.conversation_id
        assert result.role == Role.ASSISTANT
        assert result.content == "Bien, y tú?"


@pytest.mark.asyncio
async def test_get_messages_conversation_not_found():
    # Arrange
    conversation_id = 999  # ID que no existe

    mock_message_repository = MagicMock()
    mock_conversation_repository = MagicMock()

    mock_conversation_repository.get_by_id = AsyncMock(return_value=None)

    service = MessageService(mock_message_repository, mock_conversation_repository)

    # Act & Assert
    with pytest.raises(ConversationNotFoundError):
        await service.get_messages(conversation_id)

    mock_conversation_repository.get_by_id.assert_awaited_once_with(conversation_id)


@pytest.mark.asyncio
async def test_get_messages():
    # Arrange
    conversation_id = 1

    conversation_dto = ConversationDTO(
        id=conversation_id,
        title="test",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    messages_dto_response = [
        MessageDTO(
            id=2,
            conversation_id=conversation_id,
            role=Role.ASSISTANT,
            content="Bien, y tú?",
            created_at=datetime.now(),
        ),
        MessageDTO(
            id=3,
            conversation_id=conversation_id,
            role=Role.USER,
            content="¿Y tú?",
            created_at=datetime.now(),
        ),
    ]

    mock_message_repository = MagicMock()
    mock_message_repository.get_by_conversation_id = AsyncMock(
        return_value=messages_dto_response
    )

    mock_conversation_repository = MagicMock()
    mock_conversation_repository.get_by_id = AsyncMock(return_value=conversation_dto)
    mock_conversation_repository.update_updated_at = AsyncMock()

    service = MessageService(mock_message_repository, mock_conversation_repository)

    # Act
    result = await service.get_messages(conversation_id)

    # Assert
    mock_conversation_repository.get_by_id.assert_awaited_once_with(conversation_id)

    mock_message_repository.get_by_conversation_id.assert_awaited_once_with(
        conversation_id
    )

    assert result == messages_dto_response
