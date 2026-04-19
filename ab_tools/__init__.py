from . import main
import importlib
importlib.reload(main)

def init():
    """插件启动入口，负责初始化工具架和按钮"""
    main.setup_plugin()