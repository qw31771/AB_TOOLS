# -*- coding: utf-8 -*-
"""
事件管理器核心逻辑模块

职责：实现EventManager类的核心功能，包括事件注册、注销、触发等。
此文件仅包含逻辑实现，不直接对外提供接口。
对外接口统一由同一目录下的 __init__.py 提供。
"""

import threading
import logging
from typing import Any, Callable, Dict, List, Optional, Union

# 尝试导入Maya相关模块，用于在主线程中执行回调
try:
    import maya.utils
    MAYA_AVAILABLE = True
except ImportError:
    MAYA_AVAILABLE = False


class EventManager:
    """事件管理器类 - 单例模式实现"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._events: Dict[str, List[Callable]] = {}
        self._event_lock = threading.RLock()
        self._logger = logging.getLogger("ABTools.EventManager")

        # 信号字典初始为空，所有信号由 eventManager/__init__.py 在导入时注册
        self.EVENT_TYPES: Dict[str, str] = {}

        self._logger.debug("事件管理器初始化完成")

    def subscribe(self, event_type: str, callback: Callable) -> bool:
        """订阅事件"""
        if event_type not in self.EVENT_TYPES:
            raise ValueError(
                f"未定义的事件类型: {event_type}。"
                f"可用事件类型: {list(self.EVENT_TYPES.keys())}"
            )

        with self._event_lock:
            if event_type not in self._events:
                self._events[event_type] = []
            if callback not in self._events[event_type]:
                self._events[event_type].append(callback)
                self._logger.debug(f"事件 '{event_type}' 新增监听器: {callback.__name__}")
                return True
        return False

    def unsubscribe(self, event_type: str, callback: Callable) -> bool:
        """取消订阅事件"""
        with self._event_lock:
            if event_type in self._events and callback in self._events[event_type]:
                self._events[event_type].remove(callback)
                self._logger.debug(f"事件 '{event_type}' 移除监听器: {callback.__name__}")
                if not self._events[event_type]:
                    del self._events[event_type]
                return True
        return False

    def emit(self, event_type: str, *args, run_in_main_thread: bool = False, **kwargs) -> int:
        """触发事件"""
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
            callbacks = self._events[event_type].copy()

        for callback in callbacks:
            try:
                if run_in_main_thread and MAYA_AVAILABLE:
                    maya.utils.executeDeferred(
                        self._safe_execute_callback, callback, *args, **kwargs
                    )
                else:
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
        """安全执行回调函数"""
        try:
            callback(*args, **kwargs)
        except Exception as e:
            self._logger.error(
                f"回调函数 {callback.__name__} 执行出错: {str(e)}", exc_info=True
            )
            raise

    def get_event_types(self) -> Dict[str, str]:
        """获取所有已定义的事件类型及描述"""
        return self.EVENT_TYPES.copy()

    def get_listeners_count(self, event_type: Optional[str] = None) -> Union[int, Dict[str, int]]:
        """获取监听器数量"""
        with self._event_lock:
            if event_type is not None:
                return len(self._events.get(event_type, []))
            return {et: len(lst) for et, lst in self._events.items()}

    def clear_listeners(self, event_type: Optional[str] = None):
        """清理监听器"""
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
        """注册新的事件类型"""
        with self._event_lock:
            if event_type in self.EVENT_TYPES:
                self._logger.warning(f"事件类型 '{event_type}' 已存在，跳过注册")
                return False
            self.EVENT_TYPES[event_type] = description or f"自定义事件: {event_type}"
            self._logger.info(f"注册新事件类型: {event_type}")
            return True

    def is_event_type_registered(self, event_type: str) -> bool:
        """检查事件类型是否已注册"""
        return event_type in self.EVENT_TYPES