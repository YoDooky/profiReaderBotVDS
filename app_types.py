from dataclasses import dataclass


@dataclass
class Book:
    user_create_id: int
    part_numb: int
    part_text: str


@dataclass
class User:
    telegram_id: int
    telegram_username: str
    telegram_first_name: str
    telegram_last_name: str
    privilege: str
    registration_timestamp: str
    current_book: str


@dataclass
class Progress:
    telegram_id: int
    last_part_numb: int
    parts_amount: int
    book_name: str
    read_timestamp: str
    shedule_read_timestamp: str


@dataclass
class Message:
    greeting_msg: str
    add_book_msg: str
    book_format_err_msg: str
    first_book_msg: str
    same_book_msg: str
    reeding_complete_msg: str
