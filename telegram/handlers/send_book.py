import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram import markups, aux_funcs
from database.controllers import books_controller
from config.bot_config import EPUB_FOLDER
import vars_global


class SendingState(StatesGroup):
    wait_send_text = State()
    wait_next_part = State()
    wait_prev_part = State()


class SetPost:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""

        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)

        return inner

    @staticmethod
    async def add_book(call: types.CallbackQuery, state: FSMContext):
        """Add post content"""
        await state.finish()
        await call.message.answer("👉 Отправь мне книгу в формате ePub")
        await state.set_state(SendingState.wait_send_text.state)

    @staticmethod
    async def add_book_command(message: types.Message, state: FSMContext):
        """Add post content"""
        await state.finish()
        await message.answer("👉 Отправь мне книгу в формате ePub")
        await state.set_state(SendingState.wait_send_text.state)

    async def get_book_text(self, message: types.Message, state: FSMContext):
        if '.epub' not in message.document.file_name:
            await message.answer("⚠ Проверь формат. Файл должен быть в формате ePub")
            return
        filepath = f'{EPUB_FOLDER}{message.document.file_name}'
        await self.bot.download_file_by_id(message.document.file_id, filepath)
        aux_funcs.write_book_to_db(message.chat.id, filepath)
        books_part_text = aux_funcs.init_first_book(message.chat.id, filepath)
        vars_global.update_schedule = [True, message.chat.id]
        if books_part_text.get('new_book'):
            await message.answer("👌 Отлично. Держи свою первую страницу.\n"
                                 "Если захочешь начать другую книгу, введи комманду /select")
            keyboard = markups.get_next_part_button()
        else:
            await message.answer("👌 Отлично. Книга уже была добавлена ранее. Продолжаем чтение...\n"
                                 "Если захочешь начать другую книгу, введи комманду /select")
            keyboard = markups.get_nav_menu()
        await message.answer(books_part_text.get('books_part_text'), reply_markup=keyboard)
        await state.finish()

    @staticmethod
    async def get_books_next_part(call: types.CallbackQuery):
        # не удовлетворяет dry
        user_data = books_controller.db_read_users_data()
        book_filename = ''
        for user in user_data:
            if user.telegram_id != call.message.chat.id:
                continue
            book_filename = user.current_book
            break

        # переделать. Нужно вначале в Progress записать данные по количеству частей
        progress = books_controller.db_read_user_progress(call.message.chat.id, book_filename)
        book_data = books_controller.db_read_book_data(book_filename)
        if progress.last_part_numb == len(book_data):
            await call.message.edit_text('🥳 Поздравляем! Ты успешно закончил чтение книги.\n'
                                         'Если захочешь начать другую книгу, введи комманду /select')
            return

        next_page = progress.last_part_numb + 1
        books_part_text = books_controller.db_read_books_part_text(progress.book_name, next_page)
        progress.last_part_numb = next_page
        progress.read_timestamp = str(datetime.datetime.now())
        progress.shedule_read_timestamp = str(datetime.datetime.now() + datetime.timedelta(days=1))
        books_controller.db_update_progress_table(progress)
        vars_global.update_schedule = [True, call.message.chat.id]
        keyboard = markups.get_nav_menu()
        await call.message.edit_text(books_part_text, reply_markup=keyboard)

    @staticmethod
    async def get_books_prev_part(call: types.CallbackQuery):
        # не удовлетворяет dry
        user_data = books_controller.db_read_users_data()
        book_filename = ''
        for user in user_data:
            if user.telegram_id != call.message.chat.id:
                continue
            book_filename = user.current_book
            break

        progress = books_controller.db_read_user_progress(call.message.chat.id, book_filename)
        prev_page = progress.last_part_numb - 1
        books_part_text = books_controller.db_read_books_part_text(progress.book_name, prev_page)
        progress.last_part_numb = prev_page
        progress.read_timestamp = str(datetime.datetime.now())
        progress.shedule_read_timestamp = str(datetime.datetime.now() + datetime.timedelta(days=1))
        books_controller.db_update_progress_table(progress)
        vars_global.update_schedule = [True, call.message.chat.id]
        keyboard = markups.get_nav_menu()
        if prev_page == 1:
            keyboard = markups.get_next_part_button()
        await call.message.edit_text(books_part_text, reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_callback_query_handler(self.add_book, text='start_app',
                                           state='*')
        dp.register_message_handler(self.add_book_command, commands="select",
                                    state='*')
        dp.register_message_handler(self.get_book_text, content_types='document',
                                    state=SendingState.wait_send_text)
        dp.register_callback_query_handler(self.get_books_next_part, text='next_part',
                                           state='*')
        dp.register_callback_query_handler(self.get_books_prev_part, text='prev_part',
                                           state='*')
