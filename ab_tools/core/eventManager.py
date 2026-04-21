#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AB Tools 事件管理器模块 - 观察者模式实现

功能：提供统一的事件管理机制，所有自定义信号的注册、触发都要通过此模块
设计：单例模式，确保全局只有一个事件管理器实例

使用示例：
    # 导入事件管理器
    from ab_tools.core import EventManager

    # 获取单例实例
    event_manager = EventManager()

    # 定义事件处理函数
    def on_ui_opened(ui_name, timestamp):
        print(f"UI {ui_name} 在 {timestamp} 打开")

    # 注册事件监听器
    event_manager.subscribe("ui_opened", on_ui_opened)

    # 触发事件
    event_manager.emit("ui_opened", "main_window", "2024-01-01 10:00:00")

    # 注销事件监听器
    event_manager.unsubscribe("ui_opened", on_ui_opened)

事件命名规范：
    - 使用 snake_case 命名
    - 前缀表示模块或功能域，如：ui_, tool_, config_
    - 动词使用过去式表示已完成动作，如：opened, closed, updated
    - 动词使用现在进行时表示正在进行的动作，如：opening, closing, updating
"""

import threading
import logging
from typing import Any, Callable, Dict, List, Optional, Union

# 尝试导入Maya相关模块，用于在主线程中执行回调
try:
    import maya.utils
    MAYA_AVAILABLE = True
except ImportError:
    maya = None
    MAYA_AVAILABLE = False


class EventManager:
    """
    事件管理器类 - 单例模式实现

    职责：
    1. 统一管理所有自定义事件
    2. 提供事件注册、注销、触发接口
    3. 确保事件处理的线程安全
    4. 支持在主线程中执行UI相关回调
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EventManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """初始化事件管理器内部状态"""
        self._events: Dict[str, List[Callable]] = {}
        self._event_lock = threading.RLock()  # 可重入锁，支持嵌套调用
        self._logger = logging.getLogger("ABTools.EventManager")

        # 预定义的事件类型（可根据需要扩展）
        self.EVENT_TYPES = {
            # UI相关事件
            "ui_opened": "UI窗口打开事件",
            "ui_closed": "UI窗口关闭事件",
            "ui_updated": "UI内容更新事件",

            # 工具相关事件
            "tool_executed": "工具执行完成事件",
            "tool_failed": "工具执行失败事件",

            # 配置相关事件
            "config_changed": "配置发生变化事件",
            "config_loaded": "配置加载完成事件",

            # 系统相关事件
            "plugin_initialized": "插件初始化完成事件",
            "plugin_shutdown": "插件关闭事件",
        }

        self._logger.debug("事件管理器初始化完成")

    def subscribe(self, event_type: str, callback: Callable) -> bool:
        """
        订阅事件

        参数：
            event_type: str - 事件类型，必须是已定义的事件类型
            callback: Callable - 事件处理函数，接收事件参数

        返回：
            bool - 订阅是否成功

        异常：
            ValueError - 当event_type未定义时抛出
        """
        if event_type not in self.EVENT_TYPES:
            raise ValueError(
                f"未定义的事件类型: {event_type}。"
                f"可用事件类型: {list(self.EVENT_TYPES.keys())}"
            )

        with self._event_lock:
            if event_type not in self._events:
                self._events[event_type] = []

            # 避免重复注册
            if callback not in self._events[event_type]:
                self._events[event_type].append(callback)
                self._logger.debug(f"事件 '{event_type}' 新增监听器: {callback.__name__}")
                return True

        return False

    def unsubscribe(self, event_type: str, callback: Callable) -> bool:
        """
        取消订阅事件

        参数：
            event_type: str - 事件类型
            callback: Callable - 要移除的事件处理函数

        返回：
            bool - 是否成功移除
        """
        with self._event_lock:
            if event_type in self._events and callback in self._events[event_type]:
                self._events[event_type].remove(callback)
                self._logger.debug(f"事件 '{event_type}' 移除监听器: {callback.__name__}")

                # 如果没有监听器了，清理空列表
                if not self._events[event_type]:
                    del self._events[event_type]

                return True

        return False

    def emit(self, event_type: str, *args, run_in_main_thread: bool = False, **kwargs) -> int:
        """
        触发事件

        参数：
            event_type: str - 要触发的事件类型
            *args: Any - 传递给监听器的位置参数
            run_in_main_thread: bool - 是否在主线程中执行回调（仅Maya环境有效）
            **kwargs: Any - 传递给监听器的关键字参数

        返回：
            int - 成功执行的回调函数数量

        异常：
            ValueError - 当event_type未定义时抛出
        """
        if event_type not in self.EVENT_TYPES:
            raise ValueError(
                f"未定义的事件类型: {event_type}。"
                f"可用事件类型: {list(self.EVENT_TYPES.keys())}"
            )

        executed_count = 0

        with self._event_lock:
            if event_type not in self._events:
                self._logger.debug(f"事件 '{event_type}' 没有监听器")
                return 0

            callbacks = self._events[event_type].copy()  # 复制列表，避免在迭代时修改

        # 执行所有回调
        for callback in callbacks:
            try:
                if run_in_main_thread and MAYA_AVAILABLE:
                    # 在Maya主线程中异步执行
                    maya.utils.executeDeferred(
                        self._safe_execute_callback,
                        callback,
                        *args,
                        **kwargs
                    )
                else:
                    # 直接执行
                    self._safe_execute_callback(callback, *args, **kwargs)

                executed_count += 1

            except Exception as e:
                self._logger.error(
                    f"执行事件 '{event_type}' 的回调 {callback.__name__} 时出错: {str(e)}",
                    exc_info=True
                )

        self._logger.debug(f"事件 '{event_type}' 触发完成，执行了 {executed_count} 个回调")
        return executed_count

    def _safe_execute_callback(self, callback: Callable, *args, **kwargs):
        """安全执行回调函数，捕获异常并记录日志"""
        try:
            callback(*args, **kwargs)
        except Exception as e:
            self._logger.error(
                f"回调函数 {callback.__name__} 执行出错: {str(e)}",
                exc_info=True
            )
            raise

    def get_event_types(self) -> Dict[str, str]:
        """
        获取所有已定义的事件类型及其描述

        返回：
            Dict[str, str] - 事件类型到描述的映射
        """
        return self.EVENT_TYPES.copy()

    def get_listeners_count(self, event_type: Optional[str] = None) -> Union[int, Dict[str, int]]:
        """
        获取监听器数量

        参数：
            event_type: Optional[str] - 指定事件类型，为None时返回所有事件类型的统计

        返回：
            Union[int, Dict[str, int]] - 监听器数量或统计字典
        """
        with self._event_lock:
            if event_type is not None:
                return len(self._events.get(event_type, []))
            else:
                return {et: len(listeners) for et, listeners in self._events.items()}

    def clear_listeners(self, event_type: Optional[str] = None):
        """
        清理监听器

        参数：
            event_type: Optional[str] - 指定事件类型，为None时清理所有事件类型的监听器
        """
        with self._event_lock:
            if event_type is not None:
                if event_type in self._events:
                    self._events[event_type].clear()
                    del self._events[event_type]
                    self._logger.debug(f"清理事件 '{event_type}' 的所有监听器")
            else:
                self._events.clear()
                self._logger.debug("清理所有事件监听器")

    def register_event_type(self, event_type: str, description: str = "") -> bool:
        """
        注册新的事件类型

        参数：
            event_type: str - 事件类型名称
            description: str - 事件类型描述

        返回：
            bool - 注册是否成功（如果已存在则返回False）
        """
        with self._event_lock:
            if event_type in self.EVENT_TYPES:
                self._logger.warning(f"事件类型 '{event_type}' 已存在，跳过注册")
                return False

            self.EVENT_TYPES[event_type] = description or f"自定义事件: {event_type}"
            self._logger.info(f"注册新事件类型: {event_type} - {self.EVENT_TYPES[event_type]}")
            return True

    def is_event_type_registered(self, event_type: str) -> bool:
        """
        检查事件类型是否已注册

        参数：
            event_type: str - 要检查的事件类型

        返回：
            bool - 是否已注册
        """
        return event_type in self.EVENT_TYPES


# 创建全局单例实例
_event_manager_instance = None


def get_event_manager() -> EventManager:
    """
    获取事件管理器单例实例（推荐使用此函数）

    返回：
        EventManager - 事件管理器单例实例
    """
    global _event_manager_instance
    if _event_manager_instance is None:
        _event_manager_instance = EventManager()
    return _event_manager_instance


def subscribe(event_type: str, callback: Callable) -> bool:
    """快捷函数：订阅事件"""
    return get_event_manager().subscribe(event_type, callback)


def unsubscribe(event_type: str, callback: Callable) -> bool:
    """快捷函数：取消订阅事件"""
    return get_event_manager().unsubscribe(event_type, callback)


def emit(event_type: str, *args, run_in_main_thread: bool = False, **kwargs) -> int:
    """快捷函数：触发事件"""
    return get_event_manager().emit(event_type, *args, run_in_main_thread=run_in_main_thread, **kwargs)


def register_event_type(event_type: str, description: str = "") -> bool:
    """快捷函数：注册新事件类型"""
    return get_event_manager().register_event_type(event_type, description)