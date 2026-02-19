# import os
# from dotenv import load_dotenv


# load_dotenv()
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  
# POSTGRES_DB = os.getenv("POSTGRES_DB")

# DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

import os
from dotenv import load_dotenv

# Пытаемся загрузить .env (работает только локально, в Docker файла нет)
load_dotenv()

# 1. Сначала пробуем взять ГОТОВЫЙ URL (который передаёт Docker Compose)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Если готового URL нет (значит, мы запускаем локально без Docker), собираем его сами
if not DATABASE_URL:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
        raise ValueError("❌ Отсутствуют необходимые переменные окружения для подключения к БД")

    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# Проверка на всякий случай (чтобы не было None в строке)
if "None" in DATABASE_URL:
    raise ValueError(f"❌ Ошибка конфигурации: DATABASE_URL содержит None -> {DATABASE_URL}")

print(f"✅ Подключение к БД настроено: {DATABASE_URL.replace(os.getenv('POSTGRES_PASSWORD', ''), '***')}")