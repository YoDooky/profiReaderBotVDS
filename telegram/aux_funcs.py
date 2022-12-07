import textwrap
import ebooklib
from ebooklib import epub
from config.bot_config import MAX_MESSAGE_LENGHT
from bs4 import BeautifulSoup
from typing import List
from database.controllers import books_controller
from app_types import Book


def write_book_to_db(user_id: int, filepath: str):
    """Writes book text to DB"""
    epub_text = parse_epub_data(filepath)
    text_parts = divide_string_to_parts(epub_text, user_id)
    table_name = get_book_name(filepath)
    books_controller.db_add_book_table(table_name, text_parts)


def get_book_name(filepath: str) -> str:
    """Returns table name from filepath"""
    filename = filepath.split('\\')[-1]
    table_name = "".join(ch for ch in filename if ch.isalnum())
    table_name = ''.join(i for i in table_name if not i.isdigit())
    return table_name


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
    full_string.replace('<', '|')
    return full_string


def divide_string_to_parts(string_object: str, user_id: int) -> List[Book]:
    """Divivide string to list parts"""
    wrapper = textwrap.TextWrapper(width=MAX_MESSAGE_LENGHT)
    wrap_list = wrapper.wrap(text=string_object)
    book_parts = []
    for num_part, part in enumerate(wrap_list):
        book_parts.append(Book(user_create_id=user_id, part_numb=num_part + 1, part_text=part))
    return book_parts
