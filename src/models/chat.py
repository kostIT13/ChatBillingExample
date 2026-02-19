from sqlalchemy.orm import Mapped, mapped_column
from src.apps.database import Base
from sqlalchemy import String

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String) 

