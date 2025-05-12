from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()
products = {
    'liquids': {
        'text': 'Жидкости',
        'brands': [
            {
                'text': 'HOTSPOT',
                'products': [
                    'Малиновый куни',
                    'Банановая сперма'
                ]
            }
        ]
    },
    'h': {
        'text': 'Одноразки'
    }
}


async def send_product_types(chat_id: int, bot: Bot, message: Message = None):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=products[i]['text'], callback_data=f'type/{i}')]
        for i in products])
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
    brands = products[product_type]['brands']
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=v['text'], callback_data=f'brand/{product_type}/{i}')]
        for i, v in enumerate(brands)]
            + [[InlineKeyboardButton(text='Назад', callback_data='types')]])

    await callback.message.edit_text('Выбери марку товара', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.split('/')[0] == 'brand')
async def brand_query(callback: CallbackQuery, bot: Bot):
    _, product_type, brand = callback.data.split('/')
    print(product_type, brand)
    product_list = products[product_type]['brands'][brand]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=v, callback_data=f'product/{product_type}/{brand}/{i}')]
        for i, v in enumerate(product_list)])

    await callback.message.edit_text('Выбери товар', reply_markup=markup)
    await callback.answer()

