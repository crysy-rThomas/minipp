from sqlalchemy.orm import Session
from models.conversation import Conversation
from infrastructure.database import get_db


class ConversationRepository:
    def __init__(self):
        db: Session = next(get_db())
        self.db = db

    def get(self, id: int) -> Conversation:
        return self.db.query(Conversation).filter(Conversation.id == id).first()

    def create(self, conversation: Conversation) -> Conversation:
        try:
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        except Exception as e:
            self.db.rollback()
            raise e
        return conversation

    def get_all(self):
        return self.db.query(Conversation).all()

    def delete(self, conversation: Conversation):
        try:
            self.db.delete(conversation)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        return conversation
