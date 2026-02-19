import os
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
        logger.error("Отсутсвуют переменные окружения")
        raise ValueError("Отсутствуют необходимые переменные окружения для подключения к БД")

    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

if "None" in DATABASE_URL:
    logger.error("Ошибка конфигурации")
    raise ValueError(f"Ошибка конфигурации: DATABASE_URL содержит None -> {DATABASE_URL}")


logger.info("Подключение к БД настроено")