import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow
from view.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(458, 367)  # 设置窗口大小
        self.setFixedSize(458, 367)  # 设置窗口大小为固定大小

        self.formLayoutWidget = QtWidgets.QWidget(self)  # 创建一个布局控件
        self.formLayoutWidget.setGeometry(QtCore.QRect(70, 120, 311, 111))  # 设置布局控件的位置和大小
        self.formLayoutWidget.setObjectName("formLayoutWidget")  # 设置布局控件的对象名
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setHorizontalSpacing(25)
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")

        # 用户名输入框和标签
        self.userText = QtWidgets.QLabel(self.formLayoutWidget)
        self.userText.setObjectName("userText")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.userText)
        self.userNameInput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.userNameInput.setObjectName("userNameInput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.userNameInput)

        # 密码输入框和标签
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.passwordInput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setObjectName("passwordInput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordInput)

        # 登录和重置按钮
        self.loginBtn = QtWidgets.QPushButton(self)
        self.loginBtn.setGeometry(QtCore.QRect(100, 270, 93, 28))
        self.loginBtn.setObjectName("loginBtn")
        self.resetBtn = QtWidgets.QPushButton(self)
        self.resetBtn.setGeometry(QtCore.QRect(250, 270, 93, 28))
        self.resetBtn.setObjectName("resetBtn")

        ## 绑定按钮事件
        self.resetBtn.clicked.connect(self.resetForm)
        self.loginBtn.clicked.connect(self.login)

        # 标题
        self.titleLogin = QtWidgets.QLabel(self)
        self.titleLogin.setGeometry(QtCore.QRect(110, 50, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(18)
        self.titleLogin.setFont(font)
        self.titleLogin.setObjectName("titleLogin")

        # 翻译 UI 文本
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Login"))
        self.userText.setText(_translate("Form", "USER:"))
        self.label_2.setText(_translate("Form", "PASSWORD:"))
        self.loginBtn.setText(_translate("Form", "Login"))
        self.resetBtn.setText(_translate("Form", "Reset"))
        self.titleLogin.setText(_translate("Form", "AI Algorithm Box"))

    ## 重置方法
    def resetForm(self):
        self.userNameInput.setText("")
        self.passwordInput.setText("")

    ## 登录方法
    def login(self):
        # 创建主窗口并显示
        self.main_window = MainWindow()
        self.main_window.show()

        # 关闭登录窗口
        self.close()


# 测试运行代码
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
