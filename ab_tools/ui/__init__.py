# -*- coding: utf-8 -*-
from . import main_window
from . import AbWidgets


def show():
    """显示停靠在 Maya 右侧的主窗口

    Returns:
        ABToolsWindow: 窗口实例
    """
    window = main_window.show_main_ui()
    if window is not None:
        from .. import eventManager
        eventManager.emit(eventManager.UI_OPENED, "main_window")
    return window
