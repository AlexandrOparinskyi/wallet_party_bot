from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select

from database import get_async_session, Wallet


class SurveySlugFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        try:
            if len(message.text.split(" ")) != 2:
                return False

            async with get_async_session() as session:
                wallets = await session.scalars(select(Wallet).where(
                    Wallet.chat_id == message.chat.id
                ))

                wallet = message.text.split(" ")[0].replace("/", "")

                return wallet in [w.name for w in wallets]
        except:
            return False
