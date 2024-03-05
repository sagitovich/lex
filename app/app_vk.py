import os
import sys
sys.path.insert(0, 'C:\\Users\\lmuru\\PycharmProjects\\lex\\vk_lex')

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QDate, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget

from vk_lex.postsInfo import return_posts
from vk_lex.getUserFriends import take_friends_info
from vk_lex.getGroupFollowers import take_group_followers_url_name
from vk_lex.userMainDataVK import return_all_user_info, take_user_data, user_empty
from vk_lex.userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url_name
from vk_lex.getCommentsFromGroup import return_comments_group_no_filter, return_comments_group_filter
from vk_lex.groupMainDataVK import return_all_group_main_data, group_empty, take_group_data, group_is_open


# noinspection PyUnresolvedReferences
class vk_Functional(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('vkFunctional_.ui', self)
        self.setWindowTitle('VK-ФУНКЦИИ')

        # Предполагая, что info является QStackedWidget
        self.info = self.findChild(QStackedWidget, 'stackedWidget')
        self.layout = QtWidgets.QVBoxLayout(self.info)

        self.mainUser_btn.clicked.connect(self.mainUser_open)
        self.friendUser_btn.clicked.connect(self.friendUser_open)
        self.subscrUser_btn.clicked.connect(self.subscrUser_open)
        self.postsUser_btn.clicked.connect(self.postsUser_open)
        self.commUser_btn.clicked.connect(self.commUser_open)

        self.mainGroup_btn.clicked.connect(self.mainGroup_open)
        self.followersGroup_btn.clicked.connect(self.followersGroup_open)
        self.postsGroup_btn.clicked.connect(self.postsGroup_open)
        self.commGroup_btn.clicked.connect(self.groupAllComm_open)

    def mainUser_open(self):
        user_main = vk_UserMain(self)
        self.info.addWidget(user_main)
        self.info.setCurrentWidget(user_main)

    def friendUser_open(self):
        user_friend = vk_UserFriends(self)
        self.info.addWidget(user_friend)
        self.info.setCurrentWidget(user_friend)

    def subscrUser_open(self):
        user_subscr = vk_UserSubscriptions(self)
        self.info.addWidget(user_subscr)
        self.info.setCurrentWidget(user_subscr)

    def postsUser_open(self):
        user_posts = vk_UserPosts(self)
        self.info.addWidget(user_posts)
        self.info.setCurrentWidget(user_posts)

    def commUser_open(self):
        user_comm = vk_UserInGroupComm(self)
        self.info.addWidget(user_comm)
        self.info.setCurrentWidget(user_comm)

    def mainGroup_open(self):
        group_main = vk_GroupMain(self)
        self.info.addWidget(group_main)
        self.info.setCurrentWidget(group_main)

    def followersGroup_open(self):
        group_followers = vk_GroupFollowers(self)
        self.info.addWidget(group_followers)
        self.info.setCurrentWidget(group_followers)

    def postsGroup_open(self):
        group_posts = vk_GroupPosts(self)
        self.info.addWidget(group_posts)
        self.info.setCurrentWidget(group_posts)

    def groupAllComm_open(self):
        group_comm = vk_GroupAllComments(self)
        self.info.addWidget(group_comm)
        self.info.setCurrentWidget(group_comm)


# noinspection PyUnresolvedReferences
class vk_UserMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserMain_.ui', self)
        self.setWindowTitle('VK-ПОЛЬЗОВАТЕЛЬ-ОСНОВНОЕ')

        self.update_info.clicked.connect(self.click)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.click()

    def click(self):
        name = self.parent_window.input_url_user.text()
        if name != '':
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
        else:
            self.main_info.setText('')
            self.error_msg.setText('')

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserFriends(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserFriends_.ui', self)
        self.setWindowTitle('VK-ПОЛЬЗОВАТЕЛЬ-ДРУЗЬЯ')

        self.update_info.clicked.connect(self.click)
        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)
        self.click()

    def click(self):
        name = self.parent_window.input_url_user.text()
        if name != '':
            try:
                result = take_friends_info(name)
                text = ''
                for line in result:
                    for i in line:
                        text += (i + '\n')
                    text += (68 * '-' + '\n')
                self.error_msg.setText('')
                self.friends_info.setText(text)  # Устанавливаем текст для QLabel, а не для QScrollArea

            except (KeyError, IndexError, TypeError):
                self.friends_info.setText('')  # очищаем scrollArea
                text = 'страница не найдена или закрыта'
                self.error_msg.setText(text)
        else:
            self.friends_info.setText('')
            self.error_msg.setText('')

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserSubscriptions(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserSubscr_.ui', self)
        self.setWindowTitle('VK-ПОЛЬЗОВАТЕЛЬ-ПОДПИСКИ')

        self.update_info.clicked.connect(self.click)
        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)
        self.click()

    def click(self):
        name = self.parent_window.input_url_user.text()
        if name != '':
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
        else:
            self.subscr_info.setText('')
            self.error_msg.setText('')

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_Posts_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, domain, start_date_, end_date_):
        super().__init__()
        self.domain = domain
        self.start_date = start_date_
        self.end_date = end_date_
        self.is_paused = False

    def run(self):
        result = return_posts(self.domain, self.start_date, self.end_date)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (68 * '-' + '\n')
            self.data_ready.emit(text)
            if self.is_paused:
                return
        self.loading_finished.emit()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        self.start()


