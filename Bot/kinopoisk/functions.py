import json
import os

import requests


from bs4 import BeautifulSoup


def movie_href(movie_name):
    url = f'https://www.kinopoisk.ru/index.php?kp_query={movie_name}'

    headers = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers, json=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    html = soup.find('p', class_='name')
    if html is None:
        return False

    name = html.text
    if 'сериал' in name:
        category = 'series_'
    else:
        category = 'film_'


    html = str(html)
    href = 'https://www.kinopoisk.ru'
    flag = False
    for index in range(len(html)):
        if flag:
            break
        if html[index] == 'h':
            if html[index + 1] == 'r':
                if html[index + 2] == 'e':
                    if html[index + 3] == 'f':
                        for index1 in range(index + 4, len(html)):
                            if html[index1] == '"':
                                flag = True
                                continue
                            if html[index1] == '/' and html[index1 + 1] == 's' and html[index1 + 2] == 'r':
                                break
                            if flag is True:
                                href += html[index1]
    if category == 'series_':
        href = href.replace('film', 'series')
    if 'name' in href:
        return False
    return href + '/?utm_referrer=www.kinopoisk.ru', category


def movie_info(url, category):
    if category == 'film_':
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'yashr=1308056711739162196; _ym_uid=1739162199632805221; mobile=no; mda_exp_enabled=1; yandex_login=; i=rt9l6cN5yd+T4MRs7AKZFyXJ0a4AzUQg9X9sdl48lCA3Vw81QUG1VGqMoJ6QLKiM99AaXqjewEDqcYj9igFy4Pt8wLw=; yandexuid=2346427211709352542; my_perpages=%5B%5D; yuidss=2346427211709352542; _csrf=2e3PkZN55J-oOf70lsKErZx8; desktop_session_key=8bc2b861608a53b9ef3479c4e1afaf4017b9d83fbe24db20bb88df5744d5b12940453997e90c22341cbc7c44f890b9a974366a702d0d47f6e5053c21b3d6f01b23fa70cbe856f336c18b1c800cab09db07529906cf5c737f8f993eff5be9e395d7e80a9646a2b1322aa5f79c7748aa2f15ea05d36be931b04772f869b243c9107cdf107d81126eec3a32531ce4b9a71051b690344869ac5257c3db0f7f6229b338c516e06be75a57caca9e680f3d2a6b; desktop_session_key.sig=_hxcPFyGCyi1EHXMxxC9t_q5wdc; gdpr=0; _ym_isad=2; PHPSESSID=0639d71913d5d73405a98c2fd8ee885b; _csrf_csrf_token=e5k7j0tFCXYeJYFwBKm7GN6M0qRBiBEp6LFDvKWhqyQ; no-re-reg-required=1; _yasc=c5c8ZRC/dT2O8rvZBWo5Bo+2YYh67xDybwdOxTn8VlsQ9ho3IkAEwjTTFJfIuxEkurQ=; yp=1739341048.yu.2346427211709352542; ymex=1741846648.oyu.2346427211709352542; ya_sess_id=noauth:1739255263; sessar=1.1198.CiCMLxtvgmo-LjYtZ4jk5iiHIMuG2MBVWmlI8mEg58jmRw.wYEfb5OHeKfzI1SfCpnge6XnxbXGl_Tex6JTnRRPO8U; ys=c_chck.578514963; mda2_beacon=1739255263606; sso_status=sso.passport.yandex.ru:synchronized; initialUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; finalUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; cycada=/lGBltuKl4Aa6BxT6IuZYhGDEi26wU4MUjHeDo4cbWQ=; _ym_d=1739255300; _yasc=gOZZfnAAmMl2qpGkLfzaBgcvnTYlOetDcsdxvJdha5hzr+S8KEC+mj9h/rOkQTVAhbc=; _ym_d=1739262765; _ym_uid=1739162199632805221',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uber-trace-id': '4bb04c8f64df7279:1bff43fa7be80b11:0:1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-kl-safekids-ajax-request': 'Ajax_Request',
        'x-request-id': '1739255300393287-555800689866559812:1',
        'x-requested-with': 'XMLHttpRequest'
        }
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload, json=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        data = soup.find('script', type="application/ld+json").text
        data = json.loads(data)

        name = data.get('name')

        description = data.get('description')
        if description is None:
            description = 'Не найдено'

        dict_data = data.get('aggregateRating')
        rating = dict_data.get('ratingValue')
        rating_count = dict_data.get('ratingCount')
        if dict_data is None:
            all_rating = 'Отсутствует'
        else:
            all_rating = f'- Количество отзывов: {rating_count}\n- Оценка зрителей: {rating}/10'

        genres = ''
        genres_sp = data.get('genre')
        if genres_sp is None:
            genres = 'Не найдены'
        else:
            for genre in genres_sp:
                genres += '- ' + genre + '\n'

        content_rating = data.get('contentRating')
        if content_rating is None:
            content_rating = 'Отсутствует'

        family = str(data.get('isFamilyFriendly')).replace('False', 'Не подходит для семейного просмотра').replace('True', 'Подходит для семейного просмотра')
        if family == 'None':
            family = ''

        imdb = soup.find('span', class_='styles_valueSection__0Tcsy')
        if imdb is None:
            imdb = 'Не найдена'
        else:
            imdb = imdb.text

        sp = soup.find_all('div', class_="styles_titleDark___tfMR styles_title__b1HVo")
        if sp is None:
            director = 'Не найден'
            actors = 'Не найдены\n'
            producers = 'Не найдены\n'
        else:
            if len(sp) == 0:
                sp = soup.find_all('div', class_="styles_titleLight__HIbfT styles_title__b1HVo")

            director = ''
            for i in sp:
                if 'Режиссер' in i.text:
                    director = i.find_next().text
                    break
            if not director:
                director = 'Не найден'

            producers = ''
            for prod in sp:
                if 'Продюсер' in prod.text:
                    producers += prod.find_next().text + '\n'
                    break
            if not producers:
                producers = 'Не найдены\n'

            sp = soup.find('ul', class_='styles_list___ufg4').text
            actors = ''
            i = 0
            actor = '- '

            for symbol in sp:
                if symbol.isupper():
                    i += 1
                if i == 3:
                    actors += actor + '\n'
                    actor = '- '
                    i = 1
                actor += symbol

        time = data.get('timeRequired')
        time1 = time
        if time is None:
            all_time = 'Не найдено'
        else:
            if int(time) >= 60:
                time = f'{int(time) // 60}ч. {int(time) % 60} мин.'
            else:
                time += 'мин.'
            all_time = f'{time1} мин. = {time}'

        data_published = data.get('datePublished')
        if data_published is None:
            data_published = 'Не найдена'

        ages = soup.find('a', class_="styles_restrictionLink__iy4n9")
        if ages is None:
            ages = 'Не найден'

        image = str(soup.find('a', class_='styles_posterLink__C1HRc'))
        flag = False
        href = 'https:'

        if not f'{name}.png' in os.listdir('kinopoisk/images'):
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
            res = requests.get(href)
            with open(f'kinopoisk/images/{name}.png', 'wb') as f:
                f.write(res.content)

        return ((f'Название:\n{name}\n\n'
            f'Длительность:\n{all_time}\n\n'
            f'Рейтинг Kinopoisk:\n{all_rating}\n\n'
            f'Рейтинг {imdb}\n\n'
            f'Жанры:\n{genres}\n'
            f'Возраст: {ages.text}\n\n'
            f'{family}'),
            (f'Название:\n{name}\n\n'
            f'Описание:\n{description}\n\n'
            f'Длительность:\n{all_time}\n\n'
            f'Дата выхода:\n{data_published}г.\n\n'
            f'Рейтинг Kinopoisk:\n{all_rating}\n\n'
            f'Рейтинг {imdb}\n\n'
            f'Возрастной рейтинг:\n{content_rating}\n\n'
            f'Жанры:\n{genres}\n'
            f'Режиссер:\n{director}\n\n'
            f'Продюсеры:\n{producers}\n'
            f'Актеры:\n{actors}\n'
            f'Возраст: {ages.text}\n\n'
            f'{family}'),
            f'{name}.png')

    if category == 'series_':
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'yashr=1308056711739162196; _ym_uid=1739162199632805221; mobile=no; mda_exp_enabled=1; yandex_login=; i=rt9l6cN5yd+T4MRs7AKZFyXJ0a4AzUQg9X9sdl48lCA3Vw81QUG1VGqMoJ6QLKiM99AaXqjewEDqcYj9igFy4Pt8wLw=; yandexuid=2346427211709352542; my_perpages=%5B%5D; yuidss=2346427211709352542; _csrf=2e3PkZN55J-oOf70lsKErZx8; desktop_session_key=8bc2b861608a53b9ef3479c4e1afaf4017b9d83fbe24db20bb88df5744d5b12940453997e90c22341cbc7c44f890b9a974366a702d0d47f6e5053c21b3d6f01b23fa70cbe856f336c18b1c800cab09db07529906cf5c737f8f993eff5be9e395d7e80a9646a2b1322aa5f79c7748aa2f15ea05d36be931b04772f869b243c9107cdf107d81126eec3a32531ce4b9a71051b690344869ac5257c3db0f7f6229b338c516e06be75a57caca9e680f3d2a6b; desktop_session_key.sig=_hxcPFyGCyi1EHXMxxC9t_q5wdc; gdpr=0; _ym_isad=2; PHPSESSID=0639d71913d5d73405a98c2fd8ee885b; _csrf_csrf_token=e5k7j0tFCXYeJYFwBKm7GN6M0qRBiBEp6LFDvKWhqyQ; no-re-reg-required=1; _yasc=c5c8ZRC/dT2O8rvZBWo5Bo+2YYh67xDybwdOxTn8VlsQ9ho3IkAEwjTTFJfIuxEkurQ=; yp=1739341048.yu.2346427211709352542; ymex=1741846648.oyu.2346427211709352542; ya_sess_id=noauth:1739255263; sessar=1.1198.CiCMLxtvgmo-LjYtZ4jk5iiHIMuG2MBVWmlI8mEg58jmRw.wYEfb5OHeKfzI1SfCpnge6XnxbXGl_Tex6JTnRRPO8U; ys=c_chck.578514963; mda2_beacon=1739255263606; sso_status=sso.passport.yandex.ru:synchronized; initialUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; finalUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; cycada=/lGBltuKl4Aa6BxT6IuZYhGDEi26wU4MUjHeDo4cbWQ=; _ym_d=1739255300; _yasc=gOZZfnAAmMl2qpGkLfzaBgcvnTYlOetDcsdxvJdha5hzr+S8KEC+mj9h/rOkQTVAhbc=; _ym_d=1739262765; _ym_uid=1739162199632805221',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'uber-trace-id': '4bb04c8f64df7279:1bff43fa7be80b11:0:1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'x-kl-safekids-ajax-request': 'Ajax_Request',
            'x-request-id': '1739255300393287-555800689866559812:1',
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload, json=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        name = soup.find('h1', class_="styles_title___itJ6 styles_root__QSToS styles_root__5sqsd styles_rootInLight__juoEZ")

        years = soup.find('span', class_="styles_brackets__zRUuj")
        if years is None:
            years = ''
        else:
            years = years.text
        name = name.text.replace(' ' + years, '')

        info = soup.find_all('div', class_="styles_valueDark__BCk93 styles_value__g6yP4")
        genres = ''
        directors = ''
        producers = ''
        time = ''
        data_published = ''

        for i in info:
            if i.previous.text == 'Режиссер':
                directors = i.text
            if i.previous.text == 'Продюсер':
                producers = i.text
            if i.previous.text == 'Время серии':
                time = i.text
            if i.previous.text == 'Премьера в мире':
                data_published = i.text
            if i.previous.previous.text == 'Жанр':
                genres = i.text

        if not genres:
            genres = 'Не найдены'
        if not directors:
            directors = 'Не найдены'
        if not producers:
            producers = 'Не найдены'
        if not time:
            time = 'Неизвестно'

        imdb = soup.find('span', class_='styles_valueSection__0Tcsy')
        if imdb is None:
            imdb = 'Не найдена'
        else:
            imdb = imdb.text

        rating_kinopoisk = soup.find('span', class_="styles_ratingKpTop__84afd")
        if rating_kinopoisk is None:
            rating_kinopoisk = 'Не найден'

        sp = soup.find('ul', class_="styles_list___ufg4")
        if sp is None:
            actors = 'Не найдены'
        else:
            actors = ''
            i = 0
            actor = '- '

            for symbol in sp.text:
                if symbol.isupper():
                    i += 1
                if i == 3:
                    actors += actor + '\n'
                    actor = '- '
                    i = 1
                actor += symbol

        ages = soup.find('span', class_="styles_rootHighContrast__Bevle styles_rootHighContrastInLight__513Hu")
        if ages is None:
            ages = 'Неизвестно'
        else:
            ages = ages.text

        image = str(soup.find('a', class_='styles_posterLink__C1HRc'))
        flag = False
        href = ''

        if not f'{name}.png' in os.listdir('kinopoisk/images'):
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
            if href[:8] != 'https:':
                res = requests.get('https:' + href)
            else:
                res = requests.get(href)
            with open(f'kinopoisk/images/{name}.png', 'wb') as f:
                f.write(res.content)

        return ((f'Название:\n{name}\n\n'
                 f'Длительность серии:\n{time}\n\n'
                 f'Рейтинг Kinopoisk:\n{rating_kinopoisk}\n\n'
                 f'Рейтинг {imdb}\n\n'
                 f'Жанры:\n{genres}\n\n'
                 f'Возраст: {ages}\n\n'),
                (f'Название:\n{name}\n\n'
                 f'Длительность серии:\n{time}\n\n'
                 f'Дата выхода:\n{data_published}г.\n\n'
                 f'Рейтинг Kinopoisk: {rating_kinopoisk}\n\n'
                 f'Рейтинг {imdb}\n\n'
                 f'Жанры:\n{genres}\n\n'
                 f'Режиссер:\n{directors}\n\n'
                 f'Продюсеры:\n{producers}\n\n'
                 f'Актеры:\n{actors}\n'
                 f'Возраст: {ages}\n\n'),
                 f'{name}.png')
