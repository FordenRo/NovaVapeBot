from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from product import Product, ProductType, filter_by_brand, filter_by_type, get_brands

router = Router()
products = [Product(ProductType.LIQUID, 'HOTSPOT', 'Малиноввй куни', 400)]

product_type_names = {ProductType.LIQUID: 'Жидкости'}

async def send_product_types(chat_id: int, bot: Bot, message: Message | None = None):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=product_type_names[i], callback_data=f'type/{i}')]
        for i in ProductType])
    text = 'Привет!\nВыбери тип товара'

    if message:
        await message.edit_text(text, reply_markup=markup)
    else:
        await bot.send_message(chat_id, text, reply_markup=markup)


@router.callback_query(F.data == 'types')
async def product_types_query(callback: CallbackQuery, bot: Bot):
    await send_product_types(callback.from_user.id, bot, callback.message)
    await callback.answer()


@router.callback_query(F.data.split('/')[0] == 'type')
async def product_type_query(callback: CallbackQuery, bot: Bot):
    product_type = callback.data.split('/')[1]
    brands = get_brands(products)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i, callback_data=f'brand/{product_type}/{i}')]
        for i in brands]
            + [[InlineKeyboardButton(text='Назад', callback_data='types')]])

    await callback.message.edit_text('Выбери марку товара', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.split('/')[0] == 'brand')
async def brand_query(callback: CallbackQuery, bot: Bot):
    _, product_type, brand = callback.data.split('/')
    print(product_type, brand)
    product_list = filter_by_brand(filter_by_type(products, product_type), brand)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i.name, callback_data=f'product/{product_type}/{i.name}')]
        for i in enumerate(product_list)])

    await callback.message.edit_text('Выбери товар', reply_markup=markup)
    await callback.answer()

