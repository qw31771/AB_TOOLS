# -*- coding: utf-8 -*-
import os
from PySide2.QtWidgets import QApplication
from .path import Path

# --- 1. 路径（从 path 模块统一引用） ---
PATH_ICONS = Path.ICONS
PATH_UI = Path.UI
PATH_TOOLS = Path.TOOLS
PATH_PREFS = Path.PREFS

# --- 2. 缩放转换（基于屏幕分辨率） ---
_SCALING = None


def _detect_scaling():
    """从屏幕 DPI 计算缩放比（96 = 基准）"""
    global _SCALING
    if _SCALING is not None:
        return _SCALING
    try:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            _SCALING = screen.logicalDotsPerInch() / 96.0
        else:
            _SCALING = 1.0
    except:
        _SCALING = 1.0
    return _SCALING


def get_px(value, scope=None, key=None):
    """DPI 自适应转换

    get_px(32)                         → DPI 值
    get_px(250, "window", "top")       → 查 preferences，无则 DPI 默认
    """
    default = value * _detect_scaling()
    if scope and key:
        try:
            from ..core.preferences import get
        except ImportError:
            return default
        saved = get(scope, key)
        if saved is not None:
            return saved
    return default


def fetch_icon_path(name, default="pythonFamily.png"):
    """根据图标名返回绝对路径"""
    path = os.path.join(PATH_ICONS, name + ".png")
    if os.path.exists(path):
        return path
    print(f"警告: 图标文件不存在 '{path}'，使用默认图标")
    return default
