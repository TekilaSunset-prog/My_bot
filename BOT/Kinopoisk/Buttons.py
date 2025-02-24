from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def add_movie_button(redacted):
    short_info = InlineKeyboardButton(text='Краткая информация', callback_data=f'{redacted}short_info')
    full_info = InlineKeyboardButton(text='Полная информация', callback_data=f'{redacted}full_info')
    url = InlineKeyboardButton(text='Ссылка', callback_data=f'{redacted}url', url=redacted)
    return InlineKeyboardMarkup(inline_keyboard=[[short_info], [full_info], [url]])
