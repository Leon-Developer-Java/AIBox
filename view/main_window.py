import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)  # 设置主窗口大小

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序实例
    main_window = MainWindow()    # 创建主窗口实例
    main_window.show()            # 显示主窗口
    sys.exit(app.exec_())          # 进入应用程序主循环
