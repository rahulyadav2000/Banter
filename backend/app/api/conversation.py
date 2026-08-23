from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, ConversationMember, User
from app.schemas import ConversationCreate, ConversationResponse
from app.core import get_current_user
from app.services.conversation_service import (
    get_conversation_by_id,
    is_conversation_member,
    get_or_create_conversation,
    get_user_conversations,
)

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
