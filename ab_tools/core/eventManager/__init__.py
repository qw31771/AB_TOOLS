# -*- coding: utf-8 -*-
"""
AB Tools 信号大厅 - 事件管理器对外接口

职责：集中定义、注册所有信号常量，提供快捷调用接口。
设计：manager.py 为纯引擎（观察者模式），此文件为信号定义中心。

工作流程：
    1. 导入时自动执行 _register_all_signals()
    2. 将所有信号常量注册到管理器
    3. 业务代码直接使用 eventManager.常量 即可

使用方式：
    from ab_tools import eventManager

    # 订阅（监听）
    eventManager.subscribe(eventManager.UI_OPENED, on_ui_open)

    # 触发（发送）
    eventManager.emit(eventManager.UI_OPENED, "main_window")
"""

from .manager import EventManager

# 全局单例实例
_event_manager_instance = None


def get_event_manager() -> EventManager:
    """获取事件管理器单例实例"""
    global _event_manager_instance
    if _event_manager_instance is None:
        _event_manager_instance = EventManager()
    return _event_manager_instance


# ============================================================
# 快捷函数
# ============================================================

def subscribe(event_type: str, callback: callable) -> bool:
    """订阅事件"""
    return get_event_manager().subscribe(event_type, callback)


def unsubscribe(event_type: str, callback: callable) -> bool:
    """取消订阅事件"""
    return get_event_manager().unsubscribe(event_type, callback)


def emit(event_type: str, *args, run_in_main_thread: bool = False, **kwargs) -> int:
    """触发事件"""
    return get_event_manager().emit(event_type, *args, run_in_main_thread=run_in_main_thread, **kwargs)


def register_event_type(event_type: str, description: str = "") -> bool:
    """注册新的事件类型（标准接口）"""
    return get_event_manager().register_event_type(event_type, description)


def register(event_type: str, description: str = "") -> bool:
    """注册新的事件类型（简短别名）"""
    return get_event_manager().register_event_type(event_type, description)


# ============================================================
# 信号常量定义 ── 集中在此文件管理，新增信号只需在此添加
# ============================================================
# 命名规范：全大写 + snake_case

# --- UI 信号 ---
UI_OPENED = "ui_opened"
"""UI窗口打开事件"""
UI_CLOSED = "ui_closed"
"""UI窗口关闭事件"""
UI_UPDATED = "ui_updated"
"""UI内容更新事件"""

# --- 工具信号 ---
TOOL_EXECUTED = "tool_executed"
"""工具执行完成事件"""
TOOL_FAILED = "tool_failed"
"""工具执行失败事件"""

# --- 配置信号 ---
CONFIG_CHANGED = "config_changed"
"""配置发生变化事件"""
CONFIG_LOADED = "config_loaded"
"""配置加载完成事件"""

# --- 插件生命周期信号 ---
PLUGIN_INITIALIZED = "plugin_initialized"
"""插件初始化完成事件"""
PLUGIN_SHUTDOWN = "plugin_shutdown"
"""插件关闭事件"""


# ============================================================
# 自动注册 ── 将上述信号注册到管理器，业务代码无需关心注册逻辑
# ============================================================

_SIGNAL_REGISTRY = {
    # UI
    UI_OPENED: "UI窗口打开事件",
    UI_CLOSED: "UI窗口关闭事件",
    UI_UPDATED: "UI内容更新事件",
    # 工具
    TOOL_EXECUTED: "工具执行完成事件",
    TOOL_FAILED: "工具执行失败事件",
    # 配置
    CONFIG_CHANGED: "配置发生变化事件",
    CONFIG_LOADED: "配置加载完成事件",
    # 插件生命周期
    PLUGIN_INITIALIZED: "插件初始化完成事件",
    PLUGIN_SHUTDOWN: "插件关闭事件",
}


def _register_all_signals():
    """将所有信号注册到事件管理器"""
    em = get_event_manager()
    for sig_type, desc in _SIGNAL_REGISTRY.items():
        em.register_event_type(sig_type, desc)


# 导入时自动注册，确保在业务代码使用前信号已就绪
_register_all_signals()


__all__ = [
    "EventManager",
    "get_event_manager",
    "subscribe",
    "unsubscribe",
    "emit",
    "register_event_type",
    "register",
    # 信号常量
    "UI_OPENED",
    "UI_CLOSED",
    "UI_UPDATED",
    "TOOL_EXECUTED",
    "TOOL_FAILED",
    "CONFIG_CHANGED",
    "CONFIG_LOADED",
    "PLUGIN_INITIALIZED",
    "PLUGIN_SHUTDOWN",
]