from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from telegram import markups
from database.controllers import books_controller
from app_types import User
import datetime


async def start_command(message: types.Message, state: FSMContext):
    if message.chat.type != 'private':  # start only in private messages
        return
    user_object = User(telegram_id=message.from_user.id,
                       privilege='user',
                       registration_timestamp=str(datetime.datetime.now()))
    books_controller.db_write_users(user_object)
    await state.finish()
    keyboard = markups.get_start_menu()
    await message.answer(
        "👋Добро пожаловать в бот для чтения книг !\n"
        "Нажми на кнопку 'Начать работу с ботом' для продолжения", reply_markup=keyboard
    )


def register_handlers(dp: Dispatcher):
    """Register message handlers"""
    dp.register_message_handler(start_command, commands="start", state='*')
