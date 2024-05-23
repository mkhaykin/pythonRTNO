import asyncio
import logging

import httpx
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.msg import MsgIn

from .rabbit import rabbit_loop

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
async def base_handler(message: MsgIn) -> None:
    """
    Handler will forward receive a message back to the sender
    """
    # TODO try | catch
    async with httpx.AsyncClient() as client:
        _ = await client.post(
            url="http://localhost:8000/ask",
            json=message.model_dump_json(),
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
