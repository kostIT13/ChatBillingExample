from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from typing import Annotated
from fastapi import Depends
import os


POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  
POSTGRES_DB = os.getenv("POSTGRES_DB", "mydb")


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(MappedAsDataclass, DeclarativeBase):
    pass

async def get_db():
    async with new_session() as session:
        yield session
    
SessionDep = Annotated[AsyncSession, Depends(get_db)]