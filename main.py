import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from data_base.base_models import async_main
from app.hundlers import router


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print("Бот запущен")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')