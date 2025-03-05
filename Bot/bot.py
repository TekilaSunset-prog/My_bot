import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import *
from kinopoisk.functions import *
from steam.functions import *
from buttons import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


# 1. Steam
@dp.message(Command('help'))
async def myhelp(message: Message):
    await message.answer('Бот умеет отправлять информацию о фильмах, сериалах, играх и т.д.', reply_markup=add_help_button(al=True))


@dp.callback_query(lambda x: x.data == 'back')
async def help_back(callback: CallbackQuery):
    await callback.message.edit_text(text='Бот умеет отправлять информацию о фильмах, сериалах, играх и т.д.', reply_markup=add_help_button(al=True))


@dp.callback_query(lambda x: x.data == 'steam')
async def help_steam(callback: CallbackQuery):
    if '/game' not in callback.message.text:
        await callback.message.edit_text(text=steam, reply_markup=add_help_button(back=True))
    await callback.answer(text='Steam')


@dp.callback_query(lambda x: x.data == 'kinopoisk')
async def help_kinopoisk(callback: CallbackQuery):
    if '/movie' not in callback.message.text:
        await callback.message.edit_text(text=kinopoisk, reply_markup=add_help_button(back=True))
    await callback.answer(text='Kinopoisk')


@dp.message(Command('game'))
async def info1(message: Message):
    chat_id = message.chat.id
    mess = message.text.replace('/game ', '')
    mess1 = message.text.replace('/game', '')

    if mess1 == '':
        await message.reply('Введите название игры')
    else:
        msg = await message.reply('Ищем игру...')
        url = games_href(mess)

        if url is None or url == '':
            await bot.delete_message(chat_id, msg.message_id)
            await message.reply('Игра не найдена. Убедитесь, что правильно ввели ее название')
        else:
            await bot.delete_message(chat_id, msg.message_id)
            msg = await message.reply('Собираем данные об игре...')
            info = game_info(url)
            name = game_info(url, only_name=True)
            await bot.delete_message(chat_id, msg.message_id)
            file = FSInputFile(f'steam/images/{name}.png')
            await message.answer_photo(file)
            await message.reply(info, reply_markup=add_game_button(url))


@dp.callback_query(lambda x: 'game_url' in x.data)
async def button_url_game():
    pass


@dp.message(Command('user'))
async def user_info1(message: Message):
    user_id = message.text.replace('/user ', '')
    if message.text.replace('/user', '') == '':
        await message.reply('Введите id пользователя')
    else:
        await message.reply((user_info(user_id)))


@dp.message(Command('wish'))
async def wishgame(message: Message):
    mess = message.text.replace('/wish ', '')
    if message.text.replace('/wish', '') == '':
        await message.reply('Введите название игры')
    else:
        if game_info(games_href(mess), only_price=True):
            await message.reply(game_info(games_href(mess), only_price=False))
        else:
            game_name = game_info(games_href(mess), only_name=True)
            chat_id = message.chat.id

            if game_name == 'Игра не найдена. Убедитесь, что правильно ввели ее название' or game_name == 'None':
                await message.reply('Игра не найдена. Убедитесь, что правильно ввели ее название')

            else:
                await message.reply(wish_game(chat_id, game_name, True))


@dp.message(Command('wishdel'))
async def wishgame1(message: Message):
    name = message.text.replace('/wishdel ', '')
    if message.text.replace('/wishdel', '') == '':
        await message.reply('Введите название игры или all')
    else:
        if name != 'all':
            game_name = game_info(games_href(name), True)

        else:
            game_name = 'all'

        chat_id = message.chat.id
        await message.reply(wish_game(chat_id, game_name, delete=True))


@dp.message(Command('wishlist'))
async def wishgame2(message: Message):
    chat_id = message.chat.id
    await message.reply(wish_game(chat_id, json_output=True))


async def send_wish():
    await bot.send_message(chat_id=5651350400, text='Обработка началась')
    data = wish_processing()
    i = 0
    q = 0
    games = ''
    for key in data:
        names = data[key]
        q += i
        i = 0
        final_text = ''
        for name in names:
            i += 1
            games += name + '\n'
            text = game_info(games_href(name), only_price=False)
            final_text += f'{i}. {text}'
        await bot.send_message(chat_id=int(key), text=final_text)
    await bot.send_message(chat_id=5651350400, text=f'Обработано {str(q)} игр\n{games}')


# 2. Kinopoisk
@dp.message(Command('movie'))
async def movie(message: Message):
    mess = message.text.replace('/movie', '')
    chat_id = message.chat.id
    if mess == '':
        await message.reply('Введите название картины')
    else:
        msg = await message.reply('Ищем...')
        inf = movie_href(mess)
        if inf is False:
            await bot.delete_message(chat_id, msg.message_id)
            await message.reply('Кино не найдено. Убедитесь, что правильно ввели название')
        else:
            empty = False
            url = inf[0]
            category = inf[1]
            await bot.delete_message(chat_id, msg.message_id)
            msg = await message.reply('Собираем данные о кино...')
            info = movie_info(url, category)
            name = info[2].replace('.png', '')
            file = FSInputFile(f'kinopoisk/images/{info[2]}')
            await bot.delete_message(chat_id, msg.message_id)
            await message.answer_photo(file, caption=info[0], reply_markup=add_movie_button(url.replace('?utm_referrer=www.kinopoisk.ru', '') + f'name{name}', full=True))

            with open('kinopoisk/jsons/info.json', 'r') as f:
                try:
                    json_data = json.load(f)
                except JSONDecodeError:
                    empty = True
            if empty:
                gen = json_data.update({name: [info[0], info[1]]})
            else:
                gen = {name: [info[0], info[1]]}
            json.dumps(gen)
            with open('kinopoisk/jsons/info.json', 'w') as ff:
                json.dump(gen, ff, indent=2)


@dp.callback_query(lambda x: 'len_movie' in x.data)
async def button_url(callback: CallbackQuery):
    mess = str(callback.data)
    name = ''
    for index in range(len(mess)):
        if mess[index] == 'n':
            if mess[index + 1] == 'a':
                if mess[index + 2] == 'm':
                    if mess[index + 3] == 'e':
                        for index1 in range(index + 4, len(mess)):
                            name += mess[index1]
    with open('kinopoisk/jsons/info.json', 'r') as f:
        data = json.load(f)
    info = data.get(name)

    id1 = callback.inline_message_id
    if callback.message.caption.strip() == info[0].strip():
        await callback.message.edit_caption(inline_message_id=id1, caption=info[1], reply_markup=add_movie_button(mess + name, short=True))
    else:
        await callback.message.edit_caption(inline_message_id=id1, caption=info[0], reply_markup=add_movie_button(mess + name, full=True))



@dp.callback_query(lambda x: 'url' in x.data)
async def button_url():
    pass

async def main():
    scheduler.add_job(send_wish, 'cron', minute=0, hour=0)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
