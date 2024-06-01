from collections.abc import AsyncGenerator

from sqlalchemy.ext import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.connection import SQLALCHEMY_DATABASE_URL_async

async_engine = asyncio.create_async_engine(
    SQLALCHEMY_DATABASE_URL_async,
    pool_pre_ping=True,
    future=True,
)


AsyncSessionLocal = sessionmaker(  # type: ignore
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=asyncio.AsyncSession,
    expire_on_commit=False,
)


async def get_async_db() -> AsyncGenerator[None, AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
