from fastapi import APIRouter

from schemas.conversation_schema import ConversationSchema
from services.conversation_service import ConversationService

conversation_router = APIRouter()

conversation_service = ConversationService()

@conversation_router.get("/conversation")
def get_conversations():
    return conversation_service.get_all()

@conversation_router.post("/conversation")
def create_conversation(conversation: ConversationSchema):
    return conversation_service.create(conversation)

@conversation_router.get("/conversation/{id}")
def get_conversation_by_id(id: int):
    return conversation_service.get(id)

@conversation_router.delete("/conversation/{id}")
def delete_conversation(id: int):
    return conversation_service.delete(id)

@conversation_router.get("/conversation/{id}/last_message")
def get_last_message(id: int):
    return conversation_service.get_last_message(id)