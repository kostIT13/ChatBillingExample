from sqlalchemy.orm import Mapped, mapped_column
from database import Model

class BooksModel(Model):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: str 
    
