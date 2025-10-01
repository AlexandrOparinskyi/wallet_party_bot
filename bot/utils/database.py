import logging
from typing import List, Optional

from sqlalchemy import select, insert

from database import Wallet, get_async_session, Transaction

logger = logging.getLogger(__name__)


async def get_wallets_for_chat(chat_id: int) -> Optional[List[Wallet]]:
    async with get_async_session() as session:
        query = await session.execute(select(Wallet).where(
            Wallet.chat_id == chat_id
        ))
        return query.scalars().all()


async def get_wallet_for_name(chat_id: int,
                              w_name: str) -> Wallet:
    async with get_async_session() as session:
        return await session.scalar(select(Wallet).where(
            Wallet.name == w_name,
            Wallet.chat_id == chat_id
        ))


async def add_wallet_for_chat(name: str, chat_id: int) -> bool:
    async with get_async_session() as session:
        try:
            await session.execute(insert(Wallet).values(
                name=name,
                chat_id=chat_id
            ))
            await session.commit()
            return True
        except:
            return False


async def delete_wallet_for_chat(name: str, chat_id: int) -> bool:
    async with get_async_session() as session:
        query = await session.execute(select(Wallet).where(
            Wallet.name == name,
            Wallet.chat_id == chat_id
        ))
        wallet = query.scalar_one_or_none()

        if not wallet:
            return False

        await session.delete(wallet)
        await session.commit()
        return True


async def add_transaction_for_wallet(wallet_name: str,
                                     chat_id: int,
                                     amount: str) -> None:
    async with get_async_session() as session:
        wallet = await session.scalar(select(Wallet).where(
            Wallet.name == wallet_name,
            Wallet.chat_id == chat_id
        ))

        await session.execute(insert(Transaction).values(
            wallet_id=wallet.id,
            amount=float(amount)
        ))
        await session.commit()
