import time
import requests
from userMainDataVK import take_user_data, take_user_city
from groupMainDataVK import take_group_id, take_group_data, take_count_of_followers


def take_group_followers_data(domain):  # работает с url, id и доменом
    if ('https://vk.com/' in domain) or ('vk_tes.com/' in domain):
        domain = domain.split('/')[-1]
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"
    version = 5.131
    fields = 'users, groups'
    base_data = take_group_data(domain)
    group_id = take_group_id(base_data)
    count = 100
    offset = 0
    range_ = take_count_of_followers(take_group_data(domain))

    while offset < range_:
        src = requests.get('https://api.vk.com/method/groups.getMembers',
                            params={
                                'group_id': group_id,
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
        offset += 100


def take_group_followers_url_name(domain):
    data = take_group_followers_data(domain)
    try:
        for items in data:
            for item in items:
                url = f'Страница: https://vk.com/id{item["id"]}\nИмя: {item["first_name"]} {item["last_name"]}'
                link = f'id{item["id"]}'
                city = f'Город: {take_user_city(take_user_data(link))}'
                yield url, city
    except KeyError:
        pass
