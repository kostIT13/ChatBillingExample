import sys
import os
import logging
from fastapi import FastAPI
from src.api.auth.endpoints import router as auth_router 
from src.api.chat.endpoints import router as chat_router
from contextlib import asynccontextmanager
from pathlib import Path 
from src.apps.database import Base, engine
from src.models import User, Chat


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Создание таблиц")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных готова к работе")
    except Exception as e:
        logger.exception("Ошибка при создании таблиц")
        raise e
    
    yield
    
    logger.info("Выключение сервера")

app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, prefix='/api/v1')
app.include_router(router=chat_router, prefix='/api/v1')
