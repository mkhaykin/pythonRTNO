from logging import getLogger
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import models

logger = getLogger(__name__)


async def create_obj(
    session: AsyncSession,
    model: type[models.TBaseModel],
    **kwargs: Any | None,
) -> models.TBaseModel:
    logger.debug(f"create obj {model.__name__} with values {kwargs}")
    # TODO write log if Exception
    db_obj = model(**kwargs)
    try:
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
    except IntegrityError as err:
        await session.rollback()
        logger.debug(f"IntegrityError. Message: {err}")
        raise HTTPException(409, f"the {model.__tablename__} is duplicated")
    except DatabaseError as err:
        await session.rollback()
        logger.debug(f"DatabaseError. Message: {err}")
        raise HTTPException(424, f"DB error while creating {model.__tablename__}")
    return db_obj


async def get_parent_message(
    session: AsyncSession,
    original_parent_id: int,
) -> models.Message | None:
    # TODO try | except
    stmt = select(models.Message).where(models.Message.original_id == original_parent_id)
    result = await session.execute(stmt)
    item = result.scalars().one()  # TODO
    return item
