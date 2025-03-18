import json
import os
from json import JSONDecodeError

import requests

from bs4 import BeautifulSoup

from Bot.log.logs import log


@log
def games_href(game_name, different_game=None):
    url = f'https://store.steampowered.com/search/?term={game_name}&category1=998&ndl=1&ignore_preferences=1'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    if bool(different_game) not in [None, False]:
        sp = soup.find_all('div', class_='responsive_search_name_combined')
        spis = []
        try:
            for html in range(1, 11):
                spis.append(sp[html].find('span', class_='title').text)
        except IndexError:
            if len(spis) == 0:
                return False
        return spis

    text = soup.find('div', id="search_resultsRows")
    text = str(text)
    href = ''

    flag = False
    for index in range(len(text)):
        if flag:
            break
        if text[index] == 'h':
            if text[index + 1] == 'r':
                if text[index + 2] == 'e':
                    if text[index + 3] == 'f':
                        for index1 in range(index + 4, len(text)):
                            if text[index1] == '"':
                                flag = True
                                continue
                            if text[index1] == ' ':
                                break
                            if flag is True:
                                href += text[index1]
    return href


@log
def game_info(url, only_name=None, only_price=None):
    if url == '':
        return 'Игра не найдена. Убедитесь, что правильно ввели ее название'

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('div', class_="apphub_AppName").text

    if only_name is True:
        return name

    if only_price is True:
        price = soup.find_all('div', class_='game_area_purchase_platform')
        for element in price:
            price1 = element.find_next('h1')
            name1 = 'Buy ' + name
            if name1.lower() == price1.text.lower():
                disc = element.find_next('div', class_="game_purchase_action_bg")
                return '%' in disc.text
        else:
            return False

    if only_price is False:
        html = soup.find_all('div', class_='game_area_purchase_platform')
        flag = False
        for element in html:
            if flag is True:
                break
            html1 = element.find_next('h1').text
            name1 = 'Buy ' + name
            if name1.lower() == html1.lower():
                disc = element.find_next('div', class_="game_purchase_action_bg").text
                if '%' in disc:
                    percents = ''
                    final_price = ''
                    price = ''

                    for index in range(len(disc)):
                        if disc[index] == '-':
                            index1 = index
                            while disc[index1] != '%':
                                index1 += 1
                                percents += disc[index1]
                        if disc[index] == '%':
                            index2 = index
                            while disc[index2] != '.':
                                index2 += 1
                                price += disc[index2]

                            while disc[index2 + 1] != '.':
                                index2 += 1
                                final_price += disc[index2]
                            flag = True
                            break

        if flag is False:
            return False

        final_text = f'На {name} действует скидка в {percents}\nЦена без скидки: {price}\nЦена со скидкой: {final_price}.\n\n'
        return final_text

    html = soup.find_all('div', class_='game_area_purchase_platform')
    flag = False
    price_text = ''

    for element in html:
        if flag is True:
            break
        html1 = element.find_next('h1').text.strip()
        name1 = 'Buy ' + name
        name2 = 'Play ' + name
        if name1.lower() == html1.lower() or name2.lower() == html1.lower():
            disc = element.find_next('div', class_="game_purchase_action_bg").text
            if 'free to play' in disc.lower():
                price_text = 'Игра бесплатна\n\n'
            if '%' not in disc:
                price = ''
                for index in range(len(disc)):
                    if flag is True:
                        break
                    try:
                        if type(int(disc[index])) == int:
                            index1 = index - 1
                            while disc[index1] != '.':
                                index1 += 1
                                price += disc[index1]
                            price_text = f'Цена: {price}\n\n'
                            flag = True
                            break
                    except ValueError:
                        continue
            else:
                percents = ''
                final_price = ''
                price = ''

                for index in range(len(disc)):
                    if disc[index] == '-':
                        index1 = index
                        while disc[index1] != '%':
                            index1 += 1
                            percents += disc[index1]
                    if disc[index] == '%':
                        index2 = index
                        while disc[index2] != '.':
                            index2 += 1
                            price += disc[index2]

                        while disc[index2 + 1] != '.':
                            index2 += 1
                            final_price += disc[index2]
                        flag = True
                        break

                price_text = f'На данный момент на игру действует скидка в {percents}\nЦена без скидки: {price}\nЦена со скидкой: {final_price}.\n\n'

    url_for_dlcs = url.replace('app', 'dlc')
    url_for_dlcs1 = url_for_dlcs[::-1]
    delete = False

    for i in range(len(url_for_dlcs)):
        if url_for_dlcs[i] == '?':
            delete = True
        if delete is True:
            url_for_dlcs1 = url_for_dlcs1.replace(url_for_dlcs[i], ' ', 1)

    url_for_dlcs = url_for_dlcs1[::-1].replace(' ', '')
    early_access = soup.find('div', class_="game_area_comingsoon game_area_bubble")
    if early_access is not None:
        early_access = 'Игра еще не вышла'
    else:
        early_access = ''

    response_dls = requests.get(url_for_dlcs)
    response_dls.raise_for_status()
    soup_dls = BeautifulSoup(response_dls.text, 'lxml')
    dlcs = soup_dls.find_all('span', class_="color_created")

    reviews_of_all_time = soup.find_all('div', class_="summary column")[1].text.strip('\n')
    reviews_recent = soup.find_all('div', class_="summary column")[0].text.strip('\n')
    reviews_recent1 = ''
    reviews_of_all_time1 = ''

    for letter in range(len(reviews_recent)):
        if reviews_recent[letter] == '-':
            for letter2 in range(letter + 2, len(reviews_recent)):
                reviews_recent1 += reviews_recent[letter2]

    for letter3 in range(len(reviews_of_all_time)):
        if reviews_of_all_time[letter3] == '-':
            for letter4 in range(letter3 + 2, len(reviews_of_all_time)):
                reviews_of_all_time1 += reviews_of_all_time[letter4]

    reviews_of_all_time1 = reviews_of_all_time1.replace('of the', 'из').replace(
        'user reviews for this game are positive.', 'обзоров пользователей положительные')

    reviews_recent1 = reviews_recent1.replace('of the', 'из').replace(
        'user reviews in the last 30 days are positive.',
        'обзоров пользователей за последние 30 дней положительные')

    if reviews_recent1 == '':
        reviews_recent1 = 'Нет обзоров'
    if reviews_of_all_time1 == '':
        reviews_of_all_time1 = 'Нет обзоров'
    if reviews_of_all_time1 == 'Нет обзоров' and reviews_recent != 'Нет обзоров':
        reviews_of_all_time1 = reviews_recent1
        reviews_recent1 = 'Нет обзоров'

    ind = -1
    dlcs1 = 'DLC: \n'
    for item in dlcs:
        ind += 1
        item = item.text
        if item != ' ':
            dlcs1 += item + '\n'

    if len(dlcs1) == 6:
        dlcs1 = 'DLC для этой игры нет'

    if early_access != '':
        price_text = 'Цены нет\n\n'

    dev = soup.find('div', id="developers_list").text.strip()
    pub = soup.find_all('div', class_='dev_row')[1].text.replace('\n', '').replace('Publisher:', '')

    data_pub = soup.find('div', class_="date").text.replace('Coming soon', '')

    image = str(soup.find('div', class_="game_header_image_ctn"))
    flag = False
    href = ''
    for index in range(len(image)):
        if flag:
            break
        if image[index] == 's':
            if image[index + 1] == 'r':
                if image[index + 2] == 'c':
                    if image[index + 3] == '=':
                        for index1 in range(index + 5, len(image)):
                            flag = True
                            if image[index1] == '"':
                                break
                            if flag is True:
                                href += image[index1]

    if not f'{name}.png' in os.listdir('steam/images'):
        res = requests.get(href)
        with open(f'steam/images/{name}.png', 'wb') as f:
            f.write(res.content)

    return (f'{early_access}\n'
            f'Название: {name}\n\n'
            f'Дата выхода: {data_pub}\n\n'
            f'{price_text}'
            f'Разработчик: {dev}\n'
            f'Издатель: {pub}\n\n'
            f'Недавние обзоры: {reviews_recent1}\n'
            f'Обзоры за все время: {reviews_of_all_time1}\n\n'
            f'{dlcs1}'
            )


