import json
from datetime import datetime, timezone as tz
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.config import get_settings
from app.core.exceptions import (
    ConversationNotFoundError,
    InvalidMessageRoleError,
    LLMNotAvailableError,
    MessageNotFoundError,
    MessageSaveError,
)
from app.models.conversation import ConversationDTO
from app.models.message import MessageCreateFullDTO, MessageDTO, Role
from app.services.message import MessageService


def make_conversation(conversation_id: int = 1) -> ConversationDTO:
    now = datetime.now(tz.utc)
    return ConversationDTO(
        id=conversation_id,
        title="test",
        created_at=now,
        updated_at=now,
    )


def make_message(
    message_id: int = 1,
    role: Role = Role.USER,
    content: str = "Hello",
    conversation_id: int = 1,
) -> MessageDTO:
    return MessageDTO(
        id=message_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=datetime.now(tz.utc),
    )


@pytest.mark.asyncio
async def test_create_message_saves_only_user_message_and_updates_conversation():
    user_message = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hello",
    )
    saved_message = make_message()
    message_repository = MagicMock()
    message_repository.save = AsyncMock(return_value=saved_message)
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=make_conversation())
    conversation_repository.update_updated_at = AsyncMock()
    service = MessageService(message_repository, conversation_repository)

    result = await service.create_message(user_message)

    assert result == saved_message
    message_repository.save.assert_awaited_once_with(user_message)
    message_repository.get_by_conversation_id.assert_not_called()
    conversation_repository.update_updated_at.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_create_message_rejects_unknown_conversation():
    user_message = MessageCreateFullDTO(
        conversation_id=999,
        role=Role.USER,
        content="Hello",
    )
    message_repository = MagicMock()
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=None)
    service = MessageService(message_repository, conversation_repository)

    with pytest.raises(ConversationNotFoundError):
        await service.create_message(user_message)

    message_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_message_wraps_repository_save_error():
    user_message = MessageCreateFullDTO(
        conversation_id=1,
        role=Role.USER,
        content="Hello",
    )
    message_repository = MagicMock()
    message_repository.save = AsyncMock(side_effect=Exception("database error"))
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=make_conversation())
    conversation_repository.update_updated_at = AsyncMock()
    service = MessageService(message_repository, conversation_repository)

    with pytest.raises(MessageSaveError):
        await service.create_message(user_message)

    conversation_repository.update_updated_at.assert_not_awaited()


@pytest.mark.asyncio
async def test_generate_response_rejects_unknown_message():
    message_repository = MagicMock()
    message_repository.get_by_id = AsyncMock(return_value=None)
    conversation_repository = MagicMock()
    service = MessageService(message_repository, conversation_repository)

    with pytest.raises(MessageNotFoundError):
        await service.generate_response(404)

    message_repository.get_by_conversation_id.assert_not_called()
    message_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_generate_response_rejects_non_user_message():
    message_repository = MagicMock()
    message_repository.get_by_id = AsyncMock(
        return_value=make_message(role=Role.ASSISTANT)
    )
    conversation_repository = MagicMock()
    service = MessageService(message_repository, conversation_repository)

    with pytest.raises(InvalidMessageRoleError):
        await service.generate_response(1)

    conversation_repository.get_by_id.assert_not_called()
    message_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_generate_response_uses_saved_history_without_resaving_user_message():
    user_message = make_message()
    previous_assistant = make_message(
        message_id=2,
        role=Role.ASSISTANT,
        content="Earlier reply",
    )
    assistant_response = make_message(
        message_id=3,
        role=Role.ASSISTANT,
        content="How can I help?",
    )
    message_repository = MagicMock()
    message_repository.get_by_id = AsyncMock(return_value=user_message)
    message_repository.get_by_conversation_id = AsyncMock(
        return_value=[user_message, previous_assistant]
    )
    message_repository.save = AsyncMock(return_value=assistant_response)
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=make_conversation())
    conversation_repository.update_updated_at = AsyncMock()

    with patch("app.services.message.generate_response") as generate_response:
        generate_response.return_value = assistant_response.content
        service = MessageService(message_repository, conversation_repository)

        result = await service.generate_response(user_message.id)

    assert result == assistant_response
    generate_response.assert_awaited_once_with([
            {"role": Role.USER, "content": "Hello"},
            {"role": Role.ASSISTANT, "content": "Earlier reply"},
        ]
    )
    message_repository.save.assert_awaited_once()
    saved_assistant_message = message_repository.save.await_args.args[0]
    assert saved_assistant_message.role == Role.ASSISTANT
    assert saved_assistant_message.content == assistant_response.content
    conversation_repository.update_updated_at.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_generate_response_raises_llm_error_without_saving_assistant():
    user_message = make_message()
    message_repository = MagicMock()
    message_repository.get_by_id = AsyncMock(return_value=user_message)
    message_repository.get_by_conversation_id = AsyncMock(
        return_value=[user_message]
    )
    message_repository.save = AsyncMock()
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=make_conversation())
    conversation_repository.update_updated_at = AsyncMock()

    with patch("app.services.message.generate_response") as generate_response:
        generate_response.side_effect = LLMNotAvailableError()
        service = MessageService(message_repository, conversation_repository)

        with pytest.raises(LLMNotAvailableError):
            await service.generate_response(user_message.id)

    message_repository.save.assert_not_awaited()
    conversation_repository.update_updated_at.assert_not_awaited()


@pytest.mark.asyncio
async def test_generate_response_stream_emits_deltas_then_saved_response():
    user_message = make_message()
    assistant_response = make_message(
        message_id=2,
        role=Role.ASSISTANT,
        content="Hello world",
    )
    message_repository = MagicMock()
    message_repository.get_by_id = AsyncMock(return_value=user_message)
    message_repository.get_by_conversation_id = AsyncMock(
        return_value=[user_message]
    )
    message_repository.save = AsyncMock(return_value=assistant_response)
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=make_conversation())
    conversation_repository.update_updated_at = AsyncMock()

    async def mock_stream_response(messages):
        for text in ("Hello", " ", "world"):
            yield text

    with patch("app.services.message.stream_response", mock_stream_response):
        service = MessageService(message_repository, conversation_repository)
        stream = await service.generate_response_stream(user_message.id)
        chunks = [chunk async for chunk in stream]

    assert len(chunks) == 4
    assert json.loads(chunks[0])["content"] == "Hello"
    assert json.loads(chunks[-1])["content"] == "Hello world"
    assert json.loads(chunks[-1])["id"] == assistant_response.id
    message_repository.save.assert_awaited_once()
    conversation_repository.update_updated_at.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_messages_rejects_unknown_conversation():
    message_repository = MagicMock()
    conversation_repository = MagicMock()
    conversation_repository.get_by_id = AsyncMock(return_value=None)
    service = MessageService(message_repository, conversation_repository)

    with pytest.raises(ConversationNotFoundError):
        await service.get_messages(404)

    message_repository.get_by_conversation_id.assert_not_called()
