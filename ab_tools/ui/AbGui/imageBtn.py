from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ImageButton(QPushButton):
    def __init__(self, size, url, tips="",parent=None):
        """
        初始化 ImageButton。

        :param size: 按钮的大小（宽度和高度相同）
        :param url: PNG 图片的路径
        :param parent: 父控件
        """
        super().__init__(parent)
        self.setIcon(QIcon(url))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")  # 去除边框并设置背景透明
        self.setToolTip(tips)  # 设置提示文本
        self._pressed = False
        self._hovered = False  # 新增属性，用于跟踪鼠标是否悬停

    def paintEvent(self, event):
        """
        重写 paintEvent 以实现自定义绘制，包括按下和悬停效果。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 获取当前图标
        icon = self.icon()
        if icon.isNull():
            return

        # 开始绘制图标
        painter.save()
        
        # 根据状态调整透明度
        if self._pressed:
            painter.setOpacity(0.3)  # 按下时半透明
        elif self._hovered:
            painter.setOpacity(1.0)  # 悬停时半透明
        else:
            painter.setOpacity(0.7)   # 正常状态不透明

        # 绘制图标
        icon.paint(painter, self.rect(), Qt.AlignCenter)
        
        painter.restore()

    def mousePressEvent(self, event):
        """
        处理鼠标按下事件。
        """
        self._pressed = True
        self.update()  # 触发重绘
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        处理鼠标释放事件。
        """
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """
        处理鼠标进入按钮区域事件。
        """
        self._hovered = True
        self.update()  # 触发重绘
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        处理鼠标离开按钮区域事件。
        """
        self._hovered = False
        self.update()
        super().leaveEvent(event)