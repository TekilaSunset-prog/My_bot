from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def add_movie_button(redacted):
    len_info = InlineKeyboardButton(text='Изменить количество информации', callback_data=f'{redacted}len_')
    url = InlineKeyboardButton(text='Ссылка', callback_data=f'{redacted}url', url=redacted)
    return InlineKeyboardMarkup(inline_keyboard=[[len_info], [url]])
