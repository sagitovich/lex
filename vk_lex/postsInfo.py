import time
import datetime
import requests
from keys_vk import get_token
from userMainDataVK import take_user_domain, take_user_data
from groupMainDataVK import make_url_to_group, take_group_data


def take_page_data(domain, start_date, end_date):
    if domain.startswith('https://vk.com/'):
        domain = domain.split('/')[-1]

    token = get_token()
    version = 5.92
    count = 50
    offset = 0

    start_date_ = datetime.datetime.fromtimestamp(start_date).date()
    end_date_ = datetime.datetime.fromtimestamp(end_date).date()

    while offset < 100_000_000:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        if not data:
            break  # Прекратить, если нет новых записей
        offset += 50
        flag_end = False
        for post in data:
            post_date = datetime.datetime.fromtimestamp(post['date']).date()
            if start_date_ <= post_date <= end_date_:
                yield post  # возвращаем пост как только он удовлетворяет условию
            else:
                if (start_date_ <= post_date) and (post_date >= end_date_):
                    pass
                elif (start_date_ >= post_date) and (post_date <= end_date_):
                    flag_end = True
        if flag_end:  # если ничего не добавилось в all_posts -> следующие посты слишком старые
            break
        time.sleep(0.1)


def take_id_of_all_posts(data):
    all_id = []
    for item in data:
        all_id.append(item['id'])
    return all_id


def take_count_of_comments_of_all_posts(data):
    all_comm = []
    try:
        for item in data:
            all_comm.append(item['comments']['count'])
        return all_comm
    except KeyError:
        return 'комментарии скрыты'


def return_posts(domain, start_date, end_date):
    try:
        data = take_page_data(domain, start_date, end_date)
        try:
            for post in data:
                date = datetime.datetime.fromtimestamp(post['date']).strftime('%d.%m.%Y %H:%M:%S')
                url = f"https://vk.com/{str(domain)}?w=wall{str(post['owner_id'])}_{str(post['id'])}"

                if (post['text'] == '') and (post['attachments'][0]['type'] == 'photo'):
                    text = '*Фотография*'
                elif (post['text'] == '') and (post['attachments'][0]['type'] == 'video'):
                    text = '*Видео*'
                else:
                    text = post['text']

                if post['owner_id'] > 0:  # если страница пользователя
                    try:
                        author = f"https://vk.com/{str(take_user_domain(take_user_data(domain)))}"
                    except (KeyError, IndexError, TypeError):
                        author = f"https://vk.com/id{str(post['from_id'])}"
                else:  # если страница сообщества
                    try:
                        author = f"{make_url_to_group((take_group_data(domain)))}"
                    except (KeyError, IndexError, TypeError):
                        author = f"https://vk.com/id{str(post['from_id'])}"

                yield {
                    'author': {author},
                    'date': {date},
                    'text': {text},
                    'url': {url}
                }

        except (KeyError, IndexError):
            return False
    except (KeyError, IndexError):
        return False
