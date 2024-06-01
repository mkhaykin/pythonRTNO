from src.settings import settings

REDIS_URL: str = f"redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}"
