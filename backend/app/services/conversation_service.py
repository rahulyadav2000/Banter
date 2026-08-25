from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Conversation, ConversationMember


def get_conversation_by_id(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    statement = (
        select(Conversation)
        .options(
            selectinload(Conversation.members).selectinload(ConversationMember.user)
        )
        .where(Conversation.id == conversation_id)
    )

    return db.scalar(statement)


def is_conversation_member(db: Session, conversation_id: int, user_id: int) -> bool:
    statement = select(ConversationMember.id).where(
        ConversationMember.conversation_id == conversation_id,
        ConversationMember.user_id == user_id,
    )

    return db.scalar(statement) is not None


def find_direct_conversations(
    db: Session, user_id: int, another_user_id: int
) -> Conversation | None:
    statement = (
        select(Conversation)
        .join(ConversationMember)
        .options(
            selectinload(Conversation.members).selectinload(ConversationMember.user)
        )
        .where(ConversationMember.user_id == user_id)
    )

    conversations = list(db.scalars(statement).unique().all())

    target_members = {user_id, another_user_id}

    for conv in conversations:
        member_ids = {member.user_id for member in conv.members}

        if member_ids == target_members:
            return conv
    return None


def create_conversation(
    db: Session, current_user_id: int, another_user_id: int
) -> Conversation:
    conversation = Conversation()
    db.add(conversation)
    db.flush()

    current_member = ConversationMember(
        conversation_id=conversation.id, user_id=current_user_id
    )
    another_member = ConversationMember(
        conversation_id=conversation.id, user_id=another_user_id
    )

    db.add_all([current_member, another_member])
    db.commit()

    return get_conversation_by_id(db, conversation.id)


def get_or_create_conversation(
    db: Session, current_user_id: int, another_user_id: int
) -> Conversation:
    existing = find_direct_conversations(db, current_user_id, another_user_id)

    if existing:
        return existing

    return create_conversation(db, current_user_id, another_user_id)


def get_user_conversations(db: Session, user_id: int) -> list[Conversation]:
    statement = (
        select(Conversation)
        .join(ConversationMember)
        .options(
            selectinload(Conversation.members).selectinload(ConversationMember.user)
        )
        .where(ConversationMember.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )

    return list(db.scalars(statement).unique().all())


def get_conversation_for_user(
    db: Session, user_id: int, conversation_id: int
) -> Conversation | None:
    statement = (
        select(Conversation)
        .options(
            selectinload(Conversation.members).selectinload(ConversationMember.user)
        )
        .where(
            Conversation.id == conversation_id, ConversationMember.user_id == user_id
        )
    )

    return db.scalar(statement)
