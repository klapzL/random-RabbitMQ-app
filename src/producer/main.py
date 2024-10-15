import os

import aio_pika
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = "message_queue"


async def send_message_to_rabbitmq(message: str):
    connection = await aio_pika.connect_robust(RABBITMQ_HOST)
    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=QUEUE_NAME,
        )
        print(f"Sent message: {message}")


@app.post("/send/")
async def send_message(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(send_message_to_rabbitmq, message)
    return {"status": "Message sent"}
