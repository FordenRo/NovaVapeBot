from asyncio import run

from aiogram import Bot, Dispatcher

from handlers import start, product_list


async def main():
    dispatcher = Dispatcher()
    bot = Bot('7902060019:AAFsQvBlf9LD4EPVa2FLsuErnQIqRcAljOw')

    dispatcher.include_routers(start.router,
                               product_list.router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    run(main())

