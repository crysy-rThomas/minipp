from sqlalchemy import Column, ForeignKey, Integer, String
from infrastructure.database import Base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class Message(Base):
    class RoleMessage(str, PyEnum):
        ASSISTANT = "assistant"
        USER = "user"
        SYSTEM = "system"

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer)
    content = Column(String)
    role = Column(String)

    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")