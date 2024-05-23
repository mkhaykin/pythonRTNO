import aio_pika

from src.msg import MsgOut
from src.settings import settings


async def on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)

    print("Before sleep!")
    # await asyncio.sleep(5)  # Represents async I/O operations
    print("After sleep!")


async def pop_message() -> None:
    # Perform connection
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_SERVER,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_DEFAULT_USER,
        password=settings.RABBITMQ_DEFAULT_PASS,
        virtualhost=settings.RABBITMQ_DEFAULT_VHOST,
    )
    queue_name = "messages"
    # Will take no more than 10 messages in advance
    # await channel.set_qos(prefetch_count=10)

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(queue_name)

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=True)


async def push_message(msg: MsgOut) -> None:

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

        # Sending the message
        await channel.default_exchange.publish(
            aio_pika.Message(msg.model_dump_json().encode("utf-8")),
            routing_key=queue.name,
        )

        print(f" [x] Sent '{msg}'")

    print("End push")
