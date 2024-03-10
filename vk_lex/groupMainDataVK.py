import time
import requests
from userMainDataVK import take_user_data, take_user_domain


def take_group_data(domain):  # работает с url, id и доменом
    if ('https://vk.com/' in domain) or ('vk_tes.com/' in domain):
        domain = domain.split('/')[-1]
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"
    version = 5.131
    fields = 'activity, city, contacts, counters, country, description, links, members_count, start_date'

    src = requests.get('https://api.vk.com/method/groups.getById',
                       params={
                           'group_id': domain,
                           'fields': fields,
                           'access_token': token,
                           'v': version
                       }
                       )
    time.sleep(0.5)
    data = src.json()
    return data


def group_empty(data):
    try:
        if isinstance(data['error']['error_code'], int):
            return False
    except KeyError:
        return True


def group_is_open(data):
    try:
        if data['response'][0]['activity'] == 'Closed community':
            return False
        else:
            return True
    except KeyError:
        return True


def take_group_id(data):
    try:
        group_id = data['response'][0]['id']
    except KeyError:
        group_id = 'нет данных'
    return group_id


def take_domain_of_group(data):
    try:
        domain = data['response'][0]['screen_name']
    except KeyError:
        domain = 'нет данных'
    return domain


def make_url_to_group(data):
    domain = take_domain_of_group(data)
    url = f'https://vk.com/{domain}'
    return url


def take_name_of_group(data):
    try:
        name = data['response'][0]['name']
    except KeyError:
        name = 'нет данных'
    return name


def take_count_of_followers(data):
    try:
        cnt_followers = data['response'][0]['members_count']
    except KeyError:
        cnt_followers = 'нет данных'
    return cnt_followers


def take_city_of_group(data):
    try:
        city = data['response'][0]['city']['title']
    except KeyError:
        city = 'нет данных'
    return city


def take_country_of_group(data):
    try:
        country = data['response'][0]['country']['title']
    except KeyError:
        country = 'нет данных'
    return country


def take_contacts_of_group(data):
    try:
        contacts = ''
        items = data['response'][0]['contacts']
        for item in items:
            temp_data = take_user_data(str(item['user_id']))
            domain = take_user_domain(temp_data)
            contacts += f'  {item["desc"]} - https://vk.com/{domain}\n'
        contacts = contacts.rstrip('\n')
    except KeyError:
        contacts = 'нет данных'
    return contacts


# def return_all_group_main_data(domain):
#     try:
#         data = take_group_data(domain)
#         if group_empty(data):
#             info = ''
#             name = f'Название: {take_name_of_group(data)}'
#             followers = f'Количество подписчиков: {take_count_of_followers(data)}'
#             location = f'Местоположение: {take_country_of_group(data)}, {take_city_of_group(data)}'
#             contacts = f'Контакты: {take_contacts_of_group(data)}'
#             url = f'Ссылка на группу: {make_url_to_group(data)}'
#
#             info += (name + '\n' + followers + '\n' + location + '\n' + contacts + '\n' + url + '\n')
#             return info
#         else:
#             return False
#
#     except (KeyError, IndexError, TypeError):
#         return False


def return_all_group_main_data(domain):
    try:
        data = take_group_data(domain)
        if group_empty(data):
            group_info = {
                'name': take_name_of_group(data),
                'followers': take_count_of_followers(data),
                'location': f'{take_country_of_group(data)}, {take_city_of_group(data)}',
                'contacts': take_contacts_of_group(data),
                'url': make_url_to_group(data)
            }
            return group_info
        else:
            return False

    except (KeyError, IndexError, TypeError):
        return False


info = return_all_group_main_data('klops39')
for v in info.values():
    print(*{v})
