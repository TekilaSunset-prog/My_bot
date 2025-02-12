import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Config import TOKEN, my_help
from Steam.Functions import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# 1. Steam

@dp.message(Command('help'))
async def myhelp(message: Message):
    await message.reply(my_help)


@dp.message(Command('game'))
async def info1(message: Message):
    chat_id = message.chat.id
    mess = message.text.replace('/game ', '')
    mess1 = message.text.replace('/game', '')

    if mess1 == '':
        await message.reply('Введите название игры')
    else:
        msg = await message.reply('Ищем игру...')
        href = games_href(mess)

        if href is None or href == '':
            await bot.delete_message(chat_id, msg.message_id)
            await message.reply('Игра не найдена. Убедитесь, что правильно ввели ее название')
        else:
            await bot.delete_message(chat_id, msg.message_id)
            msg = await message.reply('Собираем данные об игре...')
            info = game_info(href)
            await bot.delete_message(chat_id, msg.message_id)
            await message.reply(href)
            await message.reply(info)


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


async def main():
    scheduler.add_job(send_wish, 'cron', minute=0, hour=0)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
