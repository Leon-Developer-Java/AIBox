import os
import sys

from PyQt5.QtCore import Qt, QPoint, QEvent, QSize
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListView, QGraphicsScene, QGraphicsPixmapItem
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

    def open_images(self):
        # 打开文件选择对话框，选择多张图像文件
        file_paths, _ = QFileDialog.getOpenFileNames(self, "打开图像", "", "Image Files (*.png *.jpg *.bmp)")

        # 检查是否选择了文件
        if file_paths:
            # 清空当前的图像模型
            self.model.clear()

            # 设置图像显示的统一尺寸
            icon_size = QSize(125, 125)  # 设置一个固定的尺寸，比如100x100

            # 遍历选中的文件路径
            for file_path in file_paths:
                # 加载图像并强制缩放为固定大小
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                # 创建 QStandardItem
                item = QStandardItem()
                item.setIcon(QIcon(pixmap))  # 设置图像为图标
                item.setText(file_path.split("/")[-1])  # 显示文件名
                item.setEditable(False)  # 禁用编辑功能

                # 将项添加到模型
                self.model.appendRow(item)

            # 统一设置 QListView 图标大小
            self.ui.image_listView.setIconSize(icon_size)

            # 设置模型到 QListView
            self.ui.image_listView.setModel(self.model)

            # 监听项选择变化
            # 通过lambda传递额外的参数
            self.ui.image_listView.selectionModel().selectionChanged.connect(
                lambda selected, deselected: self.on_item_click(selected, deselected, file_paths)
            )

    # 点击事件的处理函数
    def on_item_click(self, selected, deselected, file_paths):
        # 获取选中的项
        selected_indexes = selected.indexes()
        if selected_indexes:
            # 获取第一个选中的项
            selected_item = selected_indexes[0]
            # 获取该项的文件路径
            file_path = file_paths[self.model.itemFromIndex(selected_item).row()]

            # 加载图像
            pixmap = QPixmap(file_path)

            # 获取视图的尺寸，用于缩放图像
            view_size = self.ui.origin_image.viewport().size()  # 获取显示区域的大小

            # 缩放图像以保持比例并适应视图
            scaled_pixmap = pixmap.scaled(view_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            # 创建 QGraphicsScene 和 QGraphicsPixmapItem
            scene = QGraphicsScene()

            # 设置原始图像（origin_image）
            origin_image_item = QGraphicsPixmapItem(scaled_pixmap)
            scene.addItem(origin_image_item)

            # 清空当前的 QGraphicsScene
            if self.ui.origin_image.scene():
                self.ui.origin_image.scene().clear()  # 清空场景内容

            # 将新的 scene 设置到 origin_image QGraphicsView
            self.ui.origin_image.setScene(scene)
            self.ui.origin_image.setRenderHint(QPainter.Antialiasing)  # 可选，启用抗锯齿效果

            # 如果有需要处理图像，可以在这里进行图像处理（示例中只是复制）
            processed_pixmap = pixmap.copy()  # 这里可以添加图像处理代码

            # 创建处理后的图像（processed_image）
            processed_scene = QGraphicsScene()

            # 缩放处理后的图像（保持比例）
            scaled_processed_pixmap = processed_pixmap.scaled(view_size, QtCore.Qt.KeepAspectRatio,
                                                              QtCore.Qt.SmoothTransformation)
            processed_image_item = QGraphicsPixmapItem(scaled_processed_pixmap)
            processed_scene.addItem(processed_image_item)

            # 清空当前的 QGraphicsScene
            if self.ui.processed_image.scene():
                self.ui.processed_image.scene().clear()  # 清空场景内容

            # 将新的处理后的图像设置到 processed_image QGraphicsView
            self.ui.processed_image.setScene(processed_scene)
            self.ui.processed_image.setRenderHint(QPainter.Antialiasing)  # 可选，启用抗锯齿效果

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

        # 设置窗口阴影效果
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)  # 创建阴影效果对象
        self.shadow.setOffset(0, 5)  # 设置阴影偏移量
        self.shadow.setBlurRadius(10)  # 设置阴影模糊度
        self.shadow.setColor(QtCore.Qt.black)  # 设置阴影颜色
        self.ui.MainFrame.setGraphicsEffect(self.shadow)  # 设置窗口阴影效果

        # 添加toolbutton点击事件，并初始化第一个按钮处于点击状态
        self.ui.AI.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.AI.setChecked(True)
        self.ui.SystemInfo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.Key.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        # 添加toolbutton点击事件，打开文件夹、开始运行、停止运行按钮
        self.ui.openFile.clicked.connect(self.open_images)

        # self.ui.image_listView.setViewMode(QListView.IconMode)
        # self.ui.image_listView.setIconSize(QSize(100, 100))
        # self.ui.image_listView.setSpacing(10)
        #
        # # 设置水平滚动条
        # self.ui.image_listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.ui.image_listView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        # # 强制单行显示
        # self.ui.image_listView.setWrapping(False)  # 禁止自动换行
        # self.ui.image_listView.setFlow(QListView.LeftToRight)  # 从左到右显示项目
        #
        # self.model = QStandardItemModel(self.ui.image_listView)
        # self.ui.image_listView.setModel(self.model)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
