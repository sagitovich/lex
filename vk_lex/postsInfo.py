import time
import datetime
import requests
from userMainDataVK import take_user_domain, take_user_data
from groupMainDataVK import make_url_to_group, take_group_data


def take_page_data(domain, days_):
    if domain.startswith('https://vk.com/'):
        domain = domain.split('/')[-1]

    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"
    version = 5.92
    count = 50
    offset = 0

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
            if (datetime.datetime.now().date() - post_date).days <= days_:
                yield post  # возвращаем пост как только он удовлетворяет условию
            else:
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


def return_posts(domain, days_):
    try:
        data = take_page_data(domain, days_)
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

                yield [f'Дата публикации: {date}',
                       f'Ссылка на запись: {url}',
                       f'Текст: {text}',
                       f'Автор: {author}']
        except (KeyError, IndexError):
            return False
    except (KeyError, IndexError):
        return False
