from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class BooksModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str]
