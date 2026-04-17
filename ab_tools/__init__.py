from . import main
import importlib

def startup():
    """
    插件启动入口，负责调用 main.py 中的相关逻辑
    """
    # 开发期间保持模块重载，确保修改 main.py 后重新拖拽可立即生效
    importlib.reload(main)
    main.setup_plugin()