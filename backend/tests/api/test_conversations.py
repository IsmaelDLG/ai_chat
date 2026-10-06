from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.conversation import router
from app.api.deps import get_conversation_service
from app.models.conversation import ConversationCreateDTO, ConversationDTO
from datetime import datetime, timezone as tz


@pytest.fixture
def mock_conversation_service():
    return MagicMock()


@pytest.fixture
def client(mock_conversation_service):
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_conversation_service] = (
        lambda: mock_conversation_service
    )

    return TestClient(app)


def test_create_conversation(client, mock_conversation_service):
    # Arrange
    expected_response = ConversationDTO(
        id=1,
        title="Test conversation",
        created_at="2026-08-29T10:00:00Z",
        updated_at="2026-08-29T10:00:00Z",
    )

    mock_conversation_service.create_conversation = AsyncMock(
        return_value=expected_response
    )

    payload = ConversationCreateDTO(title="Test conversation").model_dump()

    print(type(payload), payload)
    # Act
    response = client.post(
        "/api/conversations",
        json=payload,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == expected_response.id
    assert response.json()["title"] == expected_response.title

    mock_conversation_service.create_conversation.assert_awaited_once()


def test_get_all_conversations(client, mock_conversation_service):
    # Arrange
    expected_responses = [
        ConversationDTO(
            id=1, title="Test Conversation 1", created_at=datetime.now(tz.utc)
        ),
        ConversationDTO(
            id=2, title="Test Conversation 2", created_at=datetime.now(tz.utc)
        ),
    ]

    mock_conversation_service.get_all_conversations = AsyncMock(
        return_value=expected_responses
    )

    # Act
    response = client.get("/api/conversations")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["title"] == "Test Conversation 1"
    assert response.json()[1]["id"] == 2
    assert response.json()[1]["title"] == "Test Conversation 2"

    mock_conversation_service.get_all_conversations.assert_awaited_once()

def test_generate_conversation_title(client, mock_conversation_service):
    # Arrange
    expected_response = ConversationDTO(
        id=1,
        title="Generated Title",
        created_at=datetime.now(tz.utc),
        updated_at=datetime.now(tz.utc),
    )

    mock_conversation_service.generate_title = AsyncMock()   

    # Act
    response = client.put(
        f"/api/conversations/{expected_response.id}/title/generate",
        json={}
    )

    # Assert
    assert response.status_code == 204
    mock_conversation_service.generate_title.assert_awaited_once_with(expected_response.id)