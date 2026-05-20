# -*- coding: utf-8 -*-
"""主窗口 — 负责窗口配置、子模块布局编排"""
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

        bg = config.Theme.BG_COLOR
        self.setStyleSheet(f"background-color: {bg};")

        self._sidebar = Sidebar(dock=self)
        self._sidebar.setStyleSheet(f"background-color: {bg};")
        self._sidebar.content.setStyleSheet(f"background-color: {bg};")

        content_layout = QtWidgets.QVBoxLayout(self._sidebar.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addStretch()

        self.setWidget(self._sidebar)


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
