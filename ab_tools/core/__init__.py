#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AB Tools 核心模块包

此模块提供核心功能组件，包括事件管理器等。

导出接口：
    - EventManager: 事件管理器类（单例模式）
    - get_event_manager(): 获取事件管理器实例的函数
    - subscribe(), unsubscribe(), emit(), register_event_type(): 快捷函数

使用示例：
    from ab_tools.core import EventManager, get_event_manager

    # 方式1：直接使用单例类
    manager = EventManager()
    manager.subscribe("ui_opened", my_callback)

    # 方式2：使用快捷函数
    from ab_tools.core import subscribe, emit
    subscribe("ui_opened", my_callback)
    emit("ui_opened", "main_window")

事件类型常量：
    UI_OPENED = "ui_opened"
    UI_CLOSED = "ui_closed"
    UI_UPDATED = "ui_updated"
    TOOL_EXECUTED = "tool_executed"
    TOOL_FAILED = "tool_failed"
    CONFIG_CHANGED = "config_changed"
    CONFIG_LOADED = "config_loaded"
    PLUGIN_INITIALIZED = "plugin_initialized"
    PLUGIN_SHUTDOWN = "plugin_shutdown"
"""

from .eventManager import (
    EventManager,
    get_event_manager,
    subscribe,
    unsubscribe,
    emit,
    register_event_type
)

# 事件类型常量（方便使用）
UI_OPENED = "ui_opened"
"""UI窗口打开事件"""
UI_CLOSED = "ui_closed"
"""UI窗口关闭事件"""
UI_UPDATED = "ui_updated"
"""UI内容更新事件"""
TOOL_EXECUTED = "tool_executed"
"""工具执行完成事件"""
TOOL_FAILED = "tool_failed"
"""工具执行失败事件"""
CONFIG_CHANGED = "config_changed"
"""配置发生变化事件"""
CONFIG_LOADED = "config_loaded"
"""配置加载完成事件"""
PLUGIN_INITIALIZED = "plugin_initialized"
"""插件初始化完成事件"""
PLUGIN_SHUTDOWN = "plugin_shutdown"
"""插件关闭事件"""

__all__ = [
    "EventManager",
    "get_event_manager",
    "subscribe",
    "unsubscribe",
    "emit",
    "register_event_type",
    "UI_OPENED",
    "UI_CLOSED",
    "UI_UPDATED",
    "TOOL_EXECUTED",
    "TOOL_FAILED",
    "CONFIG_CHANGED",
    "CONFIG_LOADED",
    "PLUGIN_INITIALIZED",
    "PLUGIN_SHUTDOWN"
]