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


def db_read_messages() -> Message:
    """Read bot messages from DB"""
    data = dbcontrol.fetchall(MESSAGES_TABLE, ['greeting_msg',
                                               'add_book_msg',
                                               'book_format_err_msg',
                                               'first_book_msg',
                                               'same_book_msg',
                                               'reeding_complete_msg'])

    messages = Message(greeting_msg=data[0].get('greeting_msg'),
                       add_book_msg=data[0].get('add_book_msg'),
                       book_format_err_msg=data[0].get('book_format_err_msg'),
                       first_book_msg=data[0].get('first_book_msg'),
                       same_book_msg=data[0].get('same_book_msg'),
                       reeding_complete_msg=data[0].get('reeding_complete_msg'))
    return messages


def db_update_message_table(message: Dict):
    """Updates message table"""
    dbcontrol.update_db(MESSAGES_TABLE, {'id': 1}, message)
