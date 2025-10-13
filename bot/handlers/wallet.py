import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.filters import SurveySlugFilter
from bot.utils import (get_wallets_for_chat,
                       add_wallet_for_chat,
                       delete_wallet_for_chat,
                       add_transaction_for_wallet,
                       get_wallet_for_name, delete_transaction_by_id)

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


@wallet_router.message(Command("добавь"))
async def add_wallet(message: Message):
    wallet_name = message.text.split(" ")[1]

    flag = await add_wallet_for_chat(" ".join(wallet_name),
                                     message.chat.id)
    if not flag:
        await message.answer("Кошелек с таким именем уже существует")
        return

    await message.answer(f"Кошелек <i>{' '.join(wallet_name)}</i> добавлен")


@wallet_router.message(Command("удали"))
async def delete_wallet(message: Message):
    wallet_name = message.text.split(" ")[1]

    flag = await delete_wallet_for_chat(" ".join(wallet_name),
                                        message.chat.id)

    if not flag:
        await message.answer("Кошелек с таким именем не существует")
        return

    await message.answer(f"Кошелек <i>{' '.join(wallet_name)}</i> удален")


@wallet_router.message(SurveySlugFilter())
async def add_transaction(message: Message):
    try:
        parts = message.text.split(" ")
        if len(parts) < 2:
            await message.answer("❌ Формат: /имя_кошелька сумма")
            return

        wallet_name = parts[0].replace("/", "")
        expression = parts[1].replace(",", ".")

        # Безопасная обработка выражения
        amount = await safe_evaluate_expression(expression)

        transaction_id = await add_transaction_for_wallet(wallet_name,
                                                          message.chat.id,
                                                          amount)
        wallet = await get_wallet_for_name(message.chat.id, wallet_name)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Откатить",
                    callback_data=f"back_{transaction_id}"
                )]
            ]
        )

        # Форматирование вывода
        sign = "+" if amount > 0 else ""
        await message.answer(f"Запомнил: {sign}{amount}\n"
                             f"Баланс <b>{wallet_name}</b>: {wallet.get_total}",
                             reply_markup=keyboard)

    except ValueError as e:
        await message.answer(f"❌ Ошибка в выражении: {e}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def safe_evaluate_expression(expression: str) -> float:
    """Безопасное вычисление математического выражения"""
    # Удаляем все пробелы
    expression = expression.replace(" ", "")

    # Проверяем, что выражение содержит только разрешённые символы
    if not re.match(r'^[0-9+\-*/().]+$', expression):
        raise ValueError("Недопустимые символы в выражении")

    # Проверяем сбалансированность скобок
    if expression.count('(') != expression.count(')'):
        raise ValueError("Несбалансированные скобки")

    try:
        # Вычисляем выражение
        result = eval(expression, {"__builtins__": {}}, {})

        # Проверяем, что результат - число
        if not isinstance(result, (int, float)):
            raise ValueError("Результат не является числом")

        return float(result)

    except ZeroDivisionError:
        raise ValueError("Деление на ноль")
    except Exception as e:
        raise ValueError(f"Некорректное выражение")


@wallet_router.callback_query(F.data.startswith("back_"))
async def back_transaction(callback: CallbackQuery):
    await callback.message.delete()

    trans_id = callback.data.split("_")[1]
    await delete_transaction_by_id(int(trans_id))

    await callback.answer("Транзакция удалена")
