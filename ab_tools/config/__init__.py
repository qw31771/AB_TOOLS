# -*- coding: utf-8 -*-
from .import config_data

class Config:
    """
    AB Tools 配置接口
    """

    # --- 名称数据 (str) ---
    TITLE: str = "AB Tools"
    """[名称] 插件官方显示名称"""
    OBJECT_NAME: str = "ABToolsWorkspaceControl"
    """[名称] Maya UI 唯一识别标识符"""

    # --- 路径数据 (str) ---
    """[路径] 图标资源目录"""
    Icons: str = config_data.PATH_ICONS
    
    UI: str = config_data.PATH_UI
    """[路径] UI脚本目录"""
    
    Tools: str = config_data.PATH_TOOLS
    """[路径] 工具脚本目录"""

    # --- 尺寸数据 (float) ---
    
    BTN_SIZE: float = config_data.get_px(32)
    """[尺寸] 按钮像素值"""
    
    SHELF_CELL: float = config_data.get_px(34)
    """[尺寸] 工具架单元格像素值"""
    
    SEP_WIDTH: float = config_data.get_px(2)
    """[尺寸] 隔离符宽度像素值"""


    
    # --- 核心接口 ---

    @staticmethod
    def px(value: float) -> float:
        """[函数] 执行自适应缩放计算"""
        return config_data.get_px(value)

    @staticmethod
    def get_icon(name: str) -> str:
        """[函数] 获取图标绝对路径 ('base'/'hover')"""
        return config_data.fetch_icon_path(name)

