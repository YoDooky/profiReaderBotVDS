from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hbold

from telegram import markups, aux_funcs
from database.controllers import books_controller
from config.bot_config import EPUB_FOLDER


class SendingState(StatesGroup):
    wait_send_text = State()
    wait_next_part = State()
    # wait_schedule_time = State()
    # wait_schedule_approve_finish = State()
    # wait_schedule_set_finish = State()


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

    async def send_book_text(self, message: types.Message, state: FSMContext):
        if '.epub' not in message.document.file_name:
            await message.answer("⚠ Проверь формат. Файл должен быть в формате ePub")
            return
        filepath = f'{EPUB_FOLDER}{message.document.file_name}'
        user_id = message.from_user.id
        await self.bot.download_file_by_id(message.document.file_id, filepath)
        aux_funcs.write_book_to_db(user_id, filepath)
        # books_controller.db_write_progress()  Прогресс доделай
        await message.answer("👌 Отлично. Держи свою первую страницу. "
                             "Если захочешь начать другую книгу, введи комманду /start")
        book_name = aux_funcs.get_book_name(filepath)
        books_part_text = books_controller.db_read_books_part_text(book_name, 'part_text', 1)
        keyboard = markups.get_next_part_button()
        await message.answer(books_part_text, reply_markup=keyboard)
        await state.set_state()

    async def get_books_next_part(self, call: types.CallbackQuery, state: FSMContext):
        pass

    # @staticmethod
    # async def set_post_schedule_period(message: types.Message, state: FSMContext):
    #     """Set period of autoreposting"""
    #     try:
    #         photo_id = message.photo[-1].file_id
    #     except Exception as ex:
    #         photo_id = None
    #         pass
    #     post_text = message.text if not message.caption else message.caption
    #     if not post_text:
    #         await message.answer("⚠ Текст поста не должен быть пустым. Если во вложении изображение, "
    #                              "пожалуйста укажи в подписи к нему текст поста")
    #         return
    #     await state.update_data(post_photo_id=photo_id, post_text=post_text)
    #     keyboard = markups.get_shedule_period_buttons()
    #     await message.answer(text='👉 Выбери периодичность авторепостинга',
    #                          reply_markup=keyboard)
    #     await state.set_state(SendingState.wait_schedule_time.state)
    #
    # @staticmethod
    # async def set_post_shedule_time(call: types.CallbackQuery, state: FSMContext):
    #     """Set post schedule time"""
    #     schedule_period = call.data.split('schedule_period_')[1]
    #     await state.update_data(schedule_period=schedule_period)
    #     await call.message.edit_text("👉 Введи время поста в формате hh:mm (например: 9:00")
    #     await state.set_state(SendingState.wait_schedule_approve_finish.state)
    #
    # @staticmethod
    # async def confirm_post_schedule(message: types.Message, state: FSMContext):
    #     """Finish set schedule time"""
    #     if not aux_funcs.check_time_format(message.text):
    #         await message.answer(
    #             "⚠ Неверный формат времени для автопостинга. Введи время формате hh:mm (например: 9:00")
    #         return
    #     await state.update_data(schedule_time=message.text)
    #     user_data = await state.get_data()
    #     keyboard = markups.get_confirmation_menu('set_approve', 'set_cancel')
    #     if user_data.get('post_photo_id'):
    #         await message.answer_photo(
    #             photo=user_data.get('post_photo_id'),
    #             caption=f"🏞 изображение 👆\n"
    #                     f"📝 текст: {user_data.get('post_text')}\n"
    #                     f"⏳ периодичность: {user_data.get('schedule_period')}\n"
    #                     f"🕔 время: {user_data.get('schedule_time')}",
    #             reply_markup=keyboard
    #         )
    #     else:
    #         await message.answer(
    #             text=f"📝 текст: {user_data.get('post_text')}\n"
    #                  f"⏳ периодичность: {user_data.get('schedule_period')}\n"
    #                  f"🕔 время: {user_data.get('schedule_time')}",
    #             reply_markup=keyboard
    #         )
    #     await state.set_state(SendingState.wait_schedule_set_finish.state)
    #
    # @staticmethod
    # async def set_post_schedule(call: types.CallbackQuery, state: FSMContext):
    #     user_data = await state.get_data()
    #     post_controller.db_write_data(user_data)
    #     await call.message.answer('👌 Пост успешно добавлен в расписание. /setpost чтобы добавить еще')
    #     await state.finish()

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_callback_query_handler(self.add_book, text='start_app',
                                           state='*')
        dp.register_message_handler(self.send_book_text, content_types='document',
                                    state=SendingState.wait_send_text)
        dp.register_callback_query_handler(self.get_books_next_part, text='next_part',
                                           state=SendingState.wait_next_part)
        # dp.register_callback_query_handler(self.edit_post_content, text='set_cancel', state='*')
        # dp.register_message_handler(self.set_post_schedule_period, content_types=['photo', 'text'],
        #                             state=SendingState.wait_schedule_period)
        # dp.register_callback_query_handler(self.set_post_shedule_time, Text(contains='schedule_period_'),
        #                                    state=SendingState.wait_schedule_time)
        # dp.register_message_handler(self.confirm_post_schedule, content_types='text',
        #                             state=SendingState.wait_schedule_approve_finish)
        # dp.register_callback_query_handler(self.set_post_schedule, text='set_approve',
        #                                    state=SendingState.wait_schedule_set_finish)
