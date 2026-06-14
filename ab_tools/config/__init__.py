# -*- coding: utf-8 -*-
from . import config_data
'''
素材库:https://www.iconfont.cn/collections/detail?spm=a313x.collections_index.i1.d9df05512.12483a81bSrPeP&cid=51865
'''

class Name:
    """通用名称"""
    Title: str = "AB Tools"
    Object_Name: str = "ABToolsWorkspaceControl"
    Shelf_Name: str = "AB_TOOLS"
    Shelf_Icon: str = "AB_TOOLS_ICONS"
    Banner: str = "ab_title"


class Ui:
    """图标资源"""
    Shelf_Icon = config_data.fetch_icon_path('ab_shelf_base')
    Shelf_Icon_High = config_data.fetch_icon_path('ab_shelf_base')
    Menu_Icon = config_data.fetch_icon_path('ab_base')
    Menu_Icon_High = config_data.fetch_icon_path('ab_high')
    White = config_data.fetch_icon_path('white_separator1')


class General:
    """通用尺寸"""
    Btn: float = config_data.get_px(32)
    Cell: float = config_data.get_px(34)
    Sep: float = config_data.get_px(2)


class Main_Window:
    """主窗口 (main_window.py)"""
    Prefs_Scope: str = "window"                    # 偏好存储域
    Min_Width: float = config_data.get_px(310)     # 窗口最小宽度
    Bg_Color: str = "rgb(34, 34, 34)"              # 背景色


class Top_Panel:
    """上方面板 (top_panel.py)"""
    Bg_Color: str = "rgb(34, 34, 34)"              # 面板背景
    Folder_Bg_Color: str = "rgb(0, 0, 0)"       # 文件夹项背景
    Folder_Text_Color: str = "rgb(173, 173, 173)"     # 文件夹项文字色
    Folder_Height: float = config_data.get_px(30)      # 文件夹项高度
    Folder_Font_Size: float = config_data.get_px(18)   # 文件夹项字体大小
    Folder_Padding: float = config_data.get_px(10)       # 文件夹项内边距
    Folder_Spacing: float = config_data.get_px(2)       # 文件夹项间距
    Folder_Selected_Bg_Color: str = "rgb(190, 98, 178)"   # 文件夹项选中背景
    Folder_Selected_Text_Color: str = "rgb(255, 255, 255)" # 文件夹项选中文字色
    Script_Bg_Color: str = "rgb(80, 80, 80)"            # 脚本项背景
    Script_Text_Color: str = "rgb(121, 243, 237)"       # 脚本项文字色
    Script_Height: float = config_data.get_px(25)       # 脚本项高度
    Script_Font_Size: float = config_data.get_px(16)    # 脚本项字体大小
    Scroll_Handle_Color: str = "rgb(100, 100, 100)"        # 滚动条滑块色
    Scroll_Bg_Color: str = "rgb(199, 199, 199)"               # 滚动条背景色
    Scroll_Width: float = config_data.get_px(8)              # 滚动条宽度
    Scroll_Handle_Min_Height: float = config_data.get_px(20) # 滑块最小高度


class Bottom_Panel:
    """下方面板 (bottom_panel.py)"""
    Bg_Color: str = "rgb(73, 73, 73)"              # 面板背景


class Banner:
    """横幅 (main_window.py)"""
    Height: float = config_data.get_px(80)          # 横幅高度


class Splitter:
    """分割条 (main_window.py)"""
    Key_Top: str = "splitter_top"                       # 上方面板记忆键
    Key_Bottom: str = "splitter_bottom"                 # 下方面板记忆键
    Handle_Bg_Color: str = "rgb(196, 196, 196)"        # 分割条颜色
    Handle_Width: float = config_data.get_px(5)         # 分割条宽度
    Top = config_data.get_px(250)                       # 上方默认高度
    Bottom = config_data.get_px(250)                    # 下方默认高度


class Footer:
    """底部状态栏 (statusbar.py)"""
    Height: float = config_data.get_px(50)              # 底部栏高度
    Text_Color: str = "rgb(200, 200, 200)"              # 底部文字色
    Font_Size: float = config_data.get_px(15)           # 底部字体大小
    Border_Color: str = "rgb(182, 182, 182)"            # 底部描边色


class Menu_Bar:
    """菜单栏 (menu_bar.py)"""
    Height: float = config_data.get_px(30)         # 菜单栏高度
    Btn_Size: float = config_data.get_px(20)       # 按钮尺寸
    Bg_Color: str = "rgb(223, 223, 223)"           # 灰白背景
    Border_Color: str = "black"                    # 黑色描边
    Btn_Color: str = "rgb(34, 34, 34)"             # 按钮文字色


class Image_Button:
    """图片按钮 (imageBtn.py)"""
    Opacity_Normal: float = 0.7       # 正常态透明度
    Opacity_Hover: float = 1.0        # 悬停态透明度
    Opacity_Pressed: float = 0.3      # 按下态透明度


class Side_Bar:
    """侧边栏 (sidebar.py)"""
    Grab_Width: float = config_data.get_px(3)          # 抓取条宽度
    Collapsed_Width: float = config_data.get_px(10)    # 收起态宽度
    Bg_Color: str = "rgb(255, 144, 41)"                # 正常态背景
    Collapsed_Bg_Color: str = "rgb(255, 85, 18)"       # 收起态背景


class Context_Menu:
    """右键菜单 (共用)"""
    Bg_Color: str = "rgb(61, 61, 61)"          # 菜单背景
    Text_Color: str = "rgb(255, 255, 255)"           # 文字色
    Hover_Bg_Color: str = "rgb(190, 98, 178)"    # 悬停高亮


def px(value: float) -> float:
    """DPI 自适应缩放"""
    return config_data.get_px(value)


def get_icon(name: str) -> str:
    """获取图标绝对路径"""
    return config_data.fetch_icon_path(name)


def load_splitter_sizes():
    """加载分割条尺寸（记忆优先，无则默认）"""
    from .. import preferences
    top = preferences.get(Main_Window.Prefs_Scope, Splitter.Key_Top)
    bot = preferences.get(Main_Window.Prefs_Scope, Splitter.Key_Bottom)
    if top is not None and bot is not None:
        return [int(top), int(bot)]
    return [int(Splitter.Top), int(Splitter.Bottom)]


def save_splitter_sizes(sizes: list):
    """保存分割条尺寸"""
    from .. import preferences
    preferences.set(Main_Window.Prefs_Scope, Splitter.Key_Top, sizes[0])
    preferences.set(Main_Window.Prefs_Scope, Splitter.Key_Bottom, sizes[1])
