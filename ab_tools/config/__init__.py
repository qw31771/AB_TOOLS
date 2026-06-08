# -*- coding: utf-8 -*-
from . import config_data


class Name:
    """通用名称常量"""
    TITLE: str = "AB Tools"
    OBJECT_NAME: str = "ABToolsWorkspaceControl"
    SHELF_NAME: str = "AB_TOOLS"
    SHELF_ICON: str = "AB_TOOLS_ICONS"
    BANNER: str = "ab_title"

class UI:
    """图标资源"""
    SHELF_iCON = config_data.fetch_icon_path('ab_shelf_base')
    SHELF_iCON_HiGH = config_data.fetch_icon_path('ab_shelf_base')
    MENU_ICON = config_data.fetch_icon_path('ab_base')
    MENU_ICON_HIGH = config_data.fetch_icon_path('ab_high')
    _WHITE = config_data.fetch_icon_path('white_separator1')

class General:
    """通用尺寸（工具架 / 分隔符）"""
    BTN: float = config_data.get_px(32)    # 按钮尺寸
    CELL: float = config_data.get_px(34)   # 工具架单元格
    SEP: float = config_data.get_px(2)     # 分隔符宽度


class MainWindow:
    """主窗口 (main_window.py)"""
    # 偏好 scope/key
    PREFS_SCOPE: str = "window"
    KEY_SPLITTER_TOP: str = "splitter_top"
    KEY_SPLITTER_BOTTOM: str = "splitter_bottom"

    MIN_WIDTH: float = config_data.get_px(310)                      # 窗口最小宽度
    BANNER_HEIGHT: float = config_data.get_px(80)                   # 顶部图标栏高度
    BANNER_PADDING: float = config_data.get_px(0)                   # 图标栏内边距
    FOOTER_HEIGHT: float = config_data.get_px(50)                   # 底部栏高度
    FOOTER_TEXT: str = "rgb(200, 200, 200)"                         # 底部文字色
    SPLITTER_HANDLE: str = "rgb(196, 196, 196)"                     # 分割条颜色
    SPLITTER_HANDLE_WIDTH: float = config_data.get_px(5)            # 分割条宽度
    SPLITTER_TOP = config_data.get_px(250, PREFS_SCOPE, KEY_SPLITTER_TOP)       # 上方面板高度
    SPLITTER_BOTTOM = config_data.get_px(250, PREFS_SCOPE, KEY_SPLITTER_BOTTOM) # 下方面板高度
    FOOTER_FONT_SIZE: float = config_data.get_px(15)                # 底部文字大小
    FOOTER_BORDER: str = "rgb(218, 189, 163)"                       # 底部描边色
    BG_COLOR: str = "rgb(34, 34, 34)"                               # 背景色
    TOP_BG_COLOR: str = "rgb(34, 34, 34)"                               # 上半背景色
    BOTTOM_BG_COLOR: str = "rgb(70, 70, 70)"                               # 下半背景色


class Sidebar:
    """侧边栏 (sidebar.py)"""
    GRAB_WIDTH: float = config_data.get_px(3)          # 抓取条宽度
    COLLAPSED_WIDTH: float = config_data.get_px(10)    # 收起态宽度
    BG_COLOR: str = "rgb(255, 144, 41)"                # 正常态背景
    COLLAPSED_BG_COLOR: str = "rgb(255, 85, 18)"       # 收起态背景


class ToolPanel:
    """工具面板 (tool_panel.py)"""
    TOOL_ROW_H: float = config_data.get_px(22)     # 工具项行高
    CATEGORY_ROW_H: float = config_data.get_px(44) # 分类项行高
    BG: str = "rgb(200, 200, 200)"                 # 面板背景
    TEXT: str = "rgb(34, 34, 34)"                  # 文字色
    SELECTED_BG: str = "rgb(160, 160, 160)"        # 工具项选中
    CATEGORY_BG: str = "rgb(200, 200, 200)"        # 分类未选中背景
    CATEGORY_SELECTED_BG: str = "rgb(255, 255, 255)"  # 分类选中背景
    CATEGORY_TEXT: str = "rgb(34, 34, 34)"         # 分类文字色


class Menu:
    """右键菜单 (共用)"""
    BG: str = "rgb(200, 200, 200)"          # 菜单背景
    TEXT: str = "rgb(34, 34, 34)"           # 文字色
    HOVER_BG: str = "rgb(160, 160, 160)"    # 悬停高亮





def px(value: float) -> float:
    """DPI 自适应缩放"""
    return config_data.get_px(value)


def get_icon(name: str) -> str:
    """获取图标绝对路径"""
    return config_data.fetch_icon_path(name)


def save_splitter_sizes(sizes: list):
    """保存分割条尺寸"""
    from .. import preferences
    preferences.set(MainWindow.PREFS_SCOPE, MainWindow.KEY_SPLITTER_TOP, sizes[0])
    preferences.set(MainWindow.PREFS_SCOPE, MainWindow.KEY_SPLITTER_BOTTOM, sizes[1])


def save_splitter_sizes(sizes: list):
    """保存分割条尺寸"""
    from .. import preferences
    preferences.set(MainWindow.PREFS_SCOPE, MainWindow.KEY_SPLITTER_TOP, sizes[0])
    preferences.set(MainWindow.PREFS_SCOPE, MainWindow.KEY_SPLITTER_BOTTOM, sizes[1])
