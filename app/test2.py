import os
import sys
sys.path.insert(0, '/Users/a.sagitovich/programming/BFU/lex/vk_lex')

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget

from vk_lex.postsInfo import return_posts
from vk_lex.getUserFriends import take_friends_info
from vk_lex.userMainDataVK import return_all_user_info
from vk_lex.getGroupFollowers import take_group_followers_url_name
from vk_lex.userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url_name
from vk_lex.groupMainDataVK import return_all_group_main_data, group_empty, take_group_data, group_is_open


# noinspection PyUnresolvedReferences
class vk_Functional(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('vkFunctional_.ui', self)
        self.setWindowTitle('lex VK-ФУНКЦИИ')

        # Предполагая, что info является QStackedWidget
        self.info = self.findChild(QStackedWidget, 'stackedWidget')
        self.layout = QtWidgets.QVBoxLayout(self.info)

        self.mainUser_btn.clicked.connect(self.mainUser_open)
        self.friendUser_btn.clicked.connect(self.friendUser_open)
        self.subscrUser_btn.clicked.connect(self.subscrUser_open)
        self.postsUser_btn.clicked.connect(self.postsUser_open)

        self.mainGroup_btn.clicked.connect(self.mainGroup_open)
        self.followersGroup_btn.clicked.connect(self.followersGroup_open)

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

    def mainGroup_open(self):
        group_main = vk_GroupMain(self)
        self.info.addWidget(group_main)
        self.info.setCurrentWidget(group_main)

    def followersGroup_open(self):
        group_followers = vk_GroupFollowers(self)
        self.info.addWidget(group_followers)
        self.info.setCurrentWidget(group_followers)


# noinspection PyUnresolvedReferences
class vk_UserMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserMain.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ОСНОВНОЕ')

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
        uic.loadUi('vkUserFriends.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ДРУЗЬЯ')

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
        uic.loadUi('vkUserSubscr.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ПОДПИСКИ')

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

    def __init__(self, domain, days):
        super().__init__()
        self.domain = domain
        self.days = days
        self.is_paused = False

    def run(self):
        result = return_posts(self.domain, self.days)
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
        self.VK_Posts_Writer = (self, self)
        uic.loadUi('vkUserPosts.ui', self)
        self.setWindowTitle('lex VK-ПОЛЬЗОВАТЕЛИ-ЗАПИСИ')

        self.old_date.setDate(QDate.currentDate().addMonths(-1))
        self.cur_date.setDate(QDate.currentDate())

        self.update_info.clicked.connect(self.click)
        self.pause_btn.clicked.connect(self.pause_or_resume)

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.click()

    def click(self):
        name = self.parent_window.input_url_group.text()
        days = 1
        if name != '':
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
        else:
            self.posts_info.setText('')
            self.error_msg.setText('')

    def update_label(self, text):
        self.posts_info.setText(text)

    def loading_finished(self):
        self.error_msg.setText("готово")

    def pause_or_resume(self):
        if self.vk_Posts_Writer.is_paused:
            self.vk_Posts_Writer.resume()
            self.pause_btn.setText("Пауза")
        else:
            self.vk_Posts_Writer.pause()
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
        uic.loadUi('vkGroupMain.ui', self)
        self.setWindowTitle('lex VK-СООБЩЕСТВО')

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
        uic.loadUi('vkGroupFollowers.ui', self)
        self.vk_GroupFollowers_Writer = self
        self.setWindowTitle('lex VK-СООБЩЕСТВО-ПОДПИСЧИКИ')

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
        self.followers_info.setText(text)

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


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication([])
    run = vk_Functional()
    run.show()
    app.exec_()


if __name__ == "__main__":
    main()
