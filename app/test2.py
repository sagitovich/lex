import sys
sys.path.insert(0, '/Users/a.sagitovich/programming/BFU/lex/vk_lex')

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget

from vk_lex.getUserFriends import take_friends_info
from vk_lex.userMainDataVK import return_all_user_info
from vk_lex.getGroupFollowers import take_group_followers_url_name
from vk_lex.userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url_name
from vk_lex.groupMainDataVK import return_all_group_main_data, group_empty, take_group_data, group_is_open


# noinspection PyUnresolvedReferences
class vk_Functional(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('vkFunctional.ui', self)
        self.setWindowTitle('lex VK-ФУНКЦИИ')

        # Предполагая, что info является QStackedWidget
        self.info = self.findChild(QStackedWidget, 'stackedWidget')

        self.mainUser_btn.clicked.connect(self.mainUser_open)
        self.friendUser_btn.clicked.connect(self.friendUser_open)
        self.subscrUser_btn.clicked.connect(self.subscrUser_open)

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

    def run(self):
        result = take_group_followers_url_name(self.domain)
        text = ''
        for line in result:
            for i in line:
                text += (i + '\n')
            text += (68 * '-' + '\n')
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

        self.update_info.clicked.connect(self.click)

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

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


app = QApplication([])
run = vk_Functional()
run.show()
app.exec_()
