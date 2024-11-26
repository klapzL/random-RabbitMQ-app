import asyncio
import logging

from aio_pika import IncomingMessage
from fastapi import FastAPI

from src.config import get_connection, settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume_message():
    async with await get_connection() as connection:
        channel = await connection.channel()
        channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(settings.RMQ_QUEUE)

        logger.info("Queue declared: %s", settings.RMQ_QUEUE)

        async def callback(message: IncomingMessage):
            async with message.process():
                logger.info("Received message: %s", message.body.decode())

        await queue.consume(callback)

        logger.info("Waiting for messages...")

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Consumer cancelled.")


async def lifespan(app: FastAPI):
    consumer = asyncio.run_coroutine_threadsafe(
        consume_message(), asyncio.get_running_loop()
    )
    logger.info("Consumer started.")

    yield

    consumer.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"status": "Consumer is running"}
