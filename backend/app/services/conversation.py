from app.models.conversation import ConversationCreateDTO as requestDTO
from app.models.conversation import ConversationDTO as responseDTO
from app.models.message import ChatCompletionMessage
from app.dataaccess.repositories.conversation import ConversationRepository
from app.dataaccess.repositories.message import MessageRepository
from app.core.exceptions import ConversationNotFoundError, ConversationSaveError
from app.integrations.llm.chat import generate_response


class ConversationService:
    def __init__(self, repo: ConversationRepository, msg_repo: MessageRepository):
        self.repository = repo
        self.msg_repository = msg_repo

    async def create_conversation(self, conversation: requestDTO) -> responseDTO:
        try:
            model: responseDTO = await self.repository.save(conversation)
        except Exception:
            raise ConversationSaveError()
        return model

    async def get_all_conversations(self) -> list[responseDTO]:
        models: list[responseDTO] = await self.repository.get_all()
        return models

    async def generate_title(self, conversation_id: int) -> responseDTO:
        conversation: responseDTO = await self.repository.get_by_id(conversation_id)
        if not conversation:
            raise ConversationNotFoundError(conversation_id)

        messages = await self.msg_repository.get_by_conversation_id(conversation_id)
        if not messages:
            raise ConversationNotFoundError(conversation_id)

        messages_parsed = [ChatCompletionMessage.model_validate(message.model_dump()) for message in messages]
        messages_parsed.append(ChatCompletionMessage(role="user", content="Based on the conversation so far, what would be a good title? Please, generate one in the language of the previous messages. Return it as plain text, without quotes or any other formatting. Keep it short."))
        messages = [message.model_dump() for message in messages_parsed]

        response_str = await generate_response(messages)

        conversation.title = response_str
        try:
            await self.repository.update_title(conversation_id, response_str)
        except Exception:
            raise ConversationSaveError()

        return conversation


        
