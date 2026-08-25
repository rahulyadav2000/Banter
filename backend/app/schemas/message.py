import datetime

from pydantic import BaseModel, Field, ConfigDict
from app.schemas import UserPublic


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=3000)


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    user_id: int
    content: str
    created_at: datetime.datetime
    read_at: datetime.datetime | None
    user: UserPublic
