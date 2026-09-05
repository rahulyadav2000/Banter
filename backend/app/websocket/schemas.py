from typing import Literal

from pydantic import BaseModel, Field
from app.schemas import MessageResponse

class MessageSendEvent(BaseModel):
    type: Literal["message.send"]
    conversation_id:int 
    content: str = Field(min_length=1, max_length=3000)

class MessageCreatedEvent(BaseModel):
    type:Literal["message.created"] = "message.created"
    message:MessageResponse

class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str