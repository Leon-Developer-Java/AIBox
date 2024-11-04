import sys

from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
from view.login import *
from view.login_v2 import *
from view.main_window import *
from PyQt5 import QtCore
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.ui = Ui_Form()
        self.ui = Ui_Login_v2()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(5, 5)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.left_login_window.setGraphicsEffect(self.shadow)


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

    # 事件过滤器函数
    def eventFilter(self, source, event):
        if source == self.topWidget:  # 检查事件是否来自 Top 小部件
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.isDragging = True
                    self.dragStartPosition = event.globalPos() - self.frameGeometry().topLeft()
                    event.accept()
                    return True
            elif event.type() == QEvent.MouseMove:
                if self.isDragging:
                    self.move(event.globalPos() - self.dragStartPosition)
                    event.accept()
                    return True
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.isDragging = False
                    event.accept()
                    return True

        # 对于不是 Top 小部件的事件，或者我们不关心的事件类型，调用基类的 eventFilter
        return super().eventFilter(source, event)

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        # 获取顶部窗口部件后，将顶部窗口设置为按住可移动
        self.topWidget = self.ui.TopFrame # 获取顶部窗口部件
        self.topWidget.installEventFilter(self) # 安装事件过滤器
        self.isDragging = False
        self.dragStartPosition = QPoint()

        # 设置窗口阴影效果
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self) # 创建阴影效果对象
        self.shadow.setOffset(0, 5) # 设置阴影偏移量
        self.shadow.setBlurRadius(10) # 设置阴影模糊度
        self.shadow.setColor(QtCore.Qt.black) # 设置阴影颜色
        self.ui.MainFrame.setGraphicsEffect(self.shadow) # 设置窗口阴影效果



        # 添加toolbutton点击事件，并初始化第一个按钮处于点击状态
        self.ui.SystemInfo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.SystemInfo.setChecked(True)
        self.ui.AI.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.Key.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))



        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
