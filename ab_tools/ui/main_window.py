# -*- coding: utf-8 -*-
"""主窗口 — 负责窗口配置、内容区管理与布局编排"""
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from .. import config
from .sub_ui.statusbar import StatusBar
from . import sub_ui


def _maya_main_window():
    """获取 Maya 主窗口"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


class ABToolsWindow(QtWidgets.QDockWidget):

    def __init__(self, parent=None):
        super(ABToolsWindow, self).__init__(parent)
        self.setWindowTitle(config.Name.TITLE)
        self.setObjectName(config.Name.OBJECT_NAME)
        self.setMinimumWidth(config.MainWindow.MIN_WIDTH)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            f"QDockWidget {{ padding: 0px; margin: 0px; }}"
            f"QDockWidget::title {{ padding: 0px; margin: 0px; }}")
        # 中央容器 [内容区 | 侧边栏]
        central = QtWidgets.QWidget()
        central.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        central.setContentsMargins(0, 0, 0, 0)
        central.setStyleSheet(
            f"background-color: {config.MainWindow.BG_COLOR};"
            f"margin: 0px; padding: 0px;")
        self.setWidget(central)

        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 内容区
        self._content = QtWidgets.QWidget()
        self._content.setStyleSheet(
            f"background-color: {config.MainWindow.BG_COLOR};")
        content_layout = QtWidgets.QVBoxLayout(self._content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 顶部图标横幅
        banner = QtWidgets.QLabel()
        banner_h = int(config.MainWindow.BANNER_HEIGHT)
        banner.setFixedHeight(banner_h)
        banner.setMinimumWidth(config.MainWindow.MIN_WIDTH)
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        banner.setMargin(0)
        banner.setScaledContents(True)
        banner.setAlignment(QtCore.Qt.AlignCenter)
        icon_path = config.get_icon(config.Name.BANNER)
        pixmap = QtGui.QPixmap(icon_path)
        if not pixmap.isNull():
            banner.setPixmap(pixmap)
        content_layout.addWidget(banner)

        # 上下可拉伸分割区
        self._splitter_init()
        content_layout.addWidget(self._splitter, 1)

        # 底部状态栏
        content_layout.addWidget(StatusBar().widget)

        layout.addWidget(self._content, 1)

        # 右侧侧边栏
        self._sidebar = sub_ui.Sidebar(dock=self, content=self._content)
        layout.addWidget(self._sidebar)

    def _splitter_init(self):
        self._splitter  = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self._splitter.setHandleWidth(config.MainWindow.SPLITTER_HANDLE_WIDTH)
        self._splitter.setStyleSheet(
            f"QSplitter::handle {{"
            f"  background-color: {config.MainWindow.SPLITTER_HANDLE};"
            f"}}")

        top = QtWidgets.QWidget()
        top.setMinimumSize(0, 0)
        top.setStyleSheet(f"background-color: {config.MainWindow.TOP_BG_COLOR};")
        self._splitter.addWidget(top)

        bottom = QtWidgets.QWidget()
        bottom.setMinimumSize(0, 0)
        bottom.setStyleSheet(f"background-color: {config.MainWindow.BOTTOM_BG_COLOR};")
        self._splitter.addWidget(bottom)

        self._splitter.setChildrenCollapsible(True)
        self._splitter.splitterMoved.connect(
            lambda: config.save_splitter_sizes(self._splitter.sizes()))

        sizes = [
            config.MainWindow.SPLITTER_TOP,
            config.MainWindow.SPLITTER_BOTTOM,
        ]

        self._splitter.setSizes(sizes)

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
