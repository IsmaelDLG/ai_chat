class ConversationNotFoundError(Exception):
    """Thrown when a conversation is not found in DDBB"""

    def __init__(self, conversation_id: int):
        self.conversation_id = conversation_id
        super().__init__(f"Conversation with ID: {conversation_id} was not found.")


class MessageSaveError(Exception):
    """Thrown when a message cannot be saved in DDBB"""

    def __init__(self, content: str):
        self.content = content
        super().__init__(f'Message with content: "{content}" could not be saved.')


class MessageNotFoundError(Exception):
    """Thrown when a message is not found in DDBB"""

    def __init__(self, message_id: int):
        self.message_id = message_id
        super().__init__(f"Message with ID: {message_id} was not found.")


class InvalidMessageRoleError(Exception):
    """Thrown when a response is requested for a non-user message"""

    def __init__(self, message_id: int):
        self.message_id = message_id
        super().__init__(f"Message with ID: {message_id} is not a user message.")


class ConversationSaveError(Exception):
    """Thrown when a conversation cannot be saved in DDBB"""

    def __init__(self):
        super().__init__("Conversation could not be saved.")


class LLMNotAvailableError(Exception):
    """Thrown when llm is not available"""

    def __init__(self):
        super().__init__("Service unavailable, please try again later.")
