# -*- coding: utf-8 -*-
"""
AB Tools 插件根接口

职责：
    1. 聚合核心模块（eventManager等），提供简便根接口调用
    2. 提供插件初始化（init）和运行（run）入口

使用方式：
    # 事件管理（推荐方式）
    from ab_tools import eventManager
    eventManager.subscribe("ui_opened", handler)
    eventManager.emit(eventManager.UI_OPENED, "main_window")

    # 插件生命周期
    from ab_tools import init, run
    init()  # 初始化工具架和按钮
    run()   # 显示UI界面
"""

from .core import eventManager  # 将eventManager提升到根接口


def init():
    """插件启动入口，负责初始化工具架和按钮"""
    from . import reloadTools
    reloadTools.reload_all()
    from . import main
    main.setup_plugin()


def run():
    """显示UI主窗口"""
    from . import reloadTools
    reloadTools.reload_all()
    from . import ui
    ui.show()


__all__ = [
    "eventManager",
    "init",
    "run",
]