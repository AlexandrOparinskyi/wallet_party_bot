from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filters import SurveySlugFilter
from bot.utils import (get_wallets_for_chat,
                       add_wallet_for_chat,
                       delete_wallet_for_chat,
                       add_transaction_for_wallet,
                       get_wallet_for_name)

wallet_router = Router()


@wallet_router.message(Command("дай"))
async def get_wallets(message: Message):
    wallets = await get_wallets_for_chat(message.chat.id)

    if not wallets:
        await message.answer("В этом чате кошельков не найдено")
        return

    if message.chat.title:
        text = f"Кошельки <b>{message.chat.title}:</b>\n"
    else:
        text = "<b>Ваши кошельки:</b>\n"

    for num, wallet in enumerate(wallets, 1):
        text += f"<b>{num}</b> <code>{wallet.name}</code> - <code>{wallet.get_total}</code>\n"

    await message.answer(text)


@wallet_router.message(Command("добавь"),)
async def add_wallet(message: Message):
    wallet_name = message.text.split(" ")[1:len(message.text.split(" "))]

    flag = await add_wallet_for_chat(" ".join(wallet_name),
                                     message.chat.id)
    if not flag:
        await message.answer("Кошелек с таким именем уже существует")
        return

    await message.answer(f"Кошелек <i>{' '.join(wallet_name)}</i> добавлен")


@wallet_router.message(Command("удали"))
async def delete_wallet(message: Message):
    wallet_name = message.text.split(" ")[1:len(message.text.split(" "))]

    flag = await delete_wallet_for_chat(" ".join(wallet_name),
                                        message.chat.id)

    if not flag:
        await message.answer("Кошелек с таким именем не существует")
        return

    await message.answer(f"Кошелек <i>{' '.join(wallet_name)}</i> удален")


@wallet_router.message(SurveySlugFilter())
async def add_transaction(message: Message):
    wallet_name, amount = message.text.split(" ")
    wallet_name = wallet_name.replace("/", "")
    amount = amount.replace(",", ".")
    await add_transaction_for_wallet(wallet_name,
                                     message.chat.id,
                                     amount)
    wallet = await get_wallet_for_name(message.chat.id, wallet_name)

    if int(amount) > 0:
        t = "+"
    else:
        t =""

    await message.answer(f"Запомнил: {t}{amount}\n"
                         f"Баланс <b>{wallet_name}</b>: {wallet.get_total}")
