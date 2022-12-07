from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram import markups
from config.bot_config import TARGET_CHANNEL_ID


class PostState(StatesGroup):
    wait_send_post_approve = State()
    wait_send_post_finish = State()


class SendPost:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""

        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)

        return inner

    @staticmethod
    async def add_post_content(message: types.Message, state: FSMContext):
        """Add post content"""
        await state.finish()
        await message.answer("👉 Напиши текст поста. Если пост с изображением, текст должен быть в подписи")
        await state.set_state(PostState.wait_send_post_approve.state)

    @staticmethod
    async def edit_post_content(call: types.CallbackQuery, state: FSMContext):
        """Edit post content (same as add_post_content but made on callbacks)"""
        await state.finish()
        await call.message.answer("👉 Напиши текст поста. Если пост с изображением, текст должен быть в подписи")
        await state.set_state(PostState.wait_send_post_approve.state)

    @staticmethod
    async def approve_post_sending(message: types.Message, state: FSMContext):
        """Finish set schedule time"""
        try:
            photo_id = message.photo[-1].file_id
        except Exception as ex:
            photo_id = None
            pass
        post_text = message.text if not message.caption else message.caption
        if not post_text:
            await message.answer("⚠ Текст поста не должен быть пустым. Если во вложении изображение, "
                                 "пожалуйста укажи в подписи к нему текст поста")
            return
        await state.update_data(post_photo_id=photo_id, post_text=post_text)
        user_data = await state.get_data()
        keyboard = markups.get_confirmation_menu('send_approve', 'send_cancel')
        if user_data.get('post_photo_id'):
            await message.answer_photo(
                photo=user_data.get('post_photo_id'),
                caption=f"🏞 изображение 👆\n"
                        f"📝 текст: {user_data.get('post_text')}\n",
                reply_markup=keyboard
            )
        else:
            await message.answer(
                text=f"📝 текст: {user_data.get('post_text')}\n",
                reply_markup=keyboard
            )
        await state.set_state(PostState.wait_send_post_finish.state)

    async def send_post(self, call: types.CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        if user_data.get('post_photo_id'):
            await self.bot.send_photo(chat_id=TARGET_CHANNEL_ID,
                                      photo=user_data.get('post_photo_id'),
                                      caption=user_data.get('post_text'))
        else:
            await self.bot.send_message(chat_id=TARGET_CHANNEL_ID,
                                        text=user_data.get('post_text'))
        await call.message.answer('👌 Пост успешно отправлен в канал. /sendpost чтобы отправить еще')
        await state.finish()

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_message_handler(self.add_post_content, commands='sendpost',
                                    state='*')
        dp.register_callback_query_handler(self.edit_post_content, text='send_cancel', state='*')
        dp.register_message_handler(self.approve_post_sending, content_types=['photo', 'text'],
                                    state=PostState.wait_send_post_approve)
        dp.register_callback_query_handler(self.send_post, text='send_approve',
                                           state=PostState.wait_send_post_finish)
