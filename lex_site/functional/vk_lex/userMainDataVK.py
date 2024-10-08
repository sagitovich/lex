# -*-  -*-  -*- #
import time
import requests
from keys_vk import get_token


def take_user_data(domain):
    if domain.startswith('https://vk.com/'):
        domain = domain.split('/')[-1]
    token = get_token()
    version = 5.131
    fields = 'bdate, city, domain, contacts, site, sex'

    src = requests.get('https://api.vk.com/method/users.get',
                       params={
                           'user_id': domain,
                           'fields': fields,
                           'access_token': token,
                           'v': version
                       }
                       )
    time.sleep(0.1)
    data = src.json()
    return data


def user_empty(data):
    if data['response'].__len__() == 0:
        return False
    else:
        return True


def take_user_id(data):
    user_id = 'нет данных'
    if (data['response'].__len__() != 0) and (data['response'][0]['sex'] != 0):  # ЕСЛИ АККАУНТ СУЩЕСТВУЕТ
        user_id = str(data['response'][0]['id'])
    return user_id


def take_user_domain(data):
    user_domain = 'нет данных'
    if (data['response'].__len__() != 0) and (data['response'][0]['sex'] != 0):  # ЕСЛИ АККАУНТ СУЩЕСТВУЕТ
        user_domain = str(data['response'][0]['domain'])
    return user_domain


def take_user_first_name(data):
    f_name = 'нет данных'
    if (data['response'].__len__() != 0) and (data['response'][0]['sex'] != 0):
        f_name = data['response'][0]['first_name']
    return f_name


def take_user_last_name(data):
    l_name = 'нет данных'
    if (data['response'].__len__() != 0) and (data['response'][0]['sex'] != 0):
        l_name = data['response'][0]['last_name']
    return l_name


def take_user_birth_date(data):
    try:
        if data['response'][0]['bdate']:
            b_date = data['response'][0]['bdate']
        else:
            b_date = 'нет данных'
    except KeyError:
        b_date = 'нет данных'
    return b_date


def take_user_sex(data):
    try:
        if data['response'][0]['sex'] != '':
            if data['response'][0]['sex'] == 1:
                sex = 'женский'
            elif data['response'][0]['sex'] == 2:
                sex = 'мужской'
            else:
                sex = 'нет данных'
        else:
            sex = 'нет данных'
    except KeyError:
        sex = 'нет данных'
    return sex


def take_user_city(data):
    try:
        if data['response'][0]['city']['title'] != '':
            city = data['response'][0]['city']['title']
        else:
            city = 'нет данных'
    except KeyError:
        city = 'нет данных'
    return city


def take_user_mobile(data):
    try:
        if data['response'][0]['mobile_phone'] != '':
            mobile = data['response'][0]['mobile_phone']
        else:
            mobile = 'нет данных'
    except KeyError:
        mobile = 'нет данных'
    return mobile


def take_user_web_site(data):
    try:
        if data['response'][0]['site'] != '':
            site = data['response'][0]['site']
        else:
            site = 'нет данных'
    except KeyError:
        site = 'нет данных'
    return site


def return_all_user_info(domain):
    data = take_user_data(domain)
    try:
        user_info = {
            'url': f'https://vk.com/{take_user_domain(data)}',
            'name': f'{take_user_first_name(data)} {take_user_last_name(data)}',
            'bdate': take_user_birth_date(data),
            'city': take_user_city(data),
            'phone': take_user_mobile(data),
            'site': take_user_web_site(data)
        }
        return user_info

    except (IndexError, KeyError):
        return f'Пользователя https://vk.com/{domain} не существует.'

