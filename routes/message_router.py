from fastapi import APIRouter

from schemas.message_schema import MessageSchemaCreate
from services.message_service import MessageService

message_router = APIRouter()

message_service = MessageService()

@message_router.get("/messages/{conversation_id}")
def get_messages(conversation_id: int):
    return message_service.get_all(conversation_id)

@message_router.get("/message/{id}")
def get_message_by_id(id: int):
    return message_service.get(id)

@message_router.post("/message")
def create_message(message: MessageSchemaCreate):
    return message_service.create(message)