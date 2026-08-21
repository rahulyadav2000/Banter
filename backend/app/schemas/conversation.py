import datetime
from pydantic import BaseModel, Field, ConfigDict


class ConversationCreate(BaseModel):
    user_id: int


class ConversationMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    members: list[ConversationMemberResponse]
