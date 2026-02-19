from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import Annotated
from fastapi import Depends
from src.apps.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with new_session() as session:
        yield session
    
SessionDep = Annotated[AsyncSession, Depends(get_db)]