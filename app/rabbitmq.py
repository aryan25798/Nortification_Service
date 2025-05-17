import asyncio
import aio_pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def publish_notification(data: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("notifications", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(data).encode()),
            routing_key=queue.name
        )