@log
def user_info(user_id):
    url = f'https://steamcommunity.com/profiles/{user_id}'

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    try:
        nickname = soup.find('span', class_="actual_persona_name").text
    except AttributeError:
        url = f'https://steamcommunity.com/profiles/id/{user_id}'

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        try:
            nickname = soup.find('span', class_="actual_persona_name").text
        except AttributeError:
            return 'Пользователь не найден. Убедитесь, что правильно ввели id'

    player_level_html = soup.find('span', class_="friendPlayerLevelNum").text
    player_level = f'Уровень профиля пользователя: {player_level_html}'

    profile_status = soup.find('div', class_="profile_private_info")
    if profile_status is not None and 'This profile is private' in profile_status.text:
        profile_status = f'Профиль пользователя {nickname} скрыт'
        return profile_status
    else:
        status_html = soup.find('div', class_="profile_in_game_header").text
        status = None

        if status_html == 'Currently Offline':
            status = 'Не в сети'

        if status_html == 'Currently Online':
            status = 'В сети'

        if status_html == 'Currently In-Game':
            status = 'В игре: '
            status_game = ((soup.find('div', class_="profile_in_game_name")).text.replace('\t', ''))
            status += status_game

        status_text = 'Его статус на текущий момент:\n' + status
        area = (soup.find('div', class_="responsive_count_link_area").text.replace('\t', '')
                .replace('\n', ''))
        count_of_games = f'Количество игр пользователя {nickname}: '
        count_of_awards = f'Количество наград пользователя {nickname}: '
        count_of_badges = f'Количество значков пользователя {nickname}: '
        count_of_screenshots = f'Количество скринов пользователя {nickname}: '
        count_of_reviews = f'Количество обзоров пользователя {nickname}: '

        for index in range(len(area)):

            if area[index] == 'P' and area[index + 1] == 'r' and area[index + 2] == 'o':
                for index2 in range(index + 15, len(area)):
                    try:
                        if type(int(area[index2])) == int:
                            count_of_awards += area[index2]
                    except ValueError:
                        break

            if area[index] == 'G' and area[index + 1] == 'a' and area[index + 2] == 'm':
                for index3 in range(index + 6, len(area)):
                    try:
                        if type(int(area[index3])) == int:
                            count_of_games += area[index3]
                    except ValueError:
                        break

            if area[index] == 'B' and area[index + 1] == 'a' and area[index + 2] == 'd':
                for index4 in range(index + 7, len(area)):
                    try:
                        if type(int(area[index4])) == int:
                            count_of_badges += area[index4]
                    except ValueError:
                        break

            if area[index] == 'S' and area[index + 1] == 'c' and area[index + 2] == 'r':
                for index5 in range(index + 12, len(area)):
                    try:
                        if type(int(area[index5])) == int:
                            count_of_screenshots += area[index5]
                    except ValueError:
                        break

            if area[index] == 'R' and area[index + 1] == 'e' and area[index + 2] == 'v':
                for index6 in range(index + 8, len(area)):
                    try:
                        if type(int(area[index6])) == int:
                            count_of_reviews += area[index6]
                    except ValueError:
                        break
        if 'Profile Awards' not in area:
            count_of_awards += 'Неизвестно'
        if 'Badges' not in area:
            count_of_badges += 'Неизвестно'
        if 'Screenshots' not in area:
            count_of_screenshots += 'Неизвестно'
        if 'Games' not in area:
            count_of_games += 'Неизвестно'
        if 'Reviews' not in area:
            count_of_reviews += 'Неизвестно'
        all_area = count_of_games + '\n' + count_of_reviews + '\n' + count_of_badges + '\n' + count_of_awards + '\n' + count_of_screenshots + '\n'

        recent_playtime = soup.find('div', class_="recentgame_quicklinks recentgame_recentplaytime").text.replace('\n',
                                                                                                                  '')
        recent_games_activity_name = soup.find_all('div', class_="game_name")
        recent_games_activity_info = soup.find_all('div', class_='game_info_details')
        link_for_game = list(recent_games_activity_name)
        hrefs = []
        first_link = ''
        second_link = ''
        third_link = ''
        q = -1
        for element in link_for_game:
            element = str(element)
            q += 1
            i = 0
            for index_ in range(len(element)):
                flag = False
                if element[index_] == 'h':
                    if element[index_ + 1] == 'r':
                        if element[index_ + 2] == 'e':
                            if element[index_ + 3] == 'f':
                                if i != 0:
                                    break
                                for index1_ in range(index_ + 4, len(element)):
                                    if i == 0:
                                        flag = False
                                        i += 1
                                    if element[index1_] == '"':
                                        flag = True
                                        continue
                                    if element[index1_] == '>':
                                        break
                                    if flag is True:
                                        if q == 0:
                                            first_link += element[index1_]
                                        if q == 1:
                                            second_link += element[index1_]
                                        if q == 2:
                                            third_link += element[index1_]

        hrefs.append(first_link)
        hrefs.append(second_link)
        hrefs.append(third_link)
        href1 = hrefs[0]
        href2 = hrefs[1]
        href3 = hrefs[2]

        if recent_games_activity_name is not None:
            first_game_name = recent_games_activity_name[0].text
            second_game_name = recent_games_activity_name[1].text
            third_game_name = recent_games_activity_name[2].text

            first_game_info = str(recent_games_activity_info[0]).replace('\t', '').replace('/div', '').replace(
                '<div class="game_info_details">\n', '').replace('<br/>', '').replace('<>', '').replace('hrs on record',
                                                                                                        'часов всего').replace(
                'last played on', 'Последний запуск').replace('Currently In-Game', 'В игре')
            second_game_info = str(recent_games_activity_info[1]).replace('\t', '').replace('/div', '').replace(
                '<div class="game_info_details">\n', '').replace('<br/>', '').replace('<>', '').replace('hrs on record',
                                                                                                        'часов всего').replace(
                'last played on', 'Последний запуск').replace('Currently In-Game', 'В игре')
            third_game_info = str(recent_games_activity_info[2]).replace('\t', '').replace('/div', '').replace(
                '<div class="game_info_details">\n', '').replace('<br/>', '').replace('<>', '').replace('hrs on record',
                                                                                                        'часов всего').replace(
                'last played on', 'Последний запуск').replace('Currently In-Game', 'В игре')

            recent_playtime = recent_playtime.replace('hours past', 'часов за последние').replace('weeks', 'недели')

            all_information_about_recent_game = ('Недавняя активность:\n'
                                                 f'{recent_playtime}\n\n'
                                                 f'{first_game_name}\n'
                                                 f'{first_game_info}\n'
                                                 f'{href1}\n\n'
                                                 f'{second_game_name}\n'
                                                 f'{second_game_info}\n'
                                                 f'{href2}\n\n'
                                                 f'{third_game_name}\n'
                                                 f'{third_game_info}\n'
                                                 f'{href3}'
                                                 )
        else:
            all_information_about_recent_game = 'Недавняя активность неизвестна'

        all_information_about_user = [f'Информация о пользователе:\n',
                                      f'1. Никнейм: {nickname}\n',
                                      f'{player_level}\n\n'
                                      f'2. {status_text}\n\n',
                                      f'3. {all_area}\n\n'
                                      f'4. {all_information_about_recent_game}']
        return ''.join(all_information_about_user)


