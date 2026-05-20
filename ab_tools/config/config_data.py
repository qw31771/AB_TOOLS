# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds

# --- 1. 路径原材料 ---
FILE_PATH = os.path.abspath(__file__)
PACKAGE_DIR = os.path.dirname(os.path.dirname(FILE_PATH))
ROOT_DIR = os.path.dirname(PACKAGE_DIR)

PATH_ICONS = os.path.join(PACKAGE_DIR, "icons")
PATH_UI = os.path.join(PACKAGE_DIR, "ui")
PATH_TOOLS = os.path.join(ROOT_DIR, "tools")

# --- 2. 缩放转换加工厂 ---
try:
    SCALING = cmds.mayaDpiSetting(query=True, realScaleValue=True)
except:
    SCALING = 1.0

def get_px(value):
    """底层数值自适应转换逻辑"""
    return value * SCALING

def fetch_icon_path(name, default="pythonFamily.png"):
    """根据图标名返回绝对路径

    Args:
        name: str - 图标文件名（不含扩展名），如 "ab_base"
        default: str - 文件不存在时的默认图标

    Returns:
        str: 图标的绝对路径
    """
    path = os.path.join(PATH_ICONS, name + ".png")
    if os.path.exists(path):
        return path
    print(f"警告: 图标文件不存在 '{path}'，使用默认图标")
    return default