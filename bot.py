import asyncio
from telegram import webhooks
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import uvicorn

from config.bot_config import TOKEN, ACCESS_ID_LIST
from telegram.handlers import common
from telegram.handlers import send_book
from telegram.auth import AccessMiddleware


class BotInit:
    """Bot initialization"""

    def __init__(self):
        self.bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.dp.middleware.setup(AccessMiddleware(ACCESS_ID_LIST))


def set_logging():
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())


async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="рестарт бота")
    ]
    await bot.set_my_commands(bot_commands)


def init_handlers():
    common.register_handlers(dp)
    user_handler = send_book.SetPost(bot)
    user_handler.register_handlers(dp)


async def main():
    set_logging()
    await setup_bot_commands()
    init_handlers()


if __name__ == '__main__':
    bot_init = BotInit()
    dp = bot_init.dp
    bot = bot_init.bot
    asyncio.run(main())
    app = FastAPI()
    webhooks.init_api(bot, dp, app)
    uvicorn.run(app, host='127.0.0.1', port=5010)
