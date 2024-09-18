from repository.message_repository import MessageRepository
from schemas.conversation_schema import ConversationSchema
from services.conversation_service import ConversationService


class MessageService:
    def __init__(self):
        self.conversation_service = ConversationService()
        self.message_repository = MessageRepository()

    def get(self, id: int):
        return self.message_repository.get(id)

    def create(self, messageSchema):
        if not messageSchema.conversation_id:
            conversationSchema = ConversationSchema(name=messageSchema.content)
            conversation = self.conversation_service.create(conversationSchema)
            messageSchema.conversation_id = conversation.id

        return self.message_repository.create(messageSchema.to_model())

    def get_all(self, conversation_id: int):
        return self.message_repository.get_all(conversation_id)

    def buildHistory(self, conversation_id: int):
        messages = self.get_all(conversation_id)
        history = ""
        for message in messages:
            history += "role: " + message.role + " content: " + message.content + "\n"
        return history
