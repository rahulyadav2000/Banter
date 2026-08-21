import datetime

from fastapi import FastAPI
from app.database import Base
from sqlalchemy import func, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), index=True
    )
    read_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    # Add relationship
    conversations = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")
