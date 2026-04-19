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

def setup_plugin():
    print("正在初始化 AB Tools 插件...")
    shelf_name = Config.SHELF_NAME
    gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")
    
    """创建工具架和按钮"""
    if not cmds.shelfLayout(shelf_name, exists=True):
        cmds.setParent(gShelfTopLevel)
        cmds.shelfLayout(shelf_name)

        cmds.shelfButton(
            image1=Config.get_icon("ab_shelf_base"),
            # highlightImage=Config.get_icon("ab_shelf_hover"),
            ann=Config.TITLE,
            command='import ab_tools; ab_tools.run()',
            annotation="点击打开AB Tools主界面",
        )
        cmds.separator(style='single', width=12,height=32)


    """创建图标"""
    if  (cmds.iconTextButton( Config.SHELF_IONS,ex=1,q=1)):
        cmds.deleteUI(Config.SHELF_IONS)

    parent=cmds.iconTextButton("statusFieldButton",q=1,p=1)
    # 添加菜单按钮 iconTextButton
    cmds.iconTextButton(Config.SHELF_IONS,
        i=Config.get_icon("ab_base"),
        hi=Config.get_icon("ab_hover"),
        ann=Config.TITLE,
        command='import ab_tools; ab_tools.run()',
        p=parent
    )

def run():
    """直接显示UI的函数，供外部调用"""
    run_main_ui()

