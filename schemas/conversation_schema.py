from typing import Optional
from pydantic import BaseModel

from models.conversation import Conversation

class ConversationSchema(BaseModel):
    id: Optional[int] = None
    name: str

    def to_model(self):
        return Conversation(id=self.id, name=self.name)

