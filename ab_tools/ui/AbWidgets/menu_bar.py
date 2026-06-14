# -*- coding: utf-8 -*-
"""菜单栏 — 横幅下方工具栏，放置信息/设置等功能按钮"""
from PySide2 import QtWidgets, QtCore
from ... import config
from .. import AbGui


class MenuBar(QtWidgets.QWidget):
    """顶部菜单栏，内含 AbGui.ImageButton 占位按钮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setFixedHeight(int(config.Menu_Bar.Height))
        self.setStyleSheet(
            f"background-color: {config.Menu_Bar.Bg_Color};"
            f"border: 1px solid {config.Menu_Bar.Border_Color};")

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(6)
        layout.addStretch()

        s = int(config.Menu_Bar.Btn_Size)
        help_btn = AbGui.ImageButton(s, config.get_icon("帮助"), "帮助")
        set_btn = AbGui.ImageButton(s, config.get_icon("设置"), "设置")
        layout.addWidget(help_btn)
        layout.addWidget(set_btn)
