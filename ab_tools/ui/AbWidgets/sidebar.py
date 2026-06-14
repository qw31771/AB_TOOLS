# -*- coding: utf-8 -*-
"""右侧侧边栏 — 窄条控件，点击折叠/展开主窗口"""
from PySide2 import QtWidgets, QtCore
from ... import config


class Sidebar(QtWidgets.QWidget):
    """右侧侧边栏 = 一条可点击的窄条

    挂在主窗口右侧，点击切换折叠/展开。不管理任何内容，只控制 dock 宽度。
    """

    _GRAB_WIDTH = config.Side_Bar.Grab_Width

    def __init__(self, parent=None, dock=None, content=None):
        super().__init__(parent)
        self._dock = dock
        self._content = content
        self._collapsed = False
        self._normal_width = config.Main_Window.Min_Width

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setFixedWidth(self._GRAB_WIDTH)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("点击缩小窗口")
        self.setStyleSheet(f"background-color: {config.Side_Bar.Bg_Color};")

    # ---- 公开 ----

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
        self.hide()
        if self._content:
            self._content.hide()
        self.setFixedWidth(config.Side_Bar.Collapsed_Width)
        self.setStyleSheet(f"background-color: {config.Side_Bar.Collapsed_Bg_Color};")
        if self._dock:
            self._dock.setFixedWidth(config.Side_Bar.Collapsed_Width)
        self.setToolTip("点击还原窗口")
        self._collapsed = True
        self.show()

    def expand(self):
        if not self._collapsed:
            return
        self.hide()
        if self._dock:
            self._dock.setMinimumWidth(config.Main_Window.Min_Width)
            self._dock.setMaximumWidth(16777215)
            self._dock.resize(self._normal_width, self._dock.height())
        if self._content:
            self._content.show()
        self.setFixedWidth(self._GRAB_WIDTH)
        self.setStyleSheet(f"background-color: {config.Side_Bar.Bg_Color};")
        self.setToolTip("点击缩小窗口")
        self._collapsed = False
        self.show()

    # ---- 交互 ----

    def mousePressEvent(self, event):
        self.toggle()

    def enterEvent(self, event):
        if not self._collapsed:
            self.setFixedWidth(self._GRAB_WIDTH * 2)
            self.setStyleSheet(f"background-color: {config.Side_Bar.Collapsed_Bg_Color};")

    def leaveEvent(self, event):
        if not self._collapsed:
            self.setFixedWidth(self._GRAB_WIDTH)
            self.setStyleSheet(f"background-color: {config.Side_Bar.Bg_Color};")
