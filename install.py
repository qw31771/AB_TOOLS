# -*- coding: utf-8 -*-
import os
import sys
import maya.cmds as cmds

def onMayaDroppedPythonFile(*args, **kwargs):
    """
    Maya 拖拽安装入口函数
    """
    # 获取当前 install.py 所在的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 将插件根目录添加到 Maya 的环境变量中 (如果不存在的话)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # 导入插件并执行初始化动作
    try:
        import ab_tools
        import importlib
        importlib.reload(ab_tools)  # 保证每次拖拽都能热更新，方便开发
        
        # 触发初始化
        ab_tools.startup()
        
        # 提示用户安装成功
        cmds.inViewMessage(amg="<hl>AB Tools</hl> 安装成功！请点击上方AB_TOOLS工具架按钮。", pos='bottomCenter', fade=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        cmds.warning(f"AB Tools 安装失败，请查看脚本编辑器获取详细信息: {e}")