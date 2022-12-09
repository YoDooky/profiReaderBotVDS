from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.bot_config import GREETING_MSG, ADD_BOOK_MSG, BOOK_FORMAT_ERR_MSG, FIRST_BOOK_MSG, SAME_BOOK_MSG, \
    REEDING_COMPLETE_MSG


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


def show_bot_messages_menu():
    bot_messages_menu = InlineKeyboardMarkup(row_width=2)
    bot_messages_button = InlineKeyboardButton(text='🔧 Редактировать сообщения бота', callback_data='edit_bot_messages')
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    bot_messages_menu.insert(start_button)
    bot_messages_menu.insert(bot_messages_button)
    return bot_messages_menu


def get_bot_messages_menu():
    bot_messages_menu = InlineKeyboardMarkup(row_width=1)
    bot_messages_buttons = [
        InlineKeyboardButton(text=GREETING_MSG, callback_data='GREETING_MSG'),
        InlineKeyboardButton(text=ADD_BOOK_MSG, callback_data='ADD_BOOK_MSG'),
        InlineKeyboardButton(text=BOOK_FORMAT_ERR_MSG, callback_data='BOOK_FORMAT_ERR_MSG'),
        InlineKeyboardButton(text=FIRST_BOOK_MSG, callback_data='FIRST_BOOK_MSG'),
        InlineKeyboardButton(text=SAME_BOOK_MSG, callback_data='SAME_BOOK_MSG'),
        InlineKeyboardButton(text=REEDING_COMPLETE_MSG, callback_data='REEDING_COMPLETE_MSG')
    ]
    for button in bot_messages_buttons:
        bot_messages_menu.insert(button)
    return bot_messages_menu
