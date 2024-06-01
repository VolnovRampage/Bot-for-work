import os
import asyncio

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types

load_dotenv(find_dotenv())

from handlers.privat_chat import private_chat_router
from callbacks.callbacks import callback_router


TOKEN: str = os.getenv("TOKEN")


bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()

dp.include_routers(
    private_chat_router,
    callback_router
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
