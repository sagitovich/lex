import time
import requests
import datetime
from groupMainDataVK import take_group_data, take_group_id
from userMainDataVK import take_user_data, take_user_domain
from postsInfo import take_page_data, take_id_of_all_posts, take_count_of_comments_of_all_posts


def take_comments_g(group, post_id, value_):

    if group.startswith('https://vk.com/'):
        group = group.split('/')[-1]

    version = 5.131
    token = "4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16"

    owner_id = -1 * int(take_group_id(take_group_data(group)))

    count = 100
    offset = 0

    value = value_
    if value != 0:
        while offset < value:
            src = requests.get('https://api.vk.com/method/wall.getComments',
                                params={
                                    'owner_id': owner_id,
                                    'post_id': post_id,
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
                    yield key

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
                                for item in thread_items:
                                    yield item
                            except KeyError:
                                pass
                            thread_offset += count
                offset += count
            except KeyError:
                pass
    else:
        pass


def return_comments_group_no_filter(group, days_):
    ids = take_id_of_all_posts(take_page_data(group, days_))
    cnt = take_count_of_comments_of_all_posts(take_page_data(group, days_))

    aboba = 1
    for i, j in zip(ids, cnt):
        if j != 0:
            try:
                data = take_comments_g(group, i, j)
                for key in data:
                    user = take_user_domain(take_user_data(f'id{key["from_id"]}'))
                    date = datetime.datetime.fromtimestamp(key['date']).strftime('%d.%m.%Y %H:%M:%S')
                    text = key["text"]

                    post_id = key.get("post_id", "")
                    owner_id = key.get("owner_id", "")
                    if post_id and owner_id:
                        post = f'{group}?w=wall{owner_id}_{post_id}'
                    else:
                        post = f'{group}?w=wall{key.get("owner_id", "")}_{key.get("post_id", "")}'

                    yield [f'Автор: {user}',
                            f'Дата: {date}',
                            f'Текст: {text}',
                            f'Запись: {post}']
            except (TypeError, IndexError, KeyError):
                pass
        else:
            pass
        print(f"{aboba} запись проверена")
        aboba += 1


def return_comments_group_filter(group, users, days_):
    ids = take_id_of_all_posts(take_page_data(group, days_))
    cnt = take_count_of_comments_of_all_posts(take_page_data(group, days_))

    aboba = 1
    for i, j in zip(ids, cnt):
        if j != 0:
            try:
                data = take_comments_g(group, i, j)
                for key in data:
                    user = take_user_domain(take_user_data(f'id{key["from_id"]}'))
                    date = datetime.datetime.fromtimestamp(key['date']).strftime('%d.%m.%Y %H:%M:%S')
                    text = key["text"]

                    post_id = key.get("post_id", "")
                    owner_id = key.get("owner_id", "")
                    if post_id and owner_id:
                        post = f'{group}?w=wall{owner_id}_{post_id}'
                    else:
                        post = f'{group}?w=wall{key.get("owner_id", "")}_{key.get("post_id", "")}'

                    if user in users:
                        yield [f'Автор: {user}',
                                f'Дата: {date}',
                                f'Текст: {text}',
                                f'Запись: {post}']
                    else:
                        pass
            except (TypeError, IndexError, KeyError):
                pass
        else:
            pass
        print(f"{aboba} запись проверена")
        aboba += 1


# group_ = 'https://vk.com/ruwest39'
# list_ = ('https://vk.com/tiamat69',
#             'https://vk.com/id818854585',
#             'https://vk.com/id30859572',
#             'https://vk.com/id767350920',
#             'https://vk.com/id767350920',
#             'https://vk.com/id114081738',
#             'https://vk.com/a.a.chernikov',
#             'https://vk.com/id44519599',
#             'https://vk.com/id711060448',
#             'https://vk.com/id573137191',
#             'https://vk.com/id573137191',
#             'https://vk.com/id608473493',
#             'https://vk.com/kantt79',
#             'https://vk.com/raslena',
#             'https://vk.com/const2013',
#             'https://vk.com/id30902015')
# temp = return_comments_group_filter(group_, list_, 30)
# for item in temp:
#     print(item)
