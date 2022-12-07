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
