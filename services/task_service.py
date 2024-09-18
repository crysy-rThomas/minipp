import json

from models.message import Message
from schemas.message_schema import MessageSchemaCreate
from services.fireworks_service import FireworksService
from services.knowledge_service import KnowledgeService
from services.message_service import MessageService


class TaskService:
    def __init__(self):
        # self.task_repository = TaskRepository()
        self.message_service = MessageService()
        self.fireworks_service = FireworksService()
        self.data = {}
        self.kg = KnowledgeService()

    def process(self, user_input):
        self.extract_data(user_input.message)
        print(self.data["Intent"])

        message_user = self.message_service.create(
            MessageSchemaCreate(
                content=user_input.message,
                role=Message.RoleMessage.USER,
                conversation_id=user_input.conversation_id,
            )
        )
        self.conversation_id = message_user.conversation_id

        history = self.message_service.buildHistory(self.conversation_id)

        intent_actions = {
            "Information": self.handle_find,
            "Find": self.handle_find,
            "Create": self.handle_create_update_delete,
            "Update": self.handle_create_update_delete,
            "Delete": self.handle_create_update_delete,
            "Confirm": self.handle_confirm,
            "Reject": self.handle_reject,
            "Greet": self.handle_greet,
            "Goodbye": self.handle_goodbye,
        }

        response = intent_actions.get(self.data["Intent"], self.handle_default)(history)

        message_assistant = MessageSchemaCreate(
            content=response,
            role=Message.RoleMessage.ASSISTANT,
            conversation_id=self.conversation_id,
        )
        self.message_service.create(message_assistant)
        return response, self.conversation_id

    def extract_data(self, user_input):
        try:
            self.data = json.loads(self.fireworks_service.intent_detector(user_input))
        except Exception as e:
            print(e)

    def handle_find(self, history):
        kg = self.kg.request(self.data, history)

        response = self.fireworks_service.chat(history, kg)
        return response

    def handle_create_update_delete(self, history):
        res = self.kg.request(self.data, history)
        return self.fireworks_service.chat(history, res)

    def handle_confirm(self, history):
        print("Confirm the action")
        return

    def handle_reject(self, history):
        print("Reject the action")
        return

    def handle_greet(self, history):
        return self.fireworks_service.greeting(history)

    def handle_goodbye(self, history):
        return self.fireworks_service.goodbye(history)

    def handle_default(self, history):
        return self.fireworks_service.chat(history, "Je n'ai pas compris")
