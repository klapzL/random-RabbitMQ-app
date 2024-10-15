import asyncio
import logging
import os

import aio_pika
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = "message_queue"


async def consume_message():
    connection = await aio_pika.connect_robust(RABBITMQ_HOST)
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(QUEUE_NAME)

        logger.info("Queue declared: %s", QUEUE_NAME)

        logger.info("Waiting for messages...")

        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                logger.info("Received message: %s", message.body.decode())

        await queue.consume(callback)

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled.")


async def lifespan(app: FastAPI):
    consumer = asyncio.create_task(consume_message())
    logger.info("Consumer task started.")

    yield

    consumer.cancel()
    await consumer


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"status": "Consumer is running"}
