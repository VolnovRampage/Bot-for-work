import os
import asyncio

from aiohttp import web
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types

load_dotenv(find_dotenv())

from handlers.privat_chat import private_chat_router
from callbacks.callbacks import callback_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from callbacks.callbacks import backup


TOKEN: str = os.getenv("TOKEN")
NGROK: str  = os.getenv("NGROK")
WEBHOOK_URL: str = f'{NGROK}/{TOKEN}'
PORT_NGROK: int = int(os.getenv('PORT_NGROK'))
HOUR: int = int(os.getenv('HOUR'))
MINUTE: int = int(os.getenv('MINUTE'))


bot: Bot = Bot(token=TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()

dp.include_routers(
    private_chat_router,
    callback_router
)


async def schedule_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(backup, CronTrigger(hour=HOUR, minute=MINUTE))
    scheduler.start()
    try:
        await asyncio.sleep(86400)
    except asyncio.CancelledError as err:
        print(err)
    finally:
        scheduler.shutdown()


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await bot.delete_my_commands()
    asyncio.create_task(schedule_task())

async def on_shutdown(app):
    await bot.delete_webhook(drop_pending_updates=True)


async def handle_webhook(request):
    url: str = str(request.url)
    index: int = url.rfind('/')
    token: str = url[index + 1:]
    if token == TOKEN:
        data = await request.json()
        update = types.Update(**data)
        await dp._process_update(bot,update)
        return web.Response()
    else:
        return web.Response(status=403)


app = web.Application()
app.router.add_post(f'/{TOKEN}', handle_webhook)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app=app, host='0.0.0.0', port=PORT_NGROK)
