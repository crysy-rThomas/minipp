from fastapi import FastAPI

from schemas.input_schema import InputSchema
from services.task_service import TaskService

app = FastAPI()
task_service = TaskService()

@app.post("/")
def input(user_input: InputSchema):
    return task_service.process(user_input)
