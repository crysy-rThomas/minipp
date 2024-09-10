from repository.conversation_repository import ConversationRepository
from repository.message_repository import MessageRepository


class ConversationService:
    def __init__(self):
        self.conversation_repository = ConversationRepository()
        self.message_repository = MessageRepository()

    def get(self, id: int):
        return self.conversation_repository.get(id)
    
    def get_all(self):
        return self.conversation_repository.get_all()
    
    def create(self, conversationSchema):
        return self.conversation_repository.create(conversationSchema.to_model())
    
    def delete(self, id: int):
        conversation = self.conversation_repository.get(id)
        return self.conversation_repository.delete(conversation)
    
    def get_last_message(self, conversation_id: int):
        messages = self.message_repository.get_all(conversation_id)
        if not messages:
            return None
        return messages[-1]