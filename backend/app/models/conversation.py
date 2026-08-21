import datetime

from fastapi import FastAPI
from app.database import Base
from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    # Add relationship
    members = relationship(
        "ConversationMember",
        back_populates="conversations",
        cascade="all, delete-orphan",
    )
    messages = relationship(
        "Message", back_populates="conversations", cascade="all, delete-orphan"
    )


class ConversationMember(Base):
    __tablename__ = "conversation_members"

    # to pass additional constraints to the db table
    __table_args__ = (
        UniqueConstraint("conversation_id", "user_id", name="uq_conversation_member"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Add relationship
    conversations = relationship("Conversation", back_populates="members")
    user = relationship("User", back_populates="conversation_memberships")
