import sys
from PyQt5.QtWidgets import QApplication
from view.login import LoginWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建并显示登录窗口
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
