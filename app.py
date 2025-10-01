import asyncio
import logging

from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import Config, load_config
from bot import bot

logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
               '%(lineno)d - %(name)s - %(message)s'
    )
logger = logging.getLogger(__name__)


async def app() -> None:
    config: Config = load_config()

    redis_client = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        decode_responses=False
    )
    storage = RedisStorage(
        redis_client,
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    await asyncio.gather(bot(config.tg_bot.token))


if __name__ == "__main__":
    asyncio.run(app())
