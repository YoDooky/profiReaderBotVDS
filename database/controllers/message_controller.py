from typing import Dict
from database.models.utils import dbcontrol
from config.db_config import MESSAGES_TABLE
from config.bot_config import GREETING_MSG, ADD_BOOK_MSG, BOOK_FORMAT_ERR_MSG, FIRST_BOOK_MSG, SAME_BOOK_MSG, \
    REEDING_COMPLETE_MSG
from app_types import Message


def db_init_message_table():
    """Init starting messages for bot"""
    if not dbcontrol.check_table_empty(MESSAGES_TABLE):  # if table with messages not empty then return
        return
    dbcontrol.insert_db(MESSAGES_TABLE, {
        'id': 1,
        'greeting_msg': GREETING_MSG,
        'add_book_msg': ADD_BOOK_MSG,
        'book_format_err_msg': BOOK_FORMAT_ERR_MSG,
        'first_book_msg': FIRST_BOOK_MSG,
        'same_book_msg': SAME_BOOK_MSG,
        'reeding_complete_msg': REEDING_COMPLETE_MSG
    })


def db_update_message_table(message: Dict):
    """Updates message table"""
    dbcontrol.update_db(MESSAGES_TABLE, {'id': 1}, message)
