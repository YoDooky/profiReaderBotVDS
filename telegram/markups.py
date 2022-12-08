from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_next_part_button():
    next_part_button = InlineKeyboardMarkup(row_width=1)
    next_button = InlineKeyboardButton(text='--------->', callback_data='next_part')
    next_part_button.insert(next_button)
    return next_part_button


def get_nav_menu():
    nav_menu = InlineKeyboardMarkup(row_width=2)
    prev_button = InlineKeyboardButton(text='<---------', callback_data='prev_part')
    next_button = InlineKeyboardButton(text='--------->', callback_data='next_part')
    nav_menu.insert(prev_button)
    nav_menu.insert(next_button)
    return nav_menu
