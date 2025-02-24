import json

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
        category = 'series'
    else:
        category = 'film'

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
    href = href.replace('film', category)
    return href + '/?utm_referrer=www.kinopoisk.ru'


def movie_info(url, length=None):
    if url is False:
        return 'Ошибка'
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'yashr=1308056711739162196; _ym_uid=1739162199632805221; mobile=no; mda_exp_enabled=1; yandex_login=; i=rt9l6cN5yd+T4MRs7AKZFyXJ0a4AzUQg9X9sdl48lCA3Vw81QUG1VGqMoJ6QLKiM99AaXqjewEDqcYj9igFy4Pt8wLw=; yandexuid=2346427211709352542; my_perpages=%5B%5D; yuidss=2346427211709352542; _csrf=2e3PkZN55J-oOf70lsKErZx8; desktop_session_key=8bc2b861608a53b9ef3479c4e1afaf4017b9d83fbe24db20bb88df5744d5b12940453997e90c22341cbc7c44f890b9a974366a702d0d47f6e5053c21b3d6f01b23fa70cbe856f336c18b1c800cab09db07529906cf5c737f8f993eff5be9e395d7e80a9646a2b1322aa5f79c7748aa2f15ea05d36be931b04772f869b243c9107cdf107d81126eec3a32531ce4b9a71051b690344869ac5257c3db0f7f6229b338c516e06be75a57caca9e680f3d2a6b; desktop_session_key.sig=_hxcPFyGCyi1EHXMxxC9t_q5wdc; gdpr=0; _ym_isad=2; PHPSESSID=0639d71913d5d73405a98c2fd8ee885b; _csrf_csrf_token=e5k7j0tFCXYeJYFwBKm7GN6M0qRBiBEp6LFDvKWhqyQ; no-re-reg-required=1; _yasc=c5c8ZRC/dT2O8rvZBWo5Bo+2YYh67xDybwdOxTn8VlsQ9ho3IkAEwjTTFJfIuxEkurQ=; yp=1739341048.yu.2346427211709352542; ymex=1741846648.oyu.2346427211709352542; ya_sess_id=noauth:1739255263; sessar=1.1198.CiCMLxtvgmo-LjYtZ4jk5iiHIMuG2MBVWmlI8mEg58jmRw.wYEfb5OHeKfzI1SfCpnge6XnxbXGl_Tex6JTnRRPO8U; ys=c_chck.578514963; mda2_beacon=1739255263606; sso_status=sso.passport.yandex.ru:synchronized; initialUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; finalUtm={%22utm_referrer%22:%22www.kinopoisk.ru%22}; cycada=/lGBltuKl4Aa6BxT6IuZYhGDEi26wU4MUjHeDo4cbWQ=; _ym_d=1739255300; _yasc=gOZZfnAAmMl2qpGkLfzaBgcvnTYlOetDcsdxvJdha5hzr+S8KEC+mj9h/rOkQTVAhbc=; _ym_d=1739262765; _ym_uid=1739162199632805221',
    'priority': 'u=1, i',
    'referer': 'https://www.kinopoisk.ru/film/198116/?utm_referrer=www.kinopoisk.ru',
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
    if name is None:
        name = 'Отсутствует'

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

    try:
        genres = ''
        genres_sp = data.get('genre')
        for genre in genres_sp:
            genres += '- ' + genre + '\n'
    except AttributeError:
        genres = 'Отсутствует'


    content_rating = data.get('contentRating')
    if content_rating is None:
        content_rating = 'Отсутствует'

    try:
        family = str(data.get('isFamilyFriendly')).replace('False', 'Не подходит для семейного просмотра').replace('True', 'Подходит для семейного просмотра')
    except AttributeError:
        family = 'Отсутствует'

    sp = soup.find_all('div', class_="styles_titleDark___tfMR styles_title__b1HVo")
    imdb = soup.find('span', class_='styles_valueSection__0Tcsy')
    if imdb is None:
        imdb = 'Не найдена'
    else:
        imdb = imdb.text
    producers = ''
    for prod in sp:
        if 'Продюсер' in prod.text:
            producers += prod.findNext().text + '\n'

    director = ''
    for i in sp:
        if 'Режиссер' in i.text:
            director = i.findNext().text
    if not director:
        director = 'Не найден'

    actors = ''
    sp = soup.find_all('li', class_='styles_root__vKDSE styles_rootInLight__EFZzH')
    for actor in sp:
        actors += '- ' + actor.text + '\n'
    if actors == '':
        actors = 'Не найдены'

    time = data.get('timeRequired')
    time1 = time
    if time is None:
        time = 'Не найдено'
    else:
        if int(time) >= 60:
            time = f'{int(time) // 60}ч. {int(time) % 60} мин.'
        else:
            time += 'мин.'

    data_published = data.get('datePublished')
    if data_published is None:
        data_published = 'Не найдено'

    image = soup.find('a', class_='styles_posterLink__C1HRc')
    print(image.get('data-tid'))
    return image
    if length is True:
        return (f'Название:\n{name}\n\n'
            f'Описание:\n{description}\n\n'
            f'Длительность:\n{time1} мин. = {time}\n\n'
            f'Дата выхода:\n{data_published}г.\n\n'
            f'Рейтинг зрителей:\n{all_rating}\n\n'
            f'Рейтинг {imdb}\n\n'
            f'Возрастной рейтинг:\n{content_rating}\n\n'
            f'Жанры:\n{genres}\n'
            f'Режиссер:\n{director}\n\n'
            f'Продюсеры:\n{producers}\n'
            f'Актеры:\n{actors}\n'
            f'{family}')

    return (f'Название:\n{name}\n\n'
     f'Длительность:\n{time1} мин. = {time}\n\n'
     f'Рейтинг {imdb}\n\n'
     f'Жанры:\n{genres}\n'
     f'{family}')

print(movie_info(movie_href('Слоник')))