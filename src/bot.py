import asyncio
import logging
import sys

from bot import bot_loop
from settings import settings

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Bot start")
    asyncio.run(bot_loop(settings.TG_BOT_TOKEN))
    logger.info("Bot finished")
