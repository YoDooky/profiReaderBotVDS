from datetime import datetime
from typing import List, Dict
from typing import Dict
from database.models import createdb
from database.models.utils import dbcontrol
from config.db_config import BOOKS_TABLE, USERS_TABLE, PROGRESS_TABLE
from telegram import vars_global
from app_types import Book, User


def db_write_users(user_data: User):
    """Write users to db"""
    dbcontrol.insert_db(USERS_TABLE, {'telegram_id': user_data.telegram_id,
                                      'privilege': user_data.privilege,
                                      'registration_timestamp': user_data.registration_timestamp})


def db_write_progress(data: Dict):
    """Write data to DB"""
    dbcontrol.insert_db(PROGRESS_TABLE, data)


def db_read_books_part_text(table_name: str, target_column: str, book_part: int) -> str:
    """Returns books part text"""
    data = dbcontrol.fetchone(table_name, target_column, {'part_numb': book_part})
    return data[0]


#
#
# def db_del_post_data(post_id: int):
#     data = {'id': post_id}
#     dbcontrol.delete(BOOKS_TABLE, data)
#     vars_global.update_schedule[0] = True


def db_add_book_table(table_name: str, books_object_list: List[Book]):
    """Create book table with demand parts amount. Return True if table alerady exist"""
    if dbcontrol.check_table_exist(table_name):
        print('[INFO] Table already exist')
        return
    dbcontrol.create_db_table(table_name)
    for book in books_object_list:
        dbcontrol.insert_db(table_name,
                            {'user_create_id': book.user_create_id,
                             'part_numb': book.part_numb,
                             'part_text': book.part_text})
