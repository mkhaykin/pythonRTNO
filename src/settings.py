from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_SERVER: str
    REDIS_PORT: int
    CACHE_LIFETIME: int

    RABBITMQ_SERVER: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_DEFAULT_VHOST: str

    TG_BOT_ID: int
    TG_BOT_TOKEN: str
    TG_BOT_API_HOST: str

    OPENAI_API_KEY: str


settings = Settings(
    POSTGRES_USER=environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=environ["POSTGRES_HOST"],
    POSTGRES_PORT=int(environ["POSTGRES_PORT"]),
    POSTGRES_DB=environ["POSTGRES_DB"],
    REDIS_SERVER=environ["REDIS_SERVER"],
    REDIS_PORT=int(environ["REDIS_PORT"]),
    CACHE_LIFETIME=int(environ["CACHE_LIFETIME"]),
    RABBITMQ_SERVER=environ["RABBITMQ_SERVER"],
    RABBITMQ_PORT=int(environ["RABBITMQ_PORT"]),
    RABBITMQ_DEFAULT_USER=environ["RABBITMQ_DEFAULT_USER"],
    RABBITMQ_DEFAULT_PASS=environ["RABBITMQ_DEFAULT_PASS"],
    RABBITMQ_DEFAULT_VHOST=environ["RABBITMQ_DEFAULT_VHOST"],
    TG_BOT_ID=int(environ["TG_BOT_ID"]),
    TG_BOT_TOKEN=environ["TG_BOT_TOKEN"],
    TG_BOT_API_HOST=environ["TG_BOT_API_HOST"],
    OPENAI_API_KEY=environ["OPENAI_API_KEY"],
)
