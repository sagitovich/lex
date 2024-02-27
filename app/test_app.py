import sys
sys.path.insert(0, '/Users/a.sagitovich/programming/BFU/lex/vk_lex')

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from vk_lex.postsInfo import return_posts
from vk_lex.getUserFriends import take_friends_info
from vk_lex.getCommentsFromGroup import return_comments_group_filter
from vk_lex.getCommentsFromUser import return_comments_user_filter
from vk_lex.userMainDataVK import return_all_user_info, user_empty, take_user_data
from vk_lex.userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url_name
from vk_lex.groupMainDataVK import return_all_group_main_data, group_empty, take_group_data, group_is_open
from vk_lex.getGroupFollowers import take_group_followers_url_name


# noinspection PyUnresolvedReferences
class lex_Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("lex")

        self.vk_window = vk_func(self)  # передайте self в качестве аргумента
        self.to_vk_btn.clicked.connect(self.open_VK)

    def open_VK(self):
        self.hide()
        self.vk_window.show()


# noinspection PyUnresolvedReferences
class vk_func(QWidget):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('vkFunctional.ui', self)
        self.setWindowTitle('lex VK-ФУНКЦИИ')

        self.main_window = main_window  # сохраните ссылку на главное окно
        self.from_vk_func_to_main_btn.clicked.connect(self.go_back)  # предполагается, что у вас есть кнопка "Назад"

        self.vk_user_main_data = vk_UserMain(self)
        self.vk_user_main_data.windowClosed.connect(self.delete_user_main_window)
        self.userMainData_btn.clicked.connect(self.open_user_main_data)

        self.vk_user_friends = vk_UserFriends(self)
        self.vk_user_friends.windowClosed.connect(self.delete_user_friends)
        self.userFriends_btn.clicked.connect(self.open_user_friends)

        self.vk_user_subscr_window = vk_UserSubscriptions(self)
        self.vk_user_subscr_window.windowClosed.connect(self.delete_subscr_window)
        self.userSubscr_btn.clicked.connect(self.open_user_subscr)

        self.vk_user_posts = vk_UserPosts(self)
        self.vk_user_posts.windowClosed.connect(self.delete_user_posts)
        self.userPosts_btn.clicked.connect(self.open_user_posts)

        self.vk_user_comm = vk_UserComments(self)
        self.vk_user_comm.windowClosed.connect(self.delete_user_comm)
        self.userComm_btn.clicked.connect(self.open_user_comm)

        self.vk_group_main_data = vk_GroupMain(self)
        self.vk_group_main_data.windowClosed.connect(self.delete_group_main_window)
        self.gorupMainData_btn.clicked.connect(self.open_group_main_data)

        self.vk_group_followers = vk_GroupFollowers(self)
        self.vk_group_followers.windowClosed.connect(self.delete_group_followers)
        self.groupFollowers_btn.clicked.connect(self.open_group_followers)

        self.vk_group_posts_data = vk_GroupPosts(self)
        self.vk_group_posts_data.windowClosed.connect(self.delete_group_posts_window)
        self.groupPosts_btn.clicked.connect(self.open_group_posts_data)

    def go_back(self):
        self.hide()
        self.main_window.show()

    def open_user_main_data(self):
        self.hide()
        if self.vk_user_main_data is not None:
            self.vk_user_main_data.windowClosed.disconnect(self.delete_user_main_window)
        self.vk_user_main_data = vk_UserMain(self)
        self.vk_user_main_data.windowClosed.connect(self.delete_user_main_window)
        self.vk_user_main_data.show()

    def delete_user_main_window(self):
        self.vk_user_main_data = None

    def open_user_friends(self):
        self.hide()
        if self.vk_user_friends is not None:
            self.vk_user_friends.windowClosed.disconnect(self.delete_user_friends)
        self.vk_user_friends = vk_UserFriends(self)
        self.vk_user_friends.windowClosed.connect(self.delete_user_friends)
        self.vk_user_friends.show()

    def delete_user_friends(self):
        self.vk_user_friends = None

    def open_user_subscr(self):
        self.hide()
        if self.vk_user_subscr_window is not None:
            self.vk_user_subscr_window.windowClosed.disconnect(self.delete_subscr_window)
        self.vk_user_subscr_window = vk_UserSubscriptions(self)
        self.vk_user_subscr_window.windowClosed.connect(self.delete_subscr_window)
        self.vk_user_subscr_window.show()

    def delete_subscr_window(self):
        self.vk_user_subscr_window = None

    def open_user_posts(self):
        self.hide()
        if self.vk_user_posts is not None:
            self.vk_user_posts.windowClosed.disconnect(self.delete_user_posts)
        self.vk_user_posts = vk_UserPosts(self)
        self.vk_user_posts.windowClosed.connect(self.delete_user_posts)
        self.vk_user_posts.show()

    def delete_user_posts(self):
        self.vk_user_posts = None

    def open_user_comm(self):
        self.hide()
        if self.vk_user_comm is not None:
            self.vk_user_comm.windowClosed.disconnect(self.delete_user_comm)
        self.vk_user_comm = vk_UserComments(self)
        self.vk_user_comm.windowClosed.connect(self.delete_user_comm)
        self.vk_user_comm.show()

    def delete_user_comm(self):
        self.vk_user_comm = None

    def open_group_main_data(self):
        self.hide()
        if self.vk_group_main_data is not None:
            self.vk_group_main_data.windowClosed.disconnect(self.delete_group_main_window)
        self.vk_group_main_data = vk_GroupMain(self)
        self.vk_group_main_data.windowClosed.connect(self.delete_group_main_window)
        self.vk_group_main_data.show()

    def delete_group_main_window(self):
        self.vk_group_main_data = None

    def open_group_followers(self):
        self.hide()
        if self.vk_group_followers is not None:
            self.vk_group_followers.windowClosed.disconnect(self.delete_group_followers)
        self.vk_group_followers = vk_GroupFollowers(self)
        self.vk_group_followers.windowClosed.connect(self.delete_group_followers)
        self.vk_group_followers.show()

    def delete_group_followers(self):
        self.vk_group_followers = None

    def open_group_posts_data(self):
        self.hide()
        if self.vk_group_posts_data is not None:
            self.vk_group_posts_data.windowClosed.disconnect(self.delete_group_posts_window)
        self.vk_group_posts_data = vk_GroupPosts(self)
        self.vk_group_posts_data.windowClosed.connect(self.delete_group_posts_window)
        self.vk_group_posts_data.show()

    def delete_group_posts_window(self):
        self.vk_group_posts_data = None


