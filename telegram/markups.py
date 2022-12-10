from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.controllers import message_controller


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_next_part_button():
    next_part_button = InlineKeyboardMarkup(row_width=1)
    next_button = InlineKeyboardButton(text='>>>', callback_data='next_part')
    next_part_button.insert(next_button)
    return next_part_button


def get_nav_menu():
    nav_menu = InlineKeyboardMarkup(row_width=2)
    prev_button = InlineKeyboardButton(text='<<<', callback_data='prev_part')
    next_button = InlineKeyboardButton(text='>>>', callback_data='next_part')
    nav_menu.insert(prev_button)
    nav_menu.insert(next_button)
    return nav_menu


def show_bot_messages_menu():
    bot_messages_menu = InlineKeyboardMarkup(row_width=2)
    bot_messages_button = InlineKeyboardButton(text='🔧 Редактировать сообщения бота',
                                               callback_data='edit_bot_messages')
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    bot_messages_menu.insert(start_button)
    bot_messages_menu.insert(bot_messages_button)
    return bot_messages_menu


def get_bot_messages_menu():
    bot_messages_menu = InlineKeyboardMarkup(row_width=1)
    bot_messages_buttons = [
        InlineKeyboardButton(text=message_controller.db_read_messages().greeting_msg,
                             callback_data='GREETING_MSG'),
        InlineKeyboardButton(text=message_controller.db_read_messages().add_book_msg,
                             callback_data='ADD_BOOK_MSG'),
        InlineKeyboardButton(text=message_controller.db_read_messages().book_format_err_msg,
                             callback_data='BOOK_FORMAT_ERR_MSG'),
        InlineKeyboardButton(text=message_controller.db_read_messages().first_book_msg,
                             callback_data='FIRST_BOOK_MSG'),
        InlineKeyboardButton(text=message_controller.db_read_messages().same_book_msg,
                             callback_data='SAME_BOOK_MSG'),
        InlineKeyboardButton(text=message_controller.db_read_messages().reeding_complete_msg,
                             callback_data='REEDING_COMPLETE_MSG')
    ]
    for button in bot_messages_buttons:
        bot_messages_menu.insert(button)
    return bot_messages_menu
