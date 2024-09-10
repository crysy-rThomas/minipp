from repository.message_repository import MessageRepository


class MessageService:
    def __init__(self):
        self.message_repository = MessageRepository()

    def get(self, id: int):
        return self.message_repository.get(id)

    def create(self, messageSchema):
        return self.message_repository.create(messageSchema.to_model())

    def get_all(self, conversation_id: int):
        return self.message_repository.get_all(conversation_id)
    
    
