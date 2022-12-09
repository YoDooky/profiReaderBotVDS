from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram import markups, aux_funcs
from database.controllers import books_controller
from config.bot_config import ADD_BOOK_MSG, BOOK_FORMAT_ERR_MSG, FIRST_BOOK_MSG, SAME_BOOK_MSG, REEDING_COMPLETE_MSG
from config.bot_config import EPUB_FOLDER
import vars_global


class EditState(StatesGroup):
    wait_edit_text = State()


class AdminPanel:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def edit_bot_messages(call: types.CallbackQuery, state: FSMContext):
        """Add post content"""
        await state.finish()
        keyboard = markups.get_bot_messages_menu()
        await call.message.answer('Выбери текст для редактирования', reply_markup=keyboard)

    @staticmethod
    async def edit_greeting_msg(call: types.CallbackQuery, state: FSMContext):
        await call.message.answer('Введи новый текст сообщения:')
        state.update_data(target_msg=call.data)
        await state.set_state(EditState.wait_edit_text.state)

    @staticmethod
    async def accept_edit_text(message: types.Message, state: FSMContext):


    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_callback_query_handler(self.edit_bot_messages, text='edit_bot_messages', state='*')
        dp.register_callback_query_handler(self.edit_greeting_msg, text='GREETING_MSG', state='*')
        # dp.register_callback_query_handler(self.edit_book_add_msg, text='ADD_BOOK_MSG')
        # dp.register_callback_query_handler(self.edit_book_format_err_msg, text='BOOK_FORMAT_ERR_MSG')
        # dp.register_callback_query_handler(self.edit_first_book_msg, text='FIRST_BOOK_MSG')
        # dp.register_callback_query_handler(self.edit_same_book_msg, text='SAME_BOOK_MSG')
        # dp.register_callback_query_handler(self.edit_reeding_complete_msg, text='REEDING_COMPLETE_MSG')
        dp.register_message_handler(self.accept_edit_text, content_types='text', state=EditState.wait_edit_text)
