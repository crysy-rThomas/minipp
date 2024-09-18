from pydantic import BaseModel


class OutputSchema(BaseModel):
    Intent: str
    Focus: str
    Frame: dict
