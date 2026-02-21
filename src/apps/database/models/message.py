from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apps.database.database import Base
from sqlalchemy import String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from datetime import datetime, timezone


class MessageRole(str, enum.Enum):
    HUMAN = "human"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String(36), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole, name="message_role_enum"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    chat = relationship("Chat", back_populates="messages")