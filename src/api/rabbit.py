import json

import aio_pika

from src.schemas import MsgForward, MsgOut
from src.settings import settings


async def push_message(msg: MsgOut | MsgForward, msg_type: str) -> None:
    connection = await aio_pika.connect(
        host=settings.RABBITMQ_SERVER,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_DEFAULT_USER,
        password=settings.RABBITMQ_DEFAULT_PASS,
        virtualhost=settings.RABBITMQ_DEFAULT_VHOST,
    )

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("messages")

        data = {
            "type": msg_type,
            "message": msg.model_dump(),
        }

        # Sending the message
        await channel.default_exchange.publish(
            aio_pika.Message(json.dumps(data).encode("utf-8")),
            routing_key=queue.name,
        )

        print(f" [x] Sent '{msg}'")

    print("End push")


async def push_message_to_send(msg: MsgOut) -> None:
    await push_message(msg, "out")


async def push_message_to_forward(msg: MsgForward) -> None:
    await push_message(msg, "forward")
