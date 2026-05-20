# -*- coding: utf-8 -*-
from . import config_data


class Name:
    """名称常量"""
    TITLE: str = "AB Tools"
    OBJECT_NAME: str = "ABToolsWorkspaceControl"
    SHELF_NAME: str = "AB_TOOLS"
    SHELF_ICON: str = "AB_TOOLS_ICONS"


class Path:
    """资源路径"""
    ICONS: str = config_data.PATH_ICONS
    UI: str = config_data.PATH_UI
    TOOLS: str = config_data.PATH_TOOLS


class Size:
    """像素尺寸（已做 DPI 自适应）"""
    BTN: float = config_data.get_px(32)
    SHELF_CELL: float = config_data.get_px(34)
    SEP: float = config_data.get_px(2)
    WINDOW_MIN_WIDTH: float = config_data.get_px(300)
    COLLAPSED_WIDTH: float = config_data.get_px(8)
    GRAB_WIDTH: float = config_data.get_px(5)

class Theme:
    """样式常量 — 颜色统一使用 rgb() 格式，便于灵活调色"""
    BG_COLOR: str = "rgb(30, 30, 30)"


class UI:
    SHELF_iCON = config_data.fetch_icon_path('ab_shelf_base')
    SHELF_iCON_HiGH = config_data.fetch_icon_path('ab_shelf_base')
    MENU_ICON = config_data.fetch_icon_path('ab_base')
    MENU_ICON_HIGH = config_data.fetch_icon_path('ab_high')
    _WHITE = config_data.fetch_icon_path('white_separator1')

def px(value: float) -> float:
    """DPI 自适应缩放"""
    return config_data.get_px(value)


def get_icon(name: str) -> str:
    """获取图标绝对路径"""
    return config_data.fetch_icon_path(name)
