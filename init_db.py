import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.database import engine, Base
from src.models.user import User

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы")

if __name__ == "__main__":
    asyncio.run(init_db())