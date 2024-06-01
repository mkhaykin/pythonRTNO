import asyncio
import logging

import httpx
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from src import models
from src.bot.rabbit import rabbit_loop
from src.db import AsyncSessionLocal, create_obj, get_parent_message
from src.schemas import user_name

dp = Dispatcher()
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        text="Hi!",
    )


@dp.message()
async def base_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender
    """
    logger.debug(f"start process message: {message}")

    async with AsyncSessionLocal() as session:
        db_parent_message: models.Message | None = None
        if message.reply_to_message:
            db_parent_message = await get_parent_message(
                session=session,
                original_parent_id=message.reply_to_message.message_id,
            )

        db_message: models.Message = await create_obj(
            session=session,
            model=models.Message,
            original_id=message.message_id,
            original_parent_id=(
                message.reply_to_message.message_id if message.reply_to_message else None
            ),
            parent_id=(db_parent_message.id if db_parent_message else None),
            user_id=message.from_user and message.from_user.id,
            user_name=(user_name(message.from_user) if message.from_user else ""),
            text=message.text,
        )
        logger.debug(f"message with id {db_message.id} added.")

    # TODO try | catch
    async with httpx.AsyncClient() as client:
        _ = await client.post(
            url="http://localhost:8000/message",
            json=message.model_copy(
                update={
                    "db_id": db_message.id,
                },
            ).model_dump_json(),
        )


async def on_startup(bot: Bot) -> None:
    asyncio.create_task(rabbit_loop(bot))  # no await. It's right!


async def bot_loop(token: str) -> None:
    bot = Bot(
        token=token,
        parse_mode=ParseMode.HTML,
    )
    logger.info("Bot loop starting ...")
    dp.startup.register(on_startup)
    await dp.start_polling(bot)
    logger.info("Bot loop finished.")
