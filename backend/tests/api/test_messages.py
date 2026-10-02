from datetime import datetime, timezone as tz
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_message_service
from app.core.exceptions import MessageNotFoundError
from app.main import app
from app.models.message import MessageDTO, Role


@pytest.fixture
def message_service():
    return MagicMock()


@pytest.fixture
def client(message_service, monkeypatch):
    monkeypatch.setitem(
        app.dependency_overrides,
        get_message_service,
        lambda: message_service,
    )
    return TestClient(app)


def make_message(
    message_id: int,
    role: Role,
    content: str,
) -> MessageDTO:
    return MessageDTO(
        id=message_id,
        conversation_id=1,
        role=role,
        content=content,
        created_at=datetime.now(tz.utc),
    )


def test_create_message_persists_without_generating_response(client, message_service):
    saved_message = make_message(10, Role.USER, "Hello")
    message_service.create_message = AsyncMock(return_value=saved_message)

    response = client.post(
        "/api/conversations/1/messages",
        json={"content": "Hello"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == saved_message.id
    assert response.json()["role"] == Role.USER.value
    message_service.create_message.assert_awaited_once()
    saved_input = message_service.create_message.await_args.args[0]
    assert saved_input.conversation_id == 1
    assert saved_input.role == Role.USER
    assert saved_input.content == "Hello"
    message_service.generate_response.assert_not_called()


def test_generate_response_routes_by_message_id(client, message_service):
    assistant_message = make_message(11, Role.ASSISTANT, "Hi!")
    message_service.generate_response = AsyncMock(return_value=assistant_message)

    response = client.post("/api/messages/10/response")

    assert response.status_code == 200
    assert response.json()["id"] == assistant_message.id
    message_service.generate_response.assert_awaited_once_with(10)


def test_generate_response_returns_not_found_for_unknown_message(client, message_service):
    message_service.generate_response = AsyncMock(
        side_effect=MessageNotFoundError(404)
    )

    response = client.post("/api/messages/404/response")

    assert response.status_code == 404
    assert "404" in response.json()["detail"]


def test_generate_stream_routes_by_message_id(client, message_service):
    async def message_stream():
        yield '{"id": null, "content": "Hi"}\n'

    message_service.generate_response_stream = AsyncMock(
        return_value=message_stream()
    )

    response = client.post("/api/messages/10/response/sse")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-ndjson"
    assert response.text == '{"id": null, "content": "Hi"}\n'
    message_service.generate_response_stream.assert_awaited_once_with(10)


def test_generate_stream_returns_not_found_for_unknown_message(client, message_service):
    message_service.generate_response_stream = AsyncMock(
        side_effect=MessageNotFoundError(404)
    )

    response = client.post("/api/messages/404/response/sse")

    assert response.status_code == 404
    assert "404" in response.json()["detail"]
