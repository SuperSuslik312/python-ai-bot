import asyncio

from aiogram import (
    Bot,
    Dispatcher
)
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers import (
    admin,
    user
)
from postgresql import start_db


async def main():
    bot = Bot(Config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(admin.router, user.router)
    await start_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Bot polling
if __name__ == '__main__':
    asyncio.run(main())
