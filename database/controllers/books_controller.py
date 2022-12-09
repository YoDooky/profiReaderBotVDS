from typing import List
from database.models.utils import dbcontrol
from config.db_config import USERS_TABLE, PROGRESS_TABLE
from app_types import Book, User, Progress


def db_write_users(user_data: User):
    """Write users to db"""
    dbcontrol.insert_db(USERS_TABLE, {'telegram_id': user_data.telegram_id,
                                      'telegram_username': user_data.telegram_username,
                                      'telegram_first_name': user_data.telegram_first_name,
                                      'telegram_last_name': user_data.telegram_last_name,
                                      'privilege': user_data.privilege,
                                      'registration_timestamp': user_data.registration_timestamp,
                                      'current_book': user_data.current_book})


def db_write_progress(progress_data: Progress):
    """Write progress to DB"""
    try:
        existed_data = db_read_user_progress(progress_data.telegram_id, progress_data.book_name)
        if existed_data:
            if existed_data.book_name == progress_data.book_name:
                return
    except TypeError:
        pass
    dbcontrol.insert_db(PROGRESS_TABLE, {'fk_user_id': progress_data.telegram_id,
                                         'last_page': progress_data.last_part_numb,
                                         'pages_amount': progress_data.parts_amount,
                                         'book_filename': progress_data.book_name,
                                         'read_timestamp': progress_data.read_timestamp,
                                         'shedule_read_timestamp': progress_data.shedule_read_timestamp})


def db_read_users_data() -> List[User]:
    """Returns users table data"""
    data = dbcontrol.fetchall(USERS_TABLE, ['telegram_id', 'privilege', 'registration_timestamp', 'current_book'])
    user_data = [User(telegram_id=each.get('telegram_id'),
                      telegram_username=each.get('telegram_username'),
                      telegram_first_name=each.get('telegram_first_name'),
                      telegram_last_name=each.get('telegram_last_name'),
                      privilege=each.get('privilege'),
                      registration_timestamp=each.get('registration_timestamp'),
                      current_book=each.get('current_book')) for each in data]
    return user_data


def db_read_user_current_book(user_id: int) -> str:
    user_data = db_read_users_data()
    for user in user_data:
        if user.telegram_id != user_id:
            continue
        return user.current_book


def db_read_user_progress(user_id: int, book_filename: str) -> Progress:
    """Returns last user selected part"""
    progress_data = dbcontrol.fetchall(PROGRESS_TABLE, [
        'fk_user_id',
        'last_page',
        'pages_amount',
        'book_filename',
        'read_timestamp',
        'shedule_read_timestamp'
    ])
    for each in progress_data:
        if each.get('fk_user_id') != user_id:
            continue
        if each.get('book_filename') != book_filename:
            continue
        return Progress(
            telegram_id=int(each.get('fk_user_id')),
            last_part_numb=int(each.get('last_page')),
            parts_amount=int(each.get('pages_amount')),
            book_name=each.get('book_filename'),
            read_timestamp=each.get('read_timestamp'),
            shedule_read_timestamp=each.get('shedule_read_timestamp')
        )


def db_read_book_data(table_name: str) -> List:
    data = dbcontrol.fetchall(table_name, ['part_numb'])
    return data


def db_read_books_part_text(table_name: str, book_part: int) -> str:
    """Returns books part text"""
    data = dbcontrol.fetchone(table_name, 'part_text', {'part_numb': book_part})
    data = data[0].replace('\\n', '\n')
    data = data.replace('\\xa0', ' ')
    return data


def db_update_progress_table(progress_data: Progress):
    """Updates last page data"""
    dbcontrol.update_db(PROGRESS_TABLE, {'fk_user_id': progress_data.telegram_id,
                                         'book_filename': progress_data.book_name},
                        {'last_page': progress_data.last_part_numb})
    dbcontrol.update_db(PROGRESS_TABLE, {'fk_user_id': progress_data.telegram_id,
                                         'book_filename': progress_data.book_name},
                        {'read_timestamp': progress_data.read_timestamp})
    dbcontrol.update_db(PROGRESS_TABLE, {'fk_user_id': progress_data.telegram_id,
                                         'book_filename': progress_data.book_name},
                        {'shedule_read_timestamp': progress_data.shedule_read_timestamp})


def db_update_users_table(user_id: int, book_name: str):
    """Updates users table"""
    dbcontrol.update_db(USERS_TABLE, {'telegram_id': user_id}, {'current_book': book_name})


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
