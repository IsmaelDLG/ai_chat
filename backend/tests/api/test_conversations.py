from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.conversation import router
from app.api.deps import get_conversation_service
from app.models.conversation import ConversationCreateDTO, ConversationDTO


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

    payload = {
        "title": "Test conversation"
    }

    # Act
    response = client.post(
        "/api/conversations",
        json=payload,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test conversation"

    mock_conversation_service.create_conversation.assert_awaited_once()