import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from .handlers import register_handlers

logger = logging.getLogger(__name__)


async def main(
        token: str,
        storage: RedisStorage | MemoryStorage = MemoryStorage()
) -> None:
    bot: Bot = Bot(token=token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher(storage=storage)

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot don`t started: {e}")
