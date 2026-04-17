# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import maya.mel as mel
from .ui import main_window # 导入UI模块
from .config import Config # 导入配置接口


# 全局变量防止UI被销毁
_ui_instance = None

def run_main_ui():
    """触发UI显示的包装函数"""
    global _ui_instance
    _ui_instance = main_window.show_plugin_ui()

def create_shelf():
    """创建工具架和按钮"""
    shelf_name = "AB_TOOLS"
    gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")
    
    if cmds.shelfLayout(shelf_name, exists=True):
        for child in cmds.shelfLayout(shelf_name, query=True, childArray=True) or []:
            cmds.deleteUI(child)
    else:
        cmds.setParent(gShelfTopLevel)
        cmds.shelfLayout(shelf_name)
        
    cmds.setParent(shelf_name)
    # 按钮逻辑：调用本模块的 run_main_ui
    cmds.shelfButton(
        label="AB Tools",
        # style="iconOnly", 
        image1=Config.get_icon("ab_shelf_base"),
        # highlightImage=Config.get_icon("ab_shelf_hover"),
        command="import ab_tools.main as abm; abm.run_main_ui()",
        annotation="点击打开AB Tools主界面"
    )
    cmds.separator(style='single', width=12,height=32)



def setup_plugin():
    """自启动逻辑入口"""
    create_shelf()
    # 如果需要在Maya启动时自动弹出UI，可以取消下行注释
    # run_main_ui()