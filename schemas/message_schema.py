from typing import Optional
from pydantic import BaseModel

from models.message import Message


class MessageSchemaCreate(BaseModel):
    content: str
    role: Message.RoleMessage
    conversation_id: Optional[int] = None

    def to_model(self):
        return Message(
            content=self.content, role=self.role, conversation_id=self.conversation_id
        )


class MessageSchemaRead(BaseModel):
    id: int
    content: str
    role: Message.RoleMessage
    conversation_id: int
    index: int