# noinspection PyUnresolvedReferences
class vk_UserPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.vk_Posts_Writer = None
        uic.loadUi('vkUserPosts_.ui', self)

        self.old_date.setDate(QDate.currentDate().addMonths(-1))
        self.cur_date.setDate(QDate.currentDate())

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        # self.click()

    def click(self):

        if self.vk_Posts_Writer is not None and self.vk_Posts_Writer.is_paused:
            self.vk_Posts_Writer = None

        name = self.parent_window.input_url_user.text()

        date1 = QDateTime(self.old_date.date())
        date2 = QDateTime(self.cur_date.date())
        # Конвертировать QDateTime в unix timestamp
        start_date = date1.toSecsSinceEpoch()
        end_date = date2.toSecsSinceEpoch()
        cur_date = QDate.currentDate()

        if name != '':
            self.error_msg.setText('')
            self.posts_info.setText('')
            if ((start_date <= QDateTime(cur_date).toSecsSinceEpoch()) and
                    (end_date <= QDateTime(cur_date).toSecsSinceEpoch())):

                if (not name) or (user_empty(take_user_data(name)) is False):
                    self.posts_info.setText('')
                    self.error_msg.setText('неверный домен или url страницы')
                else:
                    self.error_msg.setText('')
                    self.vk_Posts_Writer = vk_Posts_Writer(name, start_date, end_date)
                    self.vk_Posts_Writer.data_ready.connect(self.update_label)
                    self.vk_Posts_Writer.loading_finished.connect(self.loading_finished)
                    self.vk_Posts_Writer.start()
                    self.error_msg.setText('идёт получение...')
            else:
                self.posts_info.setText('')
                self.error_msg.setText('неверный временной диапазон')
        else:
            self.posts_info.setText('')
            self.error_msg.setText('введите пользователя')

    def update_label(self, text):
        scrollbar = self.posts_info.verticalScrollBar()
        scroll_position = scrollbar.value()  # сохраняем текущую позицию прокрутки
        self.posts_info.setText(text)
        scrollbar.setValue(scroll_position)  # восстанавливаем позицию прокрутки

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_Posts_Writer is not None:  # Добавить проверку на None
            if not self.vk_Posts_Writer.is_paused:
                self.vk_Posts_Writer.pause()
                self.error_msg.setText("сбор остановлен")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_UserInGroupComm_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, group_domain_, user_domain_, start_date_, end_date_):
        super().__init__()
        self.group_domain = group_domain_
        self.user_domain = user_domain_
        self.start_date = start_date_
        self.end_date = end_date_
        self.is_paused = False

    def run(self):
        result = return_comments_group_filter(self.group_domain, self.user_domain, self.start_date, self.end_date)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (68 * '-' + '\n')
            self.data_ready.emit(text)
            if self.is_paused:
                return
        self.loading_finished.emit()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        self.start()


