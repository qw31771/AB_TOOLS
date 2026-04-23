# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import maya.mel as mel
from .ui import show # 导入UI显示函数
from .config import Config # 导入配置接口
from . import eventManager # 导入事件管理器




def setup_plugin():
    print("正在初始化 AB Tools 插件...")

    # 触发插件初始化事件
    event_manager = eventManager.EventManager()
    event_manager.emit(eventManager.PLUGIN_INITIALIZED, "AB Tools Plugin")

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

# 全局变量防止UI被销毁
_ui_instance = None

def run():
    """直接显示UI的函数，供外部调用"""
    global _ui_instance
    _ui_instance = show()

    # 触发UI打开事件
    event_manager = eventManager.EventManager()
    event_manager.emit(eventManager.UI_OPENED, "main_window")

