import json

from models.message import Message
from schemas.message_schema import MessageSchemaCreate
from services.fireworks_service import FireworksService
from services.message_service import MessageService


class TaskService:
    def __init__(self):
        # self.task_repository = TaskRepository()
        self.message_service = MessageService()
        self.fireworks_service = FireworksService()
        self.intent = None
        self.focus = None
        self.frame = None

    def process(self, user_input):
        self.extract_data(user_input.message)
        print(self.intent)

        message_user = self.message_service.create(
            MessageSchemaCreate(
                content=user_input.message,
                role=Message.RoleMessage.USER,
                conversation_id=user_input.conversation_id,
            )
        )
        self.conversation_id = message_user.conversation_id

        history = self.message_service.buildHistory(self.conversation_id)

        if self.intent == "Information":
            # graph search with the information
            # if not found, chat with the user
            print(self.focus)
            print(self.frame)
            response = self.fireworks_service.chat(
                history, "Nom: Chirac, Prenom: Jacques, Age: 89"
            )

        elif self.intent == "Find":
            return print("Graph search or WebSearch")
        elif (
            self.intent == "Create"
            or self.intent == "Update"
            or self.intent == "Delete"
        ):
            return print(
                "Create Graph Node, based on the information , and do the action"
            )
        elif self.intent == "Confirm":
            return print("Confirm the action")
        elif self.intent == "Reject":
            return print("Reject the action")
        elif self.intent == "Greet":
            response = self.fireworks_service.greeting(history)
        elif self.intent == "Goodbye":
            response = self.fireworks_service.goodbye(history)
        else:
            response = self.fireworks_service.chat(history, "Je n'ai pas compris")

        message_assistant = MessageSchemaCreate(
            content=response,
            role=Message.RoleMessage.ASSISTANT,
            conversation_id=self.conversation_id,
        )
        self.message_service.create(message_assistant)
        return response, self.conversation_id

    def extract_data(self, user_input):
        try:
            data = json.loads(self.fireworks_service.intent_detector(user_input))
            self.intent = data["Intent"]
            if "Focus" in data:
                self.focus = data["Focus"]
            if "Frame" in data:
                self.frame = data["Frame"]
        except Exception as e:
            print(e)
