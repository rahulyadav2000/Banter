from dataclasses import dataclass
from sqlalchemy.orm import Session
from app.core.secruity import decode_access_token
from app.models import User
from app.schemas import MessageResponse, MessageCreate
from app.services.conversation_service import get_conversation_for_user
from app.services.message_service import create_message
from app.database import get_db


class WebSocketMessageError(Exception):
    pass


@dataclass
class SavedMessage:
    message: dict
    recipient_id: list[int]


def authenticate_websocket(token: str) -> int | None:
    user_id = decode_access_token(token)
    if user_id is None:
        return None

    with get_db() as db:
        user = db.get(User, user_id)
        if user is None:
            return None
        return user_id


def save_websocket_message(
    user_id: int, conversation_id: int, content: str
) -> SavedMessage:
    clean_content = content.strip()
    if not clean_content:
        raise WebSocketMessageError("Message content is required")

    with get_db() as db:
        conversation = get_conversation_for_user(
            db=db, conversation_id=conversation_id, user_id=user_id
        )
        if conversation is None:
            raise WebSocketMessageError("Conversation not found")

        receipient_ids = [
            member.user_id
            for member in conversation.members
            if member.user_id != user_id
        ]

        message = create_message(
            db=db,
            data=MessageCreate(content=content),
            conversation_id=conversation_id,
            current_user_id=user_id,
        )

        db.commit()

        message_response = MessageResponse.model_validate(message).model_dump(
            mode="json"
        )

        return SavedMessage(message=message_response, recipient_id=receipient_ids)
