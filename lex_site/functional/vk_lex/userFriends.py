import time
import requests
from keys_vk import get_token
from userMainDataVK import take_user_data, take_user_id


def take_friends_data(domain):
    if domain.startswith('https://vk.com/'):
        domain = domain.split('/')[-1]
    token = get_token()
    version = 5.131
    fields = 'bdate, city, domain'
    count = 100
    offset = 0

    while offset < 1000:
        src = requests.get('https://api.vk.com/method/friends.get',
                           params={
                               'user_id': take_user_id(take_user_data(domain)),
                               'fields': fields,
                               'access_token': token,
                               'v': version,
                               'count': count,
                               'offset': offset
                           }
                           )
        time.sleep(0.1)
        data = src.json()['response']['items']
        yield data
        offset += count


def user_friends(domain):
    data = take_friends_data(domain)

    for element in data:
        for item in element:
            url = f'https://vk.com/{item["domain"]}'
            name = f'{item["first_name"]} {item["last_name"]}'
            try:
                bdate = f'{item["bdate"]}'
            except KeyError:
                bdate = f'нет данных'
            try:
                city = f'{item["city"]["title"]}'
            except KeyError:
                city = f'нет данных'
            yield {
                'url': url,
                'name': name,
                'bdate': bdate,
                'city': city
            }
