import json
import logging

import aio_pika
from aiogram import Bot
from aiogram.types import User

from src import models
from src.db import AsyncSessionLocal, create_obj, get_parent_message
from src.schemas import MsgForward, MsgOut
from src.settings import settings

logger = logging.getLogger(__name__)


async def send_message(bot: Bot, message: MsgOut) -> None:
    logger.debug(f"send message: id={message.chat_id}, text='{message.text}'")
    tg_message = await bot.send_message(**message.model_dump())

    async with AsyncSessionLocal() as session:
        db_parent_message: models.Message | None = None
        if message.reply_to_message_id:
            db_parent_message = await get_parent_message(
                session=session,
                original_parent_id=message.reply_to_message_id,
            )

        db_message: models.Message = await create_obj(
            session=session,
            model=models.Message,
            original_id=tg_message.message_id,
            original_parent_id=(
                tg_message.reply_to_message.message_id
                if tg_message.reply_to_message
                else None
            ),
            direction=models.DirectionEnum.OUT,
            parent_id=(db_parent_message.id if db_parent_message else None),
            user_id=message.chat_id,
            user_name=str(message.chat_id),
            text=message.text,
        )
        logger.debug(f"message with id {db_message.id} added.")


async def forward_message(bot: Bot, message: MsgForward) -> None:
    logger.debug(f"forward message: id={message.chat_id}")
    tg_message = await bot.forward_message(**message.model_dump())

    async with AsyncSessionLocal() as session:
        db_parent_message: models.Message | None = await get_parent_message(
            session=session,
            original_parent_id=message.message_id,
        )

        db_message: models.Message = await create_obj(
            session=session,
            model=models.Message,
            direction=models.DirectionEnum.FORWARD,
            original_id=tg_message.message_id,
            original_parent_id=message.message_id,
            parent_id=(db_parent_message.id if db_parent_message else None),
            user_id=tg_message.forward_from and tg_message.forward_from.id,
            user_name=(
                user_name(tg_message.forward_from) if tg_message.forward_from else ""
            ),
            text="",
        )
        logger.debug(f"message with id {db_message.id} added.")


async def rabbit_loop(bot: Bot) -> None:
    logger.debug("start rabbit_loop")
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_SERVER,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_DEFAULT_USER,
        password=settings.RABBITMQ_DEFAULT_PASS,
        virtualhost=settings.RABBITMQ_DEFAULT_VHOST,
    )

    queue_name = "messages"

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for queue_message in queue_iter:
                async with queue_message.process():
                    data: dict = json.loads(queue_message.body.decode("utf-8"))
                    message_type: str | None = data.get("type")
                    message_body: dict | None = data.get("message")
                    logger.debug(f"start message '{message_type}' process")
                    logger.debug(f"message data = {message_body}")

                    if (
                        message_type is None
                        or message_type not in ("out", "forward")
                        or message_body is None
                    ):
                        raise Exception("Wrong message")

                    if message_type == "out":
                        await send_message(bot, MsgOut(**message_body))
                    else:  # forward
                        await forward_message(bot, MsgForward(**message_body))

                    logger.debug("finish message processing")

    logger.debug("fin rabbit_loop")


def user_name(user: User) -> str:
    return user.username or user.first_name or user.full_name or str(user.id)
