# -*- coding: utf-8 -*-
"""
核心模块统一入口

职责：将各子模块（eventManager等）接口聚合，方便外部一键调用。
设计：此文件只做结构导入，不包含任何逻辑运算。

使用方式：
    # 外部调用
    from ab_tools import eventManager
    eventManager.subscribe("ui_opened", handler)
    eventManager.emit(eventManager.UI_OPENED, "main_window")

扩展：后续在 core/ 下新增模块时，在此添加一行导入即可。
    例：新增 logger 模块 →
        from . import logger
        __all__ = ["eventManager", "logger"]
"""

from . import eventManager
from . import preferences

__all__ = ["eventManager", "preferences"]