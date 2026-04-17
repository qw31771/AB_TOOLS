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

def fetch_icon_path(name):
    """底层路径拼接逻辑"""
    mapping = {
        "ab_shelf_base": os.path.join(PATH_ICONS, "ab_shelf_base.png"),
        "ab_shelf_hover": os.path.join(PATH_ICONS, "ab_shelf_hover.png")
        # "ab_hover": os.path.join(PATH_ICONS, "abin_hover.png")
        # "ab_hover": os.path.join(PATH_ICONS, "abin_hover.png")

    }
    return mapping.get(name, "pythonFamily.png")