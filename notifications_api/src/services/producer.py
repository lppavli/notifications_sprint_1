import json
import aio_pika

from src.config.config import settings


async def send_msg(notice) -> None:
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("welcome-email", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(notice).encode()),
            routing_key=queue.name,
        )
