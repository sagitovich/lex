from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from functional.vk_lex.userMainDataVK import return_all_user_info as userMainInfo
from functional.vk_lex.userSubscriptionsVK import user_subscr as userSubscriptions
from functional.vk_lex.groupMainDataVK import return_all_group_main_data as groupMainInfo


def vk(request):
    return render(request, "index.html")


def userMain(request):
    # print("Запрос получен")
    username = request.GET.get('username', None)
    user_info = userMainInfo(username)
    data = (f'<b>Имя пользователя</b>: {user_info["name"]}<br>'
            f'<b>Дата рождения</b>: {user_info["bdate"]}<br>'
            f'<b>Город</b>: {user_info["city"]}<br>'
            f'<b>Телефон</b>: {user_info["phone"]}<br>'
            f'<b>Сайт</b>: {user_info["site"]}<br>'
            f'<b>Ссылка на страницу</b>: {user_info["url"]}')
    # print(data)
    return HttpResponse(data)


def userSubscr(request):
    username = request.GET.get('username', None)
    subscriptions = userSubscriptions(username)
    data = 'более сложный формат вывода данных.'
    print(subscriptions)
    return HttpResponse(data)


def groupMain(request):
    print("Запрос получен")
    groupname = request.GET.get('groupname', None)
    group_info = groupMainInfo(groupname)
    data = (f'<b>Название сообщества</b>: {group_info["name"]}<br>'
            f'<b>Количество подписчиков</b>: {group_info["followers"]}<br>'
            f'<b>Расположение</b>: {group_info["location"]}<br>'
            f'<b>Контакты</b>: {group_info["contacts"]}<br>'
            f'<b>Ссылка на страницу</b>: {group_info["url"]}')
    print(group_info)
    return HttpResponse(data)