# noinspection PyUnresolvedReferences
class vk_UserMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserMain.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ОСНОВНОЕ')

        self.check_user.clicked.connect(self.click)

        self.parent_window = parent_window
        self.from_user_main_to_vk_func_btn.clicked.connect(self.go_back)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        try:
            result = return_all_user_info(name)
            text = ''
            for i in result:
                text += (i + '\n')
            self.error_msg.setText('')
            self.main_info.setText(text)  # Устанавливаем текст для QLabel, а не для QScrollArea

        except (KeyError, IndexError, TypeError):
            self.main_info.setText('')  # очищаем scrollArea
            text = 'страница не найдена или закрыта'
            self.error_msg.setText(text)

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserFriends(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserFriends.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ДРУЗЬЯ')

        self.check_user.clicked.connect(self.click)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        try:
            result = take_friends_info(name)
            text = ''
            for line in result:
                for i in line:
                    text += (i + '\n')
                text += (96 * '-' + '\n')
            self.error_msg.setText('')
            self.friends_info.setText(text)  # Устанавливаем текст для QLabel, а не для QScrollArea

        except (KeyError, IndexError, TypeError):
            self.friends_info.setText('')  # очищаем scrollArea
            text = 'страница не найдена или закрыта'
            self.error_msg.setText(text)

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserSubscriptions(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserSubscr.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ПОДПИСКИ')

        self.check_user.clicked.connect(self.click)

        self.parent_window = parent_window
        self.from_subscr_to_vk_func_btn.clicked.connect(self.go_back)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        try:
            result = take_user_group_url_name(take_user_subscriptions_data(name))
            text = ''
            for i in result:
                text += (i + '\n')
            self.error_msg.setText('')
            self.subscr_info.setText(text)  # Устанавливаем текст для QLabel, а не для QScrollArea

        except (KeyError, IndexError, TypeError):
            self.subscr_info.setText('')  # очищаем scrollArea
            text = 'страница не найдена или закрыта'
            self.error_msg.setText(text)

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_Posts_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, domain, days):
        super().__init__()
        self.domain = domain
        self.days = days

    def run(self):
        result = return_posts(self.domain, self.days)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (96 * '-' + '\n')
            self.data_ready.emit(text)
        self.loading_finished.emit()


# noinspection PyUnresolvedReferences
class vk_UserPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.VK_Posts_Writer = (self, self)
        uic.loadUi('vkUserPosts.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ЗАПИСИ')

        self.parent_window = parent_window
        self.from_user_posts_to_vk_func_btn.clicked.connect(self.go_back)

        self.check_posts.clicked.connect(self.click)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        days = self.day_input.text()  # Получим количество дней
        self.error_msg.setText('')
        self.posts_info.setText('')
        try:
            days = int(days)
            if (not name) or (user_empty(take_user_data(name)) is False):
                self.posts_info.setText('')
                self.error_msg.setText('неверный домен или url страницы')

            elif days > 1100:
                self.posts_info.setText('')
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.VK_Posts_Writer = vk_Posts_Writer(name, days)
                self.VK_Posts_Writer.data_ready.connect(self.update_label)
                self.VK_Posts_Writer.loading_finished.connect(self.loading_finished)
                self.VK_Posts_Writer.start()
                self.error_msg.setText('идёт получение...')

        except (ValueError, TypeError):
            self.posts_info.setText('')
            self.error_msg.setText('неверный временной диапазон')

    def update_label(self, text):
        self.posts_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserCommGroup_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, group_domain, user_check, days):
        super().__init__()
        self.group_domain = group_domain
        self.user_check = user_check
        self.days = days

    def run(self):
        result = return_comments_group_filter(self.group_domain, self.user_check, self.days)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (96 * '-' + '\n')
            self.data_ready.emit(text)
        self.loading_finished.emit()


