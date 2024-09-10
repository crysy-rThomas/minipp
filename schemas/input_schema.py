from typing import Optional
from pydantic import BaseModel


class InputSchema(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    