# noinspection PyUnresolvedReferences
class vk_UserInGroupComm(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.vk_UserInGroupComm = None
        uic.loadUi('vkGroupComm_.ui', self)

        self.old_date.setDate(QDate.currentDate().addMonths(-1))
        self.cur_date.setDate(QDate.currentDate())

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

    def click(self):

        group = self.parent_window.input_url_group.text()
        user = self.parent_window.input_url_user.text()
        date1 = QDateTime(self.old_date.date())
        date2 = QDateTime(self.cur_date.date())

        # Конвертировать QDateTime в unix timestamp
        start_date = date1.toSecsSinceEpoch()
        end_date = date2.toSecsSinceEpoch()
        cur_date = QDate.currentDate()

        if user != '':
            if group != '':
                self.error_msg.setText('')
                self.comm_info.setText('')
                if ((start_date <= QDateTime(cur_date).toSecsSinceEpoch()) and
                        (end_date <= QDateTime(cur_date).toSecsSinceEpoch())):
                    if user_empty(take_user_data(user)):
                        if group_empty(take_group_data(group)):
                            if group_is_open(take_group_data(group)):
                                self.error_msg.setText('')
                                self.vk_UserInGroupComm = vk_UserInGroupComm_Writer(group, user, start_date, end_date)
                                self.vk_UserInGroupComm.data_ready.connect(self.update_label)
                                self.vk_UserInGroupComm.loading_finished.connect(self.loading_finished)
                                self.vk_UserInGroupComm.start()
                                self.error_msg.setText('идёт получение...')
                            else:
                                self.comm_info.setText('')
                                self.error_msg.setText('группа закрыта')
                        else:
                            self.comm_info.setText('')
                            self.error_msg.setText('сообщества не существует')
                    else:
                        self.comm_info.setText('')
                        self.error_msg.setText('пользователя не существует')
                else:
                    self.comm_info.setText('')
                    self.error_msg.setText('неверный временной диапазон')
            else:
                self.comm_info.setText('')
                self.error_msg.setText('введите сообщество')
        else:
            self.comm_info.setText('')
            self.error_msg.setText('введите пользователя')

    def update_label(self, text):
        scrollbar = self.comm_info.verticalScrollBar()
        scroll_position = scrollbar.value()  # сохраняем текущую позицию прокрутки
        self.comm_info.setText(text)
        scrollbar.setValue(scroll_position)  # восстанавливаем позицию прокрутки

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_UserInGroupComm is not None:  # Добавить проверку на None
            if self.vk_UserInGroupComm.is_paused:
                self.vk_UserInGroupComm.resume()
                self.pause_btn.setText("Пауза")
            else:
                self.vk_UserInGroupComm.pause()
                self.pause_btn.setText("Пуск")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkGroupMain_.ui', self)
        self.setWindowTitle('VK-СООБЩЕСТВО-ОСНОВНОЕ')

        self.update_info.clicked.connect(self.click)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.click()

    def click(self):
        name = self.parent_window.input_url_group.text()
        if name != '':
            try:
                result = return_all_group_main_data(name)
                text = ''
                for i in result:
                    text += i
                self.error_msg.setText('')
                self.main_info.setText(text)

            except (KeyError, IndexError, TypeError):
                self.main_info.setText('')
                text = 'сообщество не найдено или недоступно'
                self.error_msg.setText(text)
        else:
            self.main_info.setText('')
            self.error_msg.setText('')

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
        self.is_paused = False

    def run(self):
        result = take_group_followers_url_name(self.domain)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (68 * '-' + '\n')
            self.data_ready.emit(text)
            if self.is_paused:
                return
        self.loading_finished.emit()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        self.start()


# noinspection PyUnresolvedReferences
class vk_GroupFollowers(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkGroupFollowers_.ui', self)
        self.vk_GroupFollowers_Writer = self
        self.setWindowTitle('VK-СООБЩЕСТВО-ПОДПИСЧИКИ')

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.click()

    def click(self):
        name = self.parent_window.input_url_group.text()
        if name != '':
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
        else:
            self.followers_info.setText('')
            self.error_msg.setText('')

    def update_label(self, text):
        scrollbar = self.followers_info.verticalScrollBar()
        scroll_position = scrollbar.value()  # сохраняем текущую позицию прокрутки
        self.followers_info.setText(text)
        scrollbar.setValue(scroll_position)  # восстанавливаем позицию прокрутки

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_GroupFollowers_Writer.is_paused:
            self.vk_GroupFollowers_Writer.resume()
            self.pause_btn.setText("Пауза")
        else:
            self.vk_GroupFollowers_Writer.pause()
            self.pause_btn.setText("Пуск")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.vk_Posts_Writer = None
        uic.loadUi('vkGroupPosts_.ui', self)
        self.setWindowTitle('VK-СООБЩЕСТВО-ЗАПИСИ')

        self.old_date.setDate(QDate.currentDate().addMonths(-1))
        self.cur_date.setDate(QDate.currentDate())

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

    def click(self):

        if self.vk_Posts_Writer is not None and self.vk_Posts_Writer.is_paused:
            self.vk_Posts_Writer = None

        name = self.parent_window.input_url_group.text()

        date1 = QDateTime(self.old_date.date())
        date2 = QDateTime(self.cur_date.date())
        # Конвертировать QDateTime в unix timestamp
        start_date = date1.toSecsSinceEpoch()
        end_date = date2.toSecsSinceEpoch()
        cur_date = QDate.currentDate()

        if name != '':
            self.error_msg.setText('')
            self.posts_info.setText('')
            if ((start_date <= QDateTime(cur_date).toSecsSinceEpoch()) and
                    (end_date <= QDateTime(cur_date).toSecsSinceEpoch())):

                if (not name) or (group_empty(take_group_data(name)) is False):
                    self.posts_info.setText('')
                    self.error_msg.setText('неверный домен или url группы')
                elif not group_is_open(take_group_data(name)):
                    self.posts_info.setText('')
                    self.error_msg.setText('группа закрыта')
                else:
                    self.error_msg.setText('')
                    self.vk_Posts_Writer = vk_Posts_Writer(name, start_date, end_date)
                    self.vk_Posts_Writer.data_ready.connect(self.update_label)
                    self.vk_Posts_Writer.loading_finished.connect(self.loading_finished)
                    self.vk_Posts_Writer.start()
                    self.error_msg.setText('идёт получение...')
            else:
                self.posts_info.setText('')
                self.error_msg.setText('неверный временной диапазон')
        else:
            self.posts_info.setText('')
            self.error_msg.setText('введите сообщество')

    def update_label(self, text):
        scrollbar = self.posts_info.verticalScrollBar()
        scroll_position = scrollbar.value()  # сохраняем текущую позицию прокрутки
        self.posts_info.setText(text)
        scrollbar.setValue(scroll_position)  # восстанавливаем позицию прокрутки

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_Posts_Writer is not None:  # Добавить проверку на None
            if not self.vk_Posts_Writer.is_paused:
                self.vk_Posts_Writer.pause()
                self.error_msg.setText("сбор остановлен")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


# noinspection PyUnresolvedReferences
class vk_GroupAllComm_Writer(QThread):
    data_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, group_domain_, start_date_, end_date_):
        super().__init__()
        self.group_domain = group_domain_
        self.start_date = start_date_
        self.end_date = end_date_
        self.is_paused = False

    def run(self):
        result = return_comments_group_no_filter(self.group_domain, self.start_date, self.end_date)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (68 * '-' + '\n')
            self.data_ready.emit(text)
            if self.is_paused:
                return
        self.loading_finished.emit()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        self.start()


# noinspection PyUnresolvedReferences
class vk_GroupAllComments(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.vk_GroupAllComm = None
        uic.loadUi('vkGroupComm_.ui', self)

        self.old_date.setDate(QDate.currentDate().addMonths(-1))
        self.cur_date.setDate(QDate.currentDate())

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

    def click(self):

        if self.vk_GroupAllComm is not None and self.vk_GroupAllComm.is_paused:
            self.vk_GroupAllComm = None

        name = self.parent_window.input_url_group.text()
        date1 = QDateTime(self.old_date.date())
        date2 = QDateTime(self.cur_date.date())

        # Конвертировать QDateTime в unix timestamp
        start_date = date1.toSecsSinceEpoch()
        end_date = date2.toSecsSinceEpoch()
        cur_date = QDate.currentDate()

        if name != '':
            self.error_msg.setText('')
            self.comm_info.setText('')
            if ((start_date <= QDateTime(cur_date).toSecsSinceEpoch()) and
                    (end_date <= QDateTime(cur_date).toSecsSinceEpoch())):

                if (not name) or (group_empty(take_group_data(name)) is False):
                    self.comm_info.setText('')
                    self.error_msg.setText('неверный домен или url группы')
                elif not group_is_open(take_group_data(name)):
                    self.comm_info.setText('')
                    self.error_msg.setText('группа закрыта')
                else:
                    self.error_msg.setText('')
                    self.vk_GroupAllComm = vk_GroupAllComm_Writer(name, start_date, end_date)
                    self.vk_GroupAllComm.data_ready.connect(self.update_label)
                    self.vk_GroupAllComm.loading_finished.connect(self.loading_finished)
                    self.vk_GroupAllComm.start()
                    self.error_msg.setText('идёт получение...')
            else:
                self.comm_info.setText('')
                self.error_msg.setText('неверный временной диапазон')
        else:
            self.comm_info.setText('')
            self.error_msg.setText('введите сообщество')

    def update_label(self, text):
        scrollbar = self.comm_info.verticalScrollBar()
        scroll_position = scrollbar.value()  # сохраняем текущую позицию прокрутки
        self.comm_info.setText(text)
        scrollbar.setValue(scroll_position)  # восстанавливаем позицию прокрутки

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_GroupAllComm is not None:  # Добавить проверку на None
            if not self.vk_GroupAllComm.is_paused:
                self.vk_GroupAllComm.pause()
                self.error_msg.setText("сбор остановлен")

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication([])
    run = vk_Functional()
    run.show()
    app.exec_()


if __name__ == "__main__":
    main()
