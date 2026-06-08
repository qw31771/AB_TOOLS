# -*- coding: utf-8 -*-
"""全局状态栏单例 — 自建底部控件，管理状态文字和进度条"""
from PySide2 import QtWidgets, QtCore
from ... import config


class StatusBar:
    """全局状态栏（单例）

    自动创建底部控件，调用 .widget 获取 QWidget 加入布局。
    通过 set_status / set_progress 更新。
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._build()
        return cls._instance

    # ---- 构建 ----

    def _build(self):
        w = QtWidgets.QWidget()
        w.setFixedHeight(int(config.MainWindow.FOOTER_HEIGHT))
        w.setStyleSheet(
            f"background-color: {config.MainWindow.BG_COLOR};"
            f"color: {config.MainWindow.FOOTER_TEXT};"
            f"border-top: 1px solid {config.MainWindow.FOOTER_BORDER};")

        layout = QtWidgets.QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._label = QtWidgets.QLabel("·············")
        self._label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self._label.setStyleSheet(
            f"font-size: {int(config.MainWindow.FOOTER_FONT_SIZE)}px;"
            f"font-weight: bold;")
        layout.addWidget(self._label)

        self._bar = QtWidgets.QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        layout.addWidget(self._bar)

        self._widget = w

    # ---- 公开 ----

    @property
    def widget(self):
        """获取状态栏 QWidget，供 main_window 加入布局"""
        return self._widget

    def set_status(self, text: str):
        """设置状态文字"""
        self._label.setText(str(text))

    def set_progress(self, value: int):
        """设置进度值 (0-100)"""
        self._bar.setValue(max(0, min(100, int(value))))
