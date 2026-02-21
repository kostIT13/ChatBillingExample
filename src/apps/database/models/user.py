from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apps.database.database import Base
from sqlalchemy import String, Boolean, Float, Integer

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True) 
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    transactions = relationship("Transaction", back_populates="user", lazy="select")