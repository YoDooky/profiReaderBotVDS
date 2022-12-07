from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram import markups, aux_funcs
from database.controllers import books_controller


class PostState(StatesGroup):
    wait_del_post_approve = State()
    wait_del_post_finish = State()


class DelPost:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""

        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)

        return inner

    @staticmethod
    async def del_post_schedule(message: types.Message, state: FSMContext):
        """Show post for deleting"""
        await state.finish()
        keyboard = markups.get_post_buttons()
        await message.answer('👉 Выбери пост для удаления из расписания', reply_markup=keyboard)
        await state.set_state(PostState.wait_del_post_approve.state)

    @staticmethod
    async def del_post_schedule_edit(call: types.CallbackQuery, state: FSMContext):
        """Edit post for deleting (same as del_post_schedule but on callback)"""
        await state.finish()
        keyboard = markups.get_post_buttons()
        await call.message.answer('👉 Выбери пост для удаления из расписания', reply_markup=keyboard)
        await state.set_state(PostState.wait_del_post_approve.state)

    @staticmethod
    async def del_post_schedule_approve(call: types.CallbackQuery, state: FSMContext):
        """Approve post deleting from schedule"""
        choosen_post_id = call.data.split('post_id_')[1]
        await state.update_data(post_id=choosen_post_id)
        keyboard = markups.get_confirmation_menu('del_approve', 'del_cancel')
        await call.message.answer('😱 Действительно хочешь удалить выбранный пост из расписания?',
                                  reply_markup=keyboard)
        await state.set_state(PostState.wait_del_post_finish.state)

    @staticmethod
    async def del_post_schedule_finish(call: types.CallbackQuery, state: FSMContext):
        """Finish deleting post from schedule"""
        user_data = await state.get_data()
        books_controller.db_del_post_data(user_data.get('post_id'))
        await call.message.answer('👌 Выбранный пост успешно удален из расписания. /delpost чтобы удалить еще')
        await state.finish()

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_message_handler(self.del_post_schedule, commands='deletepost',
                                    state='*')
        dp.register_callback_query_handler(self.del_post_schedule_edit, text='del_cancel',
                                           state='*')
        dp.register_callback_query_handler(self.del_post_schedule_approve, Text(contains='post_id_'),
                                           state=PostState.wait_del_post_approve)
        dp.register_callback_query_handler(self.del_post_schedule_finish, text='del_approve',
                                           state=PostState.wait_del_post_finish)
