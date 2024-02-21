import time
import requests
import datetime
import numpy as np
from userMainDataVK import take_user_data, take_user_domain, take_user_id
from postsInfo import take_page_data, take_id_of_all_posts, take_count_of_comments_of_all_posts


def take_comments_u(user_page, post_id, value_):

    if user_page.startswith('https://vk.com/'):
        user_page = user_page.split('/')[-1]

    version = 5.131
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"

    owner_id = int(take_user_id(take_user_data(user_page)))

    count = 100
    offset = 0
    all_comments = []

    value = value_
    if value != 0:
        while offset < value:
            # меньше количества комментов к проверяемой записи
            src = requests.get('https://api.vk.com/method/wall.getComments',
                                params={
                                    'owner_id': owner_id,   # сообщество
                                    'post_id': post_id,    # запись
                                    'count': count,
                                    'offset': offset,
                                    'extended': 1,
                                    'fields': 'thread_items',
                                    'access_token': token,
                                    'v': version
                                }
                                )
            try:
                time.sleep(0.1)
                data = src.json()['response']['items']

                for key in data:
                    all_comments.append(key)

                    # Проверяем наличие ответов на комментарий
                    if 'thread' in key:
                        thread_count = key['thread']['count']
                        thread_offset = 0

                        while thread_offset < thread_count:
                            thread_src = requests.get('https://api.vk.com/method/wall.getComments',
                                                        params={
                                                            'owner_id': owner_id,
                                                            'post_id': post_id,
                                                            'comment_id': key['id'],
                                                            'count': count,
                                                            'offset': thread_offset,
                                                            'extended': 1,
                                                            'fields': 'items',
                                                            'access_token': token,
                                                            'v': version
                                                        }
                                                        )
                            try:
                                time.sleep(0.1)
                                thread_items = thread_src.json()['response']['items']
                                all_comments.extend(thread_items)
                            except KeyError:
                                pass
                            thread_offset += count
                offset += count
            except KeyError:
                pass
        return all_comments
    else:
        return False


def return_comments_user_no_filter(user_):
    info_list = []
    ids = take_id_of_all_posts(take_page_data(user_))
    cnt = take_count_of_comments_of_all_posts(take_page_data(user_))

    aboba = 1
    for i, j in zip(ids, cnt):
        if j != 0:
            try:
                data = take_comments_u(user_, i, j)
                for key in data:
                    user = take_user_domain(take_user_data(f'id{key["from_id"]}'))
                    date = datetime.datetime.fromtimestamp(key['date']).strftime('%d.%m.%Y %H:%M:%S')
                    text = key["text"]

                    # Проверяем наличие ключа 'owner_id'
                    post_id = key.get("post_id", "")
                    owner_id = key.get("owner_id", "")
                    if post_id and owner_id:
                        post = f'{user}?w=wall{owner_id}_{post_id}'
                    else:
                        post = f'{user}?w=wall{key.get("owner_id", "")}_{key.get("post_id", "")}'

                    info_list.append([user, date, text, post])
                    # print([user, date, text, post])
            except (TypeError, IndexError, KeyError) as e:
                print(f"Error processing comments for post {i}: {e}")
        else:
            pass
        print(f"{aboba} запись проверена")
        aboba += 1
    info_array = np.array(info_list, dtype=object)
    return info_array


def return_comments_user_filter(user_, users_check=()):
    info_list = []
    ids = take_id_of_all_posts(take_page_data(user_))
    cnt = take_count_of_comments_of_all_posts(take_page_data(user_))

    aboba = 1
    for i, j in zip(ids, cnt):
        if j != 0:
            try:
                data = take_comments_u(user_, i, j)
                for key in data:
                    user = take_user_domain(take_user_data(f'id{key["from_id"]}'))
                    date = datetime.datetime.fromtimestamp(key['date']).strftime('%d.%m.%Y %H:%M:%S')
                    text = key["text"]

                    # Проверяем наличие ключа 'owner_id'
                    post_id = key.get("post_id", "")
                    owner_id = key.get("owner_id", "")
                    if post_id and owner_id:
                        post = f'https://vl.com/{user}?w=wall{owner_id}_{post_id}'
                    else:
                        post = f'https://vl.com/{user}?w=wall{key.get("owner_id", "")}_{key.get("post_id", "")}'
                    if user in users_check:
                        info_list.append([user, date, text, post])
                        # print([user, date, text, post])
                    else:
                        pass
            except (TypeError, IndexError, KeyError) as e:
                print(f"Error processing comments for post {i}: {e}")
        else:
            pass
        print(f"{aboba} запись проверена")
        aboba += 1
    info_array = np.array(info_list, dtype=object)
    return info_array
