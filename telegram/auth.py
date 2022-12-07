from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from typing import List


class AccessMiddleware(BaseMiddleware):
    """Auth - get message only from specific ID's"""

    def __init__(self, access_id_list: List[int]):
        self.access_id_list = access_id_list
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.from_user.id) not in self.access_id_list:
            await message.answer("Access Denied")
            raise CancelHandler()
