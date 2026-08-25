from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models import Message
from app.schemas import MessageCreate


def create_message(
    db: Session, data: MessageCreate, conversation_id: int, current_user_id: int
) -> Message:
    content = data.content.strip()

    message = Message(
        conversation_id=conversation_id, user_id=current_user_id, content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session, conversation_id: int, before_id: int | None = None, limit: int = 40
) -> list[Message]:
    statement = (
        select(Message)
        .options(selectinload(Message.user))
        .where(Message.conversation_id == conversation_id)
    )
    # uses cursor pagination
    if before_id is not None:
        statement = statement.where(Message.id < before_id)

    statement = statement.order_by(Message.id.desc()).limit(limit)

    messages = list(db.scalars(statement).all())

    messages.reverse()

    return messages
