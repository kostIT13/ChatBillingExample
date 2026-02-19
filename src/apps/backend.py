import sys
import os
from fastapi import FastAPI
from src.api.auth.endpoints import router as auth_router 
from src.api.chat.endpoints import router as chat_router
from contextlib import asynccontextmanager
from pathlib import Path 
from src.database import Base, engine
from src.models.user import User
from src.models.chat import Chat


@asynccontextmanager
async def lifespan(app: FastAPI):

    if os.getenv("ENVIRONMENT", "development") == "development":
        print("Создание таблиц базы данных...")
        
        tables = Base.metadata.tables.keys()
        print(f"Таблицы для создания: {list(tables)}")
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы")
    
    yield 

    print("Остановка приложения...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=chat_router, prefix="/api/v1")
