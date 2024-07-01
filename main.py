import asyncio
import aiocron
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from data.load_data import TOKEN, PORT_NGROK, WEBHOOK_URL, HOUR, MINUTE
from handlers.private_chat import private_chat_router
from callbacks.callbacks import callback_router, backup

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher()

CRON: str = f'{MINUTE} {HOUR} * * *'

dp.include_routers(
    private_chat_router,
    callback_router
)


async def schedule_task():
    await backup()

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await bot.delete_my_commands()
    aiocron.crontab(CRON, func=schedule_task)

async def on_shutdown(app):
    await bot.delete_webhook(drop_pending_updates=True)

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]
    if token == TOKEN:
        data = await request.json()
        update = types.Update(**data)
        await dp._process_update(bot, update)
        return web.Response()
    else:
        return web.Response(status=403)

app = web.Application()
app.router.add_post(f'/{TOKEN}', handle_webhook)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app=app, host='0.0.0.0', port=PORT_NGROK)
