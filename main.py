import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from view.login import *
from view.main_window import *
from PyQt5 import QtCore
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setOffset(5, 5)
        # self.shadow.setBlurRadius(10)
        # self.shadow.setColor(QtCore.Qt.black)
        # self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.loginBtn.clicked.connect(self.login)
        self.ui.resetBtn.clicked.connect(self.reset)

        self.show()

    def login(self):
        if (self.ui.userNameInput.text() == "admin" and self.ui.passwordInput.text() == "123456"):
            print("登录成功")
            self.win = MainWindow()
            self.close()

        else:
            print("登录失败")
            self.ui.userNameInput.setText('')
            self.ui.passwordInput.setText('')

    def reset(self):
        self.ui.userNameInput.clear()
        self.ui.passwordInput.clear()



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setOffset(5, 5)
        # self.shadow.setBlurRadius(10)
        # self.shadow.setColor(QtCore.Qt.black)
        # self.ui.frame.setGraphicsEffect(self.shadow)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())
