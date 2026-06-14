# -*- coding: utf-8 -*-
"""下方面板 — 占位"""
from PySide2 import QtWidgets, QtCore
from .. import config


class Bottom_Panel(QtWidgets.QWidget):
    """下半面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setMinimumSize(0, 0)
        self.setStyleSheet(
            f"background-color: {config.Bottom_Panel.Bg_Color};")
