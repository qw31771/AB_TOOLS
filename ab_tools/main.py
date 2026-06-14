# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from . import config # 导入配置接口
from . import eventManager # 导入事件管理器



def setup_plugin():
    print("正在安装 AB Tools 插件...")

    # 触发插件初始化事件
    event_manager = eventManager.EventManager()
    event_manager.emit(eventManager.PLUGIN_INITIALIZED, "AB Tools Plugin")

    shelf_name = config.Name.Shelf_Name
    shlf_icon = config.Name.Shelf_Icon
    ann_show=config.Name.Title
    gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")

    # 删除旧工具架（开发阶段每次重建）
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name)

    # 创建工具架
    cmds.setParent(gShelfTopLevel)
    cmds.shelfLayout(shelf_name)
    cmds.shelfButton(
        image1=config.Ui.Shelf_Icon,
        ann=ann_show,
        command='import ab_tools; ab_tools.run()',
        annotation="点击打开AB Tools主界面",
    )
    # 白色分隔符
    cmds.shelfButton(
        image1=config.Ui.White,
        command="",
        annotation="",
    )

    # 删除旧图标按钮
    if cmds.iconTextButton(shlf_icon, ex=1, q=1):
        cmds.deleteUI(shlf_icon)

    # 创建图标按钮
    parent = cmds.iconTextButton("statusFieldButton", q=1, p=1)
    cmds.iconTextButton(shlf_icon,
        i=config.Ui.Menu_Icon,
        hi=config.Ui.Menu_Icon,
        ann=ann_show,
        command='import ab_tools; ab_tools.run()',
        p=parent
    )

    # 切换到当前工具架
    cmds.shelfTabLayout(gShelfTopLevel, edit=True, selectTab=shelf_name)

