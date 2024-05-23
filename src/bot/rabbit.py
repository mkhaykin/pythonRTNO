import json

import aio_pika
from aiogram import Bot

from src.msg import MsgOut
from src.settings import settings


async def rabbit_loop(bot: Bot) -> None:
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
                    data: dict = json.loads(queue_message.body.decode())
                    message = MsgOut(**data)
                    await bot.send_message(**message.__dict__)
