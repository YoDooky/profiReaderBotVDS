from dataclasses import dataclass


@dataclass
class Book:
    user_create_id: int
    part_numb: int
    part_text: str


@dataclass
class User:
    telegram_id: int
    privilege: str
    registration_timestamp: str
    current_book: str


@dataclass
class Progress:
    telegram_id: int
    last_part_numb: int
    book_name: str
    read_timestamp: str
    shedule_read_timestamp: str
