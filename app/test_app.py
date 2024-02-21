import sys
sys.path.insert(0, '/Users/a.sagitovich/programming/BFU/TES/vk_tes')

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from vk_tes.postsInfo import return_posts, take_page_data, check_private_page
from vk_tes.userMainDataVK import return_all_user_info, user_empty, take_user_data
from vk_tes.groupMainDataVK import return_all_group_main_data, group_empty, take_group_data
from vk_tes.userSubscriptionsVK import take_user_subscriptions_data, take_user_group_url_name


class TES_Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("TES")

        self.vk_window = TES_vk_func(self)  # передайте self в качестве аргумента
        self.to_vk_btn.clicked.connect(self.open_VK)

    def open_VK(self):
        self.hide()
        self.vk_window.show()


class TES_vk_func(QWidget):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('vkFunctional.ui', self)
        self.setWindowTitle('TES VK-ФУНКЦИИ')

        self.main_window = main_window  # сохраните ссылку на главное окно
        self.from_vk_func_to_main_btn.clicked.connect(self.go_back)  # предполагается, что у вас есть кнопка "Назад"

        self.vk_user_main_data = TES_UserMain(self)
        self.vk_user_main_data.windowClosed.connect(self.delete_user_main_window)
        self.userMainData_btn.clicked.connect(self.open_user_main_data)

        self.vk_user_subscr_window = TES_Subscriptions(self)
        self.vk_user_subscr_window.windowClosed.connect(self.delete_subscr_window)
        self.userSubscr_btn.clicked.connect(self.open_user_subscr)

        self.vk_user_posts = TES_UserPosts(self)
        self.vk_user_posts.windowClosed.connect(self.delete_user_posts)
        self.userPosts_btn.clicked.connect(self.open_user_posts)

        self.vk_user_comm = TES_UserComments(self)
        self.vk_user_comm.windowClosed.connect(self.delete_user_comm)
        self.userComm_btn.clicked.connect(self.open_user_comm)

        self.vk_group_main_data = TES_GroupMain(self)
        self.vk_group_main_data.windowClosed.connect(self.delete_group_main_window)
        self.gorupMainData_btn.clicked.connect(self.open_group_main_data)

        self.vk_group_posts_data = TES_GroupPosts(self)
        self.vk_group_posts_data.windowClosed.connect(self.delete_group_posts_window)
        self.groupPosts_btn.clicked.connect(self.open_group_posts_data)

    def go_back(self):
        self.hide()
        self.main_window.show()

    def open_user_main_data(self):
        self.hide()
        if self.vk_user_main_data is not None:
            self.vk_user_main_data.windowClosed.disconnect(self.delete_user_main_window)
        self.vk_user_main_data = TES_UserMain(self)
        self.vk_user_main_data.windowClosed.connect(self.delete_user_main_window)
        self.vk_user_main_data.show()

    def delete_user_main_window(self):
        self.vk_user_main_data = None

    def open_user_subscr(self):
        self.hide()
        if self.vk_user_subscr_window is not None:
            self.vk_user_subscr_window.windowClosed.disconnect(self.delete_subscr_window)
        self.vk_user_subscr_window = TES_Subscriptions(self)
        self.vk_user_subscr_window.windowClosed.connect(self.delete_subscr_window)
        self.vk_user_subscr_window.show()

    def delete_subscr_window(self):
        self.vk_user_subscr_window = None

    def open_user_posts(self):
        self.hide()
        if self.vk_user_posts is not None:
            self.vk_user_posts.windowClosed.disconnect(self.delete_user_posts)
        self.vk_user_posts = TES_UserPosts(self)
        self.vk_user_posts.windowClosed.connect(self.delete_user_posts)
        self.vk_user_posts.show()

    def delete_user_posts(self):
        self.vk_user_posts = None

    def open_user_comm(self):
        self.hide()
        if self.vk_user_comm is not None:
            self.vk_user_comm.windowClosed.disconnect(self.delete_user_comm)
        self.vk_user_comm = TES_UserComments(self)
        self.vk_user_comm.windowClosed.connect(self.delete_user_comm)
        self.vk_user_comm.show()

    def delete_user_comm(self):
        self.vk_user_comm = None

    def open_group_main_data(self):
        self.hide()
        if self.vk_group_main_data is not None:
            self.vk_group_main_data.windowClosed.disconnect(self.delete_group_main_window)
        self.vk_group_main_data = TES_GroupMain(self)
        self.vk_group_main_data.windowClosed.connect(self.delete_group_main_window)
        self.vk_group_main_data.show()

    def delete_group_main_window(self):
        self.vk_group_main_data = None

    def open_group_posts_data(self):
        self.hide()
        if self.vk_group_posts_data is not None:
            self.vk_group_posts_data.windowClosed.disconnect(self.delete_group_posts_window)
        self.vk_group_posts_data = TES_GroupPosts(self)
        self.vk_group_posts_data.windowClosed.connect(self.delete_group_posts_window)
        self.vk_group_posts_data.show()

    def delete_group_posts_window(self):
        self.vk_group_posts_data = None


