from userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url
from getCommentsFromGroup import return_comments_group_filter, return_comments_group_no_filter


def return_comments_subsr_no_filter(user_):
    list_subsr = take_user_group_url(take_user_subscriptions_data(user_))
    matrix = []
    cnt = 1
    for subsr in list_subsr:
        info = return_comments_group_no_filter(subsr)
        matrix.extend(info)
        print(f'{cnt} группа проверена')
        cnt += 1
    return matrix


def return_comments_subsr_filter(user_, users_check):
    list_subsr = take_user_group_url(take_user_subscriptions_data(user_))
    matrix = []
    cnt = 1
    for subsr in list_subsr:
        info = return_comments_group_filter(subsr, users_check)
        matrix.extend(info)
        print(f'{cnt} группа проверена')
        cnt += 1
    return matrix
