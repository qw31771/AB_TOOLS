# -*- coding: utf-8 -*-
"""左侧折叠侧边栏控件 — 封装抓取条与折叠/展开交互"""
from PySide2 import QtWidgets, QtCore
from .. import config


class _GrabBar(QtWidgets.QWidget):
    """左侧抓取条 — 显示 hover 样式，点击发出信号"""

    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(config.Size.GRAB_WIDTH)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("点击缩小窗口")
        self.setStyleSheet("background: transparent;")
        self._hover_on = True

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        if self._hover_on:
            self.setStyleSheet("background: #3a3a3a;")

    def leaveEvent(self, event):
        if self._hover_on:
            self.setStyleSheet("background: transparent;")

    def set_mode(self, collapsed):
        """切换折叠/展开模式，控制 hover 样式和提示文字"""
        self._hover_on = not collapsed
        self.setToolTip("点击还原窗口" if collapsed else "点击缩小窗口")
        self.setStyleSheet("background: transparent;")


class Sidebar(QtWidgets.QWidget):
    """折叠侧边栏 = [抓取条 | 内容区]

    由主窗口创建并传入 dock 引用，自动管理折叠/展开与窗口宽度。
    """

    def __init__(self, parent=None, dock=None):
        super().__init__(parent)
        self._dock = dock
        self._collapsed = False
        self._normal_width = config.Size.WINDOW_MIN_WIDTH

        self._grab = _GrabBar()
        self._grab.clicked.connect(self._on_grab_click)

        self._content = QtWidgets.QWidget()

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._grab)
        layout.addWidget(self._content)

        self.installEventFilter(self)

    # ---- 公开接口 ----

    @property
    def content(self):
        """内容区 QWidget — 外部通过此属性添加业务控件"""
        return self._content

    @property
    def is_collapsed(self):
        return self._collapsed

    def toggle(self):
        self.expand() if self._collapsed else self.collapse()

    def collapse(self):
        if self._collapsed:
            return
        if self._dock:
            self._normal_width = self._dock.width()
        self._content.hide()
        if self._dock:
            self._dock.setFixedWidth(config.Size.COLLAPSED_WIDTH)
        self._grab.set_mode(True)
        for child in self.findChildren(QtWidgets.QWidget):
            child.installEventFilter(self)
        self._collapsed = True

    def expand(self):
        if not self._collapsed:
            return
        self._content.show()
        if self._dock:
            self._dock.setMinimumWidth(config.Size.WINDOW_MIN_WIDTH)
            self._dock.setMaximumWidth(16777215)
            self._dock.resize(self._normal_width, self._dock.height())
        self._grab.set_mode(False)
        for child in self.findChildren(QtWidgets.QWidget):
            child.removeEventFilter(self)
        self._collapsed = False

    # ---- 内部 ----

    def _on_grab_click(self):
        self.toggle()

    def eventFilter(self, obj, event):
        if self._collapsed and event.type() == QtCore.QEvent.MouseButtonPress:
            self.expand()
            return True
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if self._collapsed:
            self.expand()
            event.accept()
            return
        super().mousePressEvent(event)