class TES_UserMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserMain.ui', self)
        self.setWindowTitle('TES VK-ПОЛЬЗОВАТЕЛИ-ОСНОВНОЕ')

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


class TES_Subscriptions(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserSubscr.ui', self)
        self.setWindowTitle('TES VK-ПОЛЬЗОВАТЕЛИ-ПОДПИСКИ')

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


class VK_Posts_Writer(QThread):
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


class TES_UserPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.worker = (self, self)
        uic.loadUi('vkUserPosts.ui', self)
        self.setWindowTitle('TES VK-ПОЛЬЗОВАТЕЛИ-ЗАПИСИ')

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
                self.posts_info.setText('')  # очищаем scrollArea
                self.error_msg.setText('неверный домен или url страницы')

            elif days > 1100:
                self.posts_info.setText('')  # очищаем scrollArea
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.worker = VK_Posts_Writer(name, days)
                self.worker.data_ready.connect(self.update_label)
                self.worker.loading_finished.connect(self.loading_finished)
                self.worker.start()
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


class TES_UserComments(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserCommOptions.ui', self)
        self.setWindowTitle('TES VK-ПОЛЬЗОВАТЕЛИ-КОММЕНТАРИИ')

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.user_domain = self.input_url.text()    # запомним того, кого проверяем

        self.vk_user_comm_group = TES_UserCommGroup(self)
        self.vk_user_comm_group.windowClosed.connect(self.delete_user_comm_group)
        self.one_group_btn.clicked.connect(self.open_user_comm_group)

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
            self.vk_user_comm_group = TES_UserCommGroup(self)
            self.vk_user_comm_group.windowClosed.connect(self.delete_user_comm_group)
            self.vk_user_comm_group.show()

    def delete_user_comm_group(self):
        self.vk_user_comm_group = None

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


class TES_UserCommGroup(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkUserCommGroup.ui', self)
        self.setWindowTitle('TES VK-ПОЛЬЗОВАТЕЛИ-КОММЕНТАРИИ')

        self.parent_window = parent_window
        self.back_btn.clicked.connect(self.go_back)

        self.user_who_check.setText(self.parent_window.user_domain)
        self.check_comm.clicked.connect(self.click)

    def click(self):
        name = self.input_url.text()  # Получим текст из поля ввода
        days = self.day_input.text()  # Получим количество дней
        self.error_msg.setText('')
        self.comm_info.setText('')
        try:
            days = int(days)
            if not name:
                self.comm_info.setText('')
                self.error_msg.setText('не введён домен или url страницы')
            elif group_empty(take_group_data(name)) is False:
                self.comm_info.setText('')
                self.error_msg.setText('сообщества не существует')
            elif check_private_page(take_page_data(name, days)):
                self.comm_info.setText('')
                self.error_msg.setText('сообщество закрыто')
            elif days > 1100:
                self.posts_info.setText('')
                self.error_msg.setText('выберете меньший диапазон времени')
            else:
                self.error_msg.setText('')
                self.worker = VK_Posts_Writer(name, days)
                self.worker.data_ready.connect(self.update_label)
                self.worker.loading_finished.connect(self.loading_finished)
                self.worker.start()
                self.error_msg.setText('идёт получение...')

        except (ValueError, TypeError):
            self.posts_info.setText('')
            self.error_msg.setText('неверный временной диапазон')

    def go_back(self):
        self.close()
        self.parent_window.show()
        self.windowClosed.emit()


class TES_GroupMain(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        uic.loadUi('vkGroupMain.ui', self)
        self.setWindowTitle('TES VK-СООБЩЕСТВО')

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


class TES_GroupPosts(QWidget):
    windowClosed = pyqtSignal()

    def __init__(self, parent_window):
        super().__init__()
        self.worker = (self, self)
        uic.loadUi('vkGroupPosts.ui', self)
        self.setWindowTitle('TES VK-СООБЩЕСТВО-ЗАПИСИ')

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
                self.worker = VK_Posts_Writer(name, days)
                self.worker.data_ready.connect(self.update_label)
                self.worker.loading_finished.connect(self.loading_finished)
                self.worker.start()
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
run = TES_Main()
run.show()
app.exec_()
