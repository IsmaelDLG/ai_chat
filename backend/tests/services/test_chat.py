from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.core.config import get_settings
from app.services.chat import ChatService


@pytest.mark.asyncio
async def test_chat():
  settings = get_settings()

  # 1. Crear la respuesta mock simulando el objeto que tiene .output_text
  mock_response = MagicMock()
  mock_response.output_text = "Esta es una respuesta del LLM"

  # 2. Hacer patch directamente sobre la variable 'client' del módulo del servicio
  with patch("app.services.chat.client") as mock_client:
    # 3. Configurar 'responses.create' como AsyncMock
    mock_client.responses.create = AsyncMock(return_value=mock_response)

    service = ChatService()
    result = await service.send_message("¿Qué es Docker?")

    # 4. Validar el resultado
    assert result == "Esta es una respuesta del LLM"

    # 5. Verificar que se llamó a respuestas.create con los parámetros correctos
    mock_client.responses.create.assert_awaited_once_with(
        model=settings.llm_model,
        input="¿Qué es Docker?",
    )