# noinspection PyUnresolvedReferences
class vk_UserCommUser_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, user_domain, user_check, days):
        super().__init__()
        self.user_domain = user_domain
        self.user_check = user_check
        self.days = days

    def run(self):
        result = return_comments_user_filter(self.user_domain, self.user_check, self.days)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (96 * '-' + '\n')
            self.data_ready.emit(text)
        self.loading_finished.emit()


# noinspection PyUnresolvedReferences
class vk_UserComments(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserCommOptions.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-КОММЕНТАРИИ')

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.user_domain = self.input_url.text()    # запомним того, кого проверяем

        self.vk_user_comm_user = vk_UserCommUser(self)
        self.vk_user_comm_user.windowClosed.connect(self.delete_user_comm_user)
        self.one_user_btn.clicked.connect(self.open_user_comm_user)

        self.vk_user_comm_group = vk_UserCommGroup(self)
        self.vk_user_comm_group.windowClosed.connect(self.delete_user_comm_group)
        self.one_group_btn.clicked.connect(self.open_user_comm_group)

    def open_user_comm_user(self):
        self.user_domain = self.input_url.text()  # запомним того, кого проверяем
        if not self.user_domain:
            text = 'нет ссылки на проверяемого'
            self.error_msg.setText(text)
        elif user_empty(take_user_data(self.user_domain)) is False:
            text = 'пользователя не существует'
            self.error_msg.setText(text)
        else:
            self.hide()
            if self.vk_user_comm_user is not None:
                self.vk_user_comm_user.windowClosed.disconnect(self.delete_user_comm_user)
            self.vk_user_comm_user = vk_UserCommUser(self)
            self.vk_user_comm_user.windowClosed.connect(self.delete_user_comm_user)
            self.vk_user_comm_user.show()

    def delete_user_comm_user(self):
        self.vk_user_comm_user = None

    def open_user_comm_group(self):
        self.user_domain = self.input_url.text()  # запомним того, кого проверяем
        if not self.user_domain:
            text = 'нет ссылки на проверяемого'
            self.error_msg.setText(text)
        elif user_empty(take_user_data(self.user_domain)) is False:
            text = 'пользователя не существует'
            self.error_msg.setText(text)
        else:
            self.hide()
            if self.vk_user_comm_group is not None:
                self.vk_user_comm_group.windowClosed.disconnect(self.delete_user_comm_group)
            self.vk_user_comm_group = vk_UserCommGroup(self)
            self.vk_user_comm_group.windowClosed.connect(self.delete_user_comm_group)
            self.vk_user_comm_group.show()

    def delete_user_comm_group(self):
        self.vk_user_comm_group = None

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserCommUser(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.VK_UserCommUser_Writer = (self, self, self)
        uic.loadUi('vkUserCommUser.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-КОММЕНТАРИИ')

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.user_who_check.setText(self.parent_window.user_domain)
        self.check_comm.clicked.connect(self.click)

    def click(self):
        user = self.input_url.text()  # Получим текст из поля ввода
        user_check = self.user_who_check.toPlainText()
        days = self.day_input.text()  # Получим количество дней
        self.error_msg.setText('')
        self.comm_info.setText('')
        try:
            days = int(days)
            if not user:
                self.comm_info.setText('')
                self.error_msg.setText('не введён домен или url страницы')
            elif user_empty(take_user_data(user)) is False:
                self.comm_info.setText('')
                self.error_msg.setText('пользователя не существует')
            # elif group_is_open(take_group_data(group)) is False:
            #     self.comm_info.setText('')
                self.error_msg.setText('страница закрыта')
            elif days > 1100:
                self.comm_info.setText('')
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.VK_UserCommUser_Writer = vk_UserCommUser_Writer(user, user_check, days)
                self.VK_UserCommUser_Writer.data_ready.connect(self.update_label)
                self.VK_UserCommUser_Writer.loading_finished.connect(self.loading_finished)
                self.VK_UserCommUser_Writer.start()
                self.error_msg.setText('идёт получение...')

        except (ValueError, TypeError):
            self.comm_info.setText('')
            self.error_msg.setText('неверный временной диапазон')

    def update_label(self, text):
        self.comm_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserCommGroup(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.VK_UserCommGroup_Writer = (self, self, self)
        uic.loadUi('vkUserCommGroup.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-КОММЕНТАРИИ')

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.user_who_check.setText(self.parent_window.user_domain)
        self.check_comm.clicked.connect(self.click)

    def click(self):
        group = self.input_url.text()  # Получим текст из поля ввода
        user_check = self.user_who_check.toPlainText()
        days = self.day_input.text()  # Получим количество дней
        self.error_msg.setText('')
        self.comm_info.setText('')
        try:
            days = int(days)
            if not group:
                self.comm_info.setText('')
                self.error_msg.setText('не введён домен или url страницы')
            elif group_empty(take_group_data(group)) is False:
                self.comm_info.setText('')
                self.error_msg.setText('сообщества не существует')
            elif group_is_open(take_group_data(group)) is False:
                self.comm_info.setText('')
                self.error_msg.setText('сообщество закрыто')
            elif days > 1100:
                self.comm_info.setText('')
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.VK_UserCommGroup_Writer = vk_UserCommGroup_Writer(group, user_check, days)
                self.VK_UserCommGroup_Writer.data_ready.connect(self.update_label)
                self.VK_UserCommGroup_Writer.loading_finished.connect(self.loading_finished)
                self.VK_UserCommGroup_Writer.start()
                self.error_msg.setText('идёт получение...')

        except (ValueError, TypeError):
            self.comm_info.setText('')
            self.error_msg.setText('неверный временной диапазон')

    def update_label(self, text):
        self.comm_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkGroupMain.ui', self)
        self.setWindowTitle('lex VK-СООБЩЕСТВО')

        self.check_group.clicked.connect(self.click)

        self.parent_window = parent_window
        self.from_group_main_to_vk_func_btn.clicked.connect(self.go_back)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        try:
            result = return_all_group_main_data(name)
            text = ''
            for i in result:
                text += i
            self.error_msg.setText('')
            self.main_info.setText(text)  # Устанавливаем текст для QLabel, а не для QScrollArea

        except (KeyError, IndexError, TypeError):
            self.main_info.setText('')  # очищаем scrollArea
            text = 'сообщество не найдено или недоступно'
            self.error_msg.setText(text)

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupFollowers_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        result = take_group_followers_url_name(self.domain)
        text = ''
        for line in result:
            text += (line + '\n' + (96 * '-') + '\n')
            self.data_ready.emit(text)
        self.loading_finished.emit()


# noinspection PyUnresolvedReferences
class vk_GroupFollowers(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkGroupFollowers.ui', self)
        self.vk_GroupFollowers_Writer = self
        self.setWindowTitle('lex VK-СООБЩЕСТВО-ПОДПИСЧИКИ')

        self.check_user.clicked.connect(self.click)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        if not group_empty(take_group_data(name)):
            self.followers_info.setText('')
            text = 'сообщества не существует'
            self.error_msg.setText(text)
        elif group_is_open(take_group_data(name)) is False:
            self.followers_info.setText('')
            text = 'невозможно узнать подписчиков'
            self.error_msg.setText(text)
        else:
            self.error_msg.setText('')
            self.vk_GroupFollowers_Writer = vk_GroupFollowers_Writer(name)
            self.vk_GroupFollowers_Writer.data_ready.connect(self.update_label)
            self.vk_GroupFollowers_Writer.loading_finished.connect(self.loading_finished)
            self.vk_GroupFollowers_Writer.start()
            self.error_msg.setText('идёт получение...')

    def update_label(self, text):
        self.followers_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.vk_Post_Writer = (self, self)
        uic.loadUi('vkGroupPosts.ui', self)
        self.setWindowTitle('lex VK-СООБЩЕСТВО-ЗАПИСИ')

        self.parent_window = parent_window
        self.from_group_posts_to_vk_func_btn.clicked.connect(self.go_back)

        self.check_posts.clicked.connect(self.click)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        days = self.day_input.text()  # Получим количество дней
        self.error_msg.setText('')
        self.posts_info.setText('')
        try:
            days = int(days)
            if (not name) or (group_empty(take_group_data(name)) is False):
                self.posts_info.setText('')  # очищаем scrollArea
                self.error_msg.setText('неверный домен или url группы')

            elif days > 1100:
                self.posts_info.setText('')  # очищаем scrollArea
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.vk_Post_Writer = vk_Posts_Writer(name, days)
                self.vk_Post_Writer.data_ready.connect(self.update_label)
                self.vk_Post_Writer.loading_finished.connect(self.loading_finished)
                self.vk_Post_Writer.start()
                self.error_msg.setText('идёт получение...')

        except (ValueError, TypeError):
            self.posts_info.setText('')  # очищаем scrollArea
            self.error_msg.setText('неверный временной диапазон')

    def update_label(self, text):
        self.posts_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


app = QApplication([])
run = lex_Main()
run.show()
app.exec_()
