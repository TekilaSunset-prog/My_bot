from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_movie_button(redact, full=False, short=False):
    full_info = InlineKeyboardButton(text='Полная информация', callback_data=f'{redact}len_movie')
    short_info = InlineKeyboardButton(text='Краткая информация', callback_data=f'{redact}len_movie')
    url = InlineKeyboardButton(text='Ссылка', callback_data=f'{redact}url', url=redact.replace('film_', '').replace('series_', ''))
    if full:
        return InlineKeyboardMarkup(inline_keyboard=[[full_info], [url]])
    if short:
        return InlineKeyboardMarkup(inline_keyboard=[[short_info], [url]])


def add_game_button(redact):
    url = InlineKeyboardButton(text='Ссылка', callback_data=f'{redact}game_url', url=redact)
    return InlineKeyboardMarkup(inline_keyboard=[[url]])


def add_help_button(al=False, back=None):
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    steam = InlineKeyboardButton(text='Steam', callback_data='steam')
    kinopoisk = InlineKeyboardButton(text='Kinopoisk', callback_data='kinopoisk')
    if al:
        return InlineKeyboardMarkup(inline_keyboard=[[steam], [kinopoisk]])
    if back:
        return InlineKeyboardMarkup(inline_keyboard=[[back]])