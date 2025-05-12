from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import CommandStart

from handlers.product_list import send_product_types

router = Router()
products = {'Жидкости': [], 'Одноразки': []}


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    await send_product_types(message.chat.id, bot)
    await message.delete()

