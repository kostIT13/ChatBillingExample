from sqlalchemy import Column, Integer, String
from src.database import Base

class Chat(Base):

    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)