import requests
import time
from userMainDataVK import take_user_data, take_user_id


def take_friends_data(domain):
    if domain.startswith('https://vk.com/'):
        domain = domain.split('/')[-1]
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"
    version = 5.131
    fields = 'bdate, city, domain, contacts, site, sex'  # имя, фамилия, дата рождения, город, номер телефона, сайт, пол
    fields += ', has_photo, photo_id'

    src = requests.get('https://api.vk.com/method/friends.get',
                       params={
                           'user_id': take_user_id(take_user_data(domain)),
                           'fields': fields,
                           'access_token': token,
                           'v': version
                       }
                       )
    time.sleep(0.5)
    data = src.json()['response']['items']
    return data


def take_friends_info(domain):
    data = take_friends_data(domain)

    for item in data:
        url = f'Страница: https://vk.com/{item["domain"]}'
        name = f'Имя: {item["first_name"]} {item["last_name"]}'
        try:
            bdate = f'Дата рождения: {item["bdate"]}'
        except KeyError:
            bdate = f'Дата рождения: нет данных'
        try:
            city = f'Город: {item["city"]["title"]}'
        except KeyError:
            city = f'Город: нет данных'
        yield [url, name, bdate, city]
