# -*- coding: utf-8 -*-
"""AB Tools 偏好存储 - 模块化 JSON 持久存储

每个 scope 对应一个独立的 JSON 文件，互不干扰。

使用方式:
    from ab_tools import preferences

    # scope 对象风格（推荐，读写同一个 scope 时更高效）
    win = preferences.scope("window")
    win.set("collapsed", True)
    win.get("collapsed")          # True
    win.all()                     # {"collapsed": True, ...}

    # 快捷函数风格
    preferences.set("window", "collapsed", True)
    preferences.get("window", "collapsed")  # True

    # 新增 scope 无需任何配置，直接使用即可
    preferences.set("exporter", "path", "D:/output")
"""
from ...config.path import Path
from .manager import PreferencesManager

_manager = PreferencesManager(Path.PREFS)


# ============================================================
# 公开 API
# ============================================================

def scope(name: str):
    """获取指定 scope 的偏好对象

    Args:
        name: str - scope 名称，对应 {name}.json 文件
            例: "window" → prefs/window.json

    Returns:
        ScopePrefs: 该 scope 的数据容器，支持 get/set/remove/all/clear
    """
    return _manager.scope(name)


def get(scope: str, key: str, default=None):
    """快捷读取偏好值

    Args:
        scope: str - scope 名称
        key: str - 键名
        default: 任意 - 键不存在时的默认值

    Returns:
        对应值或 default
    """
    return _manager.get(scope, key, default)


def set(scope: str, key: str, value):
    """快捷写入偏好值（自动保存）

    Args:
        scope: str - scope 名称
        key: str - 键名
        value: 任意可 JSON 序列化的值
    """
    _manager.set(scope, key, value)


def remove(scope: str, key: str):
    """快捷删除偏好值

    Args:
        scope: str - scope 名称
        key: str - 键名
    """
    _manager.remove(scope, key)


__all__ = [
    "PreferencesManager",
    "scope",
    "get",
    "set",
    "remove",
]
