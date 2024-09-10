from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )