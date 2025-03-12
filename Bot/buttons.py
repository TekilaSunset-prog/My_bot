from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from kinopoisk.functions import movie_href


def add_movie_button(redact, full=False, short=False):
    full_info = InlineKeyboardButton(text='Полная информация', callback_data=f'{redact}len_movie')
    short_info = InlineKeyboardButton(text='Краткая информация', callback_data=f'{redact}len_movie')
    url = InlineKeyboardButton(text='Ссылка', callback_data='url', url=movie_href(redact)[0])
    if full:
        return InlineKeyboardMarkup(inline_keyboard=[[full_info], [url]])
    if short:
        return InlineKeyboardMarkup(inline_keyboard=[[short_info], [url]])


def add_game_button(redact=None, name=None, li=None, url_=None):
    if li:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data=f'{li[0]}LISTS')],
            [InlineKeyboardButton(text='2', callback_data=f'{li[1]}LISTS')],
            [InlineKeyboardButton(text='3', callback_data=f'{li[2]}LISTS')],
            [InlineKeyboardButton(text='4', callback_data=f'{li[3]}LISTS')],
            [InlineKeyboardButton(text='5', callback_data=f'{li[4]}LISTS')],
            [InlineKeyboardButton(text='6', callback_data=f'{li[5]}LISTS')],
            [InlineKeyboardButton(text='7', callback_data=f'{li[6]}LISTS')],
            [InlineKeyboardButton(text='8', callback_data=f'{li[7]}LISTS')],
            [InlineKeyboardButton(text='9', callback_data=f'{li[8]}LISTS')],
            [InlineKeyboardButton(text='10', callback_data=f'{li[9]}LISTS')]
        ])
    url = InlineKeyboardButton(text='Ссылка', url=redact)
    if url_:
        return InlineKeyboardMarkup(inline_keyboard=[[url]])
    found = InlineKeyboardButton(text='Это не та игра', callback_data=f'{name}NOT FOUND GAME')
    return InlineKeyboardMarkup(inline_keyboard=[[url], [found]])


def add_help_button(al=False, back=None):
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    steam = InlineKeyboardButton(text='Steam', callback_data='steam')
    kinopoisk = InlineKeyboardButton(text='Kinopoisk', callback_data='kinopoisk')
    if al:
        return InlineKeyboardMarkup(inline_keyboard=[[steam], [kinopoisk]])
    if back:
        return InlineKeyboardMarkup(inline_keyboard=[[back]])