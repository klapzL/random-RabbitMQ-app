import aio_pika
from fastapi import BackgroundTasks, FastAPI

from src.config.rmq import get_connection, settings

app = FastAPI()


async def send_message_to_rabbitmq(message: str):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=settings.RMQ_QUEUE,
        )
        print(f"Sent message: {message}")


@app.post("/send/")
async def send_message(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(send_message_to_rabbitmq, message)
    return {"status": "Message sent"}