@log
def wish_game(chat_id, name=None, json_input=None, json_output=None, delete=None):
    empty = False
    chat_id = str(chat_id)

    with open('steam/jsons/wishlist.json', 'r') as f:
        new_dic = {'information': {str(chat_id): [name]}}

        try:
            data_json = json.load(f)
        except JSONDecodeError:
            empty = True

    if json_input is True:
        if empty is True:
            json.dumps(new_dic)
            with open('steam/jsons/wishlist.json', 'w') as ff:
                json.dump(new_dic, ff, indent=2)
            return f'{name} успешно добавлена в ваш список желаемого'

        else:
            info = data_json.get('information')

            if info.get(str(chat_id)) is None:
                dic = {str(chat_id): [name]}
                info.update(dic)

                gen = {'information': info}
                json.dumps(gen)

                with open('steam/jsons/wishlist.json', 'w') as fff:
                    json.dump(gen, fff, indent=2)

                return f'{name} успешно добавлена в ваш список желаемого'

            else:
                spisochek = info.get(str(chat_id))
                if len(spisochek) >= 35:
                    return 'В списке может находится только 35 игр'
                if name not in spisochek:
                    spisochek.append(name)
                    newer_dic = {chat_id: spisochek}

                    info.pop(chat_id)
                    info.update(newer_dic)

                    gen = {'information': info}
                    json.dumps(gen)

                    with open('steam/jsons/wishlist.json', 'w') as ff:
                        json.dump(gen, ff, indent=2)

                    return f'{name} успешно добавлена в ваш список желаемого'
                else:
                    return f'{name} уже находится в вашем списке желаемого'

    if json_output is True:

        if empty is True:
            return 'Ваш список желаемого пуст'

        info = data_json.get('information')
        user = info.get(chat_id)
        if user is None or user == []:
            return 'Ваш список желаемого пуст'

        q = 0
        out = ''
        for i in user:
            q += 1
            out += f'{q}. {i}\n'

        return 'Ваш список желаемых игр:\n' + out

    if delete is True:
        if empty is True:
            return 'Ваш список желаемого пуст'

        info = data_json.get('information')
        user = info.get(chat_id)

        if user is None:
            return 'Ваш список желаемого пуст'

        if name not in user and name != 'all':
            return 'Игра не найдена в списке'

        if name != 'all':
            user.pop(user.index(name))

        else:
            user = []

        new_dic1 = {chat_id: user}
        info.pop(chat_id)
        info.update(new_dic1)
        gen = {'information': info}
        json.dumps(gen)

        with open('steam/jsons/wishlist.json', 'w') as fff:
            json.dump(gen, fff, indent=2)

        if name != 'all':
            return f'{name} удалена из списка желаемого'

        else:
            return 'Список желаемого очищен'


@log
def wish_processing():
    data = {}
    with open('steam/jsons/wishlist.json', 'r') as f:
        try:
            data_json = json.load(f)
        except JSONDecodeError:
            return False

    info = data_json.get('information')
    for key in info:
        for value in info[key]:
            check = game_info(games_href(value), only_price=True)

            if check is True:
                new_sp = data.get(int(key))
                if new_sp is not None:
                    new_sp.append(value)
                    new_dict = {int(key): new_sp}
                else:
                    new_dict = {int(key): [value]}
                data.update(new_dict)
    new_info = info
    spisok = []

    for key in data:
        names = data[key]
        key = str(key)
        for name in names:
            spisok = new_info.get(key)
            if name in spisok:
                spisok.pop(spisok.index(name))

        new_info.pop(key)
        new_dict1 = {key: spisok}
        new_info.update(new_dict1)

    gen = {'information': new_info}
    json.dumps(gen)

    with open('steam/jsons/wishlist.json', 'w') as ff:
        json.dump(gen, ff, indent=2)

    return data
