from PyQt5 import QtWidgets, QtCore


## 主窗口阴影效果
def shadow_fun(obj):
    # 设置窗口阴影效果
    shadow = QtWidgets.QGraphicsDropShadowEffect(obj)  # 创建阴影效果对象
    shadow.setOffset(0, 5)  # 设置阴影偏移量
    shadow.setBlurRadius(10)  # 设置阴影模糊度
    shadow.setColor(QtCore.Qt.black)  # 设置阴影颜色
    obj.ui.MainFrame.setGraphicsEffect(shadow)  # 设置窗口阴影效果