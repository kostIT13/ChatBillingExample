from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apps.database.database import Base
from sqlalchemy import Integer, ForeignKey, Float, Enum, String, DateTime
import enum 
from datetime import datetime


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    CHARGE = "charge"
    REFUND = "refund"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[enum.Enum] = mapped_column(Enum(TransactionType), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="transactions")