from dataclasses import dataclass
from os import environ


@dataclass
class Settings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    TG_BOT_TOKEN: str

    OPENAI_API_KEY: str


settings = Settings(
    POSTGRES_USER=environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=environ["POSTGRES_HOST"],
    POSTGRES_PORT=int(environ["POSTGRES_PORT"]),
    POSTGRES_DB=environ["POSTGRES_DB"],
    TG_BOT_TOKEN=environ["TG_BOT_TOKEN"],
    OPENAI_API_KEY=environ["OPENAI_API_KEY"],
)
