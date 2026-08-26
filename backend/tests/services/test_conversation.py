from unittest.mock import AsyncMock, MagicMock
import pytest

from app.api.schemas.conversation import ConversationCreateDTO as requestDTO
from app.api.schemas.conversation import ConversatioDTO as responseDTO
from app.services.conversation import ConversationService  # Ajusta este import a tu ruta real


@pytest.mark.asyncio
async def test_create_conversation_success():
  # 1. Arrange (Preparación)
  mock_repository = MagicMock()

  # Mock para el DTO de entrada y el DTO retornado por el repositorio
  dto_input = MagicMock(spec=requestDTO)
  expected_dto_response = MagicMock(spec=responseDTO)

  # Configuramos el método asíncrono 'create' del repositorio
  mock_repository.create = AsyncMock(return_value=expected_dto_response)

  service = ConversationService(repository=mock_repository)

  # 2. Act (Ejecución)
  result = await service.create_conversation(dto_input)

  # 3. Assert (Verificaciones)
  # Verifica que el repositorio fue llamado exactamente una vez con el DTO esperado
  mock_repository.create.assert_called_once_with(dto_input)

  # Verifica que el servicio devuelva el resultado esperado sin ir a la BBDD
  assert result == expected_dto_response