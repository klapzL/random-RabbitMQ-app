from asyncio import AbstractEventLoop

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from src.config import settings


async def get_connection(loop: AbstractEventLoop = None) -> AbstractRobustConnection:
    return await connect_robust(url=settings.RMQ_URL, loop=loop)
