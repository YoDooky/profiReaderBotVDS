import datetime
import textwrap
import ebooklib
from ebooklib import epub
from config.bot_config import MAX_MESSAGE_LENGHT
from bs4 import BeautifulSoup
from typing import List, Dict
from database.controllers import books_controller
from app_types import Book, Progress


def write_book_to_db(user_id: int, filepath: str):
    """Writes book text to DB"""
    epub_text = parse_epub_data(filepath)
    text_parts = divide_string_to_parts(epub_text, user_id)
    table_name = get_book_name(filepath)
    books_controller.db_add_book_table(table_name, text_parts)


def get_book_name(filepath: str) -> str:
    """Returns table name from filepath"""
    filename = filepath.split('/')[-1]
    table_name = "".join(ch for ch in filename if ch.isalnum())
    table_name = ''.join(i for i in table_name if not i.isdigit())
    return table_name.lower()


def get_last_part_numb(user_id: int, book_name: str) -> int:
    """Returns last red part"""
    try:
        progress = books_controller.db_read_user_progress(user_id, book_name)
        if not progress:
            return 1
        last_red_page = progress.last_part_numb
    except TypeError:
        last_red_page = 1
    return last_red_page


def init_first_book(user_id: int, filepath: str) -> str | Dict:
    """Writes progress and returns books part text from first loaded book"""
    book_name = get_book_name(filepath)
    new_book_flag = True
    last_red_page = get_last_part_numb(user_id, book_name)
    if last_red_page > 1:
        new_book_flag = False
    books_part_text = books_controller.db_read_books_part_text(book_name, last_red_page)
    progress_data = Progress(telegram_id=user_id,
                             last_part_numb=last_red_page,
                             book_name=book_name,
                             read_timestamp=str(datetime.datetime.now()),
                             shedule_read_timestamp=str(datetime.datetime.now() + datetime.timedelta(days=1)))
    books_controller.db_update_users_table(user_id, book_name)
    books_controller.db_write_progress(progress_data)
    return {'books_part_text': books_part_text, 'new_book': new_book_flag}


def parse_epub_data(filepath: str) -> str:
    """Returns text from epub"""
    book = epub.read_epub(filepath)
    full_text = []
    tags_whitelist = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for document in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(document.content, features='xml')
        data = soup.find_all(tags_whitelist)
        for each in data:
            if not each.text:
                continue
            full_text.append(each.text)
    full_string = '\n'.join(full_text)
    return full_string.replace('<', '|')


def divide_string_to_parts(string_object: str, user_id: int) -> List[Book]:
    """Divivide string to list parts"""
    wrapper = textwrap.TextWrapper(width=MAX_MESSAGE_LENGHT, break_long_words=False, replace_whitespace=False)
    wrap_list = wrapper.wrap(text=string_object)
    book_parts = []
    for num_part, part in enumerate(wrap_list):
        book_parts.append(Book(user_create_id=user_id, part_numb=num_part + 1, part_text=part))
    return book_parts
