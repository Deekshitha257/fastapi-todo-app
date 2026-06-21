from pydantic import BaseModel
from pydantic import ConfigDict

class TodoCreate(BaseModel): ## TodoCreate validates incoming data, TodoResponse validates and filters outgoing data.
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str
    completed: bool    

class TodoResponse(BaseModel): ## response_model acts as a response filter/validator—only fields defined in TodoResponse are returned to the client, hiding unwanted model fields and improving Swagger docs.
    id: int
    title: str
    completed: bool
    user_id: int
    model_config = ConfigDict(from_attributes=True)