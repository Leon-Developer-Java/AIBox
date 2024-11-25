
import sys

from PyQt5.QtCore import Qt, QPoint, QEvent, QSize
from PyQt5.QtGui import QIcon, QPixmap,  QStandardItem, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from view.login_v2 import *
from view.main_window import *
from PyQt5 import QtCore
import utils.methods as methods


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


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scaleFactor = 1.15  # 缩放因子

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.scaleFactor, self.scaleFactor)  # 放大
        else:
            self.scale(1 / self.scaleFactor, 1 / self.scaleFactor)  # 缩小



class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale_factor = 1.15  # 缩放因子

    def wheelEvent(self, event):
        # 禁止默认的滚轮事件触发滚动行为
        if event.angleDelta().y() > 0:  # 滚轮向上
            self.scale(self.scale_factor, self.scale_factor)
        else:  # 滚轮向下
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)
        event.accept()

class MainWindow(QMainWindow):

    def open_image(self):
        # 打开图像文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.custom_view.scene().clear()  # 清空之前加载的内容
                item = QGraphicsPixmapItem(pixmap)
                self.custom_view.scene().addItem(item)

                # 设置场景矩形，适应图像大小
                self.custom_view.scene().setSceneRect(0, 0, pixmap.width(), pixmap.height())

                # 计算缩放因子，使图像高度与 origin_image 高度一致（略小）
                view_height = self.custom_view.viewport().height()
                scale_factor = (view_height * 0.92) / pixmap.height()  # 高度稍小一些，避免竖向滚动条

                # 应用缩放因子
                self.custom_view.resetTransform()  # 重置之前的缩放
                self.custom_view.scale(scale_factor, scale_factor)

                # 将视图移动到图像最左侧
                self.custom_view.horizontalScrollBar().setValue(0)  # 水平滚动条移到最左

                # 启用按钮
                self.ui.start_reg.setEnabled(True)
                self.ui.output_word.setEnabled(True)




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
        self.topWidget = self.ui.TopFrame  # 获取顶部窗口部件
        self.topWidget.installEventFilter(self)  # 安装事件过滤器
        self.isDragging = False
        self.dragStartPosition = QPoint()

        # 设置窗口阴影
        methods.shadow_fun(self)



        # 添加toolbutton点击事件，并初始化第一个按钮处于点击状态
        self.ui.AI.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.AI.setChecked(True)
        self.ui.SystemInfo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.Key.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        # 用自定义的 QGraphicsView 替换原有的 origin_image
        self.custom_view = CustomGraphicsView(self.ui.origin_image.parent())
        self.custom_view.setScene(QGraphicsScene(self.custom_view))
        self.ui.verticalLayout_4.replaceWidget(self.ui.origin_image, self.custom_view)
        self.ui.origin_image.deleteLater()  # 删除原有的控件

        # 绑定打开图像按钮
        self.ui.openFile.clicked.connect(self.open_image)



        # 窗体显示
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
