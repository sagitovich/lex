import time
import requests
from keys_vk import get_token
from userMainDataVK import take_user_id, take_user_data


def take_user_subscriptions_data(domain):
    if ('https://vk.com/' in domain) or ('vk_tes.com/' in domain):
        domain = domain.split('/')[-1]
    token = get_token()
    version = 5.131
    fields = 'users, groups'
    base_data = take_user_data(domain)
    user_id = take_user_id(base_data)
    count = 100
    offset = 0
    extended = 1
    all_subscr = []

    while offset < 500:
        src = requests.get('https://api.vk.com/method/users.getSubscriptions',
                            params={
                                'user_id': user_id,
                                'fields': fields,
                                'access_token': token,
                                'extended': extended,
                                'v': version,
                                'count': count,
                                'offset': offset
                            }
                            )
        data = src.json()['response']['items']
        all_subscr.extend(data)
        offset += 100
        time.sleep(0.5)

    return all_subscr

# def take_user_groups(data):
#     group_list = 'нет данных'
#     try:
#         if data['response']['count'] != 0:
#             group_list = ''
#             for i in data['response']['items']:
#                 group_list += ('  ' + i['name'] + ' - ' + 'https://vk.com/' + i['screen_name'] + '\n')
#         else:
#             group_list = 'нет данных'
#     except KeyError:
#         pass
#
#     try:
#         if data['error']['error_msg'] == 'This profile is private':
#             group_list = 'Невозможно получить данные. Профиль закрыт.'
#     except KeyError:
#         pass
#     return group_list
#
#
# def take_user_group_url(data):
#     items = data['response']['items']
#     all_groups_url = []
#     try:
#         for i in items:
#             if i['screen_name'] == f'club{i["id"]}':
#                 url = f'https://vk.com/public{i["id"]}'
#             else:
#                 url = f'https://vk.com/{i["screen_name"]}'
#             all_groups_url.append(url)
#     except KeyError:
#         pass
#     return all_groups_url


def user_subscr(domain):
    data = take_user_subscriptions_data(domain)
    try:
        for item in data:
            if item['screen_name'] == f'club{item["id"]}':
                url = f'https://vk.com/public{item["id"]} - {item["name"]}'
            else:
                url = f'https://vk.com/{item["screen_name"]} - {item["name"]}'
            yield {
                'url': url
            }
    except KeyError:
        pass

