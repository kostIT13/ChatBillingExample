from sqlalchemy.orm import Mapped, mapped_column
from src.apps.database import Base
from sqlalchemy import String, Boolean, Float, Integer

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True) 
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)