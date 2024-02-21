import time
import requests
from userMainDataVK import user_empty, take_user_id, take_user_data, take_user_domain


def take_user_subscriptions_data(domain):  # работает с url, id и доменом
    if ('https://vk.com/' in domain) or ('vk_tes.com/' in domain):
        domain = domain.split('/')[-1]
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"
    version = 5.131
    fields = 'users, groups'
    base_data = take_user_data(domain)
    user_id = take_user_id(base_data)
    count = 100
    extended = 1
    src = requests.get('https://api.vk.com/method/users.getSubscriptions',
                        params={
                            'user_id': user_id,
                            'fields': fields,
                            'access_token': token,
                            'extended': extended,
                            'v': version,
                            'count': count
                        }
                        )
    time.sleep(0.5)
    data = src.json()
    return data


def take_user_groups(data):
    group_list = 'нет данных'
    try:
        if data['response']['count'] != 0:
            group_list = ''
            for i in data['response']['items']:
                group_list += ('  ' + i['name'] + ' - ' + 'https://vk.com/' + i['screen_name'] + '\n')
        else:
            group_list = 'нет данных'
    except KeyError:
        pass

    try:
        if data['error']['error_msg'] == 'This profile is private':
            group_list = 'Невозможно получить данные. Профиль закрыт.'
    except KeyError:
        pass
    return group_list


def take_user_group_url(data):
    items = data['response']['items']
    all_groups_url = []
    try:
        for i in items:
            if i['screen_name'] == f'club{i["id"]}':
                url = f'https://vk.com/public{i["id"]}'
            else:
                url = f'https://vk.com/{i["screen_name"]}'
            all_groups_url.append(url)
    except KeyError:
        pass
    return all_groups_url


def take_user_group_url_name(data):
    items = data['response']['items']
    all_groups_url = []
    try:
        for i in items:
            if i['screen_name'] == f'club{i["id"]}':
                url = f'https://vk.com/public{i["id"]} - {i["name"]}'
            else:
                url = f'https://vk.com/{i["screen_name"]} - {i["name"]}'
            all_groups_url.append(url)
    except KeyError:
        pass
    return sorted(all_groups_url, key=len)


def info_collection(data, domain):
    temp_data = take_user_data(domain)
    output_info = f'Подписки пользователя https://vk.com/{take_user_domain(temp_data)}:\n'
    output_info += take_user_groups(data)
    return output_info


def print_info(info, domain):
    print(info_collection(info, domain))


def main():
    user = input('Пользователь ВКонтакте: ')
    try:
        data = take_user_subscriptions_data(user)
        if user_empty(data):
            print()
            print_info(data, user)
            print('Печать данных завершена!')
        else:
            print(f'Пользователя с таким id не существует!')
    except...:
        print(f'Ошибка! Невозможно получить данные.')

