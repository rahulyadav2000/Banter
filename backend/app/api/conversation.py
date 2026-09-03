from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, ConversationMember, User
from app.schemas import (
    ConversationCreate,
    ConversationResponse,
    MessageResponse,
    MessageCreate,
)
from app.core import get_current_user
from app.services.conversation_service import (
    get_conversation_by_id,
    is_conversation_member,
    get_or_create_conversation,
    get_user_conversations,
    get_conversation_for_user,
)
from app.services.message_service import create_message, get_messages

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if data.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot create a conversation with yourself",
        )

    other_user = db.get(User, data.user_id)

    if other_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
        )

    return get_or_create_conversation(
        db=db, current_user_id=current_user.id, another_user_id=data.user_id
    )


@router.get("", response_model=list[ConversationResponse])
def list_conversations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return get_user_conversations(db=db, user_id=current_user.id)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    conversation = get_conversation_by_id(db=db, conversation_id=conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    if not is_conversation_member(
        db=db, conversation_id=conversation_id, user_id=current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this conversation",
        )

    return conversation


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def send_messages(
    db: Annotated[Session, Depends(get_db)],
    conversation_id: int,
    data: MessageCreate,
    current_user: Annotated[User, Depends(get_current_user)],
):
    conversation = get_conversation_for_user(
        db=db, user_id=current_user.id, conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            state_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    content = data.content.strip()

    if not content:
        raise HTTPException(
            state_code=status.HTTP_400_BAD_REQUEST, detail="Message content is required"
        )

    data.content = content

    message = create_message(
        db=db,
        data=data,
        conversation_id=conversation_id,
        current_user_id=current_user.id,
    )
    return message
    #return {"message": message.content}


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def list_messages(
    db: Annotated[Session, Depends(get_db)],
    conversation_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(default=50, ge=1, le=80),
    before_id: int = Query(default=None, ge=1),
):
    conversation = get_conversation_for_user(
        db=db, user_id=current_user.id, conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            state_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    messages = get_messages(
        db=db, conversation_id=conversation_id, before_id=before_id, limit=limit
    )
    return messages
    #return [{"message": message.content} for message in messages]
