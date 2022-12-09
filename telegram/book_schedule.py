from aiogram import Bot
import aioschedule
import asyncio

from database.controllers import books_controller
import vars_global
from telegram import markups


class Schedule:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_book_text(self, user_id: int, book_name: str):
        """Send book text by shedule"""
        user_progress = books_controller.db_read_user_progress(user_id, book_name)
        if user_progress.last_part_numb >= user_progress.parts_amount:
            vars_global.update_schedule[True]
            return
        next_book_part = user_progress.last_part_numb + 1
        books_part_text = books_controller.db_read_books_part_text(book_name, next_book_part)
        user_progress.last_part_numb = next_book_part
        books_controller.db_update_progress_table(user_progress)
        keyboard = markups.get_nav_menu()
        await self.bot.send_message(chat_id=user_id, text=books_part_text, reply_markup=keyboard)

    async def scheduler(self):
        """Shedule loop"""
        self.update_schedule()  # init schedule
        while True:
            if vars_global.update_schedule[0]:
                self.update_schedule()
                vars_global.update_schedule[0] = False
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    def update_schedule(self):
        """Make shedule via DB"""
        print('[SHEDULE] Updating schedule...')
        aioschedule.clear()
        user_data = books_controller.db_read_users_data()
        for user in user_data:
            user_id = user.telegram_id
            user_book = user.current_book
            user_progress = books_controller.db_read_user_progress(user_id, user_book)
            if not user_progress:
                break
            if user_progress.last_part_numb >= user_progress.parts_amount:
                continue
            if user_book:
                aioschedule.every().minute.do(self.send_book_text,
                                              user_id=user_id,
                                              book_name=user_book)
