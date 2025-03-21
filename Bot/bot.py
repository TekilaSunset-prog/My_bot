import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from kinopoisk.functions import *
from steam.functions import *
from buttons import *
from jsons.jsfiles import get_param

logging.basicConfig(level=logging.INFO)
bot = Bot(token=get_param('Token'))
dp = Dispatcher()
scheduler = AsyncIOScheduler()


@dp.message(Command('help'))
async def myhelp(message: Message):
    await message.answer('Бот умеет отправлять информацию о фильмах, сериалах, играх и т.д.',
                         reply_markup=add_help_button(al=True))


@dp.callback_query(lambda x: x.data == 'back')
async def help_back(callback: CallbackQuery):
    await callback.message.edit_text(text='Бот умеет отправлять информацию о фильмах, сериалах, играх и т.д.',
                                     reply_markup=add_help_button(al=True))


@dp.callback_query(lambda x: x.data == 'steam')
async def help_steam(callback: CallbackQuery):
    await callback.message.edit_text(text=get_param('steam'), reply_markup=add_help_button(back=True))
    await callback.answer(text='Steam')


@dp.callback_query(lambda x: x.data == 'kinopoisk')
async def help_kinopoisk(callback: CallbackQuery):
    await callback.message.edit_text(text=get_param('kinopoisk'), reply_markup=add_help_button(back=True))
    await callback.answer(text='Kinopoisk')


# 1. Steam
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
            await message.answer_photo(file, caption=info, reply_markup=add_game_button(url, mess))


@dp.callback_query(lambda x: 'NOT FOUND GAME' in x.data)
async def different_game(callback: CallbackQuery):
    data = games_href(callback.data.replace('NOT FOUND GAME', ''), different_game=True)
    print(callback.data.replace('NOT FOUND GAME', ''))
    if data is False:
        await callback.answer('Совпадений не найдено')
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        text = 'Возможно вы имели ввиду:\n'
        for index in range(len(data)):
            text += f'{index + 1}. {data[index]}\n\n'
        await callback.message.answer(text, reply_markup=add_game_button(li=data))


@dp.callback_query(lambda x: 'LISTS' in x.data)
async def lists(callback: CallbackQuery):
    name = callback.data.replace('LISTS', '')
    url = games_href(name)
    info = game_info(url)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    file = FSInputFile(f'steam/images/{name}.png')
    await callback.message.answer_photo(file, caption=info, reply_markup=add_game_button(redact=url, url_=True))


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
            if movie_href(name) is False:
                await bot.delete_message(chat_id, msg.message_id)
                await message.reply('Кино не найдено. Убедитесь, что правильно ввели название')
            else:
                file = FSInputFile(f'kinopoisk/images/{info[2]}')
                await bot.delete_message(chat_id, msg.message_id)
                await message.answer_photo(file, caption=info[0], reply_markup=add_movie_button(name, full=True))

                with open('kinopoisk/jsons/info.json', 'r') as f:
                    try:
                        json_data = json.load(f)
                    except JSONDecodeError:
                        empty = True
                if not empty:
                    json_data.update({name: [info[0], info[1]]})
                else:
                    json_data = {name: [info[0], info[1]]}
                json.dumps(json_data)
                with open('kinopoisk/jsons/info.json', 'w') as ff:
                    json.dump(json_data, ff, indent=2)


@dp.callback_query(lambda x: 'len_movie' in x.data)
async def button_url(callback: CallbackQuery):
    name = str(callback.data).replace('len_movie', '')

    with open('kinopoisk/jsons/info.json', 'r') as f:
        data = json.load(f)
    info = data.get(name)
    id1 = callback.inline_message_id
    if callback.message.caption.strip() == info[0].strip():
        await callback.message.edit_caption(inline_message_id=id1, caption=info[1],
                                            reply_markup=add_movie_button(name, short=True))
    else:
        await callback.message.edit_caption(inline_message_id=id1, caption=info[0],
                                            reply_markup=add_movie_button(name, full=True))


@dp.callback_query(lambda x: x.data == 'url')
async def button_url():
    pass


# 3. Admin
@dp.message(Command('log'))
async def file(message: Message):
    if message.from_user.id in get_param():
        logs = FSInputFile('log/log.txt')
        await message.reply_document(logs)


async def main():
    scheduler.add_job(send_wish, 'cron', minute=0, hour=0)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
