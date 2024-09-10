from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from enum import Enum as PyEnum
from infrastructure.database import Base


class Task(Base):

    class TaskStatus(str, PyEnum):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        DONE = "done"
        CANCELLED = "cancelled"

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    intent = Column(String)
    focus = Column(String)
    status = Column(Enum(TaskStatus))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
