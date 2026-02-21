from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apps.database.database import Base
from sqlalchemy import Integer, ForeignKey, Float, Enum, String, DateTime
import enum 
from datetime import datetime
from sqlalchemy.sql import func


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    CHARGE = "charge"
    REFUND = "refund"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="transactions")