import json
from services.fireworks_service import FireworksService


class TaskService:
    def __init__(self):
        # self.task_repository = TaskRepository()
        self.fireworks_service = FireworksService()
        self.intent = None
        self.focus = None
        self.frame = None

    def process(self, user_input):
        self.extract_data(user_input.message)
        print(self.intent)
        if self.intent == "Information":
            return self.fireworks_service.chat(user_input.message, "Nom: Chirac, Prenom: Jacques, Age: 89")
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
            return self.fireworks_service.greeting(user_input.message)
        elif self.intent == "Goodbye":
            return self.fireworks_service.goodbye(user_input.message)
        else:
            return self.fireworks_service.chat(user_input.message, "Je n'ai pas compris")

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
