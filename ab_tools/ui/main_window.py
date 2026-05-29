# -*- coding: utf-8 -*-
"""主窗口 — 负责窗口配置、内容区管理与布局编排"""
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from .. import config
from .sidebar import Sidebar


def _maya_main_window():
    """获取 Maya 主窗口"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


class ABToolsWindow(QtWidgets.QDockWidget):

    def __init__(self, parent=None):
        super(ABToolsWindow, self).__init__(parent)
        self.setWindowTitle(config.Name.TITLE)
        self.setObjectName(config.Name.OBJECT_NAME)
        self.setMinimumWidth(config.Size.WINDOW_MIN_WIDTH)
        # 中央容器 [内容区 | 侧边栏]
        central = QtWidgets.QWidget()
        central.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        central.setStyleSheet(
            f"background-color: {config.Theme.MAIN_BG_COLOR};")
        self.setWidget(central)

        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 内容区
        self._content = QtWidgets.QWidget()
        self._content.setStyleSheet(
            f"background-color: {config.Theme.MAIN_BG_COLOR};")
        content_layout = QtWidgets.QVBoxLayout(self._content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addStretch()
        layout.addWidget(self._content, 1)

        # 右侧侧边栏
        self._sidebar = Sidebar(dock=self, content=self._content)
        layout.addWidget(self._sidebar)


def show_main_ui():
    """创建并停靠到 Maya 右侧

    Returns:
        ABToolsWindow: 窗口实例
    """
    maya_win = _maya_main_window()

    old = maya_win.findChild(QtWidgets.QDockWidget, config.Name.OBJECT_NAME)
    if old is not None:
        maya_win.removeDockWidget(old)
        old.deleteLater()

    ui = ABToolsWindow(parent=maya_win)
    maya_win.addDockWidget(QtCore.Qt.RightDockWidgetArea, ui)
    ui.show()
    return ui
