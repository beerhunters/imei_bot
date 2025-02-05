# bot.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.config import settings
from app.imei_checker import check_imei_api, format_imei_response
from app.rq import is_user_allowed
from app.utils import validate_imei

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    if not await is_user_allowed(message.from_user.id):
        await message.answer("У вас нет доступа к этому боту.")
        return
    await message.answer("Отправьте IMEI для проверки.")


@dp.message()
async def imei_handler(message: Message):
    if not await is_user_allowed(message.from_user.id):
        await message.answer("У вас нет доступа к этому боту.")
        return

    imei = message.text.strip()
    if not validate_imei(imei):
        await message.answer("Некорректный IMEI. Введите 15-значный номер.")
        return

    response = await check_imei_api(imei)
    result = await format_imei_response(response)
    await message.answer(result, parse_mode="HTML")


async def start_bot():
    await dp.start_polling(bot)
